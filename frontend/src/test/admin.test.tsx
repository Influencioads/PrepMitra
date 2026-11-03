import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it } from 'vitest';
import { AdminExamFormPage } from '@/pages/admin/AdminExamFormPage';
import { AdminExamsPage } from '@/pages/admin/AdminExamsPage';
import { AdminRolesPage } from '@/pages/admin/AdminRolesPage';
import { createAdminSeed, useAdminStore } from '@/store/adminStore';
import { resetAdminLoadCache } from '@/components/admin/useAdminLoad';

function renderAdmin(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/admin/exams" element={<AdminExamsPage />} />
        <Route path="/admin/exams/new" element={<AdminExamFormPage />} />
        <Route path="/admin/exams/:examId/edit" element={<AdminExamFormPage />} />
        <Route path="/admin/interview-roles" element={<AdminRolesPage />} />
      </Routes>
    </MemoryRouter>,
  );
}

beforeEach(() => {
  resetAdminLoadCache();
  useAdminStore.setState(createAdminSeed());
});

describe('admin console', () => {
  it('creates an exam through the form and shows it in the exams table', async () => {
    const user = userEvent.setup();
    const before = useAdminStore.getState().exams.length;
    const auditBefore = useAdminStore.getState().auditLog.length;
    renderAdmin('/admin/exams/new');

    await user.type(await screen.findByLabelText(/^Title/), 'Maharashtra Police Bharti Mock');
    await user.type(screen.getByLabelText(/^Short title/), 'MH Police');
    await user.type(screen.getByLabelText(/^Pattern source/), 'MPSC pattern');
    await user.type(screen.getByLabelText(/^Description/), 'Full mock based on the public police constable recruitment pattern.');
    await user.type(screen.getByLabelText(/^Name/), 'General Knowledge');
    await user.click(screen.getByRole('button', { name: 'Create exam' }));

    expect(await screen.findByRole('heading', { name: 'Exams & blueprints' })).toBeInTheDocument();
    const table = await screen.findByRole('table');
    expect(within(table).getByText('Maharashtra Police Bharti Mock')).toBeInTheDocument();

    const state = useAdminStore.getState();
    expect(state.exams).toHaveLength(before + 1);
    const created = state.exams.find((e) => e.shortTitle === 'MH Police')!;
    expect(created.status).toBe('draft');
    expect(created.totalQuestions).toBe(25);
    expect(state.auditLog.length).toBe(auditBefore + 1);
    expect(state.auditLog[0]!.action).toBe('Created exam');
  });

  it('shows field errors and does not save an invalid exam', async () => {
    const user = userEvent.setup();
    const before = useAdminStore.getState().exams.length;
    renderAdmin('/admin/exams/new');
    await user.click(await screen.findByRole('button', { name: 'Create exam' }));
    expect(await screen.findByText('Title is required')).toBeInTheDocument();
    expect(screen.getByText('Name the section')).toBeInTheDocument();
    expect(useAdminStore.getState().exams).toHaveLength(before);
  });

  it('rejects a scoring rubric whose weights do not add up to 100', async () => {
    const user = userEvent.setup();
    renderAdmin('/admin/interview-roles?tab=rubric');
    const weight = (await screen.findAllByLabelText(/^Weight %/))[0]!;
    await user.clear(weight);
    await user.type(weight, '40');
    await user.click(screen.getByRole('button', { name: 'Save rubric' }));
    expect(await screen.findByText(/must add up to 100% \(currently 110%\)/)).toBeInTheDocument();
    expect(useAdminStore.getState().interviewer.rubric[0]!.weight).toBe(30);
  });

  it('seeds users whose credit ledgers reconcile with their balances', () => {
    for (const u of useAdminStore.getState().users) {
      expect(u.ledger.reduce((s, l) => s + l.delta, 0)).toBe(u.credits);
    }
  });

  it('confirming a review fix verifies the question and creates an AI lesson', () => {
    const { resolveReview } = useAdminStore.getState();
    const lessonsBefore = useAdminStore.getState().lessons.length;
    const lesson = resolveReview('rv-2', 'fixed', { note: 'Answer key corrected', correct: [1], lessonText: 'Define the alphabet in every language-class question.' });
    const s = useAdminStore.getState();
    expect(lesson?.source).toBe('review-fix');
    expect(s.lessons).toHaveLength(lessonsBefore + 1);
    expect(s.questions.find((q) => q.id === 'q-cs-7')?.status).toBe('verified');
    expect(s.reviewQueue.find((r) => r.id === 'rv-2')?.status).toBe('fixed');
  });
});

