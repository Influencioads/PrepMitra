/**
 * Adapters between the PrepMitra FastAPI backend (`backend/`, snake_case JSON) and the
 * frontend types in `types/core.ts`. Pure functions only, shared by the website and the
 * mobile app. Backend shapes: docs/backend/API.md and http://localhost:8000/docs.
 *
 * IDs: the frontend keeps its readable exam/role ids (e.g. `ssc-cgl`); the backend uses
 * slugs (`ssc-cgl-tier1`) and UUIDs. `examIdFromSlug` / `examSlugFromId` translate.
 */
import type {
  Answer, AppNotification, Attempt, CreditLedgerEntry, CreditReason, DayPlan, Difficulty, Exam, ExamCategory, ExamReport,
  InterviewReport, InterviewRole, InterviewScores, InterviewSession, InterviewStage, LanguageCode, Loophole, NotificationType,
  Plan, PlanId, Question, QuestionOutcome, QuestionReviewItem, QuestionStatusAdmin, QuestionState, QuestionType, ScoreResult, SharedReport, ShortcutItem, Subject, User,
  UserProfile, UserSettings, WeaknessItem,
} from '../types/core';
import type { AdminOrder, AdminQuestion, AdminUserRecord, ReviewItem, ReviewReason } from '../types/admin';
import { getExamById } from '../mocks/exams';
import { getRoleById } from '../mocks/interviews';
import { getPlanSet } from '../constants';
import { DEFAULT_SETTINGS } from '../mocks/user';

// The backend payloads are validated server-side; the client reads them loosely.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type Json = any;

// ---------- ids ----------
const EXAM_ALIASES: Record<string, string> = {
  'ssc-cgl': 'ssc-cgl-tier1',
  'ssc-chsl': 'ssc-chsl-tier1',
  'rrb-ntpc': 'rrb-ntpc-cbt1',
  'ibps-po': 'ibps-po-prelims',
  'ibps-clerk': 'ibps-clerk-prelims',
  'sbi-po': 'sbi-po-prelims',
  'upsc-prelims': 'upsc-cse-prelims-gs',
  'general-aptitude': 'mini-mock-general-aptitude',
  'it-placement': 'it-placement-aptitude',
};
const ROLE_ALIASES: Record<string, string> = {
  'software-developer': 'software-developer-fresher',
  'bank-po': 'bank-po-interview',
  'sales-bd': 'sales-business-development',
};
const invert = (m: Record<string, string>) => Object.fromEntries(Object.entries(m).map(([k, v]) => [v, k]));
const EXAM_FROM_SLUG = invert(EXAM_ALIASES);
const ROLE_FROM_SLUG = invert(ROLE_ALIASES);

export const examSlugFromId = (id: string) => EXAM_ALIASES[id] ?? id;
export const examIdFromSlug = (slug: string) => EXAM_FROM_SLUG[slug] ?? slug;
export const roleSlugFromId = (id: string) => ROLE_ALIASES[id] ?? id;
export const roleIdFromSlug = (slug: string) => ROLE_FROM_SLUG[slug] ?? slug;

/** Backend UUIDs for exams/roles, filled as catalog responses arrive (needed to start attempts/interviews). */
export const backendIds = {
  exams: new Map<string, string>(), // frontend id -> uuid
  examByUuid: new Map<string, string>(), // uuid -> frontend id
  roles: new Map<string, string>(),
  roleByUuid: new Map<string, string>(),
};

// ---------- small helpers ----------
const pct = (ratio: number | null | undefined) => (ratio == null ? 0 : Math.round(ratio * 1000) / 10);
const round1 = (n: number) => Math.round(n * 10) / 10;
const stripPhone = (p?: string | null) => (p ?? '').replace(/^\+91/, '');

const CATEGORY: Record<string, ExamCategory> = {
  central_govt: 'government',
  state_psc: 'government',
  banking: 'banking',
  civil_services: 'civil-services',
  higher_education: 'higher-education',
  campus_hiring: 'campus-placement',
};
const category = (key: string, slug: string): ExamCategory => (slug.startsWith('rrb-') ? 'railway' : CATEGORY[key] ?? 'government');

export function subjectFromSection(key = '', name = ''): Subject {
  const s = `${key} ${name}`.toLowerCase();
  // Order matters: "Reasoning & Computer Aptitude" is reasoning, "Data Analysis & Interpretation" is DI.
  if (/data analysis|interpretation|dilr|\bdai\b/.test(s)) return 'data-interpretation';
  if (/reason|logical|intelligence|csat/.test(s)) return 'reasoning';
  if (/quant|math|numerical|aptitude|\bqa\b/.test(s)) return 'quant';
  if (/english|verbal|varc|comprehension/.test(s)) return 'english';
  if (/awareness|\bga\b/.test(s)) return 'general-awareness';
  if (/computer|cse/.test(s)) return 'computer-science';
  if (/electronic|ece/.test(s)) return 'electronics';
  return 'general-studies';
}

