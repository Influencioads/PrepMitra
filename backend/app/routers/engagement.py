from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.audit import CLIENT_EVENTS, track
from app.core.deps import get_current_user
from app.core.errors import AppError, not_found
from app.db import get_db, utcnow
from app.models import DeviceToken, Notification, User
from app.schemas.common import ClientEventIn, DeviceIn
from app.services import progress

router = APIRouter(tags=["dashboard & notifications"])


@router.get("/me/progress")
def my_progress(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Dashboard: history, score trend, topic heatmap, credits and plan expiry, recommended next tests."""
    return progress.progress(db, user)


@router.get("/me/notifications")
def notifications(unread_only: bool = False, limit: int = Query(default=30, ge=1, le=100),
                  offset: int = Query(default=0, ge=0), user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    stmt = select(Notification).where(Notification.user_id == user.id)
    if unread_only:
        stmt = stmt.where(Notification.read_at.is_(None))
    rows = db.scalars(stmt.order_by(Notification.created_at.desc()).limit(limit).offset(offset)).all()
    unread = db.scalar(select(func.count()).select_from(Notification).where(
        Notification.user_id == user.id, Notification.read_at.is_(None)))
    return {"items": [{"id": n.id, "kind": n.kind, "title": n.title, "body": n.body, "data": n.data,
                       "read_at": n.read_at, "created_at": n.created_at} for n in rows],
            "unread": unread, "limit": limit, "offset": offset}


@router.post("/me/notifications/{notification_id}/read", status_code=204)
def mark_read(notification_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    n = db.get(Notification, notification_id)
    if n is None or n.user_id != user.id:
        raise not_found("Notification")
    n.read_at = n.read_at or utcnow()
    db.commit()


@router.post("/me/notifications/read-all", status_code=204)
def mark_all_read(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for n in db.scalars(select(Notification).where(Notification.user_id == user.id, Notification.read_at.is_(None))):
        n.read_at = utcnow()
    db.commit()


@router.post("/me/devices", status_code=201)
def register_device(body: DeviceIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Registers an FCM/APNs push token. Re-registering the same token moves it to the current user."""
    d = db.scalar(select(DeviceToken).where(DeviceToken.token == body.token))
    if d is None:
        d = DeviceToken(token=body.token, user_id=user.id, platform=body.platform)
        db.add(d)
    d.user_id, d.platform, d.app_version, d.locale = user.id, body.platform, body.app_version, body.locale
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "device_conflict", "Could not register device")
    return {"id": d.id, "platform": d.platform}


@router.delete("/me/devices/{token}", status_code=204)
def remove_device(token: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    d = db.scalar(select(DeviceToken).where(DeviceToken.token == token, DeviceToken.user_id == user.id))
    if d is not None:
        db.delete(d)
        db.commit()


@router.post("/events", status_code=204)
def client_event(body: ClientEventIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Product analytics events sent by clients (e.g. report_viewed, app_open)."""
    if body.name not in CLIENT_EVENTS:
        raise AppError(422, "invalid_event", f"Allowed events: {sorted(CLIENT_EVENTS)}")
    track(db, user.id, body.name, **{k: v for k, v in list(body.props.items())[:20]})
    db.commit()
