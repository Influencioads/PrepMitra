"""AI Tutor Deep Dive (feature 7) and Ask Mitra Tutor Chat (feature 8).

Deep dives are cached per question, mode and language, so the second student who opens the same question gets it
from the store; the student's credit is still used (they get the full product), but PrepMitra pays nothing.
- smart: GLM-4.6 (1 Smart credit)    - master: Claude Sonnet 5.5 (1 Master credit)    - ultra: Tier 0 (1 Ultra credit)

Ask Mitra remembers the student's persona and last 3 mock summaries, keeps the last 10 turns, answers in the
student's language (Gemini Flash for Indian languages), uses Kimi for story-style replies, and moves to Claude
Sonnet when the student asks to "explain differently" twice in a row.
"""

import json
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.safety import wrap_data
from app.core.errors import AppError, not_found
from app.models import AiArtifact, AiChatMessage, Question, Report, Solution, User
from app.services.ai_features import doubts, engine, persona

S = {"type": "string"}
A = lambda items: {"type": "array", "items": items}  # noqa: E731


def _obj(props: dict) -> dict:
    return {"type": "object", "additionalProperties": False, "required": list(props), "properties": props}


OPTION = _obj({"key": S, "text": S})
PRACTICE = _obj({"level": {"type": "string", "enum": ["easy", "medium", "exam_hard"]}, "text": S, "options": A(OPTION),
                 "answer": S, "explanation": S})
VISUAL = _obj({"type": {"type": "string", "enum": ["mermaid", "table", "none"]}, "mermaid": S, "table": A(A(S)),
               "caption": S})
DEEP_DIVE_SCHEMA = _obj({
    "title": S, "visual_note": VISUAL, "concept_from_zero": A(S), "the_trap": S, "why_students_get_it_wrong": S,
    "never_again_checklist": A(S), "worked_solution": A(S), "shortcut": S, "practice_questions": A(PRACTICE),
})
CHAT_SCHEMA = _obj({"reply": S, "follow_ups": A(S), "on_topic": {"type": "boolean"}, "distress": {"type": "boolean"}})

DEEP_DIVE_SYSTEM = ("You are PrepMitra's AI Tutor for Indian competitive exams. Build a deep dive on one tough "
                    "question: a one-page visual note (a Mermaid flowchart or a small table, valid syntax), the "
                    "concept explained from first principles one idea per line, the trap that causes the mistake, "
                    "why students get it wrong, a 'never again' checklist, the worked solution, the fastest shortcut, "
                    "and exactly 3 practice questions from easy to exam-hard with 4 options keyed A-D. "
                    + engine.COACH_RULES)
CHAT_SYSTEM = ("You are Mitra, a friendly AI tutor in the PrepMitra exam-prep app. You know the student's learning "
               "profile and recent mocks (given as data). Teach step by step, check understanding with a question, "
               "keep replies under 180 words unless asked for more. Set on_topic false (and reply with a polite "
               "redirect) for requests unrelated to exam preparation. Set distress true if the student sounds "
               "hopeless or mentions self-harm. " + engine.COACH_RULES)
STORY_STYLE = "Answer as a short story or memory trick from everyday Indian life that makes the idea stick."

MODES = {"smart": ("tutor_smart", "smart_credits"), "master": ("tutor_master", "master_credits"),
         "ultra": ("ultra", "ultra_credits")}


def _question_source(db: Session, user: User, question_id, solution_id, text, options) -> tuple[str, list, str, str]:
    """Returns (normalised text, options, correct answer or "", cache key)."""
    if question_id:
        q = db.get(Question, question_id)
        if q is None or q.status != "verified":
            raise not_found("Question")
        opts = [{"key": o["key"], "text": o["text"]} for o in q.options or []]
        ans = q.correct_answer.get("value") if isinstance(q.correct_answer, dict) else ""
        ans = ",".join(ans) if isinstance(ans, list) else str(ans or "")
        return q.text, opts, ans, f"q:{q.id}"
    if solution_id:
        s = db.get(Solution, solution_id)
        if s is None or s.status != "live":
            raise not_found("Solution")
        return s.normalized_text, s.options, s.answer, f"s:{s.fingerprint}"
    if not text or len(text.strip()) < 8:
        raise AppError(422, "question_required", "Send question_id, solution_id or the question text")
    nt, no = doubts.normalize(text), doubts.norm_options(options)
    return nt, no, "", f"t:{doubts.fingerprint(nt, no)}"


def deep_dive(db: Session, user: User, *, mode: str, question_id=None, solution_id=None, text=None, options=None,
              chosen: str | None = None, language: str | None = None) -> dict:
    if mode not in MODES:
        raise AppError(422, "invalid_mode", "mode must be smart, master or ultra")
    if engine.distress(text):
        return {"support": engine.TELE_MANAS}
    route, feature = MODES[mode]
    language = engine.lang_of(user, language)
    qtext, qopts, answer, key = _question_source(db, user, question_id, solution_id, text, options)
    ref = uuid.uuid4().hex
    with engine.charge(db, user, feature, ref_id=ref):
        def make():
            prompt = wrap_data("question", qtext + ("\nOptions:\n" + "\n".join(
                f"{o['key']}. {o['text']}" for o in qopts) if qopts else ""), 4000)
            if answer:
                prompt += f"\nVerified correct answer: {answer}. Teach towards this answer."
            out = engine.ask(db, purpose=route, system=DEEP_DIVE_SYSTEM, schema=DEEP_DIVE_SCHEMA, prompt=prompt,
                             ref_id=ref, context={"question": {"text": qtext, "options": qopts}})
            return out, route

        art, hit = engine.cached_localized(db, f"deep_dive_{mode}", key, language, make,
                                           title=f"Deep dive ({mode})")
        engine.store(db, "deep_dive_saved", str(art.id), {"artifact_id": str(art.id), "mode": mode},
                     user_id=user.id, title=art.title, language=language)
        db.commit()
    out = engine.artifact_out(art, cached_hit=hit) | {"mode": mode, "credit_used": feature}
    if chosen and answer:
        out["personal_note"] = (f"You chose {chosen.upper()}; the answer is {answer}. "
                                f"The trap: {art.payload.get('the_trap', '')}").strip()
    return out


