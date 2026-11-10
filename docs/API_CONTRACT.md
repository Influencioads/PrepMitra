# PrepMitra AI — API contract (frontend ⇄ backend)

> **Status (Nov 2026): connected.** The FastAPI backend in `backend/` implements every route below. Its JSON is
> snake_case and its IDs are slugs/UUIDs, so the frontend translates both ways in `shared/src/api/adapters.ts`
> (e.g. exam `ssc-cgl` ⇄ backend slug `ssc-cgl-tier1`). The real request/response bodies are in
> `docs/backend/API.md` and live at `http://localhost:8000/docs`. The tables below describe what the screens use.

Source: the "API Plan" sheet of the 15-day plan. This file describes what the **web app**
(`frontend/`) sends and expects. Route constants live in `shared/src/constants`
(`API_ENDPOINTS`) and types in `shared/src/types/core.ts`.

**Example bodies:** `frontend/src/mocks/api/*.json`, with one file per row below.
Regenerate them with `npm run fixtures -w frontend`.

## Conventions

| Item | Rule |
| --- | --- |
| Base URL | `VITE_API_BASE_URL`; all routes start with `/v1` |
| Format | JSON over HTTPS, UTF-8, ISO-8601 timestamps |
| Auth | `Authorization: Bearer <Firebase ID token>`. The web app refreshes the token before each request (`services/http.ts`). |
| Errors | `{ "code": "SNAKE_CASE", "message": "Human readable" }` with a proper HTTP status. 401 signs the user out; 402 means not enough credits or a payment failure. |
| Mock switch | The frontend uses in-browser mocks while `VITE_USE_MOCK_API=true`. None of these routes are called in that mode. |
| Security | The server is the source of truth for timers, scoring, credits and roles. Frontend route guards are only for UX. |

**Auth column:** — = public · U = signed-in user · A = admin role (checked on the server).

## Auth & profile

| # | Method | Path | Request | Response | Auth | Screen | Fixture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | POST | `/v1/auth/session` | `{ profile?: { name, email? } }` + Firebase ID token | `AuthSession` | token | Login / Verify OTP / Google | `auth-session` |
| 2 | GET | `/v1/me` | — | `{ user: User, profile: UserProfile, settings: UserSettings }` | U | App start, Profile | `me-get` |
| 3 | PATCH | `/v1/me` | partial `{ user?, profile?, settings? }` | same as GET | U | Onboarding, Profile, Settings | `me-patch` |
| 4 | DELETE | `/v1/me` | — | `204` | U | Settings → Delete account | `me-delete` |
| 5 | POST | `/v1/me/consents` | `{ consentType, granted }` | `204` | U | Signup, Resume upload | `consents` |
| 6 | GET | `/v1/me/credits` | — | `{ credits, nextExpiry?, ledger: CreditLedgerEntry[] }` | U | Dashboard, Subscription | `credits` |
| 7 | GET | `/v1/me/progress` | — | `ProgressData` | U | Progress | `progress` |

Phone OTP and Google sign-in are handled by the **Firebase SDK in the browser**
(`services/firebaseAuth.ts`, enabled with `VITE_AUTH_PROVIDER=firebase`). The backend never
sends an SMS itself. It only verifies the ID token at `/v1/auth/session` and creates or loads the user.

## Catalog

| # | Method | Path | Request | Response | Auth | Screen | Fixture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | GET | `/v1/exams` | query `category?, language?, q?` | `Exam[]` (published only) | — | Exams list, Landing | `exams` |
| 9 | GET | `/v1/exams/{id}` | — | `Exam` | — | Exam details | `exam` |
| 10 | GET | `/v1/interview-roles` | — | `InterviewRole[]` | — | Interview setup | `interview-roles` |

## Exam attempts

| # | Method | Path | Request | Response | Auth | Screen | Fixture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | POST | `/v1/attempts` | `{ examId, language, mode: 'mini' \| 'full' }` | `Attempt` (deducts a credit unless it is the free mini mock) | U | Exam instructions → Start | `attempts-create` |
| 12 | GET | `/v1/attempts/{id}/paper?lang=` | — | `Attempt` + `questions[]` **without** `correctOptionIds`, `correctNumeric` or `explanation`; server `endsAt`; saved `states` (for resume) | U | Exam session | `attempt-paper` |
| 13 | PUT | `/v1/attempts/{id}/answers` | `{ states: Record<questionId, QuestionState>, currentIndex }` | `204` | U | Exam session autosave (every 10 s and on change) | `attempt-answers` |
| 14 | POST | `/v1/attempts/{id}/events` | `AttemptEvent { type: 'tab_switch' \| 'copy_attempt', at }` | `204` | U | Exam session (light anti-cheat, logged only) | `attempt-events` |
| 15 | POST | `/v1/attempts/{id}/submit` | `{ states, autoSubmitted }` | `202 { status: 'processing' }` (server rejects answers after `endsAt` + grace) | U | Exam session → Submit | `attempt-submit` |
| 16 | GET | `/v1/attempts/{id}/report` | — | `ReportStatusResponse`: `processing` / `ready` (+ `ExamReport`) / `failed` | U | Report processing screen (polled every 3 s, 2-min timeout) | `attempt-report-*` |
| 17 | GET | `/v1/attempts/{id}/review` | — | `QuestionReviewItem[]` (with answers and explanations) | U | Report → Question review | `attempt-review` |
| 18 | POST | `/v1/reports/{id}/rating` | `{ rating: 1–5 }` | `204` | U | Exam and interview report | `report-rating` |
| 19 | POST | `/v1/questions/{id}/flags` | `{ reason, note? }` | `204` | U | Exam session / review → Report question | `question-flags` |

