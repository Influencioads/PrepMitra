"""Exam goals, countdown, preparation dashboard and recommendations (mentor modules 5, 7 and 10).

Definitions shown to students (and used by the chatbot), all computed from stored data:
  * syllabus completion = share of the exam's topics (by weightage) that are covered: classified with enough evidence
    and at least "needs improvement", or completed (mastered)
  * preparation % = weightage-weighted average of min(1, effective accuracy / 85%) over all topics (0 until a topic
    has enough evidence to be classified)
  * topics completed = mastered; pending = not started or not enough evidence; weak = weak or very weak
"""

import uuid
from datetime import date, datetime, time, timedelta
from statistics import mean

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import AppError, not_found
from app.db import utcnow
from app.models import Attempt, AttemptAnswer, Exam, ExamGoal, PracticeSession, StudyTask, User
from app.services.mentor import analysis, clock, mastery, notebook, planner
from app.services.mentor import config as cfg

COVERED = {"needs_improvement", "good", "strong"}


# ---- goals ------------------------------------------------------------------------------------------------------
def _exam(db: Session, ref) -> Exam:
    try:
        e = db.get(Exam, uuid.UUID(str(ref)))
    except ValueError:
        e = db.scalar(select(Exam).where(Exam.slug == str(ref)))
    if e is None or e.status != "published":
        raise not_found("Exam")
    return e


def own_goal(db: Session, user: User, goal_id: int) -> ExamGoal:
    g = db.get(ExamGoal, goal_id)
    if g is None or g.user_id != user.id or g.status != "active":
        raise not_found("Exam goal")
    return g


def _validate(db: Session, user: User, exam_date: date | None, daily_minutes: int | None, rest_weekday: int | None):
    today = clock.today(clock.user_tz(db, user.id))
    if exam_date is not None and not (today <= exam_date <= today + timedelta(days=730)):
        raise AppError(422, "invalid_exam_date", "The exam date must be between today and two years from now")
    if daily_minutes is not None and not (15 <= daily_minutes <= 720):
        raise AppError(422, "invalid_daily_minutes", "Daily study time must be between 15 and 720 minutes")
    if rest_weekday is not None and not (0 <= rest_weekday <= 6):
        raise AppError(422, "invalid_rest_weekday", "rest_weekday is 0 (Monday) to 6 (Sunday)")


def create_goal(db: Session, user: User, exam_ref, exam_date: date, daily_minutes: int,
                rest_weekday: int | None) -> ExamGoal:
    exam = _exam(db, exam_ref)
    _validate(db, user, exam_date, daily_minutes, rest_weekday)
    g = db.scalar(select(ExamGoal).where(ExamGoal.user_id == user.id, ExamGoal.exam_id == exam.id))
    if g is not None and g.status == "active":
        raise AppError(409, "goal_exists", "You already have a plan for this exam; change its date instead")
    if g is None:
        g = ExamGoal(user_id=user.id, exam_id=exam.id, plan_version=0, plan_meta={})
        db.add(g)
    g.exam_date, g.daily_minutes, g.rest_weekday, g.status = exam_date, daily_minutes, rest_weekday, "active"
    db.flush()
    planner.generate(db, g)
    return g


def update_goal(db: Session, user: User, goal_id: int, changes: dict) -> ExamGoal:
    g = own_goal(db, user, goal_id)
    _validate(db, user, changes.get("exam_date"), changes.get("daily_minutes"), changes.get("rest_weekday"))
    replan = False
    for k in ("exam_date", "daily_minutes", "rest_weekday"):
        if k in changes and getattr(g, k) != changes[k]:
            setattr(g, k, changes[k])
            replan = True
    db.flush()
    if replan:  # a new date or budget means a new plan
        planner.generate(db, g)
    else:
        db.commit()
    return g


def archive_goal(db: Session, user: User, goal_id: int) -> None:
    g = own_goal(db, user, goal_id)
    g.status = "archived"
    for t in db.scalars(select(StudyTask).where(StudyTask.goal_id == g.id, StudyTask.status == "pending")):
        t.status = "superseded"
    db.commit()


