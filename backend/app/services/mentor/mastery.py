"""Topic evidence, classification and priority (mentor modules 3, 4 and 7).

Evidence is stored per (user, topic) in `user_topic_mastery` and updated by code after every scored mock and every
graded quiz. For a goal exam the mentor pools the evidence of same-named topics in the same subject across exams
(Percentage practised for IBPS PO counts for SBI PO too).

A topic is only classified once it has `min_evidence()` attempted questions; below that it is "not_started" or
"insufficient_data" and the mentor says so instead of calling it weak. "Mastered" needs high accuracy over enough
questions, in at least two sessions, at a reasonable pace, with recent form still high; it is withdrawn automatically
when recent form drops.
"""

import re
import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import utcnow
from app.models import Topic, UserTopicMastery
from app.services.mentor import config as cfg


def record(db: Session, user_id: uuid.UUID, rows: list[dict], now: datetime | None = None) -> None:
    """rows: {topic_id, status (correct|wrong|partial|unanswered), difficulty, time_sec, target_sec} for one session."""
    now = now or utcnow()
    per_topic: dict[int, list[dict]] = {}
    for r in rows:
        if r.get("topic_id") is not None:
            per_topic.setdefault(r["topic_id"], []).append(r)
    for topic_id, rs in per_topic.items():
        attempted = [r for r in rs if r["status"] != "unanswered"]
        skipped = [r for r in rs if r["status"] == "unanswered" and (r.get("time_sec") or 0) > 0]
        if not attempted and not skipped:
            continue  # never opened (ran out of time): no evidence either way
        m = db.get(UserTopicMastery, (user_id, topic_id))
        if m is None:
            m = UserTopicMastery(user_id=user_id, topic_id=topic_id, attempts_count=0, correct_count=0, wrong_count=0,
                                 skipped_count=0, time_spent_sec=0, target_time_sec=0, sessions_count=0,
                                 by_difficulty={})
            db.add(m)
        correct = sum(1 for r in attempted if r["status"] == "correct")
        m.attempts_count = (m.attempts_count or 0) + len(attempted)
        m.correct_count = (m.correct_count or 0) + correct
        m.wrong_count = (m.wrong_count or 0) + sum(1 for r in attempted if r["status"] == "wrong")
        m.skipped_count = (m.skipped_count or 0) + len(skipped)
        m.time_spent_sec = (m.time_spent_sec or 0) + sum(int(r.get("time_sec") or 0) for r in attempted)
        m.target_time_sec = (m.target_time_sec or 0) + sum(int(r.get("target_sec") or 0) for r in attempted)
        bd = {k: list(v) for k, v in (m.by_difficulty or {}).items()}
        for r in attempted:
            cell = bd.setdefault(r.get("difficulty") or "medium", [0, 0])
            cell[0] += 1
            cell[1] += 1 if r["status"] == "correct" else 0
        m.by_difficulty = bd
        if attempted:
            acc = correct / len(attempted)
            alpha = 0.5 if len(attempted) >= 3 else 0.25  # a 1-question session moves recent form only a little
            m.previous_recent_accuracy = m.recent_accuracy
            m.recent_accuracy = round(acc if m.recent_accuracy is None else alpha * acc + (1 - alpha) * m.recent_accuracy, 4)
            m.sessions_count = (m.sessions_count or 0) + 1
        # Laplace-smoothed accuracy, so one lucky answer does not mean "mastered" (kept for existing readers).
        m.mastery_score = round((m.correct_count + 1) / (m.attempts_count + 2), 4)
        m.last_seen_at = now


def topic_key(section_key: str | None, name: str) -> tuple[str, str]:
    return cfg.subject_of(section_key), re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()


def exam_topics(db: Session, exam_id) -> list[Topic]:
    topics = list(db.scalars(select(Topic).where(Topic.exam_id == exam_id)))
    parents = {t.parent_id for t in topics if t.parent_id}
    return [t for t in topics if t.id not in parents]


