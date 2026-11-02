/**
 * Admin domain types (Milestone 4). These mirror the planned `/v1/admin/*`
 * payloads so the admin console can switch from mock data to the real API.
 */
import type {
  CreditLedgerEntry, ExamCategory, ID, ISODateString, LanguageCode, PaymentMethodLabel, PlanId, Question,
  QuestionStatusAdmin,
} from './core';

// ---------- Team & RBAC ----------
export type AdminModule =
  | 'dashboard' | 'exams' | 'questions' | 'review' | 'lessons' | 'languages' | 'roles' | 'users' | 'payments'
  | 'reports' | 'settings';

export type AdminTeamRole = 'founder' | 'content-manager' | 'subject-expert' | 'language-reviewer' | 'support' | 'finance';

export type PermissionLevel = 'full' | 'edit' | 'view' | 'none';

export interface AdminTeamRoleMeta {
  id: AdminTeamRole;
  label: string;
  description: string;
}

export interface AdminTeamMember {
  id: ID;
  name: string;
  email: string;
  role: AdminTeamRole;
  languages: LanguageCode[];
  active: boolean;
  lastActiveAt: ISODateString;
}

// ---------- Audit ----------
export interface AuditLogEntry {
  id: ID;
  actor: string;
  module: AdminModule;
  action: string;
  target: string;
  details?: string;
  at: ISODateString;
}

// ---------- Question bank ----------
export type QuestionSource = 'ai-generated' | 'manual';

export interface AdminQuestion extends Question {
  status: QuestionStatusAdmin;
  /** % of learners answering correctly across attempts. */
  accuracy: number;
  attemptCount: number;
  /** Independent user reports (3+ triggers auto-quarantine when enabled). */
  reportCount: number;
  source: QuestionSource;
  updatedAt: ISODateString;
}

// ---------- Review queue ----------
export type ReviewSource = 'random-sample' | 'user-flag';
export type ReviewReason = 'wrong-answer' | 'unclear' | 'translation' | 'typo' | 'multiple-correct' | 'outdated';
export type ReviewStatus = 'open' | 'fixed' | 'rejected' | 'quarantined';

export interface ReviewFlag {
  id: ID;
  reporter: string;
  reason: ReviewReason;
  comment?: string;
  language: LanguageCode;
  at: ISODateString;
}

export interface ReviewItem {
  id: ID;
  questionId: ID;
  examId?: ID;
  source: ReviewSource;
  language: LanguageCode;
  flags: ReviewFlag[];
  status: ReviewStatus;
  createdAt: ISODateString;
  resolvedAt?: ISODateString;
  resolvedBy?: string;
  resolutionNote?: string;
}

// ---------- AI lessons & glossary ----------
export type LessonSource = 'review-fix' | 'manual' | 'flag-pattern';

export interface AiLesson {
  id: ID;
  topic: string;
  language: LanguageCode;
  lessonText: string;
  source: LessonSource;
  sourceQuestionId?: ID;
  active: boolean;
  createdAt: ISODateString;
  updatedAt: ISODateString;
}

export interface GlossaryTerm {
  id: ID;
  term: string;
  language: LanguageCode;
  approvedTranslation: string;
  updatedAt: ISODateString;
}

// ---------- Languages ----------
export interface LanguageConfig {
  code: LanguageCode;
  tier: 1 | 2;
  enabled: boolean;
  voiceSupported: boolean;
  /** % of the question bank with a verified translation. */
  coverage: number;
  reviewer: string | null;
}

// ---------- Interview config ----------
export interface RubricCriterion {
  id: ID;
  name: string;
  description: string;
  /** Percentage weight; all criteria must sum to 100. */
  weight: number;
}

export interface InterviewerPromptConfig {
  persona: string;
  systemPrompt: string;
  tone: 'friendly' | 'neutral' | 'strict';
  maxFollowUps: number;
  rubric: RubricCriterion[];
  updatedAt: ISODateString;
}

// ---------- Users ----------
export type AdminUserStatus = 'active' | 'blocked';

export interface AdminUserAttempt {
  id: ID;
  kind: 'exam' | 'interview';
  title: string;
  /** Percentage score 0–100. */
  score: number;
  at: ISODateString;
}

export interface AdminUserRecord {
  id: ID;
  name: string;
  phone: string;
  email?: string;
  state: string;
  preferredLanguage: LanguageCode;
  planId: PlanId;
  status: AdminUserStatus;
  credits: number;
  joinedAt: ISODateString;
  lastActiveAt: ISODateString;
  attempts: AdminUserAttempt[];
  ledger: CreditLedgerEntry[];
}

// ---------- Payments ----------
export type PaymentGateway = 'razorpay' | 'cashfree';
export type AdminOrderStatus = 'paid' | 'failed' | 'refunded' | 'pending';

export interface AdminOrder {
  id: ID;
  invoiceNo: string;
  userId: ID;
  userName: string;
  planId: PlanId;
  /** Amount charged, GST inclusive. */
  amountInr: number;
  gstInr: number;
  gateway: PaymentGateway;
  method: PaymentMethodLabel;
  status: AdminOrderStatus;
  createdAt: ISODateString;
  refundedAt?: ISODateString;
  refundReason?: string;
}

export interface AdminSubscription {
  id: ID;
  userId: ID;
  userName: string;
  planId: PlanId;
  status: 'active' | 'cancelled' | 'expired';
  startedAt: ISODateString;
  renewsAt: ISODateString;
  autoRenew: boolean;
  amountInr: number;
}

// ---------- Settings ----------
export interface PlanConfig {
  id: PlanId;
  priceInr: number;
  credits: number;
  validityDays: number | null;
  active: boolean;
}

export interface FeatureFlags {
  voiceInterviews: boolean;
  tabSwitchLogging: boolean;
  autoQuarantine: boolean;
  autoQuarantineThreshold: number;
  /** % of newly generated questions sampled for human review. */
  reviewSampleRate: number;
}

export interface AdminSettings {
  featureFlags: FeatureFlags;
  plans: PlanConfig[];
  /** Demo helper: makes the next admin data load fail so error states can be checked. */
  simulateLoadError: boolean;
}

// ---------- Metrics ----------
export interface SeriesPoint {
  label: string;
  value: number;
}

export interface QualityMetrics {
  avgReportRating: number;
  ratingDistribution: { stars: number; count: number }[];
  flagRate: number;
  flagRateByExam: { examId: ID; label: string; rate: number }[];
  flagRateByLanguage: { language: LanguageCode; rate: number }[];
  verificationFailureRate: number;
  aiCostPerAttemptInr: number;
  aiCostCapInr: number;
  aiCostTrend: SeriesPoint[];
  reportGenSec: number;
  reportGenTargetSec: number;
  reportGenTrend: SeriesPoint[];
}

export interface PlatformAnalytics {
  attemptsToday: number;
  attemptsByCategory: { category: ExamCategory; attempts: number }[];
  attemptsByExam: { examId: ID; label: string; attempts: number }[];
  secondAttemptRate: number;
  secondAttemptTarget: number;
  conversionRate: number;
  conversionTarget: number;
  retentionTrend: SeriesPoint[];
  conversionTrend: SeriesPoint[];
  interviewsByRole: { roleId: ID; label: string; sessions: number }[];
}
