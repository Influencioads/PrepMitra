import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Attempt, AttemptSummary, ExamReport, PracticeLog } from '@prepmitra/shared';
import { STORAGE_KEYS, addPractice, toAttemptSummary } from '@prepmitra/shared';
import { demoStorage } from './storage';

interface ExamState {
  ownerId: string | null;
  attempts: Record<string, Attempt>;
  reports: Record<string, ExamReport>;
  practiceLog: PracticeLog;
  reset: (ownerId: string, attempts: Attempt[], reports: ExamReport[], practiceLog?: PracticeLog) => void;
  logPractice: (minutes: number) => void;
  saveAttempt: (attempt: Attempt) => void;
  updateAttempt: (id: string, fn: (a: Attempt) => Attempt) => void;
  completeAttempt: (attempt: Attempt, report: ExamReport) => void;
  discardAttempt: (id: string) => void;
  rateReport: (reportId: string, rating: number) => void;
}

const toRecord = <T extends { id: string }>(items: T[]) => Object.fromEntries(items.map((i) => [i.id, i]));

/** Attempts are persisted to AsyncStorage so an unfinished exam survives an app restart (MVP doc §5.3). */
export const useExamStore = create<ExamState>()(
  persist(
    (set) => ({
      ownerId: null,
      attempts: {},
      reports: {},
      practiceLog: {},
      reset: (ownerId, attempts, reports, practiceLog = {}) =>
        set({ ownerId, attempts: toRecord(attempts), reports: toRecord(reports), practiceLog }),
      logPractice: (minutes) => set((s) => ({ practiceLog: addPractice(s.practiceLog, minutes) })),
      saveAttempt: (attempt) => set((s) => ({ attempts: { ...s.attempts, [attempt.id]: attempt } })),
      updateAttempt: (id, fn) =>
        set((s) => {
          const current = s.attempts[id];
          if (!current || current.status !== 'in-progress') return s;
          return { attempts: { ...s.attempts, [id]: fn(current) } };
        }),
      completeAttempt: (attempt, report) =>
        set((s) => ({
          practiceLog: addPractice(s.practiceLog, report.timeTakenSec / 60),
          attempts: { ...s.attempts, [attempt.id]: { ...attempt, status: 'submitted', reportId: report.id } },
          reports: { ...s.reports, [report.id]: report },
        })),
      discardAttempt: (id) =>
        set((s) => {
          const rest = { ...s.attempts };
          delete rest[id];
          return { attempts: rest };
        }),
      rateReport: (reportId, rating) =>
        set((s) => {
          const report = s.reports[reportId];
          return report ? { reports: { ...s.reports, [reportId]: { ...report, rating } } } : s;
        }),
    }),
    { name: STORAGE_KEYS.attempts, storage: demoStorage },
  ),
);

export const selectHistory = (reports: Record<string, ExamReport>): AttemptSummary[] =>
  Object.values(reports)
    .map(toAttemptSummary)
    .sort((a, b) => b.submittedAt.localeCompare(a.submittedAt));

export const selectInProgress = (attempts: Record<string, Attempt>): Attempt[] =>
  Object.values(attempts)
    .filter((a) => a.status === 'in-progress')
    .sort((a, b) => b.startedAt.localeCompare(a.startedAt));
