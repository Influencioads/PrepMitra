"""Mentor reminders (module 9): morning focus, afternoon nudge, evening summary, exam countdown, missed days.

Runs every few minutes from the scheduler. Each kind goes out at most once per student per local day, inside a
three-hour window after the student's chosen time, never more than `max_per_day` mentor notifications a day, and
only for the nearest upcoming exam (one student, one set of reminders, however many exams they track).
Countdown milestones replace the morning message on that day instead of adding another one.
"""

import logging
from datetime import datetime, time, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import utcnow
from app.models import Exam, ExamGoal, Notification, NotificationPreference, StudyTask, Topic, User, UserTopicMastery
from app.services.mentor import clock
from app.services.mentor import config as cfg
from app.services.notifications import dispatch_after_commit, notify

log = logging.getLogger(__name__)

COUNTDOWN_DAYS = {60, 30, 20, 15, 10, 7, 5, 3, 2, 1}
WINDOW = timedelta(hours=3)
MISSED_DAYS = 3
KINDS = ("mentor_morning", "mentor_countdown", "mentor_afternoon", "mentor_evening", "mentor_missed")

PREF_FIELDS = ("push_enabled", "email_enabled", "morning_enabled", "morning_time", "afternoon_enabled",
               "afternoon_time", "evening_enabled", "evening_time", "countdown_enabled", "mock_reminders_enabled",
               "max_per_day", "timezone")


def preferences(db: Session, user_id) -> NotificationPreference:
    p = db.get(NotificationPreference, user_id)
    if p is None:
        p = NotificationPreference(user_id=user_id, push_enabled=True, email_enabled=True, morning_enabled=True,
                                   morning_time="07:30", afternoon_enabled=True, afternoon_time="16:00",
                                   evening_enabled=True, evening_time="20:30", countdown_enabled=True,
                                   mock_reminders_enabled=True, max_per_day=3, timezone=clock.DEFAULT_TZ)
    return p


def pref_out(p: NotificationPreference) -> dict:
    return {f: getattr(p, f) for f in PREF_FIELDS}


def save_preferences(db: Session, user: User, changes: dict) -> dict:
    p = preferences(db, user.id)
    if p not in db:
        db.add(p)
    for k, v in changes.items():
        if k in PREF_FIELDS and v is not None:
            setattr(p, k, v)
    db.commit()
    return pref_out(p)


def _at(local_day, hhmm: str, tz) -> datetime:
    h, m = (int(x) for x in hhmm.split(":"))
    return datetime.combine(local_day, time(h, m), tz)


def _sent_today(db: Session, user_id, local_date: str) -> dict[str, int]:
    rows = db.scalars(select(Notification).where(
        Notification.user_id == user_id, Notification.kind.in_(KINDS),
        Notification.created_at >= utcnow() - timedelta(hours=36))).all()
    out: dict[str, int] = {}
    for n in rows:
        if (n.data or {}).get("local_date") == local_date:
            out[n.kind] = out.get(n.kind, 0) + 1
    return out


def _channels(p: NotificationPreference) -> list[str]:
    return ["in_app"] + (["push"] if p.push_enabled else []) + (["email"] if p.email_enabled else [])


def _subject_name(section_key: str | None) -> str:
    return cfg.SUBJECT_NAMES.get(cfg.subject_of(section_key), "practice")


def _missed_streak(db: Session, goal: ExamGoal, today) -> int:
    """Consecutive days before today that had planned work and none of it done."""
    streak = 0
    for back in range(1, 8):
        day = today - timedelta(days=back)
        tasks = db.scalars(select(StudyTask).where(StudyTask.goal_id == goal.id, StudyTask.task_date == day,
                                                   StudyTask.kind != "rest",
                                                   StudyTask.status.in_(("pending", "done", "skipped")))).all()
        if not tasks:
            break
        if any(t.status == "done" for t in tasks):
            break
        streak += 1
    return streak


def _improvement_today(db: Session, user_id, topic_ids: list[int], since: datetime) -> tuple[str, float, float] | None:
    best = None
    for m, t in db.execute(select(UserTopicMastery, Topic).join(Topic, Topic.id == UserTopicMastery.topic_id).where(
            UserTopicMastery.user_id == user_id, UserTopicMastery.topic_id.in_(topic_ids or [-1]),
            UserTopicMastery.last_seen_at >= since)).all():
        if m.previous_recent_accuracy is not None and m.recent_accuracy is not None \
                and m.recent_accuracy - m.previous_recent_accuracy >= 0.05:
            gain = m.recent_accuracy - m.previous_recent_accuracy
            if best is None or gain > best[2] - best[1]:
                best = (t.name, m.previous_recent_accuracy, m.recent_accuracy)
    return best


def _send(db: Session, user_id, kind: str, p: NotificationPreference, local_date: str, data: dict, sent: list,
          **params) -> None:
    n = notify(db, user_id, kind, {**data, "local_date": local_date, "screen": data.get("screen", "mentor")},
               channels=_channels(p), **params)
    sent.append(n.id)


