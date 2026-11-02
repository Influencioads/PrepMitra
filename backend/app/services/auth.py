import re
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.errors import AppError
from app.core.security import (
    create_access_token,
    generate_otp,
    hash_secret,
    new_refresh_token,
)
from app.db import utcnow
from app.models import AdminUser, AnalyticsEvent, OtpCode, RefreshToken, User, UserProfile
from app.services.providers import get_sms_provider

_PHONE_RE = re.compile(r"^[6-9]\d{9}$")


def normalize_phone(raw: str) -> str:
    """Accepts 10-digit Indian mobiles with optional +91/91/0 prefix; returns +91XXXXXXXXXX."""
    digits = re.sub(r"[\s\-()]", "", raw)
    if digits.startswith("+91"):
        digits = digits[3:]
    elif digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 11:
        digits = digits[1:]
    if not _PHONE_RE.match(digits):
        raise AppError(422, "invalid_phone", "Enter a valid 10-digit Indian mobile number")
    return f"+91{digits}"


def send_otp(db: Session, raw_phone: str) -> str | None:
    """Creates an OTP. Returns the plain code only in development so the UI can show it."""
    s = get_settings()
    phone = normalize_phone(raw_phone)
    since = utcnow() - timedelta(hours=1)
    sent_recently = db.scalar(
        select(func.count()).select_from(OtpCode).where(OtpCode.phone == phone, OtpCode.created_at >= since)
    )
    if s.rate_limits_enabled and sent_recently >= s.otp_send_limit_per_hour:
        raise AppError(429, "otp_rate_limited", "Too many OTP requests. Try again later.")

    code = generate_otp()
    db.add(OtpCode(phone=phone, code_hash=hash_secret(f"{phone}:{code}"), expires_at=utcnow() + timedelta(seconds=s.otp_ttl_seconds)))
    db.commit()
    get_sms_provider().send_otp(phone, code)
    return code if s.is_dev else None


def verify_otp(db: Session, raw_phone: str, code: str) -> tuple[User, bool]:
    """Returns (user, is_new_user)."""
    s = get_settings()
    phone = normalize_phone(raw_phone)
    otp = db.scalar(
        select(OtpCode)
        .where(OtpCode.phone == phone, OtpCode.consumed_at.is_(None))
        .order_by(OtpCode.created_at.desc())
        .limit(1)
        .with_for_update()
    )
    if otp is None or otp.expires_at < utcnow():
        raise AppError(400, "otp_expired", "OTP expired. Request a new one.")
    if otp.attempts >= s.otp_max_attempts:
        raise AppError(429, "otp_locked", "Too many wrong attempts. Request a new OTP.")
    otp.attempts += 1
    if otp.code_hash != hash_secret(f"{phone}:{code.strip()}"):
        db.commit()
        raise AppError(400, "otp_invalid", "Incorrect OTP")
    otp.consumed_at = utcnow()

    user = db.scalar(select(User).where(User.phone == phone))
    is_new = user is None
    if is_new:
        user = _create_user(db, phone=phone)
    elif user.status == "blocked":
        db.commit()
        raise AppError(403, "account_blocked", "This account is blocked")
    db.commit()
    return user, is_new


def google_sign_in(db: Session, id_token_str: str) -> tuple[User, bool]:
    s = get_settings()
    if not s.google_client_ids:
        raise AppError(503, "google_not_configured", "Google sign-in is not configured")
    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token

    # Web, Android and iOS each have their own OAuth client ID; accept a token issued for any of them.
    try:
        info = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), audience=None)
    except ValueError:
        raise AppError(401, "invalid_google_token", "Google sign-in failed")
    if info.get("aud") not in s.google_client_ids:
        raise AppError(401, "invalid_google_token", "Google sign-in failed")
    sub, email = info["sub"], info.get("email") if info.get("email_verified") else None

    user = db.scalar(select(User).where(User.google_sub == sub))
    if user is None and email:
        user = db.scalar(select(User).where(User.email == email))
        if user is not None:
            user.google_sub = sub
    is_new = user is None
    if is_new:
        user = _create_user(db, google_sub=sub, email=email, name=info.get("name"))
    elif user.status == "blocked":
        raise AppError(403, "account_blocked", "This account is blocked")
    db.commit()
    return user, is_new


