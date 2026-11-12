# PrepMitra AI API — Integration Guide (Web + Android + iOS)

One API for every client. Base URL: `https://<api-host>/v1` (local: `http://localhost:8000/v1`).
Live, always-current reference: **`/docs`** (Swagger) and **`/openapi.json`**. Generate a typed client from it
(for example `npx openapi-typescript http://localhost:8000/openapi.json -o src/lib/api/schema.ts`).
How to click through everything in Swagger: [SWAGGER_TESTING.md](SWAGGER_TESTING.md).

## 1. Conventions

| Topic | Rule |
|---|---|
| Format | JSON over HTTPS. Times are ISO-8601 UTC (`2026-10-31T09:53:40Z`). IDs are UUIDs (some admin ids are integers). |
| Auth | `Authorization: Bearer <token>`. The token can be a **Firebase ID token** or the backend's own access token. |
| Errors | Always `{"error": {"code": "...", "message": "...", "details"?: [...]}}`. Switch on `code`; show `message` to users. |
| Validation | 422 `validation_error` with `details: [{"field", "message"}]`. |
| Paging | `?limit=&offset=`; responses carry `items`, `total`, `limit`, `offset`. |
| Money | Paise as integers (`9900` = ₹99). Prices include 18% GST. |
| Languages | Codes from `GET /v1/meta` (`en`, `hi`, … 23 total). The launch scope offers `en` and `hi`. |
| Request IDs | Every response has `X-Request-ID`; include it in bug reports. |
| Rate limits | 429 `rate_limited`. Retry after a short wait. |

Error codes the UI should handle explicitly:

| Code | Status | What the client should do |
|---|---|---|
| `unauthenticated`, `invalid_token` | 401 | Refresh the token, or send the user to login |
| `account_blocked` | 403 | Show "account blocked, contact support" |
| `profile_incomplete` | 409 | Send the user to onboarding (`missing_fields` from `GET /v1/me`) |
| `insufficient_credits` | 402 | Send the user to pricing |
| `deadline_passed`, `attempt_closed` | 409 | Stop the exam UI, open the submit/report screen |
| `language_not_available` | 422 | Hide that language option |
| `interview_in_progress` | 409 | `details.interview_id` → resume that interview |
| `interview_ended` | 409 | Open the interview report |
| `paper_unavailable` | 503 | "Preparing your paper, try again shortly" (no credit was used) |

## 2. Login

### Option A — Firebase Authentication (planned for launch)

1. The client signs in with Firebase (phone OTP or Google) and gets the **Firebase ID token**
   (`user.getIdToken()`; Android `getIdToken(false)`; iOS `getIDToken`).
2. `POST /v1/auth/session` with `Authorization: Bearer <firebase-id-token>` on first app open after login:

```json
{
  "is_new_user": true,
  "user": {"id": "…", "phone": "+919812345678", "name": null, "preferred_language": "en",
           "profile_complete": false, "missing_fields": ["name", "dob", "target_exam_or_role", "data_processing_consent"],
           "consents": {"data_processing": false, "recruiter_sharing": false, "marketing": false}, "…": "…"},
  "access_token": "…", "refresh_token": "…", "token_type": "bearer", "expires_in": 900
}
```

3. On every later request, send the Firebase ID token (the Firebase SDK refreshes it hourly). You may instead use the
   returned backend `access_token` plus `refresh_token`; both work.

Backend needs `FIREBASE_PROJECT_ID`. Without it, `/auth/session` returns 503 `firebase_not_configured`.

### Option B — backend OTP (dev and Swagger, or if Firebase is dropped)

`POST /v1/auth/otp/send {"phone": "9876543210"}` → `{"sent": true, "expires_in": 300, "dev_otp": "123456"}`
(`dev_otp` only in development) → `POST /v1/auth/otp/verify {"phone", "code"}` → tokens.
`POST /v1/auth/refresh {"refresh_token"}` rotates tokens (a reused refresh token logs the user out everywhere).
`POST /v1/auth/logout {"refresh_token"}`.

## 3. Onboarding and profile

