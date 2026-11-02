/**
 * Admin console demo data (Milestone 4). Deterministic: everything is derived
 * from fixed seeds so tables look identical across reloads and devices.
 * Dates are relative to SEED_NOW so "2 days ago" stays true whenever the demo runs.
 */
import type { CreditLedgerEntry, LanguageCode, PaymentMethodLabel, PlanId, QuestionStatusAdmin } from '../types/core';
import type {
  AdminModule, AdminOrder, AdminOrderStatus, AdminQuestion, AdminSettings, AdminSubscription, AdminTeamMember,
  AdminTeamRole, AdminTeamRoleMeta, AdminUserAttempt, AdminUserRecord, AiLesson, AuditLogEntry, FeatureFlags,
  GlossaryTerm, InterviewerPromptConfig, LanguageConfig, PaymentGateway, PermissionLevel, PlatformAnalytics,
  QualityMetrics, ReviewItem, RubricCriterion,
} from '../types/admin';
import { EXAM_CATEGORIES, GST_RATE, LANGUAGES, PLANS } from '../constants';
import { seededRandom } from '../logic/random';
import { EXAMS } from './exams';
import { QUESTION_BANK } from './questions';
import { INTERVIEW_ROLES } from './interviews';
import { SEED_NOW } from './user';

const DAY = 86_400_000;
const HOUR = 3_600_000;
const ago = (days: number, hours = 0) => new Date(SEED_NOW - days * DAY - hours * HOUR).toISOString();
const round2 = (n: number) => Math.round(n * 100) / 100;

/** GST portion of a GST-inclusive amount. */
export const gstFromInclusive = (amountInr: number) => round2(amountInr - amountInr / (1 + GST_RATE));

// ---------- Team & permissions ----------
export const ADMIN_TEAM_ROLES: AdminTeamRoleMeta[] = [
  { id: 'founder', label: 'Founder', description: 'Full access to every module, pricing and team management.' },
  { id: 'content-manager', label: 'Content manager', description: 'Owns exam blueprints, interview roles and publishing.' },
  { id: 'subject-expert', label: 'Subject expert', description: 'Writes, verifies and fixes questions in their subjects.' },
  { id: 'language-reviewer', label: 'Language reviewer', description: 'Reviews translations and maintains the glossary.' },
  { id: 'support', label: 'Support', description: 'Helps learners: user lookup, credit restores, blocks.' },
  { id: 'finance', label: 'Finance', description: 'Orders, refunds, GST invoices and revenue reports.' },
];

export const ADMIN_MODULES: { id: AdminModule; label: string }[] = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'exams', label: 'Exams & blueprints' },
  { id: 'questions', label: 'Question bank' },
  { id: 'review', label: 'Review queue' },
  { id: 'lessons', label: 'AI lessons & glossary' },
  { id: 'languages', label: 'Languages' },
  { id: 'roles', label: 'Interview roles' },
  { id: 'users', label: 'Users' },
  { id: 'payments', label: 'Payments' },
  { id: 'reports', label: 'Reports' },
  { id: 'settings', label: 'Settings' },
];

const perms = (s: string): Record<AdminModule, PermissionLevel> => {
  const map: Record<string, PermissionLevel> = { F: 'full', E: 'edit', V: 'view', '-': 'none' };
  const levels = s.split('').map((c) => map[c] ?? 'none');
  return Object.fromEntries(ADMIN_MODULES.map((m, i) => [m.id, levels[i] ?? 'none'])) as Record<AdminModule, PermissionLevel>;
};

/** Role → module permission matrix. Order: dash, exams, qbank, review, lessons, langs, roles, users, pay, reports, settings. */
export const ADMIN_PERMISSIONS: Record<AdminTeamRole, Record<AdminModule, PermissionLevel>> = {
  founder: perms('FFFFFFFFFFF'),
  'content-manager': perms('VFEEEEF--V-'),
  'subject-expert': perms('V-EFE------'),
  'language-reviewer': perms('V-VEFE-----'),
  support: perms('V------E-V-'),
  finance: perms('V------VFF-'),
};

