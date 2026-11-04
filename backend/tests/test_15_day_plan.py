"""Backend items from PrepMitra_15_Day_Plan_Frontend_Backend.xlsx that were added on top of the PDF build:
Firebase login, API Plan endpoint names, launch scope, bank builder, weak-topic papers, "since your last attempt",
admin flags/confirm-wrong/payments/stats."""

import io
import uuid

import pytest
from sqlalchemy import select

from app.config import get_settings
from app.db import SessionLocal
from app.models import AiLesson, Exam, Question, QuestionReport, Topic, User, UserTopicMastery
from app.services import auth as auth_svc
from app.services import blueprints as bp
from app.services import memory, papers
from app.services.gateways import DEV_WEBHOOK_SECRET, MOCK_KEY_SECRET, hmac_hex
from tests.conftest import auth_headers, complete_profile, grant_credits, login

MINI = "mini-mock-general-aptitude"


# ---- Day 2: Firebase login -------------------------------------------------------------------------------------
@pytest.fixture
def firebase(monkeypatch):
    monkeypatch.setattr(get_settings(), "firebase_project_id", "prepmitra-test")
    tokens = {
        "fb-phone-token": {"sub": "uid-phone-1", "user_id": "uid-phone-1", "phone_number": "+919812345678"},
        "fb-google-token": {"sub": "uid-google-1", "email": "asha@example.com", "email_verified": True, "name": "Asha"},
    }

    def fake_decode(token):
        if token not in tokens:
            from app.core.errors import AppError
            raise AppError(401, "invalid_token", "Invalid or expired Firebase token")
        return tokens[token]

    monkeypatch.setattr(auth_svc, "decode_firebase_token", fake_decode)