**Mini mock:** `mode: 'mini'` gives at most 10 questions in 30 minutes, spread across all sections.
It is free once per user. `Attempt.isMini` and `ExamReport.isMini` are set.
The demo version is in `shared/src/logic/paper.ts` (`MINI_MOCK`, `capPaper`).

**Errors the exam screens handle (Day 6):**

| When | Server reply | What the student sees |
| --- | --- | --- |
| Start, no credits | `402 insufficient_credits` | "You need more credits" dialog; balance re-synced from the server |
| Start, incomplete profile | `409 profile_incomplete` | Toast, then the profile page |
| Start, no network | no response | "You are offline. Nothing was charged" |
| Autosave or submit after the deadline | `409 deadline_passed` | Exam closes, report processing screen |
| Autosave on a closed attempt | `409 attempt_closed` | Exam closes, report processing screen |
| Submit, no network | no response | Answers stay on the device; submit is sent again when the network returns |
| Report polling, network drop or 5xx | — | "Connection lost — still checking" and polling continues |
| Report job failed | `failed` (+ `credit_restored`) | Error card with **Try again** (`POST /v1/reports/{id}/retry`) |
| Report not ready in 2 minutes | `processing` | "Taking longer than usual" with **Check again** |

The processing screen is its own route, `/exam/{attemptId}/processing`, so a refresh keeps polling.
Submitted attempts that are still waiting for a report are listed on My tests.

## Payments (Razorpay)

| # | Method | Path | Request | Response | Auth | Screen | Fixture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20 | GET | `/v1/plans` | — | `Plan[]` | — | Pricing, Subscription | `plans` |
| 21 | POST | `/v1/orders` | `{ planId }` | `{ orderId, amountPaise, currency: 'INR', planName, prefill? }` | U | Checkout | `orders-create` |
| 22 | POST | `/v1/orders/verify` | `{ razorpay_payment_id, razorpay_order_id, razorpay_signature, planId, method }` | `DemoOrder` (status `success`; credits added) | U | Checkout → success | `orders-verify` |
| 23 | POST | `/v1/webhooks/razorpay` | Razorpay webhook body | `200` | Razorpay signature | — (server only, adds credits idempotently) | `payments-webhook` |

The frontend only knows the **Key ID** (`VITE_RAZORPAY_KEY_ID`). Card and UPI details are entered inside Razorpay's own window.
The Key Secret and webhook secret stay on the server.

Failure handling (`services/razorpay.ts`):

- **Cancelled or failed payment:** shown as "Payment failed — no money was deducted" with a Retry button.
- **Verify failure after a captured payment:** shown as "credits will appear within a few minutes" (the webhook settles it).

**Pricing sets:** `VITE_PRICING_SET=full|launch`. `launch` = Free, Pay-per-mock and a 10-credit pack (₹399, valid 90 days).

## Interviews

| # | Method | Path | Request | Response | Auth | Screen | Fixture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 24 | POST | `/v1/interviews` | `InterviewConfig` | `InterviewSession` (first question in `turns`) | U | Interview setup → Start | `interviews-create` |
| 25 | GET | `/v1/interviews/{id}` | — | `InterviewSession` | U | Resume within 10 min | `interview-get` |
| 26 | POST | `/v1/interviews/{id}/answer` | `{ text, durationSec }` | `InterviewSession` (next question or follow-up appended) | U | Interview session | `interview-answer` |
| 27 | POST | `/v1/interviews/{id}/end` | — | `202 { status: 'processing' }` | U | Interview session → End | `interview-end` |
| 28 | GET | `/v1/interviews/{id}/report` | — | `{ status: 'processing' } \| { status: 'ready', report: InterviewReport }` | U | Interview report (polled) | `interview-report-*` |
| 29 | POST | `/v1/uploads/resume` | `multipart/form-data` `file` (PDF/DOCX ≤ 5 MB) | `ResumeInfo` | U | Profile, Interview setup | `uploads-resume` |

## Notifications

| # | Method | Path | Request | Response | Auth | Screen | Fixture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 30 | GET | `/v1/me/notifications` | — | `AppNotification[]` | U | Notifications (Phase 2; launch uses email) | — |

## Admin (role checked on the server)

| # | Method | Path | Request | Response | Auth | Screen | Fixture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | GET | `/v1/admin/flags` | — | `ReviewItem[]` | A | Admin → Review queue | `admin-flags` |
| 32 | POST | `/v1/admin/flags/{id}/resolve` | `{ action, note? }` | `204` | A | Admin → Review queue | — |
| 33 | PATCH | `/v1/admin/questions/{id}` | `{ status?, ...fields, note? }` | `{ ok: true }` | A | Admin → Question bank | `admin-question-patch` |
| 34 | GET | `/v1/admin/users?q=` | — | `AdminUserRecord[]` | A | Admin → Users | `admin-users` |
| 35 | POST | `/v1/admin/users/{id}/credits` | `{ delta, reason }` | `{ credits }` | A | Admin → Users → Adjust credits | `admin-user-credits` |
| 36 | GET | `/v1/admin/payments` | — | `AdminOrder[]` | A | Admin → Payments | `admin-payments` |
| 37 | GET | `/v1/admin/stats` | — | `PlatformAnalytics` | A | Admin → Overview | `admin-stats` |

The other admin screens (lessons, glossary, team, audit log and so on) are Phase 2.
They stay on demo data at launch.

## Known frontend gaps for the real-API switch

- The exam session renders question text from the bundled demo bank (`getQuestionById`). It does not yet read `questions[]` from `/paper`. Wire this before turning mocks off.
- The resume prompt for an interview (#25) works only for sessions already in the local store. The `getSession` call exists but is not used yet.
- Landing and Pricing pages use the shared default `PLANS` (`ACTIVE_PLAN_SET` in shared). Subscription and checkout follow `VITE_PRICING_SET`.
