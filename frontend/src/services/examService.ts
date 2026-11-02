import type { Exam, ExamQuery, Question } from '@prepmitra/shared';
import { EXAMS, getExamById, getQuestionById, liveCatalog } from '@prepmitra/shared';
import { fetchExam, fetchExams } from './backend';
import { USE_MOCK, delay, mockError } from './mock';

/** Pure filter/sort used by the mock service (and unit-tested). */
export function filterExams(exams: Exam[], q: ExamQuery): Exam[] {
  const term = q.search?.trim().toLowerCase() ?? '';
  const result = exams.filter((e) => {
    if (e.status !== 'published') return false;
    if (q.category && q.category !== 'all' && e.category !== q.category) return false;
    if (q.difficulty && q.difficulty !== 'all' && e.difficulty !== q.difficulty) return false;
    if (q.language && q.language !== 'all' && !e.languages.includes(q.language)) return false;
    if (term && !`${e.title} ${e.shortTitle} ${e.conductingBody} ${e.description}`.toLowerCase().includes(term)) return false;
    return true;
  });
  const sorters: Record<NonNullable<ExamQuery['sort']>, (a: Exam, b: Exam) => number> = {
    popular: (a, b) => b.popularity - a.popularity,
    rating: (a, b) => b.rating - a.rating,
    'duration-asc': (a, b) => a.durationMin - b.durationMin,
    'duration-desc': (a, b) => b.durationMin - a.durationMin,
    'credits-asc': (a, b) => a.creditCost - b.creditCost,
    title: (a, b) => a.shortTitle.localeCompare(b.shortTitle),
  };
  return result.sort(sorters[q.sort ?? 'popular']);
}

/** Admin-managed exams override the static catalog when present (see adminStore). */
let catalogSource: () => Exam[] = () => EXAMS;
export const setExamCatalogSource = (fn: () => Exam[]) => {
  catalogSource = fn;
};

export const examService = {
  /** GET /v1/exams */
  async list(query: ExamQuery = {}): Promise<Exam[]> {
    if (!USE_MOCK) return filterExams(await fetchExams(), query);
    await delay(350);
    return filterExams(catalogSource(), query);
  },

  /** GET /v1/exams/{id} */
  async get(id: string): Promise<Exam> {
    if (!USE_MOCK) return fetchExam(id);
    await delay(300);
    const exam = catalogSource().find((e) => e.id === id) ?? getExamById(id);
    if (!exam || exam.status !== 'published') throw mockError(404, 'EXAM_NOT_FOUND', 'This exam is not available.');
    return exam;
  },

  getSync: (id: string): Exam | undefined =>
    (USE_MOCK ? undefined : liveCatalog.exam(id)) ?? catalogSource().find((e) => e.id === id) ?? getExamById(id),
  getQuestion: (id: string): Question | undefined => getQuestionById(id),
};
