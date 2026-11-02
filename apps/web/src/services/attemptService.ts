import type { Attempt, AttemptEvent, Exam, ExamReport, LanguageCode, QuestionReviewItem } from '@prepmitra/shared';
import { API_ENDPOINTS, buildExamReport, createDemoAttempt, createId, getQuestionById, scoreAttempt } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay } from './mock';

export const attemptService = {
  /** POST /v1/attempts — server deducts a credit and assigns a pre-generated paper. */
  async start(exam: Exam, language: LanguageCode, opts: { mini?: boolean } = {}): Promise<Attempt> {
    if (!USE_MOCK) {
      const created = (await http.post<Attempt>(API_ENDPOINTS.attempts, { examId: exam.id, language, mode: opts.mini ? 'mini' : 'full' })).data;
      // GET /paper returns the questions (never the answers), server end time and any saved answers.
      return (await http.get<Attempt>(API_ENDPOINTS.attemptPaper(created.id, language))).data;
    }
    await delay(700);
    return createDemoAttempt(exam, { id: createId('att'), language, mini: opts.mini });
  },

  /** POST /v1/attempts/{id}/events — tab switches and copy attempts (logged, not punished). */
  async logEvent(attemptId: string, event: AttemptEvent): Promise<void> {
    if (!USE_MOCK) {
      await http.post(API_ENDPOINTS.attemptEvents(attemptId), event).catch(() => undefined);
      return;
    }
    await delay(50);
  },

  /** GET /v1/attempts/{id}/review — question-by-question review after submit. */
  async fetchReview(attempt: Attempt): Promise<QuestionReviewItem[]> {
    if (!USE_MOCK) return (await http.get<QuestionReviewItem[]>(API_ENDPOINTS.attemptReview(attempt.id))).data;
    await delay(200);
    const result = scoreAttempt(attempt.paper, attempt.states, getQuestionById);
    return result.questions.map((q, i) => ({
      questionId: q.questionId,
      number: i + 1,
      sectionId: q.sectionId,
      question: getQuestionById(q.questionId)!,
      answer: attempt.states[q.questionId]?.answer,
      outcome: q.outcome,
      marksAwarded: q.marksAwarded,
      timeSpentSec: q.timeSpentSec,
    }));
  },

  /** PUT /v1/attempts/{id}/answers — batched autosave. The mock persists locally via the store. */
  async saveAnswers(attempt: Attempt): Promise<void> {
    if (!USE_MOCK) {
      await http.put(API_ENDPOINTS.attemptAnswers(attempt.id), { states: attempt.states, currentIndex: attempt.currentIndex });
      return;
    }
    await delay(120);
  },

  /**
   * POST /v1/attempts/{id}/submit — scoring runs on the server. In real mode this only
   * starts the report job; callers then use reportService.pollExamReport.
   */
  async submit(exam: Exam, attempt: Attempt): Promise<ExamReport | null> {
    if (!USE_MOCK) {
      await http.post(API_ENDPOINTS.attemptSubmit(attempt.id), { states: attempt.states, autoSubmitted: !!attempt.autoSubmitted });
      return null;
    }
    await delay(1200);
    return buildExamReport(exam, attempt, { id: createId('rep') });
  },

  /** POST /v1/questions/{id}/flags — hidden from new papers after 3 independent flags. */
  async reportQuestion(questionId: string, reason: string, note?: string): Promise<void> {
    if (!USE_MOCK) {
      await http.post(API_ENDPOINTS.questionFlags(questionId), { reason, note });
      return;
    }
    await delay(400);
  },
};
