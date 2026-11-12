"""Notes Maker AI (feature 10) and Topic Explainer decks (feature 16).

Notes
- Shared master notes per topic, kind and level: written once by Claude Sonnet, then translated once per language.
  A cache hit is free; the student who triggers a new one spends 1 personal-notes allowance.
- Personal notes: GLM-4.6 builds them from the student's own mistakes on that topic (1 personal-notes allowance).

Topic Explainer
- Library decks (pre-made for common syllabus topics, admin-generated) are free for everyone, including Free.
- Custom decks: GPT-5 mini writes the outline, then GLM-4.6 (smart), Claude Sonnet (master) or the Ultra model
  writes the slides. Shared by topic, level, mode and language, so most requests never reach a model.
  Paid with 1 custom-deck allowance (Pro), else 3 Smart credits / 3 Master credits (tutor packs), or 4 Ultra credits.
- Visuals are Mermaid diagrams or tables (code, not images); the first slide gets a personal note from the persona
  through a template, with no AI call.
"""

import json
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.safety import wrap_data
from app.core.errors import AppError, not_found
from app.models import AiArtifact, NotebookEntry, Question, Topic, User
from app.services import allowances
from app.services.ai_features import engine, persona, tutor

S = {"type": "string"}
A = tutor.A
_obj = tutor._obj
VISUAL = tutor.VISUAL
PRACTICE = tutor.PRACTICE

NOTE_KINDS = ("notes", "formula_sheet", "mind_map", "revision_sheet")
LEVELS = ("basic", "exam", "advanced")

NOTES_SCHEMA = _obj({
    "title": S, "summary": S,
    "sections": A(_obj({"heading": S, "bullets": A(S), "visual": VISUAL})),
    "formulas": A(_obj({"name": S, "formula": S, "when_to_use": S})),
    "mind_map_mermaid": S,
    "one_page_revision": A(S),
})
OUTLINE_SCHEMA = _obj({"title": S, "slide_titles": A(S), "key_ideas": A(S), "common_traps": A(S)})
DECK_SCHEMA = _obj({
    "title": S, "why_it_matters": S,
    "slides": A(_obj({"title": S, "points": A(S), "visual": VISUAL})),
    "worked_examples": A(_obj({"level": S, "question": S, "fastest_method": S, "steps": A(S)})),
    "traps": A(_obj({"wrong": S, "right": S, "why": S})),
    "cheat_codes": A(_obj({"code": S, "works_when": S, "fails_when": S})),
    "summary_sheet": A(S),
    "practice_questions": A(PRACTICE),
})

NOTES_SYSTEM = ("You write compact, exam-focused study notes for Indian competitive exams (banking, SSC, railways and "
                "similar). One idea per bullet. Every section gets a visual: a valid Mermaid diagram or a small table "
                "(or type none when a visual would not help). Formulas use plain text math. " + engine.COACH_RULES)
OUTLINE_SYSTEM = ("Plan a 10 to 15 slide teaching deck on one exam topic: why it matters in the exam, the concept "
                  "from zero one idea per slide, worked examples easy to exam level, traps, cheat codes, summary and "
                  "practice. " + engine.COACH_RULES)
DECK_SYSTEM = ("Write the full teaching deck from the outline. 10 to 15 slides, each with 2 to 5 short points and a "
               "visual (valid Mermaid diagram or a table; every slide should have one). Exactly 3 worked examples "
               "(easy, medium, exam), traps shown wrong-versus-right, cheat codes each with 'works when' and "
               "'fails when', a one-page summary sheet and exactly 5 practice questions with 4 options keyed A-D. "
               + engine.COACH_RULES)

DECK_MODES = {"smart": "topic_deck_smart", "master": "topic_deck_master", "ultra": "ultra"}


def _key(*parts) -> str:
    return "|".join(str(p).strip().lower() for p in parts)


def _check(topic: str, kind: str | None = None, level: str = "exam"):
    if not topic or len(topic.strip()) < 3 or len(topic) > 120:
        raise AppError(422, "invalid_topic", "Give a topic name of 3 to 120 characters")
    if kind is not None and kind not in NOTE_KINDS:
        raise AppError(422, "invalid_kind", f"kind must be one of {', '.join(NOTE_KINDS)}")
    if level not in LEVELS:
        raise AppError(422, "invalid_level", "level must be basic, exam or advanced")


