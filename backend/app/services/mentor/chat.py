"""The mentor chatbot (module 11): answers from the student's own stored data, never generic when data exists.

The model receives a compact snapshot computed by code (countdown, recent mocks and where their marks went, topic
statuses, today's and tomorrow's plan, notebook, week-on-week progress). Its answer is rejected if it cites a number
that is not in that snapshot, and a code-written answer for the detected intent is used instead. The same code path
answers when no AI provider is configured.
"""

import json
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ai.safety import DATA_RULES, wrap_data
from app.config import get_settings
from app.core.errors import AppError
from app.db import utcnow
from app.models import Attempt, ExamGoal, MentorMessage, User
from app.services.mentor import analysis, clock, dashboard, notebook
from app.services.mentor.ai import grounded_json

SYSTEM = f"""You are PrepMitra's personal banking-exam mentor talking to one student. Answer using ONLY the student's
data snapshot: their countdown, mock results, where their marks went, topic statuses, plan and progress. Every number
you write must appear in the snapshot; never estimate, round differently or invent statistics, and never claim a topic
is mastered unless the snapshot says so. If the snapshot does not contain what is needed, say what is missing and
what the student can do to get it (for example, take a mock). Be warm, specific and brief (under 140 words): explain
why, what to improve, how, when, and the next step. Plain text, no markdown tables.
{DATA_RULES}"""

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["answer", "follow_ups"],
          "properties": {"answer": {"type": "string"},
                         "follow_ups": {"type": "array", "items": {"type": "string"}, "maxItems": 3}}}


def snapshot(db: Session, user: User, goal: ExamGoal | None) -> dict:
    if goal is None:
        return {"has_goal": False, "note": "No exam date set yet."}
    ov = dashboard.overview(db, user, goal)
    exam_id = goal.exam_id
    recent = db.scalars(select(Attempt).where(Attempt.user_id == user.id, Attempt.exam_id == exam_id,
                                              Attempt.status == "scored").order_by(Attempt.submitted_at.desc())
                        .limit(5)).all()
    last = analysis.analyse_attempt(db, recent[0]) if recent else None
    tomorrow = ov["exam"]["today"] + timedelta(days=1)
    plan_days = {d["date"]: d["tasks"] for d in ov["plan"]["next_days"]}

    def t_out(t):
        return {"name": t["name"], "status": t["status"], "accuracy_pct": None if t["effective_accuracy"] is None
                else round(t["effective_accuracy"] * 100), "attempted": t["attempted"], "priority": t["priority"],
                "trend": t["trend"], "completed": t["mastered"], "time_ratio": t["time_ratio"]}

    return {
        "has_goal": True,
        "exam": {k: ov["exam"][k] for k in ("exam_name", "exam_date", "days_remaining", "weeks_remaining", "phase",
                                            "daily_minutes")},
        "coverage": ov["coverage"],
        "mocks": [{"date": a.submitted_at.date().isoformat() if a.submitted_at else None, "score": a.score,
                   "max_score": a.max_score} for a in recent],
        "last_mock": None if last is None else {
            "score": last["score"], "max_score": last["max_score"],
            "accuracy_pct": None if last["accuracy"] is None else round(last["accuracy"] * 100),
            "marks_lost": last["marks_lost"],
            "sections": [{k: s[k] for k in ("name", "total_marks", "scored", "lost", "lost_incorrect", "lost_negative",
                                            "lost_unattempted", "attempted", "correct", "wrong")} for s in last["sections"]],
            "time_observations": [o["text"] for o in last["time"]["observations"]][:6],
            "recommendations": [r["text"] for r in last["recommendations"]][:5],
            "since_last_attempt": last["since_last_attempt"]},
        "topics": [t_out(t) for t in ov["topics"]["all"]][:30],
        "completed_topics": [t["name"] for t in ov["topics"]["strong"] if t["mastered"]],
        "today_plan": [{"title": t["title"], "minutes": t["minutes"], "status": t["status"]} for t in ov["plan"]["today"]],
        "tomorrow_plan": [{"title": t["title"], "minutes": t["minutes"]} for t in plan_days.get(tomorrow, [])],
        "notebook": ov["revision"],
        "weekly_progress": ov["weekly_progress"],
        "mock_advice": ov["recommendations"]["mock_test"],
        "plan_note": ov["plan"]["note"],
    }


def _pct(x):
    return None if x is None else round(x * 100)