const difficulty = (d?: string | null, mix?: Record<string, number>): Difficulty => {
  if (d) return d === 'easy' ? 'Easy' : d === 'hard' ? 'Hard' : 'Moderate';
  if (mix && (mix.hard ?? 0) >= 35) return 'Hard';
  if (mix && (mix.easy ?? 0) >= 45) return 'Easy';
  return 'Moderate';
};

const questionType = (t?: string): QuestionType => (t === 'multi' || t === 'multiple' ? 'multiple' : t === 'numeric' ? 'numeric' : 'single');

// ---------- catalog ----------
export function toExam(e: Json): Exam {
  const id = examIdFromSlug(e.slug);
  backendIds.exams.set(id, e.id);
  backendIds.examByUuid.set(e.id, id);
  const demo = getExamById(id); // presentational extras (rating, highlights…) from the design's catalog, if any
  const p = e.pattern;
  const sections = p
    ? p.sections.map((s: Json) => ({
        id: s.key, name: s.name, subject: subjectFromSection(s.key, s.name), questionCount: s.question_count,
        marksPerQuestion: s.marks_per_question, negativeMarks: s.negative_marks ?? 0, durationMin: s.duration_min ?? undefined,
      }))
    : [];
  const types = new Set<QuestionType>();
  for (const s of p?.sections ?? []) for (const t of Object.keys(s.question_types ?? {})) types.add(questionType(t));
  const sample = e.sample_question;
  const answerIndex = sample?.options?.findIndex((o: Json) => o.key === sample.answer) ?? -1;
  const neg = p?.sections?.find((s: Json) => s.negative_marks)?.negative_marks;
  return {
    id,
    title: e.name,
    shortTitle: demo?.shortTitle ?? e.name,
    category: category(e.category, e.slug),
    description: e.description ?? demo?.description ?? '',
    conductingBody: demo?.conductingBody ?? e.category_label ?? '',
    durationMin: e.duration_min,
    totalQuestions: e.question_count,
    totalMarks: e.total_marks,
    difficulty: difficulty(null, p?.difficulty_mix) ?? demo?.difficulty,
    languages: e.languages as LanguageCode[],
    creditCost: e.is_free_trial ? 0 : e.credits_required,
    isFree: !!e.is_free_trial,
    sections,
    negativeMarking: p ? (p.negative_marking && neg ? `−${neg} per wrong answer` : 'No negative marking') : demo?.negativeMarking ?? '',
    calculatorAllowed: !!p?.calculator_allowed,
    questionTypes: types.size ? [...types] : demo?.questionTypes ?? ['single'],
    popularity: demo?.popularity ?? 50, // ordering hint only, never shown
    // The backend has no ratings or attempt counts yet; never borrow the demo numbers for real exams.
    rating: 0,
    attemptsCount: 0,
    highlights: [],
    sampleQuestion: sample
      ? { text: sample.text, options: sample.options.map((o: Json) => o.text), answerIndex: Math.max(0, answerIndex) }
      : demo?.sampleQuestion ?? { text: '', options: [], answerIndex: 0 },
    status: 'published',
    // The real paper is the full pattern; keep the design's "demo" numbers in sync with it.
    demo: {
      questionsPerSection: sections.length ? Math.round(e.question_count / sections.length) : e.question_count,
      durationMin: e.duration_min,
    },
    updatedAt: new Date().toISOString(),
  };
}

export function toRole(r: Json): InterviewRole {
  const id = roleIdFromSlug(r.slug);
  backendIds.roles.set(id, r.id);
  backendIds.roleByUuid.set(r.id, id);
  const demo = getRoleById(id);
  return {
    id,
    title: r.name,
    shortTitle: demo?.shortTitle ?? r.name.replace(/ interview$/i, ''),
    category: demo?.category ?? 'Jobs',
    icon: demo?.icon ?? 'briefcase',
    description: r.description ?? '',
    levels: (r.levels ?? ['fresher']).filter((l: string) => ['fresher', '1-3', '3-5'].includes(l)),
    durationMin: r.duration_min ?? 20,
    questionCount: r.question_count ?? 10,
    evaluates: r.evaluates ?? [],
    themes: demo?.themes ?? [],
    languages: (r.languages ?? demo?.languages ?? ['en', 'hi']) as LanguageCode[],
    voiceAvailable: (r.modes ?? []).includes('voice'),
    creditCost: r.credits_required ?? 1,
    status: 'published',
    popularity: demo?.popularity ?? 50,
  };
}

// ---------- plans & credits ----------
const PLAN_FROM_CODE: Record<string, PlanId> = { free_trial: 'free', pay_per_exam: 'pay-per-mock', credit_pack_10: 'monthly', monthly: 'monthly', yearly: 'yearly' };
let planCodes: Record<string, string> = { free: 'free_trial', 'pay-per-mock': 'pay_per_exam', monthly: 'credit_pack_10', yearly: 'yearly' };

