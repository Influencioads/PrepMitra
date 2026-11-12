"""Short practice outside the timed mocks: mistake-notebook revision and topic quizzes (mentor modules 4 and 8).

Questions are served without answers; the session is graded once, by code, and feeds the same topic evidence as a
mock. Topic quizzes prefer questions the student has never seen, at the student's current level for that topic.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import AppError, not_found
from app.db import utcnow
from app.models import Exam, NotebookEntry, PracticeSession, Question, SeenQuestion, StudyTask, Topic, User
from app.services import scoring
from app.services.mentor import config as cfg
from app.services.mentor import mastery, notebook
from app.services.mentor.planner import LEVEL_DIFFICULTY

MAX_ITEMS = 25


def _public(q: Question, entry_id: int | None, topic: Topic | None) -> dict:
    return {"question_id": str(q.id), "entry_id": entry_id, "type": q.type, "difficulty": q.difficulty,
            "topic": topic.name if topic else None, "text": q.text, "options": q.options,
            "target_time_sec": cfg.target_time({}, topic.section_key if topic else "", q.difficulty,
                                               q.expected_time_sec)}


def _task(db: Session, user: User, task_id: int | None) -> StudyTask | None:
    if task_id is None:
        return None
    t = db.get(StudyTask, task_id)
    if t is None or t.user_id != user.id:
        raise not_found("Task")
    return t


def _session_out(db: Session, s: PracticeSession, qs: list[Question], entries: dict[uuid.UUID, int]) -> dict:
    topics = {t.id: t for t in db.scalars(select(Topic).where(Topic.id.in_({q.topic_id for q in qs})))}
    return {"id": str(s.id), "kind": s.kind, "status": s.status, "created_at": s.created_at,
            "questions": [_public(q, entries.get(q.id), topics.get(q.topic_id)) for q in qs]}


def start_mistake_review(db: Session, user: User, count: int, topic_id: int | None, task_id: int | None) -> dict:
    count = max(1, min(count, MAX_ITEMS))
    task = _task(db, user, task_id)
    base = select(NotebookEntry).where(NotebookEntry.user_id == user.id, NotebookEntry.status == "active")
    if topic_id is not None:
        base = base.where(NotebookEntry.topic_id == topic_id)
    due = db.scalars(base.where(NotebookEntry.next_review_at <= utcnow())
                     .order_by(NotebookEntry.next_review_at).limit(count)).all()
    if len(due) < count:  # top up with the cards that went wrong most, earliest step first
        more = db.scalars(base.where(NotebookEntry.id.not_in([e.id for e in due] or [-1]))
                          .order_by(NotebookEntry.box, NotebookEntry.times_wrong.desc()).limit(count - len(due))).all()
        due = list(due) + list(more)
    if not due:
        raise AppError(409, "notebook_empty", "Your mistake notebook has nothing to revise yet")
    qs = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_([e.question_id for e in due])))}
    s = PracticeSession(user_id=user.id, kind="mistake_review", task_id=task.id if task else None,
                        goal_id=task.goal_id if task else None, topic_id=topic_id,
                        items=[{"question_id": str(e.question_id), "entry_id": e.id} for e in due], status="open",
                        results=[])
    db.add(s)
    db.flush()
    if task:
        task.practice_session_id = s.id
    db.commit()
    return _session_out(db, s, [qs[e.question_id] for e in due], {e.question_id: e.id for e in due})


def start_topic_quiz(db: Session, user: User, topic_id: int, count: int, task_id: int | None,
                     level: str | None) -> dict:
    count = max(1, min(count, MAX_ITEMS))
    task = _task(db, user, task_id)
    topic = db.get(Topic, topic_id)
    if topic is None or db.get(Exam, topic.exam_id).status != "published":
        raise not_found("Topic")
    key = mastery.topic_key(topic.section_key, topic.name)
    same = [t.id for t in db.scalars(select(Topic).where(Topic.name == topic.name))
            if mastery.topic_key(t.section_key, t.name) == key]
    if level is None:
        ev = mastery.pooled_evidence(db, user.id).get(key)
        level = mastery.classify(ev)["level"]
    want = LEVEL_DIFFICULTY.get(level, "medium")
    seen = select(SeenQuestion.question_id).where(SeenQuestion.user_id == user.id)
    pool = select(Question).where(Question.topic_id.in_(same), Question.status == "verified")
    picked: list[Question] = list(db.scalars(pool.where(Question.difficulty == want, Question.id.not_in(seen))
                                             .order_by(Question.times_served, Question.id).limit(count)))
    if len(picked) < count:
        picked += db.scalars(pool.where(Question.id.not_in(seen), Question.id.not_in([q.id for q in picked] or [None]))
                             .order_by(Question.times_served, Question.id).limit(count - len(picked))).all()
    if len(picked) < count:  # bank exhausted for this student: repeats are better than no practice
        picked += db.scalars(pool.where(Question.id.not_in([q.id for q in picked] or [None]))
                             .order_by(Question.id).limit(count - len(picked))).all()
    if not picked:
        raise AppError(409, "no_questions", "No verified questions are available for this topic yet")
    for q in picked:
        if db.get(SeenQuestion, (user.id, q.id)) is None:
            db.add(SeenQuestion(user_id=user.id, question_id=q.id))
        q.times_served = (q.times_served or 0) + 1
    s = PracticeSession(user_id=user.id, kind="topic_quiz", task_id=task.id if task else None,
                        goal_id=task.goal_id if task else None, topic_id=topic_id,
                        items=[{"question_id": str(q.id), "entry_id": None} for q in picked], status="open", results=[])
    db.add(s)
    db.flush()
    if task:
        task.practice_session_id = s.id
    db.commit()
    return _session_out(db, s, picked, {})


def submit(db: Session, user: User, session_id: uuid.UUID, answers: list[dict]) -> dict:
    s = db.get(PracticeSession, session_id)
    if s is None or s.user_id != user.id:
        raise not_found("Practice session")
    if s.status != "open":
        raise AppError(409, "session_closed", "This practice session was already submitted")
    given = {str(a["question_id"]): a for a in answers}
    qids = [uuid.UUID(i["question_id"]) for i in s.items]
    qs = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(qids)))}
    topics = {t.id: t for t in db.scalars(select(Topic).where(Topic.id.in_({q.topic_id for q in qs.values()})))}
    results, evidence = [], []
    for item in s.items:
        q = qs.get(uuid.UUID(item["question_id"]))
        if q is None:
            continue
        a = given.get(item["question_id"], {})
        status, _ = scoring.score_question(q.type, q.correct_answer["value"], {"value": a.get("answer")}, 1.0, 0.0, {})
        t = int(a.get("time_spent_sec") or 0)
        section = topics[q.topic_id].section_key if q.topic_id in topics else None
        target = cfg.target_time({}, section or "", q.difficulty, q.expected_time_sec)
        evidence.append({"topic_id": q.topic_id, "status": status, "difficulty": q.difficulty, "time_sec": t,
                         "target_sec": target})
        if item.get("entry_id"):
            e = db.get(NotebookEntry, item["entry_id"])
            if e is not None and e.user_id == user.id and status != "unanswered":
                notebook.review(e, status == "correct")
        results.append({"question_id": item["question_id"], "entry_id": item.get("entry_id"), "status": status,
                        "your_answer": a.get("answer"), "correct_answer": q.correct_answer["value"],
                        "explanation": q.explanation, "shortcut": q.shortcut, "time_sec": t, "target_sec": target})
    mastery.record(db, user.id, evidence)
    s.status, s.submitted_at, s.results = "submitted", utcnow(), results
    s.correct = sum(1 for r in results if r["status"] == "correct")
    if s.task_id:
        task = db.get(StudyTask, s.task_id)
        if task is not None and task.status == "pending":
            task.status, task.completed_at = "done", utcnow()
            task.actual_minutes = max(1, round(sum(r["time_sec"] for r in results) / 60))
    db.commit()
    attempted = [r for r in results if r["status"] != "unanswered"]
    return {"id": str(s.id), "kind": s.kind, "status": s.status, "correct": s.correct, "total": len(results),
            "accuracy": round(s.correct / len(attempted), 4) if attempted else None, "results": results}
