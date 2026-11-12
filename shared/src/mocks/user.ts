import type {
  InterviewReport, InterviewSession,
  AppNotification, Attempt, AttemptSummary, Exam, ExamReport, ProgressData, Recommendation, SubscriptionState,
  TopicMastery, User, UserProfile, UserSettings,
} from '../types/core';
import { EXAMS, getExamById } from './exams';
import { getQuestionById } from './questions';
import { buildDemoPaper } from '../logic/paper';
import { buildExamReport } from '../logic/report';
import { seededRandom } from '../logic/random';
import { buildInterviewReport, endInterview, startInterview, submitAnswer } from '../logic/interview';
import { getRoleById } from './interviews';

const DAY = 86_400_000;
/** Seeded history is generated relative to app start, so "2 days ago" stays true whenever the demo runs. */
export const SEED_NOW = Math.floor(Date.now() / 3_600_000) * 3_600_000;
const daysAgo = (d: number, hour = 10) => new Date(SEED_NOW - d * DAY + (hour - 10) * 3_600_000).toISOString();

export const DEMO_USER: User = {
  id: 'user-demo-1',
  name: 'Ananya Sharma',
  phone: '9876543210',
  email: 'ananya.sharma@example.com',
  dob: '2001-06-14',
  state: 'Maharashtra',
  preferredLanguage: 'en',
  role: 'user',
  createdAt: daysAgo(48),
  onboardingComplete: true,
};

export const DEMO_ADMIN: User = {
  id: 'admin-demo-1',
  name: 'Rahul Verma',
  phone: '9000000001',
  email: 'admin@prepmitra.ai',
  preferredLanguage: 'en',
  role: 'admin',
  createdAt: daysAgo(200),
  onboardingComplete: true,
};

export const DEMO_PROFILE: UserProfile = {
  educationLevel: 'graduate',
  stream: 'B.Com / BBA',
  institution: 'University of Mumbai',
  graduationYear: 2023,
  targetExamIds: ['ibps-po', 'sbi-po', 'ssc-cgl'],
  targetRoleIds: ['bank-po'],
  experienceYears: 1,
  secondaryLanguage: 'hi',
  resume: { fileName: 'Ananya_Sharma_Resume.pdf', sizeKb: 182, mimeType: 'application/pdf', uploadedAt: daysAgo(40) },
};

export const DEFAULT_SETTINGS: UserSettings = {
  notifications: { email: true, push: true, resultReady: true, practiceReminders: true, planExpiry: true, offers: false },
  privacy: { shareWithRecruiters: false, productAnalytics: true, showOnLeaderboard: false },
  examLanguageToggle: true,
  reduceMotion: false,
};

export const EMPTY_PROFILE: UserProfile = { targetExamIds: [], targetRoleIds: [], experienceYears: 0 };

/** Generates a deterministic, submitted demo attempt with a target accuracy. */
export function generateSeedAttempt(exam: Exam, seed: string, skill: number, submittedAt: string): Attempt {
  const rand = seededRandom(seed);
  const paper = buildDemoPaper(exam, seed);
  const states: Attempt['states'] = {};
  for (const item of paper) {
    const q = getQuestionById(item.questionId)!;
    const roll = rand();
    const time = Math.round(q.expectedTimeSec * (0.6 + rand() * 1.4));
    let answer: Attempt['states'][string]['answer'];
    if (roll < skill) {
      answer = q.type === 'numeric' ? { numericValue: String(q.correctNumeric) } : { selectedOptionIds: [...(q.correctOptionIds ?? [])] };
    } else if (roll < skill + (1 - skill) * 0.65) {
      if (q.type === 'numeric') answer = { numericValue: String((q.correctNumeric ?? 0) + 1) };
      else {
        const wrong = q.options!.find((o) => !q.correctOptionIds!.includes(o.id))!;
        answer = { selectedOptionIds: [wrong.id] };
      }
    }
    states[item.questionId] = { visited: true, marked: false, answer, timeSpentSec: time };
  }
  const durationSec = exam.demo.durationMin * 60;
  const used = Object.values(states).reduce((s, st) => s + st.timeSpentSec, 0);
  const startedAt = new Date(new Date(submittedAt).getTime() - Math.min(used, durationSec) * 1000).toISOString();
  return {
    id: `att-${seed}`, examId: exam.id, language: 'en', startedAt, endsAt: new Date(new Date(startedAt).getTime() + durationSec * 1000).toISOString(),
    durationSec, paper, states, currentIndex: 0, status: 'submitted', submittedAt, reportId: `rep-${seed}`, tabSwitches: 0,
  };
}