/** Backend plan code for a frontend plan id (the ₹399 10-credit pack shows as 'monthly' in the launch design). */
export const planCodeFromId = (id: string) => planCodes[id] ?? id;

export function toPlans(body: Json): Plan[] {
  const items: Json[] = body.items ?? body;
  const hasPack = items.some((p) => p.code === 'credit_pack_10');
  const design = getPlanSet(hasPack ? 'launch' : 'full');
  const out: Plan[] = [];
  for (const p of items) {
    if (hasPack && p.code === 'monthly') continue; // launch: the pack takes the 'monthly' slot
    const id = PLAN_FROM_CODE[p.code];
    if (!id) continue;
    planCodes = { ...planCodes, [id]: p.code };
    const d = design.find((x) => x.id === id);
    out.push({
      id,
      // Prices, credits and validity come from the server; names and copy from the design (translated in the UI).
      name: d?.name ?? p.name,
      priceInr: p.price_inr ?? (p.price_paise ?? 0) / 100,
      credits: p.credits,
      validityDays: p.validity_days ?? null,
      isRecurring: !!p.is_recurring,
      description: d?.description ?? '',
      features: d?.features ?? [],
      highlighted: d?.highlighted,
      badge: d?.badge,
      cta: d?.cta ?? 'Buy',
      gstInr: typeof p.gst_paise === 'number' ? p.gst_paise / 100 : undefined,
      baseInr: typeof p.taxable_paise === 'number' ? p.taxable_paise / 100 : undefined,
      purchasable: p.purchasable ?? (p.price_paise ?? p.price_inr) > 0,
    });
  }
  return out;
}

const CREDIT_REASON: Record<string, CreditReason> = {
  purchase: 'purchase', subscription: 'purchase', free_trial: 'free-trial', refund: 'refund', restore: 'refund',
  admin_grant: 'bonus', bonus: 'bonus', exam: 'exam-attempt', interview: 'interview', expired: 'expired',
};
export function toCredits(c: Json): { credits: number; nextExpiry?: string; ledger: CreditLedgerEntry[] } {
  return {
    credits: c.total ?? 0,
    nextExpiry: c.next_expiry ?? undefined,
    ledger: (c.grants ?? []).map((g: Json) => ({
      id: `grant-${g.id}`,
      delta: g.granted,
      reason: CREDIT_REASON[g.reason] ?? 'bonus',
      label: `${g.granted} credit${g.granted === 1 ? '' : 's'} (${String(g.reason).replace(/_/g, ' ')}) · ${g.remaining} left`,
      at: g.granted_at,
      expiresAt: g.expires_at ?? undefined,
    })),
  };
}

// ---------- me ----------
const EDU_FROM: Record<string, UserProfile['educationLevel']> = { '12th_pass': '12th', graduate: 'graduate', postgraduate: 'postgraduate' };
const EDU_TO: Record<string, string> = { '12th': '12th_pass', graduate: 'graduate', postgraduate: 'postgraduate' };

export function toMe(m: Json): { user: User; profile: UserProfile; settings: UserSettings } {
  const user: User = {
    id: m.id,
    name: m.name ?? '',
    phone: stripPhone(m.phone),
    email: m.email ?? undefined,
    dob: m.dob ?? undefined,
    state: m.state ?? undefined,
    preferredLanguage: (m.preferred_language ?? 'en') as LanguageCode,
    role: m.is_admin ? 'admin' : 'user',
    createdAt: m.created_at ?? new Date().toISOString(),
    onboardingComplete: !!m.profile_complete,
  };
  const p = m.profile ?? {};
  const profile: UserProfile = {
    educationLevel: p.education ? EDU_FROM[p.education] : undefined,
    stream: p.stream ?? undefined,
    targetExamIds: (p.target_exam_ids ?? []).map(examIdFromSlug),
    targetRoleIds: (p.target_role_ids ?? []).map(roleIdFromSlug),
    experienceYears: p.experience_years ?? 0,
    resume: p.has_resume ? { fileName: 'Resume on file', sizeKb: 0, mimeType: 'application/pdf', uploadedAt: '' } : undefined,
  };
  const c = m.consents ?? {};
  const settings: UserSettings = {
    ...DEFAULT_SETTINGS,
    notifications: { ...DEFAULT_SETTINGS.notifications, offers: !!c.marketing },
    privacy: { ...DEFAULT_SETTINGS.privacy, shareWithRecruiters: !!c.recruiter_sharing },
  };
  return { user, profile, settings };
}

