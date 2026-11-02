"""Memory module (PDF 6.4).

User memory: topic mastery, mistake log, seen questions (never repeated), used to personalise reports and papers.
AI self-correction memory: lessons from confirmed mistakes, retrieved by exam/topic/language (+ embedding similarity)
and added to generation prompts; known-bad questions block similar new ones during duplicate checks.
"""

import json

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.ai.embeddings import cosine, embed
from app.db import is_postgres, utcnow
from app.models import AiLesson, Attempt, Question, Topic, UserMistake, UserTopicMastery


def lessons_for(db: Session, *, exam_id, topic_id, language: str, query: str, limit: int = 5) -> list[str]:
    rows = db.scalars(select(AiLesson).where(
        AiLesson.active.is_(True),
        (AiLesson.exam_id == exam_id) | (AiLesson.exam_id.is_(None)),
        (AiLesson.topic_id == topic_id) | (AiLesson.topic_id.is_(None)),
        AiLesson.language.in_({language, "en"}),
    ).limit(200)).all()
    if not rows:
        return []
    q = embed(query)
    # Exact topic + language matches first, then by similarity to the generation request.
    rows.sort(key=lambda l: (l.topic_id == topic_id, l.language == language, cosine(q, l.embedding)), reverse=True)
    return [l.lesson_text for l in rows[:limit]]


def most_similar_question(db: Session, exam_id, vector: list[float]) -> tuple[Question | None, float]:
    """Nearest existing question in the exam's bank, including rejected/quarantined (known-bad) ones."""
    if is_postgres():
        row = db.execute(text(
            "SELECT id, 1 - (embedding <=> CAST(:v AS vector)) AS sim FROM questions "
            "WHERE exam_id = :e AND embedding IS NOT NULL ORDER BY embedding <=> CAST(:v AS vector) LIMIT 1"
        ), {"v": json.dumps(vector), "e": exam_id}).first()
        if row is None:
            return None, 0.0
        return db.get(Question, row.id), float(row.sim)
    best, best_sim = None, 0.0
    for q in db.scalars(select(Question).where(Question.exam_id == exam_id, Question.embedding.is_not(None))):
        sim = cosine(vector, q.embedding)
        if sim > best_sim:
            best, best_sim = q, sim
    return best, best_sim


def update_after_scoring(db: Session, attempt: Attempt, rows: list[dict]) -> None:
    """rows: per question {question_id, topic_id, status, error_type|None}. Called once per scored attempt."""
    now = utcnow()
    per_topic: dict[int, list[int]] = {}
    for r in rows:
        if r["status"] == "unanswered" and r.get("error_type") is None:
            continue
        stats = per_topic.setdefault(r["topic_id"], [0, 0])
        if r["status"] != "unanswered":
            stats[0] += 1
            stats[1] += 1 if r["status"] == "correct" else 0
    for topic_id, (n, c) in per_topic.items():
        m = db.get(UserTopicMastery, (attempt.user_id, topic_id))
        if m is None:
            m = UserTopicMastery(user_id=attempt.user_id, topic_id=topic_id, attempts_count=0, correct_count=0)
            db.add(m)
        m.attempts_count = (m.attempts_count or 0) + n
        m.correct_count = (m.correct_count or 0) + c
        # Laplace-smoothed accuracy, so one lucky answer does not mean "mastered".
        m.mastery_score = round((m.correct_count + 1) / (m.attempts_count + 2), 4)
        m.last_seen_at = now
    for r in rows:
        if r.get("error_type"):
            db.add(UserMistake(user_id=attempt.user_id, question_id=r["question_id"], attempt_id=attempt.id,
                               topic_id=r["topic_id"], error_type=r["error_type"]))


def memory_profile(db: Session, user_id, exam_id) -> dict:
    """Compact summary of what we know about this user, sent to the report writer."""
    mastery = db.execute(
        select(Topic.name, UserTopicMastery.mastery_score, UserTopicMastery.attempts_count)
        .join(Topic, Topic.id == UserTopicMastery.topic_id)
        .where(UserTopicMastery.user_id == user_id, Topic.exam_id == exam_id)
    ).all()
    mistakes = db.execute(
        select(UserMistake.error_type, func.count()).where(UserMistake.user_id == user_id)
        .group_by(UserMistake.error_type)
    ).all()
    past = db.execute(
        select(Attempt.submitted_at, Attempt.score, Attempt.max_score, Attempt.percentile)
        .where(Attempt.user_id == user_id, Attempt.exam_id == exam_id, Attempt.status == "scored")
        .order_by(Attempt.submitted_at.desc()).limit(6)
    ).all()
    return {
        "topic_mastery": [{"topic": n, "mastery": s, "questions_seen": c} for n, s, c in mastery],
        "mistake_types_all_time": {t: c for t, c in mistakes},
        "recent_attempts_same_exam": [
            {"date": a.isoformat() if a else None, "score": s, "max_score": m, "percentile": p} for a, s, m, p in past
        ],
    }
