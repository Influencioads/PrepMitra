"""Persona AI (feature 3), Rank & Cutoff Predictor (5) and the weekly Mistake Notebook summary (11).

Code computes every number: topic mastery 0-100, error-type mix, seconds per question, consistency, percentiles,
rank band. The model only writes words about those numbers, and its text is rejected if it cites a number that is
not in the data (`grounded_json`).

- Snapshot (everyone, including Free): rebuilt after each new mock; the AI adds a short summary and learning style.
- Deep persona (Pro, monthly): a premium model reads 20+ mocks of evidence and writes a strategy.
- Ultra strategy review (Ultra pack, 1 credit): the same review on the Tier 0 model, for the final 30 days.
"""

import statistics
import uuid
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ai.safety import wrap_data
from app.core.errors import AppError, not_found
from app.db import utcnow
from app.models import Attempt, Exam, NotebookEntry, Persona, Topic, User
from app.services.ai_features import engine
from app.services.mentor import mastery
from app.services.mentor.ai import grounded_json

S = {"type": "string"}


def _obj(props: dict) -> dict:
    return {"type": "object", "additionalProperties": False, "required": list(props), "properties": props}


SNAPSHOT_SCHEMA = _obj({"summary": S, "learning_style": S, "one_habit_to_change": S})
DEEP_SCHEMA = _obj({"summary": S, "strengths": {"type": "array", "items": S}, "risks": {"type": "array", "items": S},
                    "strategy": {"type": "array", "items": S}, "exam_day_plan": S, "learning_style": S})
RANK_SCHEMA = _obj({"explanation": S, "next_steps": {"type": "array", "items": S}})
MISTAKE_SCHEMA = _obj({"summary": S, "patterns": {"type": "array", "items": _obj({"type": S, "advice": S})},
                       "this_week": {"type": "array", "items": S}})

PERSONA_SYSTEM = ("You describe a student's learning profile for an exam-prep app from numbers computed by code. "
                  "Never invent or change a number; cite only numbers present in the data. " + engine.COACH_RULES)


# ---- code-computed profile ----------------------------------------------------------------------------------------
def compute(db: Session, user: User) -> dict:
    topics = []
    for (section, name), e in mastery.pooled_evidence(db, user.id).items():
        c = mastery.classify(e)
        if not c["attempted"]:
            continue
        topics.append({"subject": section, "topic": name, "mastery": round((c["effective_accuracy"] or 0) * 100),
                       "attempted": c["attempted"], "status": c["status"], "trend": c["trend"],
                       "avg_seconds": round(e["time"] / c["attempted"]) if c["attempted"] else None,
                       "time_ratio": c["time_ratio"]})
    topics.sort(key=lambda t: (t["mastery"], -t["attempted"]))
    errors = dict(db.execute(select(func.coalesce(NotebookEntry.mistake_type, NotebookEntry.auto_mistake_type),
                                    func.count()).where(NotebookEntry.user_id == user.id)
                             .group_by(func.coalesce(NotebookEntry.mistake_type, NotebookEntry.auto_mistake_type))).all())
    errors.pop(None, None)
    total_err = sum(errors.values()) or 1
    attempts = db.scalars(select(Attempt).where(Attempt.user_id == user.id, Attempt.status == "scored",
                                                Attempt.max_score.is_not(None))
                          .order_by(Attempt.submitted_at.desc()).limit(20)).all()
    pct = [round(a.score / a.max_score * 100, 1) for a in attempts if a.max_score]
    consistency = None
    if len(pct) >= 3:  # 100 = the same score every time; falls as scores swing
        consistency = max(0, round(100 - statistics.pstdev(pct) * 2))
    slow = [t for t in topics if (t["time_ratio"] or 0) > 1.3]
    return {
        "mocks_taken": len(attempts),
        "latest_attempt_id": str(attempts[0].id) if attempts else None,
        "recent_score_percent": pct[:5],
        "weak_topics": [t for t in topics if t["status"] in ("very_weak", "weak", "needs_improvement")][:5],
        "strong_topics": [t for t in reversed(topics) if t["status"] in ("strong", "good")][:5],
        "topic_mastery": topics,
        "error_mix_percent": {k: round(v * 100 / total_err) for k, v in sorted(errors.items(), key=lambda x: -x[1])},
        "speed_profile": "slow" if len(slow) > len(topics) / 2 and topics else ("mixed" if slow else "on_time"),
        "slow_topics": [t["topic"] for t in slow][:5],
        "consistency_score": consistency,
    }


def _latest(db: Session, user: User, kinds=("snapshot",)) -> Persona | None:
    return db.scalar(select(Persona).where(Persona.user_id == user.id, Persona.kind.in_(kinds))
                     .order_by(Persona.created_at.desc()).limit(1))


