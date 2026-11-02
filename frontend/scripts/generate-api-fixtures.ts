/**
 * Writes one example JSON per backend endpoint (15-day plan, "API Plan" sheet) into
 * frontend/src/mocks/api/. The examples are built from the same shared mock data and
 * logic the demo uses, so the backend developer can see the exact shapes the frontend
 * expects. Contract reference: docs/API_CONTRACT.md.
 *
 * Run from frontend:  npx tsx scripts/generate-api-fixtures.ts
 */
import { mkdirSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  ADMIN_ORDERS,
  ADMIN_USERS,
  DEFAULT_SETTINGS,
  DEMO_PROFILE,
  DEMO_USER,
  INTERVIEW_ROLES,
  PLATFORM_ANALYTICS,
  SEED_REVIEW_QUEUE,
  SEED_SUBSCRIPTION,
  buildExamReport,
  createDemoAttempt,
  createSeedHistory,
  createSeedInterview,
  createSeedProgress,
  getExamById,
  getPlanSet,
  getQuestionById,
  publishedExams,
  scoreAttempt,
  submitAnswer,
  startInterview,
  type Attempt,
  type AttemptEvent,
  type AuthSession,
  type DemoOrder,
  type Question,
  type QuestionReviewItem,
  type ReportStatusResponse,
  type ResumeInfo,
} from '../../shared/src/index';

const OUT = join(dirname(fileURLToPath(import.meta.url)), '..', 'src', 'mocks', 'api');
const NOW = Date.parse('2026-10-01T10:00:00.000Z');
const iso = (ms: number) => new Date(ms).toISOString();

const files: Record<string, unknown> = {};
/** name → { method, path, request?, response } */
function ex(name: string, method: string, path: string, response: unknown, request?: unknown) {
  files[name] = { method, path, ...(request !== undefined ? { request } : {}), response };
}

/** The paper never includes answers or explanations — those arrive only via /review after submit. */
function stripAnswers(q: Question): Omit<Question, 'correctOptionIds' | 'correctNumeric' | 'explanation'> {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { correctOptionIds, correctNumeric, explanation, ...rest } = q;
  return rest;
}

// ---------- Auth & profile ----------
const session: AuthSession = {
  user: DEMO_USER,
  tokens: { accessToken: '<firebase-id-token>', refreshToken: '<managed-by-firebase>', expiresAt: iso(NOW + 3_600_000) },
  isNewUser: false,
};
ex('auth-session', 'POST', '/v1/auth/session', session, { profile: { name: 'Ananya Sharma', email: 'ananya@example.com' } });
ex('me-get', 'GET', '/v1/me', { user: DEMO_USER, profile: DEMO_PROFILE, settings: DEFAULT_SETTINGS });
ex('me-patch', 'PATCH', '/v1/me', { user: DEMO_USER, profile: DEMO_PROFILE, settings: DEFAULT_SETTINGS }, { profile: { targetExamIds: ['ssc-cgl'] } });
ex('me-delete', 'DELETE', '/v1/me', null);
ex('consents', 'POST', '/v1/me/consents', null, { consentType: 'resume_processing', granted: true });
ex('credits', 'GET', '/v1/me/credits', {
  credits: SEED_SUBSCRIPTION.credits,
  nextExpiry: SEED_SUBSCRIPTION.ledger.find((l) => l.expiresAt)?.expiresAt,
  ledger: SEED_SUBSCRIPTION.ledger,
});
const history = createSeedHistory();
ex('progress', 'GET', '/v1/me/progress', createSeedProgress(history.reports));

// ---------- Catalog ----------
const exams = publishedExams();
ex('exams', 'GET', '/v1/exams?category=banking&language=en', exams.filter((e) => e.category === 'banking'));
const exam = getExamById('ssc-cgl') ?? exams[0]!;
ex('exam', 'GET', `/v1/exams/${exam.id}`, exam);
ex('interview-roles', 'GET', '/v1/interview-roles', INTERVIEW_ROLES);

// ---------- Attempts ----------
const attempt: Attempt = createDemoAttempt(exam, { id: 'att-example01', language: 'en', now: NOW, mini: true });
ex('attempts-create', 'POST', '/v1/attempts', { ...attempt, states: {}, paper: attempt.paper }, { examId: exam.id, language: 'en', mode: 'mini' });
ex('attempt-paper', 'GET', `/v1/attempts/${attempt.id}/paper`, {
  ...attempt,
  questions: attempt.paper.map((p) => stripAnswers(getQuestionById(p.questionId)!)),
});

// Answer every question deterministically: even index → first option, odd → skipped.
const answered: Attempt = { ...attempt, states: { ...attempt.states } };
attempt.paper.forEach((p, i) => {
  const q = getQuestionById(p.questionId)!;
  const prev = answered.states[p.questionId]!;
  answered.states[p.questionId] =
    i % 2 === 0
      ? { ...prev, visited: true, timeSpentSec: 45 + i * 7, answer: q.options?.length ? { selectedOptionIds: [q.options[0]!.id] } : { numericValue: '0' } }
      : { ...prev, visited: true, timeSpentSec: 20 };
});
ex('attempt-answers', 'PUT', `/v1/attempts/${attempt.id}/answers`, null, { states: answered.states, currentIndex: 4 });
const event: AttemptEvent = { type: 'tab_switch', at: iso(NOW + 300_000) };
ex('attempt-events', 'POST', `/v1/attempts/${attempt.id}/events`, null, event);
ex('attempt-submit', 'POST', `/v1/attempts/${attempt.id}/submit`, { status: 'processing' }, { states: answered.states, autoSubmitted: false });