export const ADMIN_TEAM: AdminTeamMember[] = [
  { id: 'tm-1', name: 'Rahul Verma', email: 'admin@prepmitra.ai', role: 'founder', languages: ['en', 'hi'], active: true, lastActiveAt: ago(0, 1) },
  { id: 'tm-2', name: 'Sneha Iyer', email: 'sneha.iyer@prepmitra.ai', role: 'content-manager', languages: ['en', 'ta'], active: true, lastActiveAt: ago(0, 3) },
  { id: 'tm-3', name: 'Dr. Arvind Kulkarni', email: 'arvind.k@prepmitra.ai', role: 'subject-expert', languages: ['en', 'mr'], active: true, lastActiveAt: ago(1) },
  { id: 'tm-4', name: 'Meera Banerjee', email: 'meera.b@prepmitra.ai', role: 'language-reviewer', languages: ['bn', 'as'], active: true, lastActiveAt: ago(0, 6) },
  { id: 'tm-5', name: 'Karthik Reddy', email: 'karthik.r@prepmitra.ai', role: 'language-reviewer', languages: ['te', 'kn'], active: true, lastActiveAt: ago(2) },
  { id: 'tm-6', name: 'Farhan Qureshi', email: 'farhan.q@prepmitra.ai', role: 'support', languages: ['hi', 'ur'], active: true, lastActiveAt: ago(0, 2) },
  { id: 'tm-7', name: 'Pooja Agarwal', email: 'pooja.a@prepmitra.ai', role: 'finance', languages: ['en', 'hi'], active: false, lastActiveAt: ago(21) },
];

// ---------- Users ----------
type UserSeed = [name: string, state: string, lang: LanguageCode, plan: PlanId];
const USER_SEEDS: UserSeed[] = [
  ['Ananya Sharma', 'Maharashtra', 'en', 'monthly'],
  ['Rohit Kumar', 'Bihar', 'hi', 'pay-per-mock'],
  ['Priya Nair', 'Kerala', 'ml', 'yearly'],
  ['Arjun Singh', 'Uttar Pradesh', 'hi', 'free'],
  ['Kavya Reddy', 'Telangana', 'te', 'monthly'],
  ['Sourav Das', 'West Bengal', 'bn', 'free'],
  ['Divya Patel', 'Gujarat', 'gu', 'pay-per-mock'],
  ['Mohammed Irfan', 'Karnataka', 'ur', 'free'],
  ['Lakshmi Subramanian', 'Tamil Nadu', 'ta', 'yearly'],
  ['Vikram Rathore', 'Rajasthan', 'hi', 'free'],
  ['Sneha Joshi', 'Maharashtra', 'mr', 'monthly'],
  ['Gurpreet Kaur', 'Punjab', 'pa', 'free'],
  ['Aditya Mishra', 'Madhya Pradesh', 'hi', 'pay-per-mock'],
  ['Riya Chatterjee', 'West Bengal', 'bn', 'monthly'],
  ['Karthik Raman', 'Tamil Nadu', 'ta', 'free'],
  ['Neha Gupta', 'Delhi', 'en', 'yearly'],
  ['Suresh Behera', 'Odisha', 'or', 'free'],
  ['Pallavi Hegde', 'Karnataka', 'kn', 'pay-per-mock'],
  ['Amit Yadav', 'Haryana', 'hi', 'free'],
  ['Fatima Sheikh', 'Jammu and Kashmir', 'ur', 'free'],
  ['Rahul Deshmukh', 'Maharashtra', 'mr', 'monthly'],
  ['Bhavna Choudhary', 'Assam', 'as', 'free'],
  ['Nikhil Menon', 'Kerala', 'ml', 'free'],
  ['Tanvi Shah', 'Gujarat', 'gu', 'monthly'],
  ['Deepak Thakur', 'Himachal Pradesh', 'hi', 'free'],
];
const BLOCKED_USERS = new Set([9, 19]);

const PAID_EXAMS = EXAMS.filter((e) => !e.isFree);
const planCredits = (plan: PlanId) => PLANS.find((p) => p.id === plan)?.credits ?? 0;

