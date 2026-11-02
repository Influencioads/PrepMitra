import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import get_settings
from app.db import Base, Embedding, JSONType, TimestampMixin

EMBED_DIM = get_settings().embedding_dim


class Exam(TimestampMixin, Base):
    __tablename__ = "exams"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(80), unique=True)
    name: Mapped[str] = mapped_column(String(160))
    # central_govt | banking | civil_services | higher_education | campus_hiring
    category: Mapped[str] = mapped_column(String(40), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    # draft | published | hidden
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True)
    credits_required: Mapped[int] = mapped_column(Integer, default=1)
    is_free_trial: Mapped[bool] = mapped_column(Boolean, default=False)
    current_blueprint_version: Mapped[int | None] = mapped_column(Integer)

    blueprints: Mapped[list["ExamBlueprint"]] = relationship(back_populates="exam", cascade="all, delete-orphan")
    topics: Mapped[list["Topic"]] = relationship(back_populates="exam", cascade="all, delete-orphan")


class ExamBlueprint(TimestampMixin, Base):
    """Exact pattern every paper of an exam must follow. Versioned; papers pin a version."""

    __tablename__ = "exam_blueprints"
    __table_args__ = (UniqueConstraint("exam_id", "version"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    # [{key, name, question_count, marks_per_question, negative_marks, duration_min?, topic_ids?,
    #   question_types: {single: n, multi: n, numeric: n}}]
    sections: Mapped[list] = mapped_column(JSONType)
    duration_min: Mapped[int] = mapped_column(Integer)
    # {"unanswered": 0, "multi_partial": false, "numeric_tolerance": 0.01}
    marking_scheme: Mapped[dict] = mapped_column(JSONType, default=dict)
    # {"easy": 30, "medium": 50, "hard": 20} (percent)
    difficulty_mix: Mapped[dict] = mapped_column(JSONType)
    languages: Mapped[list] = mapped_column(JSONType, default=lambda: ["en"])
    calculator_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    section_switching_allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    instructions: Mapped[str] = mapped_column(Text, default="")

    exam: Mapped[Exam] = relationship(back_populates="blueprints")


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), index=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"))
    section_key: Mapped[str | None] = mapped_column(String(40))
    name: Mapped[str] = mapped_column(String(160))
    weightage: Mapped[float] = mapped_column(Float, default=1.0)

    exam: Mapped[Exam] = relationship(back_populates="topics")


class Question(TimestampMixin, Base):
    """Master question bank. English master copy lives on the row; other languages in question_translations."""

    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), index=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="RESTRICT"), index=True)
    subtopic: Mapped[str | None] = mapped_column(String(160))
    # single | multi | numeric
    type: Mapped[str] = mapped_column(String(10))
    # easy | medium | hard
    difficulty: Mapped[str] = mapped_column(String(10), index=True)
    # draft | verified | quarantined | rejected
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True)
    text: Mapped[str] = mapped_column(Text)
    options: Mapped[list] = mapped_column(JSONType, default=list)  # [{"key": "A", "text": "..."}]
    # single: "A"; multi: ["A","C"]; numeric: 12.5
    correct_answer: Mapped[dict] = mapped_column(JSONType)  # {"value": ...}
    explanation: Mapped[str] = mapped_column(Text, default="")
    shortcut: Mapped[str] = mapped_column(Text, default="")
    expected_time_sec: Mapped[int] = mapped_column(Integer, default=60)
    source: Mapped[str] = mapped_column(String(20), default="ai")  # ai | seed | manual
    verified_by: Mapped[str | None] = mapped_column(String(80))  # e.g. "ai:dual-solve", "expert:<user_id>"
    embedding = mapped_column(Embedding(EMBED_DIM), nullable=True)
    times_served: Mapped[int] = mapped_column(Integer, default=0)
    times_answered: Mapped[int] = mapped_column(Integer, default=0)
    times_correct: Mapped[int] = mapped_column(Integer, default=0)
    accuracy_rate: Mapped[float | None] = mapped_column(Float)
    report_count: Mapped[int] = mapped_column(Integer, default=0)
    sampled_for_review: Mapped[bool] = mapped_column(Boolean, default=False)
    generation_meta: Mapped[dict] = mapped_column(JSONType, default=dict)

    translations: Mapped[list["QuestionTranslation"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )


class QuestionTranslation(TimestampMixin, Base):
    __tablename__ = "question_translations"
    __table_args__ = (UniqueConstraint("question_id", "language"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), index=True)
    language: Mapped[str] = mapped_column(String(10))
    text: Mapped[str] = mapped_column(Text)
    options: Mapped[list] = mapped_column(JSONType, default=list)
    explanation: Mapped[str] = mapped_column(Text, default="")
    shortcut: Mapped[str] = mapped_column(Text, default="")
    # pending | back_translation_ok | approved | rejected
    review_status: Mapped[str] = mapped_column(String(30), default="pending")

    question: Mapped[Question] = relationship(back_populates="translations")


class QuestionGenerationLog(TimestampMixin, Base):
    """Every generation attempt, including discarded ones (PDF 6.1 step 7)."""

    __tablename__ = "question_generation_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), index=True)
    topic_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id", ondelete="SET NULL"))
    question_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("questions.id", ondelete="SET NULL"))
    # verified | rejected_verification | rejected_duplicate | rejected_invalid | error
    outcome: Mapped[str] = mapped_column(String(40), index=True)
    reason: Mapped[str] = mapped_column(Text, default="")
    payload: Mapped[dict] = mapped_column(JSONType, default=dict)


class Paper(TimestampMixin, Base):
    __tablename__ = "papers"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), index=True)
    blueprint_version: Mapped[int] = mapped_column(Integer)
    # ordered [{"question_id": "...", "section_key": "..."}]
    items: Mapped[list] = mapped_column(JSONType)
    # ready | assigned | retired
    status: Mapped[str] = mapped_column(String(20), default="ready", index=True)


class InterviewRole(TimestampMixin, Base):
    __tablename__ = "interview_roles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(80), unique=True)
    name: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text, default="")
    levels: Mapped[list] = mapped_column(JSONType, default=lambda: ["fresher", "1-3", "3-5"])
    duration_min: Mapped[int] = mapped_column(Integer, default=20)
    # {"criteria": [{"key": "role_knowledge", "label": "...", "description": "..."}]}
    rubric: Mapped[dict] = mapped_column(JSONType, default=dict)
    # {"persona": "...", "themes": {"role_technical": [...], ...}, "question_count": 10}
    prompt_config: Mapped[dict] = mapped_column(JSONType, default=dict)
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True)
    credits_required: Mapped[int] = mapped_column(Integer, default=1)


class Glossary(TimestampMixin, Base):
    __tablename__ = "glossary"
    __table_args__ = (UniqueConstraint("term", "language"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    term: Mapped[str] = mapped_column(String(160))
    language: Mapped[str] = mapped_column(String(10))
    approved_translation: Mapped[str] = mapped_column(String(300))
