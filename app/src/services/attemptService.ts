import type { Attempt, Exam, ExamReport, LanguageCode } from '@prepmitra/shared';
import { API_ENDPOINTS, buildExamReport, createDemoAttempt, createId } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay } from './mock';

export const attemptService = {
  /** POST /v1/attempts — server deducts a credit and assigns a pre-generated paper. */
  async start(exam: Exam, language: LanguageCode): Promise<Attempt> {
    if (!USE_MOCK) return (await http.post<Attempt>(API_ENDPOINTS.attempts, { examId: exam.id, language })).data;
    await delay(700);
    return createDemoAttempt(exam, { id: createId('att'), language });
  },

  /** PUT /v1/attempts/{id}/answers — batched autosave. The mock persists locally via the store. */
  async saveAnswers(attempt: Attempt): Promise<void> {
    if (!USE_MOCK) {
      await http.put(API_ENDPOINTS.attemptAnswers(attempt.id), { states: attempt.states, currentIndex: attempt.currentIndex });
      return;
    }
    await delay(120);
  },

  /** POST /v1/attempts/{id}/submit — scoring runs on the server in production. */
  async submit(exam: Exam, attempt: Attempt): Promise<ExamReport> {
    if (!USE_MOCK) return (await http.post<ExamReport>(API_ENDPOINTS.attemptSubmit(attempt.id))).data;
    await delay(1200);
    return buildExamReport(exam, attempt, { id: createId('rep') });
  },
};
