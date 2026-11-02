import io
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.errors import AppError
from app.db import utcnow
from app.models import (
    Attempt,
    Consent,
    CreditLedger,
    InterviewSession,
    Order,
    RefreshToken,
    Report,
    User,
)
from app.services.providers import get_storage

POLICY_VERSION = "2026-10-v1"
CONSENT_TYPES = ("data_processing", "recruiter_sharing", "marketing")


def age_on(dob: date, today: date) -> int:
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def current_consents(db: Session, user_id) -> dict[str, bool]:
    """Latest decision per consent type; recruiter sharing defaults OFF."""
    result = {t: False for t in CONSENT_TYPES}
    rows = db.scalars(select(Consent).where(Consent.user_id == user_id).order_by(Consent.granted_at, Consent.id))
    for c in rows:
        result[c.consent_type] = c.granted
    return result


def missing_fields(db: Session, user: User) -> list[str]:
    """Fields required before the first attempt (PDF 5.1 AC) plus our 18+ check and data consent."""
    missing = []
    if not user.name:
        missing.append("name")
    if not user.dob:
        missing.append("dob")
    if not user.preferred_language:
        missing.append("preferred_language")
    p = user.profile
    if not (p and (p.target_exam_ids or p.target_role_ids)):
        missing.append("target_exam_or_role")
    if not current_consents(db, user.id)["data_processing"]:
        missing.append("data_processing_consent")
    return missing


def require_complete_profile(db: Session, user: User) -> None:
    missing = missing_fields(db, user)
    if missing:
        raise AppError(409, "profile_incomplete", "Complete your profile first: " + ", ".join(missing))


def update_me(db: Session, user: User, data: dict) -> User:
    s = get_settings()
    if "dob" in data and data["dob"] is not None:
        today = utcnow().date()
        if data["dob"] > today:
            raise AppError(422, "invalid_dob", "Date of birth cannot be in the future")
        if age_on(data["dob"], today) < s.min_age_years:
            raise AppError(403, "underage", f"You must be at least {s.min_age_years} years old to use this service")
    if data.get("email"):
        clash = db.scalar(select(User).where(User.email == data["email"], User.id != user.id))
        if clash:
            raise AppError(409, "email_taken", "This email is already linked to another account")

    for f in ("name", "dob", "state", "preferred_language", "email"):
        if f in data:
            setattr(user, f, data[f])
    for f in ("education", "stream", "target_exam_ids", "target_role_ids", "experience_years"):
        if f in data:
            setattr(user.profile, f, data[f])
    db.commit()
    return user


def record_consents(db: Session, user: User, choices: dict[str, bool]) -> dict[str, bool]:
    if not choices.get("data_processing"):
        raise AppError(422, "consent_required", "Consent to data processing is required to use the service")
    for t in CONSENT_TYPES:
        db.add(Consent(user_id=user.id, consent_type=t, granted=bool(choices.get(t)), policy_version=POLICY_VERSION))
    db.commit()
    return current_consents(db, user.id)


def withdraw_consent(db: Session, user: User, consent_type: str) -> None:
    if consent_type not in CONSENT_TYPES:
        raise AppError(422, "invalid_consent", "Unknown consent type")
    db.add(Consent(user_id=user.id, consent_type=consent_type, granted=False, policy_version=POLICY_VERSION))
    db.commit()


ALLOWED_RESUME = {".pdf": b"%PDF", ".docx": b"PK\x03\x04"}


def save_resume(db: Session, user: User, filename: str, data: bytes) -> None:
    s = get_settings()
    if len(data) > s.max_resume_bytes:
        raise AppError(413, "file_too_large", "Resume must be 5 MB or smaller")
    suffix = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    magic = ALLOWED_RESUME.get(suffix)
    if magic is None or not data.startswith(magic):
        raise AppError(415, "unsupported_file", "Upload a PDF or DOCX file")

    text = _extract_text(suffix, data)
    storage = get_storage()
    if user.profile.resume_path:
        storage.delete(user.profile.resume_path)
    user.profile.resume_path = storage.save("resumes", data, suffix)
    user.profile.resume_text = text[:20000]
    db.commit()