function buildUser(seed: UserSeed, i: number): AdminUserRecord {
  const [name, state, lang, planId] = seed;
  const rand = seededRandom(`admin-user-${i}`);
  const joinedDays = 6 + Math.floor(rand() * 170);
  const attemptCount = planId === 'free' ? Math.floor(rand() * 2) : 2 + Math.floor(rand() * 7);
  const attempts: AdminUserAttempt[] = [];
  const ledger: CreditLedgerEntry[] = [];
  const at = (d: number) => ago(Math.min(d, joinedDays - 1), Math.floor(rand() * 10));

  const plan = PLANS.find((p) => p.id === planId)!;
  const planLabel = `${plan.name} — ₹${plan.priceInr.toLocaleString('en-IN')}`;
  const purchased = planId === 'free' ? 0 : planCredits(planId);
  if (planId !== 'free') ledger.push({ id: `cl-${i}-p`, delta: purchased, reason: 'purchase', label: planLabel, at: at(joinedDays - 2) });
  if (planId !== 'free' || attemptCount > 0)
    ledger.push({ id: `cl-${i}-f`, delta: 0, reason: 'free-trial', label: 'Free mini mock (General Aptitude)', at: at(joinedDays - 1) });
  if (planId === 'free' && attemptCount > 0)
    attempts.push({ id: `ua-${i}-free`, kind: 'exam', title: 'General Aptitude (free mini mock)', score: 40 + Math.floor(rand() * 45), at: at(joinedDays - 1) });

  const paidAttempts = planId === 'free' ? 0 : attemptCount;
  let balance = purchased;
  for (let a = 0; a < paidAttempts; a++) {
    const isInterview = rand() < 0.25;
    const d = Math.floor((joinedDays - 3) * (1 - (a + 1) / (paidAttempts + 1)));
    const when = at(d);
    const role = isInterview ? INTERVIEW_ROLES[Math.floor(rand() * INTERVIEW_ROLES.length)]! : undefined;
    const exam = isInterview ? undefined : PAID_EXAMS[Math.floor(rand() * PAID_EXAMS.length)]!;
    const cost = Math.max(role?.creditCost ?? exam!.creditCost, 1);
    // Pay-per-mock learners top up just before an attempt when they run out.
    while (balance < cost) {
      ledger.push({ id: `cl-${i}-t${a}-${balance}`, delta: plan.credits, reason: 'purchase', label: planLabel, at: new Date(Date.parse(when) - HOUR).toISOString() });
      balance += plan.credits;
    }
    balance -= cost;
    if (role) {
      attempts.push({ id: `ua-${i}-${a}`, kind: 'interview', title: `${role.shortTitle} interview`, score: 45 + Math.floor(rand() * 45), at: when });
      ledger.push({ id: `cl-${i}-${a}`, delta: -cost, reason: 'interview', label: `${role.shortTitle} mock interview`, at: when });
    } else {
      attempts.push({ id: `ua-${i}-${a}`, kind: 'exam', title: exam!.shortTitle, score: 30 + Math.floor(rand() * 60), at: when });
      ledger.push({ id: `cl-${i}-${a}`, delta: -cost, reason: 'exam-attempt', label: `${exam!.shortTitle} mock`, at: when });
    }
  }
  const credits = Math.max(0, balance);
  attempts.sort((a, b) => b.at.localeCompare(a.at));
  ledger.sort((a, b) => b.at.localeCompare(a.at));
  const handle = name.toLowerCase().replace(/[^a-z]+/g, '.');
  return {
    id: `u-${1001 + i}`,
    name,
    phone: `${[9, 8, 7, 6][i % 4]}${String(Math.floor(rand() * 1e9)).padStart(9, '0')}`,
    email: i % 3 === 2 ? undefined : `${handle}@example.com`,
    state,
    preferredLanguage: lang,
    planId,
    status: BLOCKED_USERS.has(i) ? 'blocked' : 'active',
    credits,
    joinedAt: ago(joinedDays),
    lastActiveAt: attempts[0]?.at ?? ago(joinedDays - 1),
    attempts,
    ledger,
  };
}

export const ADMIN_USERS: AdminUserRecord[] = USER_SEEDS.map(buildUser);

// ---------- Orders & subscriptions ----------
const GATEWAYS: PaymentGateway[] = ['razorpay', 'cashfree'];
const METHODS: PaymentMethodLabel[] = ['upi', 'upi', 'upi', 'card', 'netbanking', 'wallet'];

