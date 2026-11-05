"""Mentor updates that ride on the existing exam flow (called from attempts.score_attempt, same transaction)."""

from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import utcnow
from app.models import Attempt, ExamGoal, StudyTask
from app.services.mentor import analysis, clock, notebook


def after_scoring(db: Session, a: Attempt) -> None:
    rows, _sections, _scheme = analysis.build_rows(db, a)
    notebook.record_attempt(db, a, rows)
    goal = db.scalar(select(ExamGoal).where(ExamGoal.user_id == a.user_id, ExamGoal.exam_id == a.exam_id,
                                            ExamGoal.status == "active"))
    if goal is None:
        return
    # The planned mock nearest to today counts as done (a day early or late still counts).
    today = clock.today(clock.user_tz(db, a.user_id))
    tasks = db.scalars(select(StudyTask).where(
        StudyTask.goal_id == goal.id, StudyTask.kind == "mock_test", StudyTask.status == "pending",
        StudyTask.task_date >= today - timedelta(days=3), StudyTask.task_date <= today + timedelta(days=3))).all()
    if tasks:
        t = min(tasks, key=lambda t: abs((t.task_date - today).days))
        t.status, t.completed_at = "done", utcnow()
        t.actual_minutes = int(((a.submitted_at or utcnow()) - a.started_at).total_seconds() // 60)