const SEED_PLAN: Array<{ examId: string; seed: string; skill: number; days: number }> = [
  { examId: 'general-aptitude', seed: 'seed01', skill: 0.55, days: 42 },
  { examId: 'ssc-cgl', seed: 'seed02', skill: 0.5, days: 35 },
  { examId: 'ibps-po', seed: 'seed03', skill: 0.6, days: 28 },
  { examId: 'ssc-cgl', seed: 'seed04', skill: 0.62, days: 21 },
  { examId: 'ibps-clerk', seed: 'seed05', skill: 0.7, days: 14 },
  { examId: 'sbi-po', seed: 'seed06', skill: 0.66, days: 7 },
  { examId: 'ibps-po', seed: 'seed07', skill: 0.75, days: 2 },
];

export function createSeedHistory(): { attempts: Attempt[]; reports: ExamReport[] } {
  const attempts: Attempt[] = [];
  const reports: ExamReport[] = [];
  for (const s of SEED_PLAN) {
    const exam = getExamById(s.examId)!;
    const attempt = generateSeedAttempt(exam, s.seed, s.skill, daysAgo(s.days, 18));
    attempts.push(attempt);
    reports.push(buildExamReport(exam, attempt, { id: attempt.reportId! }));
  }
  return { attempts, reports };
}

export function toAttemptSummary(report: ExamReport): AttemptSummary {
  const exam = getExamById(report.examId);
  return {
    attemptId: report.attemptId,
    reportId: report.id,
    examId: report.examId,
    examTitle: exam?.shortTitle ?? report.examTitle,
    category: exam?.category ?? 'government',
    score: report.result.score,
    maxScore: report.result.maxScore,
    accuracy: report.result.accuracy,
    percentile: report.percentile,
    submittedAt: report.createdAt,
    timeTakenSec: report.timeTakenSec,
  };
}

export const SEED_TOPIC_MASTERY: TopicMastery[] = [
  { topic: 'Percentages', subject: 'quant', mastery: 84, attempts: 18, trend: 6 },
  { topic: 'Profit and Loss', subject: 'quant', mastery: 78, attempts: 15, trend: 4 },
  { topic: 'Time and Work', subject: 'quant', mastery: 52, attempts: 12, trend: -3 },
  { topic: 'Compound Interest', subject: 'quant', mastery: 46, attempts: 10, trend: 8 },
  { topic: 'Number Series', subject: 'reasoning', mastery: 81, attempts: 16, trend: 2 },
  { topic: 'Seating Arrangement', subject: 'reasoning', mastery: 38, attempts: 11, trend: 5 },
  { topic: 'Syllogism', subject: 'reasoning', mastery: 63, attempts: 9, trend: 1 },
  { topic: 'Coding-Decoding', subject: 'reasoning', mastery: 72, attempts: 8, trend: 3 },
  { topic: 'Error Spotting', subject: 'english', mastery: 58, attempts: 14, trend: -2 },
  { topic: 'Reading Comprehension', subject: 'english', mastery: 69, attempts: 12, trend: 4 },
  { topic: 'Synonyms', subject: 'english', mastery: 88, attempts: 10, trend: 1 },
  { topic: 'Economy', subject: 'general-awareness', mastery: 55, attempts: 9, trend: 7 },
];

