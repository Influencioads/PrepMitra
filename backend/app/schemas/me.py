import uuid
from datetime import date

from pydantic import BaseModel, Field, field_validator

from app.core.languages import is_supported

EDUCATION_LEVELS = ("12th_pass", "graduate", "postgraduate")


class OtpSendIn(BaseModel):
    phone: str = Field(min_length=10, max_length=16)


class OtpSendOut(BaseModel):
    sent: bool = True
    expires_in: int
    dev_otp: str | None = None  # only populated when APP_ENV=development


class OtpVerifyIn(BaseModel):
    phone: str = Field(min_length=10, max_length=16)
    code: str = Field(pattern=r"^\d{4,8}$")


class GoogleIn(BaseModel):
    id_token: str = Field(min_length=10)


class RefreshIn(BaseModel):
    refresh_token: str = Field(min_length=20)


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    is_new_user: bool = False


class ProfileOut(BaseModel):
    education: str | None
    stream: str | None
    target_exam_ids: list[str]
    target_role_ids: list[str]
    experience_years: int | None
    has_resume: bool


class MeOut(BaseModel):
    id: uuid.UUID
    phone: str | None
    email: str | None
    name: str | None
    dob: date | None
    state: str | None
    preferred_language: str
    is_admin: bool
    admin_role: str | None
    profile: ProfileOut
    consents: dict[str, bool]
    profile_complete: bool
    missing_fields: list[str]


class MeUpdateIn(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    dob: date | None = None
    state: str | None = Field(default=None, max_length=80)
    preferred_language: str | None = None
    email: str | None = Field(default=None, max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    education: str | None = None
    stream: str | None = Field(default=None, max_length=80)
    target_exam_ids: list[str] | None = Field(default=None, max_length=20)
    target_role_ids: list[str] | None = Field(default=None, max_length=20)
    experience_years: int | None = Field(default=None, ge=0, le=50)

    @field_validator("preferred_language")
    @classmethod
    def _lang(cls, v):
        if v is not None and not is_supported(v):
            raise ValueError("Unsupported language")
        return v

    @field_validator("education")
    @classmethod
    def _edu(cls, v):
        if v is not None and v not in EDUCATION_LEVELS:
            raise ValueError(f"education must be one of {EDUCATION_LEVELS}")
        return v


class ConsentIn(BaseModel):
    data_processing: bool
    recruiter_sharing: bool = False
    marketing: bool = False