def snapshot(db: Session, user: User) -> dict:
    """The current persona. Rebuilt (with one Flash-Lite call) only when a new mock has been submitted."""
    data = compute(db, user)
    last = _latest(db, user)
    if last is not None and last.source_ref == data["latest_attempt_id"]:
        return persona_out(last)
    words = None
    if data["mocks_taken"]:
        facts = {k: data[k] for k in ("recent_score_percent", "weak_topics", "strong_topics", "error_mix_percent",
                                      "speed_profile", "consistency_score", "mocks_taken")}
        words = grounded_json(purpose="mentor_attempt_note", system=PERSONA_SYSTEM, schema=SNAPSHOT_SCHEMA,
                              prompt=wrap_data("profile", str(facts)), facts=facts,
                              text_fields=["summary", "one_habit_to_change"], ref_id=user.id, db=db)
    data["ai"] = words or {"summary": _fallback_summary(data), "learning_style": "",
                           "one_habit_to_change": _fallback_habit(data)}
    p = Persona(user_id=user.id, kind="snapshot", version=(last.version + 1) if last else 1, data=data,
                source_ref=data["latest_attempt_id"])
    db.add(p)
    db.commit()
    return persona_out(p)


def _fallback_summary(d: dict) -> str:
    if not d["mocks_taken"]:
        return "Take your first mock to build your learning profile."
    weak = ", ".join(t["topic"] for t in d["weak_topics"][:3]) or "no clear weak topic yet"
    return f"After {d['mocks_taken']} mock(s), your weakest areas are: {weak}."


def _fallback_habit(d: dict) -> str:
    mix = d["error_mix_percent"]
    if not mix:
        return "Review every wrong answer in your mistake notebook within a day."
    top = next(iter(mix))
    return {"calculation": "Re-check the last step of every calculation before marking.",
            "misread": "Underline what the question asks before you solve.",
            "guessing": "Skip instead of guessing when negative marking applies and you cannot remove two options.",
            "time_pressure": "Set a 90-second limit per question and move on.",
            "concept": "Re-learn the concept before doing more questions on it."}.get(top, "Review your mistakes daily.")


def persona_out(p: Persona) -> dict:
    return {"id": p.id, "kind": p.kind, "version": p.version, "created_at": p.created_at, **p.data}


def deep(db: Session, user: User, *, ultra: bool = False) -> dict:
    """Monthly deep persona (Pro), or the Ultra strategy review (1 Ultra credit)."""
    kind = "ultra" if ultra else "deep"
    if not ultra:
        engine.require_flag(db, user, "deep_persona", "Pro and the Topper Combo")
        last = _latest(db, user, ("deep",))
        if last is not None and last.created_at.replace(tzinfo=None) > (utcnow() - timedelta(days=28)).replace(tzinfo=None):
            return persona_out(last) | {"next_available_at": last.created_at + timedelta(days=28)}
    data = compute(db, user)
    if data["mocks_taken"] < 3:
        raise AppError(409, "not_enough_mocks", "Take at least 3 mocks so the deep persona has enough evidence.")
    ref = uuid.uuid4().hex
    feature = "ultra_credits" if ultra else None
    ctx = engine.charge(db, user, feature, ref_id=ref) if feature else _noop()
    with ctx:
        goal = db.scalar(select(Exam.name).join(Attempt, Attempt.exam_id == Exam.id)
                         .where(Attempt.user_id == user.id).order_by(Attempt.started_at.desc()).limit(1))
        out = grounded_json(purpose="ultra" if ultra else "deep_persona", system=PERSONA_SYSTEM, schema=DEEP_SCHEMA,
                            prompt=f"Target exam: {goal}.\n" + wrap_data("profile", str(data)), facts=data,
                            text_fields=["summary", "exam_day_plan"], ref_id=ref, db=db)
        if out is None:
            raise AppError(503, "ai_unavailable", "The AI is busy right now. Please try again in a minute.")
        last = _latest(db, user, (kind,))
        p = Persona(user_id=user.id, kind=kind, version=(last.version + 1) if last else 1, data=data | {"ai": out},
                    source_ref=data["latest_attempt_id"])
        db.add(p)
        db.commit()
    return persona_out(p)


class _noop:
    def __enter__(self):
        return None

    def __exit__(self, *exc):
        return False