function buildOrders(): AdminOrder[] {
  const rand = seededRandom('admin-orders');
  const buyers = ADMIN_USERS.filter((u) => u.planId !== 'free');
  const orders: AdminOrder[] = [];
  for (let i = 0; i < 30; i++) {
    const user = buyers[i % buyers.length]!;
    // First order per buyer is their plan; repeat orders are mostly top-ups.
    const planId: PlanId = i < buyers.length ? user.planId : rand() < 0.7 ? 'pay-per-mock' : user.planId;
    const plan = PLANS.find((p) => p.id === planId)!;
    const roll = rand();
    const status: AdminOrderStatus = i === 3 || i === 17 ? 'failed' : i === 8 || i === 22 ? 'refunded' : i === 1 ? 'pending' : roll < 0.04 ? 'failed' : 'paid';
    const days = Math.floor(2 + (i / 30) * 140 + rand() * 4) - (i === 1 ? 2 : 0);
    const createdAt = ago(days, Math.floor(rand() * 12));
    orders.push({
      id: `order_${(0x5f3a2c + i * 7919).toString(36).toUpperCase()}`,
      invoiceNo: `PM/2026-27/${String(1240 - i).padStart(6, '0')}`,
      userId: user.id,
      userName: user.name,
      planId,
      amountInr: plan.priceInr,
      gstInr: gstFromInclusive(plan.priceInr),
      gateway: GATEWAYS[Math.floor(rand() * 2)]!,
      method: METHODS[Math.floor(rand() * METHODS.length)]!,
      status,
      createdAt,
      refundedAt: status === 'refunded' ? ago(Math.max(0, days - 2)) : undefined,
      refundReason: status === 'refunded' ? (i === 8 ? 'Duplicate payment' : 'Exam paper failed to load — credit not used') : undefined,
    });
  }
  return orders.sort((a, b) => b.createdAt.localeCompare(a.createdAt));
}

export const ADMIN_ORDERS: AdminOrder[] = buildOrders();

export const ADMIN_SUBSCRIPTIONS: AdminSubscription[] = ADMIN_USERS.filter((u) => u.planId === 'monthly' || u.planId === 'yearly').map(
  (u, i) => {
    const plan = PLANS.find((p) => p.id === u.planId)!;
    const startedDays = Math.min(Math.round((SEED_NOW - Date.parse(u.joinedAt)) / DAY) - 2, plan.validityDays! - 3);
    const status: AdminSubscription['status'] = i === 3 ? 'cancelled' : i === 6 ? 'expired' : 'active';
    return {
      id: `sub_${1000 + i}`,
      userId: u.id,
      userName: u.name,
      planId: u.planId,
      status,
      startedAt: ago(Math.max(1, startedDays)),
      renewsAt: new Date(SEED_NOW + (plan.validityDays! - Math.max(1, startedDays)) * DAY).toISOString(),
      autoRenew: plan.isRecurring && status === 'active',
      amountInr: plan.priceInr,
    };
  },
);

// ---------- Question bank metadata ----------
const QUESTION_OVERRIDES: Record<string, { status: QuestionStatusAdmin; reportCount: number }> = {
  'q-gs-4': { status: 'quarantined', reportCount: 4 },
  'q-cs-7': { status: 'quarantined', reportCount: 3 },
  'q-reas-7': { status: 'pending-review', reportCount: 2 },
  'q-eng-6': { status: 'pending-review', reportCount: 1 },
  'q-ece-5': { status: 'pending-review', reportCount: 0 },
  'q-di-3': { status: 'pending-review', reportCount: 0 },
  'q-di-5': { status: 'rejected', reportCount: 2 },
  'q-ga-6': { status: 'pending-review', reportCount: 1 },
};

export function buildAdminQuestions(): AdminQuestion[] {
  return QUESTION_BANK.map((q) => {
    const rand = seededRandom(`qmeta-${q.id}`);
    const base = q.difficulty === 'Easy' ? 72 : q.difficulty === 'Moderate' ? 55 : 38;
    const o = QUESTION_OVERRIDES[q.id];
    return {
      ...q,
      status: o?.status ?? 'verified',
      accuracy: Math.round(base + rand() * 20 - 6),
      attemptCount: 180 + Math.floor(rand() * 3800),
      reportCount: o?.reportCount ?? (rand() < 0.2 ? 1 : 0),
      source: rand() < 0.85 ? 'ai-generated' : 'manual',
      updatedAt: ago(1 + Math.floor(rand() * 40)),
    };
  });
}

