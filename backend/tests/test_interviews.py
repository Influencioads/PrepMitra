"""AI mock interviews over REST and WebSocket (PDF 5.4, 5.6, 6.3)."""

import uuid
from datetime import timedelta

from sqlalchemy import select

from app.db import SessionLocal, utcnow
from app.models import InterviewRole, InterviewSession, Report
from app.services.interviews import stage_plan
from tests.conftest import grant_credits


def _role(catalog_seeded, slug="software-developer-fresher"):
    with SessionLocal() as s:
        return str(s.scalar(select(InterviewRole).where(InterviewRole.slug == slug)).id)


def _start(client, h, role_id, **kw):
    body = {"role_id": role_id, "level": "fresher", "language": "en", "mode": "text"} | kw
    return client.post("/v1/interviews", headers=h, json=body)


def test_stage_plan():
    plan = stage_plan(10, has_resume=True)
    assert plan[0] == "introduction" and plan[-1] == "closing" and len(plan) == 10
    assert plan.count("resume") == 2 and plan.count("role_technical") == 3
    assert "resume" not in stage_plan(8, has_resume=False)


def test_full_text_interview_with_followups_and_report(client, catalog_seeded, ready_user, db):
    grant_credits("9876500001", 1)
    r = _start(client, ready_user, _role(catalog_seeded),
               resume_text="Built a library app in Django. Phone 9876543210, mail me@x.com",
               job_description="Junior Python developer")
    assert r.status_code == 201, r.text
    s = r.json()
    assert s["transcript"][0]["speaker"] == "interviewer" and s["question_count"] == 1
    sess = db.get(InterviewSession, uuid.UUID(s["id"]))
    assert "9876543210" not in sess.resume_ref and "me@x.com" not in sess.resume_ref  # PII never reaches the LLM

    done, n = False, 0
    while not done:
        n += 1
        out = client.post(f"/v1/interviews/{s['id']}/turns", headers=ready_user,
                          json={"text": f"In my project I designed the database schema and wrote tests for answer {n}."}).json()
        done = out["done"]
        assert n <= 12
    assert out["report_id"]
    state = client.get(f"/v1/interviews/{s['id']}", headers=ready_user).json()
    assert 8 <= state["question_count"] <= 12 and state["followup_count"] >= 2
    followups = [t for t in state["transcript"] if t["is_followup"]]
    assert len(followups) >= 2 and all("You mentioned" in t["text"] for t in followups)
    stages = [t["stage"] for t in state["transcript"] if t["speaker"] == "interviewer"]
    assert stages[0] == "introduction" and "situational" in stages and stages[-1] == "closing"

    rep = client.get(f"/v1/interviews/{s['id']}/report", headers=ready_user).json()
    assert rep["status"] == "ready"
    keys = {x["criterion"] for x in rep["report"]["scores"]}
    assert keys == {"role_knowledge", "answer_structure", "communication", "confidence", "resume_consistency"}
    assert all(1 <= x["score"] <= 10 for x in rep["report"]["scores"])
    assert rep["report"]["per_question"] and len(rep["report"]["study_plan"]) == 7
    assert client.get(f"/v1/reports/{rep['id']}/pdf", headers=ready_user).content.startswith(b"%PDF")


def test_interview_requires_credit_and_valid_level(client, catalog_seeded, ready_user):
    role = _role(catalog_seeded)
    assert _start(client, ready_user, role).status_code == 402
    grant_credits("9876500001", 1)
    assert _start(client, ready_user, role, level="10+").status_code == 422
    assert _start(client, ready_user, role, mode="voice", language="sat").json()["error"]["code"] == "voice_not_available"


def test_end_early_is_evaluated_on_what_was_answered(client, catalog_seeded, ready_user):
    grant_credits("9876500001", 2)
    s = _start(client, ready_user, _role(catalog_seeded)).json()
    client.post(f"/v1/interviews/{s['id']}/turns", headers=ready_user, json={"text": "I am a CS graduate from Pune."})
    end = client.post(f"/v1/interviews/{s['id']}/end", headers=ready_user).json()
    assert end["report_status"] == "ready"
    # Ending with no answers at all restores the credit instead of charging for nothing.
    s2 = _start(client, ready_user, _role(catalog_seeded)).json()
    rep = client.post(f"/v1/interviews/{s2['id']}/end", headers=ready_user).json()
    assert rep["report_status"] == "failed"
    assert client.get("/v1/me/credits", headers=ready_user).json()["total"] == 1


