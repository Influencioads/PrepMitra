/**
 * Admin API service (Milestone 4). All admin endpoints live under /v1/admin/*
 * and MUST be protected by role-based access control on the backend — the
 * admin route guard in the web app is UI-only.
 *
 * Mock mode (default): every call simulates latency and applies the change to
 * the persisted admin store (`useAdminStore`). Real mode: the launch screens
 * (users, payments, review queue, question bank) call `/v1/admin/...` first and
 * the store is only updated after it succeeds. The Phase 2 screens (exam editor,
 * roles, lessons, languages, team, settings) stay on demo data on this device.
 */
import type {
  AdminGlossaryInput, AdminLessonInput, AdminModule, AdminQuestionInput, AdminRoleInput, AdminUserStatus, FeatureFlags,
  InterviewerPromptConfig, LanguageCode, LanguageConfig, PlanConfig, PlanId, PublishStatus, QuestionStatusAdmin,
} from '@prepmitra/shared';
import { API_ENDPOINTS, toAdminOrder, toAdminQuestion, toAdminUser, toReviewItem } from '@prepmitra/shared';
import type { Json } from '@prepmitra/shared';
import {
  useAdminStore, type AdminData, type ExamDraft, type ReviewFix, type ReviewOutcome, type TeamMemberInput,
} from '@/store/adminStore';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';

type Method = 'post' | 'put' | 'patch' | 'delete';

/** Which store slices each admin module needs; used by `load` against the real API. */
const MODULE_SLICES: Record<AdminModule, (keyof AdminData)[]> = {
  dashboard: ['users', 'orders', 'reviewQueue', 'auditLog'],
  exams: ['exams'],
  questions: ['questions'],
  review: ['reviewQueue', 'questions'],
  lessons: ['lessons', 'glossary'],
  languages: ['languages', 'team'],
  roles: ['roles', 'interviewer'],
  users: ['users'],
  payments: ['orders', 'subscriptions'],
  reports: [],
  settings: ['team', 'settings', 'auditLog'],
};

const admin = async (path: string, params?: Record<string, unknown>) => (await http.get(API_ENDPOINTS.admin(path), { params })).data;

/** Store slices backed by the real admin API, mapped to the console's types. Other slices keep demo data. */
const LIVE_SLICES: Partial<Record<keyof AdminData, () => Promise<Partial<AdminData>>>> = {
  users: async () => {
    const items: Json[] = (await admin('users', { limit: 200 })).items;
    // The list has no balances; load details (credits) for the most recent users.
    const details = await Promise.all(items.slice(0, 50).map((u) => admin(`users/${u.id}`).catch(() => u)));
    return { users: items.map((u, i) => toAdminUser({ ...u, credits: details[i]?.credits })) };
  },
  orders: async () => {
    const names = new Map(useAdminStore.getState().users.map((u) => [u.id, u.name]));
    return { orders: ((await admin('payments', { limit: 200 })).items as Json[]).map((o) => toAdminOrder(o, names.get(o.user_id) ?? '')) };
  },
  reviewQueue: async () => {
    const items: Json[] = (await admin('flags')).items;
    const flagged = items.map((f) => toAdminQuestion(f.question));
    const others = useAdminStore.getState().questions.filter((q) => !flagged.some((f) => f.id === q.id));
    return { reviewQueue: items.map(toReviewItem), questions: [...flagged, ...others] };
  },
  questions: async () => ({ questions: ((await admin('questions', { limit: 200 })).items as Json[]).map(toAdminQuestion) }),
};

/** `path: null` = a change that stays on this device in real mode (Phase 2 screens have no backend yet). */
async function mutate<T>(method: Method, path: string | null, body: unknown, apply: () => T, ms = 300): Promise<T> {
  if (!USE_MOCK) {
    if (path) await http.request({ method, url: API_ENDPOINTS.admin(path), data: body });
    return apply();
  }
  await delay(ms);
  return apply();
}

const store = () => useAdminStore.getState();

const QUESTION_ACTIONS: Partial<Record<QuestionStatusAdmin, string>> = { verified: 'approve', quarantined: 'quarantine', rejected: 'reject' };

