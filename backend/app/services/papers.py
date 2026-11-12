"""Paper assembly (PDF 6.1 "accumulation"): verified bank first, generate only the missing slots, never serve a
question the user has already seen. Papers are pre-generated in the background so Start is instant."""

import logging
import random
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models import Exam, ExamBlueprint, Paper, Question, QuestionTranslation, SeenQuestion, Topic, UserTopicMastery
from app.services import blueprints as bp
from app.services.question_pipeline import generate_question, translate_question

log = logging.getLogger(__name__)
MAX_GENERATION_TRIES = 3


def current_blueprint(db: Session, exam: Exam) -> ExamBlueprint:
    if exam.current_blueprint_version is None:
        raise AppError(409, "no_blueprint", "This exam has no active blueprint yet")
    b = db.scalar(select(ExamBlueprint).where(ExamBlueprint.exam_id == exam.id,
                                              ExamBlueprint.version == exam.current_blueprint_version))
    if b is None:
        raise AppError(409, "no_blueprint", "This exam has no active blueprint yet")
    return b


def seen_ids(db: Session, user_id) -> set:
    if user_id is None:
        return set()
    return set(db.scalars(select(SeenQuestion.question_id).where(SeenQuestion.user_id == user_id)))


def weak_topic_boost(db: Session, user_id, exam_id) -> dict[int, float]:
    """Memory module: topics with low mastery get up to 2x the blueprint weight in this user's next paper."""
    if user_id is None:
        return {}
    rows = db.execute(select(UserTopicMastery.topic_id, UserTopicMastery.mastery_score)
                      .join(Topic, Topic.id == UserTopicMastery.topic_id)
                      .where(UserTopicMastery.user_id == user_id, Topic.exam_id == exam_id)).all()
    return {tid: round(1.0 + max(0.0, 1.0 - 2 * m), 3) for tid, m in rows if m < 0.5}


def assemble_paper(db: Session, exam: Exam, *, user_id=None, allow_generate: bool = True, seed: int | None = None,
                   topic_boost: dict[int, float] | None = None) -> Paper:
    blueprint = current_blueprint(db, exam)
    topics = db.scalars(select(Topic).where(Topic.exam_id == exam.id)).all()
    topic_by_id = {t.id: t for t in topics}
    sections = {s["key"]: s for s in blueprint.sections}
    try:
        slots = bp.plan_slots(blueprint.sections, blueprint.difficulty_mix, topics, seed=seed, topic_boost=topic_boost)
    except ValueError as e:
        raise AppError(409, "blueprint_incomplete", str(e))

    excluded = seen_ids(db, user_id)
    items, chosen = [], {}
    rng = random.Random(seed)
    for slot in slots:
        candidates = db.scalars(
            select(Question).where(
                Question.exam_id == exam.id, Question.topic_id == slot["topic_id"], Question.status == "verified",
                Question.type == slot["qtype"], Question.difficulty == slot["difficulty"],
            ).order_by(Question.times_served, Question.created_at).limit(50)
        ).all()
        candidates = [q for q in candidates if q.id not in excluded]
        q = rng.choice(candidates[:10]) if candidates else None
        tries = 0
        while q is None and allow_generate and tries < MAX_GENERATION_TRIES:
            tries += 1
            q = generate_question(db, exam=exam, topic=topic_by_id[slot["topic_id"]],
                                  section_name=sections[slot["section_key"]].get("name", slot["section_key"]),
                                  difficulty=slot["difficulty"], qtype=slot["qtype"], languages=blueprint.languages)
        if q is None:
            raise AppError(503, "paper_unavailable",
                           "We could not prepare a fresh paper right now. Your credit was not used; please try again shortly.")
        excluded.add(q.id)
        chosen[str(q.id)] = q
        items.append({"seq": slot["seq"], "question_id": str(q.id), "section_key": slot["section_key"]})

    problems = bp.check_paper(blueprint.sections, blueprint.difficulty_mix, items, chosen)
    if problems:  # defensive: the slot plan guarantees this, so a failure here is a bug
        raise AppError(500, "paper_mismatch", "; ".join(problems))
    paper = Paper(exam_id=exam.id, blueprint_version=blueprint.version, items=items, status="ready")
    db.add(paper)
    db.flush()
    return paper


def pick_paper(db: Session, exam: Exam, user_id) -> Paper:
    """Users with weak topics get a personal paper that leans towards them (bank first, so it is still cheap).
    Everyone else gets a pre-generated paper with no question they have seen, else a fresh personal one."""
    blueprint = current_blueprint(db, exam)
    boost = weak_topic_boost(db, user_id, exam.id)
    if boost:
        return assemble_paper(db, exam, user_id=user_id, topic_boost=boost)
    seen = {str(s) for s in seen_ids(db, user_id)}
    ready = db.scalars(select(Paper).where(Paper.exam_id == exam.id, Paper.status == "ready",
                                           Paper.blueprint_version == blueprint.version)
                       .order_by(Paper.created_at).with_for_update(skip_locked=True).limit(20)).all()
    ids = {uuid.UUID(i["question_id"]) for p in ready for i in p.items}
    pulled = {str(q) for q in db.scalars(select(Question.id).where(
        Question.id.in_(ids), Question.status != "verified"))} if ids else set()
    for p in ready:
        if any(i["question_id"] in pulled for i in p.items):
            # A question was taken out of service after this paper was built (e.g. quarantined by 3 user flags);
            # retire the paper so the pre-generation job replaces it.
            p.status = "retired"
            continue
        if not any(i["question_id"] in seen for i in p.items):
            return p
    return assemble_paper(db, exam, user_id=user_id)


def ensure_translations(db: Session, question_ids: list, language: str) -> None:
    if language == "en":
        return
    have = set(db.scalars(select(QuestionTranslation.question_id).where(
        QuestionTranslation.question_id.in_(question_ids), QuestionTranslation.language == language)))
    for qid in question_ids:
        if qid not in have:
            q = db.get(Question, qid)
            if q is not None:
                translate_question(db, q, language)


def pregenerate(db: Session, pool_size: int) -> int:
    """Keeps `pool_size` ready papers per published exam (background job)."""
    made = 0
    for exam in db.scalars(select(Exam).where(Exam.status == "published")).all():
        if exam.current_blueprint_version is None:
            continue
        have = db.scalar(select(func.count()).select_from(Paper).where(
            Paper.exam_id == exam.id, Paper.status == "ready",
            Paper.blueprint_version == exam.current_blueprint_version)) or 0
        for _ in range(max(0, pool_size - have)):
            try:
                assemble_paper(db, exam)
                db.commit()
                made += 1
            except AppError as e:
                db.rollback()
                log.warning("pre-generation for %s stopped: %s", exam.slug, e.message)
                break
    return made
