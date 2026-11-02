/** Runtime configuration. Only non-secret values belong here — VITE_* vars ship to the browser. */
const e = import.meta.env;

export const env = {
  apiBaseUrl: e.VITE_API_BASE_URL ?? 'http://localhost:8080',
  useMockApi: e.VITE_USE_MOCK_API !== 'false',
  /** 'demo' (default) or 'firebase' (needs the VITE_FIREBASE_* values). */
  authProvider: e.VITE_AUTH_PROVIDER === 'firebase' ? 'firebase' : 'demo',
  firebase: {
    apiKey: e.VITE_FIREBASE_API_KEY ?? '',
    authDomain: e.VITE_FIREBASE_AUTH_DOMAIN ?? '',
    projectId: e.VITE_FIREBASE_PROJECT_ID ?? '',
    appId: e.VITE_FIREBASE_APP_ID ?? '',
  },
  /** Razorpay publishable key id (rzp_test_… / rzp_live_…). Never the secret. */
  razorpayKeyId: e.VITE_RAZORPAY_KEY_ID ?? '',
  /** 'full' (default) or 'launch' (15-day MVP: free, ₹99, ₹399 pack). */
  pricingSet: e.VITE_PRICING_SET === 'launch' ? 'launch' : 'full',
  sentryDsn: e.VITE_SENTRY_DSN ?? '',
  analyticsDebug: e.DEV || e.VITE_ANALYTICS_DEBUG === 'true',
} as const;

export const firebaseEnabled = () =>
  env.authProvider === 'firebase' && !!env.firebase.apiKey && !!env.firebase.authDomain && !!env.firebase.projectId && !!env.firebase.appId;