```http
POST /v1/me/consents            {"data_processing": true, "recruiter_sharing": false, "marketing": false}
PATCH /v1/me                    {"name": "Asha Kumar", "dob": "2000-05-14", "preferred_language": "hi",
                                 "education": "graduate", "stream": "B.Com", "experience_years": 0,
                                 "target_exam_ids": ["ssc-cgl-tier1"], "target_role_ids": []}
GET /v1/me                      → profile_complete, missing_fields, consents, is_admin, admin_role
DELETE /v1/me                   → 204 (personal data scrubbed, sessions revoked)
GET /v1/me/export               → all data as JSON (DPDP right to access)
POST /v1/uploads/resume         multipart "file" (PDF/DOCX ≤ 5 MB) → {"preview": "...", "characters": 1834}
DELETE /v1/me/consents/recruiter_sharing
```

Users must be 18+ (403 `underage`). The first exam is blocked until `profile_complete` is true.

## 4. Catalog (public, no token)

```http
GET /v1/exams?category=banking&q=ssc&language=hi&limit=50
GET /v1/exams/{id-or-slug}      → pattern.sections[], duration, total_marks, negative_marking, sample_question,
                                   syllabus[], languages, credits_required, is_free_trial, disclaimer
GET /v1/interview-roles         → [{id, slug, name, levels, duration_min, evaluates[]}]
GET /v1/plans                   → [{code, name, price_paise, gst_paise, credits, validity_days, purchasable}]
GET /v1/meta                    → languages (with tier, rtl), categories, education levels, event types …
GET /v1/policies/{privacy|terms|refund|ai-notice}
```

Show `disclaimer` on every exam page ("Mock test based on … pattern. Not affiliated with …").

## 5. Mock exam (CBT)

```http
POST /v1/attempts                       {"exam_id": "…", "language": "hi"}
GET  /v1/attempts/{id}/paper?lang=hi    (also GET /v1/attempts/{id})
PUT  /v1/attempts/{id}/answers          batched autosave
POST /v1/attempts/{id}/events           anti-cheat events
POST /v1/attempts/{id}/submit
GET  /v1/attempts/{id}/report           poll until status = ready
GET  /v1/attempts/{id}/review           after submit only
POST /v1/questions/{qid}/flags          {"reason": "wrong_answer|unclear|bad_translation|other", "details", "language"}
GET  /v1/attempts                       history
```

**Start** returns 201 (new) or 200 with `"resumed": true` if an attempt for that exam is still running; no second
credit is charged. It uses the one-time free trial on the free mini mock, otherwise 1 credit (oldest-expiring first).

**Paper** (no correct answers, ever):

```json
{
  "id": "…", "status": "in_progress", "language": "hi", "server_time": "…", "deadline_at": "…",
  "remaining_seconds": 1799,
  "rules": {"duration_min": 30, "calculator_allowed": false, "section_switching_allowed": true,
            "sections": [{"key": "quant", "name": "Quantitative aptitude", "question_count": 10,
                          "marks_per_question": 1, "negative_marks": 0.25}], "languages": ["en", "hi"],
            "instructions": "…"},
  "questions": [{
    "seq": 1, "question_id": "…", "section_key": "quant", "type": "single",
    "content":    {"language": "hi", "text": "…", "options": [{"key": "A", "text": "…"}]},
    "content_en": {"language": "en", "text": "…", "options": […]},
    "answer": null, "marked_for_review": false, "visited": false, "time_spent_sec": 0, "client_rev": 0
  }]
}
```

- **Timer:** count down from `deadline_at`, corrected by `server_time − device time`. Never trust the device clock.
  The server auto-submits after the deadline (plus a 30 s grace period).
- **Language toggle:** `content_en` is included, so switching needs no extra request. It is `null` when the content
  is already English. A question without a reviewed translation comes back in English.
- **Answer formats:** single `"B"` · multiple `["A","C"]` · numeric `12.5` · `null` clears the response.
- **Autosave** (every ~10 s and on change; keep a local copy for offline):

```json
PUT /v1/attempts/{id}/answers
{"answers": [{"question_id": "…", "answer": "B", "marked_for_review": false, "visited": true,
              "time_spent_sec": 42, "client_rev": 7}]}
→ {"saved": 1, "ignored_stale": 0, "remaining_seconds": 1210, "server_time": "…"}
```

