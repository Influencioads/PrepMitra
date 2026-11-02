from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.deps import bearer
from app.core.errors import AppError
from app.core.ratelimit import limit
from app.db import get_db
from app.routers.me import _me_out
from app.schemas.me import MeOut
from app.schemas.me import GoogleIn, OtpSendIn, OtpSendOut, OtpVerifyIn, RefreshIn, TokenOut
from app.services import auth

router = APIRouter(prefix="/auth", tags=["auth"])


class SessionIn(BaseModel):
    id_token: str | None = None


class SessionOut(BaseModel):
    is_new_user: bool
    user: MeOut
    # Optional backend session tokens. Firebase clients can ignore them and keep sending the Firebase ID token.
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


@router.post("/session", response_model=SessionOut, dependencies=[Depends(limit("session", 60))])
def session(body: SessionIn | None = None, creds: HTTPAuthorizationCredentials | None = Depends(bearer),
            db: Session = Depends(get_db)):
    """Firebase login (phone OTP or Google on the client): send the Firebase ID token in the Authorization header
    (or as `id_token`). Creates the user on first login and returns the profile."""
    token = (body.id_token if body and body.id_token else None) or (creds.credentials if creds else None)
    if not token:
        raise AppError(401, "unauthenticated", "Send the Firebase ID token as a bearer token")
    user, is_new = auth.firebase_session(db, token)
    return SessionOut(is_new_user=is_new, user=_me_out(db, user), **auth.issue_tokens(db, user))


@router.post("/otp/send", response_model=OtpSendOut, dependencies=[Depends(limit("otp_send", 20))])
def otp_send(body: OtpSendIn, db: Session = Depends(get_db)):
    dev_code = auth.send_otp(db, body.phone)
    return OtpSendOut(expires_in=get_settings().otp_ttl_seconds, dev_otp=dev_code)


@router.post("/otp/verify", response_model=TokenOut, dependencies=[Depends(limit("otp_verify", 30))])
def otp_verify(body: OtpVerifyIn, db: Session = Depends(get_db)):
    user, is_new = auth.verify_otp(db, body.phone, body.code)
    return TokenOut(**auth.issue_tokens(db, user), is_new_user=is_new)


@router.post("/google", response_model=TokenOut, dependencies=[Depends(limit("google", 30))])
def google(body: GoogleIn, db: Session = Depends(get_db)):
    user, is_new = auth.google_sign_in(db, body.id_token)
    return TokenOut(**auth.issue_tokens(db, user), is_new_user=is_new)


@router.post("/refresh", response_model=TokenOut)
def refresh(body: RefreshIn, db: Session = Depends(get_db)):
    return TokenOut(**auth.rotate_refresh(db, body.refresh_token))


@router.post("/logout", status_code=204)
def logout(body: RefreshIn, db: Session = Depends(get_db)):
    auth.logout(db, body.refresh_token)
