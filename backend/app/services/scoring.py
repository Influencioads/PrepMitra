"""Deterministic scoring and analytics (PDF 6: "numbers by code, words by AI").

Everything here is pure and reproducible from the stored answers, so a score can always be re-derived.
"""

from statistics import mean

CARELESS_TIME_RATIO = 0.6  # wrong on an easy question answered faster than 60% of the expected time
GUESS_TIME_RATIO = 0.35  # wrong under negative marking, answered in under 35% of the expected time
TIME_SINK_RATIO = 2.0  # took more than twice the expected time


def score_question(qtype: str, correct, answer, marks: float, negative: float, scheme: dict) -> tuple[str, float]:
    """Returns (status, marks_awarded); status is correct | wrong | partial | unanswered."""
    value = None if answer is None else answer.get("value") if isinstance(answer, dict) else answer
    if value is None or value == "" or value == []:
        return "unanswered", -float(scheme.get("unanswered", 0) or 0)
    neg = float(negative or 0)
    if qtype == "numeric" and not scheme.get("numeric_negative", False):
        neg = 0.0
    if qtype == "multi" and not scheme.get("multi_negative", True):
        neg = 0.0
    if qtype == "single":
        return ("correct", float(marks)) if str(value) == str(correct) else ("wrong", -neg)
    if qtype == "multi":
        given, right = set(value if isinstance(value, list) else [value]), set(correct)
        if given == right:
            return "correct", float(marks)
        if scheme.get("multi_partial") and given < right and given:
            return "partial", round(float(marks) * len(given) / len(right), 4)
        return "wrong", -neg
    try:
        ok = abs(float(value) - float(correct)) <= float(scheme.get("numeric_tolerance", 0.01))
    except (TypeError, ValueError):
        ok = False
    return ("correct", float(marks)) if ok else ("wrong", -neg)


def classify_error(status: str, difficulty: str, time_sec: int, expected: int, negative: float) -> str | None:
    if status == "wrong":
        if difficulty == "easy" and time_sec < CARELESS_TIME_RATIO * expected:
            return "careless_easy"
        if negative > 0 and time_sec < GUESS_TIME_RATIO * expected:
            return "negative_guess"
        if time_sec > TIME_SINK_RATIO * expected:
            return "time_sink"
        return "wrong"
    if status == "unanswered" and time_sec > TIME_SINK_RATIO * expected:
        return "time_sink"
    return None


