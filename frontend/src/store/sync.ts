import type { Attempt, ExamReport, InterviewReport, InterviewSession } from '@prepmitra/shared';
import {
  API_ENDPOINTS, DEFAULT_SETTINGS, subscriptionSlots, toCredits, toInterviewReport, toInterviewSession, toMe, toNotification,
} from '@prepmitra/shared';
import type { Json } from '@prepmitra/shared';
import { http } from '@/services/http';
import { examIdForUuid, fetchExam, fetchExams, fetchPaper, fetchRoles, mapExamReport } from '@/services/backend';
import { useAuthStore } from './authStore';
import { useExamStore } from './examStore';
import { useInterviewStore } from './interviewStore';
import { useNotificationStore } from './notificationStore';
import { useProfileStore } from './profileStore';
import { useSubscriptionStore } from './subscriptionStore';

/**
 * Real-API mode: loads the signed-in user's data from the backend into the app stores,
 * which the screens read. Runs after sign-in and on every app start.
 */
const MAX_REPORTS = 20;
let running: Promise<void> | null = null;

export function syncFromBackend(): Promise<void> {
  running ??= doSync().finally(() => {
    running = null;
  });
  return running;
}

/** Credits, ledger and free-trial state (after starting an exam or interview, or paying). */
export async function syncCredits(): Promise<void> {
  const uid = useAuthStore.getState().session?.user.id;
  if (!uid) return;
  const [credits, attempts, allowances] = await Promise.all([
    http.get(API_ENDPOINTS.credits),
    http.get(API_ENDPOINTS.attempts, { params: { limit: 50 } }),
    settled(http.get(API_ENDPOINTS.allowances)),
  ]);
  applyCredits(credits.data, attempts.data.items ?? []);
  if (allowances) applyPlans(allowances.data);
}

/**
 * Study plan (or combo) and AI Tutor pack held now, from the plan codes in `GET /v1/me/allowances`;
 * renewal date and auto-renew from the active subscriptions in `GET /v1/me/progress`.
 */
function applyPlans(allowances: Json, progress?: Json) {
  const { planId, tutorPlanId } = subscriptionSlots(allowances.plans ?? []);
  const active: Json[] = (progress?.subscriptions ?? []).filter((x: Json) => x.status === 'active');
  const renewsAt: string | undefined = active.map((x) => x.renews_at).filter(Boolean).sort()[0];
  useSubscriptionStore.setState((s) => ({
    sub: {
      ...s.sub,
      planId,
      tutorPlanId,
      ...(progress ? { renewsAt, autoRenew: active.some((x) => x.auto_renew) } : {}),
      status: planId !== 'free' || tutorPlanId ? 'active' : s.sub.status,
    },
  }));
}

function applyCredits(c: Json, attempts: Json[]) {
  const { credits, ledger } = toCredits(c);
  const usedTrial = attempts.some((a) => a.is_free_trial);
  useSubscriptionStore.setState((s) => ({
    sub: {
      ...s.sub,
      status: credits > 0 || s.sub.planId !== 'free' || s.sub.tutorPlanId ? 'active' : usedTrial ? 'expired' : 'trial',
      credits,
      ledger,
      freeMiniMockUsed: usedTrial,
    },
  }));
}

const settled = <T,>(p: Promise<T>) => p.then((v) => v, () => undefined);

