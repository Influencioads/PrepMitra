/**
 * Admin API service (Milestone 4). All admin endpoints live under /v1/admin/*
 * and MUST be protected by role-based access control on the backend — the
 * admin route guard in the web app is UI-only.
 *
 * Mock mode (default): every call simulates latency and applies the change to
 * the persisted admin store (`useAdminStore`). Real mode: the request is sent
 * to `/v1/admin/...` first and the store is only updated after it succeeds.
 */
import type {
  AdminGlossaryInput, AdminLessonInput, AdminModule, AdminQuestionInput, AdminRoleInput, AdminUserStatus, FeatureFlags,
  InterviewerPromptConfig, LanguageCode, LanguageConfig, PlanConfig, PlanId, PublishStatus, QuestionStatusAdmin,
} from '@prepmitra/shared';
import { API_ENDPOINTS } from '@prepmitra/shared';
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

/** Launch admin APIs (plan): flags, questions/{id}, users, users/{id}/credits, payments, stats. Others are Phase 2. */
const SLICE_PATHS: Partial<Record<keyof AdminData, string>> = {
  exams: 'exams', questions: 'questions', reviewQueue: 'flags', roles: 'interview-roles', interviewer: 'interviewer-config',
  lessons: 'lessons', glossary: 'glossary', languages: 'languages', users: 'users', orders: 'payments',
  subscriptions: 'subscriptions', team: 'team', settings: 'settings', auditLog: 'audit-log',
};

async function mutate<T>(method: Method, path: string, body: unknown, apply: () => T, ms = 300): Promise<T> {
  if (!USE_MOCK) {
    await http.request({ method, url: API_ENDPOINTS.admin(path), data: body });
    return apply();
  }
  await delay(ms);
  return apply();
}

const store = () => useAdminStore.getState();

export const adminService = {
  /** GET /v1/admin/{slice} for every slice the module needs. Simulates latency (and optional failure) in mock mode. */
  async load(module: AdminModule): Promise<void> {
    if (!USE_MOCK) {
      const slices = MODULE_SLICES[module];
      const results = await Promise.all(
        slices.map(async (k) => [k, (await http.get(API_ENDPOINTS.admin(SLICE_PATHS[k] ?? String(k)))).data] as const),
      );
      useAdminStore.setState(Object.fromEntries(results) as Partial<AdminData>);
      return;
    }
    await delay(550);
    if (store().settings.simulateLoadError) {
      store().setSimulateLoadError(false);
      throw mockError(503, 'ADMIN_UNAVAILABLE', 'The admin API did not respond (simulated). Try again.');
    }
  },

  // ---------- Exams ----------
  saveExam: (draft: ExamDraft, id?: string) =>
    mutate(id ? 'put' : 'post', id ? `exams/${id}` : 'exams', draft, () => store().saveExam(draft, id)),
  duplicateExam: (id: string) => mutate('post', `exams/${id}/duplicate`, null, () => store().duplicateExam(id)),
  deleteExam: (id: string) => mutate('delete', `exams/${id}`, null, () => store().deleteExam(id)),
  setExamStatus: (id: string, status: PublishStatus) =>
    mutate('patch', `exams/${id}`, { status }, () => store().setExamStatus(id, status), 200),

  // ---------- Questions ----------
  saveQuestion: (input: AdminQuestionInput, id?: string) =>
    mutate(id ? 'put' : 'post', id ? `questions/${id}` : 'questions', input, () => store().saveQuestion(input, id)),
  setQuestionStatus: (id: string, status: QuestionStatusAdmin, reason?: string) =>
    mutate('patch', `questions/${id}`, { status, reason }, () => store().setQuestionStatus(id, status, reason), 200),
  deleteQuestion: (id: string) => mutate('delete', `questions/${id}`, null, () => store().deleteQuestion(id)),

  // ---------- Review queue ----------
  resolveReview: (id: string, outcome: ReviewOutcome, fix?: ReviewFix) =>
    mutate('post', `flags/${id}/resolve`, { outcome, ...fix }, () => store().resolveReview(id, outcome, fix)),

  // ---------- Interview roles ----------
  saveRole: (input: AdminRoleInput, id?: string) =>
    mutate(id ? 'put' : 'post', id ? `interview-roles/${id}` : 'interview-roles', input, () => store().saveRole(input, id)),
  deleteRole: (id: string) => mutate('delete', `interview-roles/${id}`, null, () => store().deleteRole(id)),
  setRoleStatus: (id: string, status: PublishStatus) =>
    mutate('patch', `interview-roles/${id}`, { status }, () => store().setRoleStatus(id, status), 200),
  saveInterviewer: (config: Omit<InterviewerPromptConfig, 'updatedAt'>, section: 'prompt' | 'rubric') =>
    mutate('put', 'interviewer-config', config, () => store().saveInterviewer(config, section)),

  // ---------- Lessons & glossary ----------
  saveLesson: (input: AdminLessonInput, id?: string) =>
    mutate(id ? 'put' : 'post', id ? `lessons/${id}` : 'lessons', input, () => store().saveLesson(input, id)),
  deleteLesson: (id: string) => mutate('delete', `lessons/${id}`, null, () => store().deleteLesson(id)),
  setLessonActive: (id: string, active: boolean) =>
    mutate('patch', `lessons/${id}`, { active }, () => store().setLessonActive(id, active), 200),
  saveGlossary: (input: AdminGlossaryInput, id?: string) =>
    mutate(id ? 'put' : 'post', id ? `glossary/${id}` : 'glossary', input, () => store().saveGlossary(input, id)),
  deleteGlossary: (id: string) => mutate('delete', `glossary/${id}`, null, () => store().deleteGlossary(id)),

  // ---------- Languages ----------
  updateLanguage: (code: LanguageCode, patch: Partial<Omit<LanguageConfig, 'code' | 'tier'>>) =>
    mutate('patch', `languages/${code}`, patch, () => store().updateLanguage(code, patch), 200),

  // ---------- Users ----------
  adjustCredits: (userId: string, delta: number, reason: string) =>
    mutate('post', `users/${userId}/credits`, { delta, reason }, () => store().adjustCredits(userId, delta, reason)),
  setUserStatus: (userId: string, status: AdminUserStatus, reason?: string) =>
    mutate('patch', `users/${userId}`, { status, reason }, () => store().setUserStatus(userId, status, reason)),

  // ---------- Payments ----------
  /** Production: refunds are issued through the gateway (Razorpay/Cashfree) by the backend only. */
  refundOrder: (orderId: string, reason: string) =>
    mutate('post', `orders/${orderId}/refund`, { reason }, () => store().refundOrder(orderId, reason), 700),

  // ---------- Settings ----------
  updatePlan: (id: PlanId, patch: Partial<Omit<PlanConfig, 'id'>>) =>
    mutate('patch', `plans/${id}`, patch, () => store().updatePlan(id, patch)),
  updateFlags: (patch: Partial<FeatureFlags>) => mutate('patch', 'feature-flags', patch, () => store().updateFlags(patch)),
  saveMember: (input: TeamMemberInput, id?: string) =>
    mutate(id ? 'put' : 'post', id ? `team/${id}` : 'team', input, () => store().saveMember(input, id)),
  setMemberActive: (id: string, active: boolean) =>
    mutate('patch', `team/${id}`, { active }, () => store().setMemberActive(id, active), 200),
  removeMember: (id: string) => mutate('delete', `team/${id}`, null, () => store().removeMember(id)),
};
