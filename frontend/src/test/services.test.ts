import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  API_ENDPOINTS, conflictingPlan, getExamById, getPlanSet, MINI_MOCK, mockAllowances, planCodeFromId, subscriptionSlots, toAllowances, toPlans,
} from '@prepmitra/shared';
import { http } from '@/services/http';
import { reportService } from '@/services/reportService';
import { attemptService } from '@/services/attemptService';
import { clearTrackedEvents, getTrackedEvents, setAnalyticsProvider, track } from '@/lib/analytics';

const exam = getExamById('ssc-cgl')!;



/** Backend report body (GET /v1/attempts/{id}/report), as the FastAPI backend returns it. */
const backendReport = {
  id: 'rep-poll', kind: 'exam', status: 'ready', language: 'en', attempt_id: 'att-poll', created_at: new Date(60_000).toISOString(),
  analytics: {
    score: 6, max_score: 10, accuracy: 0.75, attempted: 4, correct: 3, wrong: 1, unanswered: 1, negative_marks_lost: 0.5, total_time_sec: 300,
    sections: [{ key: 'quant', name: 'Quantitative Aptitude', score: 6, max_score: 10, attempted: 4, correct: 3, wrong: 1, unanswered: 1, accuracy: 0.75, time_sec: 300 }],
    topics: [{ name: 'Percentages', section_key: 'quant', total: 5, attempted: 4, correct: 3, accuracy: 0.75 }],
    error_patterns: [], questions: [{ ref: 1, question_id: 'q1', section_key: 'quant', status: 'wrong', marks: -0.5, time_sec: 60 }], percentile: 72,
  },
  report: { strengths: [{ topic: 'Percentages', detail: 'Fast and accurate.' }], weaknesses: [], loopholes: [], study_plan: [{ day: 1, focus: 'Ratios', tasks: ['Revise'] }], next_test: { exam_slug: 'ssc-cgl-tier1' } },
  user_rating: null,
};

function mockStatuses(...seq: object[]) {
  const spy = vi.spyOn(http, 'get');
  seq.forEach((s) => spy.mockResolvedValueOnce({ data: s } as never));
  return spy;
}

describe('reportService.pollExamReport', () => {
  afterEach(() => vi.restoreAllMocks());

  it('polls until the report is ready and reports progress', async () => {
    const get = mockStatuses({ status: 'processing', progress: 20 }, { status: 'processing', progress: 70 }, backendReport);
    const progress: (number | undefined)[] = [];
    const out = await reportService.pollExamReport('att-poll', { intervalMs: 1, onProgress: (p) => progress.push(p) });
    expect(out.id).toBe('rep-poll');
    expect(out.result.accuracy).toBe(75);
    expect(out.percentile).toBe(72);
    expect(out.result.questions[0]!.outcome).toBe('incorrect');
    expect(out.recommendedNextExamId).toBe('ssc-cgl');
    expect(out.improvementPlan[0]!.title).toBe('Ratios');
    expect(get).toHaveBeenCalledTimes(3);
    expect(get).toHaveBeenCalledWith(API_ENDPOINTS.attemptReport('att-poll'));
    expect(progress).toEqual([20, 70]);
  });

  it('rejects with the server message when generation fails', async () => {
    mockStatuses({ status: 'processing' }, { status: 'failed', error: 'Scoring failed' });
    await expect(reportService.pollExamReport('att-poll', { intervalMs: 1 })).rejects.toThrow('Scoring failed');
  });

  it('gives up after the timeout', async () => {
    vi.spyOn(http, 'get').mockResolvedValue({ data: { status: 'processing' } } as never);
    await expect(reportService.pollExamReport('att-poll', { intervalMs: 5, timeoutMs: 12 })).rejects.toThrow(/longer than usual/);
  });

  it('stops when aborted', async () => {
    const ctrl = new AbortController();
    ctrl.abort();
    const get = vi.spyOn(http, 'get');
    await expect(reportService.pollExamReport('att-poll', { signal: ctrl.signal })).rejects.toThrow(/cancelled/);
    expect(get).not.toHaveBeenCalled();
  });
});

describe('mini mock paper', () => {
  it('attemptService.start caps the demo paper at 10 questions / 30 min', async () => {
    const mini = await attemptService.start(exam, 'en', { mini: true });
    const full = await attemptService.start(exam, 'en');
    expect(mini.paper).toHaveLength(MINI_MOCK.maxQuestions);
    expect(mini.durationSec).toBe(MINI_MOCK.durationMin * 60);
    expect(mini.isMini).toBe(true);
    expect(full.paper.length).toBeGreaterThan(MINI_MOCK.maxQuestions);
    expect(full.isMini).toBeFalsy();
  });
});