export const adminService = {
  /** GET /v1/admin/{slice} for every slice the module needs. Simulates latency (and optional failure) in mock mode. */
  async load(module: AdminModule): Promise<void> {
    if (!USE_MOCK) {
      const slices = MODULE_SLICES[module].filter((k) => LIVE_SLICES[k]);
      if (slices.includes('orders') && !slices.includes('users')) slices.unshift('users'); // names on receipts
      // Sequential: the review queue merges into questions, and payments read user names.
      for (const k of slices) useAdminStore.setState(await LIVE_SLICES[k]!());
      return;
    }
    await delay(550);
    if (store().settings.simulateLoadError) {
      store().setSimulateLoadError(false);
      throw mockError(503, 'ADMIN_UNAVAILABLE', 'The admin API did not respond (simulated). Try again.');
    }
  },

  // ---------- Exams (Phase 2: local in real mode) ----------
  saveExam: (draft: ExamDraft, id?: string) => mutate(id ? 'put' : 'post', null, draft, () => store().saveExam(draft, id)),
  duplicateExam: (id: string) => mutate('post', null, null, () => store().duplicateExam(id)),
  deleteExam: (id: string) => mutate('delete', null, null, () => store().deleteExam(id)),
  setExamStatus: (id: string, status: PublishStatus) => mutate('patch', null, { status }, () => store().setExamStatus(id, status), 200),

  // ---------- Questions ----------
  saveQuestion: (input: AdminQuestionInput, id?: string) => mutate(id ? 'put' : 'post', null, input, () => store().saveQuestion(input, id)),
  setQuestionStatus: (id: string, status: QuestionStatusAdmin, reason?: string) =>
    mutate('post', QUESTION_ACTIONS[status] ? `questions/${id}/${QUESTION_ACTIONS[status]}` : null, null, () => store().setQuestionStatus(id, status, reason), 200),
  /** Removing hides the question from new papers (it stays in past reports). */
  deleteQuestion: (id: string) => mutate('patch', `questions/${id}`, { action: 'remove' }, () => store().deleteQuestion(id)),

  // ---------- Review queue ----------
  async resolveReview(id: string, outcome: ReviewOutcome, fix?: ReviewFix) {
    if (USE_MOCK) return mutate('post', null, null, () => store().resolveReview(id, outcome, fix));
    // One review item groups every open user report on a question; resolve each report.
    const item = store().reviewQueue.find((r) => r.id === id);
    const question = item && store().questions.find((q) => q.id === item.questionId);
    const patch: Record<string, unknown> = {};
    if (fix?.explanation) patch.explanation = fix.explanation;
    if (fix?.correctNumeric) patch.correct_answer = Number(fix.correctNumeric);
    else if (fix?.correct?.length && question?.options) {
      const keys = fix.correct.map((i) => question.options![i]!.id);
      patch.correct_answer = question.type === 'multiple' ? keys : keys[0];
    }
    for (const reportId of id.split(',').filter(Boolean)) {
      await http.post(API_ENDPOINTS.admin(`question-reports/${reportId}/resolve`), {
        action: outcome === 'rejected' ? 'reject' : 'confirm',
        resolution: fix?.note?.trim() || (outcome === 'rejected' ? 'Report checked: the question is correct.' : 'Report confirmed by reviewer.'),
        fix: outcome === 'fixed' && Object.keys(patch).length ? patch : undefined,
        create_lesson: outcome === 'fixed',
        discard_question: outcome === 'quarantined',
      });
    }
    return store().resolveReview(id, outcome, fix);
  },

  // ---------- Interview roles (Phase 2: local in real mode) ----------
  saveRole: (input: AdminRoleInput, id?: string) => mutate(id ? 'put' : 'post', null, input, () => store().saveRole(input, id)),
  deleteRole: (id: string) => mutate('delete', null, null, () => store().deleteRole(id)),
  setRoleStatus: (id: string, status: PublishStatus) => mutate('patch', null, { status }, () => store().setRoleStatus(id, status), 200),
  saveInterviewer: (config: Omit<InterviewerPromptConfig, 'updatedAt'>, section: 'prompt' | 'rubric') =>
    mutate('put', null, config, () => store().saveInterviewer(config, section)),

  // ---------- Lessons & glossary (Phase 2: local in real mode) ----------
  saveLesson: (input: AdminLessonInput, id?: string) => mutate(id ? 'put' : 'post', null, input, () => store().saveLesson(input, id)),
  deleteLesson: (id: string) => mutate('delete', null, null, () => store().deleteLesson(id)),
  setLessonActive: (id: string, active: boolean) => mutate('patch', null, { active }, () => store().setLessonActive(id, active), 200),
  saveGlossary: (input: AdminGlossaryInput, id?: string) => mutate(id ? 'put' : 'post', null, input, () => store().saveGlossary(input, id)),
  deleteGlossary: (id: string) => mutate('delete', null, null, () => store().deleteGlossary(id)),

  // ---------- Languages (Phase 2: local in real mode) ----------
  updateLanguage: (code: LanguageCode, patch: Partial<Omit<LanguageConfig, 'code' | 'tier'>>) =>
    mutate('patch', null, patch, () => store().updateLanguage(code, patch), 200),

  // ---------- Users ----------
  adjustCredits: (userId: string, delta: number, reason: string) => {
    if (!USE_MOCK && delta < 0) return Promise.reject(mockError(422, 'CREDITS_DEDUCT_UNSUPPORTED', 'The backend can add credits (valid 90 days) but not remove them.'));
    return mutate('post', `users/${userId}/credits`, { credits: delta, note: reason }, () => store().adjustCredits(userId, delta, reason));
  },
  setUserStatus: (userId: string, status: AdminUserStatus, reason?: string) =>
    mutate('post', status === 'blocked' ? `users/${userId}/block` : `users/${userId}/unblock`, status === 'blocked' ? { reason: reason || 'Blocked by admin' } : null,
      () => store().setUserStatus(userId, status, reason)),

  // ---------- Payments ----------
  /** Production: refunds are issued through the gateway (Razorpay/Cashfree) by the backend only. */
  refundOrder: (orderId: string, reason: string) =>
    mutate('post', `orders/${orderId}/refund`, { reason }, () => store().refundOrder(orderId, reason), 700),

  // ---------- Settings (Phase 2: local in real mode) ----------
  updatePlan: (id: PlanId, patch: Partial<Omit<PlanConfig, 'id'>>) => mutate('patch', null, patch, () => store().updatePlan(id, patch)),
  updateFlags: (patch: Partial<FeatureFlags>) => mutate('patch', null, patch, () => store().updateFlags(patch)),
  saveMember: (input: TeamMemberInput, id?: string) => mutate(id ? 'put' : 'post', null, input, () => store().saveMember(input, id)),
  setMemberActive: (id: string, active: boolean) => mutate('patch', null, { active }, () => store().setMemberActive(id, active), 200),
  removeMember: (id: string) => mutate('delete', null, null, () => store().removeMember(id)),
};
