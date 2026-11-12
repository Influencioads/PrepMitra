"""Imports the curated banking question bank (docs/question-bank) into the catalog.

For each of the six banking exams it makes sure both stages exist (the Mains exams are created if missing), adds the
bank's syllabus topics to every section, and activates a new blueprint built from the official 2026 pattern
(docs/question-bank/exam_patterns.json) whose sections draw only on those topics, so papers come from the bank
instead of AI generation. Each finished bank question is then stored once per exam stage whose sections test its
subject (the Question model is per exam), keyed by its bank ID so a re-run updates instead of duplicating.

    python -m app.services.bank_import                       # import as draft (not served until approved)
    python -m app.services.bank_import --status verified     # serve in mock tests now
    python -m app.services.bank_import --dry-run             # report what would change

Which bank files count as finished is read from docs/question-bank/viewer/index.json
(docs/question-bank/tools/build_viewer_index.py).
"""

import argparse
import json
import logging
from collections import Counter
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Exam, ExamBlueprint, Question, Topic
from app.services import blueprints as bp

log = logging.getLogger(__name__)

DEFAULT_BANK = Path(__file__).resolve().parents[3] / "docs" / "question-bank"
EXAM_SLUGS = {"IBPS_PO": "ibps-po", "IBPS_CSA": "ibps-clerk", "IBPS_RRB_OS1": "ibps-rrb-officer",
              "IBPS_RRB_OA": "ibps-rrb-office-assistant", "SBI_PO": "sbi-po", "SBI_JA": "sbi-junior-associate"}
DIFFICULTY = {"Basic": "easy", "Intermediate": "medium", "Advanced": "hard"}
MIX = {"easy": 30, "medium": 40, "hard": 30}  # the bank's own split
# Share of a section's topic weight per subject when one section tests two subjects (real papers lean this way).
SUBJECT_SHARE = {"Reasoning Ability": 0.7, "Computer Knowledge": 0.3,
                 "General Awareness and Current Affairs": 0.5, "Banking and Financial Awareness": 0.5}
INSTRUCTIONS = ("Read each question carefully. Unanswered questions get 0 marks; each wrong answer loses one quarter "
                "of the marks for that question. Each section is separately timed.")


def load_bank(bank: Path) -> tuple[dict, dict, list[dict]]:
    patterns = json.loads((bank / "exam_patterns.json").read_text(encoding="utf-8"))
    taxonomy = json.loads((bank / "taxonomy.json").read_text(encoding="utf-8"))
    index = json.loads((bank / "viewer" / "index.json").read_text(encoding="utf-8"))
    questions = []
    for f in index["files"]:
        doc = json.loads((bank / "viewer" / f["path"]).resolve().read_text(encoding="utf-8"))
        stimuli = {s["stimulus_id"]: s for s in doc["stimuli"]}
        for q in doc["questions"]:
            q["_stimulus"] = stimuli.get(q.get("stimulus_id"))
            questions.append(q)
    return patterns, taxonomy, questions


def stage_name(exam_id: str, stage: str, patterns: dict) -> str:
    base = next(e["name"] for e in patterns["exams"] if e["exam_id"] == exam_id).split(" (")[0]
    return f"{base} {stage}"


def ensure_exam(db: Session, slug: str, name: str, stage: dict, publish: bool) -> tuple[Exam, bool]:
    exam = db.scalar(select(Exam).where(Exam.slug == slug))
    created = exam is None
    description = (f"{name} mock: {sum(s['questions'] for s in stage['sections'])} questions, "
                   f"{sum(s['max_marks'] for s in stage['sections'])} marks, {stage['duration_min']} minutes "
                   "with sectional timing, as in the official 2026 notification.")
    if created:
        exam = Exam(slug=slug, name=name, category="banking", status="published" if publish else "draft",
                    credits_required=1, description=description)
        db.add(exam)
        db.flush()
    elif publish and exam.status == "draft":
        exam.status = "published"
    if slug.endswith("-mains"):  # exams this importer owns
        exam.name, exam.description = name, description
    return exam, created