export function createSeedProgress(reports: ExamReport[]): ProgressData {
  const trend = [...reports]
    .sort((a, b) => a.createdAt.localeCompare(b.createdAt))
    .map((r) => {
      const exam = getExamById(r.examId);
      const d = new Date(r.createdAt);
      return {
        date: r.createdAt,
        label: `${d.getDate()}/${d.getMonth() + 1}`,
        score: r.result.percentage,
        accuracy: r.result.accuracy,
        examId: r.examId,
        category: exam?.category ?? 'government',
      };
    });
  return {
    trend,
    topics: SEED_TOPIC_MASTERY,
    weekly: [
      { day: 'Mon', minutes: 45 }, { day: 'Tue', minutes: 30 }, { day: 'Wed', minutes: 60 }, { day: 'Thu', minutes: 25 },
      { day: 'Fri', minutes: 50 }, { day: 'Sat', minutes: 90 }, { day: 'Sun', minutes: 40 },
    ],
    streakDays: 6,
    totalMinutes: 340,
  };
}

export const SEED_RECOMMENDATIONS: Recommendation[] = [
  { id: 'rec-1', title: 'Seating Arrangement drill', reason: 'Your weakest reasoning topic at 38% mastery.', topic: 'Seating Arrangement', examId: 'ibps-po', minutes: 20 },
  { id: 'rec-2', title: 'SBI PO full mock', reason: 'Your last IBPS PO score improved — test it on a harder paper.', examId: 'sbi-po', minutes: 60 },
  { id: 'rec-3', title: 'Bank PO mock interview', reason: 'Matches your target role. Practise banking awareness answers.', roleId: 'bank-po', minutes: 20 },
  { id: 'rec-4', title: 'Compound Interest revision', reason: 'Accuracy rose 8% last week; one more session will lock it in.', topic: 'Compound Interest', examId: 'ssc-cgl', minutes: 15 },
];

export const SEED_SUBSCRIPTION: SubscriptionState = {
  planId: 'starter_monthly',
  status: 'active',
  credits: 6,
  renewsAt: new Date(SEED_NOW + 12 * DAY).toISOString(),
  autoRenew: true,
  freeMiniMockUsed: true,
  ledger: [
    { id: 'cl-1', delta: 1, reason: 'free-trial', label: 'Free trial mini mock', at: daysAgo(48) },
    { id: 'cl-2', delta: -1, reason: 'free-trial', label: 'General Aptitude mini mock', at: daysAgo(42) },
    { id: 'cl-3', delta: 1, reason: 'purchase', label: 'Single mock with AI report — ₹29', at: daysAgo(36), expiresAt: new Date(SEED_NOW + 54 * DAY).toISOString() },
    { id: 'cl-4', delta: -1, reason: 'exam-attempt', label: 'SSC CGL mock', at: daysAgo(35) },
    { id: 'cl-5', delta: 10, reason: 'purchase', label: 'Starter (Mock Pass) · monthly — ₹149', at: daysAgo(18), expiresAt: new Date(SEED_NOW + 12 * DAY).toISOString() },
    { id: 'cl-6', delta: -1, reason: 'exam-attempt', label: 'IBPS Clerk mock', at: daysAgo(14) },
    { id: 'cl-7', delta: -1, reason: 'interview', label: 'Bank PO mock interview', at: daysAgo(10) },
    { id: 'cl-8', delta: -1, reason: 'exam-attempt', label: 'SBI PO mock', at: daysAgo(7) },
    { id: 'cl-9', delta: 1, reason: 'refund', label: 'Credit restored — report delayed', at: daysAgo(6) },
    { id: 'cl-10', delta: -1, reason: 'exam-attempt', label: 'IBPS PO mock', at: daysAgo(2) },
  ],
};

