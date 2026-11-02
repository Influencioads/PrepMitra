/**
 * PrepMitra AI — shared domain types.
 * These mirror the backend data model (MVP doc §10) so web and mobile
 * can switch from mock services to the real `/v1` API without UI changes.
 */

// ---------- Common ----------
export type ID = string;
export type ISODateString = string;

export type LanguageCode =
  | 'en' | 'hi' | 'bn' | 'mr' | 'te' | 'ta' | 'gu' | 'kn' | 'ml' | 'or' | 'pa' | 'ur'
  | 'as' | 'ne' | 'kok' | 'mai' | 'sa' | 'sd' | 'ks' | 'doi' | 'brx' | 'mni' | 'sat';

export interface Language {
  code: LanguageCode;
  name: string;
  nativeName: string;
  tier: 1 | 2;
  voiceSupported: boolean;
  rtl?: boolean;
  enabled: boolean;
}

export type IconKey =
  | 'landmark' | 'banknote' | 'train' | 'scale' | 'graduation' | 'briefcase'
  | 'code' | 'users' | 'trending' | 'calculator' | 'brain' | 'mic' | 'file' | 'target'
  | 'languages' | 'chart' | 'sparkles' | 'shield' | 'clock' | 'award';

// ---------- Users & profile ----------
export type UserRole = 'user' | 'admin';
export type EducationLevel = '12th' | 'graduate' | 'postgraduate';
export type ExperienceLevel = 'fresher' | '1-3' | '3-5';

export interface User {
  id: ID;
  name: string;
  phone: string;
  email?: string;
  dob?: string;
  state?: string;
  preferredLanguage: LanguageCode;
  role: UserRole;
  createdAt: ISODateString;
  onboardingComplete: boolean;
}

export interface ResumeInfo {
  fileName: string;
  sizeKb: number;
  mimeType: string;
  uploadedAt: ISODateString;
}

export interface UserProfile {
  educationLevel?: EducationLevel;
  stream?: string;
  institution?: string;
  graduationYear?: number;
  targetExamIds: ID[];
  targetRoleIds: ID[];
  experienceYears: number;
  secondaryLanguage?: LanguageCode;
  resume?: ResumeInfo;
}

export interface NotificationPreferences {
  email: boolean;
  push: boolean;
  resultReady: boolean;
  practiceReminders: boolean;
  planExpiry: boolean;
  offers: boolean;
}

export interface PrivacySettings {
  /** DPDP: recruiter sharing is OFF by default and opt-in only. */
  shareWithRecruiters: boolean;
  productAnalytics: boolean;
  showOnLeaderboard: boolean;
}

export interface UserSettings {
  notifications: NotificationPreferences;
  privacy: PrivacySettings;
  examLanguageToggle: boolean;
  reduceMotion: boolean;
}

// ---------- Exams ----------
export type ExamCategory =
  | 'government' | 'banking' | 'railway' | 'civil-services' | 'higher-education' | 'campus-placement';

export type Difficulty = 'Easy' | 'Moderate' | 'Hard';
export type QuestionType = 'single' | 'multiple' | 'numeric';
export type Subject =
  | 'quant' | 'reasoning' | 'english' | 'general-awareness' | 'computer-science'
  | 'electronics' | 'general-studies' | 'data-interpretation';

export interface ExamSection {
  id: ID;
  name: string;
  subject: Subject;
  questionCount: number;
  marksPerQuestion: number;
  negativeMarks: number;
  durationMin?: number;
}

export interface SampleQuestion {
  text: string;
  options: string[];
  answerIndex: number;
}

export type PublishStatus = 'published' | 'draft' | 'hidden';

export interface Exam {
  id: ID;
  title: string;
  shortTitle: string;
  category: ExamCategory;
  description: string;
  conductingBody: string;
  durationMin: number;
  totalQuestions: number;
  totalMarks: number;
  difficulty: Difficulty;
  languages: LanguageCode[];
  creditCost: number;
  isFree: boolean;
  sections: ExamSection[];
  negativeMarking: string;
  calculatorAllowed: boolean;
  questionTypes: QuestionType[];
  popularity: number;
  rating: number;
  attemptsCount: number;
  highlights: string[];
  sampleQuestion: SampleQuestion;
  status: PublishStatus;
  /** Demo paper used by the frontend prototype (shorter than the real exam). */
  demo: { questionsPerSection: number; durationMin: number };
  updatedAt: ISODateString;
}

export interface QuestionOption {
  id: ID;
  text: string;
}

export interface QuestionTranslation {
  text: string;
  options?: string[];
}

export type QuestionStatusAdmin = 'verified' | 'pending-review' | 'quarantined' | 'rejected';

export interface Question {
  id: ID;
  subject: Subject;
  topic: string;
  subtopic?: string;
  type: QuestionType;
  difficulty: Difficulty;
  text: string;
  options?: QuestionOption[];
  correctOptionIds?: ID[];
  correctNumeric?: number;
  /** Absolute tolerance accepted for numeric answers. */
  tolerance?: number;
  explanation: string;
  shortcut?: string;
  expectedTimeSec: number;
  translations?: Partial<Record<LanguageCode, QuestionTranslation>>;
}