def analyse(items: list[dict], sections: list[dict], scheme: dict) -> dict:
    """items: one dict per paper question with keys
    ref, question_id, section_key, topic_id, topic_name, type, difficulty, expected_time_sec, correct, answer,
    time_spent_sec, marked_for_review.
    """
    sec_by_key = {s["key"]: s for s in sections}
    rows = []
    for it in items:
        s = sec_by_key[it["section_key"]]
        status, marks = score_question(it["type"], it["correct"], it["answer"], s["marks_per_question"],
                                       s.get("negative_marks", 0), scheme)
        err = classify_error(status, it["difficulty"], it["time_spent_sec"], it["expected_time_sec"],
                             float(s.get("negative_marks", 0) or 0))
        rows.append({**it, "status": status, "marks": marks, "error_type": err})

    attempted = [r for r in rows if r["status"] != "unanswered"]
    correct = [r for r in rows if r["status"] == "correct"]
    score = round(sum(r["marks"] for r in rows), 4)
    max_score = float(sum(s["question_count"] * s["marks_per_question"] for s in sections))
    negative_loss = round(-sum(r["marks"] for r in rows if r["marks"] < 0), 4)

    section_stats = []
    for s in sections:
        mine = [r for r in rows if r["section_key"] == s["key"]]
        att = [r for r in mine if r["status"] != "unanswered"]
        section_stats.append({
            "key": s["key"], "name": s.get("name", s["key"]),
            "score": round(sum(r["marks"] for r in mine), 4),
            "max_score": float(s["question_count"] * s["marks_per_question"]),
            "attempted": len(att), "correct": sum(1 for r in mine if r["status"] == "correct"),
            "wrong": sum(1 for r in mine if r["status"] == "wrong"),
            "unanswered": len(mine) - len(att),
            "accuracy": round(sum(1 for r in att if r["status"] == "correct") / len(att), 4) if att else None,
            "time_sec": sum(r["time_spent_sec"] for r in mine),
        })

    topic_stats = {}
    for r in rows:
        t = topic_stats.setdefault(r["topic_id"], {"topic_id": r["topic_id"], "name": r["topic_name"],
                                                   "section_key": r["section_key"], "total": 0, "attempted": 0,
                                                   "correct": 0, "times": [], "wrong_refs": []})
        t["total"] += 1
        t["times"].append(r["time_spent_sec"])
        if r["status"] != "unanswered":
            t["attempted"] += 1
        if r["status"] == "correct":
            t["correct"] += 1
        else:
            t["wrong_refs"].append(r["ref"])
    topics = []
    for t in topic_stats.values():
        times = t.pop("times")
        t["accuracy"] = round(t["correct"] / t["attempted"], 4) if t["attempted"] else None
        t["avg_time_sec"] = round(mean(times), 1) if times else 0
        topics.append(t)
    topics.sort(key=lambda t: (t["accuracy"] if t["accuracy"] is not None else -1))

    patterns = []

    def add(kind, desc, refs, lost):
        if refs:
            patterns.append({"type": kind, "description": desc, "question_refs": refs, "marks_lost": round(lost, 4)})

    by_err = lambda e: [r for r in rows if r["error_type"] == e]  # noqa: E731
    add("careless_easy", "Wrong answers on easy questions answered quickly", [r["ref"] for r in by_err("careless_easy")],
        sum(sec_by_key[r["section_key"]]["marks_per_question"] - r["marks"] for r in by_err("careless_easy")))
    add("negative_guess", "Fast guesses that lost negative marks", [r["ref"] for r in by_err("negative_guess")],
        -sum(r["marks"] for r in by_err("negative_guess")))
    add("time_sink", "Questions that took more than twice the expected time", [r["ref"] for r in by_err("time_sink")],
        0.0)
    for s in section_stats:
        if s["attempted"] == 0:
            add("skipped_section", f"Skipped the whole {s['name']} section",
                [r["ref"] for r in rows if r["section_key"] == s["key"]], 0.0)

    times = [r["time_spent_sec"] for r in rows]
    return {
        "score": score, "max_score": max_score,
        "accuracy": round(len(correct) / len(attempted), 4) if attempted else None,
        "attempted": len(attempted), "correct": len(correct),
        "wrong": sum(1 for r in rows if r["status"] == "wrong"),
        "partial": sum(1 for r in rows if r["status"] == "partial"),
        "unanswered": len(rows) - len(attempted),
        "negative_marks_lost": negative_loss,
        "total_time_sec": sum(times), "avg_time_per_question_sec": round(mean(times), 1) if times else 0,
        "sections": section_stats,
        "topics": topics,
        "error_patterns": patterns,
        "questions": [
            {"ref": r["ref"], "question_id": str(r["question_id"]), "section_key": r["section_key"],
             "topic": r["topic_name"], "difficulty": r["difficulty"], "status": r["status"], "marks": r["marks"],
             "time_sec": r["time_spent_sec"], "expected_time_sec": r["expected_time_sec"],
             "marked_for_review": r["marked_for_review"], "error_type": r["error_type"]}
            for r in rows
        ],
    }


def percentile(score: float, others: list[float]) -> float | None:
    """Percentile rank among platform attempts of the same exam (ties count half)."""
    if not others:
        return None
    below = sum(1 for o in others if o < score)
    equal = sum(1 for o in others if o == score)
    return round(100.0 * (below + 0.5 * equal) / len(others), 2)