/** PATCH /v1/me body from the frontend's partial `{ user, profile }` update. */
export function toMePatch(patch: { user?: Partial<User>; profile?: Partial<UserProfile> }): Json {
  const u = patch.user ?? {};
  const p = patch.profile ?? {};
  const body: Json = {};
  if (u.name !== undefined) body.name = u.name;
  if (u.email !== undefined) body.email = u.email || null;
  if (u.dob !== undefined) body.dob = u.dob || null;
  if (u.state !== undefined) body.state = u.state || null;
  if (u.preferredLanguage !== undefined) body.preferred_language = u.preferredLanguage;
  if (p.educationLevel !== undefined) body.education = EDU_TO[p.educationLevel] ?? null;
  if (p.stream !== undefined) body.stream = p.stream || null;
  if (p.targetExamIds !== undefined) body.target_exam_ids = p.targetExamIds.map(examSlugFromId);
  if (p.targetRoleIds !== undefined) body.target_role_ids = p.targetRoleIds.map(roleSlugFromId);
  if (p.experienceYears !== undefined) body.experience_years = p.experienceYears;
  return body;
}

/** Frontend consent names → backend consent keys (others are device-only settings). */
export const CONSENT_KEYS: Record<string, string> = {
  'terms-and-privacy': 'data_processing',
  'data-processing': 'data_processing',
  'recruiter-sharing': 'recruiter_sharing',
  shareWithRecruiters: 'recruiter_sharing',
  offers: 'marketing',
  marketing: 'marketing',
};

// ---------- attempts ----------
export function answerFromBackend(a: Json, type: QuestionType): Answer | undefined {
  // Saved answers come back wrapped: {"value": "B"} | {"value": ["A","C"]} | {"value": 12.5}.
  if (a && typeof a === 'object' && !Array.isArray(a) && 'value' in a) a = a.value;
  if (a === null || a === undefined || a === '') return undefined;
  if (type === 'numeric') return { numericValue: String(a) };
  return { selectedOptionIds: Array.isArray(a) ? a : [String(a)] };
}

export function answerToBackend(a: Answer | undefined, type: QuestionType): string | string[] | number | null {
  if (!a) return null;
  if (type === 'numeric') {
    const n = parseFloat(a.numericValue ?? '');
    return Number.isFinite(n) ? n : null;
  }
  const ids = (a.selectedOptionIds ?? []).filter((x): x is string => typeof x === 'string' && x !== '[object Object]');
  if (!ids.length) return null;
  return type === 'multiple' ? ids : ids[0]!;
}

function paperQuestion(q: Json, attemptLang: string): Question {
  const local = q.content ?? {};
  const en = q.content_en ?? (attemptLang === 'en' ? local : null);
  const base = en ?? local; // English is the base text; the attempt language is a translation
  const translations: Question['translations'] = {};
  if (attemptLang !== 'en' && en) translations[attemptLang as LanguageCode] = { text: local.text, options: (local.options ?? []).map((o: Json) => o.text) };
  return {
    id: q.question_id,
    subject: subjectFromSection(q.section_key),
    topic: q.topic ?? '',
    type: questionType(q.type),
    difficulty: difficulty(q.difficulty),
    text: base.text,
    options: (base.options ?? []).map((o: Json) => ({ id: o.key, text: o.text })),
    explanation: '',
    expectedTimeSec: q.expected_time_sec ?? 60,
    translations,
  };
}

/** GET /v1/attempts/{id}/paper → Attempt + the questions to register in the live catalog. */
export function toAttempt(a: Json): { attempt: Attempt; questions: Question[] } {
  const sections: Record<string, Json> = Object.fromEntries((a.rules?.sections ?? []).map((s: Json) => [s.key, s]));
  const questions: Question[] = [];
  const states: Record<string, QuestionState> = {};
  const paper = (a.questions ?? []).map((q: Json) => {
    const question = paperQuestion(q, a.language);
    questions.push(question);
    const answer = answerFromBackend(q.answer, question.type);
    states[q.question_id] = { visited: !!q.visited || !!answer, marked: !!q.marked_for_review, answer, timeSpentSec: q.time_spent_sec ?? 0 };
    const s = sections[q.section_key] ?? {};
    return { questionId: q.question_id, sectionId: q.section_key, marks: s.marks_per_question ?? 1, negativeMarks: s.negative_marks ?? 0 };
  });
  // Clock: server deadline, corrected for this device's clock offset.
  const offset = a.server_time ? Date.now() - Date.parse(a.server_time) : 0;
  const endsAt = new Date(Date.parse(a.deadline_at) + offset).toISOString();
  const firstOpen = paper.findIndex((p: { questionId: string }) => !states[p.questionId]?.visited);
  return {
    questions,
    attempt: {
      id: a.id,
      examId: examIdFromSlug(a.exam.slug),
      language: a.language,
      startedAt: a.started_at,
      endsAt,
      durationSec: (a.rules?.duration_min ?? 60) * 60,
      paper,
      states,
      currentIndex: Math.max(0, firstOpen === -1 ? 0 : firstOpen),
      status: a.status === 'in_progress' ? 'in-progress' : 'submitted',
      submittedAt: a.submitted_at ?? undefined,
      tabSwitches: 0,
      isMini: !!a.is_free_trial,
    },
  };
}

