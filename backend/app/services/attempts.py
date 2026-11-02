"""Timed mock exam engine (PDF 5.3). The server owns the timer: `deadline_at` is the only source of truth."""

import uuid
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.audit import track
from app.core.errors import AppError, not_found
from app.db import utcnow
from app.jobs.queue import enqueue
from app.models import (
    Attempt,
    AttemptAnswer,
    Exam,
    ExamBlueprint,
    Paper,
    Question,
    QuestionTranslation,
    Report,
    SeenQuestion,
    Topic,
    User,
)
from app.services import credits, memory, papers, scoring
from app.services.profile import require_complete_profile

ANTI_CHEAT_EVENTS = {
    "tab_switch", "window_blur", "fullscreen_exit", "copy_attempt", "paste_attempt", "right_click",
    "screenshot_attempt", "app_background", "network_offline", "network_online",
}
MAX_EVENTS = 500


def _blueprint(db: Session, attempt_or_paper) -> ExamBlueprint:
    paper = attempt_or_paper if isinstance(attempt_or_paper, Paper) else db.get(Paper, attempt_or_paper.paper_id)
    return db.scalar(select(ExamBlueprint).where(ExamBlueprint.exam_id == paper.exam_id,
                                                 ExamBlueprint.version == paper.blueprint_version))


def _own_attempt(db: Session, user: User, attempt_id: uuid.UUID, lock: bool = False) -> Attempt:
    stmt = select(Attempt).where(Attempt.id == attempt_id, Attempt.user_id == user.id)
    if lock:
        stmt = stmt.with_for_update()
    a = db.scalar(stmt)
    if a is None:
        raise not_found("Attempt")
    return a


def remaining_seconds(a: Attempt) -> int:
    if a.status != "in_progress":
        return 0
    return max(0, int((a.deadline_at - utcnow()).total_seconds()))


def start_attempt(db: Session, user: User, exam_id: uuid.UUID, language: str) -> tuple[Attempt, bool]:
    """Returns (attempt, resumed). Starting the same exam while one is in progress resumes it (no second charge)."""
    require_complete_profile(db, user)
    exam = db.get(Exam, exam_id)
    if exam is None or exam.status != "published":
        raise not_found("Exam")
    blueprint = papers.current_blueprint(db, exam)
    if language not in blueprint.languages:
        raise AppError(422, "language_not_available", f"This exam is available in: {', '.join(blueprint.languages)}")

    open_attempt = db.scalar(select(Attempt).where(Attempt.user_id == user.id, Attempt.exam_id == exam.id,
                                                   Attempt.status == "in_progress"))
    if open_attempt is not None:
        if _expire_if_due(db, open_attempt):
            open_attempt = None
        else:
            return open_attempt, True

    paper = papers.pick_paper(db, exam, user.id)
    attempt_id = uuid.uuid4()
    free = exam.is_free_trial and db.scalar(
        select(Attempt.id).where(Attempt.user_id == user.id, Attempt.is_free_trial.is_(True)).limit(1)) is None
    ledger = None if free else credits.consume(db, user, exam.credits_required, "attempt", attempt_id)

    now = utcnow()
    attempt = Attempt(id=attempt_id, user_id=user.id, exam_id=exam.id, paper_id=paper.id, language=language,
                      started_at=now, deadline_at=now + timedelta(minutes=blueprint.duration_min),
                      status="in_progress", is_free_trial=free, credit_ledger_id=ledger.id if ledger else None,
                      anti_cheat_events=[])
    db.add(attempt)
    paper.status = "assigned"
    qids = [uuid.UUID(i["question_id"]) for i in paper.items]
    already_seen = set(db.scalars(select(SeenQuestion.question_id).where(
        SeenQuestion.user_id == user.id, SeenQuestion.question_id.in_(qids))))
    for item in paper.items:
        qid = uuid.UUID(item["question_id"])
        attempt.answers.append(AttemptAnswer(question_id=qid, seq=item["seq"], section_key=item["section_key"]))
        if qid not in already_seen:
            db.add(SeenQuestion(user_id=user.id, question_id=qid))
    for q in db.scalars(select(Question).where(Question.id.in_(qids))):
        q.times_served = (q.times_served or 0) + 1
    papers.ensure_translations(db, qids, language)
    track(db, user.id, "attempt_start", exam_id=str(exam.id), free_trial=free, language=language)
    db.commit()
    return attempt, False


