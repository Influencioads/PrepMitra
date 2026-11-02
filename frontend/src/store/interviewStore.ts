import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { InterviewReport, InterviewSession } from '@prepmitra/shared';
import { STORAGE_KEYS } from '@prepmitra/shared';
import { demoStorage } from './storage';

interface InterviewState {
  ownerId: string | null;
  sessions: Record<string, InterviewSession>;
  reports: Record<string, InterviewReport>;
  reset: (ownerId: string, sessions: InterviewSession[], reports: InterviewReport[]) => void;
  saveSession: (s: InterviewSession) => void;
  saveReport: (s: InterviewSession, r: InterviewReport) => void;
  rateReport: (reportId: string, rating: number) => void;
}

export const useInterviewStore = create<InterviewState>()(
  persist(
    (set) => ({
      ownerId: null,
      sessions: {},
      reports: {},
      reset: (ownerId, sessions, reports) =>
        set({
          ownerId,
          sessions: Object.fromEntries(sessions.map((s) => [s.id, s])),
          reports: Object.fromEntries(reports.map((r) => [r.id, r])),
        }),
      saveSession: (session) => set((st) => ({ sessions: { ...st.sessions, [session.id]: session } })),
      saveReport: (session, report) =>
        set((st) => ({ sessions: { ...st.sessions, [session.id]: session }, reports: { ...st.reports, [report.id]: report } })),
      rateReport: (reportId, rating) =>
        set((st) => (st.reports[reportId] ? { reports: { ...st.reports, [reportId]: { ...st.reports[reportId]!, rating } } } : st)),
    }),
    { name: STORAGE_KEYS.interviews, storage: demoStorage },
  ),
);
