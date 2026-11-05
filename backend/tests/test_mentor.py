"""AI Personal Exam Mentor: analysis arithmetic, evidence rules, planner rules, the API flow, isolation, reminders,
and the check that rejects AI text citing numbers that are not in the student's data."""

import uuid
from datetime import date, datetime, timedelta

from sqlalchemy import select

from app.ai.provider import MockProvider
from app.db import SessionLocal
from app.models import Attempt, ExamGoal, NotebookEntry, Notification, StudyTask, User, UserTopicMastery
from app.services.mentor import analysis, chat, clock, mastery, planner, reminders
from app.services.mentor import config as cfg
from app.services.mentor.ai import unsupported_numbers
from tests.conftest import auth_headers, complete_profile, login

MINI = "mini-mock-general-aptitude"


# ---- module 1: marks lost add up, no double counting --------------------------------------------------------------
def _row(status, full=1.0, neg=0.25, t=30, target=40, diff="medium", topic="Percentage"):
    awarded = {"correct": full, "wrong": -neg, "unanswered": 0.0}[status]
    return {"status": status, "full_marks": full, "awarded": awarded, "not_earned": full - max(awarded, 0),
            "penalty": max(-awarded, 0), "marks_lost": full - awarded, "time_sec": t, "target_sec": target,
            "time_ratio": t / target, "band": analysis._band(status, t, target), "difficulty": diff, "topic": topic,
            "topic_id": 1, "section_key": "quant", "ref": 0}


def test_marks_breakdown_matches_score_exactly():
    rows = [_row("correct")] * 82 + [_row("wrong")] * 8 + [_row("unanswered", t=0)] * 10
    score = sum(r["awarded"] for r in rows)
    assert score == 80.0
    b = analysis.marks_breakdown(rows, 100.0, score)
    items = {i["reason"]: i["marks"] for i in b["items"]}
    assert b["total_lost"] == 20.0
    assert items == {"incorrect_answers": 8.0, "negative_marking": 2.0, "unattempted": 10.0}
    assert b["gross_lost_before_penalty"] == 18.0
    assert sum(items.values()) == b["total_lost"]


def test_time_bands_and_observations_use_targets():
    assert cfg.target_time({}, "numerical", "hard", 60) == cfg.DEFAULT_TIME_TARGETS["quant"]["hard"]
    assert cfg.target_time({"time_targets": {"quant": {"hard": 120}}}, "quant", "hard", 60) == 120
    slow_wrong = _row("wrong", t=180, target=60, topic="Puzzles")
    slow_wrong["ref"] = 4
    assert slow_wrong["band"] == "time_sink"
    assert _row("wrong", t=5, target=60)["band"] == "rushed_wrong"
    assert _row("unanswered", t=45, target=60)["band"] == "skipped_after_time"
    quick = [dict(_row("correct", t=20, target=60, topic="Simplification"), ref=i, topic_id=2) for i in (1, 2)]
    rows = [slow_wrong] + quick
    obs = analysis.time_observations(rows, [{"key": "quant", "name": "Quant"}], analysis.topic_table(rows))
    texts = " ".join(o["text"] for o in obs)
    assert "3 min 0 s on a Puzzles question (Q4, target 60 seconds)" in texts
    assert any(o["kind"] == "strength" and "Simplification" in o["text"] for o in obs)


# ---- module 3/4: evidence threshold, mastery, decline -------------------------------------------------------------
def _ev(attempted, correct, sessions=1, recent=None, prev=None, diff=None, time=0, target=0):
    return {"attempted": attempted, "correct": correct, "wrong": attempted - correct, "skipped": 0, "time": time,
            "target": target, "sessions": sessions, "by_difficulty": diff or {"medium": [attempted, correct]},
            "recent": recent, "previous_recent": prev, "last_seen_at": None}