# ---- rank & cutoff predictor (Pro) --------------------------------------------------------------------------------
def rank(db: Session, user: User, exam_id: uuid.UUID) -> dict:
    engine.require_flag(db, user, "rank_predictor", "Pro and the Topper Combo")
    exam = db.get(Exam, exam_id)
    if exam is None:
        raise not_found("Exam")
    mine = db.scalars(select(Attempt).where(Attempt.user_id == user.id, Attempt.exam_id == exam_id,
                                            Attempt.status == "scored", Attempt.max_score.is_not(None))
                      .order_by(Attempt.submitted_at.desc()).limit(3)).all()
    if not mine:
        raise AppError(409, "no_attempts", "Take a mock of this exam first.")
    my_pct = round(statistics.mean(a.score / a.max_score * 100 for a in mine), 1)
    # Best score per student on this exam: the all-PrepMitra distribution.
    best = db.execute(select(Attempt.user_id, func.max(Attempt.score / Attempt.max_score * 100))
                      .where(Attempt.exam_id == exam_id, Attempt.status == "scored", Attempt.max_score > 0)
                      .group_by(Attempt.user_id)).all()
    scores = sorted(float(s) for _, s in best)
    takers = len(scores)
    above = sum(1 for s in scores if s > my_pct)
    rank_now = above + 1
    band = [max(1, rank_now - max(1, round(takers * 0.05))), min(takers, rank_now + max(1, round(takers * 0.05)))]
    percentile = round(100 * sum(1 for s in scores if s <= my_pct) / takers, 1) if takers else None
    scheme = {}
    from app.models import ExamBlueprint

    bp = db.scalar(select(ExamBlueprint).where(ExamBlueprint.exam_id == exam_id)
                   .order_by(ExamBlueprint.version.desc()).limit(1))
    if bp is not None:
        scheme = bp.marking_scheme or {}
    cutoff = scheme.get("last_year_cutoff_percent")
    facts = {"exam": exam.name, "average_score_percent_last_3": my_pct, "prepmitra_test_takers": takers,
             "expected_rank_band": band, "percentile": percentile, "last_year_cutoff_percent": cutoff,
             "gap_to_cutoff_points": round(cutoff - my_pct, 1) if cutoff is not None else None,
             "weak_topics": [t["topic"] for t in compute(db, user)["weak_topics"][:3]]}
    words = grounded_json(purpose="rank_predictor", system=PERSONA_SYSTEM, schema=RANK_SCHEMA,
                          prompt=wrap_data("rank_facts", str(facts)), facts=facts, text_fields=["explanation"],
                          ref_id=user.id, db=db)
    db.commit()
    note = ("Rank is among PrepMitra test-takers on this exam, not the official exam. "
            + ("" if cutoff is not None else "Last year's cutoff is not set for this exam yet."))
    return facts | {"ai": words or {"explanation": "", "next_steps": []}, "note": note}


# ---- weekly mistake summary (Starter+; visual PDF on Tutor Pro) ----------------------------------------------------
def mistake_summary(db: Session, user: User, language: str | None) -> dict:
    engine.require_flag(db, user, "mistake_notebook", "Starter, Pro and the Topper Combo")
    language = engine.lang_of(user, language)
    week = utcnow().strftime("%G-W%V")
    rows = db.execute(select(func.coalesce(NotebookEntry.mistake_type, NotebookEntry.auto_mistake_type), Topic.name,
                             func.count()).join(Topic, Topic.id == NotebookEntry.topic_id, isouter=True)
                      .where(NotebookEntry.user_id == user.id, NotebookEntry.status == "active")
                      .group_by(func.coalesce(NotebookEntry.mistake_type, NotebookEntry.auto_mistake_type),
                                Topic.name)).all()
    groups: dict[str, dict] = {}
    for mtype, topic, n in rows:
        g = groups.setdefault(mtype or "unclassified", {"type": mtype or "unclassified", "count": 0, "topics": {}})
        g["count"] += n
        g["topics"][topic or "Other"] = g["topics"].get(topic or "Other", 0) + n
    facts = {"week": week, "groups": sorted(groups.values(), key=lambda g: -g["count"])}
    if not groups:
        return facts | {"ai": {"summary": "No open mistakes this week. Keep it up!", "patterns": [], "this_week": []}}

    def make():
        out = grounded_json(purpose="mistake_summary", system=PERSONA_SYSTEM, schema=MISTAKE_SCHEMA,
                            prompt=wrap_data("mistakes", str(facts)), facts=facts, text_fields=["summary"],
                            ref_id=user.id, db=db)
        if out is None:
            raise AppError(503, "ai_unavailable", "The AI is busy right now. Please try again in a minute.")
        return facts | {"ai": out}, "mistake_summary"

    art, hit = engine.cached_localized(db, "mistake_summary", f"{user.id}:{week}", language, make, user_id=user.id,
                                       title=f"Mistake summary {week}")
    db.commit()
    return engine.artifact_out(art, cached_hit=hit)
