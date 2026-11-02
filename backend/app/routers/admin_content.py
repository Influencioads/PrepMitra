"""Admin: exams, blueprints, topics, papers, question bank, review queue, AI lessons, glossary, interview roles.

Roles (PDF 12): content_manager, subject_expert, language_reviewer, support, finance, product, founder (all).
"""

import random
import uuid
from typing import Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.ai.embeddings import embed
from app.core.audit import audit
from app.core.deps import require_admin
from app.core.errors import AppError, not_found
from app.core.languages import is_supported
from app.db import get_db
from app.models import (
    AiLesson,
    Exam,
    ExamBlueprint,
    Glossary,
    InterviewRole,
    Paper,
    Question,
    QuestionGenerationLog,
    QuestionReport,
    QuestionTranslation,
    Topic,
    User,
)
from app.services import blueprints as bp
from app.services import catalog, papers, questions
from app.services.question_pipeline import generate_question, translate_question

router = APIRouter(prefix="/admin", tags=["admin: content"])
content = require_admin("content_manager")
expert = require_admin("subject_expert", "language_reviewer", "content_manager")


# ---- exams --------------------------------------------------------------------------------------------------------
class ExamIn(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9-]{2,80}$")
    name: str = Field(min_length=2, max_length=160)
    category: str
    description: str = ""
    credits_required: int = Field(default=1, ge=0, le=10)
    is_free_trial: bool = False


class ExamPatch(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    category: str | None = None
    description: str | None = None
    credits_required: int | None = Field(default=None, ge=0, le=10)
    is_free_trial: bool | None = None


def _exam_out(e: Exam) -> dict:
    return {"id": e.id, "slug": e.slug, "name": e.name, "category": e.category, "description": e.description,
            "status": e.status, "credits_required": e.credits_required, "is_free_trial": e.is_free_trial,
            "current_blueprint_version": e.current_blueprint_version, "updated_at": e.updated_at}


def _exam(db: Session, exam_id) -> Exam:
    e = db.get(Exam, exam_id)
    if e is None:
        raise not_found("Exam")
    return e


@router.get("/exams")
def list_exams(status: str | None = None, q: str | None = None, admin: User = Depends(content), db: Session = Depends(get_db)):
    stmt = select(Exam)
    if status:
        stmt = stmt.where(Exam.status == status)
    if q:
        stmt = stmt.where(Exam.name.ilike(f"%{q}%"))
    return {"items": [_exam_out(e) for e in db.scalars(stmt.order_by(Exam.name))]}


@router.post("/exams", status_code=201)
def create_exam(body: ExamIn, admin: User = Depends(content), db: Session = Depends(get_db)):
    if body.category not in catalog.CATEGORIES:
        raise AppError(422, "invalid_category", f"category must be one of {list(catalog.CATEGORIES)}")
    e = Exam(**body.model_dump(), status="draft")
    db.add(e)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "slug_taken", "An exam with this slug already exists")
    audit(db, admin, "exam.create", "exam", e.id, slug=e.slug)
    db.commit()
    return _exam_out(e)


@router.get("/exams/{exam_id}")
def get_exam(exam_id: uuid.UUID, admin: User = Depends(content), db: Session = Depends(get_db)):
    e = _exam(db, exam_id)
    versions = db.scalars(select(ExamBlueprint).where(ExamBlueprint.exam_id == e.id).order_by(ExamBlueprint.version)).all()
    counts = dict(db.execute(select(Question.status, func.count()).where(Question.exam_id == e.id)
                             .group_by(Question.status)).all())
    ready = db.scalar(select(func.count()).select_from(Paper).where(Paper.exam_id == e.id, Paper.status == "ready"))
    return _exam_out(e) | {"blueprints": [_bp_out(b) for b in versions], "question_counts": counts,
                           "ready_papers": ready}


@router.patch("/exams/{exam_id}")
def patch_exam(exam_id: uuid.UUID, body: ExamPatch, admin: User = Depends(content), db: Session = Depends(get_db)):
    e = _exam(db, exam_id)
    data = body.model_dump(exclude_unset=True)
    if "category" in data and data["category"] not in catalog.CATEGORIES:
        raise AppError(422, "invalid_category", "Unknown category")
    for k, v in data.items():
        setattr(e, k, v)
    audit(db, admin, "exam.update", "exam", e.id, **data)
    db.commit()
    catalog.invalidate()
    return _exam_out(e)


