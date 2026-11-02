import type { AuthSession, User } from '@prepmitra/shared';
import { API_ENDPOINTS, DEMO_ADMIN, DEMO_OTP, DEMO_USER, toMe, toMePatch } from '@prepmitra/shared';
import type { Json } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';
import { firebaseAuth } from './firebaseAuth';
import { useAuthStore } from '@/store/authStore';

export interface OtpRequest {
  phone: string;
  purpose: 'login' | 'signup' | 'recovery';
}

export interface OtpRequestResult {
  requestId: string;
  expiresInSec: number;
  /** Mock only: tells the UI which code the simulated service accepts. */
  demoCode?: string;
}

export interface VerifyOtpInput {
  requestId: string;
  phone: string;
  otp: string;
  signup?: { name: string; email?: string };
}

const fakeTokens = () => ({
  accessToken: `demo-access-${Date.now().toString(36)}`,
  refreshToken: `demo-refresh-${Date.now().toString(36)}`,
  expiresAt: new Date(Date.now() + 3600_000).toISOString(),
});

/** Phone OTP + profile from the real backend (POST /v1/auth/otp/verify, then GET /v1/me). */
async function backendSession(tokens: Json, signup?: { name: string; email?: string }): Promise<AuthSession> {
  const auth = { headers: { Authorization: `Bearer ${tokens.access_token}` } };
  let me = (await http.get(API_ENDPOINTS.me, auth)).data;
  if (signup && !me.name) {
    me = await http.patch(API_ENDPOINTS.me, toMePatch({ user: { name: signup.name, email: signup.email } }), auth).then((r) => r.data, () => me);
  }
  return {
    user: toMe(me).user,
    tokens: {
      accessToken: tokens.access_token,
      refreshToken: tokens.refresh_token,
      expiresAt: new Date(Date.now() + tokens.expires_in * 1000).toISOString(),
    },
    isNewUser: !!tokens.is_new_user || !me.profile_complete,
  };
}

/** Founder admin seeded by `backend/scripts/dev_server.py` (BOOTSTRAP_ADMIN_PHONE). */
const DEV_ADMIN_PHONE = '9000000009';

/**
 * Auth service. Demo mode (default) simulates OTP with code 123456 and sends no SMS.
 * With VITE_AUTH_PROVIDER=firebase, Firebase sends/verifies the OTP and the ID token
 * is exchanged at POST /v1/auth/session, which creates the user on first login.
 */
export const authService = {
  async sendOtp(req: OtpRequest): Promise<OtpRequestResult> {
    if (firebaseAuth.enabled()) return { requestId: await firebaseAuth.sendOtp(req.phone), expiresInSec: 60 };
    if (!USE_MOCK) {
      // The backend returns the code as dev_otp only when it runs with APP_ENV=development.
      const { data } = await http.post('/v1/auth/otp/send', { phone: req.phone });
      return { requestId: `otp-${req.phone}-${Date.now()}`, expiresInSec: data.expires_in, demoCode: data.dev_otp ?? undefined };
    }
    await delay(600);
    return { requestId: `otp-${req.phone}-${Date.now()}`, expiresInSec: 120, demoCode: DEMO_OTP };
  },

  async verifyOtp(input: VerifyOtpInput): Promise<AuthSession> {
    if (firebaseAuth.enabled()) return firebaseAuth.verifyOtp(input.requestId, input.otp, input.signup);
    if (!USE_MOCK) {
      const { data } = await http.post('/v1/auth/otp/verify', { phone: input.phone, code: input.otp });
      return backendSession(data, input.signup);
    }
    await delay(700);
    if (input.otp !== DEMO_OTP) throw mockError(400, 'OTP_INVALID', 'That code is incorrect. In demo mode, use 123456.');
    if (input.signup) {
      const user: User = {
        id: `user-${input.phone}`,
        name: input.signup.name,
        phone: input.phone,
        email: input.signup.email || undefined,
        preferredLanguage: 'en',
        role: 'user',
        createdAt: new Date().toISOString(),
        onboardingComplete: false,
      };
      return { user, tokens: fakeTokens(), isNewUser: true };
    }
    const base = input.phone === DEMO_ADMIN.phone ? DEMO_ADMIN : { ...DEMO_USER, phone: input.phone };
    return { user: base, tokens: fakeTokens(), isNewUser: false };
  },

  /** Simulated in demo mode; no Google account is contacted. */
  async googleSignIn(): Promise<AuthSession> {
    if (firebaseAuth.enabled()) return firebaseAuth.google();
    if (!USE_MOCK) throw mockError(501, 'GOOGLE_NOT_CONFIGURED', 'Google sign-in needs Firebase (VITE_AUTH_PROVIDER=firebase). Use your mobile number for now.');
    await delay(800);
    return { user: DEMO_USER, tokens: fakeTokens(), isNewUser: false };
  },

  async demoAdminSignIn(): Promise<AuthSession> {
    if (!USE_MOCK) {
      // Development backends only: sign in as the seeded founder admin with the returned dev OTP.
      const sent = (await http.post('/v1/auth/otp/send', { phone: DEV_ADMIN_PHONE })).data;
      if (!sent.dev_otp) throw mockError(403, 'ADMIN_DEMO_DISABLED', 'Demo admin sign-in only works with a development backend. Sign in with your admin phone number.');
      return backendSession((await http.post('/v1/auth/otp/verify', { phone: DEV_ADMIN_PHONE, code: sent.dev_otp })).data);
    }
    await delay(500);
    return { user: DEMO_ADMIN, tokens: fakeTokens(), isNewUser: false };
  },

  /** Restores the profile for an already signed-in Firebase user (POST /v1/auth/session). */
  async refreshSession(): Promise<AuthSession | null> {
    if (USE_MOCK || !firebaseAuth.enabled()) return null;
    return firebaseAuth.restore();
  },

  async logout(): Promise<void> {
    await firebaseAuth.signOut().catch(() => undefined);
    if (!USE_MOCK) {
      const refreshToken = useAuthStore.getState().session?.tokens.refreshToken;
      if (refreshToken) await http.post('/v1/auth/logout', { refresh_token: refreshToken }).catch(() => undefined);
      return;
    }
    await delay(200);
  },
};