/** PUT /v1/attempts/{id}/answers body. `rev` must grow with every save (stale saves are ignored). */
export function toAnswersBody(attempt: Attempt, rev: number, lookup: (id: string) => Question | undefined): Json {
  return {
    answers: attempt.paper.map((p) => {
      const s = attempt.states[p.questionId];
      const type = lookup(p.questionId)?.type ?? 'single';
      return {
        question_id: p.questionId,
        answer: answerToBackend(s?.answer, type),
        marked_for_review: !!s?.marked,
        visited: !!s?.visited,
        time_spent_sec: Math.round(s?.timeSpentSec ?? 0),
        client_rev: rev,
      };
    }),
  };
}

// ---------- reports ----------
const OUTCOME: Record<string, QuestionOutcome> = { correct: 'correct', wrong: 'incorrect', partial: 'incorrect', unanswered: 'unanswered' };

const plan = (items: Json[] = []): DayPlan[] =>
  items.map((d, i) => ({ day: d.day ?? i + 1, title: d.focus ?? d.title ?? '', tasks: d.tasks ?? [], minutes: d.minutes ?? 45 }));

export interface ReportContext {
  examId: string;
  examTitle: string;
  durationSec: number;
  isMini?: boolean;
}

/** A ready exam report (GET /v1/attempts/{id}/report or /v1/reports/{id}) → ExamReport. */
export function toExamReport(r: Json, ctx: ReportContext): ExamReport {
  const an = r.analytics ?? {};
  const rep = r.report ?? {};
  const exam = getExamById(ctx.examId);
  const sectionMarks: Record<string, number> = Object.fromEntries((exam?.sections ?? []).map((s) => [s.id, s.marksPerQuestion]));
  // Marks per question from the server's own section totals (max marks ÷ questions) win over the local catalog.
  for (const s of an.sections ?? []) {
    const count = (s.attempted ?? 0) + (s.unanswered ?? 0);
    if (count > 0 && typeof s.max_score === 'number') sectionMarks[s.key] = Math.round((s.max_score / count) * 100) / 100;
  }
  const refToId: Record<number, string> = Object.fromEntries((an.questions ?? []).map((q: Json) => [q.ref, q.question_id]));
  const topicAcc: Record<string, number> = Object.fromEntries((an.topics ?? []).map((t: Json) => [t.name, pct(t.accuracy)]));
  const lost: Record<string, number> = Object.fromEntries((an.error_patterns ?? []).map((e: Json) => [e.type, e.marks_lost ?? 0]));
  const maxScore = an.max_score ?? 0;
  const result: ScoreResult = {
    score: an.score ?? 0,
    maxScore,
    percentage: maxScore ? round1(((an.score ?? 0) / maxScore) * 100) : 0,
    correct: an.correct ?? 0,
    incorrect: an.wrong ?? 0,
    unanswered: an.unanswered ?? 0,
    attempted: an.attempted ?? 0,
    accuracy: pct(an.accuracy),
    negativeMarksLost: an.negative_marks_lost ?? 0,
    marksLostTotal: Math.round((maxScore - (an.score ?? 0)) * 100) / 100,
    sections: (an.sections ?? []).map((s: Json) => ({
      sectionId: s.key, name: s.name, score: s.score, maxScore: s.max_score, correct: s.correct, incorrect: s.wrong,
      unanswered: s.unanswered, accuracy: pct(s.accuracy), timeSpentSec: s.time_sec ?? 0,
      attempted: s.attempted ?? (s.correct ?? 0) + (s.wrong ?? 0),
    })),
    topics: (an.topics ?? []).map((t: Json) => ({
      topic: t.name, subject: subjectFromSection(t.section_key), correct: t.correct, total: t.total, attempted: t.attempted, accuracy: pct(t.accuracy),
    })),
    questions: (an.questions ?? []).map((q: Json) => ({
      questionId: q.question_id, sectionId: q.section_key, outcome: OUTCOME[q.status] ?? 'unanswered', marksAwarded: q.marks ?? 0,
      maxMarks: sectionMarks[q.section_key] ?? 1, timeSpentSec: q.time_sec ?? 0,
      expectedTimeSec: q.expected_time_sec ?? undefined,
    })),
  };
  const weaknesses: WeaknessItem[] = (rep.weaknesses ?? []).map((w: Json) => ({
    topic: w.topic,
    accuracy: topicAcc[w.topic] ?? 0,
    evidenceQuestionIds: (w.questions?.map((q: Json) => q.question_id) ?? (w.question_refs ?? []).map((n: number) => refToId[n])).filter(Boolean),
    note: w.detail ?? '',
  }));
  const loopholes: Loophole[] = (rep.loopholes ?? []).map((l: Json) => {
    const pattern = (an.error_patterns ?? []).find((e: Json) => e.type === l.pattern && (!l.detail || e.description === l.detail))
      ?? (an.error_patterns ?? []).find((e: Json) => e.type === l.pattern);
    const title: string = pattern?.description ?? String(l.pattern).replace(/_/g, ' ');
    return {
      title,
      detail: l.detail && l.detail !== title ? l.detail : '',
      marksImpact: pattern?.marks_lost ?? lost[l.pattern] ?? 0,
      pattern: l.pattern,
      section: l.pattern === 'skipped_section' ? /Skipped the whole (.+) section/.exec(title)?.[1] : undefined,
      evidenceQuestionIds: ((l.question_refs ?? pattern?.question_refs ?? []) as number[]).map((n) => refToId[n]).filter(Boolean),
    };
  });
  const shortcuts: ShortcutItem[] = (rep.shortcuts ?? [])
    .map((s: Json) => ({ questionId: s.question_id ?? refToId[s.question_ref], technique: s.technique ?? '', detail: s.explanation ?? '' }))
    .filter((s: ShortcutItem) => s.questionId && (s.technique || s.detail));
  return {
    id: r.id,
    attemptId: r.attempt_id,
    examId: ctx.examId,
    examTitle: ctx.examTitle,
    createdAt: r.created_at,
    language: r.language,
    isDemo: false,
    result,
    timeTakenSec: an.total_time_sec ?? 0,
    durationSec: ctx.durationSec,
    percentile: an.percentile ?? 0,
    strengths: (rep.strengths ?? []).map((s: Json) => (typeof s === 'string' ? s : `${s.topic}: ${s.detail}`)),
    weaknesses,
    loopholes,
    recommendedNextExamId: rep.next_test?.exam_slug ? examIdFromSlug(rep.next_test.exam_slug) : ctx.examId,
    nextTestReason: rep.next_test?.reason || undefined,
    improvementPlan: plan(rep.study_plan),
    shortcuts,
    summary: rep.summary || undefined,
    encouragement: rep.encouragement || undefined,
    rating: r.user_rating ?? undefined,
    isMini: ctx.isMini,
  };
}