def test_no_verdict_from_one_or_two_questions():
    assert mastery.classify(_ev(2, 0))["status"] == "insufficient_data"
    assert mastery.classify(_ev(3, 3))["status"] == "insufficient_data"
    assert mastery.classify(None)["status"] == "not_started"
    assert mastery.classify(_ev(12, 4))["status"] == "very_weak"


def test_mastery_needs_volume_sessions_and_hard_evidence():
    one_session = mastery.classify(_ev(20, 19, sessions=1))
    assert one_session["status"] == "strong" and not one_session["mastered"]
    mastered = mastery.classify(_ev(20, 19, sessions=3, recent=0.95, prev=0.9))
    assert mastered["mastered"] and mastered["confidence"] == "high"
    easy_only = mastery.classify(_ev(20, 20, sessions=3, recent=1.0, diff={"easy": [20, 20]}))
    assert easy_only["status"] == "good" and not easy_only["mastered"]
    slow = mastery.classify(_ev(20, 19, sessions=3, recent=0.95, time=2000, target=1000))
    assert slow["status"] == "good" and "Accurate but slow" in slow["notes"]


def test_decline_brings_a_mastered_topic_back_into_the_plan():
    declined = mastery.classify(_ev(30, 27, sessions=4, recent=0.6, prev=0.9))
    assert declined["trend"] == "declining" and not declined["mastered"]
    t = {"topic_id": 1, "name": "Percentage", "relevance": 1.0, "weightage": 2, **declined}
    assert mastery.prioritise([t], 20)[0]["priority"] in ("medium", "high")


def test_short_time_tradeoff_is_explained_not_silent():
    weak_minor = {"topic_id": 1, "name": "Partnership", "relevance": 0.3, "weightage": 1,
                  **mastery.classify(_ev(10, 2))}
    weak_major = {"topic_id": 2, "name": "Data interpretation", "relevance": 1.0, "weightage": 3,
                  **mastery.classify(_ev(10, 2))}
    out = {t["name"]: t for t in mastery.prioritise([weak_minor, weak_major], 6)}
    assert out["Data interpretation"]["priority"] == "high"
    assert out["Partnership"]["priority"] == "low" and "not dropped" in out["Partnership"]["tradeoff"]
    later = {t["name"]: t for t in mastery.prioritise([dict(weak_minor), dict(weak_major)], 40)}
    assert later["Partnership"]["priority"] == "medium" and later["Partnership"]["tradeoff"] is None


# ---- module 6: planner rules --------------------------------------------------------------------------------------
def _topics():
    raw = [("Time and work", "quant", _ev(10, 3)), ("Reading comprehension", "english", _ev(10, 4)),
           ("Data interpretation", "quant", _ev(10, 6)), ("Syllogism", "reasoning", _ev(20, 19, 3, 0.95, 0.9)),
           ("Puzzles", "reasoning", None)]
    ts = [{"topic_id": i, "name": n, "section_key": s, "subject": cfg.subject_of(s), "relevance": 1.0, "weightage": 2,
           **mastery.classify(e)} for i, (n, s, e) in enumerate(raw, start=1)]
    return mastery.prioritise(ts, 20)


def _schedule(days=20, mocks_done=1, rest=None, minutes=180):
    start = date(2027, 1, 5)
    return start, planner.build_schedule(
        start=start, exam_date=start + timedelta(days=days), daily_minutes=minutes, rest_weekday=rest,
        topics=_topics(), mock_minutes=60, sections=[{"key": "quant", "name": "Quant", "duration_min": 20},
                                                     {"key": "english", "name": "English", "duration_min": 20}],
        subjects_acc={"quant": 0.45, "english": 0.4}, mocks_done=mocks_done, notebook_active=5, notebook_due=2)


