"""Exam blueprints: validation, and the exact slot plan every generated paper must follow (PDF 5.3 AC)."""

import random

from app.core.languages import is_supported

QTYPES = ("single", "multi", "numeric")
DIFFICULTIES = ("easy", "medium", "hard")


def largest_remainder(total: int, weights: dict[str, float]) -> dict[str, int]:
    """Splits `total` into integer parts proportional to `weights` that always sum to `total`."""
    wsum = sum(weights.values())
    if total <= 0 or wsum <= 0:
        return {k: 0 for k in weights}
    raw = {k: total * w / wsum for k, w in weights.items()}
    out = {k: int(v) for k, v in raw.items()}
    rest = total - sum(out.values())
    for k in sorted(raw, key=lambda k: (raw[k] - out[k], weights[k]), reverse=True)[:rest]:
        out[k] += 1
    return out


def validate(sections: list[dict], duration_min: int, difficulty_mix: dict, languages: list[str],
             topic_section: dict[int, str | None] | None = None) -> list[str]:
    """Returns a list of human-readable problems; empty means valid."""
    errors: list[str] = []
    if not sections:
        errors.append("At least one section is required")
    if duration_min <= 0 or duration_min > 600:
        errors.append("duration_min must be between 1 and 600")
    keys = [s.get("key") for s in sections]
    if len(set(keys)) != len(keys) or not all(keys):
        errors.append("Every section needs a unique, non-empty key")
    for s in sections:
        name = s.get("key", "?")
        count = s.get("question_count", 0)
        if not isinstance(count, int) or count <= 0:
            errors.append(f"Section {name}: question_count must be a positive integer")
            continue
        if (s.get("marks_per_question") or 0) <= 0:
            errors.append(f"Section {name}: marks_per_question must be positive")
        if (s.get("negative_marks") or 0) < 0:
            errors.append(f"Section {name}: negative_marks cannot be negative")
        types = s.get("question_types") or {"single": count}
        if any(t not in QTYPES for t in types):
            errors.append(f"Section {name}: question_types keys must be in {QTYPES}")
        if sum(types.values()) != count:
            errors.append(f"Section {name}: question_types must add up to question_count ({count})")
        for tid in s.get("topic_ids") or []:
            if topic_section is not None and tid not in topic_section:
                errors.append(f"Section {name}: topic {tid} does not belong to this exam")
    if set(difficulty_mix) - set(DIFFICULTIES):
        errors.append("difficulty_mix keys must be easy, medium, hard")
    if round(sum(difficulty_mix.values()), 6) != 100:
        errors.append("difficulty_mix must add up to 100")
    if not languages or "en" not in languages:
        errors.append("languages must include 'en' (English is the master copy)")
    bad = [l for l in languages if not is_supported(l)]
    if bad:
        errors.append(f"Unsupported languages: {bad}")
    return errors


def total_marks(sections: list[dict]) -> float:
    return sum(s["question_count"] * s["marks_per_question"] for s in sections)


def section_topics(section: dict, topics: list) -> list:
    """Leaf topics for a section: explicit topic_ids, else every topic tagged with this section key."""
    ids = set(section.get("topic_ids") or [])
    if ids:
        chosen = [t for t in topics if t.id in ids]
    else:
        chosen = [t for t in topics if t.section_key == section["key"]]
    parents = {t.parent_id for t in chosen if t.parent_id}
    leaves = [t for t in chosen if t.id not in parents]
    return leaves or chosen


def plan_slots(sections: list[dict], difficulty_mix: dict, topics: list, seed: int | None = None,
               topic_boost: dict[int, float] | None = None) -> list[dict]:
    """Exact slot list: per section, the counts of question type, difficulty and topic all match the blueprint.

    `topic_boost` (topic_id -> multiplier) tilts the topic split inside a section towards a user's weak topics;
    section sizes, question types and the difficulty mix are unaffected.

    Returns [{"seq", "section_key", "qtype", "difficulty", "topic_id"}] in exam order.
    """
    rng = random.Random(seed)
    slots: list[dict] = []
    seq = 1
    for s in sections:
        count = s["question_count"]
        types = s.get("question_types") or {"single": count}
        diffs = largest_remainder(count, {d: difficulty_mix.get(d, 0) for d in DIFFICULTIES})
        tops = section_topics(s, topics)
        if not tops:
            raise ValueError(f"Section {s['key']} has no topics; add syllabus topics before generating papers")
        boost = topic_boost or {}
        topic_counts = largest_remainder(count, {str(t.id): (t.weightage or 1.0) * boost.get(t.id, 1.0) for t in tops})

        type_list = [t for t, n in types.items() for _ in range(n)]
        diff_list = [d for d, n in diffs.items() for _ in range(n)]
        topic_list = [int(t) for t, n in topic_counts.items() for _ in range(n)]
        rng.shuffle(type_list)
        rng.shuffle(diff_list)
        rng.shuffle(topic_list)
        section_slots = [
            {"section_key": s["key"], "qtype": q, "difficulty": d, "topic_id": t}
            for q, d, t in zip(type_list, diff_list, topic_list)
        ]
        # Group by topic inside a section, like real papers (all of one topic together).
        section_slots.sort(key=lambda x: (x["topic_id"], DIFFICULTIES.index(x["difficulty"])))
        for sl in section_slots:
            sl["seq"] = seq
            seq += 1
            slots.append(sl)
    return slots


def check_paper(sections: list[dict], difficulty_mix: dict, items: list[dict], questions: dict) -> list[str]:
    """Verifies a built paper against its blueprint. `questions` maps question_id -> Question."""
    problems = []
    for s in sections:
        mine = [questions[str(i["question_id"])] for i in items if i["section_key"] == s["key"]]
        if len(mine) != s["question_count"]:
            problems.append(f"{s['key']}: {len(mine)} questions, expected {s['question_count']}")
            continue
        types = s.get("question_types") or {"single": s["question_count"]}
        for t, n in types.items():
            if sum(1 for q in mine if q.type == t) != n:
                problems.append(f"{s['key']}: wrong count of {t} questions")
        diffs = largest_remainder(s["question_count"], {d: difficulty_mix.get(d, 0) for d in DIFFICULTIES})
        for d, n in diffs.items():
            if sum(1 for q in mine if q.difficulty == d) != n:
                problems.append(f"{s['key']}: wrong count of {d} questions")
    ids = [str(i["question_id"]) for i in items]
    if len(set(ids)) != len(ids):
        problems.append("duplicate questions in paper")
    return problems