def ensure_topics(db: Session, exam: Exam, section: dict, taxonomy: dict) -> list[int]:
    """The bank's topics for this section's subjects; returns their IDs in taxonomy order."""
    existing = {(t.section_key, t.name): t for t in db.scalars(select(Topic).where(Topic.exam_id == exam.id))}
    ids = []
    for subj in taxonomy["subjects"]:
        if subj["subject"] not in section["subjects"]:
            continue
        share = SUBJECT_SHARE.get(subj["subject"], 1.0) if len(section["subjects"]) > 1 else 1.0
        for t in subj["topics"]:
            weight = round(100 * share * t["target"] / subj["target"], 3)
            topic = existing.get((section["section_key"], t["topic"]))
            if topic is None:
                topic = Topic(exam_id=exam.id, section_key=section["section_key"], name=t["topic"], weightage=weight)
                db.add(topic)
                db.flush()
            else:
                topic.weightage = weight
            ids.append(topic.id)
    return ids


def ensure_blueprint(db: Session, exam: Exam, stage: dict, topic_ids: dict[str, list[int]]) -> int | None:
    """Activates a blueprint matching the official pattern; returns the new version, or None if already current."""
    sections = []
    for s in stage["sections"]:
        per_q = round(s["max_marks"] / s["questions"], 4)
        sections.append({"key": s["section_key"], "name": s["name"], "question_count": s["questions"],
                         "marks_per_question": per_q, "negative_marks": round(per_q * stage["negative_marking_fraction"], 4),
                         "question_types": {"single": s["questions"]}, "duration_min": s["duration_min"],
                         "topic_ids": topic_ids[s["section_key"]]})
    current = None
    if exam.current_blueprint_version is not None:
        current = db.scalar(select(ExamBlueprint).where(ExamBlueprint.exam_id == exam.id,
                                                        ExamBlueprint.version == exam.current_blueprint_version))
    if current is not None and current.sections == sections and current.duration_min == stage["duration_min"] \
            and current.difficulty_mix == MIX:
        return None
    languages = current.languages if current is not None else ["en"]
    topic_section = {t.id: t.section_key for t in db.scalars(select(Topic).where(Topic.exam_id == exam.id))}
    errors = bp.validate(sections, stage["duration_min"], MIX, languages, topic_section)
    if errors:
        raise ValueError(f"{exam.slug}: blueprint invalid: {errors}")
    version = (db.scalar(select(func.max(ExamBlueprint.version)).where(ExamBlueprint.exam_id == exam.id)) or 0) + 1
    db.add(ExamBlueprint(exam_id=exam.id, version=version, sections=sections, duration_min=stage["duration_min"],
                         marking_scheme={"unanswered": 0}, difficulty_mix=MIX, languages=languages,
                         calculator_allowed=False, section_switching_allowed=False, instructions=INSTRUCTIONS))
    exam.current_blueprint_version = version
    return version


def explanation_text(q: dict) -> str:
    s = q["solution"]
    parts = [f"Concept: {s['concept']}", s["explanation"],
             "Steps:\n" + "\n".join(f"{i}. {step}" for i, step in enumerate(s["steps"], 1))]
    if s.get("why_others_wrong"):
        parts.append(f"Why the other options are wrong: {s['why_others_wrong']}")
    checks = q["verification"].get("fact_checks") or []
    if checks:
        parts.append("Sources:\n" + "\n".join(f"- {c['source_url']} (checked {c['checked_on']})" for c in checks))
    return "\n\n".join(parts)


