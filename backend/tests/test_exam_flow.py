"""Timed exam engine, scoring, AI report, credit rules and question reports (PDF 5.3, 5.5, 6.2, 7)."""

import uuid
from datetime import timedelta

from sqlalchemy import select

from app.ai.provider import AIError, MockProvider
from app.db import SessionLocal, utcnow
from app.models import Attempt, CreditLedger, Exam, Notification, Question, Report, SeenQuestion
from app.services import attempts as attempt_svc
from app.services import reports as report_svc
from tests.conftest import auth_headers, complete_profile, grant_credits, login

MINI = "mini-mock-general-aptitude"


def _start(client, h, exam_id, language="en"):
    return client.post("/v1/attempts", headers=h, json={"exam_id": str(exam_id), "language": language})


def _answer_all(client, h, attempt, rev=1, pick_first=True):
    items = []
    for q in attempt["questions"]:
        if q["type"] == "single":
            ans = q["content"]["options"][0]["key"]
        elif q["type"] == "multi":
            ans = ["A"]
        else:
            ans = 1
        items.append({"question_id": q["question_id"], "answer": ans, "client_rev": rev, "time_spent_sec": 30})
    return client.put(f"/v1/attempts/{attempt['id']}/answers", headers=h, json={"answers": items})


def test_profile_required_before_first_attempt(client, catalog_seeded, user_headers):
    r = _start(client, user_headers, catalog_seeded[MINI])
    assert r.status_code == 409 and r.json()["error"]["code"] == "profile_incomplete"


def test_free_trial_then_credits_required(client, catalog_seeded, ready_user):
    r = _start(client, ready_user, catalog_seeded[MINI])
    assert r.status_code == 201, r.text
    a = r.json()
    assert a["is_free_trial"] is True and a["resumed"] is False and len(a["questions"]) == 30
    assert 1790 <= a["remaining_seconds"] <= 1800
    client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user)
    # The free trial is one-time: the next attempt needs a credit.
    r2 = _start(client, ready_user, catalog_seeded[MINI])
    assert r2.status_code == 402 and r2.json()["error"]["code"] == "insufficient_credits"


def test_paid_attempt_consumes_oldest_expiring_credit_first(client, catalog_seeded, ready_user, db):
    grant_credits("9876500001", 1, days=60)
    grant_credits("9876500001", 1, days=5)
    r = _start(client, ready_user, catalog_seeded["general-aptitude-reasoning-verbal"])
    assert r.status_code == 201
    debit = db.scalar(select(CreditLedger).where(CreditLedger.delta < 0))
    grant = db.get(CreditLedger, debit.grant_id)
    assert (grant.expires_at - utcnow()).days < 6
    assert client.get("/v1/me/credits", headers=ready_user).json()["total"] == 1


def test_resume_returns_answers_and_server_remaining_time(client, catalog_seeded, ready_user, db):
    a = _start(client, ready_user, catalog_seeded[MINI]).json()
    q = a["questions"][0]
    client.put(f"/v1/attempts/{a['id']}/answers", headers=ready_user, json={"answers": [
        {"question_id": q["question_id"], "answer": q["content"]["options"][1]["key"], "marked_for_review": True,
         "client_rev": 1, "time_spent_sec": 40}]})
    # Simulate 10 minutes passing on the server.
    att = db.get(Attempt, uuid.UUID(a["id"]))
    att.deadline_at = att.deadline_at - timedelta(minutes=10)
    db.commit()
    again = _start(client, ready_user, catalog_seeded[MINI])  # pressing Start again resumes, no second charge
    assert again.status_code == 200 and again.json()["resumed"] is True and again.json()["id"] == a["id"]
    state = client.get(f"/v1/attempts/{a['id']}", headers=ready_user).json()
    saved = state["questions"][0]
    assert saved["answer"] == {"value": q["content"]["options"][1]["key"]} and saved["marked_for_review"]
    assert 1190 <= state["remaining_seconds"] <= 1200