def countdown(db: Session, g: ExamGoal, exam: Exam | None = None) -> dict:
    today = clock.today(clock.user_tz(db, g.user_id))
    exam = exam or db.get(Exam, g.exam_id)
    d = (g.exam_date - today).days
    return {"goal_id": g.id, "exam_id": str(exam.id), "exam_slug": exam.slug, "exam_name": exam.name,
            "exam_date": g.exam_date, "today": today, "days_remaining": d, "weeks_remaining": max(d, 0) // 7,
            "extra_days": max(d, 0) % 7, "phase": "exam_day" if d == 0 else "passed" if d < 0 else
            "final_revision" if d <= cfg.FINAL_PHASE_DAYS else "preparation",
            "daily_minutes": g.daily_minutes, "rest_weekday": g.rest_weekday}


def goals(db: Session, user: User) -> list[dict]:
    rows = db.scalars(select(ExamGoal).where(ExamGoal.user_id == user.id, ExamGoal.status == "active")
                      .order_by(ExamGoal.exam_date)).all()
    return [countdown(db, g) for g in rows]


# ---- performance -------------------------------------------------------------------------------------------------
def mock_stats(db: Session, user: User, exam_id) -> dict:
    atts = db.scalars(select(Attempt).where(Attempt.user_id == user.id, Attempt.exam_id == exam_id,
                                            Attempt.status == "scored").order_by(Attempt.submitted_at)).all()
    pct = [100 * a.score / a.max_score for a in atts if a.max_score]
    out = {"tests_completed": len(atts),
           "highest_score": max((a.score for a in atts), default=None),
           "average_score": round(mean(a.score for a in atts), 2) if atts else None,
           "recent_score": atts[-1].score if atts else None, "max_score": atts[-1].max_score if atts else None,
           "highest_pct": round(max(pct), 1) if pct else None, "average_pct": round(mean(pct), 1) if pct else None,
           "trend": [{"attempt_id": str(a.id), "at": a.submitted_at, "score": a.score, "max_score": a.max_score}
                     for a in atts[-10:]],
           "last_attempt_id": str(atts[-1].id) if atts else None, "last_at": atts[-1].submitted_at if atts else None,
           "accuracy": None, "time_management": None}
    if atts:
        last = analysis.analyse_attempt(db, atts[-1])
        bands = last["time"]["bands"]
        attempted = last["counts"]["attempted"]
        out["accuracy"] = last["accuracy"]
        out["time_management"] = {
            "efficient_share": round(bands["efficient"] / attempted, 4) if attempted else None,
            "time_sinks": bands["time_sink"], "rushed_wrong": bands["rushed_wrong"], "unseen": bands["unseen"]}
        out["last_marks_lost"] = last["marks_lost"]
        out["last_sections"] = last["sections"]
    return out


def coverage(topics: list[dict]) -> dict:
    total_w = sum(t["weightage"] or 1 for t in topics) or 1
    covered_w = sum((t["weightage"] or 1) for t in topics if t["mastered"] or t["status"] in COVERED)
    # Only topics with enough evidence count; a topic seen once or twice adds nothing yet.
    prep = sum((t["weightage"] or 1) * min(1.0, (t["effective_accuracy"] or 0) / cfg.MASTERY_MIN_ACCURACY)
               for t in topics if t["effective_accuracy"] is not None and t["status"] not in ("not_started",
                                                                                           "insufficient_data"))
    return {
        "syllabus_completion_pct": round(100 * covered_w / total_w, 1),
        "preparation_pct": round(100 * prep / total_w, 1),
        "topics_total": len(topics),
        "topics_completed": sum(1 for t in topics if t["mastered"]),
        "topics_covered": sum(1 for t in topics if t["mastered"] or t["status"] in COVERED),
        "topics_pending": sum(1 for t in topics if t["status"] in ("not_started", "insufficient_data")),
        "topics_weak": sum(1 for t in topics if t["status"] in ("weak", "very_weak")),
        "min_evidence": cfg.min_evidence(),
    }