def _localized(q: Question, tr: QuestionTranslation | None) -> dict:
    if tr is not None and tr.review_status in ("back_translation_ok", "approved"):
        return {"language": tr.language, "text": tr.text, "options": tr.options}
    return {"language": "en", "text": q.text, "options": q.options}


def attempt_state(db: Session, user: User, attempt_id: uuid.UUID, language: str | None = None) -> dict:
    """The paper: questions without answers, server end time and saved answers. `language` switches the paper
    language for this view (e.g. ?lang=hi); English is always included for the in-exam toggle."""
    a = _own_attempt(db, user, attempt_id)
    _expire_if_due(db, a)
    exam = db.get(Exam, a.exam_id)
    blueprint = _blueprint(db, a)
    lang = language or a.language
    if lang not in blueprint.languages:
        raise AppError(422, "language_not_available", f"This exam is available in: {', '.join(blueprint.languages)}")
    qids = [x.question_id for x in a.answers]
    qs = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(qids)))}
    trs = {}
    if lang != "en":
        papers.ensure_translations(db, qids, lang)
        db.commit()
        trs = {t.question_id: t for t in db.scalars(select(QuestionTranslation).where(
            QuestionTranslation.question_id.in_(qids), QuestionTranslation.language == lang))}
    questions = []
    for ans in sorted(a.answers, key=lambda x: x.seq):
        q = qs[ans.question_id]
        content = _localized(q, trs.get(q.id))
        questions.append({
            "seq": ans.seq, "question_id": q.id, "section_key": ans.section_key, "type": q.type,
            "content": content,
            # English copy for the in-exam language toggle (PDF 5.3); omitted when the content is already English.
            "content_en": None if content["language"] == "en" else {"language": "en", "text": q.text, "options": q.options},
            "answer": ans.answer, "marked_for_review": ans.marked_for_review, "visited": ans.visited,
            "time_spent_sec": ans.time_spent_sec, "client_rev": ans.client_rev,
        })
    return {
        "id": a.id, "exam": {"id": exam.id, "name": exam.name, "slug": exam.slug}, "status": a.status,
        "language": lang, "is_free_trial": a.is_free_trial, "server_time": utcnow(),
        "started_at": a.started_at, "deadline_at": a.deadline_at, "remaining_seconds": remaining_seconds(a),
        "submitted_at": a.submitted_at,
        "rules": {
            "duration_min": blueprint.duration_min, "calculator_allowed": blueprint.calculator_allowed,
            "section_switching_allowed": blueprint.section_switching_allowed, "instructions": blueprint.instructions,
            "sections": [{"key": s["key"], "name": s.get("name", s["key"]), "question_count": s["question_count"],
                          "marks_per_question": s["marks_per_question"], "negative_marks": s.get("negative_marks", 0),
                          "duration_min": s.get("duration_min")} for s in blueprint.sections],
            "languages": blueprint.languages,
        },
        "questions": questions,
    }


def _validate_answer(q: Question, value):
    if value is None:
        return None
    keys = {o["key"] for o in q.options}
    if q.type == "single":
        if not isinstance(value, str) or value not in keys:
            raise AppError(422, "invalid_answer", f"Question {q.id}: choose one of {sorted(keys)}")
        return value
    if q.type == "multi":
        if not isinstance(value, list) or not value or not set(value) <= keys:
            raise AppError(422, "invalid_answer", f"Question {q.id}: choose one or more of {sorted(keys)}")
        return sorted(set(value))
    try:
        return float(value)
    except (TypeError, ValueError):
        raise AppError(422, "invalid_answer", f"Question {q.id}: enter a number")