def pooled_evidence(db: Session, user_id) -> dict[tuple[str, str], dict]:
    """All of the user's mastery rows, summed per (subject, topic name)."""
    out: dict[tuple[str, str], dict] = {}
    rows = db.execute(select(UserTopicMastery, Topic).join(Topic, Topic.id == UserTopicMastery.topic_id)
                      .where(UserTopicMastery.user_id == user_id)).all()
    for m, t in rows:
        e = out.setdefault(topic_key(t.section_key, t.name), {
            "attempted": 0, "correct": 0, "wrong": 0, "skipped": 0, "time": 0, "target": 0, "sessions": 0,
            "by_difficulty": {}, "recent": None, "previous_recent": None, "last_seen_at": None})
        e["attempted"] += m.attempts_count or 0
        e["correct"] += m.correct_count or 0
        e["wrong"] += m.wrong_count or 0
        e["skipped"] += m.skipped_count or 0
        e["time"] += m.time_spent_sec or 0
        e["target"] += m.target_time_sec or 0
        e["sessions"] += m.sessions_count or 0
        for d, (n, c) in (m.by_difficulty or {}).items():
            cell = e["by_difficulty"].setdefault(d, [0, 0])
            cell[0] += n
            cell[1] += c
        if m.recent_accuracy is not None and (e["last_seen_at"] is None or m.last_seen_at > e["last_seen_at"]):
            e["recent"], e["previous_recent"], e["last_seen_at"] = (m.recent_accuracy, m.previous_recent_accuracy,
                                                                    m.last_seen_at)
        elif e["last_seen_at"] is None:
            e["last_seen_at"] = m.last_seen_at
    return out


def _band(acc: float) -> str:
    return next(name for floor, name in cfg.STATUS_BANDS if acc >= floor)


def classify(e: dict | None) -> dict:
    """Status, confidence, level and trend for one topic's evidence. All rules are explicit and testable."""
    e = e or {"attempted": 0, "correct": 0, "wrong": 0, "skipped": 0, "time": 0, "target": 0, "sessions": 0,
              "by_difficulty": {}, "recent": None, "previous_recent": None, "last_seen_at": None}
    n = e["attempted"]
    overall = e["correct"] / n if n else None
    recent = e["recent"]
    effective = None
    if overall is not None:
        effective = cfg.RECENT_WEIGHT * recent + (1 - cfg.RECENT_WEIGHT) * overall \
            if recent is not None and e["sessions"] >= 2 else overall
    time_ratio = round(e["time"] / e["target"], 2) if e["target"] else None
    bd = e["by_difficulty"]
    med_hard = sum(bd.get(d, [0, 0])[0] for d in ("medium", "hard"))
    out = {
        "attempted": n, "correct": e["correct"], "wrong": e["wrong"], "skipped": e["skipped"],
        "accuracy": round(overall, 4) if overall is not None else None,
        "recent_accuracy": recent, "effective_accuracy": round(effective, 4) if effective is not None else None,
        "time_ratio": time_ratio, "sessions": e["sessions"], "last_seen_at": e["last_seen_at"],
        "by_difficulty": {d: {"attempted": v[0], "correct": v[1]} for d, v in bd.items()},
        "trend": None, "mastered": False, "notes": [],
    }
    if n == 0:
        out.update(status="not_started", confidence="none", level="basic")
        if e["skipped"]:
            out["notes"].append(f"Skipped {e['skipped']} time(s) without attempting")
        return out
    if n < cfg.min_evidence():
        out.update(status="insufficient_data", confidence="low", level="basic" if (overall or 0) < 0.6 else "intermediate")
        out["notes"].append(f"Only {n} question(s) attempted; {cfg.min_evidence()} needed before judging this topic")
        return out
    status = _band(effective)
    if status == "strong" and med_hard < 3:
        status = "good"  # strong only on easy questions is not proven yet
        out["notes"].append("Accuracy so far comes mostly from easy questions")
    if status == "strong" and time_ratio is not None and time_ratio > cfg.SLOW_RATIO:
        status = "good"
        out["notes"].append("Accurate but slow")
    if recent is not None and e["previous_recent"] is not None:
        if recent - e["previous_recent"] >= 0.1:
            out["trend"] = "improving"
        elif e["previous_recent"] - recent >= 0.1:
            out["trend"] = "declining"
    if recent is not None and overall is not None and overall - recent >= cfg.DECLINE_DROP:
        out["trend"] = "declining"
    out["mastered"] = (n >= cfg.MASTERY_MIN_ATTEMPTED and e["sessions"] >= cfg.MASTERY_MIN_SESSIONS
                       and effective >= cfg.MASTERY_MIN_ACCURACY and status == "strong"
                       and (recent is None or recent >= 0.8) and out["trend"] != "declining"
                       and (time_ratio is None or time_ratio <= cfg.MASTERY_MAX_TIME_RATIO))
    conf = "high" if n >= 20 and e["sessions"] >= 2 else "medium"
    easy, med = bd.get("easy", [0, 0]), bd.get("medium", [0, 0])
    if effective < 0.55 or (easy[0] >= 3 and easy[1] / easy[0] < 0.7):
        level = "basic"
    elif med[0] < 4 or med[1] / med[0] < 0.7:
        level = "intermediate"
    else:
        level = "advanced"
    out.update(status=status, confidence=conf, level=level)
    return out


