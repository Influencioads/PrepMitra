import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { act, render, screen, within } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { createDemoAttempt, getExamById } from '@prepmitra/shared';
import { ExamSessionPage } from '@/pages/exam/ExamSessionPage';
import { useExamStore } from '@/store';
import { useI18nStore } from '@/i18n';

function renderSession(attemptId: string) {
  return render(
    <MemoryRouter initialEntries={[`/exam/${attemptId}`]}>
      <Routes>
        <Route path="/exam/:attemptId" element={<ExamSessionPage />} />
      </Routes>
    </MemoryRouter>,
  );
}

const exam = getExamById('general-aptitude')!;

describe('CBT exam screen in Hindi', () => {
  beforeEach(() => {
    useExamStore.getState().reset('user-test', [], []);
    useI18nStore.getState().setLang('hi');
  });
  afterEach(() => useI18nStore.getState().setLang('en'));

  it('shows the palette legend, palette labels and action buttons in Hindi', async () => {
    const attempt = createDemoAttempt(exam, { id: 'att-hi-1', language: 'en' });
    useExamStore.getState().saveAttempt(attempt);
    renderSession(attempt.id);

    const palette = screen.getByRole('complementary', { name: 'प्रश्न पैलेट' });
    // Standard CBT legend wording.
    for (const label of ['उत्तर दिया', 'उत्तर नहीं दिया', 'देखा नहीं', 'समीक्षा के लिए चिह्नित', 'उत्तर दिया और चिह्नित']) {
      expect(within(palette).getAllByText(label).length).toBeGreaterThan(0);
    }
    expect(within(palette).getByRole('button', { name: 'प्रश्न 1, उत्तर नहीं दिया' })).toHaveAttribute('aria-current', 'step');
    expect(within(palette).getByRole('button', { name: /टेस्ट सबमिट करें/ })).toBeInTheDocument();

    expect(screen.getAllByRole('button', { name: /सेव करें और आगे/ }).length).toBeGreaterThan(0);
    expect(screen.getAllByRole('button', { name: /समीक्षा के लिए चिह्नित करें और आगे/ }).length).toBeGreaterThan(0);
    // English labels are gone from the action bar.
    expect(screen.queryByRole('button', { name: /save & next/i })).not.toBeInTheDocument();
  });

  it('switches back to English labels without reloading', async () => {
    const attempt = createDemoAttempt(exam, { id: 'att-hi-2', language: 'en' });
    useExamStore.getState().saveAttempt(attempt);
    renderSession(attempt.id);
    expect(screen.getAllByRole('button', { name: /सेव करें और आगे/ }).length).toBeGreaterThan(0);

    act(() => useI18nStore.getState().setLang('en'));
    expect(await screen.findByRole('complementary', { name: 'Question palette' })).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: /save & next/i }).length).toBeGreaterThan(0);
  });
});