`client_rev` is a per-question counter that the client increments on every change. The server ignores a revision
older than or equal to the one it has, so retries and out-of-order deliveries are safe. `time_spent_sec` is the
total time on that question (it never decreases).
- **Palette state** comes from `answer`, `marked_for_review` and `visited`.
- **Anti-cheat:** `POST …/events {"events": [{"type": "tab_switch"}, {"type": "screenshot_attempt"}]}`. Types are in
  `GET /v1/meta`. Events are logged and shown in the report; they are never punished.
- **Resume after a crash:** `GET /v1/attempts/{id}/paper`, then merge the local copy, keeping the higher `client_rev`.

**Submit** → `{"status": "scored", "score": 18.5, "max_score": 30, "percentile": 62.5, "report_id": "…",
"report_status": "processing"}`.

**Report** (`GET /v1/attempts/{id}/report` or `GET /v1/reports/{report_id}`): poll every 3 s while
`status == "processing"` (`poll_after_seconds`), or wait for the `result_ready` notification.

```json
{
  "id": "…", "status": "ready", "language": "hi", "pdf_url": "…/v1/reports/{id}/pdf",
  "analytics": {"score": 18.5, "max_score": 30, "accuracy": 0.68, "percentile": 62.5, "negative_marks_lost": 1.5,
                "sections": [...], "topics": [{"name": "Percentage", "accuracy": 0.4, "wrong_refs": [3, 7]}],
                "error_patterns": [{"type": "careless_easy", "question_refs": [2], "marks_lost": 1.25}],
                "questions": [{"ref": 1, "status": "correct", "time_sec": 40, "expected_time_sec": 45}],
                "since_last_attempt": {"score_change": 3.5, "improved_topics": ["Percentage"], …} | null},
  "report": {"summary": "…", "score_summary": {...},
             "strengths": [{"topic", "detail"}],
             "weaknesses": [{"topic", "detail", "question_refs": [3, 7], "questions": [{"ref": 3, "question_id": "…"}]}],
             "loopholes": [{"pattern", "detail", "question_refs"}],
             "shortcuts": [{"question_ref": 7, "question_id": "…", "technique", "explanation"}],
             "study_plan": [{"day": 1, "focus", "tasks": []}],
             "next_test": {"exam_slug", "name", "reason"},
             "since_last_attempt": {"summary": "…", "score_change": 3.5, "topics": [...]} | null,
             "encouragement": "…"},
  "user_rating": null, "credit_restored": false
}
```

Numbers come from code (`analytics`, `score_summary`); the AI writes only the words. `question_refs` are the `seq`
numbers in the paper, so tapping one opens that question in the review screen. If the report fails or takes more than
10 minutes, `status` becomes `failed`, the credit is restored (`credit_restored: true`), and
`POST /v1/reports/{id}/retry` regenerates it at no charge.

Report actions: `POST /v1/reports/{id}/rating {"rating": 1-5, "comment"}` · `GET /v1/reports/{id}/pdf` ·
`POST /v1/reports/{id}/share` → `share_url` (web page) and `share_api_url` (public JSON, no token, 30 days) ·
`DELETE /v1/reports/{id}/share`.

## 6. Payments (Razorpay)

```http
GET  /v1/plans
POST /v1/orders                 {"plan_code": "credit_pack_10", "platform": "web|android|ios"}
POST /v1/orders/verify          {"razorpay_order_id", "razorpay_payment_id", "razorpay_signature"}
GET  /v1/me/credits             → {"total": 10, "next_expiry": "…", "grants": [{"remaining", "expires_at"}]}
GET  /v1/orders, GET /v1/orders/{id}, GET /v1/orders/{id}/invoice (PDF)
```

`POST /v1/orders` returns `checkout_options`. Pass that object straight to Razorpay Checkout (web
`new Razorpay(options)`, Android `Checkout.open(activity, JSONObject(options))`, iOS `razorpay.open(options)`). On the
success callback, send the three `razorpay_*` values to `/v1/orders/verify`; the response includes the new credit
balance. The webhook `POST /v1/webhooks/razorpay` (configure it in the Razorpay dashboard) does the same work on the
server, so credits arrive even if the app closes before `verify`; repeated webhooks never add credits twice.

