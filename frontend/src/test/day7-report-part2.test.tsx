import { act, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { ExamReport, Question } from '@prepmitra/shared';
import { liveCatalog, toExamReport, toSharedReport } from '@prepmitra/shared';
import { ReportPage } from '@/pages/exam/ReportPage';
import { SharedReportPage } from '@/pages/public/SharedReportPage';
import { attemptService, reportService } from '@/services';
import { useExamStore } from '@/store';
import { useI18nStore } from '@/i18n';
// Real GET /v1/attempts/{id}/report from the local backend (IBPS PO, 12 answered: 3 right, 9 wrong).
import backendReport from './fixtures/ibps-po-report.json';

const report = (): ExamReport => toExamReport(backendReport, { examId: 'ibps-po', examTitle: 'IBPS PO Prelims', durationSec: 3600 });
// The review API's questions, so the report can show them (text, answer key, explanation).
const questions: Question[] = backendReport.analytics.questions.map((q) => ({
  id: q.question_id, subject: 'english', topic: q.topic, type: 'single', difficulty: 'Moderate', text: `Question ${q.ref} text`,
  options: ['A', 'B', 'C', 'D'].map((k) => ({ id: k, text: `Option ${k}` })), correctOptionIds: ['B'], explanation: `Explanation for ${q.ref}`,
  shortcut: q.ref === 1 ? 'Read the last line first.' : undefined, expectedTimeSec: q.expected_time_sec,
}));

function renderReport(r: ExamReport, tab = 'analysis') {
  useExamStore.setState((s) => ({ reports: { ...s.reports, [r.id]: r } }));
  return render(
    <MemoryRouter initialEntries={[`/reports/${r.id}?tab=${tab}`]}>
      <Routes><Route path="/reports/:reportId" element={<ReportPage />} /></Routes>
    </MemoryRouter>,
  );
}

beforeEach(() => {
  useExamStore.getState().reset('user-d7', [], []);
  liveCatalog.registerQuestions(questions);
});
afterEach(() => {
  vi.restoreAllMocks();
  act(() => useI18nStore.getState().setLang('en'));
});

describe('Day 7 — report part 2 from the real backend report', () => {
  it('maps shortcuts, loophole evidence, summary and the next-test reason', () => {
    const r = report();
    expect(r.summary).toBe('You scored 0.75 out of 100.0 with 25% accuracy.');
    expect(r.encouragement).toMatch(/Steady practice/);
    expect(r.nextTestReason).toMatch(/Retake the same pattern/);
    expect(r.shortcuts).toHaveLength(5);
    expect(r.shortcuts![0]).toMatchObject({ technique: 'Option elimination', questionId: 'b0931ab9-fb5a-4397-992a-13122106356f' });
    const skipped = r.loopholes.filter((l) => l.pattern === 'skipped_section');
    expect(skipped.map((l) => l.section)).toEqual(['Quantitative Aptitude', 'Reasoning Ability']);
    expect(r.loopholes.find((l) => l.pattern === 'careless_easy')).toMatchObject({ marksImpact: 1.25, evidenceQuestionIds: ['169ac75c-28d2-4183-944d-3f8fff4b6876'] });
    expect(r.weaknesses[0]!.evidenceQuestionIds).toHaveLength(5);
  });

  it('shows strengths, weaknesses, loopholes, shortcuts; a question number opens that question', async () => {
    const user = userEvent.setup();
    renderReport(report());
    expect(screen.getByText('You scored 0.75 out of 100.0 with 25% accuracy.')).toBeInTheDocument();
    expect(screen.getByText(/No strong topic yet/)).toBeInTheDocument(); // the server sent no strengths
    expect(screen.getAllByText('Fill in the blanks').length).toBeGreaterThan(0);
    expect(screen.getByText('Skipped the whole Quantitative Aptitude section')).toBeInTheDocument();
    const shortcuts = screen.getByTestId('shortcuts');
    expect(within(shortcuts).getByText('Option elimination')).toBeInTheDocument();
    expect(within(shortcuts).getAllByRole('button', { name: /^Open question/ }).map((b) => b.textContent)).toEqual(['Q15', 'Q16', 'Q17', 'Q18', 'Q19']);

    await user.click(within(shortcuts).getByRole('button', { name: 'Open question 16' }));
    expect(screen.getByRole('tab', { name: /Question review/ })).toHaveAttribute('aria-selected', 'true');
    const card = document.getElementById('q-d2472d56-50cc-420a-865c-8801d551caf2')!;
    expect(within(card).getByText('Q16')).toBeInTheDocument();
    expect(card.querySelector('.ring-2')).not.toBeNull();
  });

  it('plan tab: 7 days and the recommended next test with its reason', async () => {
    renderReport(report(), 'plan');
    expect(screen.getAllByText(/^Day \d$/)).toHaveLength(7);
    expect(screen.getByText(/Why this test:/)).toHaveTextContent('Retake the same pattern to confirm improvement.');
  });

  it('every report section is labelled in Hindi', async () => {
    act(() => useI18nStore.getState().setLang('hi'));
    const user = userEvent.setup();
    renderReport(report());
    for (const h of ['मज़बूत पक्ष', 'कमज़ोरियाँ', 'गलतियों के पैटर्न', 'शॉर्टकट', 'अंक कहाँ कटे']) expect(screen.getAllByText(h).length).toBeGreaterThan(0);
    expect(screen.getByText('पूरा मात्रात्मक योग्यता सेक्शन छोड़ दिया')).toBeInTheDocument();
    await user.click(screen.getByRole('tab', { name: '7-दिन का प्लान' }));
    expect(screen.getAllByText(/^दिन \d$/)).toHaveLength(7);
    await user.click(screen.getByRole('tab', { name: /प्रश्न समीक्षा/ }));
    expect(screen.getAllByRole('button', { name: 'इस प्रश्न की शिकायत करें' }).length).toBeGreaterThan(0);
    expect(screen.getAllByText('हल करने का शॉर्टकट').length).toBe(1);
  });
});

describe('Day 7 — question-by-question review', () => {
  it('filters wrong and skipped, and sends "Report this question" with a reason', async () => {
    const user = userEvent.setup();
    const flag = vi.spyOn(attemptService, 'reportQuestion').mockResolvedValue();
    renderReport(report(), 'review');
    expect(document.querySelectorAll('li[id^="q-"]')).toHaveLength(100);
    await user.click(screen.getByRole('button', { name: /^Incorrect \(9\)/ }));
    expect(document.querySelectorAll('li[id^="q-"]')).toHaveLength(9);
    await user.click(screen.getByRole('button', { name: /^Unanswered \(88\)/ }));
    expect(document.querySelectorAll('li[id^="q-"]')).toHaveLength(88);
    await user.click(screen.getByRole('button', { name: /^All \(100\)/ }));

    const first = document.getElementById('q-169ac75c-28d2-4183-944d-3f8fff4b6876')!;
    expect(within(first).getByText('Explanation for 1')).toBeInTheDocument();
    expect(within(first).getByText('Read the last line first.')).toBeInTheDocument();
    await user.click(within(first).getByRole('button', { name: 'Report this question' }));
    const dialog = await screen.findByRole('dialog');
    await user.selectOptions(within(dialog).getByRole('combobox'), 'translation');
    await user.type(within(dialog).getByRole('textbox'), 'Hindi option C is wrong');
    await user.click(within(dialog).getByRole('button', { name: /Send report/i }));
    expect(flag).toHaveBeenCalledWith('169ac75c-28d2-4183-944d-3f8fff4b6876', 'translation', 'Hindi option C is wrong');
    expect(await within(first).findByRole('button', { name: 'Reported' })).toBeDisabled();
  });

  it('a question already reported by this student is shown as reported', async () => {
    const user = userEvent.setup();
    vi.spyOn(attemptService, 'reportQuestion').mockRejectedValue({ status: 409, code: 'already_reported', message: 'You have already reported this question' });
    renderReport(report(), 'review');
    const q2 = document.querySelectorAll('li[id^="q-"]')[1] as HTMLElement;
    await user.click(within(q2).getByRole('button', { name: 'Report this question' }));
    await user.click(within(await screen.findByRole('dialog')).getByRole('button', { name: /Send report/i }));
    expect(await within(q2).findByRole('button', { name: 'Reported' })).toBeInTheDocument();
  });
});

describe('Day 7 — rating, PDF and share', () => {
  it('saves the rating, and puts it back if the server refuses', async () => {
    const user = userEvent.setup();
    const r = report();
    const rate = vi.spyOn(reportService, 'rate').mockResolvedValueOnce().mockRejectedValueOnce({ status: 0, message: 'Unable to reach the server.' });
    renderReport(r);
    await user.click(screen.getAllByRole('radio', { name: /4 stars/ })[0]!);
    await waitFor(() => expect(useExamStore.getState().reports[r.id]!.rating).toBe(4));
    expect(rate).toHaveBeenCalledWith(r.id, 4);
    await user.click(screen.getAllByRole('radio', { name: /2 stars/ })[0]!);
    await waitFor(() => expect(useExamStore.getState().reports[r.id]!.rating).toBe(4)); // reverted
    expect(rate).toHaveBeenCalledTimes(2);
  });

  it('real reports: Download PDF gets the full server PDF, Copy share link creates a public link', async () => {
    const user = userEvent.setup();
    const pdf = vi.spyOn(reportService, 'downloadExamPdf').mockResolvedValue();
    const share = vi.spyOn(reportService, 'createShareLink').mockResolvedValue('http://localhost:5173/shared/reports/tok123');
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { value: { writeText }, configurable: true });
    const r = report();
    renderReport(r);
    await user.click(screen.getAllByRole('button', { name: 'Download PDF' })[0]!);
    expect(pdf).toHaveBeenCalledWith(expect.objectContaining({ id: r.id }));
    expect(screen.getAllByRole('button', { name: 'Print' }).length).toBeGreaterThan(0); // print layout is still there
    await user.click(screen.getAllByRole('button', { name: 'Copy share link' })[0]!);
    expect(share).toHaveBeenCalledWith(r.id);
    await waitFor(() => expect(writeText).toHaveBeenCalledWith('http://localhost:5173/shared/reports/tok123'));
  });

  it('the shared link page shows the score and feedback without logging in', async () => {
    const shared = toSharedReport({ kind: 'exam', title: 'IBPS PO Prelims', language: 'en', created_at: '2026-11-10T06:00:00Z', report: backendReport.report });
    vi.spyOn(reportService, 'getSharedReport').mockResolvedValue(shared);
    render(
      <MemoryRouter initialEntries={['/shared/reports/tok123']}>
        <Routes><Route path="/shared/reports/:token" element={<SharedReportPage />} /></Routes>
      </MemoryRouter>,
    );
    const score = await screen.findByTestId('shared-score');
    expect(score).toHaveTextContent('0.75/100');
    expect(score).toHaveTextContent('25%');
    expect(screen.getByText('Fill in the blanks')).toBeInTheDocument();
    expect(screen.getByText(/no name, phone number or questions/)).toBeInTheDocument();
  });
});

describe('Day 7 — PDF in the demo link (claude.ai artifact viewer)', () => {
  it('sends files through the viewer downloads capability, where direct downloads are blocked', async () => {
    const { saveFile, inArtifactViewer } = await import('@/lib/download');
    const save = vi.fn().mockResolvedValue({ status: 'saved' });
    (window as unknown as { claude?: unknown }).claude = { use: vi.fn(async (n: string) => (n === 'downloads' ? { save } : null)) };
    try {
      expect(inArtifactViewer()).toBe(true);
      const blob = new Blob(['%PDF-1.4'], { type: 'application/pdf' });
      await expect(saveFile('report.pdf', blob)).resolves.toBe('saved');
      expect(save).toHaveBeenCalledWith({ filename: 'report.pdf', data: blob });
      save.mockRejectedValueOnce({ code: 'declined', message: 'no' });
      await expect(saveFile('report.pdf', blob)).resolves.toBe('declined');
    } finally {
      delete (window as unknown as { claude?: unknown }).claude;
    }
  });
});