def _personal_line(db: Session, user: User, topic: str) -> str:
    weak = persona.compute(db, user)["weak_topics"]
    match = next((t for t in weak if topic.lower() in t["topic"].lower() or t["topic"].lower() in topic.lower()), None)
    if match:
        return f"Your mastery of {match['topic']} is {match['mastery']}/100. This deck focuses on what costs you marks."
    if weak:
        return f"Tip: your weakest topic right now is {weak[0]['topic']}. There is a deck for it too."
    return ""


# ---- notes --------------------------------------------------------------------------------------------------------
def notes(db: Session, user: User, *, topic: str, kind: str = "notes", level: str = "exam", personal: bool = False,
          language: str | None = None) -> dict:
    _check(topic, kind, level)
    language = engine.lang_of(user, language)
    if not allowances.summary(db, user)["limits"]["personal_notes"]["limit"]:
        raise AppError(402, "plan_required", "Notes Maker is part of Starter, Pro and the Topper Combo.")
    ref = uuid.uuid4().hex
    if personal:
        with engine.charge(db, user, "personal_notes", ref_id=ref):
            mistakes = _mistakes_on(db, user, topic)
            out = engine.ask(db, purpose="notes_personal", system=NOTES_SYSTEM, schema=NOTES_SCHEMA, ref_id=ref,
                             language=language,
                             prompt=f"Topic: {topic}\nFormat: {kind}\nLevel: {level}\nBuild the notes around these "
                                    "mistakes the student made (fix each misconception):\n"
                                    + wrap_data("mistakes", json.dumps(mistakes, ensure_ascii=False), 10000)
                                    + "\n" + engine.language_instruction(language))
            art = engine.store(db, "notes", _key(topic, kind, level, "personal", ref), out, language=language,
                               user_id=user.id, model="notes_personal")
            db.commit()
        return engine.artifact_out(art, cached_hit=False)
    key = _key(topic, kind, level)
    hit = engine.cached(db, "master_notes", key, language)
    if hit is not None:
        hit.times_served += 1
        db.commit()
        return engine.artifact_out(hit, cached_hit=True)
    with engine.charge(db, user, "personal_notes", ref_id=ref):
        def make():
            return engine.ask(db, purpose="notes_master", system=NOTES_SYSTEM, schema=NOTES_SCHEMA, ref_id=ref,
                              prompt=f"Topic: {topic}\nFormat: {kind}\nLevel: {level}"), "notes_master"

        art, cached_hit = engine.cached_localized(db, "master_notes", key, language, make, title=topic)
        db.commit()
    return engine.artifact_out(art, cached_hit=cached_hit)


def _mistakes_on(db: Session, user: User, topic: str) -> list[dict]:
    rows = db.execute(select(NotebookEntry, Question, Topic).join(Question, Question.id == NotebookEntry.question_id)
                      .join(Topic, Topic.id == NotebookEntry.topic_id, isouter=True)
                      .where(NotebookEntry.user_id == user.id).order_by(NotebookEntry.times_wrong.desc()).limit(60)).all()
    t = topic.lower()
    out = [{"question": q.text[:600], "student_answer": (e.last_answer or {}).get("value"),
            "correct_answer": (q.correct_answer or {}).get("value"),
            "mistake_type": e.mistake_type or e.auto_mistake_type}
           for e, q, tp in rows if tp is not None and (t in tp.name.lower() or tp.name.lower() in t)]
    return out[:12]


# ---- topic explainer decks ----------------------------------------------------------------------------------------
def library(db: Session, topic: str | None = None, language: str = "en") -> list[dict]:
    q = select(AiArtifact).where(AiArtifact.kind == "topic_deck_library", AiArtifact.user_id.is_(None),
                                 AiArtifact.status != "hidden", AiArtifact.language == language)
    rows = db.scalars(q.order_by(AiArtifact.title)).all()
    if topic:
        rows = [r for r in rows if topic.lower() in r.title.lower()]
    return [{"id": r.id, "title": r.title, "level": r.cache_key.split("|")[-1], "language": r.language} for r in rows]