def _extract_text(suffix: str, data: bytes) -> str:
    try:
        if suffix == ".pdf":
            from pypdf import PdfReader

            return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(data)).pages)
        from docx import Document

        return "\n".join(p.text for p in Document(io.BytesIO(data)).paragraphs)
    except Exception:
        raise AppError(422, "unreadable_file", "We could not read this file. Try another PDF or DOCX.")


def delete_resume(db: Session, user: User) -> None:
    if user.profile.resume_path:
        get_storage().delete(user.profile.resume_path)
    user.profile.resume_path = None
    user.profile.resume_text = None
    db.commit()


def export_data(db: Session, user: User) -> dict:
    """DPDP right to access: everything we hold about the user, as JSON."""
    p = user.profile
    attempts = db.scalars(select(Attempt).where(Attempt.user_id == user.id)).all()
    reports = db.scalars(select(Report).where(Report.user_id == user.id)).all()
    interviews = db.scalars(select(InterviewSession).where(InterviewSession.user_id == user.id)).all()
    orders = db.scalars(select(Order).where(Order.user_id == user.id)).all()
    ledger = db.scalars(select(CreditLedger).where(CreditLedger.user_id == user.id)).all()
    consents = db.scalars(select(Consent).where(Consent.user_id == user.id)).all()
    return {
        "exported_at": utcnow().isoformat(),
        "account": {
            "id": str(user.id), "phone": user.phone, "email": user.email, "name": user.name,
            "dob": user.dob.isoformat() if user.dob else None, "state": user.state,
            "preferred_language": user.preferred_language, "created_at": user.created_at.isoformat(),
        },
        "profile": {
            "education": p.education, "stream": p.stream, "target_exam_ids": p.target_exam_ids,
            "target_role_ids": p.target_role_ids, "experience_years": p.experience_years,
            "resume_text": p.resume_text,
        },
        "consents": [
            {"type": c.consent_type, "granted": c.granted, "policy_version": c.policy_version, "at": c.granted_at.isoformat()}
            for c in consents
        ],
        "attempts": [
            {"id": str(a.id), "exam_id": str(a.exam_id), "status": a.status, "score": a.score,
             "max_score": a.max_score, "started_at": a.started_at.isoformat()}
            for a in attempts
        ],
        "reports": [{"id": str(r.id), "kind": r.kind, "status": r.status, "report": r.report} for r in reports],
        "interviews": [
            {"id": str(i.id), "role_id": str(i.role_id), "status": i.status,
             "transcript": [{"speaker": t.speaker, "text": t.text} for t in i.turns]}
            for i in interviews
        ],
        "orders": [{"id": str(o.id), "amount_paise": o.amount_paise, "status": o.status} for o in orders],
        "credit_ledger": [{"delta": c.delta, "reason": c.reason, "at": c.created_at.isoformat()} for c in ledger],
    }


def delete_account(db: Session, user: User) -> None:
    """Scrubs personal data immediately (PDF AC: within 30 days) and revokes all sessions.

    Anonymised attempt rows are kept so platform percentiles stay stable; they no longer link to a person.
    Orders keep amounts for GST/accounting retention.
    """
    if user.profile.resume_path:
        get_storage().delete(user.profile.resume_path)
    user.phone = user.email = user.google_sub = user.firebase_uid = user.name = user.state = None
    user.dob = None
    user.status = "deleted"
    user.deleted_at = utcnow()
    p = user.profile
    p.resume_path = p.resume_text = p.stream = None
    p.target_exam_ids, p.target_role_ids = [], []
    for s in db.scalars(select(InterviewSession).where(InterviewSession.user_id == user.id)):
        s.resume_ref = s.job_description = None
        for t in s.turns:
            if t.speaker == "candidate":
                t.text = "[deleted]"
    for t in db.scalars(select(RefreshToken).where(RefreshToken.user_id == user.id, RefreshToken.revoked_at.is_(None))):
        t.revoked_at = utcnow()
    db.add(Consent(user_id=user.id, consent_type="recruiter_sharing", granted=False, policy_version=POLICY_VERSION))
    db.commit()