/** GET /v1/shared/reports/{token} → SharedReport. */
export function toSharedReport(d: Json): SharedReport {
  const rep = d.report ?? {};
  const sc = rep.score_summary;
  return {
    kind: d.kind === 'interview' ? 'interview' : 'exam',
    title: d.title ?? '',
    language: d.language ?? 'en',
    createdAt: d.created_at,
    score: sc
      ? {
          score: sc.score ?? 0, maxScore: sc.max_score ?? 0, accuracy: pct(sc.accuracy), attempted: sc.attempted ?? 0, correct: sc.correct ?? 0,
          incorrect: sc.wrong ?? 0, unanswered: sc.unanswered ?? 0, negativeMarksLost: sc.negative_marks_lost ?? 0,
        }
      : undefined,
    summary: rep.summary || undefined,
    strengths: (rep.strengths ?? []).map((s: Json) => (typeof s === 'string' ? s : [s.topic, s.detail].filter(Boolean).join(': '))),
    weaknesses: (rep.weaknesses ?? []).map((w: Json) => ({ topic: w.topic ?? '', detail: w.detail ?? '' })),
    loopholes: (rep.loopholes ?? []).map((l: Json) => ({ title: String(l.pattern ?? '').replace(/_/g, ' '), detail: l.detail ?? '' })),
    plan: plan(rep.study_plan),
    encouragement: rep.encouragement || undefined,
  };
}

/** GET /v1/attempts/{id}/review → review items, plus full questions (answer key, explanation) for the live catalog. */
export function toReview(body: Json): { items: QuestionReviewItem[]; questions: Question[] } {
  const questions: Question[] = [];
  const items = (body.questions ?? []).map((q: Json) => {
    const type = questionType(q.type);
    const question: Question = {
      id: q.question_id,
      subject: subjectFromSection(q.section_key),
      topic: q.topic ?? '',
      type,
      difficulty: difficulty(q.difficulty),
      text: q.text,
      options: (q.options ?? []).map((o: Json) => ({ id: o.key, text: o.text })),
      correctOptionIds: type === 'numeric' ? undefined : Array.isArray(q.correct_answer) ? q.correct_answer : [String(q.correct_answer)],
      correctNumeric: type === 'numeric' ? Number(q.correct_answer) : undefined,
      explanation: q.explanation ?? '',
      shortcut: q.shortcut ?? undefined,
      expectedTimeSec: q.expected_time_sec ?? 60,
    };
    questions.push(question);
    const answer = answerFromBackend(q.your_answer, type);
    return {
      questionId: q.question_id,
      number: q.seq,
      sectionId: q.section_key,
      question,
      answer,
      outcome: (answer ? (q.is_correct ? 'correct' : 'incorrect') : 'unanswered') as QuestionOutcome,
      marksAwarded: q.marks_awarded ?? 0,
      timeSpentSec: q.time_spent_sec ?? 0,
    };
  });
  return { items, questions };
}

// ---------- interviews ----------
const STAGE: Record<string, InterviewStage> = { role_technical: 'technical' };
const stage = (s: string): InterviewStage => STAGE[s] ?? (s as InterviewStage);

