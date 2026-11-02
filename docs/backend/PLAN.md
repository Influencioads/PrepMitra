# PrepMitra AI — 15-Day MVP Plan

Goal by Day 15: a **demo-ready web MVP** (React + FastAPI + Postgres/pgvector + Claude) covering signup → profile → catalog → timed exam → deterministic score → AI report, plus one text interview with evaluation, a dashboard, basic admin, and tests/docs. Mobile apps, voice and the full 22-language rollout are deferred (see §Deferred) but the architecture keeps room for them.

Status legend: **Not Started · In Progress · Blocked · Done**. The live status is in [TRACKER.md](TRACKER.md).

Estimates assume one developer working with Claude Code, about 8 hours per day.

---

### Day 1: Project setup, configuration, database
- **Features:** Repo layout (`backend/`, `frontend/`, `docs/`), `docker-compose.yml` (Postgres 16 + pgvector), `.env.example`, settings via pydantic-settings, SQLAlchemy models for the full PDF §10 data model, Alembic initial migration, health endpoint, pytest harness with a test DB.
- **FE:** Vite + React + TS scaffold, router, API client with token refresh.
- **BE:** `app/main.py`, `/v1/health`, error handler, CORS.
- **DB:** Migration `0001_initial` (all core tables + `vector` extension).
- **AI:** Provider abstraction (`ClaudeProvider`, `MockProvider`).
- **Tests:** Migration applies on a clean DB; health check; provider mock.
- **Deps:** Docker Desktop running.
- **Est:** 6 h. **DoD:** `alembic upgrade head` succeeds, `pytest` green, frontend dev server loads.

### Day 2: Authentication, profiles, consent
- **Features:** Mobile OTP send/verify (hashed OTP, 5-minute expiry, rate limit, attempt cap), Google sign-in (ID-token verify, active once `GOOGLE_CLIENT_ID` is set), JWT access + rotating refresh tokens, `/v1/me` GET/PATCH/DELETE (soft delete, then purge job), consents (data-use required, recruiter sharing OFF by default), 18+ check, data export (JSON), resume upload (PDF/DOCX ≤ 5 MB, local storage behind a storage interface).
- **FE:** Login (phone + OTP), onboarding/profile form, consent screen, profile page.
- **DB:** Uses users, user_profiles, consents, otp_codes, refresh_tokens.
- **Tests:** OTP happy path, wrong/expired OTP, rate limit, refresh rotation, under-18 rejection, consent recorded, delete account.
- **Blockers:** Real SMS needs a DLT-registered provider. Dev mode returns the OTP only when `APP_ENV=development`.
- **Est:** 8 h. **DoD:** A new user can sign up, consent, complete the profile and log out/in. All auth tests pass.

### Day 3: Catalog, blueprints, seed data
- **Features:** `GET /v1/exams` (category, search, language filters), `GET /v1/exams/{id}` (pattern, sections, duration, marks, negative marking, price, sample question, disclaimer), `GET /v1/interview-roles`, `GET /v1/plans`. Seed: **SSC CGL Tier-1 pattern** blueprint (4 sections × 25 Q, 60 min, +2/−0.5) with topic tree, a 30-min free mini mock, and 6 interview roles with rubrics.
- **FE:** Catalog with search/filter, exam detail and interview role pages.
- **Tests:** Filters, unpublished exams hidden, blueprint JSON validation.
- **Est:** 6 h. **DoD:** The catalog is built only from DB blueprints. Publishing in admin makes an exam appear without a redeploy.

### Day 4: Admin foundation and blueprint management
- **Features:** Role-based admin (`content_manager`, `subject_expert`, `support`, `finance`, `founder`), `/v1/admin/exams` CRUD + publish/hide, blueprint versioning with validation (section counts × marks = total, difficulty mix sums to 100), topics CRUD, audit log on every admin write.
- **FE:** Admin layout, exam/blueprint editor.
- **Tests:** Non-admin gets 403; blueprint validation; audit row written.
- **Est:** 7 h. **DoD:** An admin creates and publishes a new exam end-to-end.

