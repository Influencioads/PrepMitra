"""Question bank builder (15-day plan, Day 4): fills every topic of an exam with verified questions ahead of time.

Runs the full generation pipeline (generate -> verify -> duplicate check -> translate) per topic until the topic has
`per_topic` verified questions. The difficulty and question-type mix follow the blueprint. Cost per question is
reported from the ai_usage log.

    python -m app.services.bank --exam ssc-cgl-tier1 --per-topic 40
"""

import argparse
import logging
import time

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ai.provider import USD_TO_INR, cost_usd
from app.core.errors import not_found
from app.models import AiUsage, Exam, Question, Topic
from app.services import blueprints as bp
from app.services.papers import current_blueprint
from app.services.question_pipeline import generate_question

log = logging.getLogger(__name__)


def _cost_inr_since(db: Session, ref_id: str, since) -> float:
    usd = sum(cost_usd(model, tin, tout) for model, tin, tout in db.execute(
        select(AiUsage.model, func.sum(AiUsage.input_tokens), func.sum(AiUsage.output_tokens))
        .where(AiUsage.ref_id == ref_id, AiUsage.created_at >= since).group_by(AiUsage.model)))
    return round(usd * USD_TO_INR, 2)


def build_bank(db: Session, exam: Exam, per_topic: int, max_tries_factor: float = 2.0) -> dict:
    from app.db import utcnow

    started_at, t0 = utcnow(), time.monotonic()
    blueprint = current_blueprint(db, exam)
    topics = db.scalars(select(Topic).where(Topic.exam_id == exam.id)).all()
    verified = discarded = 0
    per_topic_out = []
    for section in blueprint.sections:
        types = section.get("question_types") or {"single": section["question_count"]}
        for topic in bp.section_topics(section, topics):
            have = db.scalar(select(func.count()).select_from(Question).where(
                Question.topic_id == topic.id, Question.status == "verified")) or 0
            need = max(0, per_topic - have)
            if need == 0:
                per_topic_out.append({"topic": topic.name, "had": have, "added": 0})
                continue
            # Plan the missing questions with the blueprint's difficulty and type mix.
            diffs = bp.largest_remainder(need, {d: blueprint.difficulty_mix.get(d, 0) for d in bp.DIFFICULTIES})
            qtypes = bp.largest_remainder(need, {t: n for t, n in types.items()})
            plan = list(zip([d for d, n in diffs.items() for _ in range(n)],
                            [t for t, n in qtypes.items() for _ in range(n)]))
            added = tries = 0
            budget = int(need * max_tries_factor) + 1
            while plan and tries < budget:
                diff, qtype = plan[0]
                tries += 1
                q = generate_question(db, exam=exam, topic=topic, section_name=section.get("name", section["key"]),
                                      difficulty=diff, qtype=qtype, languages=blueprint.languages)
                if q is None:
                    discarded += 1
                    continue
                plan.pop(0)
                added += 1
                verified += 1
            per_topic_out.append({"topic": topic.name, "had": have, "added": added, "short_by": len(plan)})
    cost = _cost_inr_since(db, str(exam.id), started_at)
    out = {"exam": exam.slug, "verified_added": verified, "discarded": discarded,
           "pass_rate": round(verified / (verified + discarded), 3) if verified + discarded else None,
           "ai_cost_inr": cost, "cost_per_verified_question_inr": round(cost / verified, 2) if verified else None,
           "seconds": round(time.monotonic() - t0, 1), "topics": per_topic_out}
    log.info("bank build %s: %s verified, %s discarded, ₹%s", exam.slug, verified, discarded, cost)
    return out


def build_bank_by_slug(db: Session, slug: str, per_topic: int) -> dict:
    exam = db.scalar(select(Exam).where(Exam.slug == slug))
    if exam is None:
        raise not_found("Exam")
    return build_bank(db, exam, per_topic)


if __name__ == "__main__":
    import json

    from app.db import SessionLocal

    logging.basicConfig(level=logging.INFO)
    ap = argparse.ArgumentParser(description="Fill an exam's question bank with verified AI questions")
    ap.add_argument("--exam", required=True, help="exam slug, e.g. ssc-cgl-tier1")
    ap.add_argument("--per-topic", type=int, default=20)
    args = ap.parse_args()
    with SessionLocal() as s:
        print(json.dumps(build_bank_by_slug(s, args.exam, args.per_topic), indent=2, ensure_ascii=False))
