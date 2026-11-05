"""AI Personal Exam Mentor endpoints. Every route works on the signed-in student's own data only.

Mock submission and scoring stay on the existing exam endpoints (POST /attempts/{id}/submit); scoring now also
updates topic evidence, the mistake notebook and the study plan.
"""

import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.ratelimit import hit
from app.db import get_db
from app.models import User
from app.schemas.mentor import (
    BookmarkIn,
    ChatIn,
    GoalIn,
    GoalPatch,
    MistakeQuizIn,
    NotebookPatch,
    NotificationPrefsIn,
    PlanGenerateIn,
    PracticeSubmitIn,
    TaskPatch,
    TopicQuizIn,
)
from app.services.mentor import analysis, chat, clock, dashboard, notebook, planner, practice, reminders

router = APIRouter(tags=["AI mentor"])


# ---- mock analysis ----------------------------------------------------------------------------------------------
@router.get("/attempts/{attempt_id}/analysis")
def attempt_analysis(attempt_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Where every lost mark went (incorrect, negative marking, unattempted, partial: no double counting), subject and
    topic tables, question-wise time against configurable targets, time observations and recommendations."""
    return analysis.attempt_analysis(db, user, attempt_id)


@router.get("/attempts/{attempt_id}/analysis/coach-note")
def attempt_coach_note(attempt_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Short AI coaching note on the analysis. Only numbers from the analysis are accepted; otherwise code wording."""
    hit(f"mentor_note:{user.id}", 20, 60)
    return analysis.coach_note(db, user, attempt_id)


# ---- exam goals and countdown -----------------------------------------------------------------------------------
@router.get("/me/exam-goals")
def list_goals(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Every upcoming exam the student tracks, with the live countdown (in the student's time zone)."""
    return {"items": dashboard.goals(db, user)}


@router.post("/me/exam-goals", status_code=201)
def create_goal(body: GoalIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Adds an exam with its date and daily study time and builds the first plan."""
    g = dashboard.create_goal(db, user, body.exam_id, body.exam_date, body.daily_minutes, body.rest_weekday)
    return dashboard.countdown(db, g) | {"plan": g.plan_meta}


@router.patch("/me/exam-goals/{goal_id}")
def update_goal(goal_id: int, body: GoalPatch, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Changing the exam date, daily minutes or rest day regenerates the plan from today."""
    changes = body.model_dump(exclude_unset=True, exclude={"clear_rest_day"})
    changes = {k: v for k, v in changes.items() if v is not None}
    if body.clear_rest_day:
        changes["rest_weekday"] = None
    g = dashboard.update_goal(db, user, goal_id, changes)
    return dashboard.countdown(db, g) | {"plan": g.plan_meta}


@router.delete("/me/exam-goals/{goal_id}", status_code=204)
def archive_goal(goal_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    dashboard.archive_goal(db, user, goal_id)


@router.get("/me/exams/countdown")
def countdown(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"items": dashboard.goals(db, user)}


# ---- dashboard, topics, recommendations ---------------------------------------------------------------------------
@router.get("/me/mentor/dashboard")
def mentor_dashboard(goal_id: int | None = None, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Exam overview, mock performance, subjects, topic analysis, today's recommendations, this week's calendar."""
    return dashboard.dashboard(db, user, goal_id)


@router.get("/me/mentor/topics")
def mentor_topics(goal_id: int | None = None, exam_id: str | None = None,
                  status: str | None = Query(default=None, description="weak | strong | pending | improving"),
                  user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Topic-wise evidence, status, confidence and priority. A topic needs `min_evidence` attempted questions before
    it is called weak or strong."""
    return dashboard.topics_for(db, user, goal_id, exam_id, status)


@router.get("/me/mentor/recommendations")
def mentor_recommendations(goal_id: int | None = None, user: User = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    d = dashboard.dashboard(db, user, goal_id)
    if d["selected"] is None:
        return {"goal_id": None, "recommendations": None}
    return {"goal_id": d["selected"]["exam"]["goal_id"], "recommendations": d["selected"]["recommendations"],
            "plan_note": d["selected"]["plan"]["note"]}


# ---- study plan ---------------------------------------------------------------------------------------------------
@router.get("/me/study-plan")
def study_plan(goal_id: int, start: date | None = None, end: date | None = None,
               user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Day-by-day tasks (pending, done, skipped, missed) between `start` and `end` (default: last 7 to next 30 days)."""
    return planner.plan_view(db, user, dashboard.own_goal(db, user, goal_id), start, end)


@router.post("/me/study-plan/generate")
def generate_plan(body: PlanGenerateIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Rebuilds the plan from today with the latest results. Done and skipped tasks are kept as history."""
    hit(f"plan_generate:{user.id}", 6, 60)
    g = dashboard.own_goal(db, user, body.goal_id)
    planner.generate(db, g)
    return planner.plan_view(db, user, g, None, None)


@router.patch("/me/study-plan/tasks/{task_id}")
def update_task(task_id: int, body: TaskPatch, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    t = planner.update_task(db, user, task_id, body.status, body.actual_minutes)
    return planner.serialize_task(t, {}, clock.today(clock.user_tz(db, user.id)))


# ---- mistake notebook and practice --------------------------------------------------------------------------------
@router.get("/me/mistake-notebook")
def mistake_notebook(filter: str = "all", topic_id: int | None = None, exam_id: uuid.UUID | None = None,
                     limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0),
                     user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """filter: all | wrong | corrected | repeated | slow | bookmarked | due | resolved."""
    return notebook.listing(db, user, filter, topic_id, exam_id, limit, offset)


@router.patch("/me/mistake-notebook/{entry_id}")
def update_entry(entry_id: int, body: NotebookPatch, user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    changes = body.model_dump(exclude_unset=True, exclude={"clear_mistake_type"})
    if body.clear_mistake_type:
        changes["mistake_type"] = None
    elif changes.get("mistake_type") is None:
        changes.pop("mistake_type", None)
    return notebook.update(db, user, entry_id, changes)


@router.post("/me/mistake-notebook/bookmarks", status_code=201)
def bookmark(body: BookmarkIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return notebook.bookmark_question(db, user, body.question_id, body.attempt_id)


@router.post("/me/practice/mistake-review", status_code=201)
def start_mistake_review(body: MistakeQuizIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """A revision quiz from the notebook: due cards first (spaced revision), questions without answers."""
    hit(f"practice_start:{user.id}", 20, 60)
    return practice.start_mistake_review(db, user, body.count, body.topic_id, body.task_id)


@router.post("/me/practice/topic-quiz", status_code=201)
def start_topic_quiz(body: TopicQuizIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """A short quiz on one topic at the student's current level, unseen questions first."""
    hit(f"practice_start:{user.id}", 20, 60)
    return practice.start_topic_quiz(db, user, body.topic_id, body.count, body.task_id, body.level)


@router.post("/me/practice/{session_id}/submit")
def submit_practice(session_id: uuid.UUID, body: PracticeSubmitIn, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    return practice.submit(db, user, session_id, [a.model_dump() for a in body.answers])


# ---- chat and reminders -------------------------------------------------------------------------------------------
@router.post("/me/mentor/chat")
def mentor_chat(body: ChatIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Ask the mentor. Answers come from the student's stored performance; cited numbers are checked by code."""
    hit(f"mentor_chat:{user.id}", 10, 60)
    return chat.ask(db, user, body.message, body.goal_id)


@router.get("/me/mentor/chat")
def mentor_chat_history(limit: int = Query(default=30, ge=1, le=100), user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    return {"items": chat.history(db, user, limit)}


@router.get("/me/notification-preferences")
def get_prefs(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return reminders.pref_out(reminders.preferences(db, user.id))


@router.put("/me/notification-preferences")
@router.post("/me/notification-preferences")
def save_prefs(body: NotificationPrefsIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Reminder times (24h HH:MM, student's time zone), channels, which reminders, and the daily cap (1-5)."""
    return reminders.save_preferences(db, user, body.model_dump(exclude_unset=True))
