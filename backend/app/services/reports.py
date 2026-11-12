"""AI result reports (PDF 5.5, 6.2): code computes analytics, the LLM writes the words, code validates them."""

import logging
import time
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ai import prompts, schemas
from app.ai.provider import USD_TO_INR, AIError, cost_usd, get_provider
from app.config import get_settings
from app.core.audit import track
from app.core.errors import AppError, not_found
from app.core.security import new_share_token
from app.db import SessionLocal, utcnow
from app.models import AiLesson, AiUsage, Attempt, Exam, InterviewRole, InterviewSession, Report, User
from app.services import credits, memory, pdf
from app.services.notifications import dispatch_after_commit, notify
from app.services.providers import get_storage

log = logging.getLogger(__name__)
MAX_AI_TRIES = 2


REPORT_QUESTION_KEYS = ("ref", "section_key", "topic", "difficulty", "status", "time_sec", "expected_time_sec")


def _compact_analytics(a: dict) -> dict:
    """What the LLM needs (no internal ids). Questions answered correctly within their expected time are left out
    of the list: weaknesses, loopholes and shortcuts only ever cite missed, skipped or slow questions, and the
    section and topic totals already carry the strengths. This keeps the prompt, and so the report's time and cost,
    small (a 100-question paper sends roughly half the questions)."""
    listed = [{k: q[k] for k in REPORT_QUESTION_KEYS} for q in a["questions"]
              if q["status"] != "correct" or q["time_sec"] > q["expected_time_sec"]]
    return {
        "score": a["score"], "max_score": a["max_score"], "accuracy": a["accuracy"], "percentile": a.get("percentile"),
        "attempted": a["attempted"], "correct": a["correct"], "wrong": a["wrong"], "unanswered": a["unanswered"],
        "negative_marks_lost": a["negative_marks_lost"], "avg_time_per_question_sec": a["avg_time_per_question_sec"],
        "sections": a["sections"], "topics": a["topics"], "error_patterns": a["error_patterns"],
        "questions": listed, "questions_correct_on_time": len(a["questions"]) - len(listed),
        "previous_scores": a.get("previous_scores", []), "anti_cheat": a.get("anti_cheat", {}),
        "since_last_attempt": a.get("since_last_attempt"),
    }


def validate_exam_report(raw: dict, analytics: dict, candidates: dict[str, str], default_slug: str) -> dict:
    """Enforces the report contract in code: every weakness cites real questions, a 7-day plan, a real next test."""
    refs = {q["ref"]: q for q in analytics["questions"]}
    not_correct = {r for r, q in refs.items() if q["status"] != "correct"}
    topic_wrong = {t["name"].lower(): t["wrong_refs"] for t in analytics["topics"]}

    weaknesses = []
    for w in raw.get("weaknesses", []):
        cited = [r for r in w.get("question_refs", []) if r in refs]
        if not cited:  # repair from code analytics when the model forgot the evidence
            cited = topic_wrong.get(str(w.get("topic", "")).lower(), [])[:5]
        if cited:
            weaknesses.append({**w, "question_refs": cited,
                               "questions": [{"ref": r, "question_id": refs[r]["question_id"]} for r in cited]})
    if not weaknesses and not_correct:
        for t in analytics["topics"]:
            if t["wrong_refs"]:
                weaknesses.append({"topic": t["name"], "detail": "Several questions on this topic were missed.",
                                   "question_refs": t["wrong_refs"][:5],
                                   "questions": [{"ref": r, "question_id": refs[r]["question_id"]} for r in t["wrong_refs"][:5]]})
                break

    loopholes = [{**l, "question_refs": [r for r in l.get("question_refs", []) if r in refs]} for l in raw.get("loopholes", [])]
    shortcuts = [s for s in raw.get("shortcuts", []) if s.get("question_ref") in refs]
    for s in shortcuts:
        s["question_id"] = refs[s["question_ref"]]["question_id"]

    plan = sorted(raw.get("study_plan", []), key=lambda d: d.get("day", 99))[:7]
    while len(plan) < 7:
        plan.append({"day": len(plan) + 1, "focus": "Mixed timed practice", "tasks": ["Solve 25 mixed questions in 20 minutes"]})
    for i, d in enumerate(plan, start=1):
        d["day"] = i

    nt = raw.get("next_test") or {}
    slug = nt.get("exam_slug") if nt.get("exam_slug") in candidates else default_slug
    return {
        "summary": raw.get("summary", ""),
        "score_summary": {k: analytics.get(k) for k in ("score", "max_score", "accuracy", "percentile", "attempted",
                                                         "correct", "wrong", "unanswered", "negative_marks_lost",
                                                         "total_time_sec", "avg_time_per_question_sec")},
        "strengths": raw.get("strengths", []), "weaknesses": weaknesses, "loopholes": loopholes,
        "shortcuts": shortcuts, "study_plan": plan,
        "next_test": {"exam_slug": slug, "name": candidates.get(slug, ""), "reason": nt.get("reason", "")},
        "encouragement": raw.get("encouragement", ""),
        # Numbers by code, words by AI; null on a first attempt.
        "since_last_attempt": None if not analytics.get("since_last_attempt") else {
            **analytics["since_last_attempt"], "summary": raw.get("since_last_attempt", "")},
    }


