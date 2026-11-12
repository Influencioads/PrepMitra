"""Student AI features from the Nov 2026 blueprint. Every call spends the matching allowance from
GET /v1/me/allowances (refunded automatically if the AI fails) and is routed to its model in app/ai/catalog.py.

Errors: 402 allowance_exhausted / plan_required, 422 off_topic, 503 ai_unavailable (retry later; nothing spent).
"""

import uuid
from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.deps import get_current_user, require_admin
from app.core.errors import AppError, not_found
from app.core.ratelimit import hit
from app.db import get_db
from app.models import AiArtifact, Solution, User
from app.services import allowances, pdf
from app.services.ai_features import coaching, content, doubts, engine, persona, tutor

router = APIRouter(prefix="/ai", tags=["AI features"])
admin_router = APIRouter(prefix="/admin/ai", tags=["admin: AI features"])
product = require_admin("product")


def _limit(user: User, per_minute: int = 20) -> None:
    """Per-student, per-endpoint limit (stops abuse early; allowances cap the month)."""
    import inspect

    hit(f"ai:{inspect.stack()[1].function}:{user.id}", per_minute, 60)


class OptionIn(BaseModel):
    key: str = Field(max_length=3)
    text: str = Field(max_length=500)


class DoubtIn(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    options: list[OptionIn] = Field(default_factory=list, max_length=6)
    chosen: str | None = Field(default=None, max_length=3, description="The option the student picked, if any")
    language: str | None = None
    escalate: bool = Field(default=False, description="Ask for the premium model (uses premium allowance)")


class PhotoIn(BaseModel):
    image: str = Field(description="data:image/jpeg;base64,... or an https URL")
    chosen: str | None = Field(default=None, max_length=3)
    language: str | None = None


class LangIn(BaseModel):
    language: str | None = None


class FeedbackIn(BaseModel):
    helpful: bool | None = None
    report_error: bool = False


class DeepDiveIn(BaseModel):
    mode: Literal["smart", "master", "ultra"] = "smart"
    question_id: uuid.UUID | None = None
    solution_id: uuid.UUID | None = None
    text: str | None = Field(default=None, max_length=4000)
    options: list[OptionIn] = Field(default_factory=list, max_length=6)
    chosen: str | None = Field(default=None, max_length=3)
    language: str | None = None


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: str | None = Field(default=None, max_length=64)
    style: Literal["normal", "story"] = "normal"
    explain_differently: bool = False
    language: str | None = None


class NotesIn(BaseModel):
    topic: str = Field(min_length=3, max_length=120)
    kind: Literal["notes", "formula_sheet", "mind_map", "revision_sheet"] = "notes"
    level: Literal["basic", "exam", "advanced"] = "exam"
    personal: bool = Field(default=False, description="Build from my own mistakes instead of the shared notes")
    language: str | None = None


class DeckIn(BaseModel):
    topic: str = Field(min_length=3, max_length=120)
    level: Literal["basic", "exam", "advanced"] = "exam"
    mode: Literal["library", "smart", "master", "ultra"] = "library"
    exam: str | None = Field(default=None, max_length=120)
    language: str | None = None


class RevisionIn(BaseModel):
    language: str | None = None
    count: int = Field(default=10, ge=1, le=20)


class WritingIn(BaseModel):
    task_type: Literal["essay", "formal_letter", "informal_letter", "precis", "report", "paragraph"]
    question: str = Field(min_length=5, max_length=3000)
    answer: str = Field(min_length=1, max_length=16000)
    word_limit: int | None = Field(default=None, ge=50, le=2000)
    topper_rewrite: bool = Field(default=False, description="Also rewrite it as a topper would (1 Master credit)")
    language: str | None = None


class CoachStartIn(BaseModel):
    topic_id: int
    language: str | None = None


class CoachReplyIn(BaseModel):
    message: str = Field(min_length=1, max_length=1500)


class CoachTestIn(BaseModel):
    rule: str | None = Field(default=None, max_length=1000)


class CoachLockIn(BaseModel):
    share: bool = Field(default=False, description="Let this card join the shared shortcut library if it tests well")


# ---- doubts -------------------------------------------------------------------------------------------------------
@router.post("/doubts")
def solve_doubt(body: DoubtIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Doubt Solver: solution store first (no AI on a match), then a verified AI solve. 1 doubt."""
    _limit(user)
    return doubts.solve(db, user, text=body.text, options=[o.model_dump() for o in body.options], chosen=body.chosen,
                        language=body.language, escalate=body.escalate)


@router.post("/doubts/photo")
def photo_doubt(body: PhotoIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Photo Doubt: a vision model reads the question, then the Doubt Solver pipeline. 1 photo doubt."""
    _limit(user, 10)
    return doubts.photo(db, user, image=body.image, chosen=body.chosen, language=body.language)


@router.post("/doubts/{solution_id}/explain-again")
def explain_again(solution_id: uuid.UUID, body: LangIn, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    """'Still confused': a different explanation, on the premium model while premium allowance lasts. 1 doubt."""
    _limit(user)
    return doubts.explain_again(db, user, solution_id, body.language)


@router.post("/doubts/{solution_id}/feedback")
def doubt_feedback(solution_id: uuid.UUID, body: FeedbackIn, user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    """Thumbs up/down and 'Report an error'. 2 error reports hide the stored answer until a human checks it."""
    hit(f"ai-fb:{user.id}:{solution_id}", 3, 3600)
    return doubts.feedback(db, user, solution_id, helpful=body.helpful, report_error=body.report_error)


# ---- tutor --------------------------------------------------------------------------------------------------------
@router.post("/tutor/deep-dives")
def deep_dive(body: DeepDiveIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """AI Tutor Deep Dive: smart (1 Smart credit), master (1 Master credit) or ultra (1 Ultra credit)."""
    _limit(user, 10)
    return tutor.deep_dive(db, user, mode=body.mode, question_id=body.question_id, solution_id=body.solution_id,
                           text=body.text, options=[o.model_dump() for o in body.options], chosen=body.chosen,
                           language=body.language)


@router.get("/tutor/deep-dives")
def my_deep_dives(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"items": tutor.my_deep_dives(db, user)}


@router.post("/tutor/chat")
def tutor_chat(body: ChatIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Ask Mitra: tutor chat that knows the student's persona and recent mocks. 1 tutor chat turn."""
    _limit(user, 20)
    return tutor.chat(db, user, message=body.message, session_id=body.session_id, style=body.style,
                      explain_differently=body.explain_differently, language=body.language)


@router.get("/tutor/chat")
def tutor_chat_history(session_id: str | None = None, user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    return {"items": tutor.chat_history(db, user, session_id)}


# ---- persona, rank, mistakes --------------------------------------------------------------------------------------
@router.get("/persona")
def get_persona(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Persona snapshot (everyone): topic mastery 0-100, error-type mix, speed profile, consistency."""
    return persona.snapshot(db, user)


@router.post("/persona/deep")
def deep_persona(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Monthly deep persona (Pro). Returns the existing one if made in the last 28 days."""
    _limit(user, 3)
    return persona.deep(db, user)


@router.post("/persona/ultra-review")
def ultra_review(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Final-30-days strategy review on the Ultra model (1 Ultra credit)."""
    _limit(user, 3)
    return persona.deep(db, user, ultra=True)


@router.get("/rank")
def rank(exam_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Rank & Cutoff Predictor (Pro): rank band among PrepMitra test-takers and the gap to last year's cutoff."""
    _limit(user, 10)
    return persona.rank(db, user, exam_id)


@router.get("/mistakes/summary")
def mistakes_summary(language: str | None = None, user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    """Weekly Mistake Notebook summary, grouped by error type (cached for the week)."""
    return persona.mistake_summary(db, user, language)


# ---- notes and topic decks ----------------------------------------------------------------------------------------
@router.post("/notes")
def make_notes(body: NotesIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Notes Maker: shared master notes (free when already made) or personal notes from your mistakes."""
    _limit(user, 10)
    return content.notes(db, user, topic=body.topic, kind=body.kind, level=body.level, personal=body.personal,
                         language=body.language)


@router.get("/topic-decks/library")
def deck_library(topic: str | None = None, language: str = "en", user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    """Free pre-made Topic Explainer decks (all plans, including Free)."""
    return {"items": content.library(db, topic, language)}


@router.get("/topic-decks/library/{deck_id}")
def library_deck(deck_id: uuid.UUID, language: str | None = None, user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    return content.library_deck_in(db, user, deck_id, language)


@router.post("/topic-decks")
def topic_deck(body: DeckIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Topic Explainer: library (free) or a custom 10-15 slide deck (Pro allowance, or 3 tutor credits; Ultra 4)."""
    _limit(user, 5)
    return content.topic_deck(db, user, topic=body.topic, level=body.level, mode=body.mode, exam=body.exam,
                              language=body.language)


def _readable(db: Session, user: User, artifact_id: uuid.UUID) -> AiArtifact:
    a = db.get(AiArtifact, artifact_id)
    if a is None or a.status == "hidden" or (a.user_id is not None and a.user_id != user.id and a.status != "shared"):
        raise not_found("Item")
    if a.kind.startswith("deep_dive_") and a.user_id is None:
        owned = db.scalar(select(AiArtifact.id).where(AiArtifact.user_id == user.id,
                                                      AiArtifact.kind == "deep_dive_saved",
                                                      AiArtifact.cache_key == str(a.id)).limit(1))
        if owned is None:
            raise not_found("Item")
    return a


@router.get("/artifacts/{artifact_id}")
def get_artifact(artifact_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return engine.artifact_out(_readable(db, user, artifact_id))


@router.get("/artifacts/{artifact_id}/pdf")
def artifact_pdf(artifact_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Notes, decks, deep dives and summaries as PDF. The visual mistake-notebook PDF is an AI Tutor Pro feature."""
    a = _readable(db, user, artifact_id)
    if a.kind == "mistake_summary":
        engine.require_flag(db, user, "mistake_notebook_visual", "AI Tutor Pro and the Topper Combo")
    data = pdf.study_material_pdf(app_name=get_settings().app_name, title=a.title or a.kind, language=a.language,
                                  payload=a.payload)
    return Response(data, media_type="application/pdf",
                    headers={"Content-Disposition": f'inline; filename="{a.kind}-{str(a.id)[:8]}.pdf"'})


# ---- revision, current affairs, writing ---------------------------------------------------------------------------
@router.post("/revision/today")
def revision_today(body: RevisionIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Revision AI: today's spaced-repetition quiz from your mistakes, with AI hints, plus your flashcards."""
    _limit(user, 10)
    return coaching.revision_today(db, user, body.language, body.count)


@router.get("/current-affairs")
def current_affairs(day: date | None = Query(default=None, alias="date"), language: str | None = None,
                    user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Daily current-affairs digest and 10-question GA quiz (Pro), fact-checked by a second model."""
    _limit(user, 10)
    return coaching.current_affairs(db, user, day, language)


@router.post("/writing/evaluate")
def evaluate_writing(body: WritingIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Descriptive Writing Evaluator (Pro: 4 a month): rubric scores, corrections and a model answer."""
    _limit(user, 5)
    return coaching.evaluate_writing(db, user, task_type=body.task_type, question=body.question, answer=body.answer,
                                     word_limit=body.word_limit, topper_rewrite=body.topper_rewrite,
                                     language=body.language)


# ---- cheat code coach ---------------------------------------------------------------------------------------------
@router.post("/coach/sessions")
def coach_start(body: CoachStartIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Cheat Code Coach, step 1 (Spot): 3 solved questions of one type. Uses 1 coach session."""
    _limit(user, 5)
    return coaching.coach_start(db, user, topic_id=body.topic_id, language=body.language)


@router.post("/coach/sessions/{session_id}/reply")
def coach_reply(session_id: str, body: CoachReplyIn, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """Step 2 (Shape): the student writes the rule; the coach asks until it is exact (up to 6 turns)."""
    _limit(user)
    return coaching.coach_reply(db, user, session_id, body.message)


@router.post("/coach/sessions/{session_id}/test")
def coach_test(session_id: str, body: CoachTestIn, user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    """Step 3 (Test): the rule is run on 5 bank questions; shows where it works and where it breaks."""
    _limit(user, 10)
    return coaching.coach_test(db, user, session_id, body.rule)


@router.post("/coach/sessions/{session_id}/lock")
def coach_lock(session_id: str, body: CoachLockIn, user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    """Step 4 (Lock): the rule becomes a revision card in your language; it then appears in Revision AI."""
    _limit(user, 10)
    return coaching.coach_lock(db, user, session_id, body.share)


@router.get("/coach/cards")
def my_cards(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"items": coaching.my_cards(db, user)}


@router.get("/shortcuts")
def shortcuts(topic: str | None = None, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Shared shortcut library (open to everyone)."""
    return {"items": coaching.shortcut_library(db, topic)}


# ---- admin --------------------------------------------------------------------------------------------------------
class SolutionReviewIn(BaseModel):
    action: Literal["approve", "hide"]
    answer: str | None = Field(default=None, max_length=500)


class LibraryDeckIn(BaseModel):
    topic: str = Field(min_length=3, max_length=120)
    level: Literal["basic", "exam", "advanced"] = "exam"
    exam: str | None = None


class CurrentAffairsRunIn(BaseModel):
    day: date | None = Field(default=None, alias="date")


@admin_router.get("/solutions")
def admin_solutions(status: Literal["live", "hidden", "disputed"] = "disputed", limit: int = Query(50, le=200),
                    admin: User = Depends(product), db: Session = Depends(get_db)):
    """Solution store review queue: disputed (AI checks disagreed) and hidden (error flags / thumbs-down)."""
    rows = db.scalars(select(Solution).where(Solution.status == status)
                      .order_by(Solution.error_flags.desc(), Solution.updated_at.desc()).limit(limit)).all()
    return {"items": [doubts.solution_out(s) for s in rows]}


@admin_router.patch("/solutions/{solution_id}")
def admin_review_solution(solution_id: uuid.UUID, body: SolutionReviewIn, admin: User = Depends(product),
                          db: Session = Depends(get_db)):
    return doubts.admin_review(db, solution_id, body.action, body.answer)


@admin_router.post("/library/decks")
def admin_library_deck(body: LibraryDeckIn, admin: User = Depends(product), db: Session = Depends(get_db)):
    """Pre-make a free library Topic Explainer deck (served to every student, including Free)."""
    return content.build_library_deck(db, topic=body.topic, level=body.level, exam=body.exam)


@admin_router.post("/current-affairs/run")
def admin_current_affairs(body: CurrentAffairsRunIn, admin: User = Depends(product), db: Session = Depends(get_db)):
    art = coaching.generate_current_affairs(db, body.day)
    return engine.artifact_out(art)