// ---------- Review queue ----------
export const SEED_REVIEW_QUEUE: ReviewItem[] = [
  {
    id: 'rv-1', questionId: 'q-gs-4', examId: 'upsc-prelims', source: 'user-flag', language: 'en', status: 'open', createdAt: ago(0, 5),
    flags: [
      { id: 'f-1', reporter: 'Neha Gupta', reason: 'wrong-answer', comment: 'Repo rate figure looks outdated after the latest MPC meeting.', language: 'en', at: ago(0, 5) },
      { id: 'f-2', reporter: 'Aditya Mishra', reason: 'outdated', comment: 'Answer key does not match current RBI data.', language: 'hi', at: ago(0, 9) },
      { id: 'f-3', reporter: 'Riya Chatterjee', reason: 'wrong-answer', language: 'bn', at: ago(1, 2) },
      { id: 'f-4', reporter: 'Sneha Joshi', reason: 'multiple-correct', comment: 'Options B and D both seem defensible.', language: 'mr', at: ago(1, 7) },
    ],
  },
  {
    id: 'rv-2', questionId: 'q-cs-7', examId: 'gate-cse', source: 'user-flag', language: 'en', status: 'open', createdAt: ago(1),
    flags: [
      { id: 'f-5', reporter: 'Karthik Raman', reason: 'wrong-answer', comment: 'This language is context-free, not regular.', language: 'en', at: ago(1) },
      { id: 'f-6', reporter: 'Nikhil Menon', reason: 'wrong-answer', language: 'en', at: ago(1, 4) },
      { id: 'f-7', reporter: 'Pallavi Hegde', reason: 'unclear', comment: 'Question does not define the alphabet.', language: 'kn', at: ago(2) },
    ],
  },
  {
    id: 'rv-3', questionId: 'q-reas-7', examId: 'ibps-po', source: 'user-flag', language: 'hi', status: 'open', createdAt: ago(2),
    flags: [
      { id: 'f-8', reporter: 'Rohit Kumar', reason: 'translation', comment: 'Hindi version says "बाएँ" where English says right.', language: 'hi', at: ago(2) },
      { id: 'f-9', reporter: 'Amit Yadav', reason: 'unclear', language: 'hi', at: ago(3) },
    ],
  },
  {
    id: 'rv-4', questionId: 'q-eng-6', examId: 'cat', source: 'user-flag', language: 'en', status: 'open', createdAt: ago(3),
    flags: [{ id: 'f-10', reporter: 'Tanvi Shah', reason: 'typo', comment: 'Passage has a missing word in line 2.', language: 'en', at: ago(3) }],
  },
  {
    id: 'rv-5', questionId: 'q-ga-6', examId: 'rrb-ntpc', source: 'user-flag', language: 'en', status: 'open', createdAt: ago(4),
    flags: [{ id: 'f-11', reporter: 'Suresh Behera', reason: 'outdated', comment: 'Zone count changed recently.', language: 'or', at: ago(4) }],
  },
  {
    id: 'rv-6', questionId: 'q-quant-1', examId: 'ssc-cgl', source: 'user-flag', language: 'hi', status: 'open', createdAt: ago(5),
    flags: [{ id: 'f-12', reporter: 'Vikram Rathore', reason: 'translation', comment: '"चक्रवृद्धि" should be used consistently in options.', language: 'hi', at: ago(5) }],
  },
  { id: 'rv-7', questionId: 'q-ece-5', examId: 'gate-ece', source: 'random-sample', language: 'en', status: 'open', createdAt: ago(0, 2), flags: [] },
  { id: 'rv-8', questionId: 'q-di-3', examId: 'cat', source: 'random-sample', language: 'en', status: 'open', createdAt: ago(0, 8), flags: [] },
  { id: 'rv-9', questionId: 'q-quant-5', examId: 'ssc-chsl', source: 'random-sample', language: 'ta', status: 'open', createdAt: ago(1, 3), flags: [] },
  { id: 'rv-10', questionId: 'q-reas-3', examId: 'ibps-clerk', source: 'random-sample', language: 'bn', status: 'open', createdAt: ago(2, 5), flags: [] },
  {
    id: 'rv-11', questionId: 'q-quant-3', examId: 'rrb-ntpc', source: 'user-flag', language: 'en', status: 'rejected', createdAt: ago(9),
    resolvedAt: ago(8), resolvedBy: 'Dr. Arvind Kulkarni', resolutionNote: 'Answer verified: 20 m/s × 3.6 = 72 km/h.',
    flags: [{ id: 'f-13', reporter: 'Arjun Singh', reason: 'wrong-answer', language: 'hi', at: ago(9) }],
  },
  {
    id: 'rv-12', questionId: 'q-ga-2', examId: 'ssc-cgl', source: 'random-sample', language: 'en', status: 'fixed', createdAt: ago(12),
    resolvedAt: ago(11), resolvedBy: 'Sneha Iyer', resolutionNote: 'Explanation clarified; lesson added.', flags: [],
  },
];

