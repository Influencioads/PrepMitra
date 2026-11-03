/**
 * End-to-end check of the web services against a running FastAPI backend (no mocks).
 * Skipped in the normal test run. To run it:
 *
 *   1. cd backend && .venv/Scripts/python scripts/dev_server.py --port 8001   (development mode: returns dev OTPs)
 *   2. from frontend/:
 *      VITE_LIVE_API=1 VITE_USE_MOCK_API=false VITE_API_BASE_URL=http://localhost:8001 npx vitest run src/test/live-backend.test.ts
 */
import { describe, expect, it } from 'vitest';
import { getExamById, getQuestionById, liveCatalog } from '@prepmitra/shared';
import {
  adminService, attemptService, authService, examService, interviewService, notificationService, profileService, reportService,
  subscriptionService,
} from '@/services';
import { useAdminStore } from '@/store/adminStore';
import { signInWithDemoData, syncFromBackend, useAuthStore, useExamStore, useInterviewStore, useSubscriptionStore } from '@/store';
import { USE_MOCK } from '@/services/mock';

const live = !!import.meta.env.VITE_LIVE_API;
const phone = `98${String(Date.now()).slice(-8)}`; // a new learner every run

describe.skipIf(!live)('live backend journey', () => {
  it('runs signup → onboarding → free mini mock → report → payment → interview → admin', async () => {
    expect(USE_MOCK).toBe(false);

    // Phone OTP sign-up (development backends return the code).
    const sent = await authService.sendOtp({ phone, purpose: 'signup' });
    expect(sent.demoCode).toMatch(/^\d{6}$/);
    const session = await authService.verifyOtp({ requestId: sent.requestId, phone, otp: sent.demoCode!, signup: { name: 'Live Test' } });
    expect(session.isNewUser).toBe(true);
    signInWithDemoData(session);
    await profileService.recordConsent('terms-and-privacy', true);
    await syncFromBackend();

    // Onboarding, as OnboardingPage sends it.
    const me = await profileService.updateMe({
      user: { name: 'Live Test', dob: '2001-03-04', state: 'Kerala', preferredLanguage: 'en' },
      profile: { educationLevel: 'graduate', targetExamIds: ['ssc-cgl'], targetRoleIds: ['software-developer'], experienceYears: 0 },
    });
    expect(me.user?.onboardingComplete).toBe(true);
    expect(me.profile?.targetExamIds).toEqual(['ssc-cgl']);

    // Catalog with the design's ids.
    const exams = await examService.list({});
    expect(exams.map((e) => e.id)).toEqual(expect.arrayContaining(['general-aptitude', 'ssc-cgl']));
    const free = await examService.get('general-aptitude');
    expect(free.isFree).toBe(true);
    expect(free.sections.length).toBeGreaterThan(0);
    expect(examService.getSync('general-aptitude')?.title).toBe(free.title);

    // Free mini mock: start, answer, autosave, submit, report.
    const attempt = await attemptService.start(free, 'en');
    expect(attempt.paper.length).toBeGreaterThan(0);
    const first = getQuestionById(attempt.paper[0]!.questionId)!;
    expect(first.text.length).toBeGreaterThan(5);
    expect(first.correctOptionIds).toBeUndefined(); // answers are never sent before submit
    const answered = {
      ...attempt,
      states: Object.fromEntries(attempt.paper.slice(0, 5).map((p) => [p.questionId, { visited: true, marked: false, timeSpentSec: 20, answer: { selectedOptionIds: [getQuestionById(p.questionId)!.options![0]!.id] } }])),
    };
    useExamStore.getState().saveAttempt(answered);
    await attemptService.saveAnswers(answered);
    await attemptService.logEvent(attempt.id, { type: 'tab_switch', at: new Date().toISOString() });
    expect(await attemptService.submit(free, answered)).toBeNull();
    const report = await reportService.pollExamReport(attempt.id, { intervalMs: 500, timeoutMs: 60_000 });
    expect(report.examId).toBe('general-aptitude');
    expect(report.result.attempted).toBe(5);
    expect(report.improvementPlan).toHaveLength(7);
    await reportService.rate(report.id, 5);
    const review = await attemptService.fetchReview(answered);
    expect(review[0]!.question.correctOptionIds?.length).toBe(1);
    expect(getQuestionById(review[0]!.questionId)!.explanation).not.toBe('');

    // ₹399 pack through the backend's mock gateway, then credits re-synced from the server.
    const plans = await subscriptionService.getPlans();
    expect(plans.map((p) => p.id)).toEqual(['free', 'pay-per-mock', 'monthly']);
    expect(plans.find((p) => p.id === 'monthly')!.priceInr).toBe(399);
    const order = await subscriptionService.createDemoOrder('monthly', 'upi');
    expect(order.status).toBe('success');
    expect(order.amountInr).toBe(399);
    const credits = await subscriptionService.getCredits();
    expect(credits!.credits).toBe(10);

    // Text interview: start, two answers, end, report.
    const roles = await interviewService.listRoles();
    expect(roles.map((r) => r.id)).toContain('software-developer');
    let iv = await interviewService.start({ roleId: 'software-developer', level: 'fresher', language: 'en', mode: 'text' });
    expect(iv.turns[0]!.speaker).toBe('interviewer');
    iv = await interviewService.answer(iv, 'I am a computer science graduate. In my final-year project I built a REST API with tests.', 40);
    iv = await interviewService.answer(iv, 'I would split the work, write unit tests first and review the database schema with my team.', 35);
    expect(iv.turns.filter((t) => t.speaker === 'candidate')).toHaveLength(2);
    const { report: ireport } = await interviewService.end(iv);
    expect(ireport.scores.roleKnowledge).toBeGreaterThan(0);
    expect(ireport.questionFeedback.length).toBeGreaterThan(0);

    // Everything visible in the stores after a fresh sync (what the dashboard reads).
    await syncFromBackend();
    expect(useExamStore.getState().reports[report.id]?.result.attempted).toBe(5);
    expect(useInterviewStore.getState().reports[ireport.id]).toBeDefined();
    expect(useSubscriptionStore.getState().sub.credits).toBe(9); // 10 bought − 1 interview
    expect(useSubscriptionStore.getState().sub.freeMiniMockUsed).toBe(true);
    const notes = await notificationService.list();
    expect(notes!.some((n) => n.type === 'result')).toBe(true);

    // Flag a question, then the admin console (seeded founder admin) sees it.
    await attemptService.reportQuestion(attempt.paper[0]!.questionId, 'wrong-answer', 'Live test flag');
    await authService.logout();
    useAuthStore.getState().signOut();
    liveCatalog.clear();
    const adminSession = await authService.demoAdminSignIn();
    expect(adminSession.user.role).toBe('admin');
    useAuthStore.getState().signIn(adminSession);
    await adminService.load('users');
    expect(useAdminStore.getState().users.some((u) => u.phone === phone)).toBe(true);
    await adminService.load('payments');
    expect(useAdminStore.getState().orders.some((o) => o.amountInr === 399)).toBe(true);
    await adminService.load('review');
    const item = useAdminStore.getState().reviewQueue.find((r) => r.questionId === attempt.paper[0]!.questionId);
    expect(item?.flags.length).toBeGreaterThan(0);
    await adminService.resolveReview(item!.id, 'rejected', { note: 'Checked in live test' });
    expect(getExamById('ssc-cgl')).toBeDefined();
  }, 180_000);
});
