import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from app.core.languages import is_supported


class Page(BaseModel):
    items: list[Any]
    total: int
    limit: int
    offset: int


class OkOut(BaseModel):
    ok: bool = True


# ---- attempts ---------------------------------------------------------------------------------------------------
class AttemptStartIn(BaseModel):
    exam_id: uuid.UUID
    language: str = "en"

    @field_validator("language")
    @classmethod
    def _lang(cls, v):
        if not is_supported(v):
            raise ValueError("Unsupported language")
        return v


class AnswerItem(BaseModel):
    question_id: uuid.UUID
    # single: "B" | multi: ["A","C"] | numeric: 12.5 | null clears the response. Omit to leave the answer unchanged.
    answer: str | list[str] | float | None = None
    marked_for_review: bool | None = None
    visited: bool | None = None
    time_spent_sec: int | None = Field(default=None, ge=0)
    # Monotonic per-question revision from the client; stale or repeated revisions are ignored (idempotent retries).
    client_rev: int = Field(ge=1)


class AnswersIn(BaseModel):
    answers: list[AnswerItem] = Field(min_length=1, max_length=300)

    def to_items(self) -> list[dict]:
        return [a.model_dump(exclude_unset=True) | {"question_id": a.question_id, "client_rev": a.client_rev}
                for a in self.answers]


class AnswersOut(BaseModel):
    saved: int
    ignored_stale: int
    remaining_seconds: int
    server_time: datetime


class EventItem(BaseModel):
    type: str
    at: datetime | None = None
    meta: dict = Field(default_factory=dict)


class EventsIn(BaseModel):
    events: list[EventItem] = Field(min_length=1, max_length=100)


class QuestionReportIn(BaseModel):
    reason: Literal["wrong_answer", "unclear", "bad_translation", "other"]
    details: str = Field(default="", max_length=2000)
    language: str = "en"
    attempt_id: uuid.UUID | None = None


# ---- reports ----------------------------------------------------------------------------------------------------
class RatingIn(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=1000)


class ReportOut(BaseModel):
    id: uuid.UUID
    kind: str
    status: Literal["processing", "ready", "failed"]
    language: str
    attempt_id: uuid.UUID | None
    interview_session_id: uuid.UUID | None
    analytics: dict | None
    report: dict | None
    pdf_url: str | None
    share_url: str | None
    share_api_url: str | None
    user_rating: int | None
    error: str | None
    credit_restored: bool
    created_at: datetime
    poll_after_seconds: int | None


# ---- interviews -------------------------------------------------------------------------------------------------
class InterviewStartIn(BaseModel):
    role_id: uuid.UUID
    level: str
    language: str = "en"
    mode: Literal["text", "voice"] = "text"
    job_description: str | None = Field(default=None, max_length=8000)
    resume_text: str | None = Field(default=None, max_length=20000)
    use_profile_resume: bool = True

    @field_validator("language")
    @classmethod
    def _lang(cls, v):
        if not is_supported(v):
            raise ValueError("Unsupported language")
        return v


class InterviewAnswerIn(BaseModel):
    text: str = Field(min_length=1, max_length=8000)
    duration_sec: float | None = Field(default=None, ge=0, le=1800)


class TurnOut(BaseModel):
    seq: int
    speaker: str
    stage: str
    text: str
    is_followup: bool
    audio_url: str | None = None


class InterviewTurnOut(BaseModel):
    done: bool
    turn: TurnOut
    report_id: uuid.UUID | None


# ---- payments ---------------------------------------------------------------------------------------------------
class OrderIn(BaseModel):
    plan_code: str = Field(min_length=2, max_length=30)
    platform: Literal["web", "android", "ios"] = "web"


class OrderVerifyIn(BaseModel):
    razorpay_payment_id: str = Field(min_length=3, max_length=80)
    razorpay_order_id: str | None = None
    razorpay_signature: str = Field(min_length=10, max_length=200)


class IapVerifyIn(BaseModel):
    platform: Literal["android", "ios"]
    product_id: str
    purchase_token: str


# ---- notifications / devices --------------------------------------------------------------------------------------
class DeviceIn(BaseModel):
    platform: Literal["android", "ios", "web"]
    token: str = Field(min_length=10, max_length=512)
    app_version: str | None = Field(default=None, max_length=30)
    locale: str | None = Field(default=None, max_length=10)


class ClientEventIn(BaseModel):
    name: str
    props: dict = Field(default_factory=dict)
