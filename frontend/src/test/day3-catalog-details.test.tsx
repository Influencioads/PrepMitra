import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, vi } from 'vitest';
import { toExam, toRole } from '@prepmitra/shared';
import { useI18nStore } from '@/i18n';
import { contentText } from '@/i18n/content';
import { examService, interviewService } from '@/services';
import { ExamCatalogPage } from '@/pages/public/ExamCatalogPage';
import { ExamDetailsPage } from '@/pages/public/ExamDetailsPage';

/** Shapes returned by GET /v1/exams, /v1/exams/{slug} and /v1/interview-roles (trimmed). */
const section = (key: string, name: string, n: number, marks: number, neg: number) => ({
  key, name, question_count: n, marks_per_question: marks, negative_marks: neg, question_types: { single: n }, duration_min: null,
});
const apiExam = (slug: string, name: string, category: string, n: number, sections: ReturnType<typeof section>[], free = false) => ({
  id: `uuid-${slug}`, slug, name, category, description: `${name} description`, credits_required: 1, is_free_trial: free,
  duration_min: free ? 30 : 60, question_count: n, total_marks: n * (sections[0]?.marks_per_question ?? 1), languages: ['en', 'hi'],
  pattern: { duration_min: 60, sections, negative_marking: sections.some((s) => s.negative_marks > 0), difficulty_mix: { easy: 30, medium: 50, hard: 20 }, calculator_allowed: false },
  sample_question: { text: '[Number system] Compute 44 × 39.', options: [{ key: 'A', text: '1706' }, { key: 'B', text: '1716' }], answer: 'B' },
});
const SSC = apiExam('ssc-cgl-tier1', 'SSC CGL Tier-1', 'central_govt', 100, [
  section('reasoning', 'General Intelligence and Reasoning', 25, 2, 0.5),
  section('ga', 'General Awareness', 25, 2, 0.5),
  section('quant', 'Quantitative Aptitude', 25, 2, 0.5),
  section('english', 'English Comprehension', 25, 2, 0.5),
]);
const IBPS = apiExam('ibps-po-prelims', 'IBPS PO Prelims', 'banking', 100, [
  section('english', 'English Language', 30, 1, 0.25), section('quant', 'Quantitative Aptitude', 35, 1, 0.25), section('reasoning', 'Reasoning Ability', 35, 1, 0.25),
]);
const IT = apiExam('it-placement-aptitude', 'Campus Placement Aptitude (IT services)', 'campus_hiring', 60, [
  section('quant', 'Quantitative aptitude', 20, 1, 0), section('logical', 'Logical reasoning', 20, 1, 0), section('verbal', 'Verbal ability', 20, 1, 0),
]);
const MINI = apiExam('mini-mock-general-aptitude', 'Free Mini Mock - General Aptitude', 'campus_hiring', 30, [section('quant', 'Quantitative aptitude', 10, 1, 0.25)], true);
const ROLES = [
  { id: 'r1', slug: 'bank-po-interview', name: 'Bank PO interview', description: 'Bank PO mock interview.', levels: ['fresher'], modes: ['text', 'voice'], credits_required: 1 },
  { id: 'r2', slug: 'software-developer-fresher', name: 'Software developer (fresher)', description: 'Developer mock interview.', levels: ['fresher'], modes: ['text'], credits_required: 1 },
];

const exams = [MINI, IT, IBPS, SSC].map(toExam);
const roles = ROLES.map(toRole);

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/exams" element={<ExamCatalogPage />} />
        <Route path="/exams/:id" element={<ExamDetailsPage />} />
      </Routes>
    </MemoryRouter>,
  );
}

beforeEach(() => {
  vi.spyOn(examService, 'list').mockResolvedValue(exams);
  vi.spyOn(examService, 'get').mockImplementation(async (id) => exams.find((e) => e.id === id)!);
  vi.spyOn(interviewService, 'listRoles').mockResolvedValue(roles);
});
afterEach(() => {
  vi.restoreAllMocks();
  useI18nStore.getState().setLang('en');
});