def _next_test_candidates(db: Session, user: User, exam: Exam) -> dict[str, str]:
    targets = [str(t) for t in (user.profile.target_exam_ids or [])] if user.profile else []
    rows = db.scalars(select(Exam).where(Exam.status == "published")).all()
    picked = [e for e in rows if e.id == exam.id or e.category == exam.category or str(e.id) in targets or e.slug in targets]
    return {e.slug: e.name for e in picked[:20]}


def generate_exam_report(report_id) -> None:
    with SessionLocal() as db:
        report = db.get(Report, report_id)
        if report is None or report.status != "processing":
            return
        attempt = db.get(Attempt, report.attempt_id)
        exam = db.get(Exam, attempt.exam_id)
        user = db.get(User, report.user_id)
        candidates = _next_test_candidates(db, user, exam)
        started, started_at = time.monotonic(), utcnow()
        last_error = ""
        for _ in range(MAX_AI_TRIES):
            try:
                raw = get_provider().generate_json(
                    purpose="exam_report", system=prompts.REPORT_SYSTEM, schema=schemas.EXAM_REPORT, tier="strong",
                    prompt=prompts.report_prompt(language=report.language, exam_name=exam.name,
                                                 analytics=_compact_analytics(report.analytics),
                                                 memory=memory.memory_profile(db, user.id, exam.id),
                                                 candidates=list(candidates)),
                    context={"analytics": report.analytics, "exam_slug": exam.slug}, ref_id=attempt.id, db=db,
                )
                content = validate_exam_report(raw, report.analytics, candidates, exam.slug)
                break
            except (AIError, KeyError, TypeError, ValueError) as e:
                last_error = str(e)
        else:
            _fail(db, report, f"AI report failed: {last_error}")
            return
        db.refresh(report)
        if report.status != "processing":  # the timeout sweeper got there first
            return
        report.report = content
        report.generation_ms = int((time.monotonic() - started) * 1000)
        _log_report_cost(db, report, attempt.id, started_at)
        try:
            data = pdf.exam_report_pdf(app_name=get_settings().app_name, exam_name=exam.name, language=report.language,
                                       analytics=report.analytics, report=content)
            report.pdf_path = get_storage().save("reports", data, ".pdf")
        except Exception:
            log.exception("PDF render failed for report %s (report stays available as JSON)", report.id)
        report.status = "ready"
        n = notify(db, user.id, "result_ready", {"report_id": str(report.id), "attempt_id": str(attempt.id)},
                   exam=exam.name)
        db.commit()
        dispatch_after_commit(n.id)


