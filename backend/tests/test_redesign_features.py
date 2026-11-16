"""Redesign features: exam persona profile, cheat codes with drills, blackboard lessons and teach-back.
Everything here is computed or marked by code; none of it spends an AI allowance."""

from app.services.ai_features import cheat_codes, lessons, teach_back
from tests.conftest import grant_credits
from tests.test_ai_features import _take_mock


def test_persona_profile_empty_then_after_mocks(client, catalog_seeded, ready_user):
    p = client.get("/v1/ai/persona/profile", headers=ready_user).json()
    assert p["mocks_taken"] == 0 and p["persona"] is None and len(p["personas"]) == 6

    grant_credits("9876500001", 5)
    _take_mock(client, ready_user, catalog_seeded)
    _take_mock(client, ready_user, catalog_seeded)
    p = client.get("/v1/ai/persona/profile", headers=ready_user).json()
    assert p["mocks_taken"] == 2
    assert p["persona"] in {x["key"] for x in p["personas"]}
    assert set(p["traits"]) == {"speed", "accuracy", "risk", "stamina", "recovery", "consistency"}
    assert all(0 <= v <= 100 for v in p["traits"].values())
    assert p["matches"][0]["key"] == p["persona"] and p["match_percent"] == p["matches"][0]["match"]
    assert len(p["history"]) == 2 and all(isinstance(h["score"], int) for h in p["history"])
    assert len(p["plan"]) == 3 and all(x["code_id"] in cheat_codes.BY_ID for x in p["plan"])
    assert any(e["trait"] == "risk" for e in p["evidence"])


def test_cheat_code_drill_unlocks_at_two_of_three(client, ready_user):
    cat = client.get("/v1/ai/cheat-codes", headers=ready_user).json()
    assert cat["total"] == len(cheat_codes.CODES) and cat["unlocked_count"] == 0
    assert "drill" not in cat["items"][0] and cat["yours"]

    d = client.get("/v1/ai/cheat-codes/ci-1331/drill", headers=ready_user).json()
    assert len(d["questions"]) == 3 and "answer" not in d["questions"][0]

    key = [q["answer"] for q in cheat_codes.BY_ID["ci-1331"]["drill"]]
    wrong = ["D" if k != "D" else "A" for k in key]
    r = client.post("/v1/ai/cheat-codes/ci-1331/drill", headers=ready_user, json={"answers": [key[0], *wrong[1:]]}).json()
    assert r["right"] == 1 and not r["unlocked"]

    r = client.post("/v1/ai/cheat-codes/ci-1331/drill", headers=ready_user, json={"answers": [key[0], key[1], wrong[2]]}).json()
    assert r["right"] == 2 and r["unlocked"] and r["newly_unlocked"]
    cat = client.get("/v1/ai/cheat-codes", headers=ready_user).json()
    assert cat["unlocked_count"] == 1 and cat["yours"][0]["id"] == "ci-1331" and cat["yours"][0]["unlocked"]

    assert client.post("/v1/ai/cheat-codes/nope/drill", headers=ready_user, json={"answers": []}).status_code == 404
    assert client.post("/v1/ai/cheat-codes/ci-1331/drill", headers=ready_user, json={"answers": ["A"]}).status_code == 422


def test_drill_answer_keys_are_valid_options():
    for c in cheat_codes.CODES:
        assert len(c["drill"]) == 3, c["id"]
        for q in c["drill"]:
            assert q["answer"] in {o["key"] for o in q["options"]}, (c["id"], q["text"])
    for lesson in lessons.LESSONS:
        for q in lesson["check"]:
            assert q["answer"] in {o["key"] for o in q["options"]}
    for c in teach_back.CONCEPTS:
        assert len(c["rounds"]) == 3 and all(any(o["good"] for o in r["options"]) for r in c["rounds"])


def test_lessons_pick_check(client, ready_user):
    idx = client.get("/v1/ai/tutor/lessons", headers=ready_user).json()
    assert idx["recommended"] in {x["id"] for x in idx["items"]}
    lesson = client.get("/v1/ai/tutor/lessons/circular-seating", headers=ready_user).json()
    assert len(lesson["steps"]) == 6 and "answer" not in lesson["check"][0]
    ok = client.post("/v1/ai/tutor/lessons/circular-seating/check", headers=ready_user, json={"index": 0, "answer": "A"}).json()
    assert ok["correct"] is True
    bad = client.post("/v1/ai/tutor/lessons/circular-seating/check", headers=ready_user, json={"index": 1, "answer": "D"}).json()
    assert bad["correct"] is False and bad["answer"] == "A"
    assert lessons.pick([{"topic": "Seating Arrangement", "mastery": 25}])[0]["id"] == "circular-seating"


def test_teach_back_rubric(client, ready_user):
    assert client.get("/v1/ai/teach-back", headers=ready_user).json()["items"]
    c = client.get("/v1/ai/teach-back/syllogism-all-some", headers=ready_user).json()
    assert len(c["rounds"]) == 3 and "scores" not in c["rounds"][0]["options"][0]

    good = client.post("/v1/ai/teach-back/syllogism-all-some/answer", headers=ready_user, json={"round": 0, "choice": "B"}).json()
    assert good["good"] and good["scores"]["correctness"] == 10 and good["total"] <= good["max_total"]
    trap = client.post("/v1/ai/teach-back/syllogism-all-some/answer", headers=ready_user, json={"round": 0, "choice": "A"}).json()
    assert not trap["good"] and trap["scores"]["correctness"] == 0

    own = client.post("/v1/ai/teach-back/syllogism-all-some/answer", headers=ready_user,
                      json={"round": 0, "text": "Draw A inside B. C can touch B outside A, so it does not follow — only a possibility."}).json()
    assert own["good"] and own["note"] and own["scores"]["examples"] >= 5
    last = client.post("/v1/ai/teach-back/syllogism-all-some/answer", headers=ready_user, json={"round": 2, "choice": "A"}).json()
    assert last["done"]
    assert client.post("/v1/ai/teach-back/syllogism-all-some/answer", headers=ready_user, json={"round": 0}).status_code == 422