Without Razorpay keys the backend uses a mock gateway (`"mock": true` in the order). Complete such orders with
`POST /v1/orders/{id}/mock-pay`, which works in development only.

Launch plans: free mini mock (once) · `pay_per_exam` ₹99 = 1 credit · `credit_pack_10` ₹399 = 10 credits. Credits
last 90 days and are used oldest-expiring first. Monthly/yearly auto-renew exists in the API (`/v1/subscriptions`)
but is inactive until UPI AutoPay mandates are set up (Phase 2).

## 7. Mock interview

```http
POST /v1/interviews             {"role_id", "level": "fresher|1-3|3-5", "language": "hi", "mode": "text",
                                 "job_description": "…", "use_profile_resume": true}   → session + first question
POST /v1/interviews/{id}/answer {"text": "…", "duration_sec": 35}  → {"done": false, "turn": {...}, "report_id": null}
GET  /v1/interviews/{id}        transcript (use it to restore the chat after a refresh)
POST /v1/interviews/{id}/resume after a disconnect (allowed once, within 10 minutes)
POST /v1/interviews/{id}/end    → evaluation starts
GET  /v1/interviews/{id}/report → scores (1–10) for role_knowledge, answer_structure, communication, confidence,
                                   resume_consistency; per_question good/missing/model_answer; red_flags; study_plan
```

An interview has 8–12 questions, at least 2 of them follow-ups (`turn.is_followup`), and runs introduction → resume
→ role/technical → situational → HR → closing (`turn.stage`, which can drive a progress bar). When `done` is true,
open the report screen and poll like an exam report. If the user disconnects for more than 10 minutes, the
interview is evaluated on what was answered.

### Interview WebSocket protocol (real-time text and voice)

`wss://<host>/v1/interviews/{id}/stream?token=<access-or-firebase-token>`

| Direction | Message |
|---|---|
| server → client | `{"type": "state", "interview": {...}}` on connect (the last interviewer turn is the current question) |
| client → server | `{"type": "answer", "text": "...", "duration_sec": 12}` |
| client → server | `{"type": "audio_chunk", "data": "<base64>"}` … then `{"type": "audio_end", "duration_sec": 12, "mime": "audio/webm"}` |
| server → client | `{"type": "transcript", "text": "..."}` (voice only) |
| server → client | `{"type": "question", "turn": {...}, "audio": null, "tts": "client"}` (`tts: client` means speak it with on-device TTS) |
| client → server | `{"type": "end"}` · `{"type": "ping"}` → `{"type": "pong"}` |
| server → client | `{"type": "ended", "report_id": "..."}` · `{"type": "error", "code", "message"}` |

Close codes: 4401 bad token, 4404 not found, 4409 interview ended. Reconnecting counts as the one allowed resume.
Voice uses a mock speech adapter today (see the status doc), so text over REST is the launch path.

## 8. Dashboard and notifications

```http
GET  /v1/me/progress            history, score_trend[], topic_heatmap[], credits, recommended[]
GET  /v1/me/notifications?unread_only=true   → items[{kind, title, body, data, read_at}], unread
POST /v1/me/notifications/{id}/read · POST /v1/me/notifications/read-all
POST /v1/me/devices             {"platform": "android|ios|web", "token": "<FCM token>"}   (push, Phase 2)
POST /v1/events                 {"name": "app_open|report_viewed|catalog_view|exam_view|paywall_view", "props": {}}
```

Notification `data` carries deep-link ids (`report_id`, `attempt_id`, `order_id`, `screen`). Kinds: `result_ready`,
`interview_report_ready`, `report_failed`, `payment_receipt`, `plan_expiring`, `practice_reminder`,
`refund_processed`. Emails go out for the same events when the user has an email address.

## 9. Admin (web only; role-based)

The roles are `founder` (all), `content_manager`, `subject_expert`, `language_reviewer`, `support`, `finance` and
`product`. Every write is audit-logged.