def fallback_answer(question: str, s: dict) -> str:
    """Deterministic answer for the detected intent, from the same snapshot."""
    q = question.lower()
    if not s.get("has_goal"):
        return ("Set your exam and exam date first (Mentor > Add exam). I will then build your day-by-day plan and track "
                "every mock against it.")
    ex, lm = s["exam"], s.get("last_mock")
    if any(w in q for w in ("how many days", "days left", "days are left", "countdown", "when is my exam")):
        return (f"Your {ex['exam_name']} is on {ex['exam_date']}: {ex['days_remaining']} days left "
                f"({ex['weeks_remaining']} weeks). You have covered {s['coverage']['syllabus_completion_pct']}% of the "
                "syllabus so far.")
    if any(w in q for w in ("tomorrow", "revise")):
        items = [t["title"] for t in s["tomorrow_plan"] if t["title"]]
        due = s["notebook"]["notebook_due"]
        return ("Tomorrow: " + ("; ".join(items) if items else "no tasks planned") + "."
                + (f" {due} mistake-notebook card(s) are also due for revision." if due else ""))
    if any(w in q for w in ("today", "study now", "what should i study")):
        items = [f"{t['title']} ({t['minutes']} min)" for t in s["today_plan"] if t["status"] in ("pending", "missed")]
        return ("Today: " + "; ".join(items) + "." if items else
                "Everything planned for today is done. A short mistake-notebook revision is a good extra.")
    if any(w in q for w in ("completed", "mastered", "already")):
        done = s["completed_topics"]
        return (f"Completed topics: {', '.join(done)}. They get short revision quizzes only." if done else
                "No topic is marked completed yet: that needs high accuracy over enough questions in at least two "
                "sessions.")
    if any(w in q for w in ("improv", "last week", "better", "progress")):
        wp = s["weekly_progress"]
        a, b = wp["this_week"]["accuracy"], wp["last_week"]["accuracy"]
        if a is None or b is None:
            return "I need questions answered in both weeks to compare. Keep practising and ask again."
        return (f"This week your accuracy is {_pct(a)}% over {wp['this_week']['questions']} questions, against "
                f"{_pct(b)}% last week. You completed {wp['this_week']['tasks_done']} planned tasks this week.")
    if "mock" in q and any(w in q for w in ("another", "should", "take")):
        return s["mock_advice"]["reason"]
    if lm is None:
        return ("You have not taken a mock for this exam yet. Take one full mock: it shows exactly where you lose "
                "marks, and your plan adapts to it.")
    if any(w in q for w in ("time", "slow", "puzzle", "fast")):
        obs = lm["time_observations"]
        return " ".join(obs[:3]) if obs else "Your time use in the last mock was within target on most questions."
    if any(w in q for w in ("score", "marks", "lose", "lost", "losing", "why")):
        items = sorted(lm["marks_lost"]["items"], key=lambda i: -i["marks"])
        parts = ", ".join(f"{i['reason'].replace('_', ' ')} {i['marks']:g}" for i in items if i["marks"] > 0)
        worst = max(lm["sections"], key=lambda x: x["lost"])
        return (f"In your last mock you scored {lm['score']:g} out of {lm['max_score']:g}. You lost "
                f"{lm['marks_lost']['total_lost']:g} marks: {parts}. The most were lost in {worst['name']} "
                f"({worst['lost']:g} marks).")
    high = [t["name"] for t in s["topics"] if t["priority"] == "high"][:3]
    return (f"{ex['days_remaining']} days to {ex['exam_name']}. Your last mock: {lm['score']:g} out of "
            f"{lm['max_score']:g}." + (f" Focus first on {', '.join(high)}." if high else ""))


def history(db: Session, user: User, limit: int = 30) -> list[dict]:
    rows = db.scalars(select(MentorMessage).where(MentorMessage.user_id == user.id)
                      .order_by(MentorMessage.id.desc()).limit(limit)).all()
    return [{"id": m.id, "role": m.role, "content": m.content, "goal_id": m.goal_id, "created_at": m.created_at,
             "follow_ups": (m.meta or {}).get("follow_ups", []), "source": (m.meta or {}).get("source")}
            for m in reversed(rows)]


def ask(db: Session, user: User, message: str, goal_id: int | None) -> dict:
    message = (message or "").strip()
    if not message:
        raise AppError(422, "empty_message", "Type a question for your mentor")
    today_count = db.scalar(select(func.count()).select_from(MentorMessage).where(
        MentorMessage.user_id == user.id, MentorMessage.role == "student",
        MentorMessage.created_at >= utcnow() - timedelta(days=1))) or 0
    if today_count >= get_settings().mentor_chat_daily_limit:
        raise AppError(429, "mentor_daily_limit", "You have reached today's mentor chat limit. It resets tomorrow.")
    goal = dashboard.own_goal(db, user, goal_id) if goal_id else db.scalar(
        select(ExamGoal).where(ExamGoal.user_id == user.id, ExamGoal.status == "active",
                               ExamGoal.exam_date >= clock.today(clock.user_tz(db, user.id)))
        .order_by(ExamGoal.exam_date).limit(1))
    snap = snapshot(db, user, goal)
    past = history(db, user, limit=6)
    convo = "\n".join(f"{m['role']}: {m['content'][:500]}" for m in past)
    prompt = "\n\n".join([
        wrap_data("student_snapshot", json.dumps(snap, default=str), max_chars=20000),
        wrap_data("recent_conversation", convo, max_chars=4000),
        wrap_data("student_question", message, max_chars=1000),
        "Answer the student's question from the snapshot."])
    raw = grounded_json(purpose="mentor_chat", system=SYSTEM, prompt=prompt, schema=SCHEMA, facts=snap,
                        text_fields=["answer"], ref_id=goal.id if goal else None, db=db,
                        context={"snapshot": snap, "question": message}, tier="strong")
    if raw:
        answer, follow, source = raw["answer"], raw.get("follow_ups", [])[:3], "ai"
    else:
        answer, source = fallback_answer(message, snap), "code"
        follow = ["Where am I losing marks?", "What should I study today?", "Am I improving compared with last week?"]
    db.add(MentorMessage(user_id=user.id, goal_id=goal.id if goal else None, role="student", content=message[:2000],
                         meta={}))
    reply = MentorMessage(user_id=user.id, goal_id=goal.id if goal else None, role="mentor", content=answer,
                          meta={"source": source, "follow_ups": follow})
    db.add(reply)
    db.commit()
    return {"id": reply.id, "role": "mentor", "content": answer, "follow_ups": follow, "source": source,
            "goal_id": goal.id if goal else None, "created_at": reply.created_at,
            "exam": snap.get("exam"), "notebook_due": notebook.due_count(db, user.id)}
