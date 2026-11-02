"""Admin APIs (role-based, audited), catalog publishing, review queue -> AI lessons, quality dashboard,
dashboard/progress, notifications, devices, analytics events, migrations."""

import uuid
from datetime import timedelta
from pathlib import Path

from sqlalchemy import select

from app.db import SessionLocal, utcnow
from app.models import AiLesson, AuditLog, Notification, Question, QuestionReport, User
from app.services import notifications
from tests.conftest import grant_credits, make_admin

MINI = "mini-mock-general-aptitude"
BLUEPRINT = {
    "sections": [{"key": "quant", "name": "Quant", "question_count": 4, "marks_per_question": 1, "negative_marks": 0.25,
                  "question_types": {"single": 3, "numeric": 1}}],
    "duration_min": 10, "difficulty_mix": {"easy": 50, "medium": 50, "hard": 0}, "languages": ["en", "hi"],
}


def test_non_admin_and_wrong_role_are_forbidden(client, user_headers):
    assert client.get("/v1/admin/exams", headers=user_headers).status_code == 403
    finance = make_admin(client, "finance", "9000000002")
    assert client.get("/v1/admin/exams", headers=finance).status_code == 403
    assert client.get("/v1/admin/orders", headers=finance).status_code == 200


def test_admin_creates_and_publishes_exam_that_appears_in_catalog(client, admin_headers, db):
    e = client.post("/v1/admin/exams", headers=admin_headers, json={
        "slug": "state-psc-demo", "name": "State PSC Demo", "category": "state_psc"}).json()
    assert client.post(f"/v1/admin/exams/{e['id']}/publish", headers=admin_headers).status_code == 409
    bad = client.post(f"/v1/admin/exams/{e['id']}/blueprints", headers=admin_headers,
                      json=BLUEPRINT | {"difficulty_mix": {"easy": 50, "medium": 10}})
    assert bad.status_code == 422 and bad.json()["error"]["details"]
    assert client.post(f"/v1/admin/exams/{e['id']}/blueprints", headers=admin_headers, json=BLUEPRINT).status_code == 201
    assert client.post(f"/v1/admin/exams/{e['id']}/publish", headers=admin_headers).json()["error"]["code"] == "blueprint_incomplete"
    client.post(f"/v1/admin/exams/{e['id']}/topics", headers=admin_headers, json={"name": "Percentages", "section_key": "quant"})
    assert client.get("/v1/exams", params={"q": "State PSC"}).json()["total"] == 0  # cached? no: still draft
    assert client.post(f"/v1/admin/exams/{e['id']}/publish", headers=admin_headers).status_code == 200
    catalog = client.get("/v1/exams", params={"q": "State PSC"}).json()
    assert catalog["total"] == 1 and catalog["items"][0]["question_count"] == 4
    detail = client.get("/v1/exams/state-psc-demo").json()
    assert detail["pattern"]["negative_marking"] is True and "Not affiliated" in detail["disclaimer"]

    papers = client.post(f"/v1/admin/exams/{e['id']}/papers/generate", headers=admin_headers, json={"count": 1}).json()
    assert papers["items"][0]["questions"] == 4
    actions = {a.action for a in db.scalars(select(AuditLog))}
    assert {"exam.create", "blueprint.create", "topic.create", "exam.publish", "paper.generate"} <= actions


def test_catalog_filters(client, catalog_seeded):
    all_ = client.get("/v1/exams", params={"limit": 100}).json()
    assert all_["total"] == 15
    banking = client.get("/v1/exams", params={"category": "banking"}).json()
    assert {e["slug"] for e in banking["items"]} == {"ibps-po-prelims", "ibps-clerk-prelims", "sbi-po-prelims"}
    tamil = client.get("/v1/exams", params={"language": "ta"}).json()
    assert "cat" not in {e["slug"] for e in tamil["items"]} and tamil["total"] > 0
    roles = client.get("/v1/interview-roles").json()["items"]
    assert len(roles) == 6 and roles[0]["levels"]
    assert client.get("/v1/exams/does-not-exist").status_code == 404
    meta = client.get("/v1/meta").json()
    assert len(meta["languages"]) == 23 and "tab_switch" in meta["anti_cheat_event_types"]
    assert client.get("/v1/policies/privacy").json()["status"] == "draft"


