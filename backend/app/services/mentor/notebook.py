"""Mistake notebook with spaced revision (mentor module 8).

Every wrong, skipped-after-working or very slow question of a scored mock gets a card. Revision answers move the card
through the configured intervals (1, 3, 7, 14, 30 days by default): right = next step, wrong = back to the first step.
A card that is answered right at every step is resolved; it comes back if the student gets it wrong in a mock again.
"""

import uuid
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import AppError, not_found
from app.db import utcnow
from app.models import Attempt, NotebookEntry, Question, Topic, User
from app.services.mentor import config as cfg

MISTAKE_TYPES = ("concept", "calculation", "misread", "wrong_formula", "guessing", "time_pressure", "option_confusion")
SLOW_NOTEBOOK_RATIO = 2.0  # correct but slower than twice the target: worth a speed card


def auto_type(band: str, difficulty: str, status: str) -> str | None:
    """A first guess from the evidence; the student can correct it (their choice always wins)."""
    if status != "wrong":
        return "time_pressure" if band == "skipped_after_time" else None
    if band == "rushed_wrong":
        return "guessing" if difficulty != "easy" else "misread"
    if band == "time_sink":
        return "concept"
    if difficulty == "easy":
        return "calculation"
    return None


def record_attempt(db: Session, a: Attempt, rows: list[dict]) -> int:
    """rows from analysis.build_rows. Returns how many cards were created or updated."""
    now = utcnow()
    n = 0
    for r in rows:
        reason = None
        if r["status"] == "wrong":
            reason = "wrong"
        elif r["band"] == "skipped_after_time":
            reason = "skipped"
        elif r["status"] == "correct" and r["time_ratio"] and r["time_ratio"] > SLOW_NOTEBOOK_RATIO:
            reason = "slow"
        if reason is None:
            continue
        qid = uuid.UUID(r["question_id"])
        e = db.scalar(select(NotebookEntry).where(NotebookEntry.user_id == a.user_id, NotebookEntry.question_id == qid))
        if e is None:
            e = NotebookEntry(user_id=a.user_id, question_id=qid, exam_id=a.exam_id, topic_id=r["topic_id"],
                              reasons=[], times_wrong=0, times_skipped=0, times_slow=0, revision_correct=0,
                              revision_wrong=0, box=0, last_time_sec=0, bookmarked=False, note="")
            db.add(e)
        e.reasons = sorted(set(e.reasons or []) | {reason})
        e.last_attempt_id = a.id
        e.last_answer = {"value": r["your_answer"]} if r["your_answer"] is not None else None
        e.last_time_sec = r["time_sec"]
        if reason == "wrong":
            e.times_wrong = (e.times_wrong or 0) + 1
        elif reason == "skipped":
            e.times_skipped = (e.times_skipped or 0) + 1
        else:
            e.times_slow = (e.times_slow or 0) + 1
        e.auto_mistake_type = auto_type(r["band"], r["difficulty"], r["status"]) or e.auto_mistake_type
        # A fresh mistake restarts the spacing, even on a card that was resolved before.
        e.box, e.status = 0, "active"
        e.next_review_at = now + timedelta(days=cfg.revision_intervals()[0])
        n += 1
    return n


def review(e: NotebookEntry, correct: bool) -> None:
    steps = cfg.revision_intervals()
    now = utcnow()
    e.last_reviewed_at = now
    if correct:
        e.revision_correct = (e.revision_correct or 0) + 1
        e.box = (e.box or 0) + 1
        if e.box >= len(steps):
            e.status, e.next_review_at = "resolved", None
            return
    else:
        e.revision_wrong = (e.revision_wrong or 0) + 1
        e.box = 0
    e.next_review_at = now + timedelta(days=steps[e.box])


FILTERS = ("all", "wrong", "corrected", "repeated", "slow", "bookmarked", "due", "resolved")


def _filtered(stmt, f: str):
    now = utcnow()
    if f == "wrong":
        return stmt.where(NotebookEntry.status == "active", NotebookEntry.times_wrong > 0)
    if f == "corrected":
        return stmt.where(NotebookEntry.times_wrong > 0, NotebookEntry.revision_correct > 0)
    if f == "repeated":
        return stmt.where(NotebookEntry.times_wrong + NotebookEntry.revision_wrong >= 2)
    if f == "slow":
        return stmt.where(NotebookEntry.times_slow + NotebookEntry.times_skipped > 0)
    if f == "bookmarked":
        return stmt.where(NotebookEntry.bookmarked.is_(True))
    if f == "due":
        return stmt.where(NotebookEntry.status == "active", NotebookEntry.next_review_at <= now)
    if f == "resolved":
        return stmt.where(NotebookEntry.status == "resolved")
    return stmt


def serialize(e: NotebookEntry, q: Question, topic: str | None) -> dict:
    return {
        "id": e.id, "question_id": str(e.question_id), "exam_id": str(e.exam_id), "topic_id": e.topic_id,
        "topic": topic, "difficulty": q.difficulty, "type": q.type, "text": q.text, "options": q.options,
        "your_answer": (e.last_answer or {}).get("value"), "correct_answer": q.correct_answer["value"],
        "explanation": q.explanation, "shortcut": q.shortcut, "reasons": e.reasons,
        "mistake_type": e.mistake_type or e.auto_mistake_type, "mistake_type_source": "student" if e.mistake_type else (
            "auto" if e.auto_mistake_type else None),
        "times_wrong": e.times_wrong, "times_skipped": e.times_skipped, "times_slow": e.times_slow,
        "revision_correct": e.revision_correct, "revision_wrong": e.revision_wrong, "box": e.box,
        "next_review_at": e.next_review_at, "last_reviewed_at": e.last_reviewed_at, "last_time_sec": e.last_time_sec,
        "bookmarked": e.bookmarked, "note": e.note, "status": e.status, "created_at": e.created_at,
    }