def _log_report_cost(db: Session, report: Report, attempt_id, since) -> None:
    """One log line per report with its time, tokens and cost (all exam_report AI calls for it, retries included)."""
    rows = db.execute(select(AiUsage.model, func.sum(AiUsage.input_tokens), func.sum(AiUsage.output_tokens))
                      .where(AiUsage.purpose == "exam_report", AiUsage.ref_id == str(attempt_id),
                             AiUsage.created_at >= since).group_by(AiUsage.model)).all()
    tokens_in, tokens_out = sum(r[1] or 0 for r in rows), sum(r[2] or 0 for r in rows)
    inr = sum(cost_usd(m, tin or 0, tout or 0) for m, tin, tout in rows) * USD_TO_INR
    log.info("exam report %s ready in %d ms: %d input + %d output tokens, about Rs %.2f",
             report.id, report.generation_ms, tokens_in, tokens_out, inr)


def _fail(db: Session, report: Report, error: str) -> None:
    """Marks the report failed and restores the credit (PDF 7: auto-refund of credit on technical failure)."""
    report.status = "failed"
    report.error = error[:2000]
    ref = report.attempt_id or report.interview_session_id
    if not report.credit_restored:
        credits.restore(db, report.user_id, ref)
        report.credit_restored = True
    name = ""
    if report.attempt_id:
        name = db.get(Exam, db.get(Attempt, report.attempt_id).exam_id).name
    elif report.interview_session_id:
        name = db.get(InterviewRole, db.get(InterviewSession, report.interview_session_id).role_id).name
    n = notify(db, report.user_id, "report_failed", {"report_id": str(report.id)}, name=name)
    db.commit()
    dispatch_after_commit(n.id)


def fail_report(report_id, error: str) -> None:
    with SessionLocal() as db:
        report = db.get(Report, report_id)
        if report is not None and report.status == "processing":
            _fail(db, report, error)


def sweep_timeouts(db: Session) -> int:
    cutoff = utcnow() - timedelta(minutes=get_settings().report_timeout_minutes)
    stuck = db.scalars(select(Report).where(Report.status == "processing", Report.created_at < cutoff).limit(200)).all()
    for r in stuck:
        _fail(db, r, "Report was not ready within the time limit")
    return len(stuck)


def retry(db: Session, user: User, report_id) -> Report:
    from app.jobs.queue import enqueue

    r = own_report(db, user, report_id)
    if r.status != "failed":
        raise AppError(409, "not_failed", "Only failed reports can be retried")
    r.status, r.error, r.created_at = "processing", None, utcnow()
    db.commit()
    enqueue("generate_exam_report" if r.kind == "exam" else "evaluate_interview", report_id=r.id)
    db.refresh(r)  # the job may already have finished (eager/thread mode)
    return r


def own_report(db: Session, user: User, report_id) -> Report:
    r = db.get(Report, report_id)
    if r is None or r.user_id != user.id:
        raise not_found("Report")
    return r


def report_for_attempt(db: Session, user: User, attempt_id) -> Report:
    a = db.get(Attempt, attempt_id)
    if a is None or a.user_id != user.id:
        raise not_found("Attempt")
    r = db.scalar(select(Report).where(Report.attempt_id == a.id))
    if r is None:
        raise AppError(409, "not_submitted", "Submit the exam to get your report")
    return r


def serialize(r: Report, include_analytics: bool = True) -> dict:
    base = get_settings().public_base_url.rstrip("/") + get_settings().api_prefix
    return {
        "id": r.id, "kind": r.kind, "status": r.status, "language": r.language,
        "attempt_id": r.attempt_id, "interview_session_id": r.interview_session_id,
        "analytics": r.analytics if include_analytics else None,
        "report": r.report if r.status == "ready" else None,
        "pdf_url": f"{base}/reports/{r.id}/pdf" if r.status == "ready" else None,
        "share_url": (f"{get_settings().web_base_url.rstrip('/')}/shared/reports/{r.share_token}"
                      if r.share_token else None),
        "share_api_url": f"{base}/shared/reports/{r.share_token}" if r.share_token else None,
        "user_rating": r.user_rating, "error": r.error if r.status == "failed" else None,
        "credit_restored": r.credit_restored, "created_at": r.created_at,
        "poll_after_seconds": 3 if r.status == "processing" else None,
    }


