"""Pure-function tests: scoring, analytics, percentile, blueprint validation and exact slot plans."""

import pytest

from app.services import blueprints as bp
from app.services.scoring import analyse, classify_error, percentile, score_question


@pytest.mark.parametrize("qtype,correct,answer,scheme,expected", [
    ("single", "B", {"value": "B"}, {}, ("correct", 2.0)),
    ("single", "B", {"value": "C"}, {}, ("wrong", -0.5)),
    ("single", "B", None, {}, ("unanswered", 0.0)),
    ("multi", ["A", "C"], {"value": ["C", "A"]}, {}, ("correct", 2.0)),
    ("multi", ["A", "C"], {"value": ["A"]}, {}, ("wrong", -0.5)),
    ("multi", ["A", "C"], {"value": ["A"]}, {"multi_partial": True}, ("partial", 1.0)),
    ("multi", ["A", "C"], {"value": ["B"]}, {"multi_negative": False}, ("wrong", 0.0)),
    ("numeric", 12.5, {"value": 12.505}, {}, ("correct", 2.0)),
    ("numeric", 12.5, {"value": 13}, {}, ("wrong", 0.0)),  # numeric answers carry no negative marks by default
    ("numeric", 12.5, {"value": 13}, {"numeric_negative": True}, ("wrong", -0.5)),
    ("single", "A", {"value": "B"}, {"unanswered": 0}, ("wrong", -0.5)),
])
def test_score_question(qtype, correct, answer, scheme, expected):
    assert score_question(qtype, correct, answer, 2, 0.5, scheme) == expected


def test_error_classification():
    assert classify_error("wrong", "easy", 10, 60, 0.5) == "careless_easy"
    assert classify_error("wrong", "hard", 10, 60, 0.5) == "negative_guess"
    assert classify_error("wrong", "hard", 10, 60, 0) == "wrong"
    assert classify_error("wrong", "medium", 200, 60, 0.5) == "time_sink"
    assert classify_error("correct", "easy", 5, 60, 0.5) is None


def _item(ref, sec, status_answer, correct="A", diff="medium", t=30, topic=1):
    return {"ref": ref, "question_id": f"q{ref}", "section_key": sec, "topic_id": topic, "topic_name": f"T{topic}",
            "type": "single", "difficulty": diff, "expected_time_sec": 60, "correct": correct,
            "answer": None if status_answer is None else {"value": status_answer}, "time_spent_sec": t,
            "marked_for_review": False}


def test_analyse_totals_sections_and_patterns():
    sections = [{"key": "a", "name": "A", "question_count": 3, "marks_per_question": 2, "negative_marks": 0.5},
                {"key": "b", "name": "B", "question_count": 2, "marks_per_question": 1, "negative_marks": 0.25}]
    items = [_item(1, "a", "A"), _item(2, "a", "B", diff="easy", t=5), _item(3, "a", None),
             _item(4, "b", None, topic=2), _item(5, "b", None, topic=2)]
    out = analyse(items, sections, {})
    assert out["score"] == 2 - 0.5 and out["max_score"] == 8
    assert out["attempted"] == 2 and out["correct"] == 1 and out["accuracy"] == 0.5
    assert out["negative_marks_lost"] == 0.5
    types = {p["type"]: p for p in out["error_patterns"]}
    assert types["careless_easy"]["question_refs"] == [2]
    assert types["skipped_section"]["question_refs"] == [4, 5]
    t1 = next(t for t in out["topics"] if t["topic_id"] == 1)
    assert t1["wrong_refs"] == [2, 3]
    # Reproducible: the same inputs always give the same numbers.
    assert analyse(items, sections, {}) == out