def test_review_queue_confirm_creates_lesson_and_restores_question(client, catalog_seeded, ready_user, admin_headers, db):
    a = client.post("/v1/attempts", headers=ready_user, json={"exam_id": str(catalog_seeded[MINI])}).json()
    qid = a["questions"][0]["question_id"]
    client.post(f"/v1/questions/{qid}/reports", headers=ready_user, json={"reason": "wrong_answer", "details": "should be C"})
    q = db.get(Question, uuid.UUID(qid))
    q.status = "quarantined"
    db.commit()
    queue = client.get("/v1/admin/review-queue", headers=admin_headers).json()
    assert queue["flagged"][0]["question"]["id"] == qid
    rid = queue["flagged"][0]["report_id"]
    r = client.post(f"/v1/admin/question-reports/{rid}/resolve", headers=admin_headers, json={
        "action": "confirm", "resolution": "Answer key fixed to the correct option",
        "fix": {"explanation": "Corrected explanation"}}).json()
    assert r["status"] == "confirmed" and r["question_status"] == "verified"
    lesson = db.scalar(select(AiLesson).where(AiLesson.source_ref == f"question_report:{rid}"))
    assert lesson is not None and lesson.active and lesson.embedding
    db.expire_all()
    assert db.get(Question, uuid.UUID(qid)).explanation == "Corrected explanation"
    assert client.post(f"/v1/admin/question-reports/{rid}/resolve", headers=admin_headers,
                       json={"action": "reject", "resolution": "again"}).status_code == 409


def test_question_bank_admin_actions(client, catalog_seeded, admin_headers):
    gen = client.post(f"/v1/admin/exams/{catalog_seeded[MINI]}/questions/generate", headers=admin_headers, json={
        "topic_id": client.get(f"/v1/admin/exams/{catalog_seeded[MINI]}/topics", headers=admin_headers).json()["items"][0]["id"],
        "count": 2}).json()
    assert len(gen["verified"]) == 2
    qid = gen["verified"][0]
    full = client.get(f"/v1/admin/questions/{qid}", headers=admin_headers).json()
    assert full["correct_answer"] and len(full["translations"]) >= 1
    assert client.post(f"/v1/admin/questions/{qid}/quarantine", headers=admin_headers).json()["status"] == "quarantined"
    assert client.post(f"/v1/admin/questions/{qid}/approve", headers=admin_headers).json()["verified_by"].startswith("expert:")
    res = client.get("/v1/admin/questions", headers=admin_headers, params={"exam_id": str(catalog_seeded[MINI])}).json()
    assert res["total"] == 2
    log = client.get(f"/v1/admin/exams/{catalog_seeded[MINI]}/generation-log", headers=admin_headers).json()
    assert log["items"][0]["outcome"] == "verified"


def test_admin_users_credits_block_and_roles(client, ready_user, admin_headers):
    users = client.get("/v1/admin/users", headers=admin_headers, params={"q": "Asha"}).json()
    uid = users["items"][0]["id"]
    assert client.post(f"/v1/admin/users/{uid}/credits", headers=admin_headers,
                       json={"credits": 3, "note": "goodwill"}).json()["total"] == 3
    assert client.get(f"/v1/admin/users/{uid}", headers=admin_headers).json()["credits"]["total"] == 3
    assert client.post(f"/v1/admin/users/{uid}/block", headers=admin_headers, json={"reason": "abuse"}).json()["status"] == "blocked"
    assert client.get("/v1/me", headers=ready_user).status_code == 403
    client.post(f"/v1/admin/users/{uid}/unblock", headers=admin_headers)
    assert client.get("/v1/me", headers=ready_user).status_code == 200
    assert client.put(f"/v1/admin/users/{uid}/admin-role", headers=admin_headers,
                      json={"role": "support"}).json()["admin_role"] == "support"
    assert client.get("/v1/admin/audit-log", headers=admin_headers).json()["items"]