describe('analytics track()', () => {
  beforeEach(() => clearTrackedEvents());
  afterEach(() => setAnalyticsProvider(null));

  it('queues events in order with props and forwards them to the provider', () => {
    const provider = vi.fn();
    setAnalyticsProvider(provider);
    track('exam_started', { examId: 'ssc-cgl', mode: 'mini' });
    track('exam_submitted', { examId: 'ssc-cgl' });
    const events = getTrackedEvents();
    expect(events.map((e) => e.event)).toEqual(['exam_started', 'exam_submitted']);
    expect(events[0]!.props).toMatchObject({ examId: 'ssc-cgl', mode: 'mini' });
    expect(provider).toHaveBeenCalledTimes(2);
    expect(provider).toHaveBeenCalledWith('exam_started', expect.objectContaining({ mode: 'mini' }));
  });

  it('keeps at most 200 events', () => {
    for (let i = 0; i < 250; i++) track('report_viewed', { i });
    const events = getTrackedEvents();
    expect(events).toHaveLength(200);
    expect(events.at(-1)!.props).toMatchObject({ i: 249 });
  });
});

describe('pricing blueprint', () => {
  it('mock catalog matches the backend plan codes and prices', () => {
    const plans = getPlanSet('full');
    const prices = Object.fromEntries(plans.map((p) => [p.code, p.priceInr]));
    expect(prices).toEqual({
      free_trial: 0,
      starter_monthly: 149, starter_quarterly: 399, starter_annual: 1199,
      pro_monthly: 299, pro_quarterly: 799, pro_annual: 2499,
      tutor_lite_monthly: 99, tutor_lite_annual: 999, tutor_pro_monthly: 299, tutor_pro_annual: 2999,
      combo_monthly: 499, combo_annual: 4999,
      single_mock: 29, extra_mocks_5: 49, extra_doubts_50: 39, extra_master_10: 99, interview_pack: 199, ultra_pack: 349,
    });
    expect(plans.find((p) => p.id === 'pro_quarterly')).toMatchObject({ group: 'study', period: 'quarterly', credits: 75, validityDays: 90 });
    expect(plans.find((p) => p.id === 'combo_monthly')!.entitlements.limits).toMatchObject({ doubts: 150, smart_credits: 40, master_credits: 10 });
  });

  it('maps every /v1/plans code, including ones the client does not know', () => {
    const plans = toPlans({ items: [
      { code: 'free_trial', name: 'Free', price_inr: 0, credits: 1, validity_days: 30, is_recurring: false, group: 'free', period: 'lifetime', entitlements: {} },
      { code: 'pro_annual', name: 'Pro (Selection Pass) · annual', price_inr: 2499, credits: 300, validity_days: 365, is_recurring: true, group: 'study', period: 'annual', entitlements: { limits: { doubts: 150 } } },
      { code: 'mystery_pack', name: 'Mystery pack', price_inr: 59, credits: 0, validity_days: 30, is_recurring: false, group: 'addon', period: 'one_time', entitlements: { limits: { doubts: 20 } } },
    ] });
    expect(plans.map((p) => p.id)).toEqual(['free', 'pro_annual', 'mystery_pack']);
    expect(plans[1]).toMatchObject({ group: 'study', period: 'annual', family: 'pro', badge: 'Most popular' });
    expect(plans[2]!.features).toEqual(['20 × AI doubts']);
    expect(planCodeFromId('free')).toBe('free_trial');
    expect(planCodeFromId('pro_annual')).toBe('pro_annual');
  });

  it('allows one study plan and one tutor pack; the combo is both', () => {
    const plans = getPlanSet('full');
    const plan = (id: string) => plans.find((p) => p.id === id)!;
    expect(conflictingPlan(plan('tutor_lite_monthly'), ['starter_monthly'], plans)).toBeUndefined();
    expect(conflictingPlan(plan('pro_monthly'), ['starter_annual'], plans)?.id).toBe('starter_annual');
    expect(conflictingPlan(plan('combo_monthly'), ['tutor_pro_monthly'], plans)?.id).toBe('tutor_pro_monthly');
    expect(conflictingPlan(plan('extra_mocks_5'), ['combo_monthly'], plans)).toBeUndefined();
    expect(subscriptionSlots(['starter_monthly', 'tutor_lite_annual', 'extra_doubts_50'])).toEqual({ planId: 'starter_monthly', tutorPlanId: 'tutor_lite_annual' });
  });

  it('reads /v1/me/allowances', () => {
    const a = toAllowances({
      plans: ['free_trial', 'starter_monthly'], flags: { persona: 'full' }, resets_at: '2026-12-01T00:00:00Z',
      limits: { doubts: { label: 'AI doubts', limit: 55, used: 5, remaining: 50, sources: [] } },
    });
    expect(a).toEqual({
      plans: ['starter_monthly'], flags: { persona: 'full' }, resetsAt: '2026-12-01T00:00:00Z',
      limits: [{ feature: 'doubts', label: 'AI doubts', limit: 55, used: 5, remaining: 50 }],
    });
    const mock = mockAllowances(['starter_monthly', 'extra_doubts_50']);
    expect(mock.limits.find((l) => l.feature === 'doubts')).toMatchObject({ limit: 105, remaining: 105 });
  });
});