def test_plan_covers_every_day_and_ends_with_revision_only():
    start, tasks = _schedule()
    days = sorted({t["task_date"] for t in tasks})
    assert days[0] == start and days[-1] == start + timedelta(days=19) and len(days) == 20
    final = [t for t in tasks if t["task_date"] >= start + timedelta(days=17)]
    assert not [t for t in final if t["kind"] in ("learn", "practice")]
    assert any(t["kind"] == "rest" for t in final if t["task_date"] == start + timedelta(days=19))
    assert any(t["kind"] == "mock_test" for t in final if t["task_date"] == start + timedelta(days=17))


def test_plan_puts_weak_topics_first_and_completed_topics_on_maintenance():
    _, tasks = _schedule()
    focus = [t for t in tasks if t["kind"] in ("learn", "practice")]
    names = {t["title"].split(":")[0] for t in focus}
    assert {"Time and work", "Reading comprehension", "Puzzles"} <= names
    assert "Syllogism" not in names
    assert any(t["kind"] == "revision" and t["title"].startswith("Syllogism") for t in tasks)
    assert next(t for t in focus if t["title"].startswith("Puzzles"))["kind"] == "learn"  # not started: concepts first


def test_mock_days_use_spare_time_for_one_topic():
    _, tasks = _schedule(minutes=180)
    mock_days = {t["task_date"] for t in tasks if t["kind"] == "mock_test"}
    normal_mock_day = min(d for d in mock_days if (date(2027, 1, 25) - d).days > cfg.FINAL_PHASE_DAYS)
    kinds = [t["kind"] for t in tasks if t["task_date"] == normal_mock_day]
    assert kinds[:2] == ["mock_test", "mock_review"]
    assert sum(1 for k in kinds if k in ("learn", "practice", "revision")) == 1


def test_plan_respects_budget_rest_day_and_diagnostic_mock():
    start, tasks = _schedule(mocks_done=0, rest=6)
    assert tasks[0]["kind"] == "mock_test" and "Diagnostic" in tasks[0]["title"]
    for d in {t["task_date"] for t in tasks}:
        day = [t for t in tasks if t["task_date"] == d]
        if d.weekday() == 6 and (start + timedelta(days=20) - d).days > cfg.FINAL_PHASE_DAYS:
            assert [t["kind"] for t in day] == ["rest"]
        if not any(t["kind"] == "mock_test" for t in day):
            assert sum(t["minutes"] for t in day) <= 180


# ---- the full API flow --------------------------------------------------------------------------------------------
def _take_mock(client, h, exam_id):
    a = client.post("/v1/attempts", headers=h, json={"exam_id": str(exam_id), "language": "en"}).json()
    items = []
    for i, q in enumerate(a["questions"]):
        if i % 3 == 2:
            continue  # leave some unanswered
        ans = q["content"]["options"][0]["key"] if q["type"] == "single" else (["A"] if q["type"] == "multi" else 1)
        items.append({"question_id": q["question_id"], "answer": ans, "client_rev": 1,
                      "time_spent_sec": 200 if i % 5 == 0 else 20})
    client.put(f"/v1/attempts/{a['id']}/answers", headers=h, json={"answers": items})
    assert client.post(f"/v1/attempts/{a['id']}/submit", headers=h).status_code == 200
    return a["id"]


