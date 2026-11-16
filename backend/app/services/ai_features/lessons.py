"""Blackboard lessons for the AI tutor (redesign). Fixed, checked content: each lesson is a few board steps plus
"check yourself" questions marked by code. The side chat uses the normal tutor chat (/ai/tutor/chat).
"""

from __future__ import annotations

from app.core.errors import not_found


def _q(text: str, options: list[str], answer: str, why: str) -> dict:
    return {"text": text, "options": [{"key": k, "text": t} for k, t in zip("ABCD", options)], "answer": answer,
            "explanation": why}


LESSONS: list[dict] = [
    {"id": "circular-seating", "subject": "Reasoning", "topic": "Circular seating arrangement",
     "aliases": ["seating", "arrangement", "puzzle", "circular"],
     "question": {"style": "IBPS PO style",
                  "text": "Six friends A, B, C, D, E and F sit around a circular table, all facing the centre.",
                  "clues": ["A is 2nd to the right of D", "B sits between A and D", "E sits opposite B",
                            "C is not a neighbour of D"]},
     "steps": [
         {"title": "Read & draw the table", "lines": ["Draw a circle with 6 seats.", "Everyone faces the centre."],
          "trap": "Facing outside flips left and right. Check the first line every time.", "diagram": {"seats": 6}},
         {"title": "Fix an anchor", "lines": ["Put D at the top seat.", "Every other clue is counted from D."],
          "trap": "Do not start from a clue with \"not\" — it fixes nothing.", "diagram": {"seats": 6, "placed": {"0": "D"}}},
         {"title": "Second to the right", "lines": ["A is 2nd to the RIGHT of D.", "Right = anticlockwise. Count 1, 2 from D. That is A."],
          "trap": "Counting clockwise puts A in E's seat.", "diagram": {"seats": 6, "placed": {"0": "D", "4": "A"}, "arrow": [0, 4]}},
         {"title": "Sitting between", "lines": ["B sits between A and D.", "Only one seat lies between them: B takes it."],
          "trap": "\"Between\" means the seat directly between, not anywhere on that side.",
          "diagram": {"seats": 6, "placed": {"0": "D", "5": "B", "4": "A"}}},
         {"title": "Opposite = 3 seats away", "lines": ["E sits opposite B.", "With 6 seats, opposite is 3 seats away."],
          "trap": "With 8 seats, opposite is 4 away. Count the seats first.",
          "diagram": {"seats": 6, "placed": {"0": "D", "5": "B", "4": "A", "2": "E"}}},
         {"title": "Eliminate & finish", "lines": ["C is not a neighbour of D, so C cannot sit next to D.", "C takes the seat next to E; F sits next to D."],
          "trap": "Read every \"not\" clue last — it only removes options.",
          "diagram": {"seats": 6, "placed": {"0": "D", "5": "B", "4": "A", "2": "E", "3": "C", "1": "F"}}},
     ],
     "check": [_q("Who sits immediately to the LEFT of E?", ["C", "F", "A", "B"], "A",
                  "Left = clockwise when facing the centre. The next seat clockwise from E is C."),
               _q("Who sits opposite A?", ["F", "C", "D", "E"], "A", "A and F are 3 seats apart.")]},
    {"id": "trains-platform", "subject": "Quant", "topic": "Trains crossing a platform",
     "aliases": ["train", "speed", "distance", "time"],
     "question": {"style": "SSC CGL style",
                  "text": "A train 240 m long passes a pole in 16 seconds. How long will it take to cross a 360 m platform?",
                  "clues": ["Train length 240 m", "Pole: 16 s", "Platform 360 m"]},
     "steps": [
         {"title": "What does a pole mean?", "lines": ["Passing a pole, the train covers only its own length.", "Distance = 240 m."],
          "trap": "A pole has no length — do not add anything."},
         {"title": "Find the speed", "lines": ["Speed = 240 ÷ 16 = 15 m/s."], "trap": "Keep metres and seconds; convert to km/h only if the options ask."},
         {"title": "Platform distance", "lines": ["Crossing a platform: train + platform.", "240 + 360 = 600 m."],
          "trap": "Using 360 m alone gives 24 s — the most chosen wrong option."},
         {"title": "Time = distance ÷ speed", "lines": ["600 ÷ 15 = 40 seconds."], "trap": "Check: 15 × 40 = 600."},
     ],
     "check": [_q("A 150 m train passes a pole in 10 s. Its speed?", ["15 m/s", "10 m/s", "25 m/s", "1.5 m/s"], "A", "150 ÷ 10 = 15."),
               _q("Same train, 300 m platform. Time to cross?", ["20 s", "30 s", "45 s", "25 s"], "B", "(150 + 300) ÷ 15 = 30.")]},
    {"id": "syllogism-basics", "subject": "Reasoning", "topic": "Syllogism: All and Some",
     "aliases": ["syllogism"],
     "question": {"style": "IBPS PO style", "text": "All A are B. Some B are C. Can we say: Some A are C?",
                  "clues": ["All A are B", "Some B are C"]},
     "steps": [
         {"title": "Draw the first statement", "lines": ["All A are B: draw A fully inside B."], "trap": "Do not draw A and B as equal circles."},
         {"title": "Add the second", "lines": ["Some B are C: C overlaps B somewhere."], "trap": "\"Some\" does not say where the overlap is."},
         {"title": "Try to break it", "lines": ["Can C overlap B only outside A? Yes.", "Then no A is C."], "trap": "If one valid drawing breaks the conclusion, it does not follow."},
         {"title": "Conclude", "lines": ["Some A are C does NOT follow.", "It is only a possibility."], "trap": "Only \"always true\" conclusions follow."},
     ],
     "check": [_q("Some cats are dogs. All dogs are birds. Some cats are birds?", ["Follows", "Does not follow", "Possibility only", "Cannot say"], "A", "Some + All = Some."),
               _q("All pens are books. Some books are red. Some pens are red?", ["Follows", "Does not follow", "Always true", "Definitely false"], "B", "All + Some gives no definite link.")]},
]
BY_ID = {item["id"]: item for item in LESSONS}


def _public(lesson: dict) -> dict:
    return {**{k: v for k, v in lesson.items() if k not in ("check", "aliases")},
            "check": [{"text": q["text"], "options": q["options"]} for q in lesson["check"]]}


def pick(weak_topics: list[dict]) -> tuple[dict, dict | None]:
    """The lesson for the student's weakest topic that has one, else the first lesson."""
    for t in weak_topics:
        name = str(t.get("topic", "")).lower()
        for lesson in LESSONS:
            if any(a in name for a in lesson["aliases"]):
                return lesson, t
    return LESSONS[0], None


def index(weak_topics: list[dict]) -> dict:
    lesson, why = pick(weak_topics)
    return {"recommended": lesson["id"],
            "why": ({"topic": why["topic"], "mastery": why["mastery"]} if why else None),
            "items": [{"id": x["id"], "subject": x["subject"], "topic": x["topic"], "steps": len(x["steps"])}
                      for x in LESSONS]}


def get(lesson_id: str) -> dict:
    lesson = BY_ID.get(lesson_id)
    if lesson is None:
        raise not_found("Lesson")
    return _public(lesson)


def check(lesson_id: str, index_: int, answer: str) -> dict:
    lesson = BY_ID.get(lesson_id)
    if lesson is None or not 0 <= index_ < len(lesson["check"]):
        raise not_found("Question")
    q = lesson["check"][index_]
    return {"correct": answer.upper() == q["answer"], "answer": q["answer"], "explanation": q["explanation"]}
