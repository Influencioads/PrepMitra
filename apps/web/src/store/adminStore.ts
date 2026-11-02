import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  AdminGlossaryInput, AdminLessonInput, AdminModule, AdminOrder, AdminQuestion, AdminQuestionInput, AdminRoleInput,
  AdminSettings, AdminSubscription, AdminTeamMember, AdminUserRecord, AdminUserStatus, AiLesson, AuditLogEntry, Exam,
  ExamSection, FeatureFlags, GlossaryTerm, InterviewRole, InterviewerPromptConfig, LanguageCode, LanguageConfig,
  PlanConfig, PlanId, PublishStatus, QuestionStatusAdmin, ReviewItem, Subject, AdminExamInput,
} from '@prepmitra/shared';
import {
  ADMIN_ORDERS, ADMIN_SUBSCRIPTIONS, ADMIN_TEAM, ADMIN_USERS, DEFAULT_ADMIN_SETTINGS, DEFAULT_INTERVIEWER_CONFIG, EXAMS,
  INTERVIEW_ROLES, PLANS, SEED_AUDIT_LOG, SEED_GLOSSARY, SEED_LANGUAGE_CONFIGS, SEED_LESSONS, SEED_REVIEW_QUEUE,
  STORAGE_KEYS, TIER1_LANGUAGES, buildAdminQuestions, createId, getPlan,
} from '@prepmitra/shared';
import { demoStorage } from './storage';
import { useAuthStore } from './authStore';

// ---------- Inputs ----------
export interface ExamSectionDraft {
  id?: string;
  name: string;
  subject: Subject;
  questionCount: number;
  marksPerQuestion: number;
  negativeMarks: number;
}

export type ExamDraft = AdminExamInput & { sections: ExamSectionDraft[] };

export interface ReviewFix {
  note?: string;
  explanation?: string;
  /** Option indexes for single/multiple-choice questions. */
  correct?: number[];
  correctNumeric?: string;
  lessonText?: string;
}

export type ReviewOutcome = 'fixed' | 'rejected' | 'quarantined';

export interface TeamMemberInput {
  name: string;
  email: string;
  role: AdminTeamMember['role'];
  languages: LanguageCode[];
}

// ---------- State ----------
export interface AdminData {
  exams: Exam[];
  questions: AdminQuestion[];
  reviewQueue: ReviewItem[];
  roles: InterviewRole[];
  interviewer: InterviewerPromptConfig;
  lessons: AiLesson[];
  glossary: GlossaryTerm[];
  languages: LanguageConfig[];
  users: AdminUserRecord[];
  orders: AdminOrder[];
  subscriptions: AdminSubscription[];
  team: AdminTeamMember[];
  settings: AdminSettings;
  auditLog: AuditLogEntry[];
}

export interface AdminState extends AdminData {
  log: (module: AdminModule, action: string, target: string, details?: string) => void;
  // Exams
  saveExam: (draft: ExamDraft, id?: string) => Exam;
  duplicateExam: (id: string) => Exam | undefined;
  deleteExam: (id: string) => void;
  setExamStatus: (id: string, status: PublishStatus) => void;
  // Questions
  saveQuestion: (input: AdminQuestionInput, id?: string) => AdminQuestion;
  setQuestionStatus: (id: string, status: QuestionStatusAdmin, reason?: string) => void;
  deleteQuestion: (id: string) => void;
  // Review queue
  resolveReview: (id: string, outcome: ReviewOutcome, fix?: ReviewFix) => AiLesson | undefined;
  // Roles & interviewer
  saveRole: (input: AdminRoleInput, id?: string) => InterviewRole;
  deleteRole: (id: string) => void;
  setRoleStatus: (id: string, status: PublishStatus) => void;
  saveInterviewer: (config: Omit<InterviewerPromptConfig, 'updatedAt'>, section: 'prompt' | 'rubric') => void;
  // Lessons & glossary
  saveLesson: (input: AdminLessonInput, id?: string) => AiLesson;
  deleteLesson: (id: string) => void;
  setLessonActive: (id: string, active: boolean) => void;
  saveGlossary: (input: AdminGlossaryInput, id?: string) => GlossaryTerm;
  deleteGlossary: (id: string) => void;
  // Languages
  updateLanguage: (code: LanguageCode, patch: Partial<Omit<LanguageConfig, 'code' | 'tier'>>) => void;
  // Users
  adjustCredits: (userId: string, delta: number, reason: string) => void;
  setUserStatus: (userId: string, status: AdminUserStatus, reason?: string) => void;
  // Payments
  refundOrder: (orderId: string, reason: string) => void;
  // Settings
  updatePlan: (id: PlanId, patch: Partial<Omit<PlanConfig, 'id'>>) => void;
  updateFlags: (patch: Partial<FeatureFlags>) => void;
  setSimulateLoadError: (on: boolean) => void;
  saveMember: (input: TeamMemberInput, id?: string) => AdminTeamMember;
  setMemberActive: (id: string, active: boolean) => void;
  removeMember: (id: string) => void;
  resetDemoData: () => void;
}