def test_mentor_end_to_end(client, catalog_seeded, ready_user):
    h = ready_user
    exam_date = (clock.today() + timedelta(days=20)).isoformat()
    r = client.post("/v1/me/exam-goals", headers=h, json={"exam_id": MINI, "exam_date": exam_date,
                                                          "daily_minutes": 150})
    assert r.status_code == 201, r.text
    goal = r.json()
    assert goal["days_remaining"] == 20 and goal["weeks_remaining"] == 2 and goal["plan"]["mocks_done"] == 0
    plan = client.get("/v1/me/study-plan", headers=h, params={"goal_id": goal["goal_id"]}).json()
    first = plan["days"][0]["tasks"][0]
    assert first["kind"] == "mock_test" and first["status"] == "pending"
    assert client.post("/v1/me/exam-goals", headers=h, json={"exam_id": MINI, "exam_date": exam_date}).status_code == 409

    attempt_id = _take_mock(client, h, catalog_seeded[MINI])
    an = client.get(f"/v1/attempts/{attempt_id}/analysis", headers=h).json()
    lost = sum(i["marks"] for i in an["marks_lost"]["items"])
    assert abs(lost - (an["max_score"] - an["score"])) < 0.01 and an["marks_lost"]["total_lost"] == round(lost, 2)
    assert sum(s["scored"] for s in an["sections"]) == an["score"]
    assert len(an["time"]["questions"]) == an["counts"]["questions"] == 30
    note = client.get(f"/v1/attempts/{attempt_id}/analysis/coach-note", headers=h).json()
    assert note["source"] in ("ai", "code") and note["note"]

    plan = client.get("/v1/me/study-plan", headers=h, params={"goal_id": goal["goal_id"]}).json()
    assert plan["plan_version"] == 2  # re-planned after the mock
    assert plan["days"][0]["tasks"][0]["status"] == "done"  # the planned mock is ticked off

    nb = client.get("/v1/me/mistake-notebook", headers=h).json()
    assert nb["total"] > 0 and nb["counts"]["wrong"] > 0
    entry = nb["items"][0]
    assert entry["correct_answer"] is not None and entry["explanation"] is not None
    patched = client.patch(f"/v1/me/mistake-notebook/{entry['id']}", headers=h,
                           json={"mistake_type": "calculation", "bookmarked": True}).json()
    assert patched["mistake_type"] == "calculation" and patched["mistake_type_source"] == "student"

    quiz = client.post("/v1/me/practice/mistake-review", headers=h, json={"count": 3}).json()
    assert len(quiz["questions"]) == 3 and "correct_answer" not in quiz["questions"][0]
    with SessionLocal() as s:
        ids = [uuid.UUID(q["question_id"]) for q in quiz["questions"]]
        from app.models import Question

        right = {str(q.id): q.correct_answer["value"] for q in s.scalars(select(Question).where(Question.id.in_(ids)))}
    res = client.post(f"/v1/me/practice/{quiz['id']}/submit", headers=h, json={"answers": [
        {"question_id": qid, "answer": ans, "time_spent_sec": 30} for qid, ans in right.items()]}).json()
    assert res["correct"] == 3
    again = client.post(f"/v1/me/practice/{quiz['id']}/submit", headers=h, json={"answers": []})
    assert again.status_code == 409
    with SessionLocal() as s:
        reviewed = s.scalars(select(NotebookEntry).where(NotebookEntry.id.in_(
            [q["entry_id"] for q in quiz["questions"]]))).all()
        assert all(e.box == 1 and e.revision_correct == 1 for e in reviewed)

    dash = client.get("/v1/me/mentor/dashboard", headers=h).json()
    sel = dash["selected"]
    assert sel["exam"]["days_remaining"] == 20 and sel["mock_tests"]["tests_completed"] == 1
    assert 0 <= sel["coverage"]["syllabus_completion_pct"] <= 100
    assert sel["recommendations"]["mock_test"]["advice"] in ("yes", "not_yet")
    topics = client.get("/v1/me/mentor/topics", headers=h, params={"goal_id": goal["goal_id"]}).json()
    assert topics["min_evidence"] == cfg.min_evidence() and topics["items"]
    assert all(t["status"] in ("not_started", "insufficient_data") or t["attempted"] >= cfg.min_evidence()
               for t in topics["items"])

    task = next(t for d in plan["days"] for t in d["tasks"] if t["status"] == "pending" and t["kind"] != "rest")
    done = client.patch(f"/v1/me/study-plan/tasks/{task['id']}", headers=h, json={"status": "done",
                                                                                  "actual_minutes": 25}).json()
    assert done["status"] == "done"

    moved = client.patch(f"/v1/me/exam-goals/{goal['goal_id']}", headers=h,
                         json={"exam_date": (clock.today() + timedelta(days=10)).isoformat()}).json()
    assert moved["days_remaining"] == 10 and moved["plan"]["days_left"] == 10
    plan = client.get("/v1/me/study-plan", headers=h, params={"goal_id": goal["goal_id"]}).json()
    assert max(d["date"] for d in plan["days"]) < (clock.today() + timedelta(days=10)).isoformat()

    reply = client.post("/v1/me/mentor/chat", headers=h, json={"message": "How many days are left for my exam?"}).json()
    assert "10 days" in reply["content"]
    reply = client.post("/v1/me/mentor/chat", headers=h, json={"message": "Where am I losing marks?"}).json()
    assert f"{an['score']:g}" in reply["content"]
    assert len(client.get("/v1/me/mentor/chat", headers=h).json()["items"]) == 4