def counts(db: Session, user_id) -> dict:
    base = select(func.count()).select_from(NotebookEntry).where(NotebookEntry.user_id == user_id)
    return {f: db.scalar(_filtered(base, f)) for f in FILTERS}


def listing(db: Session, user: User, f: str, topic_id: int | None, exam_id, limit: int, offset: int) -> dict:
    if f not in FILTERS:
        raise AppError(422, "invalid_filter", f"filter must be one of {FILTERS}")
    stmt = _filtered(select(NotebookEntry).where(NotebookEntry.user_id == user.id), f)
    if topic_id is not None:
        stmt = stmt.where(NotebookEntry.topic_id == topic_id)
    if exam_id is not None:
        stmt = stmt.where(NotebookEntry.exam_id == exam_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    rows = db.scalars(stmt.order_by(NotebookEntry.next_review_at.is_(None), NotebookEntry.next_review_at,
                                    NotebookEntry.id.desc()).limit(limit).offset(offset)).all()
    qs = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_([r.question_id for r in rows])))}
    names = {t.id: t.name for t in db.scalars(select(Topic).where(Topic.id.in_({r.topic_id for r in rows if r.topic_id})))}
    by_type: dict[str, int] = {}
    for t, n in db.execute(select(func.coalesce(NotebookEntry.mistake_type, NotebookEntry.auto_mistake_type), func.count())
                           .where(NotebookEntry.user_id == user.id, NotebookEntry.status == "active")
                           .group_by(func.coalesce(NotebookEntry.mistake_type, NotebookEntry.auto_mistake_type))):
        by_type[t or "untagged"] = n
    return {"items": [serialize(r, qs[r.question_id], names.get(r.topic_id)) for r in rows], "total": total,
            "limit": limit, "offset": offset, "counts": counts(db, user.id), "by_mistake_type": by_type}


def own_entry(db: Session, user: User, entry_id: int) -> NotebookEntry:
    e = db.get(NotebookEntry, entry_id)
    if e is None or e.user_id != user.id:
        raise not_found("Notebook entry")
    return e


def update(db: Session, user: User, entry_id: int, body: dict) -> dict:
    e = own_entry(db, user, entry_id)
    if "mistake_type" in body:
        mt = body["mistake_type"]
        if mt is not None and mt not in MISTAKE_TYPES:
            raise AppError(422, "invalid_mistake_type", f"mistake_type must be one of {MISTAKE_TYPES}")
        e.mistake_type = mt
    if body.get("bookmarked") is not None:
        e.bookmarked = bool(body["bookmarked"])
    if body.get("note") is not None:
        e.note = str(body["note"])[:2000]
    db.commit()
    q = db.get(Question, e.question_id)
    t = db.get(Topic, e.topic_id) if e.topic_id else None
    return serialize(e, q, t.name if t else None)


def bookmark_question(db: Session, user: User, question_id: uuid.UUID, attempt_id: uuid.UUID | None) -> dict:
    """Bookmark any question the student has seen in a submitted attempt (creates a card if needed)."""
    from app.models import AttemptAnswer

    stmt = select(AttemptAnswer, Attempt).join(Attempt, Attempt.id == AttemptAnswer.attempt_id).where(
        AttemptAnswer.question_id == question_id, Attempt.user_id == user.id, Attempt.status == "scored")
    if attempt_id:
        stmt = stmt.where(Attempt.id == attempt_id)
    hit = db.execute(stmt.limit(1)).first()
    if hit is None:
        raise not_found("Question in your submitted attempts")
    ans, a = hit
    q = db.get(Question, question_id)
    e = db.scalar(select(NotebookEntry).where(NotebookEntry.user_id == user.id, NotebookEntry.question_id == question_id))
    if e is None:
        e = NotebookEntry(user_id=user.id, question_id=question_id, exam_id=a.exam_id, topic_id=q.topic_id,
                          last_attempt_id=a.id, last_answer=ans.answer, reasons=["bookmark"], times_wrong=0,
                          times_skipped=0, times_slow=0, revision_correct=0, revision_wrong=0, box=0,
                          last_time_sec=ans.time_spent_sec or 0, bookmarked=True, note="", status="active",
                          next_review_at=utcnow() + timedelta(days=cfg.revision_intervals()[0]))
        db.add(e)
    else:
        e.bookmarked = True
        e.reasons = sorted(set(e.reasons or []) | {"bookmark"})
    db.commit()
    t = db.get(Topic, q.topic_id)
    return serialize(e, q, t.name if t else None)


def due_count(db: Session, user_id, exam_id=None) -> int:
    stmt = select(func.count()).select_from(NotebookEntry).where(
        NotebookEntry.user_id == user_id, NotebookEntry.status == "active", NotebookEntry.next_review_at <= utcnow())
    if exam_id is not None:
        stmt = stmt.where(NotebookEntry.exam_id == exam_id)
    return db.scalar(stmt) or 0