def _make_deck(db: Session, *, topic: str, level: str, mode: str, exam: str | None, ref) -> tuple[dict, str]:
    outline = engine.ask(db, purpose="topic_deck_outline", system=OUTLINE_SYSTEM, schema=OUTLINE_SCHEMA, ref_id=ref,
                         prompt=f"Topic: {topic}\nLevel: {level}\nExam: {exam or 'Indian banking and SSC exams'}")
    deck = engine.ask(db, purpose=DECK_MODES[mode], system=DECK_SYSTEM, schema=DECK_SCHEMA, ref_id=ref,
                      prompt=f"Topic: {topic}\nLevel: {level}\nExam: {exam or 'Indian banking and SSC exams'}\n"
                             + wrap_data("outline", json.dumps(outline, ensure_ascii=False), 8000))
    return deck, DECK_MODES[mode]


def _pay_for_deck(db: Session, user: User, mode: str, ref) -> str:
    """Pro's custom-deck allowance first, else tutor-pack credits (3 per deck), Ultra decks use 4 Ultra credits."""
    if mode == "ultra":
        allowances.use(db, user, "ultra_credits", ref_id=ref, units=4)
        return "ultra_credits"
    if mode == "smart":
        try:
            allowances.use(db, user, "topic_decks", ref_id=ref)
            return "topic_decks"
        except AppError:
            pass
    feature = "smart_credits" if mode == "smart" else "master_credits"
    allowances.use(db, user, feature, ref_id=ref, units=3)
    return feature


def topic_deck(db: Session, user: User, *, topic: str, level: str = "exam", mode: str = "library",
               exam: str | None = None, language: str | None = None) -> dict:
    _check(topic, level=level)
    language = engine.lang_of(user, language)
    if mode == "library":
        hit = engine.cached(db, "topic_deck_library", _key(topic, level), language) or (
            engine.cached(db, "topic_deck_library", _key(topic, level), "en"))
        if hit is None:
            raise AppError(404, "not_in_library", "This topic is not in the free library yet. Make a custom deck.")
        hit.times_served += 1
        out = engine.artifact_out(hit, cached_hit=True)
        db.commit()
        return out | {"personal_note": _personal_line(db, user, topic)}
    if mode not in DECK_MODES:
        raise AppError(422, "invalid_mode", "mode must be library, smart, master or ultra")
    ref = uuid.uuid4().hex
    try:
        paid_with = _pay_for_deck(db, user, mode, ref)
    except AppError as e:
        raise AppError(402, "allowance_exhausted", "You have no custom decks or tutor credits left. "
                                                   "Upgrade or add a pack to continue.") from e
    try:
        art, hit = engine.cached_localized(
            db, f"topic_deck_{mode}", _key(topic, level, exam or ""), language,
            lambda: _make_deck(db, topic=topic, level=level, mode=mode, exam=exam, ref=ref), title=topic)
        db.commit()
    except Exception:
        db.rollback()
        allowances.refund_use(db, user, paid_with, ref)
        db.commit()
        raise
    return engine.artifact_out(art, cached_hit=hit) | {"paid_with": paid_with,
                                                       "personal_note": _personal_line(db, user, topic)}


def build_library_deck(db: Session, *, topic: str, level: str = "exam", exam: str | None = None) -> dict:
    """Admin: pre-make a free library deck (Smart route; translated per language on first request)."""
    _check(topic, level=level)
    key = _key(topic, level)
    existing = engine.cached(db, "topic_deck_library", key, "en")
    if existing is not None:
        return engine.artifact_out(existing, cached_hit=True)
    deck, model = _make_deck(db, topic=topic, level=level, mode="smart", exam=exam, ref=uuid.uuid4().hex)
    art = engine.store(db, "topic_deck_library", key, deck, title=topic, model=model)
    db.commit()
    return engine.artifact_out(art, cached_hit=False)


def library_deck_in(db: Session, user: User, artifact_id: uuid.UUID, language: str | None) -> dict:
    a = db.get(AiArtifact, artifact_id)
    if a is None or a.kind != "topic_deck_library":
        raise not_found("Deck")
    language = engine.lang_of(user, language)
    if language == a.language:
        return engine.artifact_out(a, cached_hit=True)
    art, hit = engine.cached_localized(db, "topic_deck_library", a.cache_key, language, lambda: (a.payload, a.model),
                                       title=a.title)
    db.commit()
    return engine.artifact_out(art, cached_hit=hit)
