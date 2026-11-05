import re
import uuid
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class GoalIn(BaseModel):
    exam_id: str = Field(description="Exam UUID or slug, e.g. ibps-po-prelims")
    exam_date: date
    daily_minutes: int = Field(default=120, ge=15, le=720)
    rest_weekday: int | None = Field(default=None, ge=0, le=6, description="0 = Monday ... 6 = Sunday")


class GoalPatch(BaseModel):
    exam_date: date | None = None
    daily_minutes: int | None = Field(default=None, ge=15, le=720)
    rest_weekday: int | None = Field(default=None, ge=0, le=6)
    clear_rest_day: bool = False


class PlanGenerateIn(BaseModel):
    goal_id: int


class TaskPatch(BaseModel):
    status: Literal["done", "skipped", "pending"]
    actual_minutes: int | None = Field(default=None, ge=0, le=720)


MISTAKE_TYPE = Literal["concept", "calculation", "misread", "wrong_formula", "guessing", "time_pressure",
                       "option_confusion"]


class NotebookPatch(BaseModel):
    mistake_type: MISTAKE_TYPE | None = None
    clear_mistake_type: bool = False
    bookmarked: bool | None = None
    note: str | None = Field(default=None, max_length=2000)


class BookmarkIn(BaseModel):
    question_id: uuid.UUID
    attempt_id: uuid.UUID | None = None


class MistakeQuizIn(BaseModel):
    count: int = Field(default=10, ge=1, le=25)
    topic_id: int | None = None
    task_id: int | None = None


class TopicQuizIn(BaseModel):
    topic_id: int
    count: int = Field(default=10, ge=1, le=25)
    level: Literal["basic", "intermediate", "advanced"] | None = None
    task_id: int | None = None


class PracticeAnswer(BaseModel):
    question_id: uuid.UUID
    answer: str | list[str] | float | None = None
    time_spent_sec: int = Field(default=0, ge=0, le=3600)


class PracticeSubmitIn(BaseModel):
    answers: list[PracticeAnswer] = Field(max_length=25)


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    goal_id: int | None = None


_HHMM = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


class NotificationPrefsIn(BaseModel):
    push_enabled: bool | None = None
    email_enabled: bool | None = None
    morning_enabled: bool | None = None
    morning_time: str | None = None
    afternoon_enabled: bool | None = None
    afternoon_time: str | None = None
    evening_enabled: bool | None = None
    evening_time: str | None = None
    countdown_enabled: bool | None = None
    mock_reminders_enabled: bool | None = None
    max_per_day: int | None = Field(default=None, ge=1, le=5)
    timezone: str | None = Field(default=None, max_length=40)

    @field_validator("morning_time", "afternoon_time", "evening_time")
    @classmethod
    def _hhmm(cls, v):
        if v is not None and not _HHMM.match(v):
            raise ValueError("Use 24-hour HH:MM")
        return v

    @field_validator("timezone")
    @classmethod
    def _tz(cls, v):
        if v is None:
            return v
        try:
            from zoneinfo import ZoneInfo

            ZoneInfo(v)
        except Exception:
            raise ValueError("Unknown time zone")
        return v
