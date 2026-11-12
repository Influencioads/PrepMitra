"""AI Personal Exam Mentor: exam goals, the study plan, the mistake notebook, practice sessions, reminders, chat.

Per-question results already live in `attempt_answers` and topic evidence in `user_topic_mastery`; these tables only
hold what the mentor adds on top. Every row belongs to one user and is always read through that user's id.
"""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base, JSONType, TimestampMixin, TZDateTime, utcnow


class ExamGoal(TimestampMixin, Base):
    """One upcoming exam a student is preparing for. A student can have several, each with its own plan."""

    __tablename__ = "exam_goals"
    __table_args__ = (UniqueConstraint("user_id", "exam_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"))
    exam_date: Mapped[date] = mapped_column(Date)
    daily_minutes: Mapped[int] = mapped_column(Integer, default=120)
    # 0 = Monday ... 6 = Sunday; null = study every day
    rest_weekday: Mapped[int | None] = mapped_column(Integer)
    # active | archived
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)
    plan_version: Mapped[int] = mapped_column(Integer, default=0)
    plan_generated_at: Mapped[datetime | None] = mapped_column(TZDateTime)
    # Why the plan looks the way it does: priorities, trade-offs, phase dates, optional AI note.
    plan_meta: Mapped[dict] = mapped_column(JSONType, default=dict)


class StudyTask(Base):
    """One block of work on one day of a plan. Regenerating a plan supersedes pending future tasks only."""

    __tablename__ = "study_tasks"
    __table_args__ = (
        Index("ix_study_tasks_user_date", "user_id", "task_date"),
        Index("ix_study_tasks_goal_status", "goal_id", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    goal_id: Mapped[int] = mapped_column(ForeignKey("exam_goals.id", ondelete="CASCADE"))
    plan_version: Mapped[int] = mapped_column(Integer)
    task_date: Mapped[date] = mapped_column(Date)
    seq: Mapped[int] = mapped_column(Integer, default=0)
    # learn | practice | revision | mistake_review | sectional_test | mock_test | mock_review | formula_revision | rest
    kind: Mapped[str] = mapped_column(String(20))
    topic_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id", ondelete="SET NULL"))
    section_key: Mapped[str | None] = mapped_column(String(40))
    title: Mapped[str] = mapped_column(String(200))
    detail: Mapped[str] = mapped_column(Text, default="")
    level: Mapped[str | None] = mapped_column(String(12))  # basic | intermediate | advanced
    minutes: Mapped[int] = mapped_column(Integer, default=30)
    target_questions: Mapped[int | None] = mapped_column(Integer)
    priority: Mapped[str | None] = mapped_column(String(12))  # high | medium | maintenance | low
    reason: Mapped[str] = mapped_column(Text, default="")
    # pending | done | skipped | superseded
    status: Mapped[str] = mapped_column(String(12), default="pending")
    completed_at: Mapped[datetime | None] = mapped_column(TZDateTime)
    actual_minutes: Mapped[int | None] = mapped_column(Integer)
    practice_session_id: Mapped[uuid.UUID | None] = mapped_column(Uuid)
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)


class NotebookEntry(TimestampMixin, Base):
    """The student's mistake notebook: one row per question that went wrong, was skipped, was slow or was bookmarked.

    `user_mistakes` stays the per-attempt event log; this row is the living card with its spaced-revision state.
    """

    __tablename__ = "mistake_notebook"
    __table_args__ = (
        UniqueConstraint("user_id", "question_id"),
        Index("ix_mistake_notebook_due", "user_id", "status", "next_review_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"))
    topic_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id", ondelete="SET NULL"))
    last_attempt_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("attempts.id", ondelete="SET NULL"))
    last_answer: Mapped[dict | None] = mapped_column(JSONType)  # {"value": ...} as the student answered it
    reasons: Mapped[list] = mapped_column(JSONType, default=list)  # wrong | skipped | slow | bookmark
    # concept | calculation | misread | wrong_formula | guessing | time_pressure | option_confusion
    auto_mistake_type: Mapped[str | None] = mapped_column(String(30))
    mistake_type: Mapped[str | None] = mapped_column(String(30))  # set by the student; wins over the auto guess
    times_wrong: Mapped[int] = mapped_column(Integer, default=0)
    times_skipped: Mapped[int] = mapped_column(Integer, default=0)
    times_slow: Mapped[int] = mapped_column(Integer, default=0)
    revision_correct: Mapped[int] = mapped_column(Integer, default=0)
    revision_wrong: Mapped[int] = mapped_column(Integer, default=0)
    box: Mapped[int] = mapped_column(Integer, default=0)  # spaced-revision step (index into the interval list)
    next_review_at: Mapped[datetime | None] = mapped_column(TZDateTime)
    last_reviewed_at: Mapped[datetime | None] = mapped_column(TZDateTime)
    last_time_sec: Mapped[int] = mapped_column(Integer, default=0)
    bookmarked: Mapped[bool] = mapped_column(Boolean, default=False)
    note: Mapped[str] = mapped_column(Text, default="")
    # active | resolved
    status: Mapped[str] = mapped_column(String(12), default="active")


class PracticeSession(Base):
    """A short quiz outside the timed mocks (mistake revision or a topic quiz). Graded once, by code."""

    __tablename__ = "practice_sessions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(20))  # mistake_review | topic_quiz
    goal_id: Mapped[int | None] = mapped_column(ForeignKey("exam_goals.id", ondelete="SET NULL"))
    task_id: Mapped[int | None] = mapped_column(ForeignKey("study_tasks.id", ondelete="SET NULL"))
    topic_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id", ondelete="SET NULL"))
    items: Mapped[list] = mapped_column(JSONType, default=list)  # [{"question_id": "...", "entry_id": n|null}]
    status: Mapped[str] = mapped_column(String(12), default="open")  # open | submitted
    results: Mapped[list] = mapped_column(JSONType, default=list)
    correct: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)
    submitted_at: Mapped[datetime | None] = mapped_column(TZDateTime)


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    push_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    email_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    morning_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    morning_time: Mapped[str] = mapped_column(String(5), default="07:30")
    afternoon_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    afternoon_time: Mapped[str] = mapped_column(String(5), default="16:00")
    evening_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    evening_time: Mapped[str] = mapped_column(String(5), default="20:30")
    countdown_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    mock_reminders_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    max_per_day: Mapped[int] = mapped_column(Integer, default=3)
    timezone: Mapped[str] = mapped_column(String(40), default="Asia/Kolkata")
    updated_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow, onupdate=utcnow)


class MentorMessage(Base):
    __tablename__ = "mentor_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    goal_id: Mapped[int | None] = mapped_column(ForeignKey("exam_goals.id", ondelete="SET NULL"))
    role: Mapped[str] = mapped_column(String(10))  # student | mentor
    content: Mapped[str] = mapped_column(Text)
    meta: Mapped[dict] = mapped_column(JSONType, default=dict)
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)


class MentorInsight(Base):
    """Cached AI wording (attempt coaching notes, plan notes) so the same facts are not paid for twice."""

    __tablename__ = "mentor_insights"
    __table_args__ = (UniqueConstraint("user_id", "kind", "ref_key"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(String(30))
    ref_key: Mapped[str] = mapped_column(String(80))
    payload: Mapped[dict] = mapped_column(JSONType, default=dict)
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)
