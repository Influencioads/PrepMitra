"""Attempts, interviews, reports and the user-memory tables."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,

    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import get_settings
from app.db import Base, Embedding, JSONType, TimestampMixin, TZDateTime, utcnow

EMBED_DIM = get_settings().embedding_dim


class Attempt(TimestampMixin, Base):
    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), index=True)
    paper_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("papers.id", ondelete="RESTRICT"))
    language: Mapped[str] = mapped_column(String(10), default="en")
    started_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)
    # Server-controlled timer: the only source of truth for remaining time.
    deadline_at: Mapped[datetime] = mapped_column(TZDateTime, index=True)
    submitted_at: Mapped[datetime | None] = mapped_column(TZDateTime)
    # in_progress | submitted | scored | failed
    status: Mapped[str] = mapped_column(String(20), default="in_progress", index=True)
    submit_reason: Mapped[str | None] = mapped_column(String(20))  # user | timeout
    score: Mapped[float | None] = mapped_column(Float)
    max_score: Mapped[float | None] = mapped_column(Float)
    percentile: Mapped[float | None] = mapped_column(Float)
    credit_ledger_id: Mapped[int | None] = mapped_column(ForeignKey("credit_ledger.id", ondelete="SET NULL"))
    is_free_trial: Mapped[bool] = mapped_column(Boolean, default=False)
    tab_switch_count: Mapped[int] = mapped_column(Integer, default=0)
    anti_cheat_events: Mapped[list] = mapped_column(JSONType, default=list)

    answers: Mapped[list["AttemptAnswer"]] = relationship(back_populates="attempt", cascade="all, delete-orphan")


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"
    __table_args__ = (UniqueConstraint("attempt_id", "question_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("attempts.id", ondelete="CASCADE"), index=True)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id", ondelete="RESTRICT"))
    seq: Mapped[int] = mapped_column(Integer)
    section_key: Mapped[str] = mapped_column(String(40))
    answer: Mapped[dict | None] = mapped_column(JSONType)  # {"value": ...} or null when cleared
    is_correct: Mapped[bool | None] = mapped_column(Boolean)
    marks_awarded: Mapped[float | None] = mapped_column(Float)
    time_spent_sec: Mapped[int] = mapped_column(Integer, default=0)
    marked_for_review: Mapped[bool] = mapped_column(Boolean, default=False)
    visited: Mapped[bool] = mapped_column(Boolean, default=False)
    # Client-side monotonically increasing counter so retried/out-of-order autosaves never overwrite newer data.
    client_rev: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow, onupdate=utcnow)

    attempt: Mapped[Attempt] = relationship(back_populates="answers")


class InterviewSession(TimestampMixin, Base):
    __tablename__ = "interview_sessions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_roles.id", ondelete="RESTRICT"))
    level: Mapped[str] = mapped_column(String(20))
    language: Mapped[str] = mapped_column(String(10), default="en")
    mode: Mapped[str] = mapped_column(String(10), default="text")  # text | voice
    resume_ref: Mapped[str | None] = mapped_column(Text)  # resume text snapshot (PII-stripped)
    job_description: Mapped[str | None] = mapped_column(Text)
    # active | ended | evaluated | failed
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)
    stage: Mapped[str] = mapped_column(String(30), default="introduction")
    question_count: Mapped[int] = mapped_column(Integer, default=0)
    followup_count: Mapped[int] = mapped_column(Integer, default=0)
    target_questions: Mapped[int] = mapped_column(Integer, default=10)
    last_activity_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(TZDateTime)
    resumes_used: Mapped[int] = mapped_column(Integer, default=0)
    disconnected_at: Mapped[datetime | None] = mapped_column(TZDateTime)
    # Voice mode only: {"words": n, "speaking_sec": s, "fillers": {...}}; computed by code
    voice_metrics: Mapped[dict] = mapped_column(JSONType, default=dict)
    credit_ledger_id: Mapped[int | None] = mapped_column(ForeignKey("credit_ledger.id", ondelete="SET NULL"))

    turns: Mapped[list["InterviewTurn"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", order_by="InterviewTurn.seq"
    )


class InterviewTurn(Base):
    __tablename__ = "interview_turns"
    __table_args__ = (UniqueConstraint("session_id", "seq"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True)
    seq: Mapped[int] = mapped_column(Integer)
    stage: Mapped[str] = mapped_column(String(30))
    speaker: Mapped[str] = mapped_column(String(15))  # interviewer | candidate
    text: Mapped[str] = mapped_column(Text)
    audio_url: Mapped[str | None] = mapped_column(String(500))
    is_followup: Mapped[bool] = mapped_column(Boolean, default=False)
    # Candidate turns in voice mode: {"duration_sec": 12.5}
    meta: Mapped[dict] = mapped_column(JSONType, default=dict)
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)

    session: Mapped[InterviewSession] = relationship(back_populates="turns")


class Report(TimestampMixin, Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(15))  # exam | interview
    attempt_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("attempts.id", ondelete="CASCADE"), unique=True
    )
    interview_session_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"), unique=True
    )
    # processing | ready | failed
    status: Mapped[str] = mapped_column(String(20), default="processing", index=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    analytics: Mapped[dict] = mapped_column(JSONType, default=dict)  # computed by code
    report: Mapped[dict] = mapped_column(JSONType, default=dict)  # written by AI, validated by code
    pdf_path: Mapped[str | None] = mapped_column(String(500))
    share_token: Mapped[str | None] = mapped_column(String(64), unique=True)
    user_rating: Mapped[int | None] = mapped_column(Integer)
    rating_comment: Mapped[str | None] = mapped_column(Text)
    error: Mapped[str | None] = mapped_column(Text)
    generation_ms: Mapped[int | None] = mapped_column(Integer)
    credit_restored: Mapped[bool] = mapped_column(Boolean, default=False)
    share_expires_at: Mapped[datetime | None] = mapped_column(TZDateTime)


class UserTopicMastery(Base):
    __tablename__ = "user_topic_mastery"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True)
    mastery_score: Mapped[float] = mapped_column(Float, default=0.0)  # 0..1
    attempts_count: Mapped[int] = mapped_column(Integer, default=0)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    last_seen_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)
    # Evidence used by the mentor (classification needs more than accuracy): attempted = correct + wrong (+ partial).
    wrong_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    skipped_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    # Seconds spent on attempted questions, and the sum of their target times, so time ratio = spent / target.
    time_spent_sec: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    target_time_sec: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    # Exponentially weighted accuracy per session (mock or quiz): recent form, so improvement or decline shows.
    recent_accuracy: Mapped[float | None] = mapped_column(Float)
    previous_recent_accuracy: Mapped[float | None] = mapped_column(Float)
    sessions_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    # {"easy": [attempted, correct], "medium": [...], "hard": [...]}
    by_difficulty: Mapped[dict] = mapped_column(JSONType, default=dict)


class UserMistake(Base):
    __tablename__ = "user_mistakes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("attempts.id", ondelete="CASCADE"))
    topic_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id", ondelete="SET NULL"))
    # wrong | careless_easy | negative_guess | time_sink | skipped
    error_type: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)


class SeenQuestion(Base):
    __tablename__ = "seen_questions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
    first_seen_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)


class QuestionReport(TimestampMixin, Base):
    __tablename__ = "question_reports"
    __table_args__ = (UniqueConstraint("question_id", "user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    attempt_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("attempts.id", ondelete="SET NULL"))
    reason: Mapped[str] = mapped_column(String(30))  # wrong_answer | unclear | bad_translation | other
    language: Mapped[str] = mapped_column(String(10), default="en")
    details: Mapped[str] = mapped_column(Text, default="")
    # open | confirmed | rejected
    status: Mapped[str] = mapped_column(String(20), default="open", index=True)
    resolution: Mapped[str | None] = mapped_column(Text)
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))


class AiLesson(TimestampMixin, Base):
    """Global AI self-correction memory (PDF 6.4)."""

    __tablename__ = "ai_lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exam_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), index=True)
    topic_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id", ondelete="SET NULL"), index=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    lesson_text: Mapped[str] = mapped_column(Text)
    embedding = mapped_column(Embedding(EMBED_DIM), nullable=True)
    # question_report:<id> | verification_failure:<log id> | report_rating:<report id> | manual
    source_ref: Mapped[str] = mapped_column(String(80), default="manual")
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)


class AiUsage(Base):
    """Per-call AI token usage, for cost-per-attempt tracking."""

    __tablename__ = "ai_usage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose: Mapped[str] = mapped_column(String(40), index=True)
    model: Mapped[str] = mapped_column(String(60))
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    ref_id: Mapped[str | None] = mapped_column(String(64), index=True)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow, index=True)
