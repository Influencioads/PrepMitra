# AI Personal Exam Mentor

Every student gets a mentor that explains **why** marks were lost, **what** to improve, **how**, **when** to study it
and **what to do next**, until their actual exam date. Numbers are computed by code; the LLM only writes words, and
its words are rejected if they cite a number that is not in the student's data.

## What was reused (no duplicates)

| Requirement | Existing piece used | Added |
|---|---|---|
| Mock submission + scoring | `POST /v1/attempts/{id}/submit`, `services/scoring.py` | scoring now also feeds the mentor (`services/mentor/hooks.py`) |
| Per-question answers, time, marks | `attempt_answers` | — |
| Topic mastery | `user_topic_mastery` | evidence columns (wrong, skipped, time vs target, recent form, sessions, by difficulty) |
| Mistake log | `user_mistakes` (event log, kept) | `mistake_notebook` (one living card per question, spaced revision) |
| Notifications, push, email | `notifications`, `services/notifications.py`, FCM/SMTP adapters | `notification_preferences`, mentor reminder kinds, per-call channel filter |
| Exam patterns, syllabus, weightage | `exam_blueprints`, `topics.weightage` | time targets per section/difficulty (overridable in `marking_scheme.time_targets`) |
| Background jobs | `jobs/queue.py`, `jobs/scheduler.py` | `mentor_replan` job, reminder sweep (every 10 min) |
| AI provider + guards | `ai/provider.py`, `ai/safety.py` | `services/mentor/ai.py` (number grounding check) |

The database is **PostgreSQL** (SQLite for dev/tests), as in the rest of the project; migration `0003_mentor.py`.

## Tables (migration 0003)

`exam_goals` (one per user per exam: date, daily minutes, rest day, plan version and plan notes) ·
`study_tasks` (day-by-day plan; regenerating supersedes pending future tasks only) · `mistake_notebook` ·
`practice_sessions` (quizzes graded once by code) · `notification_preferences` · `mentor_messages` (chat) ·
`mentor_insights` (cached AI wording). Every row has `user_id`; every query filters by the signed-in user.

## Endpoints (all under `/v1`, bearer auth)

| Spec name | Implemented as |
|---|---|
| POST /api/mock-tests/submit | existing `POST /attempts/{id}/submit` |
| GET /api/mock-tests/{id}/analysis | `GET /attempts/{id}/analysis` (+ `/analysis/coach-note`) |
| GET /api/student/performance/dashboard | `GET /me/mentor/dashboard?goal_id=` |
| GET /api/student/topics/weak, /strong | `GET /me/mentor/topics?goal_id=&status=weak\|strong\|pending\|improving` |
| GET /api/student/study-plan | `GET /me/study-plan?goal_id=&start=&end=` |
| POST /api/student/study-plan/generate | `POST /me/study-plan/generate` |
| PUT /api/student/study-plan/tasks/{id} | `PATCH /me/study-plan/tasks/{id}` |
| GET /api/student/exams/countdown | `GET /me/exams/countdown`; goals: `GET/POST /me/exam-goals`, `PATCH/DELETE /me/exam-goals/{id}` |
| GET /api/student/mistake-notebook | `GET /me/mistake-notebook?filter=`, `PATCH /me/mistake-notebook/{id}`, `POST /me/mistake-notebook/bookmarks` |
| (revision quizzes) | `POST /me/practice/mistake-review`, `POST /me/practice/topic-quiz`, `POST /me/practice/{id}/submit` |
| GET /api/student/recommendations | `GET /me/mentor/recommendations` |
| POST /api/student/mentor/chat | `POST /me/mentor/chat`, history `GET /me/mentor/chat` |
| POST /api/student/notifications/preferences | `GET` / `PUT` (or `POST`) `/me/notification-preferences` |

## Rules worth knowing

- **Marks lost** = incorrect (full marks of each wrong question) + negative-marking penalty + unattempted + partial
  shortfall. The split must equal `max_score − score` or the request fails (it is a scoring bug, not rounding).
- **Time**: each question is compared with its target (subject × difficulty, overridable per exam). Bands: on time,
  slow-correct, slow-and-wrong, rushed-wrong, skipped after working, not opened.
- **Evidence threshold**: no topic is called weak or strong below `MENTOR_MIN_EVIDENCE` (8) attempted questions.
  Strong needs medium/hard evidence and a reasonable pace. **Completed (mastered)** needs ≥15 questions in ≥2
  sessions at ≥85% effective accuracy, recent form ≥80% and not declining; it is withdrawn automatically on decline.
  Evidence is pooled across exams for the same subject + topic name.
- **Priority**: high / medium / maintenance / low from status, topic weightage and days left. With ≤10 days left, a
  very weak low-weightage topic may drop to low, always with a written trade-off. Topics are never dropped silently.
- **Plan**: diagnostic mock first if none taken; full mocks every 7/5/3/2 days as the exam nears; sectional test for
  the weakest section; due notebook cards; weekly maintenance quizzes; the rest of the daily minutes go to priority
  topics (concept lesson first for weak/new ones). The last 3 days are revision only, with a light day before the exam.
  The plan is regenerated after every scored mock, on a date/hours change, on demand, and after 3 missed days.
- **Reminders**: morning (countdown milestones replace it that day), afternoon nudge only if nothing is done,
  evening summary only if something is done, missed-days nudge at most every 3 days. Once per kind per local day,
  in a 3-hour window after the student's time, capped at `max_per_day`, nearest exam only.

## Configuration

`MENTOR_MIN_EVIDENCE`, `MENTOR_REVISION_INTERVALS_DAYS` (default `1,3,7,14,30`), `MENTOR_PLAN_HORIZON_DAYS` (60;
later days are added as the plan rolls forward), `MENTOR_CHAT_DAILY_LIMIT`, `MENTOR_REMINDER_INTERVAL_SECONDS`.
Thresholds and default time targets: `backend/app/services/mentor/config.py`.

## Deployment notes

- Run `alembic upgrade head` (0003) before deploying the API. `tzdata` is now in requirements (student-local dates).
- Run the scheduler in exactly one place (`python -m app.worker` with Redis locks in production) so reminders and
  re-plans are not duplicated; the reminder sweep scans users with active goals, so batch it by user id before
  very large scale.
- Mentor chat and coach notes use the existing provider (`AI_PROVIDER=claude`); usage is logged to `ai_usage` under
  `mentor_chat`, `mentor_attempt_note`, `mentor_plan_note`. Without a key, code-written answers are used.
- The local dev server (`scripts/dev_server.py`) now adds new columns to an existing `dev.db` automatically.

## Tests

`backend/tests/test_mentor.py`: marks arithmetic, time bands, evidence/mastery/decline rules, short-time
trade-offs, planner rules (every day covered, final phase, weak topics first, rest day, mock days), the full API
flow (goal → mock → analysis → notebook → revision quiz → dashboard → date change → chat), cross-student isolation,
reminder windows/dedup/cap/preferences, missed-day reflow, and rejection of AI text with invented numbers.