def save_answers(db: Session, user: User, attempt_id: uuid.UUID, items: list[dict]) -> dict:
    """Batched, idempotent autosave. Each item carries a client_rev; older or repeated revisions are ignored, so
    retries and out-of-order deliveries from a flaky network can never overwrite newer answers."""
    a = _own_attempt(db, user, attempt_id, lock=True)
    if a.status != "in_progress":
        raise AppError(409, "attempt_closed", "This attempt has already been submitted")
    grace = timedelta(seconds=get_settings().attempt_grace_seconds)
    if utcnow() > a.deadline_at + grace:
        _expire_if_due(db, a)
        raise AppError(409, "deadline_passed", "Time is up. Your exam was submitted automatically.")
    by_q = {x.question_id: x for x in a.answers}
    qs = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(list(by_q))))}
    saved = ignored = 0
    for it in items:
        ans = by_q.get(it["question_id"])
        if ans is None:
            raise AppError(422, "unknown_question", f"Question {it['question_id']} is not part of this attempt")
        if it["client_rev"] <= ans.client_rev:
            ignored += 1
            continue
        if "answer" in it:
            value = _validate_answer(qs[ans.question_id], it["answer"])
            ans.answer = None if value is None else {"value": value}
        if it.get("marked_for_review") is not None:
            ans.marked_for_review = it["marked_for_review"]
        if it.get("visited") is not None:
            ans.visited = it["visited"]
        if it.get("time_spent_sec") is not None:
            # Time can only grow; cap at the exam duration to ignore broken client clocks.
            cap = int((a.deadline_at - a.started_at).total_seconds())
            ans.time_spent_sec = min(max(ans.time_spent_sec, int(it["time_spent_sec"])), cap)
        ans.client_rev = it["client_rev"]
        saved += 1
    db.commit()
    return {"saved": saved, "ignored_stale": ignored, "remaining_seconds": remaining_seconds(a), "server_time": utcnow()}


def log_events(db: Session, user: User, attempt_id: uuid.UUID, events: list[dict]) -> dict:
    """Light anti-cheat (PDF 5.3): events are logged and shown in the report, never punished."""
    a = _own_attempt(db, user, attempt_id, lock=True)
    if a.status != "in_progress":
        raise AppError(409, "attempt_closed", "This attempt has already been submitted")
    current = list(a.anti_cheat_events or [])
    for e in events:
        if e["type"] not in ANTI_CHEAT_EVENTS:
            raise AppError(422, "invalid_event", f"Unknown event type {e['type']}")
        if e["type"] == "tab_switch":
            a.tab_switch_count += 1
        if len(current) < MAX_EVENTS:
            current.append({"type": e["type"], "at": (e.get("at") or utcnow()).isoformat(),
                            "meta": e.get("meta") or {}})
    a.anti_cheat_events = current
    db.commit()
    return {"tab_switch_count": a.tab_switch_count, "events_logged": len(current)}


def _expire_if_due(db: Session, a: Attempt) -> bool:
    if a.status == "in_progress" and utcnow() > a.deadline_at + timedelta(seconds=get_settings().attempt_grace_seconds):
        finalize(db, a, "timeout")
        return True
    return False


def submit(db: Session, user: User, attempt_id: uuid.UUID) -> Attempt:
    a = _own_attempt(db, user, attempt_id, lock=True)
    if a.status == "in_progress":
        finalize(db, a, "user")
    return a


def finalize(db: Session, a: Attempt, reason: str) -> None:
    """Submit + score + memory update + queue the AI report. Safe to call twice (idempotent on status)."""
    if a.status != "in_progress":
        return
    now = utcnow()
    a.submitted_at = min(now, a.deadline_at) if reason == "timeout" else now
    a.submit_reason = reason
    a.status = "submitted"
    analytics = score_attempt(db, a)
    report = Report(user_id=a.user_id, kind="exam", attempt_id=a.id, status="processing",
                    language=db.get(User, a.user_id).preferred_language or a.language, analytics=analytics)
    db.add(report)
    track(db, a.user_id, "submit", attempt_id=str(a.id), reason=reason, score=a.score)
    db.commit()
    enqueue("generate_exam_report", report_id=report.id)