### Day 5: Question bank and AI question pipeline
- **Features:** Generate (strict JSON schema), independent verification solve (answers must match), Python numeric check for numeric answers, embedding dedup (pgvector cosine), tagging, status `verified`/`rejected`, failure log, lesson injection from `ai_lessons`. Paper assembly: bank first, generate only the missing slots, never serve seen questions. Background pre-generation job.
- **AI:** Claude for generate and verify. Embeddings sit behind an interface (local hashing embedder for MVP, swappable for Voyage etc.).
- **Tests:** With the mock provider: a mismatched answer is rejected, a duplicate is rejected, the paper matches the blueprint exactly.
- **Est:** 8 h. **DoD:** `POST /v1/admin/exams/{id}/papers/generate` builds a blueprint-exact paper.

### Day 6: Timed exam engine (backend)
- **Features:** `POST /v1/attempts` (consume credit oldest-expiring-first or the free trial, assign an unseen paper, server `deadline_at`), `GET /v1/attempts/{id}` (resume: answers + server remaining time), `PUT /answers` batched idempotent autosave (rejected after the deadline + grace period), `POST /submit`, auto-submit sweeper for expired attempts, anti-cheat event log, `POST /v1/questions/{id}/reports` with auto-quarantine at 3 reports.
- **Tests:** Resume returns the correct remaining time, writes after the deadline are rejected, auto-submit, no credit → 402, double submit is idempotent.
- **Est:** 8 h. **DoD:** API-level attempt lifecycle fully covered by tests.

### Day 7: Exam UI (CBT-style)
- **Features:** Instructions + language choice, question palette (answered / not answered / marked / not visited), mark for review, clear response, section tabs, server-synced countdown, localStorage + server autosave with retry queue, auto-submit at 0, tab-switch counter, copy-paste disabled, report-question dialog, English toggle (when a translation exists), on-screen calculator only if the blueprint allows it.
- **Tests:** Manual browser run-through; reload mid-exam resumes.
- **Est:** 8 h. **DoD:** A full timed attempt is possible in the browser, including a network drop.

### Day 8: Deterministic scoring and answer review
- **Features:** Scoring service (single MCQ, multi MCQ exact-match, numeric with tolerance), section scores, accuracy, negative-marking loss, time per question, percentile among platform attempts for the same exam, error patterns (careless easy errors, negative-marking guesses, time sinks, skipped sections), user memory updates (topic mastery, mistakes, seen questions). Review page with the correct answer and explanation.
- **Tests:** Table-driven scoring tests incl. negative marks and multi-correct; percentile.
- **Est:** 6 h. **DoD:** Scores are reproducible from stored answers; the AI never sets numbers.

### Day 9: AI exam report
- **Features:** Background report job: analytics + memory profile → Claude (structured JSON template) → strengths, weaknesses (each citing question IDs, validated in code), loopholes, shortcuts (legitimate only), 7-day plan, next test. Written in the user's language. Status processing → ready / failed, with auto-restore of the credit if it fails or takes more than 10 minutes. PDF export (reportlab + Noto fonts), share link (signed token), 1–5 rating.
- **FE:** Report page with polling, rating, PDF download, share.
- **Tests:** Mock provider report; a weakness without a cited question is rejected/repaired; rating endpoint; PDF generated.
- **Est:** 8 h. **DoD:** Report is ready in under 60 s with a real key and downloadable as PDF.

### Day 10: Memory module and question quality
- **Features:** Admin review queue (flagged + 10% random sample), confirm/reject, a confirmed fix writes an `ai_lessons` row with an embedding, lessons retrieved by topic + language into generation prompts, known-bad questions block similar new ones, glossary CRUD.
- **Tests:** Lesson retrieval; quarantine; review flow writes the audit log.
- **Est:** 6 h. **DoD:** A user report can become a lesson that changes later prompts.