export function createAdminSeed(): AdminData {
  return {
    exams: structuredClone(EXAMS),
    questions: buildAdminQuestions(),
    reviewQueue: structuredClone(SEED_REVIEW_QUEUE),
    roles: structuredClone(INTERVIEW_ROLES),
    interviewer: structuredClone(DEFAULT_INTERVIEWER_CONFIG),
    lessons: structuredClone(SEED_LESSONS),
    glossary: structuredClone(SEED_GLOSSARY),
    languages: structuredClone(SEED_LANGUAGE_CONFIGS),
    users: structuredClone(ADMIN_USERS),
    orders: structuredClone(ADMIN_ORDERS),
    subscriptions: structuredClone(ADMIN_SUBSCRIPTIONS),
    team: structuredClone(ADMIN_TEAM),
    settings: structuredClone(DEFAULT_ADMIN_SETTINGS),
    auditLog: structuredClone(SEED_AUDIT_LOG),
  };
}

const now = () => new Date().toISOString();
const actorName = () => useAuthStore.getState().session?.user.name ?? 'Admin';
const slugify = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'item';

function uniqueId(base: string, taken: string[]): string {
  let id = slugify(base);
  let n = 2;
  while (taken.includes(id)) id = `${slugify(base)}-${n++}`;
  return id;
}

const AUDIT_LIMIT = 300;