def score_attempt(db: Session, a: Attempt) -> dict:
    blueprint = _blueprint(db, a)
    qids = [x.question_id for x in a.answers]
    qs = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(qids)))}
    topics = {t.id: t.name for t in db.scalars(select(Topic).where(Topic.exam_id == a.exam_id))}
    items = []
    for ans in sorted(a.answers, key=lambda x: x.seq):
        q = qs[ans.question_id]
        items.append({
            "ref": ans.seq, "question_id": q.id, "section_key": ans.section_key, "topic_id": q.topic_id,
            "topic_name": topics.get(q.topic_id, "General"), "type": q.type, "difficulty": q.difficulty,
            "expected_time_sec": q.expected_time_sec, "correct": q.correct_answer["value"], "answer": ans.answer,
            "time_spent_sec": ans.time_spent_sec, "marked_for_review": ans.marked_for_review,
        })
    result = scoring.analyse(items, blueprint.sections, blueprint.marking_scheme or {})

    by_ref = {r["ref"]: r for r in result["questions"]}
    for ans in a.answers:
        r = by_ref[ans.seq]
        ans.is_correct = r["status"] == "correct"
        ans.marks_awarded = r["marks"]
        q = qs[ans.question_id]
        if r["status"] != "unanswered":
            q.times_answered = (q.times_answered or 0) + 1
            q.times_correct = (q.times_correct or 0) + (1 if r["status"] == "correct" else 0)
            q.accuracy_rate = round(q.times_correct / q.times_answered, 4)

    others = list(db.scalars(select(Attempt.score).where(
        Attempt.exam_id == a.exam_id, Attempt.status == "scored", Attempt.id != a.id, Attempt.score.is_not(None))))
    a.score, a.max_score = result["score"], result["max_score"]
    a.percentile = scoring.percentile(a.score, others)
    a.status = "scored"
    result["percentile"] = a.percentile
    result["percentile_population"] = len(others)
    result["anti_cheat"] = {"tab_switch_count": a.tab_switch_count,
                            "events": len(a.anti_cheat_events or []),
                            "by_type": _count_types(a.anti_cheat_events or [])}
    prev = db.execute(select(Attempt.score, Attempt.max_score).where(
        Attempt.user_id == a.user_id, Attempt.exam_id == a.exam_id, Attempt.status == "scored", Attempt.id != a.id)
        .order_by(Attempt.submitted_at.desc()).limit(5)).all()
    result["previous_scores"] = [{"score": s, "max_score": m} for s, m in prev]
    result["since_last_attempt"] = since_last_attempt(db, a, result)
    memory.update_after_scoring(db, a, [
        {"question_id": uuid.UUID(r["question_id"]), "topic_id": qs[uuid.UUID(r["question_id"])].topic_id,
         "status": r["status"], "error_type": r["error_type"]} for r in result["questions"]
    ])
    return result


def since_last_attempt(db: Session, a: Attempt, now: dict) -> dict | None:
    """Numbers for "since your last attempt" (memory module): score, accuracy, percentile and per-topic accuracy
    change versus the user's previous scored attempt of the same exam. None on a first attempt."""
    prev = db.scalar(select(Attempt).where(
        Attempt.user_id == a.user_id, Attempt.exam_id == a.exam_id, Attempt.status == "scored", Attempt.id != a.id)
        .order_by(Attempt.submitted_at.desc()).limit(1))
    if prev is None:
        return None
    prev_report = db.scalar(select(Report).where(Report.attempt_id == prev.id))
    before = {t["name"]: t["accuracy"] for t in ((prev_report.analytics or {}).get("topics", []) if prev_report else [])}
    prev_acc = (prev_report.analytics or {}).get("accuracy") if prev_report else None

    def delta(x, y):
        return None if x is None or y is None else round(x - y, 4)

    topics = [{"topic": t["name"], "before": before.get(t["name"]), "now": t["accuracy"],
               "change": delta(t["accuracy"], before.get(t["name"]))} for t in now["topics"] if t["name"] in before]
    topics.sort(key=lambda t: (t["change"] is None, -(t["change"] or 0)))
    return {"previous_attempt_id": str(prev.id), "previous_date": prev.submitted_at.isoformat() if prev.submitted_at else None,
            "score_before": prev.score, "score_now": now["score"], "score_change": delta(now["score"], prev.score),
            "accuracy_before": prev_acc, "accuracy_now": now["accuracy"], "accuracy_change": delta(now["accuracy"], prev_acc),
            "percentile_before": prev.percentile, "topics": topics,
            "improved_topics": [t["topic"] for t in topics if (t["change"] or 0) > 0],
            "declined_topics": [t["topic"] for t in topics if (t["change"] or 0) < 0]}


