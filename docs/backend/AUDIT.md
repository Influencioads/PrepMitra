# PrepMitra AI — Implementation Audit

**Date:** 2026-10-26 (Day 1)
**Source of truth:** `Exam app.pdf` (MVP Document, 22 pages, dated 2026-10-22)

## 1. What exists today

| Area | Finding |
|---|---|
| Project folder `examapp/` | **Empty** at audit time — no source code, schema, APIs, frontend, dependencies or config. |
| Other folders in `Downloads/` | Searched for `exam`, `prep`, `mitra`, `mock`: no related codebase found. |
| Database | PostgreSQL **not installed** natively (`C:\Program Files\PostgreSQL\17` contains only an empty `bin`). Docker Desktop 29.6 is installed → Postgres + pgvector run via `docker-compose.yml`. |
| Tooling | Python 3.14.7, Node 22.16 / npm 11.19, git 2.50, Docker 29.6. |

**Conclusion:** This is a green-field build. Nothing is implemented, partially implemented or broken — every feature in the PDF is *Missing*.

## 2. Decisions taken (confirmed with owner on Day 1)

| Decision | Choice | Notes |
|---|---|---|
| Backend | **FastAPI (Python)** modular monolith | AI module lives in `app/ai/` behind a provider abstraction; can be split into its own service later (PDF §9). |
| Web frontend | **React (Vite + TypeScript)** | PDF suggested Next.js; owner chose React. API is client-agnostic so React Native apps can reuse it. |
| Database | **PostgreSQL 16 + pgvector** via Docker | Alembic migrations. |
| LLM | **Claude API** (`claude-opus-5-5`) via `anthropic` SDK | Owner adds `ANTHROPIC_API_KEY` to `.env`. A deterministic `mock` provider is used in automated tests so tests never spend money. |
| Minimum age | **18+ only** | DOB checked at profile completion; parental-consent flow deferred. |

## 3. Open decisions from the PDF (§15) — defaults assumed until owner confirms

| Item | Assumed default |
|---|---|
| Product name | "PrepMitra AI" (configurable `APP_NAME`) |
| GST | Prices are **GST-inclusive**; GST (18%) is back-calculated on the invoice |
| Yearly plan | ₹2,999 / 150 credits / 365 days (as proposed) |
| Interview price | Same as exam: 1 credit |
| 2 state PSCs | Not seeded; blueprints can be added from admin without code |
| AI cost cap | ₹20 per attempt target; tracked in `ai_usage` table |

## 4. Gap list vs PDF (all Missing at audit)

Registration/OTP/Google sign-in · profile · consents · data export/delete · catalog · blueprints · topics · question bank · translations · papers · timed exam engine · autosave · resume · auto-submit · anti-cheat logging · question reports · deterministic scoring · percentile · AI question generation + verification + dedup · AI report · PDF export/share link · report rating · user memory · AI lessons/glossary · interviews (text, voice) · interview report · dashboard · notifications · plans/orders/webhooks/credits · admin panel + audit log · quality dashboard · i18n · policies/disclaimers · tests · deployment docs.
