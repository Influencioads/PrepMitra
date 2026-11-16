"""AI student / teach-back (redesign): the student explains a concept to Chotu, an AI junior aspirant.

Three rounds per concept. Scores (clarity, correctness, examples; 0-10 each) come from a fixed rubric computed by code:
picked explanations carry fixed scores, and free-text answers are scored on keywords, length and examples. The margin
note for a free-text answer is written by AI when available, with a code-written fallback.
"""

from __future__ import annotations

import re

from sqlalchemy.orm import Session

from app.ai.safety import wrap_data
from app.core.errors import AppError, not_found
from app.models import User
from app.services.mentor.ai import grounded_json


def _opt(key: str, text: str, scores: tuple[int, int, int], note: str, good: bool) -> dict:
    return {"key": key, "text": text, "scores": dict(zip(("clarity", "correctness", "examples"), scores)),
            "note": note, "good": good}


CONCEPTS: list[dict] = [
    {"id": "syllogism-all-some", "topic": "Syllogism",
     "board": ["All A are B.", "Some B are C."], "ask": "Can we say: Some A are C?",
     "diagram": "venn-all-some",
     "rounds": [
         {"kind": "Conclusion check", "mood": "curious",
          "chotu": "Bhaiya, A sits inside B, and B touches C… so some A must be C, na? Looks obvious to me!",
          "coach_hint": "Ask yourself: is it ALWAYS true, or just possible? Only \"always\" follows.",
          "keywords": ["draw", "outside", "not follow", "doesn't follow", "does not follow", "possib", "always"],
          "options": [
              _opt("A", "Yes, it follows. A is inside B and C touches B, so A and C have to meet somewhere.", (6, 0, 2),
                   "Chotu agrees — but you taught him the classic trap. C can touch B away from A.", False),
              _opt("B", "Draw it. Put A fully inside B. C can overlap only the part of B outside A — so no A has to be C. It does not follow.", (9, 10, 9),
                   "Spot on. You showed one drawing that breaks the conclusion — that is the proof.", True),
              _opt("C", "No conclusion — the middle term B is not distributed in either statement.", (5, 8, 2),
                   "Correct, but Chotu does not know what \"distributed\" means. Show him with a drawing.", True)]},
         {"kind": "Possibility", "mood": "confused",
          "chotu": "Okay, it doesn't follow. But then is \"Some A are C\" false? Should I mark it wrong?",
          "coach_hint": "Not following is different from being false. Can it be true in some drawing?",
          "keywords": ["possib", "can be", "may be", "might", "either", "both", "draw"],
          "options": [
              _opt("A", "Yes, it is false. If it does not follow, it is wrong.", (6, 0, 0),
                   "Careful — \"does not follow\" is not \"false\". It can still be true in another drawing.", False),
              _opt("B", "Not false — it is a possibility. Draw C over A too and it becomes true. Exams ask this as \"Some A being C is a possibility\".", (9, 10, 8),
                   "Great. Two drawings, two outcomes — so it is only a possibility.", True),
              _opt("C", "We cannot say anything about A and C at all.", (6, 6, 0),
                   "Half right. We can say it is possible. Show him a drawing where it is true.", False)]},
         {"kind": "Flip it", "mood": "testing",
          "chotu": "What if it said \"Some A are B. All B are C.\" Now does Some A are C follow?",
          "coach_hint": "Some + All = Some. The middle term carries it.",
          "keywords": ["follow", "some + all", "inside", "all b", "carries", "draw"],
          "options": [
              _opt("A", "Yes. The part of A inside B is also inside C, because all of B is inside C. So some A are C.", (9, 10, 8),
                   "Exactly — Some + All = Some. You traced the overlap through B.", True),
              _opt("B", "No, same as before — it never follows.", (5, 0, 0),
                   "Order matters. With \"All B are C\", every bit of B sits inside C.", False),
              _opt("C", "Only a possibility.", (5, 3, 0),
                   "Draw it: the A-and-B overlap is inside B, and B is inside C. It is definite.", False)]},
     ]},
    {"id": "right-anticlockwise", "topic": "Circular seating",
     "board": ["Six people sit around a table,", "facing the centre."], "ask": "Is \"right\" clockwise or anticlockwise?",
     "diagram": "circle-6",
     "rounds": [
         {"kind": "Direction", "mood": "curious",
          "chotu": "Right is always clockwise na? Like a clock goes to the right?",
          "coach_hint": "Sit at the table yourself. Which way does your right hand point?",
          "keywords": ["anticlockwise", "anti-clockwise", "counter", "facing", "centre", "center", "hand"],
          "options": [
              _opt("A", "Yes, right is clockwise always.", (6, 0, 0), "That is true only when people face outside.", False),
              _opt("B", "Facing the centre, your right hand points anticlockwise. So right = anticlockwise, left = clockwise.", (9, 10, 7),
                   "Clear and correct. The \"sit at the table\" picture makes it stick.", True),
              _opt("C", "It depends on the question.", (4, 5, 0), "True but vague. Say what it depends on: facing in or out.", False)]},
         {"kind": "Facing outside", "mood": "confused",
          "chotu": "And if they face outside, everything flips?",
          "coach_hint": "Turn around in your chair. What happens to your right hand?",
          "keywords": ["flip", "clockwise", "reverse", "opposite", "turn"],
          "options": [
              _opt("A", "Yes. Facing outside, right = clockwise and left = anticlockwise.", (9, 10, 5),
                   "Correct. Add an example and Chotu will never forget it.", True),
              _opt("B", "No, it stays the same.", (5, 0, 0), "Turn around and check — your right hand now points the other way.", False),
              _opt("C", "Only left flips.", (4, 0, 0), "Both flip together.", False)]},
         {"kind": "Count it", "mood": "testing",
          "chotu": "D is at the top, facing the centre. Who is 2nd to the right of D if seats go D, F, E, C, A, B clockwise?",
          "coach_hint": "Right = anticlockwise. Count two seats that way.",
          "keywords": ["a", "anticlockwise", "count", "two"],
          "options": [
              _opt("A", "E — count two clockwise.", (6, 0, 4), "That is 2nd to the left.", False),
              _opt("B", "A — right is anticlockwise, so count B (1), A (2).", (9, 10, 9), "Perfect, and you showed the counting.", True),
              _opt("C", "B", (3, 0, 0), "B is only 1st to the right.", False)]},
     ]},
]
BY_ID = {c["id"]: c for c in CONCEPTS}
NOTE_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["note"], "properties": {"note": {"type": "string"}}}
NOTE_SYSTEM = ("You are Mitra, a warm exam coach marking a student's explanation of a concept to a junior. Write one "
               "or two short sentences: what was right, and one thing to add. Do not give a score. Plain words.")


