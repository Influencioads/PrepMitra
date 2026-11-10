import { act, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes, useParams } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { ExamReport } from '@prepmitra/shared';
import { createDemoAttempt, getExamById, toExamReport } from '@prepmitra/shared';
import { ReportPage } from '@/pages/exam/ReportPage';
import { ReportProcessingPage } from '@/pages/exam/ReportProcessingPage';
import { ExamSessionPage } from '@/pages/exam/ExamSessionPage';
import { ExamInstructionsPage } from '@/pages/exam/ExamInstructionsPage';
import { attemptService, reportService } from '@/services';
import { useExamStore, useSubscriptionStore } from '@/store';
// A real GET /v1/attempts/{id}/report response from the local backend: IBPS PO Prelims (100 questions,
// +1 / −0.25). 12 answered in English: 3 correct, 9 wrong → 3 − 9 × 0.25 = 0.75.
import backendReport from './fixtures/ibps-po-report.json';

const ctx = { examId: 'ibps-po', examTitle: 'IBPS PO Prelims', durationSec: 3600, isMini: false };
const mapped = (): ExamReport => toExamReport(backendReport, ctx);

function Probe({ label }: { label: string }) {
  const p = useParams();
  return <p>{label} {Object.values(p).join(',')}</p>;
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.useRealTimers();
});
beforeEach(() => useExamStore.getState().reset('user-d6', [], []));

describe('Day 6 — report part 1 numbers (real backend report)', () => {
  it('maps the server analytics without changing any number', () => {
    const r = mapped();
    expect(r.isDemo).toBe(false);
    expect(r.result).toMatchObject({ score: 0.75, maxScore: 100, correct: 3, incorrect: 9, unanswered: 88, attempted: 12, accuracy: 25, negativeMarksLost: 2.25, marksLostTotal: 99.25 });
    expect(r.result.questions).toHaveLength(100);
    const english = r.result.sections.find((s) => s.sectionId === 'english')!;
    expect(english).toMatchObject({ score: 0.75, maxScore: 30, attempted: 12, correct: 3, incorrect: 9, unanswered: 18, accuracy: 25, timeSpentSec: 570 });
    // Marks per question come from the server's section totals; expected time from its question bank.
    expect(r.result.questions[0]).toMatchObject({ outcome: 'incorrect', marksAwarded: -0.25, maxMarks: 1, timeSpentSec: 20, expectedTimeSec: 45 });
    const wrongLost = r.result.questions.filter((q) => q.outcome === 'incorrect').reduce((s, q) => s + q.maxMarks, 0);
    const skippedLost = r.result.questions.filter((q) => q.outcome === 'unanswered').reduce((s, q) => s + q.maxMarks, 0);
    expect(wrongLost + r.result.negativeMarksLost + skippedLost).toBeCloseTo(r.result.marksLostTotal);
  });

  it('shows the score card, section table, accuracy, attempt rate and negative marks', async () => {
    const r = mapped();
    useExamStore.setState((s) => ({ reports: { ...s.reports, [r.id]: r } }));
    render(
      <MemoryRouter initialEntries={[`/reports/${r.id}`]}>
        <Routes><Route path="/reports/:reportId" element={<ReportPage />} /></Routes>
      </MemoryRouter>,
    );
    const table = await screen.findByTestId('section-table');
    const cells = (name: RegExp) => within(within(table).getByRole('rowheader', { name }).closest('tr')!).getAllByRole('cell').map((c) => c.textContent);
    expect(cells(/English Language/)).toEqual(['12', '3', '9', '18', '0.75/30', '25%', '9m 30s']);
    expect(cells(/Quantitative Aptitude/).slice(0, 6)).toEqual(['0', '0', '0', '35', '0/35', 'Not attempted']);
    expect(cells(/^Total$/).slice(0, 5)).toEqual(['12', '3', '9', '88', '0.75/100']);

    expect(screen.getByText('12% (12/100)')).toBeInTheDocument(); // attempt rate
    expect(screen.getAllByText('−2.25').length).toBeGreaterThan(0); // marks lost to negative marking
    expect(screen.getAllByText('25%').length).toBeGreaterThan(0); // accuracy
    // Real reports are not labelled "demo"; the notice says the server did the scoring.
    expect(screen.queryByText('Demo analysis')).not.toBeInTheDocument();
    expect(screen.getByText(/Scores are calculated by the server/)).toBeInTheDocument();
    // Time-per-question chart can be narrowed to one section.
    await userEvent.click(screen.getByRole('button', { name: 'Reasoning Ability' }));
    expect(screen.getByRole('button', { name: 'Reasoning Ability' })).toHaveAttribute('aria-pressed', 'true');
  });
});