@router.post("/exams/{exam_id}/publish")
def publish(exam_id: uuid.UUID, admin: User = Depends(content), db: Session = Depends(get_db)):
    e = _exam(db, exam_id)
    if e.current_blueprint_version is None:
        raise AppError(409, "no_blueprint", "Add and activate a blueprint before publishing")
    b = papers.current_blueprint(db, e)
    topics = db.scalars(select(Topic).where(Topic.exam_id == e.id)).all()
    missing = [s["key"] for s in b.sections if not bp.section_topics(s, topics)]
    if missing:
        raise AppError(409, "blueprint_incomplete", f"Sections without syllabus topics: {missing}")
    e.status = "published"
    audit(db, admin, "exam.publish", "exam", e.id)
    db.commit()
    catalog.invalidate()
    return _exam_out(e)


@router.post("/exams/{exam_id}/hide")
def hide(exam_id: uuid.UUID, admin: User = Depends(content), db: Session = Depends(get_db)):
    e = _exam(db, exam_id)
    e.status = "hidden"
    audit(db, admin, "exam.hide", "exam", e.id)
    db.commit()
    catalog.invalidate()
    return _exam_out(e)


# ---- blueprints ---------------------------------------------------------------------------------------------------
class SectionIn(BaseModel):
    key: str = Field(pattern=r"^[a-z0-9_]{1,40}$")
    name: str
    question_count: int = Field(ge=1, le=300)
    marks_per_question: float = Field(gt=0)
    negative_marks: float = Field(default=0, ge=0)
    question_types: dict[str, int] | None = None
    topic_ids: list[int] | None = None
    duration_min: int | None = None


class BlueprintIn(BaseModel):
    sections: list[SectionIn] = Field(min_length=1, max_length=20)
    duration_min: int
    marking_scheme: dict = Field(default_factory=dict)
    difficulty_mix: dict[str, float]
    languages: list[str] = ["en"]
    calculator_allowed: bool = False
    section_switching_allowed: bool = True
    instructions: str = ""
    activate: bool = True


def _bp_out(b: ExamBlueprint) -> dict:
    return {"id": b.id, "version": b.version, "sections": b.sections, "duration_min": b.duration_min,
            "marking_scheme": b.marking_scheme, "difficulty_mix": b.difficulty_mix, "languages": b.languages,
            "calculator_allowed": b.calculator_allowed, "section_switching_allowed": b.section_switching_allowed,
            "instructions": b.instructions, "total_marks": bp.total_marks(b.sections), "created_at": b.created_at}


@router.post("/exams/{exam_id}/blueprints", status_code=201)
def add_blueprint(exam_id: uuid.UUID, body: BlueprintIn, admin: User = Depends(content), db: Session = Depends(get_db)):
    """Creates a new blueprint version (old papers keep their pinned version). Validated before saving."""
    e = _exam(db, exam_id)
    sections = [s.model_dump(exclude_none=True) for s in body.sections]
    topic_section = {t.id: t.section_key for t in db.scalars(select(Topic).where(Topic.exam_id == e.id))}
    errors = bp.validate(sections, body.duration_min, body.difficulty_mix, body.languages, topic_section)
    if errors:
        raise AppError(422, "invalid_blueprint", "Blueprint is invalid", errors)
    version = (db.scalar(select(func.max(ExamBlueprint.version)).where(ExamBlueprint.exam_id == e.id)) or 0) + 1
    b = ExamBlueprint(exam_id=e.id, version=version, sections=sections, duration_min=body.duration_min,
                      marking_scheme=body.marking_scheme, difficulty_mix=body.difficulty_mix, languages=body.languages,
                      calculator_allowed=body.calculator_allowed, section_switching_allowed=body.section_switching_allowed,
                      instructions=body.instructions)
    db.add(b)
    if body.activate:
        e.current_blueprint_version = version
    audit(db, admin, "blueprint.create", "exam", e.id, version=version, activate=body.activate)
    db.commit()
    catalog.invalidate()
    return _bp_out(b)


