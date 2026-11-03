import type { Exam, InterviewRole, Question } from '../types/core';

/**
 * Live catalog: exams, interview roles and questions loaded from the real backend.
 * `getExamById`, `getRoleById` and `getQuestionById` look here first, so screens built
 * on the demo data show backend content without changes once the real API is on.
 */
const exams = new Map<string, Exam>();
const roles = new Map<string, InterviewRole>();
const questions = new Map<string, Question>();
let onChange: (() => void) | null = null;

export interface LiveSnapshot {
  exams: Exam[];
  roles: InterviewRole[];
  questions: Question[];
}

/** Keep at most this many questions (oldest dropped) so persisted storage stays small. */
const MAX_QUESTIONS = 1500;

export const liveCatalog = {
  registerExams(list: Exam[]) {
    for (const e of list) {
      const prev = exams.get(e.id);
      // A list item has no sections; keep the richer copy from GET /exams/{id}.
      exams.set(e.id, prev && prev.sections.length && !e.sections.length ? { ...e, sections: prev.sections } : e);
    }
    onChange?.();
  },
  registerRoles(list: InterviewRole[]) {
    for (const r of list) roles.set(r.id, r);
    onChange?.();
  },
  registerQuestions(list: Question[]) {
    for (const q of list) {
      const prev = questions.get(q.id);
      questions.delete(q.id);
      // Review data (explanation, answer key) arrives after the paper; never overwrite it with less.
      questions.set(q.id, prev ? { ...prev, ...q, explanation: q.explanation || prev.explanation, translations: { ...prev.translations, ...q.translations } } : q);
    }
    while (questions.size > MAX_QUESTIONS) questions.delete(questions.keys().next().value!);
    onChange?.();
  },
  /** Everything loaded so far, for the app to persist (e.g. localStorage) across page refreshes. */
  snapshot: (): LiveSnapshot => ({ exams: [...exams.values()], roles: [...roles.values()], questions: [...questions.values()] }),
  restore(snap: Partial<LiveSnapshot>) {
    for (const e of snap.exams ?? []) exams.set(e.id, e);
    for (const r of snap.roles ?? []) roles.set(r.id, r);
    for (const q of snap.questions ?? []) questions.set(q.id, q);
  },
  /** Called after every change, so the app can persist the snapshot. */
  onChange(fn: (() => void) | null) {
    onChange = fn;
  },
  exam: (id: string) => exams.get(id),
  role: (id: string) => roles.get(id),
  question: (id: string) => questions.get(id),
  exams: () => [...exams.values()],
  roles: () => [...roles.values()],
  clear() {
    exams.clear();
    roles.clear();
    questions.clear();
    onChange?.();
  },
};