def _public_round(r: dict) -> dict:
    return {"kind": r["kind"], "mood": r["mood"], "chotu": r["chotu"], "coach_hint": r["coach_hint"],
            "options": [{"key": o["key"], "text": o["text"]} for o in r["options"]]}


def index() -> dict:
    return {"items": [{"id": c["id"], "topic": c["topic"], "ask": c["ask"]} for c in CONCEPTS]}


def get(concept_id: str) -> dict:
    c = BY_ID.get(concept_id)
    if c is None:
        raise not_found("Concept")
    return {"id": c["id"], "topic": c["topic"], "board": c["board"], "ask": c["ask"], "diagram": c["diagram"],
            "rounds": [_public_round(r) for r in c["rounds"]]}


def rubric(text: str, keywords: list[str]) -> dict:
    """Free-text scores, 0-10 each, by code."""
    t = text.lower()
    words = len(re.findall(r"\w+", t))
    hits = sum(1 for k in keywords if k in t)
    clarity = 3 if words < 6 else 9 if words <= 45 else 7 if words <= 80 else 5
    correctness = min(10, hits * 3 + (1 if words >= 8 else 0))
    examples = min(10, (5 if re.search(r"\b(e\.?g\.?|for example|like|suppose|draw|imagine)\b", t) else 0)
                   + (3 if re.search(r"\d", t) else 0) + (2 if re.search(r"\b[a-f]\b", t) else 0))
    return {"clarity": clarity, "correctness": correctness, "examples": examples}


def answer(db: Session, user: User, concept_id: str, round_: int, choice: str | None, text: str | None) -> dict:
    c = BY_ID.get(concept_id)
    if c is None or not 0 <= round_ < len(c["rounds"]):
        raise not_found("Round")
    r = c["rounds"][round_]
    if choice:
        opt = next((o for o in r["options"] if o["key"] == choice.upper()), None)
        if opt is None:
            raise AppError(422, "bad_choice", "Pick one of the options")
        scores, note, good, written = opt["scores"], opt["note"], opt["good"], opt["text"]
    else:
        written = (text or "").strip()
        if len(written) < 3:
            raise AppError(422, "empty_answer", "Write your explanation")
        if len(written) > 1200:
            raise AppError(422, "too_long", "Keep it under 1,200 characters")
        scores = rubric(written, r["keywords"])
        good = scores["correctness"] >= 6
        facts = {"scores": scores, "question": r["chotu"]}
        out = grounded_json(purpose="mentor_attempt_note", system=NOTE_SYSTEM, schema=NOTE_SCHEMA,
                            prompt=wrap_data("chotu_question", r["chotu"]) + "\n" + wrap_data("explanation", written),
                            facts=facts, text_fields=["note"], ref_id=user.id, db=db)
        note = (out or {}).get("note") or (
            "Good — you named the key idea. Add a quick drawing or example so it sticks." if good else
            f"Not quite. {r['coach_hint']}")
    reply = ("Ohh, samajh gaya! Next one…" if good else "Hmm, I'm still confused…") if round_ < len(c["rounds"]) - 1 \
        else ("Thank you bhaiya, now I can do these!" if good else "I think I need one more try…")
    return {"round": round_, "scores": scores, "total": sum(scores.values()), "max_total": 30, "good": good,
            "note": note, "written": written, "chotu_reply": reply, "done": round_ == len(c["rounds"]) - 1}
