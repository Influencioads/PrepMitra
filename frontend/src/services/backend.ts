import type { Attempt, Exam, ExamReport, InterviewRole, LiveSnapshot } from '@prepmitra/shared';
import {
  backendIds, examIdFromSlug, examSlugFromId, getQuestionById, liveCatalog, roleSlugFromId, toAttempt, toExam, toExamReport, toRole,
} from '@prepmitra/shared';
import type { Json } from '@prepmitra/shared';
import { useExamStore } from '@/store/examStore';
import { http } from './http';

/**
 * Helpers for the real backend (VITE_USE_MOCK_API=false): catalog cache, exam papers and
 * report context. Response mapping lives in `@prepmitra/shared` (api/adapters.ts).
 */

// Persist what the live catalog has loaded, so an exam in progress survives a page refresh.
const LIVE_KEY = 'pm.live-catalog';
try {
  const raw = localStorage.getItem(LIVE_KEY);
  if (raw) liveCatalog.restore(JSON.parse(raw) as LiveSnapshot);
} catch {
  /* storage unavailable or corrupt — start empty */
}
let saveTimer: ReturnType<typeof setTimeout> | undefined;
liveCatalog.onChange(() => {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    try {
      localStorage.setItem(LIVE_KEY, JSON.stringify(liveCatalog.snapshot()));
    } catch {
      /* quota exceeded — the catalog is reloaded from the API when needed */
    }
  }, 300);
});

export async function fetchExams(): Promise<Exam[]> {
  const { data } = await http.get('/v1/exams', { params: { limit: 100 } });
  const exams = (data.items as Json[]).map(toExam);
  liveCatalog.registerExams(exams);
  return exams;
}

export async function fetchExam(id: string): Promise<Exam> {
  const exam = toExam((await http.get(`/v1/exams/${encodeURIComponent(examSlugFromId(id))}`)).data);
  liveCatalog.registerExams([exam]);
  return exam;
}

export async function fetchRoles(): Promise<InterviewRole[]> {
  const { data } = await http.get('/v1/interview-roles');
  const roles = ((data.items ?? data) as Json[]).map(toRole);
  liveCatalog.registerRoles(roles);
  return roles;
}

export async function examUuid(id: string): Promise<string> {
  return backendIds.exams.get(id) ?? (await fetchExam(id), backendIds.exams.get(id)!);
}

export async function roleUuid(id: string): Promise<string> {
  if (!backendIds.roles.has(id)) {
    const role = toRole((await http.get(`/v1/interview-roles/${encodeURIComponent(roleSlugFromId(id))}`)).data);
    liveCatalog.registerRoles([role]);
  }
  return backendIds.roles.get(id)!;
}

/** Frontend exam id for a backend exam UUID (loads the catalog once if needed). */
export async function examIdForUuid(uuid: string): Promise<string | undefined> {
  if (!backendIds.examByUuid.has(uuid)) await fetchExams().catch(() => undefined);
  return backendIds.examByUuid.get(uuid);
}

/** GET /v1/attempts/{id}/paper → Attempt, with its questions registered for the exam screen. */
export async function fetchPaper(attemptId: string, lang?: string): Promise<Attempt> {
  const { data } = await http.get(`/v1/attempts/${attemptId}/paper`, { params: lang && lang !== 'en' ? { lang } : undefined });
  if (!liveCatalog.exam(examIdFromSlug(data.exam.slug))) await fetchExam(examIdFromSlug(data.exam.slug)).catch(() => undefined);
  const { attempt, questions } = toAttempt(data);
  liveCatalog.registerQuestions(questions);
  revs.set(attemptId, Math.max(revs.get(attemptId) ?? 0, ...(data.questions as Json[]).map((q) => q.client_rev ?? 0)));
  return attempt;
}

// Autosave revisions must only grow; seconds since 2023 keep them monotonic across page refreshes.
const revs = new Map<string, number>();
export function nextRev(attemptId: string): number {
  const rev = Math.max((revs.get(attemptId) ?? 0) + 1, Math.floor(Date.now() / 1000) - 1_670_000_000);
  revs.set(attemptId, rev);
  return rev;
}

export const questionLookup = getQuestionById;

/** Exam title/duration for a report, from the local attempt or the catalog. */
export function reportContext(attemptId: string, fallbackExamId?: string) {
  const attempt = useExamStore.getState().attempts[attemptId];
  const examId = attempt?.examId ?? fallbackExamId ?? '';
  const exam = liveCatalog.exam(examId);
  return {
    examId,
    examTitle: exam?.title ?? examId,
    durationSec: attempt?.durationSec ?? (exam?.durationMin ?? 0) * 60,
    isMini: attempt?.isMini ?? exam?.isFree,
  };
}

export const mapExamReport = (body: Json, attemptId: string, fallbackExamId?: string): ExamReport =>
  toExamReport(body, reportContext(attemptId, fallbackExamId));