@router.post("/exams/{exam_id}/blueprints/{version}/activate")
def activate_blueprint(exam_id: uuid.UUID, version: int, admin: User = Depends(content), db: Session = Depends(get_db)):
    e = _exam(db, exam_id)
    if db.scalar(select(ExamBlueprint).where(ExamBlueprint.exam_id == e.id, ExamBlueprint.version == version)) is None:
        raise not_found("Blueprint version")
    e.current_blueprint_version = version
    audit(db, admin, "blueprint.activate", "exam", e.id, version=version)
    db.commit()
    catalog.invalidate()
    return _exam_out(e)


# ---- topics -------------------------------------------------------------------------------------------------------
class TopicIn(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    parent_id: int | None = None
    section_key: str | None = None
    weightage: float = Field(default=1.0, gt=0)


class TopicPatch(BaseModel):
    name: str | None = None
    section_key: str | None = None
    weightage: float | None = Field(default=None, gt=0)


def _topic_out(t: Topic) -> dict:
    return {"id": t.id, "exam_id": t.exam_id, "parent_id": t.parent_id, "section_key": t.section_key,
            "name": t.name, "weightage": t.weightage}


@router.get("/exams/{exam_id}/topics")
def list_topics(exam_id: uuid.UUID, admin: User = Depends(expert), db: Session = Depends(get_db)):
    return {"items": [_topic_out(t) for t in db.scalars(select(Topic).where(Topic.exam_id == exam_id).order_by(Topic.id))]}


@router.post("/exams/{exam_id}/topics", status_code=201)
def add_topic(exam_id: uuid.UUID, body: TopicIn, admin: User = Depends(content), db: Session = Depends(get_db)):
    _exam(db, exam_id)
    if body.parent_id and (p := db.get(Topic, body.parent_id)) is not None and p.exam_id != exam_id:
        raise AppError(422, "invalid_parent", "Parent topic belongs to another exam")
    t = Topic(exam_id=exam_id, **body.model_dump())
    db.add(t)
    db.flush()
    audit(db, admin, "topic.create", "topic", t.id, name=t.name)
    db.commit()
    return _topic_out(t)


@router.patch("/topics/{topic_id}")
def patch_topic(topic_id: int, body: TopicPatch, admin: User = Depends(content), db: Session = Depends(get_db)):
    t = db.get(Topic, topic_id)
    if t is None:
        raise not_found("Topic")
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(t, k, v)
    audit(db, admin, "topic.update", "topic", t.id, **data)
    db.commit()
    return _topic_out(t)


@router.delete("/topics/{topic_id}", status_code=204)
def delete_topic(topic_id: int, admin: User = Depends(content), db: Session = Depends(get_db)):
    t = db.get(Topic, topic_id)
    if t is None:
        raise not_found("Topic")
    if db.scalar(select(func.count()).select_from(Question).where(Question.topic_id == t.id)):
        raise AppError(409, "topic_in_use", "Questions use this topic; reduce its weightage instead of deleting it")
    audit(db, admin, "topic.delete", "topic", t.id, name=t.name)
    db.delete(t)
    db.commit()


# ---- papers & generation --------------------------------------------------------------------------------------------
class PaperGenIn(BaseModel):
    count: int = Field(default=1, ge=1, le=5)


@router.post("/exams/{exam_id}/papers/generate", status_code=201)
def generate_papers(exam_id: uuid.UUID, body: PaperGenIn, admin: User = Depends(content), db: Session = Depends(get_db)):
    """Builds blueprint-exact papers now (bank first, generating only missing slots)."""
    e = _exam(db, exam_id)
    made = []
    for _ in range(body.count):
        p = papers.assemble_paper(db, e)
        db.commit()
        made.append({"id": p.id, "blueprint_version": p.blueprint_version, "questions": len(p.items)})
    audit(db, admin, "paper.generate", "exam", e.id, count=len(made))
    db.commit()
    return {"items": made}


@router.get("/exams/{exam_id}/papers")
def list_papers(exam_id: uuid.UUID, status: str | None = None, admin: User = Depends(content), db: Session = Depends(get_db)):
    stmt = select(Paper).where(Paper.exam_id == exam_id)
    if status:
        stmt = stmt.where(Paper.status == status)
    return {"items": [{"id": p.id, "blueprint_version": p.blueprint_version, "status": p.status,
                       "questions": len(p.items), "created_at": p.created_at}
                      for p in db.scalars(stmt.order_by(Paper.created_at.desc()).limit(200))]}


class BankBuildIn(BaseModel):
    per_topic: int = Field(default=20, ge=1, le=500)
    background: bool = True


@router.post("/exams/{exam_id}/bank/build", status_code=202)
def build_bank(exam_id: uuid.UUID, body: BankBuildIn, admin: User = Depends(content), db: Session = Depends(get_db)):
    """Question bank builder: fill every topic with `per_topic` verified questions (generate + verify + dedup +
    translate). Runs as a background job by default; `background: false` runs it now and returns the stats
    (pass rate, AI cost per verified question)."""
    from app.jobs.queue import enqueue
    from app.services.bank import build_bank as run

    e = _exam(db, exam_id)
    audit(db, admin, "bank.build", "exam", e.id, per_topic=body.per_topic, background=body.background)
    db.commit()
    if body.background:
        enqueue("build_bank", exam_id=e.id, per_topic=body.per_topic)
        return {"status": "queued", "exam": e.slug, "per_topic": body.per_topic}
    return {"status": "done"} | run(db, e, body.per_topic)


class QuestionGenIn(BaseModel):
    topic_id: int
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    qtype: Literal["single", "multi", "numeric"] = "single"
    count: int = Field(default=1, ge=1, le=10)


@router.post("/exams/{exam_id}/questions/generate", status_code=201)
def generate_questions(exam_id: uuid.UUID, body: QuestionGenIn, admin: User = Depends(expert), db: Session = Depends(get_db)):
    e = _exam(db, exam_id)
    t = db.get(Topic, body.topic_id)
    if t is None or t.exam_id != e.id:
        raise not_found("Topic")
    langs = papers.current_blueprint(db, e).languages if e.current_blueprint_version else ["en"]
    out = []
    for _ in range(body.count):
        q = generate_question(db, exam=e, topic=t, section_name=t.section_key or "", difficulty=body.difficulty,
                              qtype=body.qtype, languages=langs)
        out.append(str(q.id) if q else None)
    audit(db, admin, "question.generate", "exam", e.id, topic_id=t.id, requested=body.count,
          verified=sum(1 for x in out if x))
    db.commit()
    return {"verified": [x for x in out if x], "discarded": sum(1 for x in out if not x)}


@router.get("/exams/{exam_id}/generation-log")
def generation_log(exam_id: uuid.UUID, outcome: str | None = None, limit: int = Query(default=50, le=200),
                   admin: User = Depends(expert), db: Session = Depends(get_db)):
    stmt = select(QuestionGenerationLog).where(QuestionGenerationLog.exam_id == exam_id)
    if outcome:
        stmt = stmt.where(QuestionGenerationLog.outcome == outcome)
    return {"items": [{"id": l.id, "topic_id": l.topic_id, "outcome": l.outcome, "reason": l.reason,
                       "question_id": l.question_id, "created_at": l.created_at}
                      for l in db.scalars(stmt.order_by(QuestionGenerationLog.id.desc()).limit(limit))]}


# ---- question bank ------------------------------------------------------------------------------------------------
def _q_out(q: Question, full: bool = False) -> dict:
    out = {"id": q.id, "exam_id": q.exam_id, "topic_id": q.topic_id, "subtopic": q.subtopic, "type": q.type,
           "difficulty": q.difficulty, "status": q.status, "text": q.text, "times_served": q.times_served,
           "accuracy_rate": q.accuracy_rate, "report_count": q.report_count, "sampled_for_review": q.sampled_for_review,
           "verified_by": q.verified_by, "source": q.source, "created_at": q.created_at}
    if full:
        out |= {"options": q.options, "correct_answer": q.correct_answer["value"], "explanation": q.explanation,
                "shortcut": q.shortcut, "expected_time_sec": q.expected_time_sec, "generation_meta": q.generation_meta,
                "translations": [{"language": t.language, "text": t.text, "options": t.options,
                                  "explanation": t.explanation, "shortcut": t.shortcut,
                                  "review_status": t.review_status} for t in q.translations]}
    return out


@router.get("/questions")
def search_questions(exam_id: uuid.UUID | None = None, topic_id: int | None = None, status: str | None = None,
                     difficulty: str | None = None, q: str | None = None, reported: bool | None = None,
                     sampled: bool | None = None, limit: int = Query(default=50, ge=1, le=200),
                     offset: int = Query(default=0, ge=0), admin: User = Depends(expert), db: Session = Depends(get_db)):
    stmt = select(Question)
    for cond, clause in ((exam_id, Question.exam_id == exam_id), (topic_id, Question.topic_id == topic_id),
                         (status, Question.status == status), (difficulty, Question.difficulty == difficulty)):
        if cond is not None:
            stmt = stmt.where(clause)
    if q:
        stmt = stmt.where(Question.text.ilike(f"%{q}%"))
    if reported is not None:
        stmt = stmt.where(Question.report_count > 0 if reported else Question.report_count == 0)
    if sampled is not None:
        stmt = stmt.where(Question.sampled_for_review.is_(sampled))
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    rows = db.scalars(stmt.order_by(Question.created_at.desc()).limit(limit).offset(offset)).all()
    return {"items": [_q_out(x) for x in rows], "total": total, "limit": limit, "offset": offset}


@router.get("/questions/{question_id}")
def get_question(question_id: uuid.UUID, admin: User = Depends(expert), db: Session = Depends(get_db)):
    q = db.get(Question, question_id)
    if q is None:
        raise not_found("Question")
    reps = db.scalars(select(QuestionReport).where(QuestionReport.question_id == q.id)).all()
    return _q_out(q, full=True) | {"reports": [{"id": r.id, "reason": r.reason, "details": r.details,
                                                 "language": r.language, "status": r.status,
                                                 "resolution": r.resolution, "created_at": r.created_at} for r in reps]}


class QuestionPatch(BaseModel):
    text: str | None = None
    options: list[dict] | None = None
    correct_answer: str | list[str] | float | None = None
    explanation: str | None = None
    shortcut: str | None = None
    difficulty: Literal["easy", "medium", "hard"] | None = None
    expected_time_sec: int | None = Field(default=None, ge=10, le=900)
    subtopic: str | None = None


class QuestionAdminPatch(QuestionPatch):
    # edit: change fields | remove: hide from new papers | confirm_wrong: hide + save correction + write an AI lesson
    action: Literal["edit", "remove", "confirm_wrong"] = "edit"
    correction: str | None = Field(default=None, max_length=2000)


@router.patch("/questions/{question_id}")
def edit_question(question_id: uuid.UUID, body: QuestionAdminPatch, admin: User = Depends(expert),
                  db: Session = Depends(get_db)):
    """Edit, remove, or confirm a flagged question as wrong (API Plan #32)."""
    q = db.get(Question, question_id)
    if q is None:
        raise not_found("Question")
    fix = body.model_dump(exclude_unset=True, exclude={"action", "correction"})
    if body.action == "confirm_wrong":
        if not body.correction:
            raise AppError(422, "correction_required", "Describe what was wrong and the correct answer")
        lesson = questions.confirm_wrong(db, admin, q, body.correction, fix or None)
        return _q_out(q, full=True) | {"lesson": _lesson_out(lesson)}
    if body.action == "remove":
        q.status = "rejected"
        audit(db, admin, "question.remove", "question", q.id)
    else:
        questions.apply_fix(db, q, fix)
        audit(db, admin, "question.edit", "question", q.id, fields=list(fix))
    db.commit()
    return _q_out(q, full=True)


@router.get("/flags")
def flagged_questions(status: Literal["open", "confirmed", "rejected"] = "open", exam_id: uuid.UUID | None = None,
                      limit: int = Query(default=100, le=500), admin: User = Depends(expert), db: Session = Depends(get_db)):
    """Flagged questions with every flag (reason, language, details), most-flagged first (API Plan #31)."""
    stmt = select(QuestionReport).where(QuestionReport.status == status).order_by(QuestionReport.created_at)
    flags = db.scalars(stmt.limit(2000)).all()
    by_q: dict = {}
    for f in flags:
        by_q.setdefault(f.question_id, []).append({"id": f.id, "reason": f.reason, "details": f.details,
                                                   "language": f.language, "user_id": f.user_id,
                                                   "created_at": f.created_at, "resolution": f.resolution})
    qs = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(list(by_q))))}
    if exam_id:
        qs = {k: v for k, v in qs.items() if v.exam_id == exam_id}
    items = [{"question": _q_out(q, full=True), "flag_count": len(by_q[qid]), "flags": by_q[qid]} for qid, q in qs.items()]
    items.sort(key=lambda i: i["flag_count"], reverse=True)
    return {"items": items[:limit], "total": len(items)}