// ---------- AI lessons & glossary ----------
export const SEED_LESSONS: AiLesson[] = [
  { id: 'ls-1', topic: 'Compound Interest', language: 'en', lessonText: 'Always state whether interest is compounded annually, half-yearly or quarterly; default to annual only when the exam pattern does.', source: 'review-fix', sourceQuestionId: 'q-quant-1', active: true, createdAt: ago(30), updatedAt: ago(30) },
  { id: 'ls-2', topic: 'Economy', language: 'en', lessonText: 'Do not hard-code RBI policy rates; phrase questions around concepts or cite the date of the figure used.', source: 'flag-pattern', active: true, createdAt: ago(18), updatedAt: ago(6) },
  { id: 'ls-3', topic: 'Seating Arrangement', language: 'hi', lessonText: 'हिंदी अनुवाद में दिशा (बाएँ/दाएँ) को मूल प्रश्न से मिलाकर जाँचें; उत्तर बदल सकता है।', source: 'review-fix', sourceQuestionId: 'q-reas-7', active: true, createdAt: ago(10), updatedAt: ago(10) },
  { id: 'ls-4', topic: 'Geography', language: 'en', lessonText: 'Explanations for river questions must name the origin and the state where the river enters the sea.', source: 'review-fix', sourceQuestionId: 'q-ga-2', active: true, createdAt: ago(11), updatedAt: ago(11) },
  { id: 'ls-5', topic: 'Theory of Computation', language: 'en', lessonText: 'Define the alphabet explicitly in every language-class question and check with a pumping-lemma argument before finalising.', source: 'flag-pattern', active: true, createdAt: ago(4), updatedAt: ago(4) },
  { id: 'ls-6', topic: 'Antonyms', language: 'ta', lessonText: 'தமிழ் மொழிபெயர்ப்பில் எதிர்ச்சொல் கேள்விகளை மொழிபெயர்க்க வேண்டாம்; ஆங்கிலச் சொல்லையே வைத்திருக்கவும்.', source: 'manual', active: true, createdAt: ago(25), updatedAt: ago(25) },
  { id: 'ls-7', topic: 'Railways', language: 'en', lessonText: 'Railway zone counts change; include “as of” context or avoid count-based questions.', source: 'manual', active: false, createdAt: ago(40), updatedAt: ago(15) },
  { id: 'ls-8', topic: 'Percentages', language: 'bn', lessonText: 'বাংলা অনুবাদে দশমিক চিহ্ন ও শতাংশ চিহ্ন অপরিবর্তিত রাখুন।', source: 'manual', active: true, createdAt: ago(20), updatedAt: ago(20) },
];

export const SEED_GLOSSARY: GlossaryTerm[] = [
  { id: 'gl-1', term: 'Compound interest', language: 'hi', approvedTranslation: 'चक्रवृद्धि ब्याज', updatedAt: ago(40) },
  { id: 'gl-2', term: 'Simple interest', language: 'hi', approvedTranslation: 'साधारण ब्याज', updatedAt: ago(40) },
  { id: 'gl-3', term: 'Repo rate', language: 'hi', approvedTranslation: 'रेपो दर', updatedAt: ago(22) },
  { id: 'gl-4', term: 'Profit percentage', language: 'hi', approvedTranslation: 'लाभ प्रतिशत', updatedAt: ago(35) },
  { id: 'gl-5', term: 'Compound interest', language: 'ta', approvedTranslation: 'கூட்டு வட்டி', updatedAt: ago(28) },
  { id: 'gl-6', term: 'Average', language: 'ta', approvedTranslation: 'சராசரி', updatedAt: ago(28) },
  { id: 'gl-7', term: 'Ratio', language: 'ta', approvedTranslation: 'விகிதம்', updatedAt: ago(27) },
  { id: 'gl-8', term: 'Compound interest', language: 'bn', approvedTranslation: 'চক্রবৃদ্ধি সুদ', updatedAt: ago(19) },
  { id: 'gl-9', term: 'Blood relation', language: 'bn', approvedTranslation: 'রক্তের সম্পর্ক', updatedAt: ago(19) },
  { id: 'gl-10', term: 'Fundamental rights', language: 'bn', approvedTranslation: 'মৌলিক অধিকার', updatedAt: ago(17) },
  { id: 'gl-11', term: 'Time and work', language: 'te', approvedTranslation: 'కాలం మరియు పని', updatedAt: ago(15) },
  { id: 'gl-12', term: 'Percentage', language: 'mr', approvedTranslation: 'टक्केवारी', updatedAt: ago(14) },
  { id: 'gl-13', term: 'Direction sense', language: 'gu', approvedTranslation: 'દિશા જ્ઞાન', updatedAt: ago(12) },
  { id: 'gl-14', term: 'Inflation', language: 'kn', approvedTranslation: 'ಹಣದುಬ್ಬರ', updatedAt: ago(9) },
];