export function toInterviewSession(s: Json): InterviewSession {
  const active = s.status === 'active';
  const transcript: Json[] = s.transcript ?? [];
  const lastSeq = transcript.length ? transcript[transcript.length - 1].seq : -1;
  return {
    id: s.id,
    config: { roleId: roleIdFromSlug(s.role.slug), level: s.level, language: s.language, mode: s.mode },
    status: active ? 'in-progress' : 'completed',
    turns: (s.transcript ?? []).map((t: Json) => ({
      id: `${s.id}-${t.seq}`,
      speaker: t.speaker === 'interviewer' ? 'interviewer' : 'candidate',
      text: t.text,
      stage: stage(t.stage),
      // The farewell after the last answer is not a question (see isInterviewFinished).
      questionId: t.speaker === 'interviewer' && (active || t.seq !== lastSeq) ? `turn-${t.seq}` : undefined,
      isFollowUp: !!t.is_followup,
      at: t.at ?? s.created_at,
    })),
    questionQueue: [],
    askedCount: s.question_count ?? 0,
    totalQuestions: s.target_questions ?? undefined,
    followUpsAsked: s.followup_count ?? 0,
    startedAt: s.created_at,
    endedAt: s.ended_at ?? undefined,
    reportId: s.report_id ?? undefined,
  };
}

const SCORE_KEYS: Record<string, keyof InterviewScores> = {
  role_knowledge: 'roleKnowledge', answer_structure: 'answerStructure', communication: 'communication', confidence: 'confidence',
  resume_consistency: 'resumeConsistency',
};

export function toInterviewReport(r: Json, session: InterviewSession): InterviewReport {
  const rep = r.report ?? {};
  const scores: InterviewScores = { roleKnowledge: 0, answerStructure: 0, communication: 0, confidence: 0, resumeConsistency: 0 };
  const labelled: { label: string; score: number; why: string }[] = [];
  for (const s of rep.scores ?? []) {
    const k = SCORE_KEYS[s.criterion];
    if (k) scores[k] = s.score;
    labelled.push({ label: s.label ?? s.criterion, score: s.score, why: s.justification ?? '' });
  }
  const answers: Record<number, string> = {};
  session.turns.forEach((t) => {
    const seq = Number(t.id.split('-').pop());
    if (t.speaker === 'candidate') answers[seq] = t.text;
  });
  const role = getRoleById(session.config.roleId);
  const started = Date.parse(session.startedAt);
  const ended = session.endedAt ? Date.parse(session.endedAt) : Date.parse(r.created_at);
  const vm = r.analytics?.voice_metrics;
  return {
    id: r.id,
    sessionId: session.id,
    roleId: session.config.roleId,
    roleTitle: role?.title ?? session.config.roleId,
    level: session.config.level,
    mode: session.config.mode,
    language: r.language ?? session.config.language,
    createdAt: r.created_at,
    isDemo: false,
    scores,
    overall: rep.overall ?? 0,
    voiceMetrics: vm ? { wordsPerMinute: vm.words_per_minute ?? 0, fillerWords: vm.filler_words ?? 0 } : undefined,
    strengths: labelled.filter((s) => s.score >= 7).map((s) => `${s.label}: ${s.why}`),
    weaknesses: labelled.filter((s) => s.score < 7).map((s) => `${s.label}: ${s.why}`),
    redFlags: (rep.red_flags ?? []).map((f: Json) => (typeof f === 'string' ? f : f.detail ?? f.flag ?? '')),
    questionFeedback: (rep.per_question ?? []).map((q: Json) => ({
      questionId: `turn-${q.turn_ref}`,
      question: q.question ?? '',
      answer: answers[q.turn_ref] ?? '',
      good: q.good ?? '',
      missing: q.missing ?? '',
      modelAnswer: q.model_answer ?? '',
      score: q.score ?? rep.overall ?? 0,
    })),
    plan: plan(rep.study_plan),
    durationSec: Number.isFinite(ended - started) ? Math.max(0, Math.round((ended - started) / 1000)) : 0,
    rating: r.user_rating ?? undefined,
  };
}

// ---------- notifications ----------
function notificationType(kind: string): NotificationType {
  if (kind.includes('interview')) return 'interview';
  if (/report|result/.test(kind)) return 'result';
  if (/payment|order|receipt|invoice/.test(kind)) return 'payment';
  if (/credit|expir|subscription|plan/.test(kind)) return 'plan';
  if (/remind|inactive/.test(kind)) return 'reminder';
  return 'system';
}

export function toNotification(n: Json): AppNotification {
  const type = notificationType(n.kind ?? '');
  const rid = n.data?.report_id;
  return {
    id: String(n.id),
    type,
    title: n.title,
    body: n.body,
    createdAt: n.created_at,
    read: !!n.read_at,
    link: rid ? (type === 'interview' ? `/interview/report/${rid}` : `/reports/${rid}`) : type === 'plan' || type === 'payment' ? '/subscription' : undefined,
  };
}