### Day 11: Text mock interview
- **Features:** `POST /v1/interviews` (role, level, language, resume text, JD), stage controller (intro → resume → role/technical → situational → HR → closing, 8–12 questions, at least 2 follow-ups), `POST /v1/interviews/{id}/turns` (REST for text MVP; WebSocket reserved for voice), resume within 10 minutes, `POST /end`, transcript saved; prompt-injection-safe prompts (user text wrapped as data, PII stripped).
- **FE:** Chat-style interview screen.
- **Tests:** Stage progression, follow-up count, resume window, ending.
- **Est:** 8 h. **DoD:** A full text interview completes with the transcript stored.

### Day 12: Interview report and dashboard
- **Features:** Interview report (5 rubric scores 1–10 computed by the LLM against the rubric but clamped/validated by code; per-question good/missing/model answer; red flags; 7-day plan), PDF. `GET /v1/me/progress`: history, score trend, topic heatmap, credits + expiry, recommended tests.
- **FE:** Dashboard with charts, interview report page.
- **Est:** 8 h. **DoD:** Dashboard reflects real attempts.

### Day 13: Payments, credits, notifications
- **Features:** Plans, `POST /v1/orders` (Razorpay order in **test mode only**), signature-verified idempotent webhook (`/v1/webhooks/payments/razorpay`), credit ledger grants with expiry, GST invoice (PDF), subscriptions record (auto-renew mandate deferred). Notifications: email via a provider interface (console in dev, SES-ready), in-app notifications for result ready, receipt, expiry in 3 days and 7-day inactivity (scheduled job).
- **Tests:** Bad signature → 400; repeated webhook adds credits once; credit expiry ordering.
- **Blockers:** Razorpay test keys from the owner. Without them, the flow is tested against signed fixtures only.
- **Est:** 8 h. **DoD:** A test-mode purchase grants credits exactly once.

### Day 14: Admin completion, security, i18n, polish
- **Features:** Admin users (search, view, add/restore credits, block), payments list/refund flag, quality dashboard (ratings, flag rate, verification failure rate, AI cost per attempt, report time), interview role editor. Security: rate limits, input validation, OWASP pass, CORS lock-down, security headers. i18n framework (react-i18next) with English + Hindi + Tamil UI strings, Noto fonts, RTL support for Urdu. Policies pages (privacy, terms, refund, AI notice) + "not affiliated" disclaimers.
- **Est:** 8 h. **DoD:** Admin can operate the platform. Security checklist done.

### Day 15: Testing, deployment, documentation
- **Features:** End-to-end API flow test (signup → exam → report → interview), bug bash, production Dockerfiles, compose for prod, `docs/DEPLOYMENT.md`, `docs/FINAL_REPORT.md` (completed, deferred, tests, known issues, risks).
- **Est:** 8 h. **DoD:** A clean checkout runs with the documented commands. All tests green.

---

## Deferred beyond the 15-day MVP (and why)

| Feature | Reason |
|---|---|
| Android & iOS apps (React Native/Expo) | Separate client builds + store review take weeks; the API is client-agnostic so apps can start right after the MVP. |
| Voice interviews (STT/TTS, < 3 s latency) | Needs per-language speech provider evaluation (Bhashini/Sarvam/Google/Azure) and streaming infra; the WebSocket endpoint is reserved. |
| Full 22-language content + native reviewer workflow | Translation pipeline + glossary are built; mass translation and human review need reviewers and budget. MVP ships with English + Hindi + Tamil UI and on-demand question translation. |
| Real SMS OTP (DLT), push (FCM/APNs), SES email | Require provider accounts/DLT registration; interfaces are built with dev providers. |
| Live payments, UPI AutoPay mandates, app-store billing | Need gateway KYC, legal review of store rules; test mode only. |
| Redis-based timers/queues | Server timers use DB deadlines (correct and restart-safe); Redis/RQ can replace the in-process job runner when scaling. |
| S3 storage, India-region cloud deployment, Sentry, backups | Need cloud accounts; storage/monitoring sit behind interfaces with local implementations. |
| Remaining ~14 launch exams | Blueprint-driven: added from admin with no code; MVP seeds one full exam + a mini mock. |
| Descriptive answers, HR talent portal, proctoring | Phase 2/3 per PDF. |
