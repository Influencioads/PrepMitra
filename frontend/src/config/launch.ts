import type { Exam, ExamCategory } from '@prepmitra/shared';

/**
 * Launch switches (read at call time so tests can change them).
 *
 *   VITE_OPEN_EXAM_CATEGORIES   comma list of exam categories students can attempt, or `all`.
 *                               Default `banking`: other exams are listed as "Coming soon".
 *   VITE_INTERVIEWS_ENABLED     `true` to show mock interviews. Default off.
 *
 * The free mini mock (the one-time free trial) always stays open so new users can try the product.
 */
const env = () => import.meta.env as Record<string, string | undefined>;

export function openExamCategories(): 'all' | ExamCategory[] {
  const raw = (env().VITE_OPEN_EXAM_CATEGORIES ?? 'banking').trim();
  if (!raw || raw === 'all') return 'all';
  return raw.split(',').map((s) => s.trim()).filter(Boolean) as ExamCategory[];
}

export const isCategoryOpen = (category: ExamCategory): boolean => {
  const open = openExamCategories();
  return open === 'all' || open.includes(category);
};

/** Can a student start this exam right now? */
export const isExamOpen = (exam: Pick<Exam, 'category' | 'isFree'>): boolean => exam.isFree || isCategoryOpen(exam.category);

export const interviewsEnabled = (): boolean => env().VITE_INTERVIEWS_ENABLED === 'true';

/** Open exams first, keeping the original order inside each group. */
export const openFirst = <T extends Pick<Exam, 'category' | 'isFree'>>(exams: T[]): T[] =>
  [...exams].sort((a, b) => Number(isExamOpen(b)) - Number(isExamOpen(a)));
