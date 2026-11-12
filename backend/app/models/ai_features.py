"""Tables for the blueprint's student AI features ("solve once, store forever").

- `solutions`: the doubt solution store. A verified solution is served to every student who asks the same question.
- `ai_artifacts`: generated content cached by key and language: shared (user_id null: master notes, library topic
  decks, deep dives by question, the daily current affairs) or personal (personal notes, cheat-code cards...).
- `ai_chat_messages`: Ask Mitra tutor chat and Cheat Code Coach conversations.
- `personas`: versioned learning-profile JSON (snapshot after mocks, monthly deep persona).
"""

import uuid
from datetime import datetime

from sqlalchemy import Float, ForeignKey, Index, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base, JSONType, TimestampMixin, TZDateTime, utcnow


class Solution(TimestampMixin, Base):
    __tablename__ = "solutions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    # sha256 of the normalised question text + sorted options: exact match in one indexed lookup
    fingerprint: Mapped[str] = mapped_column(String(64), unique=True)
    normalized_text: Mapped[str] = mapped_column(Text)
    # sorted numbers in the question, so "Rs 1,331 at 10%" never matches "Rs 2,662 at 10%"
    number_signature: Mapped[str] = mapped_column(String(300), default="")
    options: Mapped[list] = mapped_column(JSONType, default=list)
    embedding: Mapped[list] = mapped_column(JSONType, default=list)
    subject: Mapped[str] = mapped_column(String(20), default="math")  # math | verbal | gk
    topic: Mapped[str | None] = mapped_column(String(160))
    difficulty: Mapped[str] = mapped_column(String(10), default="medium")
    answer: Mapped[str] = mapped_column(Text)
    # steps, shortcut, memory_hook, real_life_example, common_trap, practice_question, method (for new numbers)
    payload: Mapped[dict] = mapped_column(JSONType, default=dict)
    translations: Mapped[dict] = mapped_column(JSONType, default=dict)  # language -> payload in that language
    numeric_check: Mapped[str] = mapped_column(String(300), default="")
    solver_model: Mapped[str] = mapped_column(String(80), default="")
    prompt_version: Mapped[str] = mapped_column(String(20), default="v1")
    # code_checked | two_models | human | unverified
    verification: Mapped[str] = mapped_column(String(20), default="unverified")
    # live | hidden (error flags / thumbs-down) | disputed (sent to a human)
    status: Mapped[str] = mapped_column(String(20), default="live", index=True)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("solutions.id", ondelete="SET NULL"))
    times_served: Mapped[int] = mapped_column(Integer, default=0)
    thumbs_up: Mapped[int] = mapped_column(Integer, default=0)
    thumbs_down: Mapped[int] = mapped_column(Integer, default=0)
    error_flags: Mapped[int] = mapped_column(Integer, default=0)


class AiArtifact(Base):
    __tablename__ = "ai_artifacts"
    __table_args__ = (Index("ix_ai_artifacts_lookup", "kind", "cache_key", "language"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    # deep_dive | notes | master_notes | topic_deck | current_affairs | mistake_summary | cheat_card | hint |
    # writing_eval | rank_note
    kind: Mapped[str] = mapped_column(String(30))
    cache_key: Mapped[str] = mapped_column(String(300))
    language: Mapped[str] = mapped_column(String(10), default="en")
    title: Mapped[str] = mapped_column(String(300), default="")
    payload: Mapped[dict] = mapped_column(JSONType, default=dict)
    model: Mapped[str] = mapped_column(String(80), default="")
    # live | hidden | shared (a personal item the student allowed into the shared library)
    status: Mapped[str] = mapped_column(String(20), default="live")
    times_served: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow, index=True)


class AiChatMessage(Base):
    __tablename__ = "ai_chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    thread: Mapped[str] = mapped_column(String(20))  # tutor | coach
    session_id: Mapped[str | None] = mapped_column(String(64), index=True)
    role: Mapped[str] = mapped_column(String(10))  # user | assistant
    content: Mapped[str] = mapped_column(Text)
    meta: Mapped[dict] = mapped_column(JSONType, default=dict)
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow, index=True)


class Persona(Base):
    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(10))  # snapshot | deep | ultra
    version: Mapped[int] = mapped_column(Integer, default=1)
    data: Mapped[dict] = mapped_column(JSONType, default=dict)
    source_ref: Mapped[str | None] = mapped_column(String(64))  # latest attempt id the snapshot was built from
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow, index=True)
