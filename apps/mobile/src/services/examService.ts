import type { Exam, ExamQuery, Question } from '@prepmitra/shared';
import { API_ENDPOINTS, EXAMS, getExamById, getQuestionById } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';

/** Pure filter/sort used by the mock service (same rules as the web app). */
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

export const examService = {
  /** GET /v1/exams */
  async list(query: ExamQuery = {}): Promise<Exam[]> {
    if (!USE_MOCK) return (await http.get<Exam[]>(API_ENDPOINTS.exams, { params: query })).data;
    await delay(350);
    return filterExams(EXAMS, query);
  },

  /** GET /v1/exams/{id} */
  async get(id: string): Promise<Exam> {
    if (!USE_MOCK) return (await http.get<Exam>(API_ENDPOINTS.exam(id))).data;
    await delay(300);
    const exam = getExamById(id);
    if (!exam || exam.status !== 'published') throw mockError(404, 'EXAM_NOT_FOUND', 'This exam is not available.');
    return exam;
  },

  getSync: (id: string): Exam | undefined => getExamById(id),
  getQuestion: (id: string): Question | undefined => getQuestionById(id),
};
