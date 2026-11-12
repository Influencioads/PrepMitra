"""Student AI features: doubt solver + solution store, photo doubts, tutor deep dives and chat, persona, rank,
notes, topic decks, revision, current affairs, writing evaluator, cheat code coach, admin review, allowances."""

import json
import re
import uuid

import pytest
from sqlalchemy import func, select

from app.ai.provider import MockProvider
from app.db import SessionLocal
from app.models import AiArtifact, AiUsage, Attempt, Question, Solution, User
from tests.conftest import auth_headers, complete_profile, login

MINI = "mini-mock-general-aptitude"
Q = {"text": "A sum of Rs 1,331 is lent at 10% compound interest for 3 years. Find the amount.",
     "options": [{"key": "A", "text": "1771.56"}, {"key": "B", "text": "1700"}, {"key": "C", "text": "1800"},
                 {"key": "D", "text": "1650"}]}


def _ai_calls() -> int:
    with SessionLocal() as s:
        return s.scalar(select(func.count()).select_from(AiUsage)) or 0


def _buy(client, h, code):
    o = client.post("/v1/orders", headers=h, json={"plan_code": code})
    assert o.status_code == 201, o.text
    client.post(f"/v1/orders/{o.json()['order_id']}/mock-pay", headers=h)


def _solution(answer="A", check="1331*1.1**3"):
    return {"answer": answer, "answer_text": "1771.56", "steps": ["A = P(1+r)^n", "1331 x 1.331 = 1771.561"],
            "shortcut": "11^3 = 1331, so multiply by 1.331", "memory_hook": "Chai price rising 10% every year",
            "real_life_example": "An FD at a bank", "common_trap": "Using simple interest",
            "practice_question": {"text": "x", "options": [], "answer": "A", "explanation": "y"},
            "method": "Amount = P(1+r/100)^n", "numeric_check": check}


# ---- doubt solver and the solution store --------------------------------------------------------------------------
def test_doubt_solved_verified_stored_then_served_without_ai(client, catalog_seeded, user_headers):
    MockProvider.force("doubt_solve_math", _solution())
    r = client.post("/v1/ai/doubts", headers=user_headers, json=Q | {"chosen": "B"})
    assert r.status_code == 200, r.text
    out = r.json()
    assert out["source"] == "solved" and out["verified"] and out["answer"] == "A"
    assert out["verification"] == "code_checked"  # 1331 * 1.1^3 = 1771.561 matches option A
    assert "You chose B; the answer is A" in out["personal_note"]
    calls = _ai_calls()
    # Same question with different spacing, case and digits formatting: exact match, no AI call.
    again = client.post("/v1/ai/doubts", headers=user_headers,
                        json=Q | {"text": "a sum of Rs 1331 is lent at 10%  compound interest for 3 years. find the amount."})
    assert again.json()["source"] == "exact" and _ai_calls() == calls
    assert again.json()["solution_id"] == out["solution_id"]
    a = client.get("/v1/me/allowances", headers=user_headers).json()["limits"]["doubts"]
    assert a["used"] == 2 and a["remaining"] == 3  # Free: 5 doubts for life


def test_same_method_new_numbers_recomputed_and_checked_in_code(client, catalog_seeded, user_headers):
    MockProvider.force("doubt_solve_math", _solution())
    first = client.post("/v1/ai/doubts", headers=user_headers, json=Q).json()
    q2 = {"text": Q["text"].replace("1,331", "2,662"),
          "options": [{"key": "A", "text": "3543.22"}, {"key": "B", "text": "3400"}, {"key": "C", "text": "3600"},
                      {"key": "D", "text": "3300"}]}
    MockProvider.force("doubt_same_method", _solution(check="2662*1.1**3") | {"answer_text": "3543.22"})
    out = client.post("/v1/ai/doubts", headers=user_headers, json=q2).json()
    assert out["source"] == "method" and out["verified"] and out["solution_id"] != first["solution_id"]
    with SessionLocal() as s:
        child = s.get(Solution, uuid.UUID(out["solution_id"]))
        assert str(child.parent_id) == first["solution_id"] and child.verification == "code_checked"


