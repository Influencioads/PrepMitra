import { describe, expect, it, beforeEach } from 'vitest';
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes, useParams } from 'react-router-dom';
import { createDemoAttempt, getExamById, getQuestionById } from '@prepmitra/shared';
import { ExamSessionPage } from '@/pages/exam/ExamSessionPage';
import { useExamStore } from '@/store';
import { evaluateExpression } from '@/components/exam/Calculator';

function ResultProbe() {
  const { reportId } = useParams();
  return <p>Result page {reportId}</p>;
}

function renderSession(attemptId: string) {
  return render(
    <MemoryRouter initialEntries={[`/exam/${attemptId}`]}>
      <Routes>
        <Route path="/exam/:attemptId" element={<ExamSessionPage />} />
        <Route path="/exam-result/:reportId" element={<ResultProbe />} />
      </Routes>
    </MemoryRouter>,
  );
}

const exam = getExamById('general-aptitude')!;

describe('exam session flow', () => {
  beforeEach(() => {
    useExamStore.getState().reset('user-test', [], []);
  });

  it('answers, marks for review, submits and lands on the result', async () => {
    const user = userEvent.setup();
    const attempt = createDemoAttempt(exam, { id: 'att-test-1', language: 'en' });
    useExamStore.getState().saveAttempt(attempt);
    renderSession(attempt.id);

    const firstQ = getQuestionById(attempt.paper[0]!.questionId)!;
    const palette = screen.getByRole('complementary', { name: /question palette/i });
    expect(within(palette).getByRole('button', { name: 'Question 1, not answered' })).toHaveAttribute('aria-current', 'step');

    if (firstQ.type === 'numeric') {
      await user.type(screen.getByLabelText('Your answer'), '42');
    } else {
      const [first] = screen.getAllByRole(firstQ.type === 'multiple' ? 'checkbox' : 'radio');
      await user.click(first!);
    }
    expect(within(palette).getByRole('button', { name: 'Question 1, answered' })).toBeInTheDocument();

    // Mark for review & next moves to question 2 and keeps question 1 answered + marked.
    await user.click(screen.getAllByRole('button', { name: /mark for review/i })[0]!);
    expect(within(palette).getByRole('button', { name: 'Question 1, answered and marked for review' })).toBeInTheDocument();
    expect(useExamStore.getState().attempts[attempt.id]!.currentIndex).toBe(1);

    await user.click(within(palette).getByRole('button', { name: /submit test/i }));
    const dialog = await screen.findByRole('dialog');
    expect(within(dialog).getByText(/still unanswered/i)).toBeInTheDocument();
    await user.click(within(dialog).getByRole('button', { name: 'Submit test' }));

    await screen.findByText(/Result page/);
    const state = useExamStore.getState();
    expect(state.attempts[attempt.id]!.status).toBe('submitted');
    const reportId = state.attempts[attempt.id]!.reportId!;
    expect(state.reports[reportId]).toBeDefined();
    expect(state.reports[reportId]!.result.attempted).toBe(1);
  });

  it('restores an unfinished attempt at the saved question after a refresh', async () => {
    const attempt = createDemoAttempt(exam, { id: 'att-test-2', language: 'en' });
    useExamStore.getState().saveAttempt({ ...attempt, currentIndex: 3 });
    const first = renderSession(attempt.id);
    expect(screen.getByRole('heading', { name: /Question 4/ })).toBeInTheDocument();
    first.unmount();

    // Simulate a reload: the persisted store still holds the attempt.
    const persisted = JSON.parse(localStorage.getItem('pm.attempts')!);
    expect(persisted.state.attempts[attempt.id].currentIndex).toBe(3);
    renderSession(attempt.id);
    await waitFor(() => expect(screen.getByRole('heading', { name: /Question 4/ })).toBeInTheDocument());
  });

  it('auto-submits when the time is already over', async () => {
    const attempt = createDemoAttempt(exam, { id: 'att-test-3', language: 'en', now: Date.now() - exam.demo.durationMin * 60_000 - 1000 });
    useExamStore.getState().saveAttempt(attempt);
    renderSession(attempt.id);
    await screen.findByText(/Result page/);
    const a = useExamStore.getState().attempts[attempt.id]!;
    expect(a.status).toBe('submitted');
    expect(useExamStore.getState().reports[a.reportId!]!.autoSubmitted).toBe(true);
  });

  it('shows an error state for unknown attempts', () => {
    renderSession('missing');
    expect(screen.getByText('Attempt not found')).toBeInTheDocument();
  });
});

describe('calculator', () => {
  it('evaluates arithmetic safely', () => {
    expect(evaluateExpression('2+3×4')).toBe(14);
    expect(evaluateExpression('(2+3)×4')).toBe(20);
    expect(evaluateExpression('10÷4')).toBe(2.5);
    expect(evaluateExpression('−3+5')).toBe(2);
    expect(() => evaluateExpression('2+')).toThrow();
  });
});