def mark_viewed(db: Session, user: User, r: Report) -> None:
    if r.status == "ready":
        track(db, user.id, "report_viewed", report_id=str(r.id), kind=r.kind)
        db.commit()


def rate(db: Session, user: User, report_id, rating: int, comment: str | None) -> Report:
    r = own_report(db, user, report_id)
    if r.status != "ready":
        raise AppError(409, "report_not_ready", "You can rate the report once it is ready")
    r.user_rating, r.rating_comment = rating, (comment or None)
    track(db, user.id, "report_rating", report_id=str(r.id), rating=rating)
    if rating <= 2:
        # Low-rated reports feed the AI self-correction memory. Inactive until a content manager reviews it,
        # because the comment is untrusted user text.
        exam_id = db.get(Attempt, r.attempt_id).exam_id if r.attempt_id else None
        db.add(AiLesson(exam_id=exam_id, language=r.language, active=False, source_ref=f"report_rating:{r.id}",
                        lesson_text=f"Low-rated {r.kind} report ({rating}/5). User comment: {(comment or '')[:400]}"))
    db.commit()
    return r


def share(db: Session, user: User, report_id) -> Report:
    r = own_report(db, user, report_id)
    if r.status != "ready":
        raise AppError(409, "report_not_ready", "You can share the report once it is ready")
    if not r.share_token or (r.share_expires_at and r.share_expires_at < utcnow()):
        r.share_token = new_share_token()
    r.share_expires_at = utcnow() + timedelta(days=get_settings().report_share_days)
    db.commit()
    return r


def unshare(db: Session, user: User, report_id) -> None:
    r = own_report(db, user, report_id)
    r.share_token, r.share_expires_at = None, None
    db.commit()


def by_share_token(db: Session, token: str) -> Report:
    r = db.scalar(select(Report).where(Report.share_token == token))
    if r is None or r.status != "ready" or (r.share_expires_at and r.share_expires_at < utcnow()):
        raise not_found("Shared report")
    return r


def public_view(db: Session, r: Report) -> dict:
    """Shared link view: no personal data, no question ids."""
    title = ""
    if r.attempt_id:
        title = db.get(Exam, db.get(Attempt, r.attempt_id).exam_id).name
    elif r.interview_session_id:
        title = db.get(InterviewRole, db.get(InterviewSession, r.interview_session_id).role_id).name
    rep = dict(r.report or {})
    for w in rep.get("weaknesses", []):
        w.pop("questions", None)
    for s in rep.get("shortcuts", []):
        s.pop("question_id", None)
    return {"kind": r.kind, "title": title, "language": r.language, "report": rep, "created_at": r.created_at}


def pdf_bytes(db: Session, r: Report) -> bytes:
    if r.status != "ready":
        raise AppError(409, "report_not_ready", "The report is not ready yet")
    storage = get_storage()
    if r.pdf_path:
        try:
            return storage.read(r.pdf_path)
        except FileNotFoundError:
            pass
    s = get_settings()
    if r.kind == "exam":
        exam = db.get(Exam, db.get(Attempt, r.attempt_id).exam_id)
        data = pdf.exam_report_pdf(app_name=s.app_name, exam_name=exam.name, language=r.language,
                                   analytics=r.analytics, report=r.report)
    else:
        role = db.get(InterviewRole, db.get(InterviewSession, r.interview_session_id).role_id)
        data = pdf.interview_report_pdf(app_name=s.app_name, role_name=role.name, language=r.language, report=r.report)
    r.pdf_path = storage.save("reports", data, ".pdf")
    db.commit()
    return data