def _topic_brief(t: dict) -> dict:
    return {k: t.get(k) for k in ("topic_id", "name", "subject", "section_key", "status", "priority", "action",
                                  "effective_accuracy", "accuracy", "attempted", "trend", "mastered", "confidence",
                                  "level", "time_ratio", "tradeoff", "notes", "last_seen_at")}


def recommendations(db: Session, user: User, g: ExamGoal, topics: list[dict], stats: dict,
                    today_tasks: list[dict]) -> dict:
    d = (g.exam_date - clock.today(clock.user_tz(db, user.id))).days
    now = utcnow()
    stale = [t for t in topics if t["mastered"] and t["last_seen_at"] and (now - t["last_seen_at"]).days >= 7]
    due = notebook.due_count(db, user.id)
    every = cfg.mock_every_days(max(d, 0))
    since_mock = (now - stats["last_at"]).days if stats.get("last_at") else None
    if d <= 1:
        mock = {"advice": "no", "reason": "Too close to the exam for a full mock: revise and rest."}
    elif stats["tests_completed"] == 0:
        mock = {"advice": "yes", "reason": "You have not taken a mock for this exam yet; one diagnostic mock "
                "shows where you actually lose marks."}
    elif since_mock is not None and since_mock >= every:
        mock = {"advice": "yes", "reason": f"Your last mock was {since_mock} days ago; at this stage aim for one "
                f"every {every} days."}
    else:
        mock = {"advice": "not_yet", "reason": f"Your last mock was {since_mock} day(s) ago. Work on its weak "
                "topics first, then take the next one."}
    return {
        "study_today": [{"task_id": t["id"], "title": t["title"], "minutes": t["minutes"], "kind": t["kind"]}
                        for t in today_tasks if t["kind"] != "rest"],
        "revise": ([{"title": f"{due} mistake-notebook card(s) are due", "kind": "notebook"}] if due else [])
        + [{"title": f"{t['name']}: revision quiz", "topic_id": t["topic_id"], "kind": "maintenance"} for t in stale[:3]],
        "practise": [_topic_brief(t) for t in topics if t["priority"] == "medium"][:3],
        "more_attention": [_topic_brief(t) for t in topics if t["priority"] == "high"][:4],
        "less_time": [_topic_brief(t) for t in topics if t["priority"] == "low"][:4],
        "mock_test": mock,
    }


def weekly_progress(db: Session, user: User, today: date) -> dict:
    """Accuracy on every answered question (mocks and quizzes) this week vs last week."""
    start = today - timedelta(days=today.weekday())

    tz = clock.tz(clock.user_tz(db, user.id))

    def window(a: date, b: date) -> dict:
        t0, t1 = datetime.combine(a, time.min, tz), datetime.combine(b, time.min, tz)
        rows = db.execute(select(AttemptAnswer.is_correct, AttemptAnswer.answer).join(
            Attempt, Attempt.id == AttemptAnswer.attempt_id).where(
            Attempt.user_id == user.id, Attempt.status == "scored", Attempt.submitted_at >= t0,
            Attempt.submitted_at < t1)).all()
        n = sum(1 for c, ans in rows if ans and (ans or {}).get("value") not in (None, "", []))
        c = sum(1 for ok, _ in rows if ok)
        for s in db.scalars(select(PracticeSession).where(PracticeSession.user_id == user.id,
                                                          PracticeSession.status == "submitted",
                                                          PracticeSession.submitted_at >= t0,
                                                          PracticeSession.submitted_at < t1)):
            n += sum(1 for r in s.results if r["status"] != "unanswered")
            c += sum(1 for r in s.results if r["status"] == "correct")
        tasks = db.scalars(select(StudyTask).where(StudyTask.user_id == user.id, StudyTask.task_date >= a,
                                                   StudyTask.task_date < b, StudyTask.status == "done")).all()
        return {"from": a, "to": b - timedelta(days=1), "questions": n, "correct": c,
                "accuracy": round(c / n, 4) if n else None, "tasks_done": len(tasks),
                "minutes": sum((t.actual_minutes or t.minutes) for t in tasks)}

    this, last = window(start, start + timedelta(days=7)), window(start - timedelta(days=7), start)
    change = None if this["accuracy"] is None or last["accuracy"] is None else round(this["accuracy"] - last["accuracy"], 4)
    return {"this_week": this, "last_week": last, "accuracy_change": change}