def test_firebase_session_creates_user_and_token_works_everywhere(client, firebase, db):
    r = client.post("/v1/auth/session", headers={"Authorization": "Bearer fb-phone-token"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["is_new_user"] is True and body["user"]["phone"] == "+919812345678"
    assert body["user"]["profile_complete"] is False and body["access_token"]
    again = client.post("/v1/auth/session", json={"id_token": "fb-phone-token"}).json()
    assert again["is_new_user"] is False and again["user"]["id"] == body["user"]["id"]
    # The Firebase ID token itself is accepted on every API (API Plan note).
    me = client.get("/v1/me", headers={"Authorization": "Bearer fb-phone-token"})
    assert me.status_code == 200 and me.json()["id"] == body["user"]["id"]
    google = client.post("/v1/auth/session", headers={"Authorization": "Bearer fb-google-token"}).json()
    assert google["user"]["email"] == "asha@example.com" and google["user"]["name"] == "Asha"
    assert client.post("/v1/auth/session", headers={"Authorization": "Bearer forged"}).status_code == 401
    assert client.get("/v1/me", headers={"Authorization": "Bearer forged"}).status_code == 401


def test_firebase_links_to_existing_otp_account(client, firebase, db):
    login(client, "9812345678")  # same phone signed up earlier with the backend OTP
    body = client.post("/v1/auth/session", headers={"Authorization": "Bearer fb-phone-token"}).json()
    assert body["is_new_user"] is False
    assert db.scalar(select(User).where(User.phone == "+919812345678")).firebase_uid == "uid-phone-1"


def test_firebase_not_configured(client):
    r = client.post("/v1/auth/session", headers={"Authorization": "Bearer anything-long-enough"})
    assert r.status_code == 503 and r.json()["error"]["code"] == "firebase_not_configured"


# ---- Day 2 / 8: launch scope ------------------------------------------------------------------------------------
def test_launch_scope_catalog_and_plans(client):
    from app.seed import seed

    seed(scope="launch")
    exams = client.get("/v1/exams").json()
    # Banking only, plus the free mini mock.
    assert {e["slug"] for e in exams["items"]} == {
        MINI, "ibps-po-prelims", "ibps-clerk-prelims", "ibps-rrb-officer-prelims", "ibps-rrb-office-assistant-prelims",
        "sbi-po-prelims", "sbi-junior-associate-prelims"}
    assert all(e["languages"] == ["en", "hi"] for e in exams["items"])
    roles = {r["slug"] for r in client.get("/v1/interview-roles").json()["items"]}
    assert roles == {"bank-po-interview"}
    plans = {p["code"]: p for p in client.get("/v1/plans").json()["items"]}
    assert set(plans) == {"free_trial", "pay_per_exam", "credit_pack_10"}
    assert plans["credit_pack_10"]["price_paise"] == 39900 and plans["credit_pack_10"]["credits"] == 10
    assert plans["credit_pack_10"]["is_recurring"] is False and plans["credit_pack_10"]["validity_days"] == 90
    # Drafts exist and can be published from admin later without code.
    with SessionLocal() as s:
        assert s.scalar(select(Exam).where(Exam.slug == "cat")).status == "draft"
        assert s.scalar(select(Exam).where(Exam.slug == "ssc-cgl-tier1")).status == "draft"


# ---- API Plan endpoint names --------------------------------------------------------------------------------------
def test_paper_endpoint_with_hindi(client, catalog_seeded, ready_user):
    a = client.post("/v1/attempts", headers=ready_user, json={"exam_id": str(catalog_seeded[MINI])}).json()
    paper = client.get(f"/v1/attempts/{a['id']}/paper", headers=ready_user, params={"lang": "hi"}).json()
    q = paper["questions"][0]
    assert paper["language"] == "hi" and q["content"]["language"] == "hi" and q["content_en"]["language"] == "en"
    assert "correct_answer" not in str(paper) and paper["deadline_at"] and paper["remaining_seconds"] > 0
    assert client.get(f"/v1/attempts/{a['id']}/paper", headers=ready_user, params={"lang": "xx"}).status_code == 422


def test_flags_endpoint(client, catalog_seeded, ready_user):
    a = client.post("/v1/attempts", headers=ready_user, json={"exam_id": str(catalog_seeded[MINI])}).json()
    qid = a["questions"][0]["question_id"]
    r = client.post(f"/v1/questions/{qid}/flags", headers=ready_user, json={"reason": "bad_translation", "language": "hi"})
    assert r.status_code == 201 and r.json()["status"] == "open"


def test_orders_verify_and_razorpay_webhook_paths(client, catalog_seeded, user_headers):
    o = client.post("/v1/orders", headers=user_headers, json={"plan_code": "credit_pack_10"}).json()
    sig = hmac_hex(MOCK_KEY_SECRET, f"{o['gateway_order_id']}|pay_abc".encode())
    v = client.post("/v1/orders/verify", headers=user_headers, json={
        "razorpay_order_id": o["gateway_order_id"], "razorpay_payment_id": "pay_abc", "razorpay_signature": sig}).json()
    assert v["status"] == "paid" and v["credits"]["total"] == 10
    grant = v["credits"]["grants"][0]
    assert grant["expires_at"] and grant["reason"] == "purchase"

    o2 = client.post("/v1/orders", headers=user_headers, json={"plan_code": "pay_per_exam"}).json()
    raw = (b'{"event":"payment.captured","payload":{"payment":{"entity":{"id":"pay_w1","order_id":"'
           + o2["gateway_order_id"].encode() + b'"}}}}')
    hdr = {"X-Razorpay-Signature": hmac_hex(DEV_WEBHOOK_SECRET, raw), "X-Razorpay-Event-Id": "evt_w1",
           "Content-Type": "application/json"}
    assert client.post("/v1/webhooks/razorpay", content=raw, headers=hdr).json()["status"] == "fulfilled"
    assert client.post("/v1/webhooks/razorpay", content=raw, headers=hdr).json()["status"] == "duplicate"
    assert client.get("/v1/me/credits", headers=user_headers).json()["total"] == 11


def test_interview_answer_path_and_resume_upload(client, catalog_seeded, ready_user, db):
    from docx import Document

    doc = Document()
    doc.add_paragraph("Asha Kumar, Python developer. Phone 9876543210, email asha@mail.com. Built a Django library app.")
    buf = io.BytesIO()
    doc.save(buf)
    up = client.post("/v1/uploads/resume", headers=ready_user,
                     files={"file": ("cv.docx", buf.getvalue(), "application/octet-stream")}).json()
    assert up["has_resume"] and "Django" in up["preview"]
    assert "9876543210" not in up["preview"] and "asha@mail.com" not in up["preview"]

    grant_credits("9876500001", 1)
    role = client.get("/v1/interview-roles").json()["items"][0]
    s = client.post("/v1/interviews", headers=ready_user, json={"role_id": role["id"], "level": role["levels"][0]}).json()
    out = client.post(f"/v1/interviews/{s['id']}/answer", headers=ready_user, json={"text": "I built a Django app."}).json()
    assert out["done"] is False and out["turn"]["speaker"] == "interviewer"
    state = client.get(f"/v1/interviews/{s['id']}", headers=ready_user).json()
    assert len(state["transcript"]) == 3  # question, answer, next question: enough to resume
    from app.models import InterviewSession
    assert "Django" in db.get(InterviewSession, uuid.UUID(s["id"])).resume_ref  # profile resume used


# ---- Day 4: question bank builder ----------------------------------------------------------------------------------
def test_bank_builder_fills_every_topic(client, catalog_seeded, admin_headers, db):
    exam_id = catalog_seeded[MINI]
    r = client.post(f"/v1/admin/exams/{exam_id}/bank/build", headers=admin_headers,
                    json={"per_topic": 2, "background": False}).json()
    assert r["status"] == "done" and r["verified_added"] > 0 and r["pass_rate"] == 1.0
    assert all(t["had"] + t["added"] >= 2 for t in r["topics"])
    assert "cost_per_verified_question_inr" in r
    # Running again tops up nothing: every topic already has enough.
    again = client.post(f"/v1/admin/exams/{exam_id}/bank/build", headers=admin_headers,
                        json={"per_topic": 2, "background": False}).json()
    assert again["verified_added"] == 0
    queued = client.post(f"/v1/admin/exams/{exam_id}/bank/build", headers=admin_headers, json={"per_topic": 2}).json()
    assert queued["status"] == "queued"


# ---- Day 12: memory --------------------------------------------------------------------------------------------------
class _T:
    def __init__(self, id, section_key, weightage=1.0):
        self.id, self.section_key, self.weightage, self.parent_id = id, section_key, weightage, None


def test_weak_topics_get_more_questions_but_blueprint_stays_exact():
    sections = [{"key": "a", "question_count": 20, "marks_per_question": 1}]
    topics = [_T(1, "a"), _T(2, "a")]
    mix = {"easy": 30, "medium": 50, "hard": 20}
    even = bp.plan_slots(sections, mix, topics, seed=1)
    tilted = bp.plan_slots(sections, mix, topics, seed=1, topic_boost={2: 2.0})
    count = lambda slots, t: sum(1 for s in slots if s["topic_id"] == t)  # noqa: E731
    assert count(even, 2) == 10 and count(tilted, 2) > 10
    assert len(tilted) == 20
    assert {d: sum(1 for s in tilted if s["difficulty"] == d) for d in mix} == {"easy": 6, "medium": 10, "hard": 4}


def test_weak_topic_boost_from_mastery(client, catalog_seeded, ready_user, db):
    user = db.scalar(select(User).where(User.phone == "+919876500001"))
    exam_id = catalog_seeded[MINI]
    weak, strong = db.scalars(select(Topic).where(Topic.exam_id == exam_id).limit(2)).all()
    db.add_all([UserTopicMastery(user_id=user.id, topic_id=weak.id, mastery_score=0.1, attempts_count=5, correct_count=0),
                UserTopicMastery(user_id=user.id, topic_id=strong.id, mastery_score=0.9, attempts_count=5, correct_count=5)])
    db.commit()
    boost = papers.weak_topic_boost(db, user.id, exam_id)
    assert boost == {weak.id: 1.8}


def test_second_attempt_report_compares_with_first(client, catalog_seeded, ready_user):
    grant_credits("9876500001", 1)
    reps = []
    for _ in range(2):
        a = client.post("/v1/attempts", headers=ready_user, json={"exam_id": str(catalog_seeded[MINI])}).json()
        items = [{"question_id": q["question_id"], "answer": q["content"]["options"][0]["key"] if q["type"] == "single"
                  else (["A"] if q["type"] == "multi" else 1), "client_rev": 1, "time_spent_sec": 30}
                 for q in a["questions"]]
        client.put(f"/v1/attempts/{a['id']}/answers", headers=ready_user, json={"answers": items})
        client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user)
        reps.append(client.get(f"/v1/attempts/{a['id']}/report", headers=ready_user).json())
    assert reps[0]["report"]["since_last_attempt"] is None
    cmp = reps[1]["report"]["since_last_attempt"]
    assert cmp["score_before"] == reps[0]["analytics"]["score"] and cmp["score_now"] == reps[1]["analytics"]["score"]
    assert cmp["summary"] and "score_change" in cmp and isinstance(cmp["topics"], list)


# ---- Day 12-13: admin --------------------------------------------------------------------------------------------
def test_admin_flags_and_confirm_wrong_creates_lesson(client, catalog_seeded, ready_user, admin_headers, db):
    a = client.post("/v1/attempts", headers=ready_user, json={"exam_id": str(catalog_seeded[MINI])}).json()
    qid = a["questions"][0]["question_id"]
    client.post(f"/v1/questions/{qid}/flags", headers=ready_user, json={"reason": "wrong_answer", "details": "Key is C"})
    flags = client.get("/v1/admin/flags", headers=admin_headers).json()
    assert flags["total"] == 1 and flags["items"][0]["flag_count"] == 1
    assert flags["items"][0]["question"]["correct_answer"] is not None

    assert client.patch(f"/v1/admin/questions/{qid}", headers=admin_headers,
                        json={"action": "confirm_wrong"}).status_code == 422
    r = client.patch(f"/v1/admin/questions/{qid}", headers=admin_headers, json={
        "action": "confirm_wrong", "correction": "Option C is correct; 48 x 26 = 1248"}).json()
    assert r["status"] == "rejected" and r["lesson"]["active"] is True
    db.expire_all()
    q = db.get(Question, uuid.UUID(qid))
    assert q.generation_meta["correction"].startswith("Option C")
    assert db.scalar(select(QuestionReport)).status == "confirmed"
    assert client.get("/v1/admin/flags", headers=admin_headers).json()["total"] == 0
    # The lesson is now retrieved for new questions on this topic.
    assert r["lesson"]["lesson_text"] in memory.lessons_for(db, exam_id=q.exam_id, topic_id=q.topic_id, language="en",
                                                             query="new question")
    other = a["questions"][1]["question_id"]
    assert client.patch(f"/v1/admin/questions/{other}", headers=admin_headers,
                        json={"action": "remove"}).json()["status"] == "rejected"


def test_admin_payments_and_stats(client, catalog_seeded, ready_user, admin_headers):
    o = client.post("/v1/orders", headers=ready_user, json={"plan_code": "pay_per_exam"}).json()
    client.post(f"/v1/orders/{o['order_id']}/mock-pay", headers=ready_user)
    a = client.post("/v1/attempts", headers=ready_user, json={"exam_id": str(catalog_seeded[MINI])}).json()
    rid = client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user).json()["report_id"]
    client.post(f"/v1/reports/{rid}/rating", headers=ready_user, json={"rating": 5})
    pay = client.get("/v1/admin/payments", headers=admin_headers).json()
    assert pay["total"] == 1 and pay["items"][0]["status"] == "paid"
    st = client.get("/v1/admin/stats", headers=admin_headers).json()
    assert st["users"]["total"] >= 2 and st["attempts"]["started"] == 1 and st["attempts"]["free_trial"] == 1
    assert st["revenue"]["gross_paise"] == 9900 and st["report_rating"]["average"] == 5.0
    assert st["report_time_ms"]["p50"] is not None and "ai_cost_per_attempt_inr" in st
    assert client.get("/v1/admin/stats", headers=ready_user).status_code == 403


def test_rate_limit_switch(client, monkeypatch):
    for _ in range(5):
        client.post("/v1/auth/otp/send", json={"phone": "9811111111"})
    assert client.post("/v1/auth/otp/send", json={"phone": "9811111111"}).status_code == 429
    monkeypatch.setattr(get_settings(), "rate_limits_enabled", False)
    assert client.post("/v1/auth/otp/send", json={"phone": "9811111111"}).status_code == 200


def test_resend_email_adapter_selected(monkeypatch):
    from app.services import notifications

    monkeypatch.setattr(get_settings(), "email_provider", "resend")
    assert isinstance(notifications.get_email(), notifications.ResendEmail)
