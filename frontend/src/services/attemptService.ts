import type { Attempt, AttemptEvent, Exam, ExamReport, LanguageCode, QuestionReviewItem } from '@prepmitra/shared';
import {
  API_ENDPOINTS, buildExamReport, createDemoAttempt, createId, getQuestionById, liveCatalog, scoreAttempt, toAnswersBody, toReview,
} from '@prepmitra/shared';
import { examUuid, fetchPaper, nextRev } from './backend';
import { http } from './http';
import { USE_MOCK, delay } from './mock';

export const attemptService = {
  /** POST /v1/attempts — server deducts a credit (or uses the free trial) and assigns a pre-generated paper. */
  async start(exam: Exam, language: LanguageCode, opts: { mini?: boolean } = {}): Promise<Attempt> {
    if (!USE_MOCK) {
      // The free mini mock is its own exam on the backend (exam.isFree); any other exam is a full paper.
      const { data } = await http.post(API_ENDPOINTS.attempts, { exam_id: await examUuid(exam.id), language });
      void import('@/store/sync').then((m) => m.syncCredits()).catch(() => undefined);
      // GET /paper returns the questions (never the answers), server end time and any saved answers.
      return fetchPaper(data.id, language);
    }
    await delay(700);
    return createDemoAttempt(exam, { id: createId('att'), language, mini: opts.mini });
  },

  /** GET /v1/attempts/{id}/paper — reload a paper (resume, or another language). */
  fetchPaper,

  /**
   * POST /v1/attempts/{id}/events — tab switches, copy/paste and right-click attempts, network
   * drops (logged, not punished). Events that cannot be sent (offline) wait in browser storage
   * and go with the next successful call or when the network returns.
   */
  async logEvent(attemptId: string, event: AttemptEvent): Promise<void> {
    queueEvent(attemptId, event);
    await flushEvents(attemptId);
  },

  /** Sends any events still waiting for this attempt. */
  flushEvents: (attemptId: string) => flushEvents(attemptId),

  /** GET /v1/attempts/{id}/review — question-by-question review after submit. */
  async fetchReview(attempt: Attempt): Promise<QuestionReviewItem[]> {
    if (!USE_MOCK) {
      const { items, questions } = toReview((await http.get(API_ENDPOINTS.attemptReview(attempt.id))).data);
      liveCatalog.registerQuestions(questions);
      return items;
    }
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

  /** Loads review data for a report so its question list can show text, answers and explanations. */
  async loadReviewQuestions(attemptId: string): Promise<void> {
    if (USE_MOCK) return;
    liveCatalog.registerQuestions(toReview((await http.get(API_ENDPOINTS.attemptReview(attemptId))).data).questions);
  },

  /**
   * GET /v1/attempts/{id}/review by attempt id: every question with the student's answer, the answer key,
   * explanation and shortcut, in the attempt's language. Registers the questions so the report can show them.
   */
  async fetchReviewItems(attemptId: string): Promise<QuestionReviewItem[]> {
    if (USE_MOCK) return [];
    const { items, questions } = toReview((await http.get(API_ENDPOINTS.attemptReview(attemptId))).data);
    liveCatalog.registerQuestions(questions);
    return items;
  },

  /**
   * PUT /v1/attempts/{id}/answers — batched autosave. The mock persists locally via the store.
   * Returns the server's remaining seconds so the timer can follow the server clock.
   */
  async saveAnswers(attempt: Attempt): Promise<{ remainingSec?: number }> {
    if (!USE_MOCK) {
      const { data } = await http.put(API_ENDPOINTS.attemptAnswers(attempt.id), toAnswersBody(attempt, nextRev(attempt.id), getQuestionById));
      void flushEvents(attempt.id);
      return { remainingSec: typeof data?.remaining_seconds === 'number' ? data.remaining_seconds : undefined };
    }
    await delay(120);
    return {};
  },

  /**
   * POST /v1/attempts/{id}/submit — scoring runs on the server. In real mode this only
   * starts the report job; callers then use reportService.pollExamReport.
   */
  async submit(exam: Exam, attempt: Attempt): Promise<ExamReport | null> {
    if (!USE_MOCK) {
      // Flush the final answers first; the server rejects writes after its deadline (+ grace), which is fine.
      await http.put(API_ENDPOINTS.attemptAnswers(attempt.id), toAnswersBody(attempt, nextRev(attempt.id), getQuestionById)).catch(() => undefined);
      await http.post(API_ENDPOINTS.attemptSubmit(attempt.id));
      return null;
    }
    await delay(1200);
    return buildExamReport(exam, attempt, { id: createId('rep') });
  },

  /** POST /v1/questions/{id}/flags — hidden from new papers after 3 independent flags. */
  async reportQuestion(questionId: string, reason: string, note?: string): Promise<void> {
    if (!USE_MOCK) {
      await http.post(API_ENDPOINTS.questionFlags(questionId), { reason: FLAG_REASONS[reason] ?? 'other', details: note ?? '' });
      return;
    }
    await delay(400);
  },
};

// ---- Anti-cheat event queue (survives reloads and offline periods) ----
const EVENTS_KEY = 'pm.pendingEvents';
type Pending = Record<string, AttemptEvent[]>;
const readPending = (): Pending => {
  try {
    return JSON.parse(localStorage.getItem(EVENTS_KEY) ?? '{}') as Pending;
  } catch {
    return {};
  }
};
const writePending = (p: Pending) => {
  try {
    localStorage.setItem(EVENTS_KEY, JSON.stringify(p));
  } catch {
    /* storage full or blocked: events are best effort */
  }
};
function queueEvent(attemptId: string, event: AttemptEvent) {
  const p = readPending();
  p[attemptId] = [...(p[attemptId] ?? []), event].slice(-100);
  writePending(p);
}
const flushing = new Set<string>();
async function flushEvents(attemptId: string): Promise<void> {
  if (flushing.has(attemptId)) return;
  const events = readPending()[attemptId] ?? [];
  if (!events.length) return;
  flushing.add(attemptId);
  try {
    if (!USE_MOCK) await http.post(API_ENDPOINTS.attemptEvents(attemptId), { events });
    else await delay(50);
    const p = readPending();
    p[attemptId] = (p[attemptId] ?? []).slice(events.length);
    if (!p[attemptId]!.length) delete p[attemptId];
    writePending(p);
  } catch (e) {
    // Closed attempts (409) or invalid events (422) will never succeed: drop them. Network errors stay queued.
    const err = e as { status?: number; response?: { status?: number } };
    const status = err?.status || err?.response?.status;
    if (status && status >= 400 && status < 500) {
      const p = readPending();
      delete p[attemptId];
      writePending(p);
    }
  } finally {
    flushing.delete(attemptId);
  }
}

/** Report-question reasons in the UI → backend reasons (wrong_answer | unclear | bad_translation | other). */
const FLAG_REASONS: Record<string, string> = {
  'wrong-answer': 'wrong_answer', wrong_answer: 'wrong_answer', 'wrong-key': 'wrong_answer',
  unclear: 'unclear', typo: 'unclear', 'unclear-question': 'unclear',
  translation: 'bad_translation', 'bad-translation': 'bad_translation', bad_translation: 'bad_translation',
};
