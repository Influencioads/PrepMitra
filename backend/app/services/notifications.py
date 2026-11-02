"""Notifications (PDF 5.8): in-app inbox + push (FCM for Android, iOS via APNs-through-FCM, web) + email.

Dev adapters log instead of sending. Production adapters: FCM HTTP v1 (service-account JSON) and SMTP
(Amazon SES exposes SMTP). WhatsApp is Phase 2.
"""

import json
import logging
import smtplib
from datetime import timedelta
from email.message import EmailMessage

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.i18n import message
from app.db import SessionLocal, utcnow
from app.jobs.queue import enqueue
from app.models import CreditLedger, DeviceToken, Notification, User

log = logging.getLogger(__name__)


def notify(db: Session, user_id, kind: str, data: dict | None = None, **params) -> Notification:
    """Creates the in-app notification; push/email are sent by a job after the caller commits."""
    user = db.get(User, user_id)
    lang = (user.preferred_language if user else "en") or "en"
    title, body = message(kind, lang, **params)
    channels = ["in_app", "push"] + (["email"] if user is not None and user.email else [])
    n = Notification(user_id=user_id, kind=kind, title=title, body=body, channels=channels, data=data or {})
    db.add(n)
    db.flush()
    return n


def dispatch_after_commit(notification_id: int) -> None:
    enqueue("send_notification", notification_id=notification_id)


def send(notification_id: int) -> None:
    with SessionLocal() as db:
        n = db.get(Notification, int(notification_id))
        if n is None:
            return
        user = db.get(User, n.user_id)
        if user is None or user.status != "active":
            return
        if "push" in n.channels:
            for d in db.scalars(select(DeviceToken).where(DeviceToken.user_id == user.id)):
                try:
                    get_push().send(d.token, n.title, n.body, {**n.data, "kind": n.kind, "notification_id": str(n.id)})
                except Exception:
                    log.warning("push to device %s failed", d.id)
        if "email" in n.channels and user.email:
            try:
                get_email().send(user.email, n.title, n.body)
            except Exception:
                log.warning("email for notification %s failed", n.id)


class ConsolePush:
    def send(self, token: str, title: str, body: str, data: dict) -> None:
        log.info("push (dev) to ...%s: %s", token[-6:], title)


class FcmPush:
    """FCM HTTP v1. Needs FCM_CREDENTIALS_FILE (service account JSON) - not exercised without real credentials."""

    def __init__(self):
        import os

        from google.oauth2 import service_account

        path = os.environ.get("FCM_CREDENTIALS_FILE", "")
        self.creds = service_account.Credentials.from_service_account_file(
            path, scopes=["https://www.googleapis.com/auth/firebase.messaging"])
        self.project = json.load(open(path))["project_id"]

    def send(self, token: str, title: str, body: str, data: dict) -> None:
        import httpx
        from google.auth.transport.requests import Request

        if not self.creds.valid:
            self.creds.refresh(Request())
        httpx.post(
            f"https://fcm.googleapis.com/v1/projects/{self.project}/messages:send",
            headers={"Authorization": f"Bearer {self.creds.token}"},
            json={"message": {"token": token, "notification": {"title": title, "body": body},
                              "data": {k: str(v) for k, v in data.items()}}},
            timeout=10,
        ).raise_for_status()


class ConsoleEmail:
    def send(self, to: str, subject: str, body: str) -> None:
        log.info("email (dev) to %s: %s", to.split("@")[-1], subject)


class SmtpEmail:
    def send(self, to: str, subject: str, body: str) -> None:
        s = get_settings()
        msg = EmailMessage()
        msg["From"], msg["To"], msg["Subject"] = s.email_from, to, subject
        msg.set_content(body)
        with smtplib.SMTP(s.smtp_host, s.smtp_port, timeout=15) as server:
            server.starttls()
            if s.smtp_user:
                server.login(s.smtp_user, s.smtp_password)
            server.send_message(msg)


class ResendEmail:
    """Resend (https://resend.com) HTTP API. Needs RESEND_API_KEY and a verified sender domain in EMAIL_FROM."""

    def send(self, to: str, subject: str, body: str) -> None:
        import httpx

        s = get_settings()
        httpx.post("https://api.resend.com/emails", headers={"Authorization": f"Bearer {s.resend_api_key}"},
                   json={"from": s.email_from, "to": [to], "subject": subject, "text": body}, timeout=15).raise_for_status()


def get_push():
    return FcmPush() if get_settings().push_provider == "fcm" else ConsolePush()


def get_email():
    provider = get_settings().email_provider
    return {"smtp": SmtpEmail, "resend": ResendEmail}.get(provider, ConsoleEmail)()


def _recently_sent(db: Session, user_id, kind: str, days: int) -> bool:
    return db.scalar(select(func.count()).select_from(Notification).where(
        Notification.user_id == user_id, Notification.kind == kind,
        Notification.created_at > utcnow() - timedelta(days=days))) > 0


def notify_expiring_credits(db: Session) -> int:
    """Daily: users whose credits expire within 3 days (PDF 5.8 "plan expiring in 3 days")."""
    from app.services.credits import balance

    now = utcnow()
    user_ids = set(db.scalars(select(CreditLedger.user_id).where(
        CreditLedger.delta > 0, CreditLedger.grant_id.is_(None),
        CreditLedger.expires_at > now, CreditLedger.expires_at <= now + timedelta(days=3))))
    sent = []
    for uid in user_ids:
        user = db.get(User, uid)
        if user is None or user.status != "active" or _recently_sent(db, uid, "plan_expiring", 3):
            continue
        b = balance(db, uid)
        expiring = sum(g["remaining"] for g in b["grants"] if g["expires_at"] and g["expires_at"] <= now + timedelta(days=3))
        if expiring <= 0:
            continue
        n = notify(db, uid, "plan_expiring", {"screen": "credits"}, credits=expiring,
                   expires=b["next_expiry"].strftime("%d %b %Y"))
        sent.append(n.id)
    db.commit()
    for nid in sent:
        dispatch_after_commit(nid)
    return len(sent)


def notify_inactive_users(db: Session) -> int:
    """Daily: practice reminder for users inactive for 7 days (at most once a week)."""
    cutoff = utcnow() - timedelta(days=7)
    users = db.scalars(select(User).where(User.status == "active", User.last_active_at.is_not(None),
                                          User.last_active_at < cutoff).limit(5000)).all()
    sent = []
    for u in users:
        if _recently_sent(db, u.id, "practice_reminder", 7):
            continue
        sent.append(notify(db, u.id, "practice_reminder", {"screen": "catalog"}).id)
    db.commit()
    for nid in sent:
        dispatch_after_commit(nid)
    return len(sent)