def question_fields(q: dict, status: str) -> dict:
    stim = q["_stimulus"]
    text = q["question_text"] if stim is None else f"{stim['title']}\n\n{stim['content']}\n\n{q['question_text']}"
    tags = q["verification"]["verified_by"]
    weak = "ai:independent-check" not in tags or "web:search-confirmed" in tags
    return {
        "subtopic": q["subtopic"], "type": "single", "difficulty": DIFFICULTY[q["difficulty"]], "status": status,
        "text": text, "options": q["options"], "correct_answer": {"value": q["correct_answer"]},
        "explanation": explanation_text(q), "shortcut": q["solution"].get("shortcut") or "",
        "expected_time_sec": q["suggested_time_seconds"], "source": "bank",
        "verified_by": ("bank:" + ",".join(tags))[:80],
        # weaker-checked questions go to the human review sample (admin review queue)
        "sampled_for_review": status == "verified" and weak,
        "generation_meta": {"bank_id": q["question_id"], "bank_review_status": q["verification"]["review_status"],
                            "stimulus_id": q.get("stimulus_id"), "set_position": q.get("set_position"),
                            "current_affairs": q.get("current_affairs"), "verification": q["verification"],
                            "bank_exam_mappings": q["exam_mappings"]},
    }


def run(db: Session, bank: Path, status: str, publish: bool, dry_run: bool) -> dict:
    patterns, taxonomy, questions = load_bank(bank)
    report = {"exams_created": [], "blueprints_activated": {}, "questions": Counter(), "skipped": Counter()}
    # (exam stage slug) -> (exam, {subject: (section_key, {topic name: topic id})})
    targets = {}
    for e in patterns["exams"]:
        for stage in e["stages"]:
            slug = f"{EXAM_SLUGS[e['exam_id']]}-{stage['stage'].lower()}"
            # name Mains like the app's existing Prelims exam ("IBPS PO Prelims" -> "IBPS PO Mains")
            prelims = db.scalar(select(Exam).where(Exam.slug == f"{EXAM_SLUGS[e['exam_id']]}-prelims"))
            name = prelims.name.replace("Prelims", stage["stage"]) if prelims else \
                stage_name(e["exam_id"], stage["stage"], patterns)
            exam, created = ensure_exam(db, slug, name, stage, publish)
            if created:
                report["exams_created"].append(slug)
            topic_ids = {s["section_key"]: ensure_topics(db, exam, s, taxonomy) for s in stage["sections"]}
            version = ensure_blueprint(db, exam, stage, topic_ids)
            if version:
                report["blueprints_activated"][slug] = version
            names = {t.id: t.name for t in db.scalars(select(Topic).where(Topic.exam_id == exam.id))}
            subjects = {}
            for s in stage["sections"]:
                for subj in s["subjects"]:
                    subjects[subj] = (s["section_key"], {names[i]: i for i in topic_ids[s["section_key"]]})
            targets[slug] = (exam, subjects)

    for slug, (exam, subjects) in targets.items():
        have = {}
        for row in db.scalars(select(Question).where(Question.exam_id == exam.id, Question.source == "bank")):
            have[(row.generation_meta or {}).get("bank_id")] = row
        for q in questions:
            if q["subject"] not in subjects:
                continue
            _, topic_by_name = subjects[q["subject"]]
            topic_id = topic_by_name.get(q["topic"])
            if topic_id is None:
                report["skipped"][f"no topic {q['topic']}"] += 1
                continue
            fields = question_fields(q, status) | {"topic_id": topic_id}
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
        log.info("%s: bank questions in place", slug)
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
    ap = argparse.ArgumentParser(description="Import the curated banking question bank into the catalog")
    ap.add_argument("--bank", type=Path, default=DEFAULT_BANK, help="docs/question-bank folder")
    ap.add_argument("--status", choices=["draft", "verified"], default="draft",
                    help="draft: wait for expert approval; verified: serve in mock tests now")
    ap.add_argument("--publish", action="store_true", help="publish newly created Mains exams")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with SessionLocal() as s:
        print(json.dumps(run(s, args.bank, args.status, args.publish, args.dry_run), indent=2))