def test_quality_dashboard_and_revenue(client, catalog_seeded, ready_user, admin_headers):
    a = client.post("/v1/attempts", headers=ready_user, json={"exam_id": str(catalog_seeded[MINI])}).json()
    rid = client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user).json()["report_id"]
    client.post(f"/v1/reports/{rid}/rating", headers=ready_user, json={"rating": 4})
    qd = client.get("/v1/admin/quality", headers=admin_headers).json()
    assert qd["report_ratings"][0]["average"] == 4.0
    assert qd["question_generation"]["total"] >= 30 and qd["ai_cost"]["attempts_and_interviews"] == 1
    assert qd["report_generation_ms"]["p50"] is not None
    o = client.post("/v1/orders", headers=ready_user, json={"plan_code": "pay_per_exam"}).json()
    client.post(f"/v1/orders/{o['order_id']}/mock-pay", headers=ready_user)
    rev = client.get("/v1/admin/revenue", headers=admin_headers).json()
    assert rev["gross_paise"] == 9900 and rev["gst_paise"] == 1510


def test_progress_dashboard(client, catalog_seeded, ready_user):
    p0 = client.get("/v1/me/progress", headers=ready_user).json()
    assert p0["recommended"][0]["slug"] == MINI  # the free mini mock first
    a = client.post("/v1/attempts", headers=ready_user, json={"exam_id": str(catalog_seeded[MINI])}).json()
    client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user)
    p = client.get("/v1/me/progress", headers=ready_user).json()
    assert p["history"][0]["report_status"] == "ready"
    assert p["score_trend"][0]["points"] and p["topic_heatmap"] == [] or isinstance(p["topic_heatmap"], list)
    assert "total" in p["credits"] and p["recommended"]


def test_notifications_inbox_devices_and_jobs(client, catalog_seeded, ready_user, db):
    assert client.post("/v1/me/devices", headers=ready_user,
                       json={"platform": "android", "token": "fcm-token-1234567890"}).status_code == 201
    grant_credits("9876500001", 2, days=2)
    user = db.scalar(select(User).where(User.phone == "+919876500001"))
    user.last_active_at = utcnow() - timedelta(days=8)
    db.commit()
    with SessionLocal() as s:
        assert notifications.notify_expiring_credits(s) == 1 and notifications.notify_expiring_credits(s) == 0
        assert notifications.notify_inactive_users(s) == 1 and notifications.notify_inactive_users(s) == 0
    inbox = client.get("/v1/me/notifications", headers=ready_user).json()
    assert {n["kind"] for n in inbox["items"]} == {"plan_expiring", "practice_reminder"} and inbox["unread"] == 2
    client.post("/v1/me/notifications/read-all", headers=ready_user)
    assert client.get("/v1/me/notifications", headers=ready_user).json()["unread"] == 0


def test_notifications_are_localized(client, catalog_seeded, db):
    from tests.conftest import auth_headers, complete_profile, login

    h = auth_headers(login(client, "9876500077"))
    complete_profile(client, h, language="hi")
    a = client.post("/v1/attempts", headers=h, json={"exam_id": str(catalog_seeded[MINI]), "language": "hi"}).json()
    client.post(f"/v1/attempts/{a['id']}/submit", headers=h)
    n = db.scalar(select(Notification).where(Notification.kind == "result_ready"))
    assert "रिपोर्ट" in n.title and n.data["report_id"]


def test_client_events_and_error_envelope(client, user_headers):
    assert client.post("/v1/events", headers=user_headers, json={"name": "app_open", "props": {"platform": "ios"}}).status_code == 204
    r = client.post("/v1/events", headers=user_headers, json={"name": "purchase"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_event"
    v = client.post("/v1/attempts", headers=user_headers, json={"exam_id": "not-a-uuid"})
    assert v.status_code == 422 and v.json()["error"]["code"] == "validation_error" and v.json()["error"]["details"]
    assert client.get("/v1/nope").json()["error"]["code"] == "not_found"
    assert client.get("/v1/health").headers.get("X-Request-ID")


def test_migration_covers_every_table():
    """The Alembic migration (PostgreSQL DDL) must create every table the models define."""
    from app.db import Base

    text = next((Path(__file__).resolve().parents[1] / "alembic" / "versions").glob("0001_*.py")).read_text("utf-8")
    missing = [t for t in Base.metadata.tables if f"op.create_table('{t}'" not in text]
    assert missing == [], f"tables missing from migration (run alembic revision --autogenerate): {missing}"
    assert "CREATE EXTENSION IF NOT EXISTS vector" in text and "Vector(256)" in text