def test_autosave_is_idempotent_and_ignores_stale_revisions(client, catalog_seeded, ready_user):
    a = _start(client, ready_user, catalog_seeded[MINI]).json()
    q = next(x for x in a["questions"] if x["type"] == "single")
    url = f"/v1/attempts/{a['id']}/answers"
    newer = {"question_id": q["question_id"], "answer": "B", "client_rev": 5, "time_spent_sec": 50}
    older = {"question_id": q["question_id"], "answer": "C", "client_rev": 4, "time_spent_sec": 10}
    assert client.put(url, headers=ready_user, json={"answers": [newer]}).json()["saved"] == 1
    r = client.put(url, headers=ready_user, json={"answers": [older, newer]}).json()  # late retry + duplicate
    assert r["saved"] == 0 and r["ignored_stale"] == 2
    state = client.get(f"/v1/attempts/{a['id']}", headers=ready_user).json()
    s = next(x for x in state["questions"] if x["question_id"] == q["question_id"])
    assert s["answer"] == {"value": "B"} and s["time_spent_sec"] == 50
    # Clearing a response.
    client.put(url, headers=ready_user, json={"answers": [{"question_id": q["question_id"], "answer": None, "client_rev": 6}]})
    state = client.get(f"/v1/attempts/{a['id']}", headers=ready_user).json()
    assert next(x for x in state["questions"] if x["question_id"] == q["question_id"])["answer"] is None


def test_invalid_answers_rejected(client, catalog_seeded, ready_user):
    a = _start(client, ready_user, catalog_seeded[MINI]).json()
    q = next(x for x in a["questions"] if x["type"] == "single")
    r = client.put(f"/v1/attempts/{a['id']}/answers", headers=ready_user,
                   json={"answers": [{"question_id": q["question_id"], "answer": "Z", "client_rev": 1}]})
    assert r.status_code == 422
    r = client.put(f"/v1/attempts/{a['id']}/answers", headers=ready_user,
                   json={"answers": [{"question_id": str(uuid.uuid4()), "answer": "A", "client_rev": 1}]})
    assert r.status_code == 422


def test_writes_after_deadline_rejected_and_auto_submitted(client, catalog_seeded, ready_user, db):
    a = _start(client, ready_user, catalog_seeded[MINI]).json()
    _answer_all(client, ready_user, a)
    att = db.get(Attempt, uuid.UUID(a["id"]))
    att.deadline_at = utcnow() - timedelta(minutes=5)
    db.commit()
    q = a["questions"][0]
    r = client.put(f"/v1/attempts/{a['id']}/answers", headers=ready_user,
                   json={"answers": [{"question_id": q["question_id"], "answer": None, "client_rev": 9}]})
    assert r.status_code == 409 and r.json()["error"]["code"] == "deadline_passed"
    db.expire_all()
    att = db.get(Attempt, uuid.UUID(a["id"]))
    assert att.status == "scored" and att.submit_reason == "timeout"
    assert att.submitted_at <= att.deadline_at


def test_scheduler_auto_submits_expired_attempts(client, catalog_seeded, ready_user, db):
    a = _start(client, ready_user, catalog_seeded[MINI]).json()
    att = db.get(Attempt, uuid.UUID(a["id"]))
    att.deadline_at = utcnow() - timedelta(minutes=1)
    db.commit()
    with SessionLocal() as s:
        assert attempt_svc.auto_submit_expired(s) == 1
    db.expire_all()
    assert db.get(Attempt, uuid.UUID(a["id"])).status == "scored"
    assert db.scalar(select(Report).where(Report.attempt_id == uuid.UUID(a["id"]))).status == "ready"