// ---------- Attempts ----------
export interface Answer {
  selectedOptionIds?: ID[];
  numericValue?: string;
}

export type PaletteStatus =
  | 'not-visited' | 'not-answered' | 'answered' | 'marked' | 'answered-marked';

export interface QuestionState {
  visited: boolean;
  marked: boolean;
  answer?: Answer;
  timeSpentSec: number;
}

export interface PaperQuestion {
  questionId: ID;
  sectionId: ID;
  marks: number;
  negativeMarks: number;
}

export type AttemptStatus = 'in-progress' | 'submitted';

export interface Attempt {
  id: ID;
  examId: ID;
  language: LanguageCode;
  startedAt: ISODateString;
  /** Demo only: computed on the client. Production timers are server-controlled. */
  endsAt: ISODateString;
  durationSec: number;
  paper: PaperQuestion[];
  states: Record<ID, QuestionState>;
  currentIndex: number;
  status: AttemptStatus;
  submittedAt?: ISODateString;
  reportId?: ID;
  tabSwitches: number;
  copyAttempts?: number;
  autoSubmitted?: boolean;
  /** Free 30-minute mini mock: a shortened paper of the exam. */
  isMini?: boolean;
}

export type QuestionOutcome = 'correct' | 'incorrect' | 'unanswered';

export interface QuestionResult {
  questionId: ID;
  sectionId: ID;
  outcome: QuestionOutcome;
  marksAwarded: number;
  maxMarks: number;
  timeSpentSec: number;
}

export interface SectionResult {
  sectionId: ID;
  name: string;
  score: number;
  maxScore: number;
  correct: number;
  incorrect: number;
  unanswered: number;
  accuracy: number;
  timeSpentSec: number;
}

export interface TopicResult {
  topic: string;
  subject: Subject;
  correct: number;
  total: number;
  attempted: number;
  accuracy: number;
}

export interface ScoreResult {
  score: number;
  maxScore: number;
  percentage: number;
  correct: number;
  incorrect: number;
  unanswered: number;
  attempted: number;
  accuracy: number;
  negativeMarksLost: number;
  marksLostTotal: number;
  sections: SectionResult[];
  topics: TopicResult[];
  questions: QuestionResult[];
}

export interface DayPlan {
  day: number;
  title: string;
  tasks: string[];
  minutes: number;
}

export interface WeaknessItem {
  topic: string;
  accuracy: number;
  evidenceQuestionIds: ID[];
  note: string;
}

export interface Loophole {
  title: string;
  detail: string;
  marksImpact: number;
}

export interface ExamReport {
  id: ID;
  attemptId: ID;
  examId: ID;
  examTitle: string;
  createdAt: ISODateString;
  language: LanguageCode;
  /** Always true in the prototype: analysis is generated by deterministic demo code, not live AI. */
  isDemo: boolean;
  result: ScoreResult;
  timeTakenSec: number;
  durationSec: number;
  percentile: number;
  strengths: string[];
  weaknesses: WeaknessItem[];
  loopholes: Loophole[];
  recommendedNextExamId: ID;
  improvementPlan: DayPlan[];
  rating?: number;
  autoSubmitted?: boolean;
  isMini?: boolean;
}

/** GET /v1/attempts/{id}/report — the report is generated in a background job after submit. */
export type ReportStatusResponse =
  | { status: 'processing'; progress?: number }
  | { status: 'ready'; report: ExamReport }
  | { status: 'failed'; message: string };

/** GET /v1/attempts/{id}/review — one item per question, in the attempt's language. */
export interface QuestionReviewItem {
  questionId: ID;
  number: number;
  sectionId: ID;
  question: Question;
  answer?: Answer;
  outcome: QuestionOutcome;
  marksAwarded: number;
  timeSpentSec: number;
}

/** Event logged during an attempt (light anti-cheat; shown in the report, never punished). */
export interface AttemptEvent {
  type: 'tab_switch' | 'copy_attempt';
  at: ISODateString;
}

export interface AttemptSummary {
  attemptId: ID;
  reportId: ID;
  examId: ID;
  examTitle: string;
  category: ExamCategory;
  score: number;
  maxScore: number;
  accuracy: number;
  percentile: number;
  submittedAt: ISODateString;
  timeTakenSec: number;
}

// ---------- Interviews ----------
export type InterviewMode = 'text' | 'voice';
export type InterviewStage = 'introduction' | 'resume' | 'technical' | 'situational' | 'hr' | 'closing';

export interface InterviewRole {
  id: ID;
  title: string;
  shortTitle: string;
  category: string;
  icon: IconKey;
  description: string;
  levels: ExperienceLevel[];
  durationMin: number;
  questionCount: number;
  evaluates: string[];
  themes: string[];
  languages: LanguageCode[];
  voiceAvailable: boolean;
  creditCost: number;
  status: PublishStatus;
  popularity: number;
}