@router.post("/questions/{question_id}/{action}")
def question_action(question_id: uuid.UUID, action: Literal["approve", "quarantine", "reject"],
                    admin: User = Depends(expert), db: Session = Depends(get_db)):
    """approve: verified by a subject expert (also clears the 10% sample flag); quarantine: out of new papers;
    reject: permanently out, kept as a known-bad question for duplicate blocking."""
    q = db.get(Question, question_id)
    if q is None:
        raise not_found("Question")
    q.status = {"approve": "verified", "quarantine": "quarantined", "reject": "rejected"}[action]
    if action == "approve":
        q.verified_by = f"expert:{admin.id}"
        q.sampled_for_review = False
    audit(db, admin, f"question.{action}", "question", q.id)
    db.commit()
    return _q_out(q)


class TranslationIn(BaseModel):
    text: str
    options: list[dict] = []
    explanation: str = ""
    shortcut: str = ""
    review_status: Literal["approved", "rejected", "pending"] = "approved"


@router.put("/questions/{question_id}/translations/{language}")
def upsert_translation(question_id: uuid.UUID, language: str, body: TranslationIn,
                       admin: User = Depends(expert), db: Session = Depends(get_db)):
    if not is_supported(language) or language == "en":
        raise AppError(422, "invalid_language", "Choose a supported non-English language")
    q = db.get(Question, question_id)
    if q is None:
        raise not_found("Question")
    tr = db.scalar(select(QuestionTranslation).where(QuestionTranslation.question_id == q.id,
                                                     QuestionTranslation.language == language))
    if tr is None:
        tr = QuestionTranslation(question_id=q.id, language=language, text=body.text)
        db.add(tr)
    tr.text, tr.options, tr.explanation, tr.shortcut = body.text, body.options or q.options, body.explanation, body.shortcut
    tr.review_status = body.review_status
    audit(db, admin, "translation.upsert", "question", q.id, language=language, review_status=body.review_status)
    db.commit()
    return {"question_id": q.id, "language": language, "review_status": tr.review_status}


