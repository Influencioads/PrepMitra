# PrepMitra AI

Your Personal AI Exam & Interview Coach: AI mock exams and AI mock interviews in English and Indian languages,
with automated reports.

| Folder | What it is |
|---|---|
| `frontend/` | Website + PWA: React 19, TypeScript, Vite, Tailwind CSS v4, React Router 7, Zustand |
| `app/` | Android/iOS app: React Native, Expo SDK 58, Expo Router (see `app/README.md`) |
| `shared/` | Code used by both `frontend/` and `app/`: types, constants, design tokens, demo data, pure logic, and the backend adapters (`shared/src/api`) |
| `docs/` | `API_CONTRACT.md` (screens ⇄ endpoints) |

The backend (FastAPI) is developed on the `integrate-backend` branch.

## Run the website locally (no keys needed)

From the repo root (Node 20.19+):

```bash
npm install
```

```bash
npm run dev:web
```

Open http://localhost:5173. Without `frontend/.env.local` the website runs on in-browser demo data (log in with any
number; the code is 123456).

To use the backend (from the `integrate-backend` branch) instead, start it on port 8000 and create `frontend/.env.local` with

```
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCK_API=false
VITE_PRICING_SET=launch
```

then run `npm run dev:web` again. With a development backend, any mobile number works and the verify screen shows the
code (no SMS is sent).

Mobile app (still on demo data, see below):

```bash
cd app && npx expo start
```

## How the website talks to the backend

- `frontend/src/services/*` — one service per area; each has a demo branch and a real branch (`VITE_USE_MOCK_API`).
- `shared/src/api/adapters.ts` — maps backend JSON to the frontend types and back (IDs, answers, reports, plans…).
- `shared/src/api/live.ts` — exams, roles and questions loaded from the backend; `getExamById`, `getRoleById` and
  `getQuestionById` read it first, so the screens work unchanged.
- `frontend/src/store/sync.ts` — after sign-in and on every app start, loads the user's profile, credits, past
  reports, interviews and notifications from the backend into the stores the screens read.
- The server is the source of truth for timers, scoring, credits and roles. Access tokens (15 min) refresh
  automatically.

Admin console with the real API: users (credits, block), payments (refunds), review queue (flagged questions) and
the question bank use the backend. Exam editor, roles, AI lessons, languages, team and settings are Phase 2 and
stay on demo data on the device.

## Tests

```bash
npm test
```

End-to-end check of the website's services against a running backend (signup → onboarding → free mini mock →
report → ₹399 pack → interview → admin), with the backend on port 8001:

```bash
cd frontend && VITE_LIVE_API=1 VITE_USE_MOCK_API=false VITE_API_BASE_URL=http://localhost:8001 npx vitest run src/test/live-backend.test.ts
```

## CI and deploys

- `.github/workflows/ci.yml` — website/app/shared: lint, typecheck, tests, web build.
- Vercel: set **Root Directory** to `frontend` (`frontend/vercel.json` holds the build and SPA rewrites) and add the
  `VITE_*` variables from `frontend/.env.example`.

## Not connected yet

- The mobile app (`app/`) still uses on-device demo services; it can reuse `shared/src/api` the same way.
- Google sign-in needs Firebase (`VITE_AUTH_PROVIDER=firebase` + `FIREBASE_PROJECT_ID` on the backend).
- Real AI, payments, email: configured on the backend (`integrate-backend` branch).