def test_students_cannot_see_each_others_mentor_data(client, catalog_seeded, ready_user):
    exam_date = (clock.today() + timedelta(days=15)).isoformat()
    goal = client.post("/v1/me/exam-goals", headers=ready_user, json={"exam_id": MINI, "exam_date": exam_date}).json()
    attempt_id = _take_mock(client, ready_user, catalog_seeded[MINI])
    entry = client.get("/v1/me/mistake-notebook", headers=ready_user).json()["items"][0]
    other = auth_headers(login(client, "9876500002"))
    complete_profile(client, other)
    assert client.get(f"/v1/attempts/{attempt_id}/analysis", headers=other).status_code == 404
    assert client.get("/v1/me/study-plan", headers=other, params={"goal_id": goal["goal_id"]}).status_code == 404
    assert client.patch(f"/v1/me/mistake-notebook/{entry['id']}", headers=other, json={"bookmarked": True}).status_code == 404
    assert client.get("/v1/me/mistake-notebook", headers=other).json()["total"] == 0
    with SessionLocal() as s:
        task = s.scalar(select(StudyTask).where(StudyTask.goal_id == goal["goal_id"]))
    assert client.patch(f"/v1/me/study-plan/tasks/{task.id}", headers=other, json={"status": "done"}).status_code == 404
    assert client.get("/v1/me/mentor/dashboard", headers=other).json() == {"goals": [], "selected": None}


def test_goal_validation(client, catalog_seeded, ready_user):
    past = (clock.today() - timedelta(days=1)).isoformat()
    r = client.post("/v1/me/exam-goals", headers=ready_user, json={"exam_id": MINI, "exam_date": past})
    assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_exam_date"
    r = client.post("/v1/me/exam-goals", headers=ready_user, json={"exam_id": "no-such-exam",
                                                                    "exam_date": (clock.today() + timedelta(days=9)).isoformat()})
    assert r.status_code == 404


# ---- module 9: reminders ------------------------------------------------------------------------------------------
def test_reminders_respect_window_dedup_cap_and_preferences(client, catalog_seeded, ready_user):
    exam_date = (clock.today() + timedelta(days=7)).isoformat()
    client.post("/v1/me/exam-goals", headers=ready_user, json={"exam_id": MINI, "exam_date": exam_date})
    prefs = client.put("/v1/me/notification-preferences", headers=ready_user,
                       json={"morning_time": "07:00", "email_enabled": False, "max_per_day": 2}).json()
    assert prefs["morning_time"] == "07:00" and prefs["max_per_day"] == 2
    bad = client.put("/v1/me/notification-preferences", headers=ready_user, json={"morning_time": "7am"})
    assert bad.status_code == 422

    tz = clock.tz("Asia/Kolkata")
    day = clock.today()
    with SessionLocal() as s:
        user = s.scalar(select(User).where(User.phone == "+919876500001"))
        early = datetime.combine(day, datetime.min.time(), tz).replace(hour=6)
        assert reminders.remind_user(s, user, early) == []
        morning = early.replace(hour=7, minute=10)
        ids = reminders.remind_user(s, user, morning)
        s.commit()
        assert len(ids) == 1
        n = s.get(Notification, ids[0])
        assert n.kind == "mentor_countdown" and "7 days" in n.title and "email" not in n.channels
        assert reminders.remind_user(s, user, morning + timedelta(minutes=30)) == []  # once per day
        assert len(reminders.remind_user(s, user, morning.replace(hour=16, minute=5))) == 1  # afternoon nudge
        s.commit()
        assert reminders.remind_user(s, user, morning.replace(hour=20, minute=40)) == []  # cap of 2 reached


