# Testing the API in Swagger

## 1. Start the server (no Docker, no API keys)

```bash
cd backend && .venv/Scripts/python scripts/dev_server.py
```

This uses a local SQLite file (`backend/dev.db`), the **mock AI** and the **mock payment gateway**. It seeds 15 exams,
6 interview roles and 4 plans on the first run. Open **http://localhost:8000/docs** (the port is printed on startup).
The phone number `9000000009` becomes a **founder admin** at first login, so you can test the admin APIs too.
Delete `backend/dev.db` to start over.

## 2. Log in and authorize

1. `POST /v1/auth/otp/send` → body `{"phone": "9000000009"}` → copy `dev_otp` from the response
   (shown only in development; production sends an SMS).
2. `POST /v1/auth/otp/verify` → body `{"phone": "9000000009", "code": "<dev_otp>"}` → copy `access_token`.
3. Click **Authorize** (top right), paste the `access_token` (without the word "Bearer"), click **Authorize**, then
   **Close**. The token survives page reloads. Access tokens last 15 minutes; get a new one with
   `POST /v1/auth/refresh` and `{"refresh_token": "..."}`.

## 3. Complete the profile (required before the first exam)

- `POST /v1/me/consents` → `{"data_processing": true, "recruiter_sharing": false}`
- `PATCH /v1/me` →
  `{"name": "Asha Kumar", "dob": "2000-05-14", "preferred_language": "ta", "target_exam_ids": ["ssc-cgl-tier1"]}`
- `GET /v1/me` → `profile_complete` should be `true`.

## 4. Take the free mini mock

1. `GET /v1/exams` → copy the `id` of `mini-mock-general-aptitude` (`is_free_trial: true`).
2. `POST /v1/attempts` → `{"exam_id": "<id>", "language": "ta"}` → 30 questions, `remaining_seconds` ≈ 1800.
   Each question has `content` (Tamil) and `content_en` (English toggle). Copy the attempt `id` and a few
   `question_id`s.
3. `PUT /v1/attempts/{attempt_id}/answers` →
   ```json
   {"answers": [{"question_id": "<qid>", "answer": "A", "client_rev": 1, "time_spent_sec": 40,
                 "marked_for_review": false}]}
   ```
   Send the same body again: `saved: 0, ignored_stale: 1` (idempotent autosave). Use `["A","C"]` for
   multiple-correct questions and a number for numeric ones; `"answer": null` clears a response.
4. `POST /v1/attempts/{attempt_id}/events` → `{"events": [{"type": "tab_switch"}]}` (anti-cheat log).
5. `GET /v1/attempts/{attempt_id}` → resume view with saved answers and the server's remaining time.
6. `POST /v1/attempts/{attempt_id}/submit` → score now, `report_status: "processing"`.
7. `GET /v1/attempts/{attempt_id}/report` → poll until `status: "ready"` (a second or two with the mock AI).
8. `GET /v1/attempts/{attempt_id}/review` → correct answers + explanations.
9. `GET /v1/reports/{report_id}/pdf` → Swagger shows a **Download file** link.
10. `POST /v1/reports/{report_id}/rating` → `{"rating": 5}`; `POST /v1/reports/{report_id}/share` → `share_api_url`
    opens without a token.

Starting the mini mock a second time returns **402 insufficient_credits**, because the free trial is one-time.

## 5. Buy credits (mock gateway)

1. `GET /v1/plans`
2. `POST /v1/orders` → `{"plan_code": "monthly", "platform": "web"}` → copy `order_id`.
3. `POST /v1/orders/{order_id}/mock-pay` (dev only) → status `paid`, 10 credits.
4. `GET /v1/me/credits`, `GET /v1/orders/{order_id}/invoice` (GST invoice PDF), `GET /v1/subscriptions`,
   `POST /v1/subscriptions/{id}/cancel`.

## 6. Mock interview (text, over REST)

1. `GET /v1/interview-roles` → copy a role `id`.
2. `POST /v1/interviews` →
   `{"role_id": "<id>", "level": "fresher", "language": "en", "mode": "text", "job_description": "Junior Python developer"}`
   → the first question is in `transcript`.
3. `POST /v1/interviews/{id}/turns` → `{"text": "your answer"}` repeatedly (about 10 times) until `done: true`,
   or `POST /v1/interviews/{id}/end` to stop early.
4. `GET /v1/interviews/{id}/report` → 5 rubric scores (1–10), per-answer feedback, red flags, a 7-day plan.

The real-time **WebSocket** (`/v1/interviews/{id}/stream?token=...`) cannot be tested in Swagger. Use a WebSocket
client such as Postman or `wscat`; see the protocol in [docs/API.md](API.md).

## 7. Dashboard, notifications

- `GET /v1/me/progress` → history, score trend, topic heatmap, credits, recommendations.
- `GET /v1/me/notifications` → "result ready", "payment received" and similar items.
- `POST /v1/me/devices` → `{"platform": "android", "token": "test-fcm-token-123"}`.

## 8. Admin (logged in as 9000000009)

- `GET /v1/admin/exams`, `POST /v1/admin/exams/{id}/papers/generate` → `{"count": 1}`
- `GET /v1/admin/questions?exam_id=...`, `GET /v1/admin/review-queue`
- `GET /v1/admin/users?q=Asha`, `POST /v1/admin/users/{id}/credits` → `{"credits": 2, "note": "goodwill"}`
- `GET /v1/admin/quality`, `GET /v1/admin/revenue`, `GET /v1/admin/audit-log`

Log in with another phone number (for example `9876543210`) to check that a non-admin gets **403** on `/v1/admin/...`.

## Errors

Every error has the same shape, so it is easy to check in Swagger:

```json
{"error": {"code": "insufficient_credits", "message": "You have no exam credits left. Buy a plan to continue."}}
```

Validation errors add `details: [{"field": "...", "message": "..."}]`.
