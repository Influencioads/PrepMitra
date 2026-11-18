"""Imports the curated NEET (UG) question bank (docs/neet-bank) into the catalog.

Makes sure the NEET (UG) exam exists (category "medical"), adds the bank's NMC-syllabus topics to each of the four
sections, activates a blueprint built from the official pattern (docs/neet-bank/exam_patterns.json: 4 x 45 questions,
+4/-1, 180 minutes) whose sections draw only on those topics, and stores every bank question keyed by its bank ID so
a re-run updates instead of duplicating. Re-running never undoes an admin's approve/reject.

    python -m app.services.neet_import                       # import as draft (not served until approved)
    python -m app.services.neet_import --status verified     # serve in mock tests now (local dev)
    python -m app.services.neet_import --publish             # also publish the exam
    python -m app.services.neet_import --dry-run             # report what would change

Every file in docs/neet-bank/batches/*.json is imported; run tools/qbank.py validate on them first.
"""

import argparse
import json
import logging
from collections import Counter
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Exam, Question, Topic
from app.services.bank_import import DIFFICULTY, ensure_blueprint, question_fields

log = logging.getLogger(__name__)

DEFAULT_BANK = Path(__file__).resolve().parents[3] / "docs" / "neet-bank"
SLUG = "neet-ug"
MIX = {"easy": 30, "medium": 40, "hard": 30}  # the bank's own split
INSTRUCTIONS = ("All 180 questions are compulsory. Each correct answer gets 4 marks, each wrong answer loses 1 mark "
                "and an unanswered question gets 0. You may move between sections freely within the 3 hours.")


def load_bank(bank: Path) -> tuple[dict, dict, list[dict]]:
    patterns = json.loads((bank / "exam_patterns.json").read_text(encoding="utf-8"))
    taxonomy = json.loads((bank / "taxonomy.json").read_text(encoding="utf-8"))
    questions = []
    for path in sorted((bank / "batches").glob("BATCH_*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        stimuli = {s["stimulus_id"]: s for s in doc.get("stimuli", [])}
        for q in doc["questions"]:
            q["_stimulus"] = stimuli.get(q.get("stimulus_id"))
            questions.append(q)
    return patterns, taxonomy, questions


def ensure_exam(db: Session, stage: dict, publish: bool) -> tuple[Exam, bool]:
    exam = db.scalar(select(Exam).where(Exam.slug == SLUG))
    created = exam is None
    if created:
        n = sum(s["questions"] for s in stage["sections"])
        exam = Exam(slug=SLUG, name="NEET (UG)", category="medical", status="draft", credits_required=1,
                    description=f"NEET (UG) mock: {n} questions, {sum(s['max_marks'] for s in stage['sections'])} "
                                f"marks, {stage['duration_min']} minutes, +4/-1 marking.")
        db.add(exam)
        db.flush()
    if publish:
        exam.status = "published"
    return exam, created


def ensure_topics(db: Session, exam: Exam, section: dict, taxonomy: dict) -> dict[str, int]:
    """The bank's topics for this section's subject, weighted by planned questions; returns {name: id}."""
    existing = {(t.section_key, t.name): t for t in db.scalars(select(Topic).where(Topic.exam_id == exam.id))}
    out = {}
    for subj in taxonomy["subjects"]:
        if subj["subject"] not in section["subjects"]:
            continue
        for t in subj["topics"]:
            weight = round(100 * t["target"] / subj["target"], 3)
            topic = existing.get((section["section_key"], t["topic"]))
            if topic is None:
                topic = Topic(exam_id=exam.id, section_key=section["section_key"], name=t["topic"], weightage=weight)
                db.add(topic)
                db.flush()
            else:
                topic.weightage = weight
            out[t["topic"]] = topic.id
    return out


def neet_fields(q: dict, status: str) -> dict:
    """Banking field mapping plus the NEET-only bits (stem format, NCERT reference)."""
    fields = question_fields(q, status)
    ref = q["solution"].get("ncert_reference")
    if ref:
        fields["explanation"] += f"\n\nNCERT: {ref}"
    fields["generation_meta"] |= {"format": q["format"], "ncert_reference": ref}
    return fields


def run(db: Session, bank: Path, status: str, publish: bool, dry_run: bool) -> dict:
    patterns, taxonomy, questions = load_bank(bank)
    stage = patterns["exams"][0]["stages"][0]
    report = {"exam_created": False, "blueprint_activated": None, "questions": Counter(), "skipped": Counter()}

    exam, report["exam_created"] = ensure_exam(db, stage, publish)
    topics = {s["section_key"]: ensure_topics(db, exam, s, taxonomy) for s in stage["sections"]}
    # ensure_blueprint (shared with banking) derives negative marks as a fraction of per-question marks: 1/4 of 4.
    neg_fraction = -stage["marks_wrong"] / stage["marks_correct"]
    bp_stage = {"duration_min": stage["duration_min"], "negative_marking_fraction": neg_fraction,
                "sections": stage["sections"]}
    topic_ids = {k: list(v.values()) for k, v in topics.items()}
    report["blueprint_activated"] = ensure_blueprint(db, exam, bp_stage, topic_ids, mix=MIX, instructions=INSTRUCTIONS)

    section_of = {subj: s["section_key"] for s in stage["sections"] for subj in s["subjects"]}
    have = {(r.generation_meta or {}).get("bank_id"): r
            for r in db.scalars(select(Question).where(Question.exam_id == exam.id, Question.source == "bank"))}
    for q in questions:
        topic_id = topics.get(section_of.get(q["subject"]), {}).get(q["topic"])
        if topic_id is None or q["difficulty"] not in DIFFICULTY:
            report["skipped"][f"no topic {q['subject']}/{q['topic']}"] += 1
            continue
        fields = neet_fields(q, status) | {"topic_id": topic_id}
        row = have.get(q["question_id"])
        if row is None:
            db.add(Question(exam_id=exam.id, **fields))
            report["questions"]["added"] += 1
        else:
            fields.pop("status")  # never undo an admin's approve/quarantine/reject on re-import
            for k, v in fields.items():
                setattr(row, k, v)
            report["questions"]["updated"] += 1
    db.flush()
    if dry_run:
        db.rollback()
    else:
        db.commit()
    report["questions"] = dict(report["questions"])
    report["skipped"] = dict(report["skipped"])
    report["bank_questions"] = len(questions)
    return report


if __name__ == "__main__":
    from app.db import SessionLocal

    logging.basicConfig(level=logging.INFO)
    ap = argparse.ArgumentParser(description="Import the curated NEET (UG) question bank into the catalog")
    ap.add_argument("--bank", type=Path, default=DEFAULT_BANK, help="docs/neet-bank folder")
    ap.add_argument("--status", choices=["draft", "verified"], default="draft",
                    help="draft: wait for expert approval; verified: serve in mock tests now")
    ap.add_argument("--publish", action="store_true", help="publish the NEET (UG) exam")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with SessionLocal() as s:
        print(json.dumps(run(s, args.bank, args.status, args.publish, args.dry_run), indent=2))