def test_submit_scores_report_and_double_submit_is_idempotent(client, catalog_seeded, ready_user, db):
    a = _start(client, ready_user, catalog_seeded[MINI]).json()
    _answer_all(client, ready_user, a)
    client.post(f"/v1/attempts/{a['id']}/events", headers=ready_user,
                json={"events": [{"type": "tab_switch"}, {"type": "tab_switch"}, {"type": "copy_attempt"}]})
    s1 = client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user).json()
    s2 = client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user).json()
    assert s1 == s2 and s1["status"] == "scored" and s1["report_status"] == "ready"
    assert db.scalar(select(Report).where(Report.attempt_id == uuid.UUID(a["id"]))) is not None

    rep = client.get(f"/v1/attempts/{a['id']}/report", headers=ready_user).json()
    assert rep["status"] == "ready" and rep["pdf_url"]
    an = rep["analytics"]
    assert an["max_score"] == 30 and an["anti_cheat"]["tab_switch_count"] == 2
    assert rep["report"]["score_summary"]["score"] == s1["score"]  # numbers by code, copied verbatim
    assert len(rep["report"]["study_plan"]) == 7
    refs = {q["ref"] for q in an["questions"]}
    for w in rep["report"]["weaknesses"]:
        assert w["question_refs"] and set(w["question_refs"]) <= refs  # every weakness cites real questions
    assert db.scalar(select(Notification).where(Notification.kind == "result_ready")) is not None

    review = client.get(f"/v1/attempts/{a['id']}/review", headers=ready_user).json()
    assert len(review["questions"]) == 30 and "correct_answer" in review["questions"][0]
    assert client.get(f"/v1/reports/{rep['id']}/pdf", headers=ready_user).content.startswith(b"%PDF")


def test_correct_answers_hidden_until_submitted(client, catalog_seeded, ready_user):
    a = _start(client, ready_user, catalog_seeded[MINI]).json()
    paper = client.get(f"/v1/attempts/{a['id']}/paper", headers=ready_user).json()
    for body in (a, paper):
        assert body["questions"]
        for q in body["questions"]:
            assert not {"correct_answer", "explanation", "shortcut"} & set(q)
            assert not {"correct_answer", "explanation", "shortcut"} & set(q["content"])
    assert client.get(f"/v1/attempts/{a['id']}/review", headers=ready_user).status_code == 409


def test_second_attempt_never_repeats_seen_questions(client, catalog_seeded, ready_user, db):
    grant_credits("9876500001", 2)
    first = _start(client, ready_user, catalog_seeded[MINI]).json()
    client.post(f"/v1/attempts/{first['id']}/submit", headers=ready_user)
    second = _start(client, ready_user, catalog_seeded[MINI]).json()
    assert {q["question_id"] for q in first["questions"]}.isdisjoint({q["question_id"] for q in second["questions"]})
    assert len(list(db.scalars(select(SeenQuestion)))) == 60


def test_language_toggle_content(client, catalog_seeded, ready_user):
    a = _start(client, ready_user, catalog_seeded[MINI], language="ta").json()
    q = a["questions"][0]
    assert q["content"]["language"] == "ta" and q["content_en"]["language"] == "en"
    assert _start(client, ready_user, catalog_seeded["cat"], language="ta").status_code == 422


def test_report_failure_restores_credit(client, catalog_seeded, ready_user, db):
    grant_credits("9876500001", 1)
    a = _start(client, ready_user, catalog_seeded["general-aptitude-reasoning-verbal"]).json()
    assert client.get("/v1/me/credits", headers=ready_user).json()["total"] == 0
    MockProvider.force("exam_report", AIError("down"))
    MockProvider.force("exam_report", AIError("still down"))
    client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user)
    rep = client.get(f"/v1/attempts/{a['id']}/report", headers=ready_user).json()
    assert rep["status"] == "failed" and rep["credit_restored"] is True
    assert client.get("/v1/me/credits", headers=ready_user).json()["total"] == 1
    # Retry works and does not charge again.
    assert client.post(f"/v1/reports/{rep['id']}/retry", headers=ready_user).json()["status"] == "ready"
    assert client.get("/v1/me/credits", headers=ready_user).json()["total"] == 1