def test_resume_once_within_ten_minutes(client, catalog_seeded, ready_user, db):
    grant_credits("9876500001", 2)
    s = _start(client, ready_user, _role(catalog_seeded)).json()
    sid = uuid.UUID(s["id"])
    sess = db.get(InterviewSession, sid)
    sess.disconnected_at = utcnow() - timedelta(minutes=3)
    db.commit()
    assert client.post(f"/v1/interviews/{s['id']}/resume", headers=ready_user).status_code == 200
    db.expire_all()
    sess = db.get(InterviewSession, sid)
    assert sess.resumes_used == 1 and sess.disconnected_at is None
    sess.disconnected_at = utcnow() - timedelta(minutes=1)
    db.commit()
    r = client.post(f"/v1/interviews/{s['id']}/resume", headers=ready_user)  # second resume is not allowed
    assert r.status_code == 409 and r.json()["error"]["code"] == "interview_ended"

    s2 = _start(client, ready_user, _role(catalog_seeded)).json()
    client.post(f"/v1/interviews/{s2['id']}/turns", headers=ready_user, json={"text": "Hello, I am Asha."})
    sess2 = db.get(InterviewSession, uuid.UUID(s2["id"]))
    sess2.disconnected_at = utcnow() - timedelta(minutes=11)
    db.commit()
    r = client.post(f"/v1/interviews/{s2['id']}/resume", headers=ready_user)
    assert r.status_code == 409
    assert db.scalar(select(Report).where(Report.interview_session_id == sess2.id)).status == "ready"


def test_websocket_text_and_voice_flow(client, catalog_seeded, ready_user, db):
    grant_credits("9876500001", 1)
    s = _start(client, ready_user, _role(catalog_seeded), mode="voice", language="hi").json()
    token = ready_user["Authorization"].split()[1]
    import base64

    with client.websocket_connect(f"/v1/interviews/{s['id']}/stream?token={token}") as ws:
        first = ws.receive_json()
        assert first["type"] == "state" and first["interview"]["mode"] == "voice"
        ws.send_json({"type": "ping"})
        assert ws.receive_json()["type"] == "pong"
        ws.send_json({"type": "answer", "text": "Um, I basically built a matlab tool", "duration_sec": 6})
        q = ws.receive_json()
        assert q["type"] == "question" and q["tts"] == "client" and q["turn"]["speaker"] == "interviewer"
        # Voice: audio chunks then audio_end -> transcript -> next question.
        ws.send_json({"type": "audio_chunk", "data": base64.b64encode(b"I led a team of three").decode()})
        ws.send_json({"type": "audio_end", "duration_sec": 4})
        assert ws.receive_json() == {"type": "transcript", "text": "I led a team of three"}
        assert ws.receive_json()["type"] == "question"
        ws.send_json({"type": "end"})
        ended = ws.receive_json()
        assert ended["type"] == "ended" and ended["report_id"]
    rep = client.get(f"/v1/interviews/{s['id']}/report", headers=ready_user).json()
    vm = rep["report"]["voice_metrics"]
    assert vm["filler_count"] >= 2 and vm["words_per_minute"] == 78.0  # 13 words in 10 s


def test_websocket_rejects_bad_token(client, catalog_seeded, ready_user):
    grant_credits("9876500001", 1)
    s = _start(client, ready_user, _role(catalog_seeded)).json()
    with client.websocket_connect(f"/v1/interviews/{s['id']}/stream?token=bad") as ws:
        msg = ws.receive_json()
        assert msg["type"] == "error" and msg["code"] == "invalid_token"


def test_websocket_disconnect_marks_session(client, catalog_seeded, ready_user, db):
    grant_credits("9876500001", 1)
    s = _start(client, ready_user, _role(catalog_seeded)).json()
    token = ready_user["Authorization"].split()[1]
    with client.websocket_connect(f"/v1/interviews/{s['id']}/stream?token={token}") as ws:
        ws.receive_json()
    db.expire_all()
    assert db.get(InterviewSession, uuid.UUID(s["id"])).disconnected_at is not None
