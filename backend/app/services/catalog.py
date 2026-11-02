"""Exam and interview catalog (PDF 5.2). Built only from published DB blueprints, so publishing in admin makes an
exam appear on web and apps without a release. Responses are cached in Redis for a minute and invalidated on
every admin change."""

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.cache import cache_delete_prefix, cache_get_json, cache_set_json
from app.core.errors import not_found
from app.models import Exam, ExamBlueprint, InterviewRole, Question, Topic
from app.services.blueprints import total_marks

CACHE_PREFIX = "catalog:"
CATEGORIES = {
    "central_govt": "Central government jobs", "banking": "Banking", "civil_services": "Civil services",
    "state_psc": "State PSC", "higher_education": "Higher education", "campus_hiring": "Campus and corporate hiring",
}
INTERVIEW_EVALUATES = ["Role knowledge", "Answer structure", "Communication", "Confidence", "Resume consistency"]


def disclaimer(exam_name: str) -> str:
    return (f"Mock test based on the {exam_name} pattern. Not affiliated with SSC, UPSC, IBPS, SBI, RRB, NTA, "
            f"IIMs, IITs or any exam-conducting body.")


def invalidate() -> None:
    cache_delete_prefix(CACHE_PREFIX)


def _blueprints(db: Session, exams: list[Exam]) -> dict:
    pairs = [(e.id, e.current_blueprint_version) for e in exams if e.current_blueprint_version]
    if not pairs:
        return {}
    rows = db.scalars(select(ExamBlueprint).where(ExamBlueprint.exam_id.in_([p[0] for p in pairs]))).all()
    want = set(pairs)
    return {b.exam_id: b for b in rows if (b.exam_id, b.version) in want}


def exam_summary(e: Exam, b: ExamBlueprint | None) -> dict:
    return {
        "id": e.id, "slug": e.slug, "name": e.name, "category": e.category,
        "category_label": CATEGORIES.get(e.category, e.category), "description": e.description,
        "credits_required": e.credits_required, "is_free_trial": e.is_free_trial,
        "duration_min": b.duration_min if b else None,
        "question_count": sum(s["question_count"] for s in b.sections) if b else None,
        "total_marks": total_marks(b.sections) if b else None,
        "languages": b.languages if b else ["en"], "disclaimer": disclaimer(e.name),
    }


def list_exams(db: Session, *, category: str | None, q: str | None, language: str | None,
               limit: int, offset: int) -> dict:
    key = f"{CACHE_PREFIX}exams:{category}:{q}:{language}:{limit}:{offset}"
    cached = cache_get_json(key)
    if cached is not None:
        return cached
    stmt = select(Exam).where(Exam.status == "published")
    if category:
        stmt = stmt.where(Exam.category == category)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(or_(Exam.name.ilike(like), Exam.slug.ilike(like), Exam.description.ilike(like)))
    exams = db.scalars(stmt.order_by(Exam.is_free_trial.desc(), Exam.name)).all()
    bps = _blueprints(db, exams)
    items = [exam_summary(e, bps.get(e.id)) for e in exams]
    if language:
        items = [i for i in items if language in i["languages"]]
    out = {"items": items[offset:offset + limit], "total": len(items),
           "categories": [{"key": k, "label": v} for k, v in CATEGORIES.items()]}
    cache_set_json(key, out, 60)
    return out


def exam_detail(db: Session, exam_ref: str) -> dict:
    stmt = select(Exam).where(Exam.status == "published")
    try:
        import uuid

        stmt = stmt.where(Exam.id == uuid.UUID(exam_ref))
    except ValueError:
        stmt = stmt.where(Exam.slug == exam_ref)
    e = db.scalar(stmt)
    if e is None:
        raise not_found("Exam")
    b = _blueprints(db, [e]).get(e.id)
    topics = db.scalars(select(Topic).where(Topic.exam_id == e.id)).all()
    sample = db.scalar(select(Question).where(Question.exam_id == e.id, Question.status == "verified",
                                              Question.type == "single").order_by(Question.created_at).limit(1))
    out = exam_summary(e, b)
    out.update({
        "pattern": None if b is None else {
            "blueprint_version": b.version, "duration_min": b.duration_min,
            "sections": [{"key": s["key"], "name": s.get("name", s["key"]), "question_count": s["question_count"],
                          "marks_per_question": s["marks_per_question"], "negative_marks": s.get("negative_marks", 0),
                          "question_types": s.get("question_types") or {"single": s["question_count"]},
                          "duration_min": s.get("duration_min")} for s in b.sections],
            "negative_marking": any((s.get("negative_marks") or 0) > 0 for s in b.sections),
            "marking_scheme": b.marking_scheme, "difficulty_mix": b.difficulty_mix,
            "calculator_allowed": b.calculator_allowed, "section_switching_allowed": b.section_switching_allowed,
            "instructions": b.instructions,
        },
        "syllabus": [{"id": t.id, "name": t.name, "parent_id": t.parent_id, "section_key": t.section_key,
                      "weightage": t.weightage} for t in topics],
        # A sample question with its answer hidden (it is shown publicly before purchase).
        "sample_question": None if sample is None else {"text": sample.text, "options": sample.options,
                                                        "type": sample.type, "difficulty": sample.difficulty},
    })
    return out


def role_out(r: InterviewRole) -> dict:
    criteria = (r.rubric or {}).get("criteria") or []
    return {"id": r.id, "slug": r.slug, "name": r.name, "description": r.description, "levels": r.levels,
            "duration_min": r.duration_min, "credits_required": r.credits_required,
            "question_count": (r.prompt_config or {}).get("question_count", 10),
            "modes": ["text", "voice"],
            "evaluates": [c.get("label", c["key"]) for c in criteria] or INTERVIEW_EVALUATES}


def list_roles(db: Session, q: str | None) -> list[dict]:
    stmt = select(InterviewRole).where(InterviewRole.status == "published")
    if q:
        stmt = stmt.where(InterviewRole.name.ilike(f"%{q}%"))
    return [role_out(r) for r in db.scalars(stmt.order_by(InterviewRole.name))]


def role_detail(db: Session, ref: str) -> dict:
    import uuid

    try:
        r = db.get(InterviewRole, uuid.UUID(ref))
    except ValueError:
        r = db.scalar(select(InterviewRole).where(InterviewRole.slug == ref))
    if r is None or r.status != "published":
        raise not_found("Interview role")
    return role_out(r)
