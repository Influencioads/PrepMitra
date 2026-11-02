import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { API_ENDPOINTS, buildExamReport, createDemoAttempt, getExamById, getPlanSet, MINI_MOCK, type ReportStatusResponse } from '@prepmitra/shared';
import { http } from '@/services/http';
import { reportService } from '@/services/reportService';
import { attemptService } from '@/services/attemptService';
import { clearTrackedEvents, getTrackedEvents, setAnalyticsProvider, track } from '@/lib/analytics';

const exam = getExamById('ssc-cgl')!;
const attempt = createDemoAttempt(exam, { id: 'att-poll', language: 'en', now: 0 });
const report = buildExamReport(exam, { ...attempt, status: 'submitted', submittedAt: new Date(60_000).toISOString() }, { id: 'rep-poll' });

function mockStatuses(...seq: ReportStatusResponse[]) {
  const spy = vi.spyOn(http, 'get');
  seq.forEach((s) => spy.mockResolvedValueOnce({ data: s } as never));
  return spy;
}

describe('reportService.pollExamReport', () => {
  afterEach(() => vi.restoreAllMocks());

  it('polls until the report is ready and reports progress', async () => {
    const get = mockStatuses({ status: 'processing', progress: 20 }, { status: 'processing', progress: 70 }, { status: 'ready', report });
    const progress: (number | undefined)[] = [];
    const out = await reportService.pollExamReport('att-poll', { intervalMs: 1, onProgress: (p) => progress.push(p) });
    expect(out.id).toBe('rep-poll');
    expect(get).toHaveBeenCalledTimes(3);
    expect(get).toHaveBeenCalledWith(API_ENDPOINTS.attemptReport('att-poll'));
    expect(progress).toEqual([20, 70]);
  });

  it('rejects with the server message when generation fails', async () => {
    mockStatuses({ status: 'processing' }, { status: 'failed', message: 'Scoring failed' });
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
