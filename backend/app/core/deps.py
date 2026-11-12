import uuid
from collections.abc import Callable

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import decode_access_token
from app.db import get_db, utcnow
from app.models import User

# Declared as an OpenAPI security scheme so Swagger UI shows an "Authorize" button.
bearer = HTTPBearer(auto_error=False, description="Access token from /v1/auth/otp/verify (or /google, /refresh)")


def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if creds is None or creds.scheme.lower() != "bearer":
        raise AppError(401, "unauthenticated", "Missing bearer token")
    try:
        payload = decode_access_token(creds.credentials)
        user = db.get(User, uuid.UUID(payload["sub"]))
    except jwt.PyJWTError:
        user = _firebase_user(db, creds.credentials)
    if user is None or user.status == "deleted":
        raise AppError(401, "invalid_token", "Account not found")
    if user.status == "blocked":
        raise AppError(403, "account_blocked", "This account is blocked")
    user.last_active_at = utcnow()
    db.commit()
    return user


def _firebase_user(db: Session, token: str) -> User:
    """Clients using Firebase Authentication send the Firebase ID token on every request (API Plan sheet)."""
    from app.config import get_settings
    from app.services.auth import firebase_session

    if not get_settings().firebase_project_id:
        raise AppError(401, "invalid_token", "Invalid or expired token")
    return firebase_session(db, token)[0]


def require_admin(*roles: str) -> Callable[..., User]:
    """Role-based admin guard. 'founder' passes every check."""

    def _guard(user: User = Depends(get_current_user)) -> User:
        if user.admin is None:
            raise AppError(403, "forbidden", "Admin access required")
        if roles and user.admin.role != "founder" and user.admin.role not in roles:
            raise AppError(403, "forbidden", "Your admin role cannot perform this action")
        return user

    return _guard
