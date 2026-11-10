import { render, screen, within } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { EXAMS, buildDemoPaper, examIdFromSlug, getExamById, subjectFromSection } from '@prepmitra/shared';
import { interviewsEnabled, isExamOpen, openExamCategories } from '@/config/launch';
import { ExamCatalogPage } from '@/pages/public/ExamCatalogPage';
import { ExamDetailsPage } from '@/pages/public/ExamDetailsPage';
import { ExamInstructionsPage } from '@/pages/exam/ExamInstructionsPage';

// Launch settings: banking exams only, interviews off (the production defaults).
beforeEach(() => {
  vi.stubEnv('VITE_OPEN_EXAM_CATEGORIES', 'banking');
  vi.stubEnv('VITE_INTERVIEWS_ENABLED', 'false');
});
afterEach(() => vi.unstubAllEnvs());

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/exams" element={<ExamCatalogPage />} />
        <Route path="/exams/:id" element={<ExamDetailsPage />} />
        <Route path="/exams/:id/instructions" element={<ExamInstructionsPage />} />
      </Routes>
    </MemoryRouter>,
  );
}

describe('Launch: banking exams only', () => {
  it('opens banking exams and the free mini mock; everything else is coming soon', () => {
    expect(openExamCategories()).toEqual(['banking']);
    expect(isExamOpen(getExamById('ibps-po')!)).toBe(true);
    expect(isExamOpen(getExamById('sbi-po')!)).toBe(true);
    expect(isExamOpen(getExamById('ssc-cgl')!)).toBe(false);
    expect(isExamOpen(getExamById('general-aptitude')!)).toBe(true); // the one-time free trial
    expect(interviewsEnabled()).toBe(false);
  });

  it('catalog: banking cards first, other cards say "Coming soon", no interviews', async () => {
    renderAt('/exams');
    const section = (await screen.findByRole('heading', { name: /^Exam mocks/ })).closest('section')!;
    const titles = (await within(section).findAllByRole('heading', { level: 3 })).map((h) => h.textContent);
    const firstClosed = titles.findIndex((x) => !/IBPS|SBI/.test(x ?? ''));
    expect(titles.slice(0, firstClosed).every((x) => /IBPS|SBI/.test(x ?? ''))).toBe(true);
    const ssc = within(section).getByRole('link', { name: /SSC CGL Tier 1/ });
    expect(within(ssc).getAllByText('Coming soon').length).toBeGreaterThan(0);
    const ibps = within(section).getByRole('link', { name: /IBPS PO Prelims/ });
    expect(within(ibps).queryByText('Coming soon')).not.toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: /^Mock interviews/ })).not.toBeInTheDocument();
    expect(screen.getByText('open now')).toBeInTheDocument();
  });

  it('detail page of a closed exam has no start buttons', async () => {
    renderAt('/exams/ssc-cgl');
    expect(await screen.findByText('Opening soon')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Start/ })).not.toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'See open exams' })).toHaveAttribute('href', '/exams?category=banking');
  });

  it('detail page of a banking exam can be started', async () => {
    renderAt('/exams/ibps-po');
    expect(await screen.findByRole('button', { name: /Start full mock/ })).toBeInTheDocument();
    expect(screen.queryByText('Opening soon')).not.toBeInTheDocument();
  });

  it('a direct link to the instructions of a closed exam goes back to its detail page', async () => {
    renderAt('/exams/ssc-cgl/instructions');
    expect(await screen.findByText('Opening soon')).toBeInTheDocument();
  });
});

describe('Banking catalog matches the backend question bank', () => {
  // GET /v1/exams on the backend with the 10,000-question bank: 6 banking exams × prelims + mains.
  const BACKEND_BANKING = [
    'ibps-po-prelims', 'ibps-po-mains', 'ibps-clerk-prelims', 'ibps-clerk-mains', 'sbi-po-prelims', 'sbi-po-mains',
    'sbi-junior-associate-prelims', 'sbi-junior-associate-mains', 'ibps-rrb-officer-prelims', 'ibps-rrb-officer-mains',
    'ibps-rrb-office-assistant-prelims', 'ibps-rrb-office-assistant-mains',
  ];

  it('has every backend banking exam, open now, with a demo paper covering every section', () => {
    for (const slug of BACKEND_BANKING) {
      const exam = getExamById(examIdFromSlug(slug));
      expect(exam, slug).toBeDefined();
      expect(exam!.category).toBe('banking');
      expect(isExamOpen(exam!)).toBe(true);
      expect(exam!.sections.reduce((n, s) => n + s.questionCount, 0)).toBe(exam!.totalQuestions);
      const paper = buildDemoPaper(exam!, `t-${slug}`);
      expect(new Set(paper.map((p) => p.sectionId)).size, slug).toBe(exam!.sections.length);
    }
    expect(EXAMS.filter((e) => e.category === 'banking')).toHaveLength(12);
  });

  it('maps the new section names to the right subject', () => {
    expect(subjectFromSection('reasoning_computer', 'Reasoning & Computer Aptitude')).toBe('reasoning');
    expect(subjectFromSection('dai', 'Data Analysis & Interpretation')).toBe('data-interpretation');
    expect(subjectFromSection('numerical', 'Numerical Ability')).toBe('quant');
    expect(subjectFromSection('computer', 'Computer Knowledge')).toBe('computer-science');
    expect(subjectFromSection('ga', 'General/ Economy/ Banking Awareness/ Digital/ Financial Awareness including RBI circulars')).toBe('general-awareness');
    expect(subjectFromSection('language', 'English Language (or Hindi Language - candidate opts one)')).toBe('english');
    expect(subjectFromSection('quant', 'Quantitative Aptitude')).toBe('quant');
  });
});
