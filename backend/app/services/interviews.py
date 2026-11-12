"""AI mock interview engine (PDF 5.4, 5.6, 6.3).

A stage controller (introduction -> resume -> role/technical -> situational -> HR -> closing) decides the stage of
each question; the LLM writes the question from the stage, role, resume and the previous answer. Code guarantees
at least 2 follow-ups, 8-12 questions, resume once within 10 minutes of a disconnect, and evaluation on whatever
was answered.
"""

import logging
import time
import uuid
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai import prompts, schemas
from app.ai.provider import AIError, get_provider
from app.ai.safety import strip_pii
from app.config import get_settings
from app.core.audit import track
from app.core.errors import AppError, not_found
from app.core.languages import is_supported
from app.db import SessionLocal, utcnow
from app.jobs.queue import enqueue
from app.models import InterviewRole, InterviewSession, InterviewTurn, Report, User
from app.services import credits, pdf
from app.services.blueprints import largest_remainder
from app.services.notifications import dispatch_after_commit, notify
from app.services.profile import require_complete_profile
from app.services.providers import get_storage
from app.services.reports import _fail
from app.services.speech import speaking_metrics, voice_supported

log = logging.getLogger(__name__)
STAGES = ["introduction", "resume", "role_technical", "situational", "hr", "closing"]
STAGE_WEIGHTS = {"resume": 2, "role_technical": 3, "situational": 2, "hr": 1}
MIN_FOLLOWUPS = 2
DEFAULT_CRITERIA = [
    {"key": "role_knowledge", "label": "Role knowledge"},
    {"key": "answer_structure", "label": "Answer structure"},
    {"key": "communication", "label": "Communication"},
    {"key": "confidence", "label": "Confidence"},
    {"key": "resume_consistency", "label": "Resume consistency"},
]
CLOSING_TEXT = "Thank you, that brings us to the end of the interview. Your detailed feedback report is being prepared."


def stage_plan(total: int, has_resume: bool) -> list[str]:
    """Stage for each question number (1-based index = position)."""
    weights = dict(STAGE_WEIGHTS)
    if not has_resume:
        weights["role_technical"] += weights.pop("resume")
    counts = largest_remainder(total - 2, weights)
    plan = ["introduction"]
    for st in STAGES[1:-1]:
        plan += [st] * counts.get(st, 0)
    return plan + ["closing"]


def _rubric(role: InterviewRole) -> list[dict]:
    return (role.rubric or {}).get("criteria") or DEFAULT_CRITERIA


def _own(db: Session, user: User, session_id, lock: bool = False) -> InterviewSession:
    stmt = select(InterviewSession).where(InterviewSession.id == session_id, InterviewSession.user_id == user.id)
    if lock:
        stmt = stmt.with_for_update()
    s = db.scalar(stmt)
    if s is None:
        raise not_found("Interview")
    return s


def start(db: Session, user: User, *, role_id, level: str, language: str, mode: str,
          job_description: str | None, resume_text: str | None, use_profile_resume: bool) -> InterviewSession:
    require_complete_profile(db, user)
    role = db.get(InterviewRole, role_id)
    if role is None or role.status != "published":
        raise not_found("Interview role")
    if level not in (role.levels or []):
        raise AppError(422, "invalid_level", f"Choose one of: {', '.join(role.levels or [])}")
    if not is_supported(language):
        raise AppError(422, "unsupported_language", "Unsupported language")
    if mode == "voice" and not voice_supported(language):
        raise AppError(422, "voice_not_available", "Voice interviews are not yet available in this language. Use text mode.")
    active = db.scalar(select(InterviewSession).where(InterviewSession.user_id == user.id,
                                                      InterviewSession.status == "active"))
    if active is not None:
        raise AppError(409, "interview_in_progress", "Finish or end your current interview first",
                       {"interview_id": str(active.id)})

    resume = resume_text or (user.profile.resume_text if use_profile_resume and user.profile else None)
    target = int((role.prompt_config or {}).get("question_count", 10))
    session_id = uuid.uuid4()
    ledger = credits.consume(db, user, role.credits_required, "interview", session_id)
    s = InterviewSession(
        id=session_id, user_id=user.id, role_id=role.id, level=level, language=language, mode=mode,
        resume_ref=strip_pii(resume)[:20000] if resume else None,
        job_description=strip_pii(job_description)[:8000] if job_description else None,
        status="active", stage="introduction", question_count=0, followup_count=0,
        target_questions=max(8, min(12, target)), credit_ledger_id=ledger.id, last_activity_at=utcnow(),
    )
    db.add(s)
    db.flush()
    _ask_next(db, s, role, last_answer=None)
    track(db, user.id, "interview_start", role=role.slug, mode=mode, language=language)
    db.commit()
    return s


