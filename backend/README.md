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

Runs on SQLite with the mock AI and mock payments, seeds the 15-day launch catalog (3 exams + free mini mock,
2 interview roles, English + Hindi, ₹99 / ₹399 plans) and opens Swagger at `http://localhost:8000/docs`. Phone
`9000000009` is a founder admin. `SEED_SCOPE=full` publishes all 15 exams and 6 roles instead.

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
