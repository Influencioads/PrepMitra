import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom';
import type { AuthSession, User } from '@prepmitra/shared';
import { DEMO_OTP, DEMO_USER, EMPTY_PROFILE, isProfileReady } from '@prepmitra/shared';
import { RequireAuth, RequireReadyProfile } from '@/app/guards';
import { OnboardingPage } from '@/pages/auth/OnboardingPage';
import axios from 'axios';
import type { AxiosAdapter } from 'axios';
import { http } from '@/services/http';
import { profileService } from '@/services/profileService';
import { authService } from '@/services/authService';
import { useAuthStore, useProfileStore } from '@/store';

const baseUser: User = {
  id: 'u-new',
  name: 'Ananya Rao',
  phone: '9876500000',
  dob: '1999-05-10',
  preferredLanguage: 'en',
  role: 'user',
  createdAt: new Date(0).toISOString(),
  onboardingComplete: true,
};
const session = (user: Partial<User> = {}): AuthSession => ({
  user: { ...baseUser, ...user },
  tokens: { accessToken: 't', refreshToken: 'r', expiresAt: new Date(Date.now() + 3600_000).toISOString() },
  isNewUser: false,
});

function Where() {
  const l = useLocation();
  return <p data-testid="where">{l.pathname + l.search}</p>;
}

function renderGuarded(initial: string) {
  return render(
    <MemoryRouter initialEntries={[initial]}>
      <Routes>
        <Route path="/exams/:id/instructions" element={<RequireAuth><RequireReadyProfile><p>Instructions page</p></RequireReadyProfile></RequireAuth>} />
        <Route path="*" element={<Where />} />
      </Routes>
    </MemoryRouter>,
  );
}

afterEach(() => {
  vi.restoreAllMocks();
  useAuthStore.setState({ session: null, pending: null });
  useProfileStore.setState({ ownerId: null, profile: EMPTY_PROFILE, draft: null });
});

describe('Day 2 · login', () => {
  it('sends logged-out users to login with the page they wanted', () => {
    renderGuarded('/exams/ssc-cgl/instructions');
    expect(screen.getByTestId('where')).toHaveTextContent('/login?redirect=%2Fexams%2Fssc-cgl%2Finstructions');
  });

  it('on a 401 refreshes the access token once and retries the request', async () => {
    useAuthStore.getState().signIn(session());
    const seen: (string | undefined)[] = [];
    const adapter: AxiosAdapter = async (config) => {
      seen.push(String(config.headers.Authorization));
      if (seen.length === 1) throw Object.assign(new Error('401'), { config, isAxiosError: true, response: { status: 401, data: {}, config } });
      return { data: { ok: true }, status: 200, statusText: 'OK', headers: {}, config };
    };
    vi.spyOn(axios, 'post').mockResolvedValue({ data: { access_token: 'fresh', refresh_token: 'r2', expires_in: 900 } });
    const original = http.defaults.adapter;
    http.defaults.adapter = adapter;
    try {
      await expect(http.get('/v1/me')).resolves.toMatchObject({ data: { ok: true } });
      expect(seen).toEqual(['Bearer t', 'Bearer fresh']);
      expect(useAuthStore.getState().session?.tokens).toMatchObject({ accessToken: 'fresh', refreshToken: 'r2' });
    } finally {
      http.defaults.adapter = original;
    }
  });

  it('signs the user out when the refresh token is no longer valid', async () => {
    useAuthStore.getState().signIn(session());
    vi.spyOn(axios, 'post').mockRejectedValue(new Error('refresh rejected'));
    const original = http.defaults.adapter;
    http.defaults.adapter = async (config) => {
      throw Object.assign(new Error('401'), { config, isAxiosError: true, response: { status: 401, data: {}, config } });
    };
    try {
      await expect(http.get('/v1/me')).rejects.toMatchObject({ status: 401 });
      expect(useAuthStore.getState().session).toBeNull();
    } finally {
      http.defaults.adapter = original;
    }
  });

  it('does not try to refresh on a failed login call', async () => {
    const post = vi.spyOn(axios, 'post');
    const original = http.defaults.adapter;
    http.defaults.adapter = async (config) => {
      throw Object.assign(new Error('401'), { config, isAxiosError: true, response: { status: 401, data: {}, config } });
    };
    try {
      await expect(http.post('/v1/auth/otp/verify', {})).rejects.toMatchObject({ status: 401 });
      expect(post).not.toHaveBeenCalled();
    } finally {
      http.defaults.adapter = original;
    }
  });
});

describe('Day 2 · demo login sends new numbers to onboarding', () => {
  it('treats an unknown number as a new user and the seeded learner as returning', async () => {
    localStorage.removeItem('pm.demoAccounts');
    const fresh = await authService.verifyOtp({ requestId: 'r', phone: '9000012345', otp: DEMO_OTP });
    expect(fresh.isNewUser).toBe(true);
    expect(fresh.user.onboardingComplete).toBe(false);
    const demo = await authService.verifyOtp({ requestId: 'r', phone: DEMO_USER.phone, otp: DEMO_OTP });
    expect(demo.isNewUser).toBe(false);
    expect(demo.user.onboardingComplete).toBe(true);
  });
});