def _ask_next(db: Session, s: InterviewSession, role: InterviewRole, last_answer: str | None) -> InterviewTurn:
    plan = stage_plan(s.target_questions, bool(s.resume_ref))
    n = s.question_count + 1
    stage = plan[min(n, len(plan)) - 1]
    remaining_before_closing = len(plan) - 1 - n  # questions left after this one, excluding closing
    prev_q = next((t for t in reversed(s.turns) if t.speaker == "interviewer"), None)
    need = MIN_FOLLOWUPS - s.followup_count
    must_follow_up = bool(
        last_answer and stage != "closing" and need > 0 and (prev_q is None or not prev_q.is_followup)
        and (remaining_before_closing < need * 2 or stage in ("resume", "role_technical", "situational") and n >= 3)
    )
    cfg = role.prompt_config or {}
    transcript = [{"speaker": t.speaker, "text": t.text} for t in s.turns]
    try:
        out = get_provider().generate_json(
            purpose="interview_next", system=prompts.INTERVIEW_SYSTEM, schema=schemas.INTERVIEW_NEXT, tier="strong",
            effort="low",  # replies must start within 3 s in voice mode
            prompt=prompts.interview_next_prompt(
                role=role.name, level=s.level, language=s.language, stage=stage,
                themes=(cfg.get("themes") or {}).get(stage, []), persona=cfg.get("persona", "a fair, experienced panelist"),
                resume=s.resume_ref, jd=s.job_description, transcript=transcript, must_follow_up=must_follow_up,
                question_no=n, total=s.target_questions),
            context={"stage": stage, "question_no": n, "role": role.name, "must_follow_up": must_follow_up,
                     "last_answer": last_answer}, ref_id=s.id, db=db,
        )
        # A requested follow-up counts even if the model forgets to flag it; the prompt required it.
        text = out["question"].strip()
        is_follow = bool(last_answer) and (must_follow_up or bool(out.get("is_followup")))
    except (AIError, KeyError):
        # Keep the interview going with a rubric theme question rather than failing the session.
        themes = (cfg.get("themes") or {}).get(stage) or ["Tell me about a challenge you solved recently."]
        text, is_follow = themes[(n - 1) % len(themes)], False
    if not text:
        text = "Could you tell me more about that?"
    s.question_count = n
    s.stage = stage
    if is_follow:
        s.followup_count += 1
    turn = InterviewTurn(session_id=s.id, seq=len(s.turns) + 1, stage=stage, speaker="interviewer", text=text,
                         is_followup=is_follow)
    s.turns.append(turn)
    db.flush()
    return turn


def answer(db: Session, user: User, session_id, text: str, duration_sec: float | None = None) -> dict:
    s = _own(db, user, session_id, lock=True)
    _check_active(db, s)
    text = (text or "").strip()
    if not text:
        raise AppError(422, "empty_answer", "Answer cannot be empty")
    role = db.get(InterviewRole, s.role_id)
    last_q = s.turns[-1] if s.turns else None
    s.turns.append(InterviewTurn(session_id=s.id, seq=len(s.turns) + 1, stage=s.stage, speaker="candidate",
                                 text=text[:8000], meta={"duration_sec": duration_sec} if duration_sec else {}))
    s.last_activity_at = utcnow()
    if s.question_count >= s.target_questions or (last_q is not None and last_q.stage == "closing"):
        s.turns.append(InterviewTurn(session_id=s.id, seq=len(s.turns) + 1, stage="closing", speaker="interviewer",
                                     text=CLOSING_TEXT))
        report = _end(db, s, "completed")
        db.commit()
        enqueue("evaluate_interview", report_id=report.id)
        return {"done": True, "turn": s.turns[-1], "report_id": report.id}
    turn = _ask_next(db, s, role, last_answer=text)
    db.commit()
    return {"done": False, "turn": turn, "report_id": None}


