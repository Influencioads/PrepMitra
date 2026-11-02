"""AI question generation pipeline (PDF 6.1).

blueprint -> generate (strict JSON, lessons injected) -> structural checks -> Python numeric check ->
independent second solve (answers must match) -> duplicate / known-bad check (embeddings) -> tag ->
translate + back-translate -> store as "verified". Every outcome, including discarded questions, is logged.
"""

import logging
import random
import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai import prompts, schemas
from app.ai.embeddings import cosine, embed
from app.ai.provider import AIError, get_provider
from app.ai.safety import safe_eval
from app.config import get_settings
from app.models import Exam, Glossary, Question, QuestionGenerationLog, QuestionTranslation, Topic
from app.services import memory

log = logging.getLogger(__name__)
_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def _normalize_answer(qtype: str, raw: str) -> str | None:
    raw = (raw or "").strip().upper()
    if not raw or raw == "AMBIGUOUS":
        return None
    if qtype == "single":
        return raw[:1] if raw[:1] in "ABCD" and len(raw.replace(".", "")) == 1 else None
    if qtype == "multi":
        keys = sorted({k.strip() for k in raw.replace(" ", "").split(",") if k.strip()})
        return ",".join(keys) if keys and all(k in "ABCD" and len(k) == 1 for k in keys) else None
    try:
        return repr(round(float(raw.replace(",", "")), 6))
    except ValueError:
        return None


def correct_answer_value(qtype: str, normalized: str):
    if qtype == "single":
        return normalized
    if qtype == "multi":
        return normalized.split(",")
    return float(normalized)


def _structure_errors(q: dict, qtype: str) -> list[str]:
    errs = []
    if len(q.get("text", "").strip()) < 10:
        errs.append("question text too short")
    opts = q.get("options") or []
    if qtype in ("single", "multi"):
        keys = [o.get("key") for o in opts]
        if keys != ["A", "B", "C", "D"]:
            errs.append("MCQ must have options A-D in order")
        texts = [o.get("text", "").strip().lower() for o in opts]
        if len(set(texts)) != len(texts) or not all(texts):
            errs.append("options must be non-empty and distinct")
    elif opts:
        errs.append("numeric questions must not have options")
    if _normalize_answer(qtype, q.get("answer", "")) is None:
        errs.append(f"answer '{q.get('answer')}' is not valid for type {qtype}")
    if not q.get("explanation", "").strip():
        errs.append("explanation missing")
    return errs


def _numeric_check(q: dict, qtype: str, normalized: str) -> str | None:
    """Runs the model's arithmetic in Python. Returns an error message, or None when consistent/not applicable."""
    expr = (q.get("numeric_check") or "").strip()
    if not expr:
        return None
    try:
        value = safe_eval(expr)
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
        return f"numeric_check '{expr}' could not be evaluated"
    tol = max(1e-6, abs(value) * 1e-4)
    if qtype == "numeric":
        return None if abs(float(normalized) - value) <= max(tol, 0.01) else f"answer {normalized} != computed {value}"
    if qtype == "single":
        opt = next((o for o in q["options"] if o["key"] == normalized), None)
        nums = _NUM.findall(opt["text"].replace(",", "")) if opt else []
        if len(nums) == 1 and abs(float(nums[0]) - value) > max(tol, 0.01):
            return f"correct option value {nums[0]} != computed {value}"
    return None


def _log(db: Session, exam_id, topic_id, outcome: str, reason: str = "", payload: dict | None = None, question_id=None):
    db.add(QuestionGenerationLog(exam_id=exam_id, topic_id=topic_id, outcome=outcome, reason=reason[:2000],
                                 payload=payload or {}, question_id=question_id))


