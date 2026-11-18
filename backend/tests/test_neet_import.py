"""NEET (UG) bank import and the "medical" catalog category (docs/neet-bank)."""

from sqlalchemy import select

from app.models import Exam, ExamBlueprint, Question, Topic
from app.services import neet_import


def test_neet_import_builds_official_pattern_and_is_idempotent(db):
    from app.seed import seed

    seed(scope="launch")  # the launch catalog keeps NEET (UG) in draft
    report = neet_import.run(db, neet_import.DEFAULT_BANK, "draft", publish=False, dry_run=False)
    assert report["skipped"] == {}
    assert report["questions"] == {"added": report["bank_questions"]} and report["bank_questions"] >= 20

    exam = db.scalar(select(Exam).where(Exam.slug == "neet-ug"))
    assert exam.category == "medical" and exam.status == "draft"  # not served until an admin publishes it
    bp = db.scalar(select(ExamBlueprint).where(ExamBlueprint.exam_id == exam.id,
                                               ExamBlueprint.version == exam.current_blueprint_version))
    assert bp.duration_min == 180 and bp.difficulty_mix == {"easy": 30, "medium": 40, "hard": 30}
    assert [s["key"] for s in bp.sections] == ["physics", "chemistry", "botany", "zoology"]
    for s in bp.sections:
        assert (s["question_count"], s["marks_per_question"], s["negative_marks"]) == (45, 4, 1)
        assert "duration_min" not in s and s["topic_ids"]
    assert bp.section_switching_allowed  # one timer for the whole paper, as in NEET
    section_of = {t.id: t.section_key for t in db.scalars(select(Topic).where(Topic.exam_id == exam.id))}
    rows = list(db.scalars(select(Question).where(Question.exam_id == exam.id)))
    assert all(r.status == "draft" and r.source == "bank" for r in rows)
    assert {section_of[r.topic_id] for r in rows} == {"physics", "chemistry", "botany", "zoology"}
    sample = next(r for r in rows if r.generation_meta["bank_id"] == "NEET_ZOO_000005")
    assert sample.correct_answer == {"value": "D"} and sample.generation_meta["format"] == "assertion_reason"

    # an admin's decision survives a re-import; nothing is duplicated and the blueprint is not re-versioned
    sample.status = "verified"
    db.commit()
    again = neet_import.run(db, neet_import.DEFAULT_BANK, "draft", publish=True, dry_run=False)
    assert again["questions"] == {"updated": len(rows)} and again["blueprint_activated"] is None
    db.refresh(sample)
    db.refresh(exam)
    assert sample.status == "verified" and exam.status == "published"


def test_medical_category_is_listed(client, catalog_seeded):
    body = client.get("/v1/exams").json()
    assert {"key": "medical", "label": "Medical entrance"} in body["categories"]