describe('Day 2 · exams stay locked until the profile is ready', () => {
  it('needs name, language and at least one target', () => {
    const ready = { targetExamIds: ['ssc-cgl'], targetRoleIds: [] };
    expect(isProfileReady(baseUser, ready)).toBe(true);
    expect(isProfileReady({ ...baseUser, onboardingComplete: false }, ready)).toBe(false);
    expect(isProfileReady({ ...baseUser, name: ' ' }, ready)).toBe(false);
    expect(isProfileReady({ ...baseUser, dob: undefined }, ready)).toBe(false); // backend needs 18+ DOB too
    expect(isProfileReady({ ...baseUser, preferredLanguage: '' as never }, ready)).toBe(false);
    expect(isProfileReady(baseUser, { targetExamIds: [], targetRoleIds: [] })).toBe(false);
    expect(isProfileReady(baseUser, { targetExamIds: [], targetRoleIds: ['bank-po'] })).toBe(true);
  });

  it('sends a user who has not finished onboarding to /onboarding', () => {
    useAuthStore.getState().signIn(session({ onboardingComplete: false }));
    renderGuarded('/exams/ssc-cgl/instructions');
    expect(screen.getByTestId('where')).toHaveTextContent('/onboarding');
  });

  it('sends a user with no target to their profile, then back to the exam', () => {
    useAuthStore.getState().signIn(session());
    useProfileStore.setState({ profile: { ...EMPTY_PROFILE } });
    renderGuarded('/exams/ssc-cgl/instructions');
    expect(screen.getByTestId('where')).toHaveTextContent('/profile?complete=1&redirect=%2Fexams%2Fssc-cgl%2Finstructions');
  });

  it('opens the exam when the profile is ready', () => {
    useAuthStore.getState().signIn(session());
    useProfileStore.setState({ profile: { ...EMPTY_PROFILE, targetExamIds: ['ssc-cgl'] } });
    renderGuarded('/exams/ssc-cgl/instructions');
    expect(screen.getByText('Instructions page')).toBeInTheDocument();
  });
});

describe('Day 2 · 3-step onboarding', () => {
  it('collects name + language, education, targets and consent, then unlocks exams', async () => {
    const consent = vi.spyOn(profileService, 'recordConsent').mockResolvedValue();
    const updateMe = vi.spyOn(profileService, 'updateMe').mockImplementation(async (p) => p);
    useAuthStore.getState().signIn(session({ name: '', dob: undefined, onboardingComplete: false }));
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/onboarding']}>
        <Routes>
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/dashboard" element={<p>Dashboard page</p>} />
        </Routes>
      </MemoryRouter>,
    );

    // Step 1 · About you
    expect(screen.getByRole('heading', { name: 'Tell us about yourself' })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Continue' }));
    expect(await screen.findByText('Enter your full name')).toBeInTheDocument();
    expect(screen.getByText('Select your date of birth')).toBeInTheDocument();
    await user.type(screen.getByLabelText(/Full name/), 'Ananya Rao');
    await user.type(screen.getByLabelText(/Date of birth/), '2015-01-01');
    await user.click(screen.getByRole('button', { name: 'Continue' }));
    expect(await screen.findByText('You must be between 18 and 80 years old')).toBeInTheDocument();
    await user.clear(screen.getByLabelText(/Date of birth/));
    await user.type(screen.getByLabelText(/Date of birth/), '1999-05-10');
    await user.click(screen.getByRole('button', { name: 'Continue' }));

    // Step 2 · Education & experience
    expect(await screen.findByRole('heading', { name: 'Your education' })).toBeInTheDocument();
    await user.click(screen.getByRole('radio', { name: /Graduate/ }));
    await user.click(screen.getByRole('button', { name: /More experience/ })); // experience counter 0 → 1
    await user.selectOptions(screen.getByLabelText(/^Stream/), 'Commerce');
    await user.click(screen.getByRole('button', { name: 'Continue' }));

    // Step 3 · Targets + consent
    expect(await screen.findByRole('heading', { name: 'What are you preparing for?' })).toBeInTheDocument();
    const finish = screen.getByRole('button', { name: 'Finish and start practising' });
    await user.click(finish);
    expect(await screen.findByText('Pick at least one target exam or job role')).toBeInTheDocument();
    expect(screen.getByText('Please agree to the Terms of Use and Privacy Policy to continue')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Privacy Policy' })).toHaveAttribute('href', '/privacy');

    await user.click(screen.getByRole('button', { name: /SSC CGL/ }));
    await user.click(screen.getByRole('checkbox'));
    await user.click(finish);

    expect(await screen.findByText('Dashboard page')).toBeInTheDocument();
    expect(consent).toHaveBeenCalledWith('terms-and-privacy', true);
    expect(updateMe).toHaveBeenCalledWith(expect.objectContaining({ user: expect.objectContaining({ name: 'Ananya Rao', dob: '1999-05-10', preferredLanguage: 'en', onboardingComplete: true }) }));
    await waitFor(() => {
      const u = useAuthStore.getState().session?.user;
      expect(isProfileReady(u, useProfileStore.getState().profile)).toBe(true);
    });
    expect(useProfileStore.getState().profile.targetExamIds).toContain('ssc-cgl');
    expect(useProfileStore.getState().profile.educationLevel).toBe('graduate');
    expect(useProfileStore.getState().profile.experienceYears).toBe(1);
  });
});
