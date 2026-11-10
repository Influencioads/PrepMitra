import { act, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { Attempt } from '@prepmitra/shared';
import { answerFromBackend, answerToBackend, createDemoAttempt, getExamById } from '@prepmitra/shared';
import { CountdownTimer } from '@/components/exam/CountdownTimer';
import { ExamSessionPage } from '@/pages/exam/ExamSessionPage';
import { mergeLocalAttempt } from '@/store/sync';
import { useExamStore } from '@/store';

afterEach(() => vi.useRealTimers());

describe('Day 5 — saved answers from the API', () => {
  it('unwraps {"value": …} answers (the server format) for every question type', () => {
    expect(answerFromBackend({ value: 'B' }, 'single')).toEqual({ selectedOptionIds: ['B'] });
    expect(answerFromBackend({ value: ['A', 'C'] }, 'multiple')).toEqual({ selectedOptionIds: ['A', 'C'] });
    expect(answerFromBackend({ value: 12.5 }, 'numeric')).toEqual({ numericValue: '12.5' });
    expect(answerFromBackend(null, 'single')).toBeUndefined();
    expect(answerFromBackend('D', 'single')).toEqual({ selectedOptionIds: ['D'] });
  });

  it('never sends a broken option value back to the server', () => {
    expect(answerToBackend({ selectedOptionIds: ['[object Object]'] }, 'single')).toBeNull();
    expect(answerToBackend({ selectedOptionIds: ['B'] }, 'single')).toBe('B');
  });
});

describe('Day 5 — recovery after reload', () => {
  const exam = getExamById('ssc-cgl')!;
  const base = createDemoAttempt(exam, { id: 'att-merge', language: 'en' });
  const [q1, q2] = base.paper.map((p) => p.questionId) as [string, string];

  it('keeps answers that only exist on this device and takes the end time from the server', () => {
    const server: Attempt = { ...base, endsAt: '2030-01-01T10:00:00.000Z', states: { ...base.states, [q1]: { visited: true, marked: false, timeSpentSec: 30, answer: { selectedOptionIds: ['A'] } } } };
    const local: Attempt = {
      ...base,
      endsAt: '2030-01-01T10:05:00.000Z',
      currentIndex: 4,
      states: {
        ...base.states,
        [q1]: { visited: true, marked: true, timeSpentSec: 12, answer: { selectedOptionIds: ['B'] } },
        [q2]: { visited: true, marked: false, timeSpentSec: 5, answer: { selectedOptionIds: ['C'] } }, // answered offline
      },
    };
    const merged = mergeLocalAttempt(server, local);
    expect(merged.endsAt).toBe(server.endsAt);
    expect(merged.currentIndex).toBe(4);
    expect(merged.states[q1]).toMatchObject({ marked: true, answer: { selectedOptionIds: ['B'] }, timeSpentSec: 30 });
    expect(merged.states[q2]?.answer).toEqual({ selectedOptionIds: ['C'] });
  });

  it('uses the server copy when this device has none', () => {
    expect(mergeLocalAttempt(base, undefined)).toBe(base);
  });
});

describe('Day 5 — timer', () => {
  it('warns once at 5 minutes and auto-submits at zero', () => {
    vi.useFakeTimers({ toFake: ['setInterval', 'clearInterval', 'Date'] });
    const now = new Date('2030-01-01T10:00:00Z').getTime();
    vi.setSystemTime(now);
    const onWarning = vi.fn();
    const onExpire = vi.fn();
    render(<CountdownTimer endsAt={new Date(now + 302_000).toISOString()} onWarning={onWarning} onExpire={onExpire} />);
    expect(screen.getByRole('timer')).toHaveTextContent('05:02');
    act(() => vi.advanceTimersByTime(1000));
    expect(onWarning).not.toHaveBeenCalled();
    act(() => vi.advanceTimersByTime(2000));
    expect(onWarning).toHaveBeenCalledTimes(1);
    act(() => vi.advanceTimersByTime(60_000));
    expect(onWarning).toHaveBeenCalledTimes(1);
    act(() => vi.advanceTimersByTime(300_000));
    expect(onExpire).toHaveBeenCalledTimes(1);
  });
});

describe('Day 5 — submit screen', () => {
  it('shows totals and a section-by-section summary before submitting', async () => {
    const user = userEvent.setup();
    useExamStore.getState().reset('user-test', [], []);
    const exam = getExamById('ssc-cgl')!;
    const attempt = createDemoAttempt(exam, { id: 'att-summary', language: 'en' });
    useExamStore.getState().saveAttempt(attempt);
    render(
      <MemoryRouter initialEntries={[`/exam/${attempt.id}`]}>
        <Routes><Route path="/exam/:attemptId" element={<ExamSessionPage />} /></Routes>
      </MemoryRouter>,
    );
    await user.click(screen.getAllByRole('radio')[0]!);
    await user.click(screen.getAllByRole('button', { name: 'Save & Next' })[0]!);
    await user.click(screen.getAllByRole('button', { name: /submit test/i })[0]!);
    const dialog = await screen.findByRole('dialog');
    const table = within(dialog).getByRole('table', { name: 'Answers by section' });
    const sections = new Set(attempt.paper.map((p) => p.sectionId)).size;
    expect(within(table).getAllByRole('row')).toHaveLength(sections + 1);
    expect(within(dialog).getAllByText('Answered').length).toBeGreaterThan(0);
    expect(within(dialog).getAllByText('Not answered').length).toBeGreaterThan(0);
    expect(within(dialog).getAllByText('Marked for review').length).toBeGreaterThan(0);
  });
});