| Area | Endpoints |
|---|---|
| Flags | `GET /v1/admin/flags` · `PATCH /v1/admin/questions/{id}` with `{"action": "edit", ...fields}`, `{"action": "remove"}` or `{"action": "confirm_wrong", "correction": "..."}` (hides the question, saves the correction, writes an AI lesson, closes its flags) |
| Questions | `GET /v1/admin/questions`, `GET /v1/admin/questions/{id}`, `POST …/{id}/approve|quarantine|reject`, `PUT …/{id}/translations/{lang}`, `GET /v1/admin/review-queue`, `POST /v1/admin/question-reports/{id}/resolve` |
| Exams | `GET/POST/PATCH /v1/admin/exams`, `POST …/{id}/publish|hide`, `POST …/{id}/blueprints`, topics, `POST …/{id}/papers/generate`, `POST …/{id}/bank/build {"per_topic": 40}`, `GET …/{id}/generation-log` |
| AI memory | `GET/POST/PATCH /v1/admin/lessons`, `GET/PUT/DELETE /v1/admin/glossary` |
| Roles | `GET/POST/PATCH /v1/admin/interview-roles` |
| Users | `GET /v1/admin/users?q=`, `GET …/{id}`, `POST …/{id}/credits`, `POST …/{id}/credits/restore`, `POST …/{id}/block|unblock`, `PUT …/{id}/admin-role` |
| Money | `GET /v1/admin/payments`, `POST /v1/admin/orders/{id}/refund`, `GET /v1/admin/orders/{id}/invoice`, `GET /v1/admin/revenue`, `GET/PUT /v1/admin/plans`, `GET /v1/admin/subscriptions` |
| Stats | `GET /v1/admin/stats` (users, attempts, revenue, report rating, AI cost per attempt, report time), `GET /v1/admin/quality`, `GET /v1/admin/audit-log` |

## 10. API Plan sheet → actual endpoints

All 36 rows of the API Plan sheet are **Ready**:

| # | API Plan | Endpoint |
|---|---|---|
| 1 | Login | `POST /v1/auth/session` |
| 2–4, 30 | Profile, consent, delete | `GET/PATCH/DELETE /v1/me`, `POST /v1/me/consents` |
| 5–7 | Catalog | `GET /v1/exams`, `/v1/exams/{id}`, `/v1/interview-roles` |
| 8–12 | Mock exam | `POST /v1/attempts`, `GET /v1/attempts/{id}/paper`, `PUT …/answers`, `POST …/events`, `POST …/submit` |
| 13–16 | Report, review, rating, flags | `GET …/report`, `GET …/review`, `POST /v1/reports/{id}/rating`, `POST /v1/questions/{id}/flags` |
| 17–21 | Payments | `GET /v1/plans`, `POST /v1/orders`, `POST /v1/orders/verify`, `POST /v1/webhooks/razorpay`, `GET /v1/me/credits` |
| 22–27 | Interview | `POST /v1/interviews`, `POST …/{id}/answer`, `GET …/{id}`, `POST /v1/uploads/resume`, `POST …/{id}/end`, `GET …/{id}/report` |
| 28–29 | Dashboard, Hindi paper | `GET /v1/me/progress`, `GET /v1/attempts/{id}/paper?lang=hi` |
| 31–36 | Admin | `GET /v1/admin/flags`, `PATCH /v1/admin/questions/{id}`, `GET /v1/admin/users`, `POST /v1/admin/users/{id}/credits`, `GET /v1/admin/payments`, `GET /v1/admin/stats` |

## 11. Client checklist

- Store tokens securely: Keychain on iOS, EncryptedSharedPreferences on Android, memory plus an httpOnly cookie
  proxy or secure storage on the web.
- On 401, refresh once, then send the user to login.
- Exam screen: a local copy of answers, an autosave queue with `client_rev`, a timer from `server_time`, and
  recovery via `/paper`.
- Show report `processing` with polling; handle `failed` with its credit-restored message and a retry button.
- Razorpay: call `/orders/verify` on success, then refresh `/me/credits`.
- Copy-paste blocking and screenshot blocking (Android `FLAG_SECURE`) are client-side; only report them as events.