@router.post("/questions/{question_id}/translations/{language}/generate")
def generate_translation(question_id: uuid.UUID, language: str, admin: User = Depends(expert), db: Session = Depends(get_db)):
    q = db.get(Question, question_id)
    if q is None:
        raise not_found("Question")
    tr = translate_question(db, q, language)
    db.commit()
    if tr is None:
        raise AppError(502, "translation_failed", "Translation failed; try again")
    return {"question_id": q.id, "language": language, "review_status": tr.review_status, "text": tr.text}


# ---- review queue -------------------------------------------------------------------------------------------------
@router.get("/review-queue")
def review_queue(exam_id: uuid.UUID | None = None, language: str | None = None, limit: int = Query(default=50, le=200),
                 admin: User = Depends(expert), db: Session = Depends(get_db)):
    """Every user-flagged question plus the 10% random sample of new AI questions (PDF 6.1 human check)."""
    rs = select(QuestionReport).where(QuestionReport.status == "open")
    if language:
        rs = rs.where(QuestionReport.language == language)
    reports = db.scalars(rs.order_by(QuestionReport.created_at).limit(limit)).all()
    flagged_ids = {r.question_id for r in reports}
    flagged = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(flagged_ids)))}
    if exam_id:
        flagged = {k: v for k, v in flagged.items() if v.exam_id == exam_id}
    ss = select(Question).where(Question.sampled_for_review.is_(True), Question.status == "verified")
    if exam_id:
        ss = ss.where(Question.exam_id == exam_id)
    sample = db.scalars(ss.order_by(Question.created_at).limit(limit)).all()
    return {
        "flagged": [{"report_id": r.id, "reason": r.reason, "details": r.details, "language": r.language,
                     "created_at": r.created_at, "question": _q_out(flagged[r.question_id])}
                    for r in reports if r.question_id in flagged],
        "sample": [_q_out(q) for q in sample],
    }