describe('Day 6 — report processing screen', () => {
  const renderProcessing = (attemptId: string) =>
    render(
      <MemoryRouter initialEntries={[`/exam/${attemptId}/processing`]}>
        <Routes>
          <Route path="/exam/:attemptId/processing" element={<ReportProcessingPage />} />
          <Route path="/exam-result/:reportId" element={<Probe label="Result page" />} />
        </Routes>
      </MemoryRouter>,
    );

  it('checks /report every 3 seconds, rides out a network drop and opens the report when ready', async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    const attempt = { ...createDemoAttempt(getExamById('ibps-po')!, { id: 'att-proc', language: 'en' }), status: 'submitted' as const };
    useExamStore.getState().saveAttempt(attempt);
    const report = { ...mapped(), attemptId: 'att-proc' };
    const calls: number[] = [];
    const responses = [
      () => Promise.resolve({ status: 'processing' as const }),
      () => Promise.reject({ status: 0, code: 'ERR_NETWORK', message: 'offline' }),
      () => Promise.resolve({ status: 'processing' as const }),
      () => Promise.resolve({ status: 'ready' as const, report }),
    ];
    vi.spyOn(reportService, 'getReportStatus').mockImplementation(() => {
      calls.push(Date.now());
      return responses[calls.length - 1]!();
    });
    renderProcessing('att-proc');
    expect(await screen.findByText('Preparing your report')).toBeInTheDocument();
    await act(() => vi.advanceTimersByTimeAsync(3000));
    expect(await screen.findByText(/Connection lost/)).toBeInTheDocument();
    await act(() => vi.advanceTimersByTimeAsync(6000));
    expect(await screen.findByText(`Result page ${report.id}`)).toBeInTheDocument();
    expect(calls).toHaveLength(4);
    calls.slice(1).forEach((t, i) => expect(t - calls[i]!).toBeGreaterThanOrEqual(3000));
    const saved = useExamStore.getState();
    expect(saved.attempts['att-proc']!.reportId).toBe(report.id);
    expect(saved.reports[report.id]!.result.score).toBe(0.75);
  });

  it('shows a clear error with retry when the report job failed', async () => {
    vi.spyOn(reportService, 'getReportStatus')
      .mockResolvedValueOnce({ status: 'failed', message: 'Report generation failed.', reportId: 'rep-9', creditRestored: true })
      .mockResolvedValue({ status: 'processing' });
    const retry = vi.spyOn(reportService, 'retryReport').mockResolvedValue();
    renderProcessing('att-failed');
    expect(await screen.findByRole('heading', { name: 'We could not prepare your report' })).toBeInTheDocument();
    expect(screen.getByText('Your credit has been restored.')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /My tests/i })).toHaveAttribute('href', '/my-tests');
    await userEvent.click(screen.getByRole('button', { name: 'Try again' }));
    expect(retry).toHaveBeenCalledWith('rep-9');
    expect(await screen.findByText('Preparing your report')).toBeInTheDocument();
  });
});

describe('Day 6 — exam errors from the real API', () => {
  const renderSession = (id: string) =>
    render(
      <MemoryRouter initialEntries={[`/exam/${id}`]}>
        <Routes>
          <Route path="/exam/:attemptId" element={<ExamSessionPage />} />
          <Route path="/exam/:attemptId/processing" element={<Probe label="Processing" />} />
          <Route path="/exam-result/:reportId" element={<Probe label="Result page" />} />
        </Routes>
      </MemoryRouter>,
    );

  it('expired attempt: when the server says time is up, the exam closes and waits for the report', async () => {
    const attempt = createDemoAttempt(getExamById('ibps-po')!, { id: 'att-expired', language: 'en' });
    useExamStore.getState().saveAttempt(attempt);
    vi.spyOn(attemptService, 'saveAnswers').mockRejectedValue({ status: 409, code: 'deadline_passed', message: 'Time is up.' });
    renderSession(attempt.id);
    expect(await screen.findByText('Processing att-expired')).toBeInTheDocument();
    const a = useExamStore.getState().attempts['att-expired']!;
    expect(a.status).toBe('submitted');
    expect(a.autoSubmitted).toBe(true);
  });

  it('network down on submit: answers stay on the device and the submit goes through when back online', async () => {
    const user = userEvent.setup();
    const attempt = createDemoAttempt(getExamById('ibps-po')!, { id: 'att-offline', language: 'en' });
    useExamStore.getState().saveAttempt(attempt);
    const submit = vi.spyOn(attemptService, 'submit')
      .mockRejectedValueOnce({ status: 0, code: 'ERR_NETWORK', message: 'Unable to reach the server.' })
      .mockResolvedValueOnce(null); // real API: scoring done, report job queued
    renderSession(attempt.id);
    const palette = screen.getByRole('complementary', { name: /question palette/i });
    await user.click(within(palette).getByRole('button', { name: /submit test/i }));
    await user.click(within(await screen.findByRole('dialog')).getByRole('button', { name: 'Submit test' }));
    await waitFor(() => expect(submit).toHaveBeenCalledTimes(1));
    expect(useExamStore.getState().attempts['att-offline']!.status).toBe('in-progress');
    await act(async () => void window.dispatchEvent(new Event('online')));
    expect(await screen.findByText('Processing att-offline')).toBeInTheDocument();
    expect(submit).toHaveBeenCalledTimes(2);
    expect(useExamStore.getState().attempts['att-offline']!.status).toBe('submitted');
  });

  it('no credits: a 402 from the server opens the "need more credits" dialog', async () => {
    const user = userEvent.setup();
    useSubscriptionStore.setState((s) => ({ sub: { ...s.sub, credits: 5 } }));
    vi.spyOn(attemptService, 'start').mockRejectedValue({ status: 402, code: 'insufficient_credits', message: 'You have no exam credits left.' });
    render(
      <MemoryRouter initialEntries={['/exams/ibps-po/instructions']}>
        <Routes><Route path="/exams/:id/instructions" element={<ExamInstructionsPage />} /></Routes>
      </MemoryRouter>,
    );
    await user.click(await screen.findByRole('checkbox'));
    await user.click(screen.getByRole('button', { name: /Start test/ }));
    expect(await screen.findByRole('dialog', { name: 'You need more credits' })).toBeInTheDocument();
    expect(useSubscriptionStore.getState().sub.credits).toBe(5); // the local charge was refunded
  });
});