export const SEED_NOTIFICATIONS: AppNotification[] = [
  { id: 'n-1', type: 'result', title: 'Your IBPS PO report is ready', body: 'See your section-wise score, weak topics with evidence, and your 7-day plan.', createdAt: daysAgo(2, 19), read: false, link: '/reports/rep-seed07' },
  { id: 'n-2', type: 'reminder', title: 'Keep your 6-day streak going', body: 'A 15-minute Compound Interest drill is waiting for you.', createdAt: daysAgo(1, 9), read: false, link: '/progress' },
  { id: 'n-3', type: 'plan', title: 'Monthly plan renews in 12 days', body: 'Your 6 remaining credits expire at renewal. Plan ahead to use them.', createdAt: daysAgo(3, 11), read: false, link: '/subscription' },
  { id: 'n-4', type: 'payment', title: 'Payment receipt — ₹399', body: 'Monthly plan activated with 10 credits. GST invoice available in Subscription.', createdAt: daysAgo(18, 12), read: true, link: '/subscription' },
  { id: 'n-5', type: 'interview', title: 'Interview report ready', body: 'Your Bank PO mock interview feedback is ready. Review the model answers.', createdAt: daysAgo(10, 16), read: true, link: '/interview/report/irep-seed01' },
  { id: 'n-6', type: 'system', title: 'New exam added: CUET-PG', body: 'CUET-PG General Paper mock is now available in 12 languages.', createdAt: daysAgo(20, 10), read: true, link: '/exams/cuet-pg' },
];

export const publishedExams = () => EXAMS.filter((e) => e.status === 'published');

/** Seeded completed interview so dashboards and reports have history on first load. */
export function createSeedInterview(): { session: InterviewSession; report: InterviewReport } {
  const role = getRoleById('bank-po')!;
  const t0 = SEED_NOW - 10 * DAY;
  let session = startInterview(
    { roleId: 'bank-po', level: 'fresher', language: 'en', mode: 'text', resumeFileName: 'Ananya_Sharma_Resume.pdf' },
    { id: 'int-seed01', now: t0 },
  );
  const answers = [
    'I am Ananya, a commerce graduate from Mumbai University. I interned at a cooperative bank where I helped customers open accounts, and I am interested in banking because I want to work on financial inclusion in rural areas.',
    'During my commerce degree I studied accounting and economics, and the internship showed me how banks serve customers and support the economy, so banking felt like the right growth path.',
    'The repo rate is the rate at which the RBI lends to banks. When it increases, loans become costlier so EMI goes up, and it helps control inflation.',
    'RBI also uses CRR, SLR and open market operations.',
    'An NPA is a loan overdue for more than 90 days. A branch can reduce it through better credit appraisal, regular monitoring and recovery follow-ups.',
    'First I would listen calmly and apologise, then check the transaction status, escalate to the pension cell if needed, and update the customer with a clear timeline.',
    'Yes, I am comfortable. A rural posting helps me learn about priority sector lending and serve customers who need banking the most.',
    'What does success look like for a new PO in the first six months?',
  ];
  answers.forEach((a, i) => {
    session = submitAnswer(session, a, { now: t0 + (i + 1) * 120_000, durationSec: 60 });
  });
  session = endInterview(session, t0 + 18 * 60_000);
  const report = buildInterviewReport(session, role, { id: 'irep-seed01', now: t0 + 18 * 60_000 });
  session = { ...session, reportId: report.id };
  return { session, report };
}

/** Minutes practised per day (yyyy-mm-dd), used for streaks and weekly charts. */
export type PracticeLog = Record<string, number>;

export const dayKey = (ms: number) => {
  const d = new Date(ms);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

export function createSeedPracticeLog(now: number = Date.now()): PracticeLog {
  const minutes = [40, 90, 50, 25, 60, 30, 45, 0, 35, 20, 0, 55, 30, 0];
  const log: PracticeLog = {};
  minutes.forEach((m, i) => {
    if (m > 0) log[dayKey(now - (i + 1) * DAY)] = m;
  });
  return log;
}