// ---------- Languages ----------
const COVERAGE: Partial<Record<LanguageCode, number>> = {
  en: 100, hi: 97, bn: 88, mr: 84, te: 82, ta: 86, gu: 74, kn: 71, ml: 69, or: 58, pa: 55, ur: 52,
  as: 34, ne: 28, kok: 18, mai: 22, sa: 12, sd: 9, ks: 7, doi: 11, brx: 6, mni: 8, sat: 5,
};
const REVIEWERS: Partial<Record<LanguageCode, string>> = {
  en: 'Sneha Iyer', hi: 'Farhan Qureshi', bn: 'Meera Banerjee', mr: 'Dr. Arvind Kulkarni', te: 'Karthik Reddy',
  ta: 'Sneha Iyer', kn: 'Karthik Reddy', ur: 'Farhan Qureshi', as: 'Meera Banerjee',
};

export const SEED_LANGUAGE_CONFIGS: LanguageConfig[] = LANGUAGES.map((l) => ({
  code: l.code,
  tier: l.tier,
  enabled: (COVERAGE[l.code] ?? 0) >= 15,
  voiceSupported: l.voiceSupported,
  coverage: COVERAGE[l.code] ?? 0,
  reviewer: REVIEWERS[l.code] ?? null,
}));

// ---------- Interviewer config ----------
export const DEFAULT_RUBRIC: RubricCriterion[] = [
  { id: 'rb-1', name: 'Role knowledge', description: 'Accuracy and depth of domain answers for the selected role.', weight: 30 },
  { id: 'rb-2', name: 'Answer structure', description: 'STAR / point-first structure, relevance and completeness.', weight: 20 },
  { id: 'rb-3', name: 'Communication', description: 'Clarity, vocabulary and pace in the chosen language.', weight: 20 },
  { id: 'rb-4', name: 'Confidence', description: 'Composure under follow-ups; low filler-word usage in voice mode.', weight: 15 },
  { id: 'rb-5', name: 'Resume consistency', description: 'Claims match the uploaded resume and earlier answers.', weight: 15 },
];

export const DEFAULT_INTERVIEWER_CONFIG: InterviewerPromptConfig = {
  persona: 'Priya, a calm senior interviewer with 10 years of hiring experience in Indian companies.',
  systemPrompt:
    'You are conducting a mock job interview for the role of {{role}} at {{level}} level in {{language}}. Ask one question at a time. ' +
    'Start with a short introduction, then cover resume, technical, situational and HR stages. Ask at most {{maxFollowUps}} follow-ups when an answer is vague. ' +
    'Never reveal scores during the interview. Do not ask about religion, caste, marital status or other protected attributes.',
  tone: 'friendly',
  maxFollowUps: 2,
  rubric: DEFAULT_RUBRIC,
  updatedAt: ago(14),
};

// ---------- Settings ----------
export const DEFAULT_FEATURE_FLAGS: FeatureFlags = {
  voiceInterviews: true,
  tabSwitchLogging: true,
  autoQuarantine: true,
  autoQuarantineThreshold: 3,
  reviewSampleRate: 10,
};

export const DEFAULT_ADMIN_SETTINGS: AdminSettings = {
  featureFlags: DEFAULT_FEATURE_FLAGS,
  plans: PLANS.map((p) => ({ id: p.id, priceInr: p.priceInr, credits: p.credits, validityDays: p.validityDays, active: true })),
  simulateLoadError: false,
};

