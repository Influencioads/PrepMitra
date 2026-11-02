# PrepMitra AI — mobile app

Native iOS/Android app for **PrepMitra AI** (React Native 0.88 + Expo SDK 58 + TypeScript + Expo Router).
This is a **frontend prototype**: all data comes from the shared seeded mocks in `@prepmitra/shared`
and simulated services. OTP, payments, AI analysis and voice are simulated, and no backend is required.

## Run it

```bash
# 1. Install once from the monorepo root (npm workspaces; one shared node_modules)
cd prepmitra-ai
npm install

# 2. Start the Expo dev server from the mobile app
cd apps/mobile
npx expo start          # or: npm run start --workspace @prepmitra/mobile (from the root)
```

Then:

- **Expo Go**: scan the QR code with the Expo Go app (Android) or the Camera app (iOS).
  Every native module used here (safe-area, screens, svg, async-storage, document-picker,
  vector-icons) ships in Expo Go, so no development build is needed.
- **Emulator/simulator**: press `a` (Android emulator) or `i` (iOS simulator) in the terminal.

Useful commands (from `apps/mobile`):

| Command | What it does |
| --- | --- |
| `npx tsc --noEmit` | Typecheck |
| `npx expo export --platform android` / `--platform ios` | Production bundle without a device |
| `npx expo-doctor` | Dependency/config health check (needs network) |

## Demo login

| Flow | How |
| --- | --- |
| Returning learner with history | Log in with **9876543210**, code **123456** (or “Continue with Google (demo)”) |
| New learner | Sign up with any valid number (starts with 6–9), code **123456**. You get an empty account with a free 30-minute mini mock and a 6-step onboarding |

A returning login seeds the same demo history as the web app: 7 past mocks, 1 interview report,
the Monthly plan with 6 credits, and notifications. Data is stored on the device with AsyncStorage
and kept per user. Logging out keeps it; **Settings → Delete account** wipes it.

## Environment variables

Copy `.env.example` to `.env`:

| Variable | Default | Purpose |
| --- | --- | --- |
| `EXPO_PUBLIC_API_BASE_URL` | `http://localhost:8080` | Base URL of the future `/v1` API |
| `EXPO_PUBLIC_USE_MOCK_API` | `true` | Any value other than `false` uses the on-device mock services |

`EXPO_PUBLIC_*` values are compiled into the bundle, so never put secrets in them.

## Structure

```
src/
  app/          Expo Router routes (file = screen, _layout = navigator)
    (auth)/     welcome, login, signup, verify-otp      (signed-out only)
    onboarding  6-step profile wizard                     (signed-in, profile incomplete)
    (tabs)/     home, explore, practice, reports, profile (signed-in + onboarded)
    exams/[id]/, exam/[attemptId], exam-result/[reportId], reports/[reportId],
    interviews/, interview/session/[sessionId], interview/report/[reportId],
    progress, subscription, notifications, settings, edit-profile
  components/   Reusable native UI (Button, Input, Select, BottomSheet, charts, palette…)
  features/     Feature-specific pieces (onboarding steps, interview chat/voice, checkout…)
  hooks/        useAsync, useProgress, useNow, useResumePicker, useReducedMotion
  services/     axios client + mock/real services (auth, profile, exam, attempt, report…)
  store/        Zustand stores persisted to AsyncStorage + demo-data bootstrap
  theme/        Re-exports the shared design tokens + native shadows/type scale
  utils/        env, icon mapping, link mapping, share-text builders
```

Scoring, palette states, interview scripting, report building and progress maths all come
from `@prepmitra/shared`; the app does not reimplement them.

**Auth gating.** The root `_layout.tsx` waits for every persisted store to rehydrate and shows
a splash meanwhile. It then uses `Stack.Protected` guards: `(auth)` is available only while
signed out, `onboarding` only while the profile is incomplete, and everything else only when
signed in and onboarded. When a guard flips (sign-in, finishing onboarding, logout or delete),
the router lands on `/`, which redirects to the right place. These guards only control the UI;
the backend must enforce real authorization.

## Prototype limitations

- **OTP**: no SMS is sent. The code is always `123456`, and the app says so on screen.
- **Payments**: demo checkout only. You pick a plan and a payment-method *label*, and credits are
  added locally. The app has no card, UPI or bank fields anywhere.
- **AI**: reports and interview feedback come from deterministic rules in `@prepmitra/shared` and
  are labelled “Demo analysis”.
- **Voice interview**: simulated. The microphone, speech-to-text and text-to-speech are never used;
  the interviewer's “speech” and your “recording” are timers. The transcript is an editable scaffold.
- **Exam timer**: runs on the device and is derived from the attempt's absolute end time, so it
  keeps counting while the app is closed. In production the server controls the clock.
- **Resume upload**: picked with the system document picker and validated (PDF/DOCX, ≤ 5 MB), but never
  uploaded anywhere.
- **Share/download**: reports and “my data” are shared as plain text or JSON through the native share sheet.
  Production would share a server-generated PDF.