export interface ScriptedQuestion {
  id: ID;
  stage: InterviewStage;
  text: string;
  /** Keywords a strong answer usually contains; used by the demo evaluator. */
  keywords: string[];
  modelAnswer: string;
  followUp?: { trigger: string[]; text: string };
}

export interface InterviewTurn {
  id: ID;
  speaker: 'interviewer' | 'candidate';
  text: string;
  stage: InterviewStage;
  questionId?: ID;
  isFollowUp?: boolean;
  at: ISODateString;
  durationSec?: number;
}

export interface InterviewConfig {
  roleId: ID;
  level: ExperienceLevel;
  language: LanguageCode;
  mode: InterviewMode;
  resumeFileName?: string;
  jobDescription?: string;
}

export type InterviewStatus = 'in-progress' | 'completed';

export interface InterviewSession {
  id: ID;
  config: InterviewConfig;
  status: InterviewStatus;
  turns: InterviewTurn[];
  questionQueue: ID[];
  askedCount: number;
  /** Planned number of questions (set by the backend; the demo uses the role script length). */
  totalQuestions?: number;
  followUpsAsked: number;
  startedAt: ISODateString;
  endedAt?: ISODateString;
  reportId?: ID;
}

export interface InterviewScores {
  roleKnowledge: number;
  answerStructure: number;
  communication: number;
  confidence: number;
  resumeConsistency: number;
}

export interface InterviewQuestionFeedback {
  questionId: ID;
  question: string;
  answer: string;
  good: string;
  missing: string;
  modelAnswer: string;
  score: number;
}

export interface InterviewReport {
  id: ID;
  sessionId: ID;
  roleId: ID;
  roleTitle: string;
  level: ExperienceLevel;
  mode: InterviewMode;
  language: LanguageCode;
  createdAt: ISODateString;
  isDemo: boolean;
  scores: InterviewScores;
  overall: number;
  voiceMetrics?: { wordsPerMinute: number; fillerWords: number };
  strengths: string[];
  weaknesses: string[];
  redFlags: string[];
  questionFeedback: InterviewQuestionFeedback[];
  plan: DayPlan[];
  durationSec: number;
  rating?: number;
}

// ---------- Plans, credits, payments ----------
export type PlanId = 'free' | 'pay-per-mock' | 'monthly' | 'yearly';

export interface Plan {
  id: PlanId;
  name: string;
  priceInr: number;
  credits: number;
  validityDays: number | null;
  isRecurring: boolean;
  description: string;
  features: string[];
  highlighted?: boolean;
  badge?: string;
  cta: string;
}

export type CreditReason = 'purchase' | 'exam-attempt' | 'interview' | 'refund' | 'free-trial' | 'bonus' | 'expired';

export interface CreditLedgerEntry {
  id: ID;
  delta: number;
  reason: CreditReason;
  label: string;
  at: ISODateString;
  expiresAt?: ISODateString;
}

export interface SubscriptionState {
  planId: PlanId;
  status: 'active' | 'cancelled' | 'expired' | 'trial';
  credits: number;
  renewsAt?: ISODateString;
  autoRenew: boolean;
  freeMiniMockUsed: boolean;
  ledger: CreditLedgerEntry[];
}

export type PaymentMethodLabel = 'upi' | 'card' | 'netbanking' | 'wallet';

export interface DemoOrder {
  id: ID;
  planId: PlanId;
  amountInr: number;
  gstInr: number;
  method: PaymentMethodLabel;
  status: 'success' | 'failed' | 'refunded' | 'pending';
  createdAt: ISODateString;
}

// ---------- Notifications ----------
export type NotificationType = 'result' | 'payment' | 'reminder' | 'plan' | 'system' | 'interview';

export interface AppNotification {
  id: ID;
  type: NotificationType;
  title: string;
  body: string;
  createdAt: ISODateString;
  read: boolean;
  link?: string;
}

// ---------- Progress ----------
export interface TrendPoint {
  date: string;
  label: string;
  score: number;
  accuracy: number;
  examId: ID;
  category: ExamCategory;
}

export interface TopicMastery {
  topic: string;
  subject: Subject;
  mastery: number;
  attempts: number;
  trend: number;
}

export interface WeeklyPractice {
  day: string;
  minutes: number;
}

export interface ProgressData {
  trend: TrendPoint[];
  topics: TopicMastery[];
  weekly: WeeklyPractice[];
  streakDays: number;
  totalMinutes: number;
}

export interface Recommendation {
  id: ID;
  title: string;
  reason: string;
  examId?: ID;
  roleId?: ID;
  topic?: string;
  minutes: number;
}

// ---------- API ----------
export interface ApiError {
  status: number;
  code: string;
  message: string;
}

export interface Paginated<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

export interface ExamQuery {
  search?: string;
  category?: ExamCategory | 'all';
  difficulty?: Difficulty | 'all';
  language?: LanguageCode | 'all';
  sort?: 'popular' | 'rating' | 'duration-asc' | 'duration-desc' | 'credits-asc' | 'title';
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresAt: ISODateString;
}

export interface AuthSession {
  user: User;
  tokens: AuthTokens;
  isNewUser: boolean;
}