def remind_user(db: Session, user: User, now: datetime | None = None) -> list[int]:
    """Decides and creates this user's due reminders. Returns notification ids (caller commits and dispatches)."""
    p = preferences(db, user.id)
    tz = clock.tz(p.timezone)
    now_l = (now or utcnow()).astimezone(tz)
    today = now_l.date()
    goals = db.scalars(select(ExamGoal).where(ExamGoal.user_id == user.id, ExamGoal.status == "active",
                                              ExamGoal.exam_date >= today).order_by(ExamGoal.exam_date)).all()
    if not goals:
        return []
    goal = goals[0]
    exam = db.get(Exam, goal.exam_id)
    days = (goal.exam_date - today).days
    local_date = today.isoformat()
    already = _sent_today(db, user.id, local_date)
    budget = max(0, p.max_per_day - sum(already.values()))
    tasks = db.scalars(select(StudyTask).where(StudyTask.goal_id == goal.id, StudyTask.task_date == today,
                                               StudyTask.status.in_(("pending", "done", "skipped")),
                                               StudyTask.kind != "rest").order_by(StudyTask.seq)).all()
    pending = [t for t in tasks if t.status == "pending"]
    done = [t for t in tasks if t.status == "done"]
    sent: list[int] = []
    data = {"goal_id": goal.id, "exam_id": str(exam.id)}

    def due(enabled: bool, at: str) -> bool:
        start = _at(today, at, tz)
        return enabled and start <= now_l < start + WINDOW

    if budget and due(p.morning_enabled, p.morning_time) and not (
            already.get("mentor_morning") or already.get("mentor_countdown") or already.get("mentor_missed")):
        missed = _missed_streak(db, goal, today)
        focus = ", ".join(dict.fromkeys(t.title.split(":")[0] for t in pending if t.kind in (
            "learn", "practice", "revision", "sectional_test", "mock_test")))[:160] or "revision"
        recently_nudged = db.scalar(select(Notification.id).where(
            Notification.user_id == user.id, Notification.kind == "mentor_missed",
            Notification.created_at >= utcnow() - timedelta(days=MISSED_DAYS)).limit(1)) is not None
        if missed >= MISSED_DAYS and not recently_nudged:
            from app.services.mentor import planner

            planner.generate(db, goal, with_note=False)  # reflow the plan around the missed days
            _send(db, user.id, "mentor_missed", p, local_date, {**data, "screen": "mentor_plan"}, sent,
                  days=missed, exam=exam.name, exam_days=days)
        elif p.countdown_enabled and days in COUNTDOWN_DAYS:
            _send(db, user.id, "mentor_countdown", p, local_date, data, sent, exam=exam.name, days=days, focus=focus,
                  advice=("Focus on revision, sectional tests and full-length mock practice" if days <= 7 else
                          "Keep following the daily plan"))
        elif pending:
            mock = p.mock_reminders_enabled and any(t.kind == "mock_test" for t in pending)
            _send(db, user.id, "mentor_morning", p, local_date, data, sent, exam=exam.name, days=days,
                  focus=("a full-length mock test" if mock else focus))
        budget -= len(sent)

    if budget and due(p.afternoon_enabled, p.afternoon_time) and not already.get("mentor_afternoon") \
            and pending and not done:
        first = next((t for t in pending if t.kind in ("practice", "learn", "sectional_test", "mock_test")), pending[0])
        _send(db, user.id, "mentor_afternoon", p, local_date, data, sent,
              subject=_subject_name(first.section_key), task=first.title)
        budget -= 1

    if budget and due(p.evening_enabled, p.evening_time) and not already.get("mentor_evening") and done:
        start_of_day = _at(today, "00:00", tz)
        imp = _improvement_today(db, user.id, [t.topic_id for t in done if t.topic_id], start_of_day)
        extra = (f" You improved your accuracy in {imp[0]} from {round(imp[1] * 100)}% to {round(imp[2] * 100)}%."
                 if imp else "")
        if pending:
            _send(db, user.id, "mentor_evening", p, local_date, data, sent, done=len(done), total=len(tasks),
                  status=f"You completed {len(done)} of {len(tasks)} tasks today.", extra=extra)
        else:
            _send(db, user.id, "mentor_evening", p, local_date, data, sent, done=len(done), total=len(tasks),
                  status="Today's preparation is completed.", extra=extra)
    return sent


def sweep(db: Session, now: datetime | None = None) -> int:
    user_ids = list(db.scalars(select(ExamGoal.user_id).where(ExamGoal.status == "active").distinct()))
    total = 0
    for uid in user_ids:
        user = db.get(User, uid)
        if user is None or user.status != "active":
            continue
        try:
            ids = remind_user(db, user, now)
            db.commit()
        except Exception:
            db.rollback()
            log.exception("mentor reminders failed for a user")
            continue
        for nid in ids:
            dispatch_after_commit(nid)
        total += len(ids)
    return total