class ResolveIn(BaseModel):
    action: Literal["confirm", "reject"]
    resolution: str = Field(min_length=3, max_length=2000)
    fix: QuestionPatch | None = None
    create_lesson: bool = True
    discard_question: bool = False


@router.post("/question-reports/{report_id}/resolve")
def resolve(report_id: int, body: ResolveIn, admin: User = Depends(expert), db: Session = Depends(get_db)):
    """Confirm (apply fix / discard, write an AI lesson) or reject a user report."""
    r = questions.resolve_report(db, admin, report_id, action=body.action, resolution=body.resolution,
                                 fix=body.fix.model_dump(exclude_unset=True) if body.fix else None,
                                 create_lesson=body.create_lesson and body.action == "confirm",
                                 discard_question=body.discard_question)
    return {"id": r.id, "status": r.status, "question_status": db.get(Question, r.question_id).status}


@router.post("/review-sample/draw")
def draw_sample(exam_id: uuid.UUID, rate: float = Query(default=0.1, gt=0, le=1), admin: User = Depends(expert),
                db: Session = Depends(get_db)):
    """Re-draws a random sample of verified, not-yet-expert-reviewed questions for review."""
    rows = db.scalars(select(Question).where(Question.exam_id == exam_id, Question.status == "verified",
                                             ~Question.verified_by.like("expert:%"))).all()
    picked = random.sample(rows, k=max(1, int(len(rows) * rate))) if rows else []
    for q in picked:
        q.sampled_for_review = True
    audit(db, admin, "review_sample.draw", "exam", exam_id, count=len(picked))
    db.commit()
    return {"sampled": len(picked)}