def _check_active(db: Session, s: InterviewSession) -> None:
    if s.status != "active":
        raise AppError(409, "interview_ended", "This interview has ended")
    limit = timedelta(minutes=get_settings().interview_resume_minutes)
    idle_since = s.disconnected_at or s.last_activity_at
    if idle_since and utcnow() - idle_since > limit:
        report = _end(db, s, "disconnect_timeout")
        db.commit()
        if report is not None:
            enqueue("evaluate_interview", report_id=report.id)
        raise AppError(409, "interview_ended", "The interview ended because the connection was lost for over 10 minutes. "
                                               "It is being evaluated on what you answered.")


def mark_disconnected(db: Session, session_id) -> None:
    s = db.get(InterviewSession, session_id)
    if s is not None and s.status == "active" and s.disconnected_at is None:
        s.disconnected_at = utcnow()
        db.commit()


def resume(db: Session, user: User, session_id) -> InterviewSession:
    """Reconnect after a drop: allowed once, within 10 minutes (PDF 5.4 AC)."""
    s = _own(db, user, session_id, lock=True)
    _check_active(db, s)
    if s.disconnected_at is not None:
        if s.resumes_used >= 1:
            report = _end(db, s, "disconnect_limit")
            db.commit()
            enqueue("evaluate_interview", report_id=report.id)
            raise AppError(409, "interview_ended", "An interview can be resumed only once. It is being evaluated now.")
        s.resumes_used += 1
        s.disconnected_at = None
        s.last_activity_at = utcnow()
        db.commit()
    return s


def end(db: Session, user: User, session_id) -> Report | None:
    s = _own(db, user, session_id, lock=True)
    if s.status != "active":
        return db.scalar(select(Report).where(Report.interview_session_id == s.id))
    report = _end(db, s, "user_ended")
    db.commit()
    enqueue("evaluate_interview", report_id=report.id)
    db.refresh(report)
    return report


def _end(db: Session, s: InterviewSession, reason: str) -> Report:
    if s.status != "active":
        return db.scalar(select(Report).where(Report.interview_session_id == s.id))
    s.status = "ended"
    s.ended_at = utcnow()
    user = db.get(User, s.user_id)
    report = Report(user_id=s.user_id, kind="interview", interview_session_id=s.id, status="processing",
                    language=s.language or user.preferred_language, analytics={"end_reason": reason})
    db.add(report)
    db.flush()
    return report


def sweep_stale(db: Session) -> int:
    limit = utcnow() - timedelta(minutes=get_settings().interview_resume_minutes)
    stale = db.scalars(select(InterviewSession).where(
        InterviewSession.status == "active",
        ((InterviewSession.disconnected_at.is_not(None)) & (InterviewSession.disconnected_at < limit))
        | (InterviewSession.last_activity_at < limit)).limit(200)).all()
    reports = [_end(db, s, "disconnect_timeout") for s in stale]
    db.commit()
    for r in reports:
        enqueue("evaluate_interview", report_id=r.id)
    return len(stale)