def decode_firebase_token(token: str) -> dict:
    """Verifies a Firebase ID token (signature, expiry, audience = project). Raises AppError(401) when invalid."""
    s = get_settings()
    if not s.firebase_project_id:
        raise AppError(503, "firebase_not_configured", "Firebase sign-in is not configured")
    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token

    try:
        claims = id_token.verify_firebase_token(token, google_requests.Request(), audience=s.firebase_project_id)
    except ValueError:
        raise AppError(401, "invalid_token", "Invalid or expired Firebase token")
    if not claims or claims.get("iss") != f"https://securetoken.google.com/{s.firebase_project_id}":
        raise AppError(401, "invalid_token", "Invalid or expired Firebase token")
    return claims


def firebase_session(db: Session, token: str) -> tuple[User, bool]:
    """Finds or creates the user behind a Firebase ID token (phone OTP or Google). Returns (user, is_new)."""
    claims = decode_firebase_token(token)
    uid = claims.get("user_id") or claims["sub"]
    phone = normalize_phone(claims["phone_number"]) if claims.get("phone_number") else None
    email = claims.get("email") if claims.get("email_verified") else None
    user = db.scalar(select(User).where(User.firebase_uid == uid))
    if user is None and phone:
        user = db.scalar(select(User).where(User.phone == phone))
    if user is None and email:
        user = db.scalar(select(User).where(User.email == email))
    is_new = user is None
    if is_new:
        user = _create_user(db, firebase_uid=uid, phone=phone, email=email, name=claims.get("name"))
    else:
        if user.status == "blocked":
            raise AppError(403, "account_blocked", "This account is blocked")
        if user.status == "deleted":
            raise AppError(401, "invalid_token", "Account not found")
        user.firebase_uid = user.firebase_uid or uid
    db.commit()
    return user, is_new


def _create_user(db: Session, **fields) -> User:
    user = User(**fields)
    user.profile = UserProfile()
    db.add(user)
    db.flush()
    boot = get_settings().bootstrap_admin_phone
    if boot and fields.get("phone") and fields["phone"] == normalize_phone(boot):
        db.add(AdminUser(user_id=user.id, role="founder", permissions=[]))
        db.flush()
        db.refresh(user)
    db.add(AnalyticsEvent(user_id=user.id, name="signup", props={"method": "firebase" if fields.get("firebase_uid")
                                                                   else "google" if fields.get("google_sub") else "otp"}))
    return user


def issue_tokens(db: Session, user: User) -> dict:
    s = get_settings()
    refresh = new_refresh_token()
    db.add(RefreshToken(user_id=user.id, token_hash=hash_secret(refresh), expires_at=utcnow() + timedelta(days=s.refresh_token_days)))
    db.commit()
    return {
        "access_token": create_access_token(user.id, is_admin=user.admin is not None),
        "refresh_token": refresh,
        "token_type": "bearer",
        "expires_in": s.access_token_minutes * 60,
    }


def rotate_refresh(db: Session, refresh: str) -> dict:
    row = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_secret(refresh)).with_for_update())
    if row is None or row.expires_at < utcnow():
        raise AppError(401, "invalid_refresh", "Session expired. Please log in again.")
    if row.revoked_at is not None:
        # Reuse of a rotated token suggests theft: revoke every session of this user.
        _revoke_all(db, row.user_id)
        db.commit()
        raise AppError(401, "invalid_refresh", "Session expired. Please log in again.")
    user = db.get(User, row.user_id)
    if user is None or user.status != "active":
        raise AppError(401, "invalid_refresh", "Session expired. Please log in again.")
    row.revoked_at = utcnow()
    return issue_tokens(db, user)


def logout(db: Session, refresh: str) -> None:
    row = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_secret(refresh)))
    if row is not None and row.revoked_at is None:
        row.revoked_at = utcnow()
        db.commit()


def _revoke_all(db: Session, user_id) -> None:
    for t in db.scalars(select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))):
        t.revoked_at = utcnow()
