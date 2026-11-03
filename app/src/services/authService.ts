import type { AuthSession, User } from '@prepmitra/shared';
import { API_ENDPOINTS, DEMO_OTP, DEMO_USER } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';

export interface OtpRequest {
  phone: string;
  purpose: 'login' | 'signup';
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

export const authService = {
  /**
   * The mock does NOT send any SMS. In production the OTP is sent and verified by
   * Firebase Authentication on the device (native SDK, Phase 2), and the resulting
   * ID token is exchanged at POST /v1/auth/session.
   */
  async sendOtp(req: OtpRequest): Promise<OtpRequestResult> {
    if (!USE_MOCK) throw mockError(501, 'FIREBASE_REQUIRED', 'Phone login on the app needs the Firebase native SDK (Phase 2).');
    await delay(600);
    return { requestId: `otp-${req.phone}-${Date.now()}`, expiresInSec: 120, demoCode: DEMO_OTP };
  },

  /** POST /v1/auth/session with the Firebase ID token (real mode). */
  async verifyOtp(input: VerifyOtpInput): Promise<AuthSession> {
    if (!USE_MOCK) return (await http.post<AuthSession>(API_ENDPOINTS.authSession, { idToken: input.otp, profile: input.signup })).data;
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
    return { user: { ...DEMO_USER, phone: input.phone }, tokens: fakeTokens(), isNewUser: false };
  },

  /** Simulated; no Google account is contacted. Production: Firebase Google sign-in → POST /v1/auth/session. */
  async googleSignIn(): Promise<AuthSession> {
    if (!USE_MOCK) throw mockError(501, 'FIREBASE_REQUIRED', 'Google sign-in on the app needs the Firebase native SDK (Phase 2).');
    await delay(800);
    return { user: DEMO_USER, tokens: fakeTokens(), isNewUser: false };
  },

  async logout(): Promise<void> {
    if (!USE_MOCK) {
      await http.post('/v1/auth/logout').catch(() => undefined);
      return;
    }
    await delay(200);
  },
};