describe('Day 3 — catalog from the API', () => {
  it('never shows a made-up rating for backend exams', () => {
    for (const e of exams) {
      expect(e.rating).toBe(0);
      expect(e.highlights).toEqual([]);
    }
  });

  it('lists the 3 exams and 2 interview roles, with the free mini mock promoted separately', async () => {
    renderAt('/exams');
    const examsSection = (await screen.findByRole('heading', { name: /^Exam mocks/ })).closest('section')!;
    await waitFor(() => expect(within(examsSection).getAllByRole('heading', { level: 3 })).toHaveLength(3));
    for (const title of ['SSC CGL Tier-1', 'IBPS PO Prelims', 'Campus Placement Aptitude (IT services)']) {
      expect(within(examsSection).getByRole('heading', { name: title })).toBeInTheDocument();
    }
    const rolesSection = screen.getByRole('heading', { name: /^Mock interviews/ }).closest('section')!;
    expect(within(rolesSection).getAllByRole('heading', { level: 3 })).toHaveLength(2);
    expect(within(examsSection).getByRole('link', { name: 'View details for SSC CGL Tier-1' })).toHaveAttribute('href', '/exams/ssc-cgl');
        expect(screen.getByRole('link', { name: /Free 30-minute mini mock/ })).toHaveAttribute('href', '/exams/general-aptitude');
    // Only categories with content get a tile (no empty Railway / Civil Services).
    const tiles = within(screen.getByRole('group', { name: 'Filter by category' })).getAllByRole('button');
    expect(tiles.map((b) => b.textContent)).toEqual(['All', 'Government Exams1', 'Banking Exams1', 'Campus Placements1', 'Interviews2']);
  });

  it('filters by category and by search', async () => {
    const user = userEvent.setup();
    renderAt('/exams');
    await screen.findByRole('heading', { name: 'SSC CGL Tier-1' });
    await user.click(screen.getByRole('button', { name: /Banking Exams/ }));
    expect(screen.getByRole('heading', { name: 'IBPS PO Prelims' })).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: 'SSC CGL Tier-1' })).not.toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: /^Mock interviews/ })).not.toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /Interviews/ }));
    expect(screen.queryByRole('heading', { name: /^Exam mocks/ })).not.toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Bank PO interview' })).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /^All/ }));
    await user.type(screen.getByRole('searchbox', { name: 'Search exams and interviews' }), 'developer');
    await waitFor(() => expect(screen.queryByRole('heading', { name: 'SSC CGL Tier-1' })).not.toBeInTheDocument());
    expect(screen.getByRole('heading', { name: 'Software developer (fresher)' })).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: 'Bank PO interview' })).not.toBeInTheDocument();
  });

  it('switches the catalog to Hindi, including API content', async () => {
    useI18nStore.getState().setLang('hi');
    renderAt('/exams');
    expect(await screen.findByRole('heading', { level: 1 })).toHaveTextContent('आप किसकी तैयारी कर रहे हैं?');
    expect(await screen.findByRole('heading', { name: 'कैंपस प्लेसमेंट एप्टीट्यूड (IT सर्विसेज़)' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Bank PO इंटरव्यू' })).toBeInTheDocument();
  });
});

describe('Day 3 — exam detail page matches the blueprint', () => {
  it.each([
    ['ssc-cgl', 'SSC CGL Tier-1', 4, '200 marks', '−0.5'],
    ['ibps-po', 'IBPS PO Prelims', 3, '100 marks', '−0.25'],
    ['it-placement', 'Campus Placement Aptitude (IT services)', 3, '60 marks', 'None'],
  ])('%s: pattern table, price, sample question and both start buttons', async (id, title, sectionCount, marks, negative) => {
    renderAt(`/exams/${id}`);
    expect(await screen.findByRole('heading', { level: 1, name: title })).toBeInTheDocument();
    const table = screen.getByRole('table');
    const rows = within(table).getAllByRole('row');
    expect(rows).toHaveLength(sectionCount + 2); // header + sections + total
    expect(within(table).getByText(marks)).toBeInTheDocument();
    expect(within(table).getAllByText(negative).length).toBe(sectionCount);
    expect(within(table).getByText('60 min')).toBeInTheDocument();
    expect(screen.getAllByText('1 credit').length).toBeGreaterThan(0);
    expect(screen.getByText('Full mock · or ₹29 as a single mock')).toBeInTheDocument();
    expect(screen.getByText('Compute 44 × 39.')).toBeInTheDocument();
    expect(screen.getByText('Topic: Number system')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start free mini mock (30 min)' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start full mock' })).toBeInTheDocument();
    expect(screen.queryByText(/rating/i)).not.toBeInTheDocument();
  });

  it('sample question gives instant feedback', async () => {
    const user = userEvent.setup();
    renderAt('/exams/ssc-cgl');
    await user.click(await screen.findByRole('radio', { name: /1706/ }));
    expect(screen.getByRole('status')).toHaveTextContent('the answer is B');
  });
});

describe('Content translation table', () => {
  it('translates known content, generated marking rules, and falls back to English', () => {
    expect(contentText('General Awareness', 'hi')).toBe('सामान्य जागरूकता');
    expect(contentText('−0.5 per wrong answer', 'hi')).toBe('हर गलत उत्तर पर −0.5');
    expect(contentText('SSC pattern', 'hi')).toBe('SSC पैटर्न');
    expect(contentText('A brand new admin exam', 'hi')).toBe('A brand new admin exam');
    expect(contentText('General Awareness', 'en')).toBe('General Awareness');
  });
});