def test_disagreement_is_not_stored_on_free_but_escalates_on_pro(client, catalog_seeded, user_headers):
    MockProvider.force("doubt_solve_math", _solution(answer="B", check=""))
    MockProvider.force("doubt_verify", {"answer": "A"})
    out = client.post("/v1/ai/doubts", headers=user_headers, json=Q).json()
    assert out["verified"] is False and out["solution_id"] is None and out["notice"]
    _buy(client, user_headers, "pro_monthly")
    MockProvider.force("doubt_solve_math", _solution(answer="B", check=""))
    MockProvider.force("doubt_verify", {"answer": "A"})
    MockProvider.force("doubt_solve_math", _solution(answer="A"))  # the premium re-solve
    out = client.post("/v1/ai/doubts", headers=user_headers, json=Q).json()
    assert out["verified"] and out["premium_used"] and out["solution_id"]
    lim = client.get("/v1/me/allowances", headers=user_headers).json()["limits"]
    assert lim["premium_doubts"]["used"] == 1


def test_off_topic_and_distress_cost_nothing(client, catalog_seeded, user_headers):
    MockProvider.force("doubt_router", {"on_topic": False, "subject": "math", "difficulty": "easy", "topic": ""})
    r = client.post("/v1/ai/doubts", headers=user_headers, json={"text": "Write my Python homework for sorting a list"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "off_topic"
    r = client.post("/v1/ai/doubts", headers=user_headers, json={"text": "I failed again, I want to die"})
    assert "14416" in r.json()["support"]
    assert client.get("/v1/me/allowances", headers=user_headers).json()["limits"]["doubts"]["used"] == 0


def test_error_reports_hide_a_stored_answer_and_admin_review(client, catalog_seeded, user_headers, admin_headers):
    MockProvider.force("doubt_solve_math", _solution())
    sid = client.post("/v1/ai/doubts", headers=user_headers, json=Q).json()["solution_id"]
    other = auth_headers(login(client, "9123456781"))
    client.post(f"/v1/ai/doubts/{sid}/feedback", headers=user_headers, json={"report_error": True})
    st = client.post(f"/v1/ai/doubts/{sid}/feedback", headers=other, json={"report_error": True}).json()
    assert st["status"] == "hidden"
    queue = client.get("/v1/admin/ai/solutions", headers=admin_headers, params={"status": "hidden"}).json()
    assert queue["items"][0]["id"] == sid
    ok = client.patch(f"/v1/admin/ai/solutions/{sid}", headers=admin_headers, json={"action": "approve"}).json()
    assert ok["status"] == "live" and ok["verification"] == "human"


def test_doubt_in_hindi_is_translated_once_and_stored(client, catalog_seeded, user_headers):
    MockProvider.force("doubt_solve_math", _solution())
    sid = client.post("/v1/ai/doubts", headers=user_headers, json=Q).json()["solution_id"]
    hi = client.post("/v1/ai/doubts", headers=user_headers, json=Q | {"language": "hi"}).json()
    assert hi["language"] == "hi" and hi["source"] == "exact"
    with SessionLocal() as s:
        assert "hi" in s.get(Solution, uuid.UUID(sid)).translations
    calls = _ai_calls()
    client.post("/v1/ai/doubts", headers=user_headers, json=Q | {"language": "hi"})
    assert _ai_calls() == calls


def test_photo_doubt_needs_tutor_pack_and_uses_photo_allowance(client, catalog_seeded, user_headers):
    img = "data:image/jpeg;base64,/9j/4AAQ"
    assert client.post("/v1/ai/doubts/photo", headers=user_headers, json={"image": img}).status_code == 402
    _buy(client, user_headers, "tutor_lite_monthly")
    MockProvider.force("photo_doubt_read", {"readable": True, "question_text": Q["text"], "options": Q["options"]})
    MockProvider.force("doubt_solve_math", _solution())
    out = client.post("/v1/ai/doubts/photo", headers=user_headers, json={"image": img})
    assert out.status_code == 200, out.text
    assert out.json()["answer"] == "A" and out.json()["read_question"]["text"] == Q["text"]
    lim = client.get("/v1/me/allowances", headers=user_headers).json()["limits"]
    assert lim["photo_doubts"]["used"] == 1 and lim["doubts"]["used"] == 0


def test_explain_again(client, catalog_seeded, user_headers):
    MockProvider.force("doubt_solve_math", _solution())
    sid = client.post("/v1/ai/doubts", headers=user_headers, json=Q).json()["solution_id"]
    out = client.post(f"/v1/ai/doubts/{sid}/explain-again", headers=user_headers, json={}).json()
    assert out["answer"] == "A" and out["premium_used"] is False  # Free has no premium allowance


# ---- tutor ---------------------------------------------------------------------------------------------------------
def test_deep_dive_free_sample_then_cache_for_others(client, catalog_seeded, user_headers):
    body = {"mode": "smart", "text": Q["text"], "options": Q["options"]}
    r = client.post("/v1/ai/tutor/deep-dives", headers=user_headers, json=body)
    assert r.status_code == 200 and r.json()["from_cache"] is False
    assert client.post("/v1/ai/tutor/deep-dives", headers=user_headers, json=body).status_code == 402  # 1 sample
    assert client.post("/v1/ai/tutor/deep-dives", headers=user_headers,
                       json=body | {"mode": "master"}).status_code == 402
    other = auth_headers(login(client, "9123456782"))
    calls = _ai_calls()
    hit = client.post("/v1/ai/tutor/deep-dives", headers=other, json=body).json()
    assert hit["from_cache"] is True and _ai_calls() == calls
    assert len(client.get("/v1/ai/tutor/deep-dives", headers=other).json()["items"]) == 1
    pdf = client.get(f"/v1/ai/artifacts/{hit['id']}/pdf", headers=other)
    assert pdf.status_code == 200 and pdf.content.startswith(b"%PDF")
    stranger = auth_headers(login(client, "9123456783"))
    assert client.get(f"/v1/ai/artifacts/{hit['id']}", headers=stranger).status_code == 404


def test_tutor_chat_needs_pack_and_keeps_history(client, catalog_seeded, user_headers):
    assert client.post("/v1/ai/tutor/chat", headers=user_headers, json={"message": "hi"}).status_code == 402
    _buy(client, user_headers, "tutor_lite_monthly")
    r = client.post("/v1/ai/tutor/chat", headers=user_headers, json={"message": "Explain compound interest"}).json()
    sid = r["session_id"]
    assert r["reply"]
    client.post("/v1/ai/tutor/chat", headers=user_headers,
                json={"message": "explain differently", "session_id": sid, "explain_differently": True})
    third = client.post("/v1/ai/tutor/chat", headers=user_headers,
                        json={"message": "still lost", "session_id": sid, "explain_differently": True}).json()
    assert third["premium_used"] is True  # asked to explain differently twice in a row
    hist = client.get("/v1/ai/tutor/chat", headers=user_headers, params={"session_id": sid}).json()["items"]
    assert len(hist) == 6
    sup = client.post("/v1/ai/tutor/chat", headers=user_headers, json={"message": "I can't go on like this"}).json()
    assert sup["support"] and "14416" in sup["reply"]
    assert client.get("/v1/me/allowances", headers=user_headers).json()["limits"]["tutor_chat_turns"]["used"] == 3


# ---- persona, rank, mistakes, revision -------------------------------------------------------------------------------
def _take_mock(client, h, catalog):
    """Answers every question with option A / 1 (so some are wrong and land in the mistake notebook)."""
    a = client.post("/v1/attempts", headers=h, json={"exam_id": str(catalog[MINI])}).json()
    items = [{"question_id": q["question_id"], "client_rev": 1, "time_spent_sec": 30,
              "answer": "A" if q["type"] == "single" else (["A"] if q["type"] == "multi" else 1)}
             for q in a["questions"]]
    client.put(f"/v1/attempts/{a['id']}/answers", headers=h, json={"answers": items})
    client.post(f"/v1/attempts/{a['id']}/submit", headers=h)
    return a


def test_persona_rank_mistakes_and_revision(client, catalog_seeded, ready_user):
    assert client.get("/v1/ai/persona", headers=ready_user).json()["mocks_taken"] == 0
    a = _take_mock(client, ready_user, catalog_seeded)
    p = client.get("/v1/ai/persona", headers=ready_user).json()
    assert p["mocks_taken"] == 1 and p["latest_attempt_id"] == a["id"] and p["ai"]["summary"]
    assert client.get("/v1/ai/persona", headers=ready_user).json()["id"] == p["id"]  # cached until the next mock
    assert client.get("/v1/ai/rank", headers=ready_user, params={"exam_id": str(catalog_seeded[MINI])}).status_code == 402
    assert client.post("/v1/ai/persona/deep", headers=ready_user).status_code == 402
    assert client.post("/v1/ai/revision/today", headers=ready_user, json={}).status_code == 402
    _buy(client, ready_user, "pro_monthly")
    rk = client.get("/v1/ai/rank", headers=ready_user, params={"exam_id": str(catalog_seeded[MINI])}).json()
    assert rk["prepmitra_test_takers"] == 1 and rk["expected_rank_band"][0] == 1
    assert client.post("/v1/ai/persona/deep", headers=ready_user).json()["error"]["code"] == "not_enough_mocks"
    ms = client.get("/v1/ai/mistakes/summary", headers=ready_user)
    assert ms.status_code == 200
    rev = client.post("/v1/ai/revision/today", headers=ready_user, json={"count": 5}).json()
    assert len(rev["questions"]) == 5 and all("hint" in q for q in rev["questions"])


# ---- notes and topic decks ----------------------------------------------------------------------------------------
def test_notes_shared_once_and_personal(client, catalog_seeded, user_headers):
    body = {"topic": "Compound interest", "kind": "formula_sheet"}
    assert client.post("/v1/ai/notes", headers=user_headers, json=body).status_code == 402
    _buy(client, user_headers, "pro_monthly")
    first = client.post("/v1/ai/notes", headers=user_headers, json=body).json()
    again = client.post("/v1/ai/notes", headers=user_headers, json=body).json()
    assert first["from_cache"] is False and again["from_cache"] is True and again["id"] == first["id"]
    personal = client.post("/v1/ai/notes", headers=user_headers, json=body | {"personal": True}).json()
    assert personal["shared"] is False
    assert client.get("/v1/me/allowances", headers=user_headers).json()["limits"]["personal_notes"]["used"] == 2


def test_topic_decks_library_and_custom(client, catalog_seeded, user_headers, admin_headers):
    body = {"topic": "Blood relations"}
    assert client.post("/v1/ai/topic-decks", headers=user_headers, json=body).json()["error"]["code"] == "not_in_library"
    client.post("/v1/admin/ai/library/decks", headers=admin_headers, json=body)
    lib = client.post("/v1/ai/topic-decks", headers=user_headers, json=body).json()  # Free student, free deck
    assert lib["from_cache"] and lib["payload"]["slides"]
    assert client.get("/v1/ai/topic-decks/library", headers=user_headers).json()["items"][0]["title"] == "Blood relations"
    assert client.post("/v1/ai/topic-decks", headers=user_headers, json=body | {"mode": "smart"}).status_code == 402
    _buy(client, user_headers, "pro_monthly")
    custom = client.post("/v1/ai/topic-decks", headers=user_headers, json=body | {"mode": "smart", "language": "hi"}).json()
    assert custom["paid_with"] == "topic_decks" and custom["language"] == "hi"


# ---- writing, current affairs --------------------------------------------------------------------------------------
def test_writing_evaluator(client, catalog_seeded, user_headers):
    body = {"task_type": "essay", "question": "Digital payments in rural India", "word_limit": 250,
            "answer": " ".join(["Digital payments are growing quickly across villages."] * 8)}
    assert client.post("/v1/ai/writing/evaluate", headers=user_headers, json=body).status_code == 402
    _buy(client, user_headers, "pro_monthly")
    MockProvider.force("descriptive_eval", {
        "scores": [{"criterion": c, "score": 7, "comment": "ok"} for c in
                   ("content", "structure", "language", "vocabulary", "relevance")],
        "corrections": [], "strengths": [], "improvements": [], "model_answer": "...", "overall_feedback": "Good"})
    out = client.post("/v1/ai/writing/evaluate", headers=user_headers, json=body).json()
    assert out["payload"]["total_score"] == 70 and out["payload"]["word_count"] == 56
    assert client.post("/v1/ai/writing/evaluate", headers=user_headers,
                       json=body | {"topper_rewrite": True}).status_code == 402  # no Master credits on Pro


def test_current_affairs_fact_checked_and_shared(client, catalog_seeded, user_headers):
    assert client.get("/v1/ai/current-affairs", headers=user_headers).status_code == 402
    _buy(client, user_headers, "pro_monthly")
    MockProvider.force("current_affairs_check", {"items": [{"index": 0, "verified": False}], "quiz": [
        {"index": 0, "verified": True}]})
    out = client.get("/v1/ai/current-affairs", headers=user_headers).json()
    assert out["payload"]["items"] == [] and len(out["payload"]["quiz"]) == 1  # the unverified item was dropped
    assert out["payload"]["dropped_after_fact_check"] == 1
    calls = _ai_calls()
    assert client.get("/v1/ai/current-affairs", headers=user_headers).json()["from_cache"] and _ai_calls() == calls


# ---- cheat code coach ----------------------------------------------------------------------------------------------
def _seed_topic_questions(n=10) -> int:
    with SessionLocal() as s:
        base = s.scalar(select(Question).where(Question.status == "verified", Question.type == "single").limit(1))
        for i in range(n):
            s.add(Question(exam_id=base.exam_id, topic_id=base.topic_id, type="single", difficulty="medium",
                           status="verified", text=f"Coach question {i}: what is {i} + {i}?",
                           options=[{"key": "A", "text": str(2 * i)}, {"key": "B", "text": str(2 * i + 1)}],
                           correct_answer={"value": "A"}, explanation="Add them."))
        s.commit()
        return base.topic_id


def test_cheat_code_coach_spot_shape_test_lock(client, catalog_seeded, ready_user, monkeypatch):
    _take_mock(client, ready_user, catalog_seeded)  # publishes questions
    topic_id = _seed_topic_questions()
    assert client.post("/v1/ai/coach/sessions", headers=ready_user, json={"topic_id": topic_id}).status_code == 402
    _buy(client, ready_user, "starter_monthly")
    start = client.post("/v1/ai/coach/sessions", headers=ready_user, json={"topic_id": topic_id}).json()
    sid = start["session_id"]
    assert len(start["solved_questions"]) == 3 and start["step"] == "shape"
    MockProvider.force("cheat_code_coach", {"reply": "Exact!", "rule_draft": "Double the number", "rule_is_exact": True})
    rep = client.post(f"/v1/ai/coach/sessions/{sid}/reply", headers=ready_user, json={"message": "double it"}).json()
    assert rep["step"] == "test"

    def apply_rule(self, ctx, prompt):  # the mock 'model' applies the rule correctly to every question
        ids = re.findall(r'"question_id": "([0-9a-f-]{36})"', prompt)
        return {"results": [{"question_id": i, "applies": True, "answer": "A", "working": "doubled"} for i in ids]}

    monkeypatch.setattr(MockProvider, "_m_rule_test", apply_rule, raising=False)
    test = client.post(f"/v1/ai/coach/sessions/{sid}/test", headers=ready_user, json={}).json()
    assert test["step"] == "lock" and test["pass_rate"] >= 0.6 and len(test["results"]) == 5
    card = client.post(f"/v1/ai/coach/sessions/{sid}/lock", headers=ready_user, json={"share": True}).json()
    assert card["kind"] == "cheat_card"
    assert client.get("/v1/ai/coach/cards", headers=ready_user).json()["items"][0]["id"] == card["id"]
    lib = client.get("/v1/ai/shortcuts", headers=ready_user).json()["items"]
    assert any(c["id"] == card["id"] for c in lib) == (test["pass_rate"] >= 0.8)


def test_ai_failure_refunds_the_allowance(client, catalog_seeded, user_headers):
    from app.ai.provider import AIError

    MockProvider.force("tutor_smart", AIError("provider down"))
    r = client.post("/v1/ai/tutor/deep-dives", headers=user_headers, json={"mode": "smart", "text": Q["text"]})
    assert r.status_code == 503 and r.json()["error"]["code"] == "ai_unavailable"
    assert client.get("/v1/me/allowances", headers=user_headers).json()["limits"]["smart_credits"]["used"] == 0
