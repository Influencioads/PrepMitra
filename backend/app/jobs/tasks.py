"""Job and periodic-task registry. Each task opens its own DB session and is safe to run more than once."""

import logging
import uuid

from app.config import get_settings
from app.db import SessionLocal
from app.jobs.queue import task

log = logging.getLogger(__name__)


@task("generate_exam_report")
def generate_exam_report(report_id: str) -> None:
    from app.services.reports import generate_exam_report as run

    run(uuid.UUID(str(report_id)))


@task("evaluate_interview")
def evaluate_interview(report_id: str) -> None:
    from app.services.interviews import evaluate

    evaluate(uuid.UUID(str(report_id)))


@task("send_notification")
def send_notification(notification_id: int) -> None:
    from app.services.notifications import send

    send(notification_id)


@task("mentor_replan")
def mentor_replan(user_id: str, exam_id: str | None = None) -> None:
    """A scored mock changed the student's topic evidence: re-plan their active exam goals from today."""
    from app.services.mentor.planner import replan_user

    with SessionLocal() as db:
        replan_user(db, uuid.UUID(str(user_id)), exam_id)


@task("build_bank")
def build_bank(exam_id: str, per_topic: int) -> None:
    from app.models import Exam
    from app.services.bank import build_bank as run

    with SessionLocal() as db:
        exam = db.get(Exam, uuid.UUID(str(exam_id)))
        if exam is not None:
            run(db, exam, int(per_topic))


@task("pregenerate_papers")
def pregenerate_papers() -> None:
    from app.services.papers import pregenerate

    with SessionLocal() as db:
        pregenerate(db, get_settings().papers_pool_size)


def _with_db(fn):
    def run():
        with SessionLocal() as db:
            return fn(db)

    run.__name__ = fn.__name__
    return run


def periodic() -> list[tuple[int, object]]:
    """(interval_seconds, callable) pairs run by the scheduler."""
    from app.services import attempts, credits, interviews, notifications, payments, reports
    from app.services.mentor import reminders

    return [
        (15, _with_db(attempts.auto_submit_expired)),  # server-side auto-submit when time ends
        (60, _with_db(reports.sweep_timeouts)),  # report not ready in 10 min -> credit restored
        (60, _with_db(interviews.sweep_stale)),  # interview disconnected > 10 min -> evaluated as-is
        (600, pregenerate_papers),  # keep pre-generated papers ready
        (3600, _with_db(credits.expire_credits)),
        (3600, _with_db(payments.expire_subscriptions)),
        (6 * 3600, _with_db(notifications.notify_expiring_credits)),
        (6 * 3600, _with_db(notifications.notify_inactive_users)),
        (get_settings().mentor_reminder_interval_seconds, _with_db(reminders.sweep)),  # mentor nudges, deduplicated
    ]
