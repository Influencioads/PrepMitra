"""The student's local date and time. The countdown and the daily plan follow the student's day, not UTC."""

from datetime import date, datetime, timedelta, timezone

from app.db import utcnow

IST = timezone(timedelta(hours=5, minutes=30), "IST")
DEFAULT_TZ = "Asia/Kolkata"


def tz(name: str | None):
    try:
        from zoneinfo import ZoneInfo

        return ZoneInfo(name or DEFAULT_TZ)
    except Exception:  # no tz database on this machine: India has no DST, so a fixed offset is exact for IST
        return IST


def now_local(tz_name: str | None = None) -> datetime:
    return utcnow().astimezone(tz(tz_name))


def today(tz_name: str | None = None) -> date:
    return now_local(tz_name).date()


def user_tz(db, user_id) -> str:
    from app.models import NotificationPreference

    p = db.get(NotificationPreference, user_id)
    return p.timezone if p and p.timezone else DEFAULT_TZ