def test_report_timeout_sweeper_restores_credit(client, catalog_seeded, ready_user, db):
    grant_credits("9876500001", 1)
    a = _start(client, ready_user, catalog_seeded["general-aptitude-reasoning-verbal"]).json()
    with SessionLocal() as s:  # simulate a stuck job: score but leave the report processing
        att = s.get(Attempt, uuid.UUID(a["id"]))
        att.status, att.submitted_at = "scored", utcnow()
        s.add(Report(user_id=att.user_id, kind="exam", attempt_id=att.id, status="processing", analytics={},
                     created_at=utcnow() - timedelta(minutes=11)))
        s.commit()
    with SessionLocal() as s:
        assert report_svc.sweep_timeouts(s) == 1
        assert report_svc.sweep_timeouts(s) == 0
    assert client.get("/v1/me/credits", headers=ready_user).json()["total"] == 1


def test_rating_share_and_public_view(client, catalog_seeded, ready_user, db):
    a = _start(client, ready_user, catalog_seeded[MINI]).json()
    _answer_all(client, ready_user, a)
    rid = client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user).json()["report_id"]
    assert client.post(f"/v1/reports/{rid}/rating", headers=ready_user, json={"rating": 6}).status_code == 422
    r = client.post(f"/v1/reports/{rid}/rating", headers=ready_user, json={"rating": 2, "comment": "too generic"}).json()
    assert r["user_rating"] == 2
    from app.models import AiLesson
    lesson = db.scalar(select(AiLesson).where(AiLesson.source_ref.like("report_rating:%")))
    assert lesson is not None and lesson.active is False  # untrusted text waits for review

    shared = client.post(f"/v1/reports/{rid}/share", headers=ready_user).json()
    token = shared["share_api_url"].rsplit("/", 1)[1]
    public = client.get(f"/v1/shared/reports/{token}").json()
    assert public["title"] and "Asha" not in str(public) and "question_id" not in str(public)
    assert client.get(f"/v1/shared/reports/{token}/pdf").content.startswith(b"%PDF")
    client.delete(f"/v1/reports/{rid}/share", headers=ready_user)
    assert client.get(f"/v1/shared/reports/{token}").status_code == 404


def test_other_users_cannot_access_attempt_or_report(client, catalog_seeded, ready_user):
    a = _start(client, ready_user, catalog_seeded[MINI]).json()
    rid = client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user).json()["report_id"]
    other = auth_headers(login(client, "9123456780"))
    assert client.get(f"/v1/attempts/{a['id']}", headers=other).status_code == 404
    assert client.get(f"/v1/reports/{rid}", headers=other).status_code == 404


def test_three_reports_quarantine_a_question(client, catalog_seeded, db):
    users = []
    for i in range(3):
        phone = f"98765000{10 + i}"
        h = auth_headers(login(client, phone))
        complete_profile(client, h)
        users.append(h)
    a = _start(client, users[0], catalog_seeded[MINI]).json()
    qid = a["questions"][0]["question_id"]
    # Users can only report questions they were served.
    assert client.post(f"/v1/questions/{qid}/reports", headers=users[1], json={"reason": "wrong_answer"}).status_code == 403
    with SessionLocal() as s:  # serve the same question to the other two users
        for h in users[1:]:
            from app.models import AttemptAnswer, User
            from app.core.security import decode_access_token
            uid = uuid.UUID(decode_access_token(h["Authorization"].split()[1])["sub"])
            src = s.get(Attempt, uuid.UUID(a["id"]))
            att = Attempt(user_id=uid, exam_id=src.exam_id, paper_id=src.paper_id, deadline_at=utcnow(),
                          status="scored", anti_cheat_events=[])
            att.answers.append(AttemptAnswer(question_id=uuid.UUID(qid), seq=1, section_key="quant"))
            s.add(att)
        s.commit()
    for h in users:
        r = client.post(f"/v1/questions/{qid}/reports", headers=h, json={"reason": "wrong_answer", "details": "Key is B"})
        assert r.status_code == 201
    assert client.post(f"/v1/questions/{qid}/reports", headers=users[0], json={"reason": "unclear"}).status_code == 409
    db.expire_all()
    assert db.get(Question, uuid.UUID(qid)).status == "quarantined"
