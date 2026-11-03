import type { AuthSession } from '@prepmitra/shared';
import { API_ENDPOINTS, toMe } from '@prepmitra/shared';
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
  // The backend verifies the Firebase ID token, creates the user on first login and returns its own tokens.
  const auth = { headers: { Authorization: `Bearer ${idToken}` } };
  const { data } = await http.post(API_ENDPOINTS.authSession, { id_token: idToken }, auth);
  let me = data.user;
  if (profile?.name && !me.name) {
    me = await http.patch(API_ENDPOINTS.me, { name: profile.name, ...(profile.email ? { email: profile.email } : {}) }, auth).then((r) => r.data, () => me);
  }
  return {
    user: toMe(me).user,
    tokens: {
      accessToken: data.access_token,
      refreshToken: data.refresh_token,
      expiresAt: new Date(Date.now() + data.expires_in * 1000).toISOString(),
    },
    isNewUser: !!data.is_new_user || !me.profile_complete,
  };
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

  /** Re-exchanges the current Firebase user's token (page reload). */
  async restore(): Promise<AuthSession | null> {
    const auth = await getFirebaseAuth();
    await auth.authStateReady();
    return auth.currentUser ? exchangeSession(await auth.currentUser.getIdToken()) : null;
  },

  async signOut(): Promise<void> {
    if (!firebaseEnabled() || !authPromise) return;
    const auth = await authPromise;
    await auth.signOut();
    setTokenProvider(null);
  },
};
