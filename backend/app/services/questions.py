"""Question reports from users and the review workflow that turns confirmed mistakes into AI lessons (PDF 6.1, 6.4)."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.ai import prompts, schemas
from app.ai.embeddings import embed
from app.ai.provider import AIError, get_provider
from app.config import get_settings
from app.core.audit import audit
from app.core.errors import AppError, not_found
from app.models import AiLesson, Attempt, AttemptAnswer, Question, QuestionReport, QuestionTranslation, Topic, User

REPORT_REASONS = ("wrong_answer", "unclear", "bad_translation", "other")


def report_question(db: Session, user: User, question_id: uuid.UUID, reason: str, details: str,
                    language: str, attempt_id: uuid.UUID | None) -> QuestionReport:
    q = db.get(Question, question_id)
    if q is None:
        raise not_found("Question")
    # Users may only report questions they were actually served.
    served = db.scalar(select(func.count()).select_from(AttemptAnswer).join(Attempt).where(
        Attempt.user_id == user.id, AttemptAnswer.question_id == q.id))
    if not served:
        raise AppError(403, "not_served", "You can only report questions from your own attempts")
    r = QuestionReport(question_id=q.id, user_id=user.id, attempt_id=attempt_id, reason=reason,
                       details=(details or "")[:2000], language=language, status="open")
    db.add(r)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "already_reported", "You have already reported this question")
    q.report_count = db.scalar(select(func.count(func.distinct(QuestionReport.user_id))).where(
        QuestionReport.question_id == q.id, QuestionReport.status == "open"))
    if q.report_count >= get_settings().auto_quarantine_reports and q.status == "verified":
        q.status = "quarantined"  # removed from new papers until a subject expert reviews it
    db.commit()
    return r


def resolve_report(db: Session, admin: User, report_id: int, *, action: str, resolution: str,
                   fix: dict | None, create_lesson: bool, discard_question: bool) -> QuestionReport:
    """confirm: the user was right -> apply the fix (or discard), write a lesson. reject: the question was fine."""
    r = db.get(QuestionReport, report_id)
    if r is None:
        raise not_found("Question report")
    if r.status != "open":
        raise AppError(409, "already_resolved", "This report was already resolved")
    q = db.get(Question, r.question_id)
    r.status = "confirmed" if action == "confirm" else "rejected"
    r.resolution = resolution
    r.reviewed_by = admin.id

    if action == "confirm":
        if fix:
            apply_fix(db, q, fix, language=r.language if r.reason == "bad_translation" else "en")
        if discard_question:
            q.status = "rejected"  # stays in the bank as a known-bad question that blocks similar new ones
        if create_lesson:
            add_lesson_from(db, q, reason=r.reason, resolution=resolution, language=r.language,
                            source_ref=f"question_report:{r.id}")
        # Every other open report on this question is settled by the same review.
        for other in db.scalars(select(QuestionReport).where(QuestionReport.question_id == q.id,
                                                             QuestionReport.status == "open",
                                                             QuestionReport.id != r.id)):
            other.status, other.resolution, other.reviewed_by = "confirmed", resolution, admin.id
    open_left = db.scalar(select(func.count()).select_from(QuestionReport).where(
        QuestionReport.question_id == q.id, QuestionReport.status == "open", QuestionReport.id != r.id))
    q.report_count = open_left
    if q.status == "quarantined" and open_left == 0 and not discard_question:
        q.status = "verified"
        q.verified_by = f"expert:{admin.id}"
    audit(db, admin, f"question_report.{r.status}", "question_report", r.id, question_id=str(q.id),
          resolution=resolution, fixed=bool(fix), discarded=discard_question)
    db.commit()
    return r


def apply_fix(db: Session, q: Question, fix: dict, language: str = "en") -> None:
    if language != "en":
        tr = db.scalar(select(QuestionTranslation).where(QuestionTranslation.question_id == q.id,
                                                         QuestionTranslation.language == language))
        if tr is None:
            tr = QuestionTranslation(question_id=q.id, language=language, text=fix.get("text", q.text))
            db.add(tr)
        for f in ("text", "options", "explanation", "shortcut"):
            if f in fix:
                setattr(tr, f, fix[f])
        tr.review_status = "approved"
        return
    for f in ("text", "options", "explanation", "shortcut", "difficulty", "expected_time_sec", "subtopic"):
        if f in fix:
            setattr(q, f, fix[f])
    if "correct_answer" in fix:
        q.correct_answer = {"value": fix["correct_answer"]}
    if "text" in fix or "options" in fix:
        q.embedding = embed(q.text + " " + " ".join(o["text"] for o in q.options or []))
        # English changed: translations must be redone or re-approved.
        for tr in db.scalars(select(QuestionTranslation).where(QuestionTranslation.question_id == q.id)):
            tr.review_status = "pending"


def add_lesson_from(db: Session, q: Question, *, reason: str, resolution: str, language: str, source_ref: str) -> AiLesson:
    topic = db.get(Topic, q.topic_id)
    try:
        lesson = get_provider().generate_json(
            purpose="lesson", system=prompts.LESSON_SYSTEM, schema=schemas.LESSON, tier="fast",
            prompt=prompts.lesson_prompt(topic=topic.name if topic else "", language=language, question_text=q.text,
                                         reason=reason, resolution=resolution),
            context={"topic": topic.name if topic else "", "resolution": resolution}, ref_id=q.id, db=db,
        )["lesson"].strip()
    except (AIError, KeyError):
        lesson = f"{reason.replace('_', ' ')} on {topic.name if topic else 'this topic'}: {resolution}"[:300]
    row = AiLesson(exam_id=q.exam_id, topic_id=q.topic_id, language=language, lesson_text=lesson,
                   embedding=embed(lesson), source_ref=source_ref, active=True)
    db.add(row)
    db.flush()
    return row


def confirm_wrong(db: Session, admin: User, q: Question, correction: str, fix: dict | None) -> AiLesson:
    """Admin confirms a question is wrong (15-day plan, Day 13): hide it, save the correction, write a lesson that
    future generation prompts on this topic will use, and close its open flags."""
    if fix:
        apply_fix(db, q, fix)
    q.status = "rejected"  # hidden from new papers; kept as a known-bad question that blocks similar ones
    q.generation_meta = {**(q.generation_meta or {}), "correction": correction, "confirmed_wrong_by": str(admin.id)}
    lesson = add_lesson_from(db, q, reason="wrong_answer", resolution=correction, language="en",
                             source_ref=f"question:{q.id}")
    for r in db.scalars(select(QuestionReport).where(QuestionReport.question_id == q.id, QuestionReport.status == "open")):
        r.status, r.resolution, r.reviewed_by = "confirmed", correction, admin.id
    q.report_count = 0
    audit(db, admin, "question.confirm_wrong", "question", q.id, correction=correction, lesson_id=lesson.id)
    db.commit()
    return lesson