// ---------- Audit log ----------
export const SEED_AUDIT_LOG: AuditLogEntry[] = [
  { id: 'al-1', actor: 'Sneha Iyer', module: 'exams', action: 'Published exam', target: 'SSC CHSL Tier 1 Mock Test', at: ago(0, 4) },
  { id: 'al-2', actor: 'Farhan Qureshi', module: 'users', action: 'Restored credits', target: 'Rohit Kumar', details: '+1 credit · Paper failed to load', at: ago(0, 7) },
  { id: 'al-3', actor: 'System', module: 'questions', action: 'Auto-quarantined question', target: 'q-gs-4', details: '4 independent reports', at: ago(1, 1) },
  { id: 'al-4', actor: 'Dr. Arvind Kulkarni', module: 'review', action: 'Rejected flag', target: 'q-quant-3', details: 'Answer verified', at: ago(8) },
  { id: 'al-5', actor: 'Meera Banerjee', module: 'lessons', action: 'Added glossary term', target: 'Fundamental rights (bn)', at: ago(17) },
  { id: 'al-6', actor: 'Pooja Agarwal', module: 'payments', action: 'Issued refund', target: 'Order refund — Duplicate payment', at: ago(20) },
  { id: 'al-7', actor: 'Sneha Iyer', module: 'review', action: 'Confirmed fix', target: 'q-ga-2', details: 'Lesson created', at: ago(11) },
  { id: 'al-8', actor: 'Rahul Verma', module: 'settings', action: 'Updated feature flags', target: 'Auto-quarantine threshold', details: '3 reports', at: ago(26) },
  { id: 'al-9', actor: 'Sneha Iyer', module: 'roles', action: 'Updated interviewer prompt', target: 'Interviewer config', at: ago(14) },
  { id: 'al-10', actor: 'Karthik Reddy', module: 'languages', action: 'Assigned reviewer', target: 'Kannada', details: 'Karthik Reddy', at: ago(30) },
];

// ---------- Metrics ----------
const examRand = seededRandom('admin-exam-metrics');
export const QUALITY_METRICS: QualityMetrics = {
  avgReportRating: 4.4,
  ratingDistribution: [
    { stars: 5, count: 1284 },
    { stars: 4, count: 862 },
    { stars: 3, count: 241 },
    { stars: 2, count: 74 },
    { stars: 1, count: 39 },
  ],
  flagRate: 1.3,
  flagRateByExam: EXAMS.map((e) => ({ examId: e.id, label: e.shortTitle, rate: round2(0.4 + examRand() * 2.6) })),
  flagRateByLanguage: (['en', 'hi', 'bn', 'mr', 'te', 'ta', 'gu', 'kn', 'ml', 'or', 'pa', 'ur'] as LanguageCode[]).map((language, i) => ({
    language,
    rate: round2(0.6 + i * 0.18 + examRand() * 0.5),
  })),
  verificationFailureRate: 3.8,
  aiCostPerAttemptInr: 14.6,
  aiCostCapInr: 20,
  aiCostTrend: ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8'].map((label, i) => ({ label, value: round2(18.9 - i * 0.6 + examRand() * 0.8) })),
  reportGenSec: 41,
  reportGenTargetSec: 60,
  reportGenTrend: ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8'].map((label, i) => ({ label, value: Math.round(58 - i * 2.4 + examRand() * 4) })),
};

const catRand = seededRandom('admin-platform');
export const PLATFORM_ANALYTICS: PlatformAnalytics = {
  attemptsToday: 1286,
  attemptsByCategory: EXAM_CATEGORIES.map((c) => ({
    category: c.id,
    attempts: EXAMS.filter((e) => e.category === c.id).reduce((s, e) => s + e.attemptsCount, 0),
  })),
  attemptsByExam: [...EXAMS]
    .sort((a, b) => b.attemptsCount - a.attemptsCount)
    .slice(0, 8)
    .map((e) => ({ examId: e.id, label: e.shortTitle, attempts: Math.round(e.attemptsCount / 30 + catRand() * 20) })),
  secondAttemptRate: 38.2,
  secondAttemptTarget: 35,
  conversionRate: 4.3,
  conversionTarget: 5,
  retentionTrend: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'].map((label, i) => ({ label, value: round2(27 + i * 2.1 + catRand() * 1.5) })),
  conversionTrend: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'].map((label, i) => ({ label, value: round2(2.6 + i * 0.34 + catRand() * 0.2) })),
  interviewsByRole: INTERVIEW_ROLES.map((r) => ({ roleId: r.id, label: r.shortTitle, sessions: Math.round(r.popularity * 18 + catRand() * 120) })),
};