const submitted: Attempt = { ...answered, status: 'submitted', submittedAt: iso(NOW + 1_500_000) };
const report = buildExamReport(exam, submitted, { id: 'rep-example01', now: NOW + 1_500_000 });
const processing: ReportStatusResponse = { status: 'processing', progress: 40 };
const ready: ReportStatusResponse = { status: 'ready', report };
const failed: ReportStatusResponse = { status: 'failed', message: 'Report generation failed. Your answers are saved — we will retry automatically.' };
ex('attempt-report-processing', 'GET', `/v1/attempts/${attempt.id}/report`, processing);
ex('attempt-report-ready', 'GET', `/v1/attempts/${attempt.id}/report`, ready);
ex('attempt-report-failed', 'GET', `/v1/attempts/${attempt.id}/report`, failed);

const scored = scoreAttempt(submitted.paper, submitted.states, getQuestionById);
const review: QuestionReviewItem[] = scored.questions.map((q, i) => ({
  questionId: q.questionId,
  number: i + 1,
  sectionId: q.sectionId,
  question: getQuestionById(q.questionId)!,
  answer: submitted.states[q.questionId]?.answer,
  outcome: q.outcome,
  marksAwarded: q.marksAwarded,
  timeSpentSec: q.timeSpentSec,
}));
ex('attempt-review', 'GET', `/v1/attempts/${attempt.id}/review`, review);
ex('report-rating', 'POST', `/v1/reports/${report.id}/rating`, null, { rating: 5 });
ex('question-flags', 'POST', `/v1/questions/${attempt.paper[0]!.questionId}/flags`, null, { reason: 'wrong_answer', note: 'Option B looks correct.' });

// ---------- Payments ----------
ex('plans', 'GET', '/v1/plans', getPlanSet('launch'));
ex('orders-create', 'POST', '/v1/orders', { orderId: 'order_Example123', amountPaise: 39900, currency: 'INR', planName: '10-Credit Pack', prefill: { name: DEMO_USER.name, contact: DEMO_USER.phone } }, { planId: 'monthly' });
const order: DemoOrder = { id: 'pay_Example123', planId: 'monthly', amountInr: 399, gstInr: 60.86, method: 'upi', status: 'success', createdAt: iso(NOW) };
ex('orders-verify', 'POST', '/v1/orders/verify', order, {
  razorpay_payment_id: 'pay_Example123',
  razorpay_order_id: 'order_Example123',
  razorpay_signature: '<hmac-sha256 computed by Razorpay>',
  planId: 'monthly',
  method: 'upi',
});
ex('payments-webhook', 'POST', '/v1/webhooks/razorpay', { ok: true }, { event: 'payment.captured', payload: '<Razorpay webhook body — verified with the webhook secret on the server>' });

// ---------- Interviews ----------
const seed = createSeedInterview();
const started = startInterview(seed.session.config, { id: 'int-example01', now: NOW });
ex('interviews-create', 'POST', '/v1/interviews', started, seed.session.config);
ex('interview-get', 'GET', `/v1/interviews/${started.id}`, started);
const afterOne = submitAnswer(started, 'I am a commerce graduate who interned at a cooperative bank…', { now: NOW + 120_000, durationSec: 60 });
ex('interview-answer', 'POST', `/v1/interviews/${started.id}/answer`, afterOne, { text: 'I am a commerce graduate who interned at a cooperative bank…', durationSec: 60 });
ex('interview-end', 'POST', `/v1/interviews/${started.id}/end`, { status: 'processing' });
ex('interview-report-processing', 'GET', `/v1/interviews/${started.id}/report`, { status: 'processing' });
ex('interview-report-ready', 'GET', `/v1/interviews/${started.id}/report`, { status: 'ready', report: seed.report });
const resume: ResumeInfo = { fileName: 'Ananya_Sharma_Resume.pdf', sizeKb: 182, mimeType: 'application/pdf', uploadedAt: iso(NOW) };
ex('uploads-resume', 'POST', '/v1/uploads/resume', resume, '<multipart/form-data: file (PDF/DOCX, ≤ 5 MB)>');

// ---------- Admin ----------
ex('admin-flags', 'GET', '/v1/admin/flags', SEED_REVIEW_QUEUE);
ex('admin-question-patch', 'PATCH', `/v1/admin/questions/${attempt.paper[0]!.questionId}`, { ok: true }, { status: 'retired', note: 'Ambiguous options' });
ex('admin-users', 'GET', '/v1/admin/users?q=ananya', ADMIN_USERS.slice(0, 5));
ex('admin-user-credits', 'POST', `/v1/admin/users/${ADMIN_USERS[0]!.id}/credits`, { credits: 6 }, { delta: 2, reason: 'Goodwill — report delayed' });
ex('admin-payments', 'GET', '/v1/admin/payments', ADMIN_ORDERS.slice(0, 10));
ex('admin-stats', 'GET', '/v1/admin/stats', PLATFORM_ANALYTICS);

// ---------- Write ----------
mkdirSync(OUT, { recursive: true });
for (const f of readdirSync(OUT)) if (f.endsWith('.json')) rmSync(join(OUT, f));
for (const [name, body] of Object.entries(files)) writeFileSync(join(OUT, `${name}.json`), `${JSON.stringify(body, null, 2)}\n`);
console.log(`Wrote ${Object.keys(files).length} fixtures to ${OUT}`);