/** Backend error envelope `{ error: { code, message } }` → `{ code, message }`. */
export function toApiErrorBody(data: Json): { code?: string; message?: string } {
  const e = data?.error ?? data ?? {};
  const message = typeof e.message === 'string' ? e.message : typeof data?.detail === 'string' ? data.detail : undefined;
  return { code: typeof e.code === 'string' ? e.code.toUpperCase() : undefined, message };
}

// ---------- admin (launch screens: users, payments, review queue, question bank) ----------

const Q_STATUS: Record<string, QuestionStatusAdmin> = {
  verified: 'verified', pending_review: 'pending-review', draft: 'pending-review', quarantined: 'quarantined', rejected: 'rejected', removed: 'rejected',
};

export function toAdminQuestion(q: Json): AdminQuestion {
  const type = questionType(q.type);
  return {
    id: q.id,
    subject: 'quant',
    topic: q.topic ?? q.subtopic ?? '',
    subtopic: q.subtopic ?? undefined,
    type,
    difficulty: difficulty(q.difficulty),
    text: q.text,
    options: (q.options ?? []).map((o: Json) => ({ id: o.key, text: o.text })),
    correctOptionIds: type === 'numeric' ? undefined : Array.isArray(q.correct_answer) ? q.correct_answer : q.correct_answer ? [String(q.correct_answer)] : [],
    correctNumeric: type === 'numeric' ? Number(q.correct_answer) : undefined,
    explanation: q.explanation ?? '',
    shortcut: q.shortcut ?? undefined,
    expectedTimeSec: q.expected_time_sec ?? 60,
    translations: Object.fromEntries((q.translations ?? []).map((t: Json) => [t.language, { text: t.text, options: (t.options ?? []).map((o: Json) => o.text) }])),
    status: Q_STATUS[q.status] ?? 'pending-review',
    accuracy: pct(q.accuracy_rate),
    attemptCount: q.times_served ?? 0,
    reportCount: q.report_count ?? 0,
    source: q.source === 'manual' ? 'manual' : 'ai-generated',
    updatedAt: q.updated_at ?? q.created_at,
  };
}

const FLAG_REASON: Record<string, ReviewReason> = { wrong_answer: 'wrong-answer', unclear: 'unclear', bad_translation: 'translation', other: 'typo' };

/** GET /v1/admin/flags (grouped by question) → review items; the item id is the open report ids joined by ','. */
export function toReviewItem(f: Json): ReviewItem {
  const open = (f.flags ?? []).filter((x: Json) => !x.resolution);
  const flags = open.length ? open : f.flags ?? [];
  return {
    id: flags.map((x: Json) => x.id).join(','),
    questionId: f.question.id,
    examId: backendIds.examByUuid.get(f.question.exam_id),
    source: 'user-flag',
    language: (flags[0]?.language ?? 'en') as LanguageCode,
    flags: flags.map((x: Json) => ({
      id: String(x.id), reporter: `User ${String(x.user_id).slice(0, 8)}`, reason: FLAG_REASON[x.reason] ?? 'unclear',
      comment: x.details || undefined, language: (x.language ?? 'en') as LanguageCode, at: x.created_at,
    })),
    status: open.length ? 'open' : 'fixed',
    createdAt: flags[0]?.created_at ?? new Date().toISOString(),
  };
}

export function toAdminUser(u: Json): AdminUserRecord {
  return {
    id: u.id,
    name: u.name ?? '(no name yet)',
    phone: stripPhone(u.phone),
    email: u.email ?? undefined,
    state: u.state ?? '',
    preferredLanguage: (u.preferred_language ?? 'en') as LanguageCode,
    planId: (u.credits ?? 0) > 0 ? 'pay-per-mock' : 'free',
    status: u.status === 'blocked' ? 'blocked' : 'active',
    credits: u.credits ?? 0,
    joinedAt: u.created_at,
    lastActiveAt: u.last_active_at ?? u.created_at,
    attempts: [],
    ledger: [],
  };
}

export function toAdminOrder(o: Json, userName = ''): AdminOrder {
  return {
    id: o.id,
    invoiceNo: o.invoice_no ?? '—',
    userId: o.user_id,
    userName,
    planId: PLAN_FROM_CODE[o.plan_code] ?? 'pay-per-mock',
    amountInr: o.amount_paise / 100,
    gstInr: (o.gst_amount_paise ?? 0) / 100,
    gateway: o.gateway === 'cashfree' ? 'cashfree' : 'razorpay',
    method: 'upi',
    status: o.status === 'paid' ? 'paid' : o.status === 'refunded' ? 'refunded' : o.status === 'failed' ? 'failed' : 'pending',
    createdAt: o.paid_at ?? o.created_at,
    refundedAt: o.refunded_at ?? undefined,
    refundReason: o.refund_reason ?? undefined,
  };
}
