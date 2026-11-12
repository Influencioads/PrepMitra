# PrepMitra AI — Backend

One FastAPI backend for the **website and the Android/iOS apps**: AI mock exams and AI mock interviews in English
and the 22 scheduled Indian languages, with automated AI reports. Built from `Exam app.pdf` (MVP document,
22 pages).

- **Integration guide for web + mobile teammates:** [../docs/backend/API.md](../docs/backend/API.md)
- **Requirement-by-requirement status and remaining work:** [../docs/backend/REQUIREMENTS_STATUS.md](../docs/backend/REQUIREMENTS_STATUS.md)
- **Testing in Swagger, step by step:** [../docs/backend/SWAGGER_TESTING.md](../docs/backend/SWAGGER_TESTING.md)
- **Interactive API docs (when running):** `http://localhost:8000/docs` (Swagger) · `/redoc` · `/openapi.json`

## Stack

Python 3.12+ · FastAPI · SQLAlchemy 2 · Alembic · PostgreSQL 16 + pgvector · Redis (queue, rate limits, cache) ·
JWT (access + rotating refresh) · Anthropic Claude behind a provider layer · reportlab PDFs · Razorpay (test mode).

## Fastest way to try it (no Docker, no keys)

```bash
cd backend && .venv/Scripts/python scripts/dev_server.py
```

Runs on SQLite with the mock AI and mock payments, seeds the launch catalog (banking only: 6 bank exams + free mini mock,
the Bank PO interview, English + Hindi, ₹99 / ₹399 plans) and opens Swagger at `http://localhost:8000/docs`. Phone
`9000000009` is a founder admin. `SEED_SCOPE=full` publishes all 18 exams and 6 roles instead.

## Quick start (development)

```bash
docker compose up -d db redis
```

```bash
cd backend && python -m venv .venv && .venv/Scripts/pip install -r requirements.txt
```

Copy `backend/.env.example` to `backend/.env` and set `JWT_SECRET`. For a first run keep `AI_PROVIDER=mock` (no
API key needed); switch to `AI_PROVIDER=claude` with `ANTHROPIC_API_KEY` for real questions and reports.

```bash
cd backend && .venv/Scripts/python -m alembic upgrade head
```

```bash
cd backend && .venv/Scripts/python -m app.seed
```

`app.seed` publishes the 15-day launch scope by default; `--scope full` publishes the whole proposed catalog.

```bash
cd backend && .venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

On Linux/macOS use `.venv/bin/...` instead of `.venv/Scripts/...`. Set `BOOTSTRAP_ADMIN_PHONE` in `.env` so your
number becomes a founder admin at first login. In development `POST /v1/auth/otp/send` returns the OTP in
`dev_otp` (no SMS is sent).

**Without Docker** (no Postgres available): point `DATABASE_URL` at SQLite, e.g.
`DATABASE_URL=sqlite:///./dev.db`, then create the schema with
`python -c "from app.db import Base, engine; import app.models; Base.metadata.create_all(engine)"` and seed.
SQLite is for local demos and tests only; production and migrations target PostgreSQL.

### Full stack in containers

```bash
docker compose --profile full up -d --build
```

This runs migrations + seed once, then the API (port 8000) and a background worker on Redis.

## Tests

```bash
cd backend && .venv/Scripts/python -m pytest
```

115 tests cover auth (incl. Firebase), profile/DPDP, catalog, the question pipeline, paper assembly, the timed exam engine,
scoring, reports, credit rules, interviews over REST and WebSocket, payments/webhooks, admin, notifications and the
migration. By default they use a throwaway SQLite DB with the mock AI and mock payment gateway; to run them against
PostgreSQL + pgvector (migrated with Alembic) set `TEST_DATABASE_URL` to a Postgres URL.

## Project layout

```
backend/
  app/
    main.py            FastAPI app, middleware, router wiring, scheduler lifespan
    config.py          all settings (env vars)
    db.py              engine/session + portable types (timestamptz, JSONB, pgvector)
    seed.py            plans, 15 launch exams with blueprints + syllabus, 6 interview roles, glossary
    worker.py          `python -m app.worker`: Redis job consumer + periodic scheduler
    core/              auth deps, JWT, errors, Redis/cache, rate limits, audit/analytics, i18n, languages
    ai/                provider layer (Claude + mock), prompts, JSON schemas, embeddings, prompt-injection/PII guards
    models/            SQLAlchemy models (35 tables; PDF section 10 + supporting tables)
    schemas/           request/response models
    services/          business logic (one module per domain)
    routers/           HTTP + WebSocket endpoints (public, user, admin)
    jobs/              job queue (eager/thread/redis), task registry, scheduler
  alembic/             migrations (0001 = initial schema)
  tests/               pytest suite
docs/                  API guide, requirement status, plan/tracker
```

## AI model routing and pricing (Nov 2026 blueprint)

All AI goes through one gateway, `app/ai/provider.py`. With `AI_PROVIDER=openrouter` and `OPENROUTER_API_KEY` set,
each call is routed by feature (`app/ai/catalog.py`): a cheap primary model, fallbacks for outages, and a premium
model only when the caller asks for escalation and the student still has premium allowance. Model ids and prices
are OpenRouter's list on 2026-11-12, at ₹90 = $1; every call logs tokens, cache hits and cost to `ai_usage`.

