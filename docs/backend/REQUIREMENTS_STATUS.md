# Backend status — 15-day plan and MVP PDF

Sources: `PrepMitra_15_Day_Plan_Frontend_Backend.xlsx` (Backend Developer rows + API Plan) and `Exam app.pdf`.
Updated 2026-10-31. **The 115 automated tests pass** (`cd backend && .venv/Scripts/python -m pytest`).

Legend: **Done** = built and covered by tests · **Done, needs your input** = code complete, waiting on an account,
key or decision from you · **Not done** = cannot be done from code alone (explained).

## 1. Backend tasks from the 15-day plan

| Day | Task | Status | Where / notes |
|---|---|---|---|
| 1 | Backend project setup, `/health`, Dockerfile, .env | Done | `backend/`, `GET /v1/health`, `backend/Dockerfile`, `.env.example` |
| 1 | Database schema v1 + Alembic | Done | 35 tables; migrations `0001`, `0002`; tested to cover every table |
| 1 | API contract + Swagger | Done | `/docs`, [API.md](API.md), [SWAGGER_TESTING.md](SWAGGER_TESTING.md) |
| 2 | Login: verify Firebase token, `POST /v1/auth/session` | Done, needs your input | Set `FIREBASE_PROJECT_ID`. Every API also accepts the Firebase ID token. Backend OTP + Google remain for dev/Swagger. |
| 2 | Profile, consent, delete-account APIs | Done | `/v1/me`, `/v1/me/consents`, 18+ check, DPDP export |
| 2 | 3 exam blueprints, 2 roles, catalog APIs | Done | Launch seed: SSC CGL Tier 1, IBPS PO Prelims, Campus Placement Aptitude + free mini mock; Software Developer (Fresher) + Bank PO. The other 11 exams / 4 roles are seeded as drafts. |
| 3 | Claude API layer (retries, timeouts, JSON, cost log) | Done, needs your input | `app/ai/provider.py`; strict JSON output, refusal fallback, per-call tokens in `ai_usage`. Needs `ANTHROPIC_API_KEY` + `AI_PROVIDER=claude`. |
| 3 | Question generation prompt + schema validation | Done | `app/ai/prompts.py`, `app/ai/schemas.py`, `question_pipeline.py` |
| 3 | Independent answer verification + Python maths check | Done | Second solve must match; `numeric_check` evaluated in a sandboxed evaluator; failures logged |
| 4 | Question bank builder (background job) | Done | `POST /v1/admin/exams/{id}/bank/build`, `python -m app.services.bank --exam … --per-topic …`; reports pass rate and ₹ per question. Dedup uses vector similarity (pgvector) instead of pg_trgm; it also blocks known-bad questions. |
| 4 | Paper assembly exactly per blueprint, no repeats | Done | `papers.py`; blueprint check enforced in code and tests |
| 4 | Run the SSC CGL bank overnight (400+ questions) | Not done | Needs the Claude key, then one command (see §3). Content work, not code. |
| 5 | Start attempt + paper APIs (credits / free mini mock) | Done | `POST /v1/attempts`, `GET /v1/attempts/{id}/paper`; answers never sent before submit |
| 5 | Autosave, events, submit, auto-submit, resume | Done | Idempotent `client_rev` autosave; scheduler auto-submits every 15 s |
| 5 | Deploy backend to staging (AWS Mumbai, CI) | Done, needs your input | `docker-compose.yml --profile full`, `Dockerfile`, CI `.github/workflows/backend.yml` (tests on Postgres + pgvector). Needs AWS account to deploy. |
| 6 | Scoring engine (code, not AI) | Done | `scoring.py`: negative marking, sections, accuracy, time, topics, percentile, error patterns |
| 6 | AI report generation (cites questions, user's language) | Done | `reports.py`; code validates every weakness cites questions, 7-day plan, real next test |
| 6 | Report status API (background job) | Done | `GET /v1/attempts/{id}/report` processing → ready; auto credit restore after 10 min |
| 7 | Question review API | Done | `GET /v1/attempts/{id}/review` in the attempt's language |
| 7 | Rating + "report this question" (hide after 3 flags) | Done | `POST /v1/reports/{id}/rating`, `POST /v1/questions/{id}/flags`; auto-quarantine at 3 users |
| 7 | Banks for IBPS PO and Placement Aptitude | Not done | Same command as Day 4, after the Claude key |
| 7 | Report speed/cost tuning (< 60 s) | Done (instrumented) | `generation_ms` per report; p50/p95 in `/v1/admin/stats`. Real timing needs the Claude key. |
| 8 | Razorpay orders + verification | Done, needs your input | `POST /v1/orders`, `POST /v1/orders/verify`; mock gateway until Razorpay test keys are set |
| 8 | Webhook + credit ledger (90-day expiry, idempotent), receipt email | Done | `POST /v1/webhooks/razorpay`; ₹399 = 10-credit one-time pack; oldest-expiring credits first |
| 9 | Interview engine (stages, 8–12 questions, follow-ups) | Done | `interviews.py`; at least 2 follow-ups guaranteed by code |
| 9 | Answer + resume APIs (resume once within 10 min) | Done | `POST /v1/interviews/{id}/answer`, `GET /v1/interviews/{id}`, `POST …/resume` |
| 10 | Interview report (5 scores, model answers, red flags, plan) | Done | Scores clamped 1–10 and completeness-checked in code; PDF |
| 10 | Resume upload + text extraction, PII removed | Done | `POST /v1/uploads/resume` (PDF/DOCX ≤ 5 MB, magic-byte check); phones/emails stripped before AI |
| 11 | Hindi questions (glossary + back-translation), reports, interviews | Done | `translate_question`; `GET …/paper?lang=hi`; reports/interviews written in the chosen language. Real quality needs the Claude key + your Hindi reviewer. |
| 11 | Progress API | Done | `GET /v1/me/progress` |
| 12 | User memory (mastery, mistakes, seen, weak-topic papers, comparison) | Done | Papers lean towards weak topics (blueprint stays exact); report has a code-computed "since your last attempt" block |
| 12 | Admin APIs (flags, users, credits, payments, stats) | Done | `/v1/admin/flags`, `/questions/{id}` (edit/remove/confirm_wrong), `/users`, `/users/{id}/credits`, `/payments`, `/stats` |
| 13 | AI self-correction lessons | Done | `confirm_wrong` hides the question, saves the correction, writes a lesson used by later prompts (tested) |
| 13 | Email notifications (SES or Resend) | Done, needs your input | `EMAIL_PROVIDER=resend` (+ `RESEND_API_KEY`) or `smtp` (SES SMTP); receipt, report ready, credits expiring in 3 days |
| 13 | Security hardening | Done | Rate limits on login/AI endpoints, input validation, prompt-injection guard, CORS allow-list, secrets from env, security headers, refresh-token reuse detection |
| 14 | End-to-end testing with frontend | Not done | Backend journey verified on a live server (signup → profile → Hindi mini mock → report → ₹399 pack → Hindi interview → admin). Joint testing needs the frontend. |
| 14 | Production setup (backups, live keys, Sentry, uptime, logs) | Done, needs your input | Sentry wired (`SENTRY_DSN`, no PII sent). Needs AWS, managed Postgres with daily backups, Razorpay live keys, uptime monitor. |
| 15 | Final content check (pre-built papers, en + hi) | Not done | `python -m app.seed --papers 3` after the banks are built; needs your 1-hour review |
| 15 | Load test: 200 users, save/submit < 300 ms | Script done; target not yet measured | `backend/scripts/loadtest.py`. A 30-user run on this laptop with SQLite: submit p95 140 ms, autosave p95 1.07 s (SQLite allows one writer at a time). Must be run on Postgres staging. |
| 15 | Go-live and monitoring | Not done | Needs production |

## 2. What you need to provide (from the sheet's "What you must give the team")

| Item | Unlocks | Setting |
|---|---|---|
| Claude API key with billing | Real questions, reports, interviews, Hindi translation; bank building | `AI_PROVIDER=claude`, `ANTHROPIC_API_KEY` |
| Firebase project | Firebase login | `FIREBASE_PROJECT_ID` |
| Razorpay test keys, later live keys + webhook secret | Real checkout | `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET` |
| Email sender domain + Resend key (or SES SMTP) | Emails | `EMAIL_PROVIDER`, `RESEND_API_KEY`, `EMAIL_FROM` |
| AWS account (Mumbai), domain | Staging/production, backups | see README "Full stack in containers" |
| Sentry project | Error tracking | `SENTRY_DSN` |
| Decisions: GST included (assumed yes), company legal name + GSTIN | Invoices | `GSTIN`, `COMPANY_LEGAL_NAME` |
| Policy text (privacy, terms, refund) | Legal pages | Draft text is served by `GET /v1/policies/{kind}`; replace with lawyer-checked text |

## 3. Commands once the Claude key is set

```bash
cd backend && .venv/Scripts/python -m app.services.bank --exam ssc-cgl-tier1 --per-topic 40
```

```bash
cd backend && .venv/Scripts/python -m app.services.bank --exam ibps-po-prelims --per-topic 40
```

```bash
cd backend && .venv/Scripts/python -m app.services.bank --exam it-placement-aptitude --per-topic 30
```

```bash
cd backend && .venv/Scripts/python -m app.seed --papers 3
```

## 4. PDF requirements beyond the 15-day scope (Phase 2 in the sheet)

Already built in the backend and ready when the clients need them: all 23 languages (data, prompts, RTL flags,
per-language fonts), the full 15-exam / 6-role catalog (drafts), blueprint/topic/glossary/lesson/role admin APIs,
monthly/yearly subscriptions (auto-renew needs UPI AutoPay mandates), GST invoice PDFs, push notifications (FCM
adapter + device tokens), the WebSocket interview channel, voice metrics (pace, filler words), the quality dashboard
and the audit log.

Incomplete integrations (clearly marked in code):

| Item | State |
|---|---|
| Voice STT/TTS (Bhashini / Sarvam / Google / Azure) | Mock adapter only (`app/services/speech.py`); needs a provider choice and accounts |
| In-app purchases (Google Play / App Store) | `POST /v1/iap/verify` returns 501; needs store credentials and the legal decision on store billing |
| UPI AutoPay mandates for auto-renew | Renewal webhook handling exists; creating the mandate needs Razorpay subscription plans |
| Cashfree gateway | Not implemented (Razorpay chosen) |
| Real SMS OTP (DLT) | Not needed if Firebase phone auth is used; dev OTP adapter otherwise |
| Indic-script PDF shaping | reportlab + Noto fonts (put them in `FONTS_DIR`); complex conjuncts need a HarfBuzz renderer before launch for Hindi PDFs |
| S3 storage | Local storage behind an interface; switch to S3 (ap-south-1) in production |