# ---- AI lessons & glossary ----------------------------------------------------------------------------------------
class LessonIn(BaseModel):
    lesson_text: str = Field(min_length=5, max_length=500)
    exam_id: uuid.UUID | None = None
    topic_id: int | None = None
    language: str = "en"
    active: bool = True


class LessonPatch(BaseModel):
    lesson_text: str | None = Field(default=None, min_length=5, max_length=500)
    active: bool | None = None
    language: str | None = None


def _lesson_out(l: AiLesson) -> dict:
    return {"id": l.id, "exam_id": l.exam_id, "topic_id": l.topic_id, "language": l.language,
            "lesson_text": l.lesson_text, "source_ref": l.source_ref, "active": l.active, "created_at": l.created_at}


@router.get("/lessons")
def list_lessons(exam_id: uuid.UUID | None = None, active: bool | None = None, language: str | None = None,
                 admin: User = Depends(content), db: Session = Depends(get_db)):
    stmt = select(AiLesson)
    if exam_id:
        stmt = stmt.where(AiLesson.exam_id == exam_id)
    if active is not None:
        stmt = stmt.where(AiLesson.active.is_(active))
    if language:
        stmt = stmt.where(AiLesson.language == language)
    return {"items": [_lesson_out(l) for l in db.scalars(stmt.order_by(AiLesson.id.desc()).limit(500))]}


@router.post("/lessons", status_code=201)
def add_lesson(body: LessonIn, admin: User = Depends(content), db: Session = Depends(get_db)):
    l = AiLesson(**body.model_dump(), embedding=embed(body.lesson_text), source_ref="manual")
    db.add(l)
    db.flush()
    audit(db, admin, "lesson.create", "ai_lesson", l.id)
    db.commit()
    return _lesson_out(l)


@router.patch("/lessons/{lesson_id}")
def patch_lesson(lesson_id: int, body: LessonPatch, admin: User = Depends(content), db: Session = Depends(get_db)):
    l = db.get(AiLesson, lesson_id)
    if l is None:
        raise not_found("Lesson")
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(l, k, v)
    if "lesson_text" in data:
        l.embedding = embed(l.lesson_text)
    audit(db, admin, "lesson.update", "ai_lesson", l.id, **data)
    db.commit()
    return _lesson_out(l)


class GlossaryIn(BaseModel):
    term: str = Field(min_length=1, max_length=160)
    language: str
    approved_translation: str = Field(min_length=1, max_length=300)


lang_admin = require_admin("content_manager", "language_reviewer")


@router.get("/glossary")
def list_glossary(language: str | None = None, q: str | None = None, admin: User = Depends(lang_admin),
                  db: Session = Depends(get_db)):
    stmt = select(Glossary)
    if language:
        stmt = stmt.where(Glossary.language == language)
    if q:
        stmt = stmt.where(or_(Glossary.term.ilike(f"%{q}%"), Glossary.approved_translation.ilike(f"%{q}%")))
    return {"items": [{"id": g.id, "term": g.term, "language": g.language,
                       "approved_translation": g.approved_translation} for g in db.scalars(stmt.order_by(Glossary.term))]}


