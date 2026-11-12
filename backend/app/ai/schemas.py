"""Strict JSON schemas for every LLM call (structured outputs). Code validates the result again after parsing."""


def obj(props: dict, required: list[str] | None = None) -> dict:
    return {"type": "object", "properties": props, "required": required or list(props), "additionalProperties": False}


def arr(items: dict) -> dict:
    return {"type": "array", "items": items}


S = {"type": "string"}
I = {"type": "integer"}
B = {"type": "boolean"}
N = {"type": "number"}

OPTION = obj({"key": S, "text": S})
PLAN_DAY = obj({"day": I, "focus": S, "tasks": arr(S)})

QUESTION = obj({
    "text": S,
    "options": arr(OPTION),
    # single: "B" | multi: "A,C" | numeric: "12.5"
    "answer": S,
    "explanation": S,
    "shortcut": S,
    "subtopic": S,
    "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
    "expected_time_sec": I,
    # Pure arithmetic expression whose value equals the numeric answer, or "" when not applicable.
    "numeric_check": S,
})

VERIFY = obj({"answer": S, "working": S})

TRANSLATION = obj({"text": S, "options": arr(OPTION), "explanation": S, "shortcut": S})

BACK_TRANSLATION = obj({"text": S})

EXAM_REPORT = obj({
    "summary": S,
    "strengths": arr(obj({"topic": S, "detail": S})),
    "weaknesses": arr(obj({"topic": S, "detail": S, "question_refs": arr(I)})),
    "loopholes": arr(obj({"pattern": S, "detail": S, "question_refs": arr(I)})),
    "shortcuts": arr(obj({"question_ref": I, "technique": S, "explanation": S})),
    "study_plan": arr(PLAN_DAY),
    "next_test": obj({"exam_slug": S, "reason": S}),
    "encouragement": S,
    # One or two sentences on progress since the last attempt ("" on a first attempt). Numbers come from code.
    "since_last_attempt": S,
})

INTERVIEW_NEXT = obj({"question": S, "is_followup": B, "refers_to": S})

INTERVIEW_REPORT = obj({
    "summary": S,
    "scores": arr(obj({"criterion": S, "score": I, "justification": S})),
    "per_question": arr(obj({"turn_ref": I, "good": S, "missing": S, "model_answer": S})),
    "red_flags": arr(S),
    "study_plan": arr(PLAN_DAY),
})

LESSON = obj({"lesson": S})
