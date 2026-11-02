# PrepMitra AI — Frontend

Your Personal AI Exam & Interview Coach. Frontend prototype (mock data, simulated services) for:

- `apps/web` — React 19 + TypeScript + Vite + Tailwind CSS v4 + React Router 7 + Zustand + React Hook Form + Zod + Recharts
- `apps/mobile` — React Native + Expo SDK 58 + Expo Router (native screens, no WebView) — see `apps/mobile/README.md`
- `packages/shared` — types, constants, Zod schemas, design tokens, mock data, and pure logic (scoring, palette states, reports, interview script, progress)

## Run

```bash
npm install                 # from the repo root (Node 20.19+)

npm run dev:web             # website at http://localhost:5173
npm run build:web           # production build (tsc -b && vite build)
npm test                    # shared unit tests + web unit/integration tests

cd apps/mobile && npx expo start   # mobile: scan with Expo Go or press a / i
```

Static hosting without SPA rewrites: `VITE_ROUTER_MODE=hash VITE_BASE=./ npm run build:web`.

```bash
npm run lint                # ESLint (web)
npm run ci                  # lint + typecheck + tests + build — the same checks CI runs
```

## CI and preview deploys

- `.github/workflows/ci.yml` runs lint, typecheck, tests and the web build on every push and pull request.
- Vercel: import the GitHub repo, set **Root Directory** to `apps/web`. `apps/web/vercel.json` holds the install/build commands and SPA rewrites, so every push gets a preview URL. Add the `VITE_*` variables from `apps/web/.env.example` in the Vercel project settings.
- Folder layout follows the 15-day plan: `src/app` (router, providers), `src/components`, `src/lib/api` (HTTP client, endpoints, services), `src/i18n` (English + Hindi). The plan names Next.js; this project uses React + Vite as agreed in the original brief.

## Demo accounts

- Learner: mobile `9876543210`, OTP `123456` (seeded history, 6 credits)
- New user: sign up with any valid number → onboarding → free 30-min mini mock
- Admin: on /login click "Open demo admin console" (or `9000000001` / `123456`)

## Backend integration

Every service in `apps/web/src/services` (and `apps/mobile/src/services`) has a mock branch and a real axios branch hitting the `/v1` endpoints in `packages/shared/src/constants`. Set `VITE_USE_MOCK_API=false` and `VITE_API_BASE_URL` (web) or `EXPO_PUBLIC_*` (mobile). No secrets belong in frontend env files.

## Prototype limitations

- OTP, Google sign-in, payments, AI evaluation, speech-to-text/text-to-speech and resume upload are simulated. No SMS is sent; no payment details are collected.
- The exam timer runs on the client; in production it must be server-controlled.
- Route guards are UI-only. Real authorization must be enforced by the backend (JWT + role-based access on `/v1/admin/*`).
- Data persists in localStorage (web) / AsyncStorage (mobile) on the device only.