def _count_types(events: list[dict]) -> dict:
    out: dict[str, int] = {}
    for e in events:
        out[e["type"]] = out.get(e["type"], 0) + 1
    return out


def auto_submit_expired(db: Session) -> int:
    grace = timedelta(seconds=get_settings().attempt_grace_seconds)
    due = db.scalars(select(Attempt).where(Attempt.status == "in_progress", Attempt.deadline_at < utcnow() - grace)
                     .limit(200)).all()
    for a in due:
        finalize(db, a, "timeout")
    return len(due)


def review(db: Session, user: User, attempt_id: uuid.UUID, language: str | None) -> dict:
    """Question-by-question review with the correct answer and step-by-step explanation (after submission only)."""
    a = _own_attempt(db, user, attempt_id)
    if a.status == "in_progress":
        raise AppError(409, "attempt_in_progress", "The review is available after you submit")
    lang = language or a.language
    qids = [x.question_id for x in a.answers]
    qs = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(qids)))}
    trs = {t.question_id: t for t in db.scalars(select(QuestionTranslation).where(
        QuestionTranslation.question_id.in_(qids), QuestionTranslation.language == lang))} if lang != "en" else {}
    topics = {t.id: t.name for t in db.scalars(select(Topic).where(Topic.exam_id == a.exam_id))}
    out = []
    for ans in sorted(a.answers, key=lambda x: x.seq):
        q = qs[ans.question_id]
        tr = trs.get(q.id)
        use_tr = tr is not None and tr.review_status in ("back_translation_ok", "approved")
        out.append({
            "seq": ans.seq, "question_id": q.id, "section_key": ans.section_key, "topic": topics.get(q.topic_id),
            "type": q.type, "difficulty": q.difficulty, "language": lang if use_tr else "en",
            "text": tr.text if use_tr else q.text, "options": tr.options if use_tr else q.options,
            "explanation": tr.explanation if use_tr else q.explanation,
            "shortcut": tr.shortcut if use_tr else q.shortcut,
            "correct_answer": q.correct_answer["value"], "your_answer": (ans.answer or {}).get("value"),
            "is_correct": ans.is_correct, "marks_awarded": ans.marks_awarded, "time_spent_sec": ans.time_spent_sec,
            "expected_time_sec": q.expected_time_sec, "marked_for_review": ans.marked_for_review,
        })
    return {"attempt_id": a.id, "score": a.score, "max_score": a.max_score, "percentile": a.percentile, "questions": out}


def list_attempts(db: Session, user: User, limit: int, offset: int) -> tuple[list, int]:
    from sqlalchemy import func

    base = select(Attempt).where(Attempt.user_id == user.id)
    total = db.scalar(select(func.count()).select_from(base.subquery()))
    rows = db.scalars(base.order_by(Attempt.started_at.desc()).limit(limit).offset(offset)).all()
    exams = {e.id: e for e in db.scalars(select(Exam).where(Exam.id.in_({r.exam_id for r in rows})))}
    return [{"id": r.id, "exam_id": r.exam_id, "exam_name": exams[r.exam_id].name, "status": r.status,
             "language": r.language, "started_at": r.started_at, "submitted_at": r.submitted_at, "score": r.score,
             "max_score": r.max_score, "percentile": r.percentile, "is_free_trial": r.is_free_trial,
             "remaining_seconds": remaining_seconds(r)} for r in rows], total