def generate_question(db: Session, *, exam: Exam, topic: Topic, section_name: str, difficulty: str, qtype: str,
                      languages: list[str] | None = None, seed: int | None = None) -> Question | None:
    """Runs the full pipeline once. Returns the stored verified question, or None if it was discarded."""
    s = get_settings()
    provider = get_provider()
    seed = seed if seed is not None else random.randrange(1 << 30)
    lessons = memory.lessons_for(db, exam_id=exam.id, topic_id=topic.id, language="en",
                                 query=f"{topic.name} {difficulty} {qtype}")
    recent = db.scalars(select(Question.text).where(Question.topic_id == topic.id)
                        .order_by(Question.created_at.desc()).limit(5)).all()
    try:
        q = provider.generate_json(
            purpose="question_generate", system=prompts.QUESTION_SYSTEM, schema=schemas.QUESTION, tier="strong",
            prompt=prompts.question_prompt(exam_name=exam.name, section=section_name, topic=topic.name,
                                           difficulty=difficulty, qtype=qtype, language="en", lessons=lessons,
                                           avoid=list(recent)),
            context={"seed": seed, "qtype": qtype, "topic": topic.name, "difficulty": difficulty}, ref_id=exam.id, db=db,
        )
    except AIError as e:
        _log(db, exam.id, topic.id, "error", f"generate: {e}")
        db.commit()
        return None

    errs = _structure_errors(q, qtype)
    if errs:
        _log(db, exam.id, topic.id, "rejected_invalid", "; ".join(errs), q)
        db.commit()
        return None
    answer = _normalize_answer(qtype, q["answer"])

    problem = _numeric_check(q, qtype, answer)
    if problem:
        _log(db, exam.id, topic.id, "rejected_numeric_check", problem, q)
        db.commit()
        return None

    try:
        solved = provider.generate_json(
            purpose="question_verify", system=prompts.VERIFY_SYSTEM, schema=schemas.VERIFY, tier="strong",
            prompt=prompts.verify_prompt(q, qtype), context={"question": {"text": q["text"], "options": q["options"]}},
            ref_id=exam.id, db=db,
        )
    except AIError as e:
        _log(db, exam.id, topic.id, "error", f"verify: {e}", q)
        db.commit()
        return None
    if _normalize_answer(qtype, solved.get("answer", "")) != answer:
        _log(db, exam.id, topic.id, "rejected_verification",
             f"generator answered {answer}, independent solve answered {solved.get('answer')}", q)
        db.commit()
        return None

    full_text = q["text"] + " " + " ".join(o["text"] for o in q.get("options", []))
    vector = embed(full_text)
    near, sim = memory.most_similar_question(db, exam.id, vector)
    if near is not None and sim >= s.dedup_similarity_threshold:
        kind = "known-bad" if near.status in ("rejected", "quarantined") else "existing"
        _log(db, exam.id, topic.id, "rejected_duplicate", f"{sim:.3f} similar to {kind} question {near.id}", q)
        db.commit()
        return None

    question = Question(
        exam_id=exam.id, topic_id=topic.id, subtopic=(q.get("subtopic") or "")[:160] or None, type=qtype,
        difficulty=difficulty, status="verified", text=q["text"], options=q.get("options", []),
        correct_answer={"value": correct_answer_value(qtype, answer)}, explanation=q["explanation"],
        shortcut=q.get("shortcut", ""), expected_time_sec=max(15, min(int(q.get("expected_time_sec") or 60), 600)),
        source="ai", verified_by="ai:dual-solve" + ("+python" if q.get("numeric_check") else ""),
        embedding=vector, sampled_for_review=random.random() < s.review_sample_rate,
        generation_meta={"model_difficulty": q.get("difficulty"), "lessons_used": len(lessons), "seed": seed,
                         "provider": provider.name},
    )
    db.add(question)
    db.flush()
    _log(db, exam.id, topic.id, "verified", "", {}, question.id)
    for lang in languages or []:
        if lang != "en":
            translate_question(db, question, lang)
    db.commit()
    return question


def glossary_for(db: Session, language: str, text: str) -> dict[str, str]:
    low = text.lower()
    rows = db.scalars(select(Glossary).where(Glossary.language == language)).all()
    return {g.term: g.approved_translation for g in rows if g.term.lower() in low}


def translate_question(db: Session, question: Question, language: str) -> QuestionTranslation | None:
    """Translate with the approved glossary, then back-translate to English and compare meaning (PDF 6.1 step 6)."""
    existing = db.scalar(select(QuestionTranslation).where(
        QuestionTranslation.question_id == question.id, QuestionTranslation.language == language))
    if existing is not None:
        return existing
    provider = get_provider()
    src = {"text": question.text, "options": question.options, "explanation": question.explanation,
           "shortcut": question.shortcut}
    glossary = glossary_for(db, language, question.text + " " + question.explanation)
    try:
        t = provider.generate_json(
            purpose="translate", system=prompts.TRANSLATE_SYSTEM, schema=schemas.TRANSLATION, tier="strong",
            prompt=prompts.translate_prompt(src, language, glossary), context={"question": src, "language": language},
            ref_id=question.id, db=db,
        )
        if [o["key"] for o in t.get("options", [])] != [o["key"] for o in question.options]:
            raise AIError("translated options do not match the original keys")
        back = provider.generate_json(
            purpose="back_translate", system=prompts.BACK_TRANSLATE_SYSTEM, schema=schemas.BACK_TRANSLATION,
            tier="fast", prompt=prompts.back_translate_prompt(t["text"]), context={"text": t["text"]},
            ref_id=question.id, db=db,
        )
    except AIError as e:
        log.warning("translation of %s to %s failed: %s", question.id, language, e)
        return None
    sim = cosine(embed(back["text"]), embed(question.text))
    status = "back_translation_ok" if sim >= get_settings().back_translation_min_similarity else "rejected"
    row = QuestionTranslation(question_id=question.id, language=language, text=t["text"], options=t["options"],
                              explanation=t.get("explanation", ""), shortcut=t.get("shortcut", ""),
                              review_status=status)
    db.add(row)
    db.flush()
    return row