async function doSync() {
  const session = useAuthStore.getState().session;
  if (!session) return;
  const uid = session.user.id;
  await Promise.all([settled(fetchExams()), settled(fetchRoles())]);
  const [me, credits, attemptsRes, progress, notes, allowances] = await Promise.all([
    settled(http.get(API_ENDPOINTS.me)),
    settled(http.get(API_ENDPOINTS.credits)),
    settled(http.get(API_ENDPOINTS.attempts, { params: { limit: 50 } })),
    settled(http.get(API_ENDPOINTS.progress)),
    settled(http.get(API_ENDPOINTS.notifications)),
    settled(http.get(API_ENDPOINTS.allowances)),
  ]);
  if (useAuthStore.getState().session?.user.id !== uid) return; // signed out meanwhile

  if (me) {
    const m = toMe(me.data);
    useAuthStore.getState().updateUser(m.user);
    const local = useProfileStore.getState();
    const keep = local.ownerId === uid;
    useProfileStore.getState().reset(uid, { ...m.profile, resume: m.profile.resume && keep ? local.profile.resume ?? m.profile.resume : m.profile.resume }, {
      ...(keep ? local.settings : DEFAULT_SETTINGS),
      privacy: { ...(keep ? local.settings.privacy : DEFAULT_SETTINGS.privacy), shareWithRecruiters: m.settings.privacy.shareWithRecruiters },
      notifications: { ...(keep ? local.settings.notifications : DEFAULT_SETTINGS.notifications), offers: m.settings.notifications.offers },
    });
  }

  const attemptItems: Json[] = attemptsRes?.data.items ?? [];
  if (credits) {
    if (useSubscriptionStore.getState().ownerId !== uid) useSubscriptionStore.getState().reset(uid, useSubscriptionStore.getState().sub);
    applyCredits(credits.data, attemptItems);
  }
  if (allowances) applyPlans(allowances.data, progress?.data);

  // Exam attempts: unfinished ones (to resume) and reports for the most recent submitted ones.
  const attempts: Attempt[] = [];
  const reports: ExamReport[] = [];
  const examIds = new Set<string>();
  for (const a of attemptItems) {
    const examId = await examIdForUuid(a.exam_id);
    if (examId) examIds.add(examId);
  }
  await Promise.all([...examIds].map((id) => settled(fetchExam(id)))); // sections, for per-question marks
  await Promise.all(
    attemptItems.map(async (a, i) => {
      const examId = (await examIdForUuid(a.exam_id)) ?? a.exam_id;
      if (a.status === 'in_progress') {
        if (a.remaining_seconds > 0) {
          const attempt = await settled(fetchPaper(a.id, a.language));
          if (attempt) attempts.push(attempt);
        }
        return;
      }
      if (i >= MAX_REPORTS) return;
      const res = await settled(http.get(API_ENDPOINTS.attemptReport(a.id)));
      const report = res?.data.status === 'ready' ? mapExamReport(res.data, a.id, examId) : undefined;
      attempts.push({
        id: a.id, examId, language: a.language, startedAt: a.started_at, endsAt: a.submitted_at ?? a.started_at, durationSec: report?.durationSec ?? 0,
        paper: [], states: {}, currentIndex: 0, status: 'submitted', submittedAt: a.submitted_at ?? undefined, reportId: report?.id, tabSwitches: 0,
        isMini: !!a.is_free_trial,
      });
      if (report) reports.push(report);
    }),
  );
  if (attemptsRes) {
    const local = useExamStore.getState();
    const mine = local.ownerId === uid ? local.attempts : {};
    // Keep this device's answers for unfinished attempts (they may not have reached the server yet).
    const merged = attempts.map((a) => mergeLocalAttempt(a, mine[a.id]));
    useExamStore.getState().reset(uid, merged, reports, local.ownerId === uid ? local.practiceLog : {});
  }

  // Interviews: sessions and ready reports from the progress history.
  if (progress) {
    const sessions: InterviewSession[] = [];
    const ireports: InterviewReport[] = [];
    const items = (progress.data.history as Json[]).filter((h) => h.kind === 'interview').slice(0, MAX_REPORTS);
    await Promise.all(
      items.map(async (h) => {
        const s = await settled(http.get(API_ENDPOINTS.interview(h.id)));
        if (!s) return;
        const session = toInterviewSession(s.data);
        sessions.push(session);
        if (!session.reportId) return;
        const r = await settled(http.get(`/v1/reports/${session.reportId}`));
        if (r?.data.status === 'ready') ireports.push(toInterviewReport(r.data, session));
      }),
    );
    useInterviewStore.getState().reset(uid, sessions, ireports);
  }

  if (notes) useNotificationStore.getState().reset(uid, (notes.data.items as Json[]).map(toNotification));
}

/**
 * Server copy + this device's copy of the same unfinished attempt. Per question, the device's state
 * wins when it has anything (answer, mark, visit): changes made offline only exist here until the next
 * autosave. The server stays the source of truth for the paper and the end time.
 */
export function mergeLocalAttempt(server: Attempt, local?: Attempt): Attempt {
  if (!local || server.status !== 'in-progress' || local.status !== 'in-progress' || local.id !== server.id) return server;
  const states = { ...server.states };
  const inPaper = new Set(server.paper.map((p) => p.questionId));
  for (const [qid, l] of Object.entries(local.states)) {
    if (!inPaper.has(qid)) continue;
    if (l.visited || l.marked || l.answer) {
      states[qid] = { ...l, timeSpentSec: Math.max(l.timeSpentSec ?? 0, states[qid]?.timeSpentSec ?? 0) };
    }
  }
  return {
    ...server,
    states,
    currentIndex: local.currentIndex,
    tabSwitches: Math.max(local.tabSwitches, server.tabSwitches),
    copyAttempts: local.copyAttempts,
    fiveMinWarned: local.fiveMinWarned,
  };
}