| Feature (current call site) | Primary | Fallback | Premium |
|---|---|---|---|
| Mock report + time analysis (`exam_report`) | DeepSeek V3.2 | Gemini 2.5 Flash | — |
| Persona micro-update (`mentor_attempt_note`) | Gemini 2.5 Flash-Lite | GPT-5 nano | — |
| Study planner (`mentor_plan_note`) | GPT-5 mini | DeepSeek V3.2 | — |
| Ask Mitra chat (`mentor_chat`) | DeepSeek V3.2 (Gemini Flash for Indian languages) | Claude Haiku 5.5 | Claude Sonnet 5.5 |
| Interview turns / scoring | Kimi K2 / GPT-5 | GLM-4.6 / Claude Sonnet 5.5 | — |
| Question bank write / verify | GPT-5 / DeepSeek V3.2 (reasoning) | Gemini 3.1 Pro | Claude Opus 5.5 |
| Translation / back-translation | Gemini 2.5 Flash / GPT-5 mini | Flash-Lite / DeepSeek | — |

`GET /v1/admin/ai/costs` shows ₹ per feature and the routing in force; `AI_MODEL_OVERRIDES` swaps a model without a
release.

### Student AI features (`/v1/ai/...`, code in `app/services/ai_features/`)

| Feature | Endpoint | Allowance / plan |
|---|---|---|
| Doubt Solver (solution store first, verified by a second model, saved for everyone) | `POST /ai/doubts`, `/ai/doubts/{id}/explain-again`, `/feedback` | doubts (Free 5 for life, Starter 50, Pro 150 incl. 50 premium) |
| Photo Doubt | `POST /ai/doubts/photo` | photo doubts (Tutor packs) |
| AI Tutor Deep Dive (smart / master / ultra) | `POST /ai/tutor/deep-dives`, `GET` for history | Smart / Master / Ultra credits (Free: 1 sample) |
| Ask Mitra tutor chat | `POST /ai/tutor/chat`, `GET` for history | tutor chat turns (Tutor packs) |
| Persona, deep persona, Ultra review | `GET /ai/persona`, `POST /ai/persona/deep`, `/ai/persona/ultra-review` | everyone / Pro monthly / 1 Ultra credit |
| Rank & Cutoff Predictor | `GET /ai/rank?exam_id=` | Pro |
| Mistake Notebook weekly summary (PDF on Tutor Pro) | `GET /ai/mistakes/summary` | Starter+ |
| Notes Maker (shared master notes or personal) | `POST /ai/notes` | personal notes (Starter 5, Pro 20) |
| Topic Explainer (free library or custom deck) | `GET /ai/topic-decks/library`, `POST /ai/topic-decks` | library free; custom: Pro 5, or 3 tutor credits, Ultra 4 |
| Revision AI (spaced quiz + AI hints + flashcards) | `POST /ai/revision/today` | Starter+ |
| Current Affairs digest + quiz (daily, fact-checked) | `GET /ai/current-affairs` | Pro |
| Descriptive Writing Evaluator (+ topper rewrite) | `POST /ai/writing/evaluate` | Pro 4/month (+1 Master credit) |
| Cheat Code Coach (spot, shape, test, lock) and shortcut library | `/ai/coach/sessions...`, `GET /ai/coach/cards`, `GET /ai/shortcuts` | coach sessions |
| Any item as PDF | `GET /ai/artifacts/{id}/pdf` | owner or shared |

Admin: `GET/PATCH /admin/ai/solutions` (disputed and flagged answers), `POST /admin/ai/library/decks`,
`POST /admin/ai/current-affairs/run`. A failed AI call returns 503 and refunds the allowance; off-topic requests get
422; messages showing distress get the Tele-MANAS helpline (14416) instead of an AI reply.

Plans follow the blueprint (`app/services/plan_catalog.py`): Free, Starter ₹149/399/1,199, Pro ₹299/799/2,499,
AI Tutor Lite ₹99/999, AI Tutor Pro ₹299/2,999, Topper Combo ₹499/4,999 and add-ons (₹29 mock, ₹49 for 5 mocks,
₹39 doubts, ₹99 Master deep dives, ₹199 interview pack, ₹349 Ultra pack). Full mocks are exam credits as before; the
other AI limits are monthly allowances (`app/services/allowances.py`, `GET /v1/me/allowances`) that fall back to
the cheaper model instead of blocking when the premium allowance runs out.

## Background jobs

| Job | Trigger | What it does |
|---|---|---|
| `generate_exam_report` | exam submit | AI report from code-computed analytics, validated, PDF, push |
| `evaluate_interview` | interview end | rubric scoring (clamped by code), per-answer feedback, PDF, push |
| `send_notification` | any notification | push (FCM) + email (SMTP/SES) |
| auto-submit | every 15 s | submits attempts whose server deadline passed |
| report timeouts | every 60 s | report not ready in 10 min → failed + credit restored |
| interview timeouts | every 60 s | disconnected > 10 min → evaluated on what was answered |
| paper pre-generation | every 10 min | keeps `PAPERS_POOL_SIZE` blueprint-exact papers ready per exam |
| credit expiry, subscription expiry | hourly | ledger expiry rows, lapsed subscriptions |
| expiring-credit and inactivity reminders | every 6 h (deduplicated) | "plan expiring in 3 days", "inactive 7 days" |

`JOB_MODE=thread` runs these inside the API process (single instance). In production use `JOB_MODE=redis`,
`RUN_SCHEDULER_IN_API=false` and run one or more `python -m app.worker` processes.

## Security notes

OTP hashed + rate limited (per phone and per IP), refresh-token rotation with reuse detection, role-based admin with
an audit log of every write, security headers, CORS allow-list, signed + idempotent payment webhooks, no card/UPI
data stored, user text wrapped as data in prompts with phones/emails stripped, resumes checked by magic bytes and
size. Secrets come from the environment (use a vault in production).
