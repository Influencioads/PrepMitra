import type { AuthSession, User } from '@prepmitra/shared';
import { API_ENDPOINTS, DEMO_ADMIN, DEMO_OTP, DEMO_USER } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';
import { firebaseAuth } from './firebaseAuth';

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

/**
 * Auth service. Demo mode (default) simulates OTP with code 123456 and sends no SMS.
 * With VITE_AUTH_PROVIDER=firebase, Firebase sends/verifies the OTP and the ID token
 * is exchanged at POST /v1/auth/session, which creates the user on first login.
 */
export const authService = {
  async sendOtp(req: OtpRequest): Promise<OtpRequestResult> {
    if (firebaseAuth.enabled()) return { requestId: await firebaseAuth.sendOtp(req.phone), expiresInSec: 60 };
    await delay(600);
    return { requestId: `otp-${req.phone}-${Date.now()}`, expiresInSec: 120, demoCode: DEMO_OTP };
  },

  async verifyOtp(input: VerifyOtpInput): Promise<AuthSession> {
    if (firebaseAuth.enabled()) return firebaseAuth.verifyOtp(input.requestId, input.otp, input.signup);
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
    await delay(800);
    return { user: DEMO_USER, tokens: fakeTokens(), isNewUser: false };
  },

  async demoAdminSignIn(): Promise<AuthSession> {
    await delay(500);
    return { user: DEMO_ADMIN, tokens: fakeTokens(), isNewUser: false };
  },

  /** Restores the profile for an already signed-in Firebase user (POST /v1/auth/session). */
  async refreshSession(): Promise<AuthSession | null> {
    if (USE_MOCK) return null;
    return (await http.post<AuthSession>(API_ENDPOINTS.authSession, {})).data;
  },

  async logout(): Promise<void> {
    await firebaseAuth.signOut().catch(() => undefined);
    if (!USE_MOCK) return;
    await delay(200);
  },
};