export const useAdminStore = create<AdminState>()(
  persist(
    (set, get) => {
      const log: AdminState['log'] = (module, action, target, details) =>
        set((s) => ({
          auditLog: [{ id: createId('al'), actor: actorName(), module, action, target, details, at: now() }, ...s.auditLog].slice(0, AUDIT_LIMIT),
        }));

      return {
        ...createAdminSeed(),
        log,

        // ---------- Exams ----------
        saveExam: (draft, id) => {
          const { sections: sectionDrafts, ...input } = draft;
          const existing = id ? get().exams.find((e) => e.id === id) : undefined;
          const examId = existing?.id ?? uniqueId(input.shortTitle, get().exams.map((e) => e.id));
          const sections: ExamSection[] = sectionDrafts.map((s, i) => ({
            ...existing?.sections.find((x) => x.id === s.id),
            id: s.id || `${examId}-s${i + 1}-${createId('x').slice(-4)}`,
            name: s.name.trim(),
            subject: s.subject,
            questionCount: s.questionCount,
            marksPerQuestion: s.marksPerQuestion,
            negativeMarks: s.negativeMarks,
          }));
          const base: Exam = existing ?? {
            id: examId,
            title: '',
            shortTitle: '',
            category: 'government',
            description: '',
            conductingBody: '',
            durationMin: 60,
            totalQuestions: 0,
            totalMarks: 0,
            difficulty: 'Moderate',
            languages: ['en'],
            creditCost: 1,
            isFree: false,
            sections: [],
            negativeMarking: '',
            calculatorAllowed: false,
            questionTypes: ['single'],
            popularity: 50,
            rating: 0,
            attemptsCount: 0,
            highlights: ['Never-repeat AI papers', 'Section-wise analysis'],
            sampleQuestion: { text: 'Sample question will be generated after the first verified batch.', options: ['A', 'B', 'C', 'D'], answerIndex: 0 },
            status: 'draft',
            demo: { questionsPerSection: 4, durationMin: 16 },
            updatedAt: now(),
          };
          const exam: Exam = {
            ...base,
            ...input,
            languages: input.languages as LanguageCode[],
            sections,
            isFree: input.creditCost === 0,
            demo: {
              questionsPerSection: Math.min(5, Math.max(2, Math.min(...sections.map((s) => s.questionCount)))),
              durationMin: Math.min(input.durationMin, Math.max(10, sections.length * 5)),
            },
            updatedAt: now(),
          };
          set((s) => ({ exams: existing ? s.exams.map((e) => (e.id === exam.id ? exam : e)) : [exam, ...s.exams] }));
          log('exams', existing ? 'Updated exam' : 'Created exam', exam.title, `${sections.length} sections · ${exam.status}`);
          return exam;
        },
        duplicateExam: (id) => {
          const src = get().exams.find((e) => e.id === id);
          if (!src) return undefined;
          const newId = uniqueId(`${src.id}-copy`, get().exams.map((e) => e.id));
          const copy: Exam = {
            ...structuredClone(src),
            id: newId,
            title: `${src.title} (Copy)`,
            shortTitle: `${src.shortTitle} copy`.slice(0, 20),
            status: 'draft',
            attemptsCount: 0,
            sections: src.sections.map((s, i) => ({ ...s, id: `${newId}-s${i + 1}` })),
            updatedAt: now(),
          };
          set((s) => ({ exams: [copy, ...s.exams] }));
          log('exams', 'Duplicated exam', src.title, `New draft: ${copy.title}`);
          return copy;
        },
        deleteExam: (id) => {
          const exam = get().exams.find((e) => e.id === id);
          set((s) => ({ exams: s.exams.filter((e) => e.id !== id) }));
          log('exams', 'Deleted exam', exam?.title ?? id);
        },
        setExamStatus: (id, status) => {
          const exam = get().exams.find((e) => e.id === id);
          set((s) => ({ exams: s.exams.map((e) => (e.id === id ? { ...e, status, updatedAt: now() } : e)) }));
          log('exams', status === 'published' ? 'Published exam' : status === 'hidden' ? 'Hid exam' : 'Moved exam to draft', exam?.title ?? id);
        },

        // ---------- Questions ----------
        saveQuestion: (input, id) => {
          const existing = id ? get().questions.find((q) => q.id === id) : undefined;
          const qid = existing?.id ?? `q-${input.subject}-${createId('n').slice(-6)}`;
          const isNumeric = input.type === 'numeric';
          const filled = input.options.map((o) => o.trim());
          const options = isNumeric ? undefined : filled.map((text, i) => ({ id: `${qid}-${String.fromCharCode(97 + i)}`, text })).filter((o) => o.text);
          const correctOptionIds = isNumeric ? undefined : input.correct.filter((i) => filled[i]).map((i) => `${qid}-${String.fromCharCode(97 + i)}`);
          const q: AdminQuestion = {
            ...(existing ?? {
              id: qid,
              expectedTimeSec: 45,
              status: 'pending-review' as const,
              accuracy: 0,
              attemptCount: 0,
              reportCount: 0,
              source: 'manual' as const,
            }),
            subject: input.subject as Subject,
            topic: input.topic.trim(),
            type: input.type,
            difficulty: input.difficulty,
            text: input.text.trim(),
            options,
            correctOptionIds,
            correctNumeric: isNumeric ? Number(input.correctNumeric) : undefined,
            tolerance: isNumeric ? (existing?.tolerance ?? 0) : undefined,
            explanation: input.explanation.trim(),
            shortcut: input.shortcut?.trim() || undefined,
            updatedAt: now(),
          } as AdminQuestion;
          set((s) => ({ questions: existing ? s.questions.map((x) => (x.id === qid ? q : x)) : [q, ...s.questions] }));
          log('questions', existing ? 'Updated question' : 'Created question', qid, `${q.topic} · ${q.type}`);
          return q;
        },
        setQuestionStatus: (id, status, reason) => {
          set((s) => ({ questions: s.questions.map((q) => (q.id === id ? { ...q, status, updatedAt: now() } : q)) }));
          const label = { verified: 'Approved question', quarantined: 'Quarantined question', rejected: 'Rejected question', 'pending-review': 'Sent question to review' }[status];
          log('questions', label, id, reason);
        },
        deleteQuestion: (id) => {
          set((s) => ({ questions: s.questions.filter((q) => q.id !== id), reviewQueue: s.reviewQueue.filter((r) => r.questionId !== id) }));
          log('questions', 'Deleted question', id);
        },

        // ---------- Review queue ----------
        resolveReview: (id, outcome, fix) => {
          const item = get().reviewQueue.find((r) => r.id === id);
          if (!item) return undefined;
          const q = get().questions.find((x) => x.id === item.questionId);
          let lesson: AiLesson | undefined;
          set((s) => ({
            reviewQueue: s.reviewQueue.map((r) =>
              r.id === id ? { ...r, status: outcome, resolvedAt: now(), resolvedBy: actorName(), resolutionNote: fix?.note } : r,
            ),
          }));
          if (outcome === 'fixed' && q) {
            const patch: Partial<AdminQuestion> = { status: 'verified', reportCount: 0, updatedAt: now() };
            if (fix?.explanation) patch.explanation = fix.explanation.trim();
            if (q.type === 'numeric' && fix?.correctNumeric) patch.correctNumeric = Number(fix.correctNumeric);
            if (q.type !== 'numeric' && fix?.correct?.length && q.options)
              patch.correctOptionIds = fix.correct.map((i) => q.options![i]?.id).filter((x): x is string => !!x);
            set((s) => ({ questions: s.questions.map((x) => (x.id === q.id ? { ...x, ...patch } : x)) }));
            const text = (fix?.lessonText?.trim() || `For ${q.topic} questions: ${fix?.note?.trim() || 'double-check the answer key and explanation against a worked solution before publishing.'}`).slice(0, 400);
            lesson = { id: createId('ls'), topic: q.topic, language: item.language, lessonText: text, source: 'review-fix', sourceQuestionId: q.id, active: true, createdAt: now(), updatedAt: now() };
            set((s) => ({ lessons: [lesson!, ...s.lessons] }));
            log('review', 'Confirmed fix', q.id, fix?.note);
            log('lessons', 'Created AI lesson', q.topic, `From review of ${q.id}`);
          } else if (outcome === 'quarantined') {
            set((s) => ({ questions: s.questions.map((x) => (x.id === item.questionId ? { ...x, status: 'quarantined', updatedAt: now() } : x)) }));
            log('review', 'Quarantined question', item.questionId, fix?.note);
          } else {
            if (q && q.status === 'pending-review') {
              set((s) => ({ questions: s.questions.map((x) => (x.id === q.id ? { ...x, status: 'verified', updatedAt: now() } : x)) }));
            }
            log('review', item.source === 'random-sample' ? 'Passed sample review' : 'Rejected flag', item.questionId, fix?.note);
          }
          return lesson;
        },

        // ---------- Roles ----------
        saveRole: (input, id) => {
          const existing = id ? get().roles.find((r) => r.id === id) : undefined;
          const themes = input.themes.split(',').map((t) => t.trim()).filter(Boolean);
          const role: InterviewRole = {
            ...(existing ?? {
              id: uniqueId(input.shortTitle, get().roles.map((r) => r.id)),
              icon: 'briefcase' as const,
              evaluates: themes.slice(0, 4),
              languages: [...TIER1_LANGUAGES],
              creditCost: 1,
              popularity: 50,
            }),
            title: input.title.trim(),
            shortTitle: input.shortTitle.trim(),
            category: input.category.trim(),
            description: input.description.trim(),
            levels: input.levels,
            durationMin: input.durationMin,
            questionCount: input.questionCount,
            themes,
            voiceAvailable: input.voiceAvailable,
            status: input.status,
          };
          set((s) => ({ roles: existing ? s.roles.map((r) => (r.id === role.id ? role : r)) : [role, ...s.roles] }));
          log('roles', existing ? 'Updated interview role' : 'Created interview role', role.title);
          return role;
        },
        deleteRole: (id) => {
          const role = get().roles.find((r) => r.id === id);
          set((s) => ({ roles: s.roles.filter((r) => r.id !== id) }));
          log('roles', 'Deleted interview role', role?.title ?? id);
        },
        setRoleStatus: (id, status) => {
          const role = get().roles.find((r) => r.id === id);
          set((s) => ({ roles: s.roles.map((r) => (r.id === id ? { ...r, status } : r)) }));
          log('roles', status === 'published' ? 'Published interview role' : 'Unpublished interview role', role?.title ?? id);
        },
        saveInterviewer: (config, section) => {
          set({ interviewer: { ...config, updatedAt: now() } });
          log('roles', section === 'prompt' ? 'Updated interviewer prompt' : 'Updated scoring rubric', 'Interviewer config',
            section === 'rubric' ? config.rubric.map((c) => `${c.name} ${c.weight}%`).join(', ') : `Tone: ${config.tone}`);
        },

        // ---------- Lessons & glossary ----------
        saveLesson: (input, id) => {
          const existing = id ? get().lessons.find((l) => l.id === id) : undefined;
          const lesson: AiLesson = {
            ...(existing ?? { id: createId('ls'), source: 'manual' as const, createdAt: now() }),
            topic: input.topic.trim(),
            language: input.language as LanguageCode,
            lessonText: input.lessonText.trim(),
            active: input.active,
            updatedAt: now(),
          };
          set((s) => ({ lessons: existing ? s.lessons.map((l) => (l.id === lesson.id ? lesson : l)) : [lesson, ...s.lessons] }));
          log('lessons', existing ? 'Updated AI lesson' : 'Created AI lesson', lesson.topic, lesson.language);
          return lesson;
        },
        deleteLesson: (id) => {
          const l = get().lessons.find((x) => x.id === id);
          set((s) => ({ lessons: s.lessons.filter((x) => x.id !== id) }));
          log('lessons', 'Deleted AI lesson', l?.topic ?? id);
        },
        setLessonActive: (id, active) => {
          const l = get().lessons.find((x) => x.id === id);
          set((s) => ({ lessons: s.lessons.map((x) => (x.id === id ? { ...x, active, updatedAt: now() } : x)) }));
          log('lessons', active ? 'Activated AI lesson' : 'Deactivated AI lesson', l?.topic ?? id);
        },
        saveGlossary: (input, id) => {
          const existing = id ? get().glossary.find((g) => g.id === id) : undefined;
          const term: GlossaryTerm = {
            id: existing?.id ?? createId('gl'),
            term: input.term.trim(),
            language: input.language as LanguageCode,
            approvedTranslation: input.approvedTranslation.trim(),
            updatedAt: now(),
          };
          set((s) => ({ glossary: existing ? s.glossary.map((g) => (g.id === term.id ? term : g)) : [term, ...s.glossary] }));
          log('lessons', existing ? 'Updated glossary term' : 'Added glossary term', `${term.term} (${term.language})`);
          return term;
        },
        deleteGlossary: (id) => {
          const g = get().glossary.find((x) => x.id === id);
          set((s) => ({ glossary: s.glossary.filter((x) => x.id !== id) }));
          log('lessons', 'Deleted glossary term', g ? `${g.term} (${g.language})` : id);
        },

        // ---------- Languages ----------
        updateLanguage: (code, patch) => {
          set((s) => ({ languages: s.languages.map((l) => (l.code === code ? { ...l, ...patch } : l)) }));
          const details = Object.entries(patch).map(([k, v]) => `${k}: ${v ?? 'unassigned'}`).join(', ');
          log('languages', 'Updated language', code, details);
        },

        // ---------- Users ----------
        adjustCredits: (userId, delta, reason) => {
          const user = get().users.find((u) => u.id === userId);
          set((s) => ({
            users: s.users.map((u) =>
              u.id === userId
                ? {
                    ...u,
                    credits: Math.max(0, u.credits + delta),
                    ledger: [{ id: createId('cl'), delta, reason: delta > 0 ? 'bonus' : 'expired', label: `Admin adjustment — ${reason}`, at: now() }, ...u.ledger],
                  }
                : u,
            ),
          }));
          log('users', delta > 0 ? 'Restored credits' : 'Removed credits', user?.name ?? userId, `${delta > 0 ? '+' : ''}${delta} · ${reason}`);
        },
        setUserStatus: (userId, status, reason) => {
          const user = get().users.find((u) => u.id === userId);
          set((s) => ({ users: s.users.map((u) => (u.id === userId ? { ...u, status } : u)) }));
          log('users', status === 'blocked' ? 'Blocked user' : 'Unblocked user', user?.name ?? userId, reason);
        },

        // ---------- Payments ----------
        refundOrder: (orderId, reason) => {
          const order = get().orders.find((o) => o.id === orderId);
          if (!order) return;
          const credits = getPlan(order.planId)?.credits ?? 0;
          set((s) => ({
            orders: s.orders.map((o) => (o.id === orderId ? { ...o, status: 'refunded', refundedAt: now(), refundReason: reason } : o)),
            users: s.users.map((u) =>
              u.id === order.userId
                ? { ...u, credits: Math.max(0, u.credits - credits), ledger: [{ id: createId('cl'), delta: -credits, reason: 'refund', label: `Order ${order.id} refunded — credits revoked`, at: now() }, ...u.ledger] }
                : u,
            ),
          }));
          log('payments', 'Issued refund', `${order.id} · ${order.userName}`, `₹${order.amountInr} · ${reason}`);
        },

        // ---------- Settings ----------
        updatePlan: (id, patch) => {
          set((s) => ({ settings: { ...s.settings, plans: s.settings.plans.map((p) => (p.id === id ? { ...p, ...patch } : p)) } }));
          const name = PLANS.find((p) => p.id === id)?.name ?? id;
          log('settings', 'Updated pricing', name, Object.entries(patch).map(([k, v]) => `${k}: ${v ?? '—'}`).join(', '));
        },
        updateFlags: (patch) => {
          set((s) => ({ settings: { ...s.settings, featureFlags: { ...s.settings.featureFlags, ...patch } } }));
          log('settings', 'Updated feature flags', Object.keys(patch).join(', '), Object.entries(patch).map(([k, v]) => `${k}: ${v}`).join(', '));
        },
        setSimulateLoadError: (on) => set((s) => ({ settings: { ...s.settings, simulateLoadError: on } })),
        saveMember: (input, id) => {
          const existing = id ? get().team.find((m) => m.id === id) : undefined;
          const member: AdminTeamMember = {
            ...(existing ?? { id: createId('tm'), active: true, lastActiveAt: now() }),
            name: input.name.trim(),
            email: input.email.trim().toLowerCase(),
            role: input.role,
            languages: input.languages,
          };
          set((s) => ({ team: existing ? s.team.map((m) => (m.id === member.id ? member : m)) : [...s.team, member] }));
          log('settings', existing ? 'Updated team member' : 'Invited team member', member.name, member.role);
          return member;
        },
        setMemberActive: (id, active) => {
          const m = get().team.find((x) => x.id === id);
          set((s) => ({ team: s.team.map((x) => (x.id === id ? { ...x, active } : x)) }));
          log('settings', active ? 'Reactivated team member' : 'Deactivated team member', m?.name ?? id);
        },
        removeMember: (id) => {
          const m = get().team.find((x) => x.id === id);
          set((s) => ({ team: s.team.filter((x) => x.id !== id) }));
          log('settings', 'Removed team member', m?.name ?? id);
        },
        resetDemoData: () => {
          set(createAdminSeed());
          log('settings', 'Reset demo data', 'Admin console');
        },
      };
    },
    {
      name: STORAGE_KEYS.admin,
      storage: demoStorage,
      version: 1,
      partialize: (s): AdminData => ({
        exams: s.exams, questions: s.questions, reviewQueue: s.reviewQueue, roles: s.roles, interviewer: s.interviewer,
        lessons: s.lessons, glossary: s.glossary, languages: s.languages, users: s.users, orders: s.orders,
        subscriptions: s.subscriptions, team: s.team, settings: s.settings, auditLog: s.auditLog,
      }),
    },
  ),
);

// ---------- Selectors (usable outside React, e.g. examService.setExamCatalogSource) ----------
// Array-returning selectors create new arrays: in components use them with `useShallow` from 'zustand/react/shallow'.
export const getAdminExams = (): Exam[] => useAdminStore.getState().exams;
export const getAdminRoles = (): InterviewRole[] => useAdminStore.getState().roles;
export const selectPublishedExams = (s: AdminData): Exam[] => s.exams.filter((e) => e.status === 'published');
export const selectPublishedRoles = (s: AdminData): InterviewRole[] => s.roles.filter((r) => r.status === 'published');
export const selectOpenReviewCount = (s: AdminData): number => s.reviewQueue.filter((r) => r.status === 'open').length;