def evaluate(report_id) -> None:
    """Scores the transcript against the rubric. Scores are clamped and completeness-checked by code."""
    with SessionLocal() as db:
        report = db.get(Report, report_id)
        if report is None or report.status != "processing":
            return
        s = db.get(InterviewSession, report.interview_session_id)
        role = db.get(InterviewRole, s.role_id)
        rubric = _rubric(role)
        transcript, questions_by_answer, answers = [], {}, []
        last_q = None
        for t in s.turns:
            transcript.append({"ref": t.seq, "speaker": t.speaker, "text": t.text})
            if t.speaker == "interviewer":
                last_q = t
            else:
                questions_by_answer[t.seq] = last_q.text if last_q else ""
                answers.append({"ref": t.seq, "text": t.text})
        if not answers:
            _fail(db, report, "No answers were given, so there is nothing to evaluate")
            return
        started = time.monotonic()
        content, last_error = None, ""
        for _ in range(2):
            try:
                raw = get_provider().generate_json(
                    purpose="interview_report", system=prompts.INTERVIEW_REPORT_SYSTEM, schema=schemas.INTERVIEW_REPORT,
                    tier="strong",
                    prompt=prompts.interview_report_prompt(role=role.name, level=s.level, language=report.language,
                                                           rubric=rubric, resume=s.resume_ref, transcript=transcript),
                    context={"answers": answers, "criteria": [c["key"] for c in rubric]}, ref_id=s.id, db=db,
                )
                content = validate_interview_report(raw, rubric, questions_by_answer)
                break
            except (AIError, KeyError, TypeError, ValueError) as e:
                last_error = str(e)
        if content is None:
            _fail(db, report, f"Interview evaluation failed: {last_error}")
            return
        if s.mode == "voice":
            metrics = speaking_metrics([(t.text, (t.meta or {}).get("duration_sec")) for t in s.turns
                                        if t.speaker == "candidate"], s.language)
            s.voice_metrics = metrics
            content["voice_metrics"] = metrics
        content["followups_asked"] = s.followup_count
        content["questions_asked"] = s.question_count
        report.report = content
        report.generation_ms = int((time.monotonic() - started) * 1000)
        s.status = "evaluated"
        try:
            data = pdf.interview_report_pdf(app_name=get_settings().app_name, role_name=role.name,
                                            language=report.language, report=content)
            report.pdf_path = get_storage().save("reports", data, ".pdf")
        except Exception:
            log.exception("PDF render failed for interview report %s", report.id)
        report.status = "ready"
        track(db, s.user_id, "interview_completed", role=role.slug, mode=s.mode, questions=s.question_count)
        n = notify(db, s.user_id, "interview_report_ready", {"report_id": str(report.id), "interview_id": str(s.id)},
                   role=role.name)
        db.commit()
        dispatch_after_commit(n.id)


def validate_interview_report(raw: dict, rubric: list[dict], questions_by_answer: dict[int, str]) -> dict:
    by_key = {str(sc.get("criterion")): sc for sc in raw.get("scores", [])}
    scores = []
    for c in rubric:
        sc = by_key.get(c["key"])
        if sc is None:
            raise ValueError(f"missing score for {c['key']}")
        scores.append({"criterion": c["key"], "label": c.get("label", c["key"]),
                       "score": max(1, min(10, int(round(float(sc["score"]))))),
                       "justification": sc.get("justification", "")})
    per_q = [{**p, "question": questions_by_answer[p["turn_ref"]]} for p in raw.get("per_question", [])
             if p.get("turn_ref") in questions_by_answer]
    plan = sorted(raw.get("study_plan", []), key=lambda d: d.get("day", 99))[:7]
    while len(plan) < 7:
        plan.append({"day": len(plan) + 1, "focus": "Mock answer practice", "tasks": ["Answer two questions aloud using STAR"]})
    for i, d in enumerate(plan, start=1):
        d["day"] = i
    return {"summary": raw.get("summary", ""), "scores": scores,
            "overall": round(sum(s["score"] for s in scores) / len(scores), 1),
            "per_question": per_q, "red_flags": raw.get("red_flags", []), "study_plan": plan}


def state(db: Session, user: User, session_id) -> dict:
    s = _own(db, user, session_id)
    role = db.get(InterviewRole, s.role_id)
    report = db.scalar(select(Report).where(Report.interview_session_id == s.id))
    return {
        "id": s.id, "role": {"id": role.id, "name": role.name, "slug": role.slug}, "level": s.level,
        "language": s.language, "mode": s.mode, "status": s.status, "stage": s.stage,
        "question_count": s.question_count, "target_questions": s.target_questions,
        "followup_count": s.followup_count, "resumes_used": s.resumes_used, "created_at": s.created_at,
        "ended_at": s.ended_at, "report_id": report.id if report else None,
        "transcript": [{"seq": t.seq, "speaker": t.speaker, "stage": t.stage, "text": t.text,
                        "is_followup": t.is_followup, "audio_url": t.audio_url, "at": t.created_at} for t in s.turns],
    }


def report_for_session(db: Session, user: User, session_id) -> Report:
    s = _own(db, user, session_id)
    r = db.scalar(select(Report).where(Report.interview_session_id == s.id))
    if r is None:
        raise AppError(409, "interview_active", "End the interview to get your report")
    return r
