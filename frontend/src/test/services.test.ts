import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { API_ENDPOINTS, getExamById, getPlanSet, MINI_MOCK } from '@prepmitra/shared';
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

describe('pricing sets', () => {
  it('launch set has the 10-credit pack at ₹399', () => {
    const launch = getPlanSet('launch');
    expect(launch.map((p) => p.id)).toEqual(['free', 'pay-per-mock', 'monthly']);
    expect(launch.find((p) => p.id === 'monthly')).toMatchObject({ priceInr: 399, credits: 10 });
    expect(getPlanSet('full')).toHaveLength(4);
  });
});