def overview(db: Session, user: User, g: ExamGoal) -> dict:
    exam = db.get(Exam, g.exam_id)
    cd = countdown(db, g, exam)
    topics = mastery.exam_topic_view(db, user.id, g.exam_id, max(cd["days_remaining"], 0))
    stats = mock_stats(db, user, g.exam_id)
    plan = planner.plan_view(db, user, g, cd["today"], cd["today"] + timedelta(days=6))
    today_tasks = next((d["tasks"] for d in plan["days"] if d["date"] == cd["today"]), [])
    nb = notebook.counts(db, user.id)
    return {
        "exam": cd,
        "coverage": coverage(topics),
        "mock_tests": stats,
        "subjects": mastery.subject_summary(topics),
        "topics": {
            "strong": [_topic_brief(t) for t in topics if t["mastered"] or t["status"] == "strong"],
            "weak": [_topic_brief(t) for t in topics if t["status"] in ("weak", "very_weak")],
            "pending": [_topic_brief(t) for t in topics if t["status"] in ("not_started", "insufficient_data")],
            "needs_revision": [_topic_brief(t) for t in topics if t["mastered"] and t["last_seen_at"]
                               and (utcnow() - t["last_seen_at"]).days >= 7],
            "all": [_topic_brief(t) for t in topics],
        },
        "revision": {"notebook_due": nb["due"], "notebook_active": nb["all"] - nb["resolved"],
                     "notebook_resolved": nb["resolved"]},
        "recommendations": recommendations(db, user, g, topics, stats, today_tasks),
        "plan": {"note": (g.plan_meta or {}).get("note"), "version": g.plan_version,
                 "generated_at": g.plan_generated_at, "today": today_tasks, "next_days": plan["days"],
                 "week": plan["week"], "tradeoffs": (g.plan_meta or {}).get("tradeoffs", [])},
        "weekly_progress": weekly_progress(db, user, cd["today"]),
    }


def dashboard(db: Session, user: User, goal_id: int | None) -> dict:
    all_goals = goals(db, user)
    if not all_goals:
        return {"goals": [], "selected": None}
    if goal_id is None:
        goal_id = next((x["goal_id"] for x in all_goals if x["days_remaining"] >= 0), all_goals[0]["goal_id"])
    g = own_goal(db, user, goal_id)
    return {"goals": all_goals, "selected": overview(db, user, g)}


def topics_for(db: Session, user: User, goal_id: int | None, exam_ref, status: str | None) -> dict:
    if goal_id is not None:
        g = own_goal(db, user, goal_id)
        exam_id, days = g.exam_id, (g.exam_date - clock.today(clock.user_tz(db, user.id))).days
    elif exam_ref is not None:
        exam_id, days = _exam(db, exam_ref).id, None
    else:
        raise AppError(422, "goal_or_exam_required", "Pass goal_id or exam_id")
    topics = mastery.exam_topic_view(db, user.id, exam_id, days)
    groups = {"weak": ("weak", "very_weak"), "strong": ("strong",), "pending": ("not_started", "insufficient_data"),
              "improving": None}
    if status == "strong":
        topics = [t for t in topics if t["mastered"] or t["status"] == "strong"]
    elif status == "improving":
        topics = [t for t in topics if t.get("trend") == "improving"]
    elif status in groups:
        topics = [t for t in topics if t["status"] in groups[status]]
    elif status is not None:
        raise AppError(422, "invalid_status", "status must be weak, strong, pending or improving")
    return {"exam_id": str(exam_id), "min_evidence": cfg.min_evidence(), "items": [_topic_brief(t) | {
        "weightage": t["weightage"], "by_difficulty": t["by_difficulty"], "wrong": t["wrong"], "skipped": t["skipped"],
        "recent_accuracy": t["recent_accuracy"], "sessions": t["sessions"], "reason": planner._topic_reason(t)}
        for t in topics]}