def my_deep_dives(db: Session, user: User, limit: int = 50) -> list[dict]:
    refs = db.scalars(select(AiArtifact).where(AiArtifact.user_id == user.id, AiArtifact.kind == "deep_dive_saved")
                      .order_by(AiArtifact.created_at.desc()).limit(limit)).all()
    out = []
    for r in refs:
        a = db.get(AiArtifact, uuid.UUID(r.payload["artifact_id"]))
        if a is not None and a.status != "hidden":
            out.append({"id": a.id, "mode": r.payload.get("mode"), "title": a.title, "language": a.language,
                        "saved_at": r.created_at})
    return out


# ---- Ask Mitra -----------------------------------------------------------------------------------------------------
def _context(db: Session, user: User) -> dict:
    p = persona.snapshot(db, user)
    reports = db.scalars(select(Report).where(Report.user_id == user.id, Report.kind == "exam",
                                              Report.status == "ready")
                         .order_by(Report.created_at.desc()).limit(3)).all()
    return {
        "persona": {k: p.get(k) for k in ("weak_topics", "strong_topics", "error_mix_percent", "speed_profile",
                                          "consistency_score")} | {"style": (p.get("ai") or {}).get("learning_style")},
        "last_mocks": [{"score": (r.analytics or {}).get("score"), "max": (r.analytics or {}).get("max_score"),
                        "summary": (r.report or {}).get("summary", "")[:400]} for r in reports],
    }


def chat(db: Session, user: User, *, message: str, session_id: str | None = None, style: str = "normal",
         explain_differently: bool = False, language: str | None = None) -> dict:
    message = (message or "").strip()
    if not message:
        raise AppError(422, "empty_message", "Type a message")
    language = engine.lang_of(user, language)
    session_id = session_id or uuid.uuid4().hex
    history = db.scalars(select(AiChatMessage).where(AiChatMessage.user_id == user.id, AiChatMessage.thread == "tutor",
                                                     AiChatMessage.session_id == session_id)
                         .order_by(AiChatMessage.id.desc()).limit(10)).all()[::-1]
    if engine.distress(message):
        db.add(AiChatMessage(user_id=user.id, thread="tutor", session_id=session_id, role="user", content=message))
        db.add(AiChatMessage(user_id=user.id, thread="tutor", session_id=session_id, role="assistant",
                             content=engine.TELE_MANAS, meta={"support": True}))
        db.commit()
        return {"session_id": session_id, "reply": engine.TELE_MANAS, "follow_ups": [], "support": True}
    prev_differently = any(m.meta.get("explain_differently") for m in history[-2:] if m.role == "user")
    premium = explain_differently and prev_differently
    ref = uuid.uuid4().hex
    with engine.charge(db, user, "tutor_chat_turns", ref_id=ref):
        convo = "\n".join(f"{m.role}: {m.content[:1500]}" for m in history)
        prompt = (wrap_data("student_profile", json.dumps(_context(db, user), default=str), 6000) + "\n"
                  + wrap_data("conversation_so_far", convo, 12000) + "\n" + wrap_data("student_message", message, 4000)
                  + "\n" + engine.language_instruction(language)
                  + ("\n" + STORY_STYLE if style == "story" else "")
                  + ("\nThe student asked you to explain differently: use a completely new approach." if
                     explain_differently else ""))
        out = engine.ask(db, purpose="tutor_chat_story" if style == "story" else "tutor_chat", system=CHAT_SYSTEM,
                         schema=CHAT_SCHEMA, prompt=prompt, ref_id=ref, premium=premium, language=language)
        reply = out.get("reply", "")
        if out.get("distress"):
            reply = engine.TELE_MANAS + "\n\n" + reply
        db.add(AiChatMessage(user_id=user.id, thread="tutor", session_id=session_id, role="user", content=message,
                             meta={"explain_differently": explain_differently, "style": style}))
        db.add(AiChatMessage(user_id=user.id, thread="tutor", session_id=session_id, role="assistant", content=reply,
                             meta={"premium": premium, "on_topic": out.get("on_topic", True)}))
        db.commit()
    return {"session_id": session_id, "reply": reply, "follow_ups": out.get("follow_ups", [])[:3],
            "premium_used": premium, "language": language}


def chat_history(db: Session, user: User, session_id: str | None, limit: int = 50) -> list[dict]:
    q = select(AiChatMessage).where(AiChatMessage.user_id == user.id, AiChatMessage.thread == "tutor")
    if session_id:
        q = q.where(AiChatMessage.session_id == session_id)
    rows = db.scalars(q.order_by(AiChatMessage.id.desc()).limit(limit)).all()[::-1]
    return [{"id": m.id, "session_id": m.session_id, "role": m.role, "content": m.content, "created_at": m.created_at}
            for m in rows]
