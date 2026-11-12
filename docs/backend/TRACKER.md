# PrepMitra AI — Project Tracker

Plan: [PLAN.md](PLAN.md) · Excel: [PrepMitra_15_Day_Plan.xlsx](PrepMitra_15_Day_Plan.xlsx) · Audit: [AUDIT.md](AUDIT.md)

| Day | Task | Status |
|---|---|---|
| 1 | Project setup, configuration, database | In Progress (blocked on Docker engine for migration + test run) |
| 2 | Authentication, profiles, consent | In Progress (code + tests written, not yet run) |
| 3–15 | See plan | Not Started |

---

## Session log: Day 1 (2026-10-26)

**Completed work**
- Read the full 22-page PDF and audited the workspace: `examapp/` was empty, so this is a green-field build ([AUDIT.md](AUDIT.md)).
- Confirmed the stack with the owner: React + FastAPI + PostgreSQL/pgvector + Claude, 18+ only.
- 15-day plan written ([PLAN.md](PLAN.md)) and exported to Excel.
- Backend scaffold: settings, DB session, **34-table SQLAlchemy data model** covering all of PDF §10 plus OTP, refresh tokens, webhook idempotency, AI usage, notifications and analytics events.
- Auth module (Day 2 work pulled forward): OTP send/verify (hashed with HMAC, 5-minute TTL, 5 sends/hour, 5 tries), Google sign-in (active once `GOOGLE_CLIENT_ID` is set), JWT access tokens + rotating refresh tokens with reuse detection, logout.
- Profile module: `/v1/me` GET/PATCH/DELETE, 18+ check, required-fields check before the first attempt, consents (versioned, recruiter sharing OFF by default, withdrawable), DPDP data export, account deletion (PII scrubbed immediately, sessions revoked), resume upload (PDF/DOCX, magic-byte check, ≤ 5 MB, text extracted).
- `docker-compose.yml` (pgvector/pg16 + test DB), `.env.example`, local `.env` with a random JWT secret, Alembic configured, pytest harness against a real Postgres test DB.

**Files created**
- `docs/AUDIT.md`, `docs/PLAN.md`, `docs/TRACKER.md`, `docs/PrepMitra_15_Day_Plan.xlsx`
- `docker-compose.yml`, `.env.example`, `.gitignore`, `backend/requirements.txt`, `backend/pytest.ini`
- `backend/app/{config,db,main}.py`
- `backend/app/core/{security,errors,deps,languages}.py`
- `backend/app/models/{users,catalog,activity,billing,__init__}.py`
- `backend/app/services/{auth,profile,providers}.py`
- `backend/app/schemas/me.py`, `backend/app/routers/{auth,me}.py`
- `backend/alembic/env.py`, `backend/scripts/init-test-db.sql`
- `backend/tests/{conftest,test_auth,test_me}.py`

**APIs:** `GET /v1/health`, `GET /v1/languages`, `POST /v1/auth/otp/send`, `POST /v1/auth/otp/verify`, `POST /v1/auth/google`, `POST /v1/auth/refresh`, `POST /v1/auth/logout`, `GET|PATCH|DELETE /v1/me`, `POST /v1/me/consents`, `DELETE /v1/me/consents/{type}`, `GET /v1/me/export`, `POST|DELETE /v1/me/resume`

**DB changes:** Models defined. The initial Alembic migration is **not generated yet** because it needs a running Postgres.

**Tests executed**
- App and all models import cleanly. 34 tables registered.
- 23 auth/profile tests written. **Not yet run**, because there is no database.

**Outstanding issues / blockers**
- **Docker Desktop engine fails to start**: its backend crashes with `initializing Inference manager … remove …\AppData\Local\Docker\run\dockerInference: The file cannot be accessed by the system`. The fix is to quit Docker Desktop, delete that stale socket file, and restart (or turn off Docker Model Runner in Settings). This needs the owner's go-ahead.
- Real SMS provider (DLT), Google client ID, Anthropic key and Razorpay test keys are still to be supplied in `.env`.

**Next actions**
1. Start Postgres, then run `alembic revision --autogenerate -m initial`, `alembic upgrade head` and `pytest`. Fix any failures.
2. Day 1 remainder: AI provider abstraction (Claude + mock) and the React (Vite + TS) scaffold with login/profile screens.
3. Day 3: seed blueprints, catalog APIs and catalog UI.