def test_hand_checked_sample_paper():
    """A small prelims-style paper worked out by hand: +1 per correct, -0.25 per wrong, 0 for skipped."""
    sections = [{"key": "quant", "name": "Quant", "question_count": 4, "marks_per_question": 1, "negative_marks": 0.25},
                {"key": "english", "name": "English", "question_count": 3, "marks_per_question": 1,
                 "negative_marks": 0.25}]
    items = [
        _item(1, "quant", "A", t=40, topic=1),  # correct +1
        _item(2, "quant", "B", t=50, topic=1),  # wrong -0.25
        _item(3, "quant", None, t=10, topic=2),  # skipped 0
        _item(4, "quant", "A", t=130, topic=2),  # correct +1 (slow, but correct)
        _item(5, "english", "A", t=20, topic=3),  # correct +1
        _item(6, "english", "C", diff="hard", t=10, topic=3),  # wrong -0.25, a fast guess
        _item(7, "english", None, t=0, topic=3),  # skipped 0
    ]
    out = analyse(items, sections, {})
    assert (out["score"], out["max_score"]) == (2.5, 7.0)
    assert (out["attempted"], out["correct"], out["wrong"], out["unanswered"]) == (5, 3, 2, 2)
    assert (out["accuracy"], out["attempt_rate"], out["negative_marks_lost"]) == (0.6, 0.7143, 0.5)
    assert (out["total_time_sec"], out["avg_time_per_question_sec"]) == (260, 37.1)

    quant, english = out["sections"]
    assert (quant["score"], quant["max_score"], quant["accuracy"], quant["attempt_rate"], quant["time_sec"]) == \
        (1.75, 4.0, 0.6667, 0.75, 230)
    assert (english["score"], english["max_score"], english["accuracy"], english["attempt_rate"],
            english["time_sec"]) == (0.75, 3.0, 0.5, 0.6667, 30)

    topics = {t["topic_id"]: t for t in out["topics"]}
    assert (topics[1]["accuracy"], topics[1]["avg_time_sec"], topics[1]["wrong_refs"]) == (0.5, 45.0, [2])
    assert (topics[2]["accuracy"], topics[2]["avg_time_sec"], topics[2]["wrong_refs"]) == (1.0, 70.0, [3])
    assert (topics[3]["accuracy"], topics[3]["avg_time_sec"], topics[3]["wrong_refs"]) == (0.5, 10.0, [6, 7])

    assert out["error_patterns"] == [{"type": "negative_guess", "description": "Fast guesses that lost negative marks",
                                      "question_refs": [6], "marks_lost": 0.25}]


def test_percentile():
    assert percentile(50, []) is None
    assert percentile(50, [10, 20, 50, 80]) == 62.5
    assert percentile(100, [10, 20]) == 100.0


def test_largest_remainder_always_sums():
    for total in (1, 7, 25, 100):
        parts = bp.largest_remainder(total, {"easy": 30, "medium": 50, "hard": 20})
        assert sum(parts.values()) == total
    assert bp.largest_remainder(25, {"easy": 30, "medium": 50, "hard": 20}) == {"easy": 7, "medium": 13, "hard": 5}


def test_blueprint_validation():
    good = [{"key": "q", "name": "Q", "question_count": 10, "marks_per_question": 1, "negative_marks": 0.25,
             "question_types": {"single": 8, "numeric": 2}}]
    assert bp.validate(good, 30, {"easy": 30, "medium": 50, "hard": 20}, ["en", "hi"]) == []
    errors = bp.validate(
        [{"key": "q", "question_count": 10, "marks_per_question": 0, "question_types": {"single": 9}}],
        0, {"easy": 50, "medium": 40}, ["hi", "xx"])
    joined = " | ".join(errors)
    for expected in ("duration_min", "marks_per_question", "add up to question_count", "difficulty_mix",
                     "must include 'en'", "Unsupported"):
        assert expected in joined


class _T:
    def __init__(self, id, section_key, weightage=1.0, parent_id=None):
        self.id, self.section_key, self.weightage, self.parent_id = id, section_key, weightage, parent_id


def test_slot_plan_matches_blueprint_exactly():
    sections = [{"key": "a", "question_count": 25, "marks_per_question": 2, "question_types": {"single": 20, "numeric": 5}},
                {"key": "b", "question_count": 10, "marks_per_question": 1}]
    topics = [_T(1, "a", 2), _T(2, "a", 1), _T(3, "b")]
    mix = {"easy": 30, "medium": 50, "hard": 20}
    slots = bp.plan_slots(sections, mix, topics, seed=7)
    a = [s for s in slots if s["section_key"] == "a"]
    assert len(a) == 25 and sum(1 for s in a if s["qtype"] == "numeric") == 5
    assert {d: sum(1 for s in a if s["difficulty"] == d) for d in mix} == {"easy": 7, "medium": 13, "hard": 5}
    assert sum(1 for s in a if s["topic_id"] == 1) == 17  # weightage 2:1
    assert [s["seq"] for s in slots] == list(range(1, 36))
    with pytest.raises(ValueError):
        bp.plan_slots([{"key": "c", "question_count": 2, "marks_per_question": 1}], mix, topics)
