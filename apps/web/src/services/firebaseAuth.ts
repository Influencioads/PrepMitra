import type { AuthSession } from '@prepmitra/shared';
import { API_ENDPOINTS } from '@prepmitra/shared';
import type { Auth, ConfirmationResult, RecaptchaVerifier } from 'firebase/auth';
import { env, firebaseEnabled } from '@/utils/env';
import { http, setTokenProvider } from './http';

/**
 * Firebase Authentication adapter (15-day plan, Day 2): phone OTP + Google
 * sign-in. Loaded lazily and ONLY when VITE_AUTH_PROVIDER=firebase and the
 * VITE_FIREBASE_* values are set, so demo mode never downloads the SDK.
 * After Firebase signs the user in, the ID token is exchanged at POST /v1/auth/session.
 */
export const RECAPTCHA_CONTAINER_ID = 'pm-recaptcha';

let authPromise: Promise<Auth> | null = null;
let verifier: RecaptchaVerifier | null = null;
const confirmations = new Map<string, ConfirmationResult>();

async function getFirebaseAuth(): Promise<Auth> {
  if (!firebaseEnabled()) throw new Error('Firebase authentication is not configured.');
  authPromise ??= (async () => {
    const [{ initializeApp }, { getAuth }] = await Promise.all([import('firebase/app'), import('firebase/auth')]);
    const app = initializeApp(env.firebase);
    const auth = getAuth(app);
    auth.languageCode = document.documentElement.lang || 'en';
    setTokenProvider(async () => (auth.currentUser ? auth.currentUser.getIdToken() : null));
    return auth;
  })();
  return authPromise;
}

async function exchangeSession(idToken: string, profile?: { name: string; email?: string }): Promise<AuthSession> {
  const res = await http.post<AuthSession>(
    API_ENDPOINTS.authSession,
    { profile },
    { headers: { Authorization: `Bearer ${idToken}` } },
  );
  return res.data;
}

export const firebaseAuth = {
  enabled: firebaseEnabled,

  /** Sends the SMS through Firebase. Returns a request id the verify step uses. */
  async sendOtp(phone: string): Promise<string> {
    const auth = await getFirebaseAuth();
    const { RecaptchaVerifier, signInWithPhoneNumber } = await import('firebase/auth');
    verifier ??= new RecaptchaVerifier(auth, RECAPTCHA_CONTAINER_ID, { size: 'invisible' });
    const confirmation = await signInWithPhoneNumber(auth, `+91${phone}`, verifier);
    const requestId = `fb-${phone}-${Date.now()}`;
    confirmations.set(requestId, confirmation);
    return requestId;
  },

  async verifyOtp(requestId: string, code: string, profile?: { name: string; email?: string }): Promise<AuthSession> {
    const confirmation = confirmations.get(requestId);
    if (!confirmation) throw new Error('This code has expired. Request a new one.');
    const cred = await confirmation.confirm(code);
    confirmations.delete(requestId);
    return exchangeSession(await cred.user.getIdToken(), profile);
  },

  async google(): Promise<AuthSession> {
    const auth = await getFirebaseAuth();
    const { GoogleAuthProvider, signInWithPopup } = await import('firebase/auth');
    const cred = await signInWithPopup(auth, new GoogleAuthProvider());
    return exchangeSession(await cred.user.getIdToken());
  },

  async signOut(): Promise<void> {
    if (!firebaseEnabled() || !authPromise) return;
    const auth = await authPromise;
    await auth.signOut();
    setTokenProvider(null);
  },
};
