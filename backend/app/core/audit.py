"""Audit log (every admin write) and product analytics events (PDF section 13)."""

from sqlalchemy.orm import Session

from app.models import AnalyticsEvent, AuditLog, User

ANALYTICS_EVENTS = {
    "signup", "purchase", "attempt_start", "submit", "report_viewed", "report_rating", "interview_completed",
    "interview_start", "app_open", "catalog_view", "exam_view", "paywall_view",
}
# Events a client may send itself through POST /v1/events (the rest are recorded server-side only).
CLIENT_EVENTS = {"report_viewed", "app_open", "catalog_view", "exam_view", "paywall_view"}


def audit(db: Session, actor: User | None, action: str, target_type: str, target_id=None, **details) -> None:
    db.add(AuditLog(
        actor_user_id=actor.id if actor else None, action=action, target_type=target_type,
        target_id=str(target_id) if target_id is not None else None,
        details={k: (str(v) if not isinstance(v, (int, float, bool, str, list, dict, type(None))) else v)
                 for k, v in details.items()},
    ))


def track(db: Session, user_id, name: str, **props) -> None:
    db.add(AnalyticsEvent(user_id=user_id, name=name, props=props))