ACTIONS = {
    "not_started": "Learn the concept from basics, then try 15 basic questions",
    "insufficient_data": "Practise a short mixed set so the mentor can judge this topic",
    "very_weak": "Learn from basics: concept lesson, then basic questions",
    "weak": "Concept revision plus daily basic-to-intermediate practice",
    "needs_improvement": "Timed intermediate practice and sectional sets",
    "good": "Mixed practice with harder questions",
    "strong": "Short quizzes to keep it sharp",
}


def prioritise(topics: list[dict], days_left: int | None) -> list[dict]:
    """Adds priority (high | medium | maintenance | low), action and reason to classified exam topics.

    relevance = topic weightage in the exam (from the syllabus / previous-year frequency), scaled 0..1.
    """
    if not topics:
        return topics
    rel_sorted = sorted(t["relevance"] for t in topics)
    median_rel = rel_sorted[len(rel_sorted) // 2]
    short = days_left is not None and days_left <= 10
    for t in topics:
        s, rel = t["status"], t["relevance"]
        important = rel >= median_rel
        tradeoff = None
        if t["mastered"]:
            prio, action = "maintenance", "Completed: weekly revision quiz only"
        elif s == "not_started":
            prio = "high" if important else "medium"
            action = ACTIONS[s]
        elif s == "insufficient_data":
            prio, action = "medium", ACTIONS[s]
        elif s in ("very_weak", "weak"):
            prio, action = ("high" if important else "medium"), ACTIONS[s]
            if short and s == "very_weak" and not important:
                prio = "low"
                tradeoff = (f"With {days_left} days left, this lower-weightage topic would need long practice to "
                            "improve, so the plan gives it light revision only and spends the time on higher-return "
                            "topics, revision and mocks. It is not dropped: pick it up again if time allows.")
        elif s == "needs_improvement":
            prio = "high" if important and t.get("trend") == "declining" else "medium"
            action = ACTIONS[s]
        elif s == "good":
            prio, action = ("medium" if important else "low"), ACTIONS[s]
        else:  # strong, not yet mastered
            prio, action = "low", ACTIONS["strong"]
        if t.get("trend") == "declining" and prio in ("maintenance", "low"):
            prio, action = "medium", "Recent accuracy dropped: back in the plan for focused practice"
        eff = t["effective_accuracy"]
        gain = rel * ((0.85 - eff) if eff is not None else 0.5)
        t.update(priority=prio, action=action, tradeoff=tradeoff, gain=round(max(gain, 0.0), 4))
    order = {"high": 0, "medium": 1, "low": 2, "maintenance": 3}
    topics.sort(key=lambda t: (order[t["priority"]], -t["gain"], t["name"]))
    return topics


def exam_topic_view(db: Session, user_id, exam_id, days_left: int | None = None) -> list[dict]:
    """Every syllabus topic of the exam with pooled evidence, classification and priority."""
    topics = exam_topics(db, exam_id)
    evidence = pooled_evidence(db, user_id)
    max_w = max((t.weightage or 1.0) for t in topics) if topics else 1.0
    out = []
    for t in topics:
        c = classify(evidence.get(topic_key(t.section_key, t.name)))
        out.append({"topic_id": t.id, "name": t.name, "section_key": t.section_key,
                    "subject": cfg.subject_of(t.section_key), "weightage": t.weightage,
                    "relevance": round((t.weightage or 1.0) / max_w, 3), **c})
    return prioritise(out, days_left)


def subject_summary(topics: list[dict]) -> list[dict]:
    by: dict[str, list[dict]] = {}
    for t in topics:
        by.setdefault(t["subject"], []).append(t)
    out = []
    for subj, ts in by.items():
        n = sum(t["attempted"] for t in ts)
        c = sum(t["correct"] for t in ts)
        out.append({"subject": subj, "name": cfg.SUBJECT_NAMES.get(subj, subj.title()), "topics": len(ts),
                    "attempted": n, "accuracy": round(c / n, 4) if n else None,
                    "weak": sum(1 for t in ts if t["status"] in ("weak", "very_weak")),
                    "strong": sum(1 for t in ts if t["status"] == "strong" or t["mastered"]),
                    "not_started": sum(1 for t in ts if t["status"] == "not_started")})
    out.sort(key=lambda s: (s["accuracy"] is None, s["accuracy"] or 0))
    return out