def test_missed_days_reflow_the_plan(client, catalog_seeded, ready_user):
    exam_date = (clock.today() + timedelta(days=25)).isoformat()
    goal = client.post("/v1/me/exam-goals", headers=ready_user, json={"exam_id": MINI, "exam_date": exam_date}).json()
    with SessionLocal() as s:
        g = s.get(ExamGoal, goal["goal_id"])
        for t in s.scalars(select(StudyTask).where(StudyTask.goal_id == g.id)):
            t.task_date = t.task_date - timedelta(days=4)  # pretend the plan started 4 days ago, nothing done
        s.commit()
        user = s.get(User, g.user_id)
        at = datetime.combine(clock.today(), datetime.min.time(), clock.tz("Asia/Kolkata")).replace(hour=8)
        ids = reminders.remind_user(s, user, at)
        s.commit()
        assert [s.get(Notification, i).kind for i in ids] == ["mentor_missed"]
        assert s.get(ExamGoal, g.id).plan_version == 2


# ---- module 13: AI output is checked against the data --------------------------------------------------------------
def test_invented_numbers_are_rejected():
    facts = {"score": 72, "max_score": 100, "accuracy": 0.81, "time_sec": 150}
    assert unsupported_numbers("You scored 72 out of 100 with 81% accuracy, 2 min 30 s.", facts) == []
    assert unsupported_numbers("You scored 72 and can reach 95 next week.", facts) == ["95"]


def test_chat_falls_back_when_the_model_invents_numbers(client, catalog_seeded, ready_user):
    exam_date = (clock.today() + timedelta(days=12)).isoformat()
    client.post("/v1/me/exam-goals", headers=ready_user, json={"exam_id": MINI, "exam_date": exam_date})
    MockProvider.force("mentor_chat", {"answer": "You have 99 days and 87% accuracy.", "follow_ups": []})
    MockProvider.force("mentor_chat", {"answer": "You have 98 days left.", "follow_ups": []})
    r = client.post("/v1/me/mentor/chat", headers=ready_user, json={"message": "How many days are left?"}).json()
    assert r["source"] == "code" and "12 days" in r["content"]
    MockProvider.force("mentor_chat", {"answer": "Your exam is in 12 days. Start with a mock.", "follow_ups": ["Why?"]})
    r = client.post("/v1/me/mentor/chat", headers=ready_user, json={"message": "How many days are left?"}).json()
    assert r["source"] == "ai" and r["follow_ups"] == ["Why?"]


def test_scoring_updates_topic_evidence_without_counting_unseen_questions(client, catalog_seeded, ready_user):
    _take_mock(client, ready_user, catalog_seeded[MINI])
    with SessionLocal() as s:
        a = s.scalar(select(Attempt))
        rows = s.scalars(select(UserTopicMastery).where(UserTopicMastery.user_id == a.user_id)).all()
        answered = sum(1 for x in a.answers if x.answer is not None)
        assert sum(m.attempts_count for m in rows) == answered
        assert all(m.sessions_count == 1 and m.recent_accuracy is not None for m in rows if m.attempts_count)
        assert sum(m.time_spent_sec for m in rows) > 0 and sum(m.target_time_sec for m in rows) > 0