@router.put("/glossary")
def upsert_glossary(body: GlossaryIn, admin: User = Depends(lang_admin), db: Session = Depends(get_db)):
    if not is_supported(body.language):
        raise AppError(422, "invalid_language", "Unsupported language")
    g = db.scalar(select(Glossary).where(Glossary.term == body.term, Glossary.language == body.language))
    if g is None:
        g = Glossary(term=body.term, language=body.language, approved_translation=body.approved_translation)
        db.add(g)
    g.approved_translation = body.approved_translation
    db.flush()
    audit(db, admin, "glossary.upsert", "glossary", g.id, term=g.term, language=g.language)
    db.commit()
    return {"id": g.id, "term": g.term, "language": g.language, "approved_translation": g.approved_translation}


@router.delete("/glossary/{glossary_id}", status_code=204)
def delete_glossary(glossary_id: int, admin: User = Depends(lang_admin), db: Session = Depends(get_db)):
    g = db.get(Glossary, glossary_id)
    if g is None:
        raise not_found("Glossary term")
    audit(db, admin, "glossary.delete", "glossary", g.id, term=g.term)
    db.delete(g)
    db.commit()


# ---- interview roles ----------------------------------------------------------------------------------------------
class RoleIn(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9-]{2,80}$")
    name: str
    description: str = ""
    levels: list[str] = ["fresher", "1-3", "3-5"]
    duration_min: int = Field(default=20, ge=10, le=45)
    rubric: dict = Field(default_factory=dict)
    prompt_config: dict = Field(default_factory=dict)
    credits_required: int = Field(default=1, ge=0, le=10)


class RolePatch(BaseModel):
    name: str | None = None
    description: str | None = None
    levels: list[str] | None = None
    duration_min: int | None = Field(default=None, ge=10, le=45)
    rubric: dict | None = None
    prompt_config: dict | None = None
    credits_required: int | None = Field(default=None, ge=0, le=10)
    status: Literal["draft", "published", "hidden"] | None = None


def _role_admin_out(r: InterviewRole) -> dict:
    return catalog.role_out(r) | {"status": r.status, "rubric": r.rubric, "prompt_config": r.prompt_config}


def _check_role_config(rubric: dict | None, cfg: dict | None) -> None:
    if rubric is not None:
        crit = rubric.get("criteria")
        if not isinstance(crit, list) or not crit or not all(isinstance(c, dict) and c.get("key") for c in crit):
            raise AppError(422, "invalid_rubric", 'rubric must be {"criteria": [{"key", "label", "description"}]}')
    if cfg is not None and "question_count" in cfg and not 8 <= int(cfg["question_count"]) <= 12:
        raise AppError(422, "invalid_prompt_config", "question_count must be between 8 and 12")


@router.get("/interview-roles")
def list_roles(admin: User = Depends(content), db: Session = Depends(get_db)):
    return {"items": [_role_admin_out(r) for r in db.scalars(select(InterviewRole).order_by(InterviewRole.name))]}


@router.post("/interview-roles", status_code=201)
def create_role(body: RoleIn, admin: User = Depends(content), db: Session = Depends(get_db)):
    _check_role_config(body.rubric or None, body.prompt_config)
    r = InterviewRole(**body.model_dump(), status="draft")
    db.add(r)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "slug_taken", "A role with this slug already exists")
    audit(db, admin, "interview_role.create", "interview_role", r.id, slug=r.slug)
    db.commit()
    return _role_admin_out(r)


@router.patch("/interview-roles/{role_id}")
def patch_role(role_id: uuid.UUID, body: RolePatch, admin: User = Depends(content), db: Session = Depends(get_db)):
    r = db.get(InterviewRole, role_id)
    if r is None:
        raise not_found("Interview role")
    data = body.model_dump(exclude_unset=True)
    _check_role_config(data.get("rubric"), data.get("prompt_config"))
    for k, v in data.items():
        setattr(r, k, v)
    audit(db, admin, "interview_role.update", "interview_role", r.id, fields=list(data))
    db.commit()
    return _role_admin_out(r)
