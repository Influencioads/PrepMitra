import { http } from './http';
import { USE_MOCK, mockError } from './mock';

/**
 * AI Personal Exam Mentor (backend `/v1/me/mentor/*`, `/v1/me/exam-goals`, `/v1/me/study-plan`,
 * `/v1/me/mistake-notebook`, `/v1/me/practice/*`, `/v1/attempts/{id}/analysis`).
 * Every number on these screens is computed by the backend from the student's own answers.
 * The mentor needs the real backend: in demo mode (VITE_USE_MOCK_API not "false") calls reject with
 * `MENTOR_NEEDS_BACKEND` and the screens show a notice.
 */

export type TopicStatus = 'not_started' | 'insufficient_data' | 'very_weak' | 'weak' | 'needs_improvement' | 'good' | 'strong';
export type Priority = 'high' | 'medium' | 'low' | 'maintenance';
export type TaskKind =
  | 'learn' | 'practice' | 'revision' | 'mistake_review' | 'sectional_test' | 'mock_test' | 'mock_review' | 'formula_revision' | 'rest';
export type TaskStatus = 'pending' | 'done' | 'skipped' | 'missed';

export interface Countdown {
  goal_id: number;
  exam_id: string;
  exam_slug: string;
  exam_name: string;
  exam_date: string;
  today: string;
  days_remaining: number;
  weeks_remaining: number;
  extra_days: number;
  phase: 'preparation' | 'final_revision' | 'exam_day' | 'passed';
  daily_minutes: number;
  rest_weekday: number | null;
}

export interface TopicBrief {
  topic_id: number;
  name: string;
  subject: string;
  section_key: string | null;
  status: TopicStatus;
  priority: Priority;
  action: string;
  effective_accuracy: number | null;
  accuracy: number | null;
  attempted: number;
  trend: 'improving' | 'declining' | null;
  mastered: boolean;
  confidence: 'none' | 'low' | 'medium' | 'high';
  level: 'basic' | 'intermediate' | 'advanced';
  time_ratio: number | null;
  tradeoff: string | null;
  notes: string[];
  last_seen_at: string | null;
}

export interface TopicDetail extends TopicBrief {
  weightage: number;
  wrong: number;
  skipped: number;
  recent_accuracy: number | null;
  sessions: number;
  reason: string;
  by_difficulty: Record<string, { attempted: number; correct: number }>;
}

export interface StudyTask {
  id: number;
  goal_id: number;
  date: string;
  seq: number;
  kind: TaskKind;
  topic_id: number | null;
  topic: string | null;
  section_key: string | null;
  title: string;
  detail: string;
  level: string | null;
  minutes: number;
  target_questions: number | null;
  priority: Priority | null;
  reason: string;
  status: TaskStatus;
  completed_at: string | null;
  actual_minutes: number | null;
}

export interface PlanDay {
  date: string;
  days_to_exam: number;
  tasks: StudyTask[];
  minutes: number;
  done: number;
  total: number;
}

export interface WeekSummary {
  start: string;
  total: number;
  done: number;
  skipped: number;
  missed: number;
  minutes_done: number;
}

export interface PlanMeta {
  days_left?: number;
  mocks_planned?: number;
  horizon_end?: string | null;
  final_phase_from?: string;
  priority_counts?: Partial<Record<Priority, number>>;
  tradeoffs?: { topic: string; note: string }[];
  note?: { note: string; source: 'ai' | 'code' } | null;
}

export interface StudyPlan {
  goal_id: number;
  plan_version: number;
  generated_at: string | null;
  today: string;
  exam_date: string;
  meta: PlanMeta;
  days: PlanDay[];
  week: WeekSummary;
}

export interface MarksLostItem {
  reason: 'incorrect_answers' | 'negative_marking' | 'unattempted' | 'partially_correct';
  marks: number;
  questions: number;
}

export interface SectionRow {
  key: string;
  name: string;
  subject: string;
  total_marks: number;
  scored: number;
  lost: number;
  lost_incorrect: number;
  lost_negative: number;
  lost_unattempted: number;
  questions: number;
  attempted: number;
  correct: number;
  wrong: number;
  unanswered: number;
  accuracy: number | null;
  time_sec: number;
  time_limit_sec: number | null;
}

export type TimeBand = 'efficient' | 'slow_correct' | 'time_sink' | 'rushed_wrong' | 'wrong' | 'skipped_after_time' | 'skipped' | 'unseen';

export interface AttemptAnalysis {
  attempt_id: string;
  exam: { id: string; slug: string; name: string };
  submitted_at: string;
  report_id: string | null;
  score: number;
  max_score: number;
  percentile: number | null;
  accuracy: number | null;
  counts: { questions: number; attempted: number; correct: number; wrong: number; partial: number; unanswered: number };
  negative_marking: boolean;
  marks_lost: { total_lost: number; gross_lost_before_penalty: number; items: MarksLostItem[] };
  sections: SectionRow[];
  topics: {
    topic_id: number; topic: string; section_key: string; questions: number; attempted: number; correct: number;
    wrong: number; unanswered: number; marks_lost: number; accuracy: number | null; avg_time_sec: number | null;
    avg_target_sec: number;
  }[];
  time: {
    total_sec: number;
    bands: Record<TimeBand, number>;
    questions: {
      ref: number; question_id: string; section_key: string; topic: string; difficulty: string; status: string;
      time_sec: number; target_sec: number; time_ratio: number | null; band: TimeBand; marks_lost: number;
    }[];
    observations: { kind: string; severity: 'high' | 'medium' | 'positive'; text: string; question_refs: number[] }[];
  };
  recommendations: { kind: string; text: string; topic: string | null }[];
}

export interface MockStats {
  tests_completed: number;
  highest_score: number | null;
  average_score: number | null;
  recent_score: number | null;
  max_score: number | null;
  highest_pct: number | null;
  average_pct: number | null;
  trend: { attempt_id: string; at: string; score: number; max_score: number }[];
  last_attempt_id: string | null;
  accuracy: number | null;
  time_management: { efficient_share: number | null; time_sinks: number; rushed_wrong: number; unseen: number } | null;
}

export interface Overview {
  exam: Countdown;
  coverage: {
    syllabus_completion_pct: number; preparation_pct: number; topics_total: number; topics_completed: number;
    topics_covered: number; topics_pending: number; topics_weak: number; min_evidence: number;
  };
  mock_tests: MockStats;
  subjects: { subject: string; name: string; topics: number; attempted: number; accuracy: number | null; weak: number; strong: number; not_started: number }[];
  topics: { strong: TopicBrief[]; weak: TopicBrief[]; pending: TopicBrief[]; needs_revision: TopicBrief[]; all: TopicBrief[] };
  revision: { notebook_due: number; notebook_active: number; notebook_resolved: number };
  recommendations: {
    study_today: { task_id: number; title: string; minutes: number; kind: TaskKind }[];
    revise: { title: string; kind: string; topic_id?: number }[];
    practise: TopicBrief[];
    more_attention: TopicBrief[];
    less_time: TopicBrief[];
    mock_test: { advice: 'yes' | 'not_yet' | 'no'; reason: string };
  };
  plan: {
    note: { note: string; source: 'ai' | 'code' } | null;
    version: number;
    generated_at: string | null;
    today: StudyTask[];
    next_days: PlanDay[];
    week: WeekSummary;
    tradeoffs: { topic: string; note: string }[];
  };
  weekly_progress: {
    this_week: { questions: number; correct: number; accuracy: number | null; tasks_done: number; minutes: number };
    last_week: { questions: number; correct: number; accuracy: number | null; tasks_done: number; minutes: number };
    accuracy_change: number | null;
  };
}

export interface MentorDashboard {
  goals: Countdown[];
  selected: Overview | null;
}

export type MistakeType = 'concept' | 'calculation' | 'misread' | 'wrong_formula' | 'guessing' | 'time_pressure' | 'option_confusion';
export type NotebookFilter = 'all' | 'wrong' | 'corrected' | 'repeated' | 'slow' | 'bookmarked' | 'due' | 'resolved';

export interface NotebookEntry {
  id: number;
  question_id: string;
  topic: string | null;
  topic_id: number | null;
  difficulty: string;
  type: 'single' | 'multi' | 'numeric';
  text: string;
  options: { key: string; text: string }[];
  your_answer: unknown;
  correct_answer: unknown;
  explanation: string;
  shortcut: string;
  reasons: string[];
  mistake_type: MistakeType | null;
  mistake_type_source: 'student' | 'auto' | null;
  times_wrong: number;
  revision_correct: number;
  revision_wrong: number;
  box: number;
  next_review_at: string | null;
  last_time_sec: number;
  bookmarked: boolean;
  note: string;
  status: 'active' | 'resolved';
}

export interface NotebookPage {
  items: NotebookEntry[];
  total: number;
  counts: Record<NotebookFilter, number>;
  by_mistake_type: Record<string, number>;
}

export interface PracticeQuestion {
  question_id: string;
  entry_id: number | null;
  type: 'single' | 'multi' | 'numeric';
  difficulty: string;
  topic: string | null;
  text: string;
  options: { key: string; text: string }[];
  target_time_sec: number;
}

export interface PracticeSession {
  id: string;
  kind: 'mistake_review' | 'topic_quiz';
  questions: PracticeQuestion[];
}

export interface PracticeResult {
  id: string;
  correct: number;
  total: number;
  accuracy: number | null;
  results: { question_id: string; status: string; your_answer: unknown; correct_answer: unknown; explanation: string; shortcut: string; time_sec: number; target_sec: number }[];
}

export interface ChatMessage {
  id: number;
  role: 'student' | 'mentor';
  content: string;
  follow_ups: string[];
  source?: 'ai' | 'code' | null;
  created_at: string;
}

export interface ReminderPrefs {
  push_enabled: boolean;
  email_enabled: boolean;
  morning_enabled: boolean;
  morning_time: string;
  afternoon_enabled: boolean;
  afternoon_time: string;
  evening_enabled: boolean;
  evening_time: string;
  countdown_enabled: boolean;
  mock_reminders_enabled: boolean;
  max_per_day: number;
  timezone: string;
}

export interface ExamOption {
  slug: string;
  name: string;
  category: string;
}

export const MENTOR_NEEDS_BACKEND = 'MENTOR_NEEDS_BACKEND';

function live() {
  if (USE_MOCK) {
    throw mockError(0, MENTOR_NEEDS_BACKEND, 'The AI mentor works with your real results. Connect the app to the PrepMitra backend to use it.');
  }
}

const get = async <T>(url: string, params?: object): Promise<T> => {
  live();
  return (await http.get(url, { params })).data as T;
};
const send = async <T>(method: 'post' | 'put' | 'patch' | 'delete', url: string, body?: object): Promise<T> => {
  live();
  return (await http[method](url, body)).data as T;
};

export const mentorService = {
  goals: async () => (await get<{ items: Countdown[] }>('/v1/me/exam-goals')).items,
  dashboard: (goalId?: number) => get<MentorDashboard>('/v1/me/mentor/dashboard', goalId ? { goal_id: goalId } : undefined),
  examOptions: async (): Promise<ExamOption[]> =>
    ((await get<{ items: ExamOption[] }>('/v1/exams', { limit: 100 })).items ?? []).filter((e) => e.category === 'banking' || e.slug.startsWith('mini')),
  createGoal: (body: { exam_id: string; exam_date: string; daily_minutes: number; rest_weekday: number | null }) =>
    send<Countdown>('post', '/v1/me/exam-goals', body),
  updateGoal: (goalId: number, body: { exam_date?: string; daily_minutes?: number; rest_weekday?: number; clear_rest_day?: boolean }) =>
    send<Countdown>('patch', `/v1/me/exam-goals/${goalId}`, body),
  archiveGoal: (goalId: number) => send<void>('delete', `/v1/me/exam-goals/${goalId}`),
  topics: (goalId: number, status?: string) => get<{ items: TopicDetail[]; min_evidence: number }>('/v1/me/mentor/topics', { goal_id: goalId, status }),
  plan: (goalId: number, start?: string, end?: string) => get<StudyPlan>('/v1/me/study-plan', { goal_id: goalId, start, end }),
  regenerate: (goalId: number) => send<StudyPlan>('post', '/v1/me/study-plan/generate', { goal_id: goalId }),
  setTask: (taskId: number, status: 'done' | 'skipped' | 'pending', actualMinutes?: number) =>
    send<StudyTask>('patch', `/v1/me/study-plan/tasks/${taskId}`, { status, actual_minutes: actualMinutes }),
  analysis: (attemptId: string) => get<AttemptAnalysis>(`/v1/attempts/${attemptId}/analysis`),
  coachNote: (attemptId: string) => get<{ note: string; source: 'ai' | 'code' }>(`/v1/attempts/${attemptId}/analysis/coach-note`),
  notebook: (filter: NotebookFilter, offset = 0) => get<NotebookPage>('/v1/me/mistake-notebook', { filter, offset, limit: 20 }),
  updateEntry: (id: number, body: { mistake_type?: MistakeType; clear_mistake_type?: boolean; bookmarked?: boolean; note?: string }) =>
    send<NotebookEntry>('patch', `/v1/me/mistake-notebook/${id}`, body),
  startMistakeReview: (count = 10, taskId?: number) => send<PracticeSession>('post', '/v1/me/practice/mistake-review', { count, task_id: taskId }),
  startTopicQuiz: (topicId: number, count = 10, taskId?: number) =>
    send<PracticeSession>('post', '/v1/me/practice/topic-quiz', { topic_id: topicId, count, task_id: taskId }),
  submitPractice: (id: string, answers: { question_id: string; answer: string | string[] | number | null; time_spent_sec: number }[]) =>
    send<PracticeResult>('post', `/v1/me/practice/${id}/submit`, { answers }),
  chatHistory: () => get<{ items: ChatMessage[] }>('/v1/me/mentor/chat'),
  chat: (message: string, goalId?: number) => send<ChatMessage>('post', '/v1/me/mentor/chat', { message, goal_id: goalId }),
  reminderPrefs: () => get<ReminderPrefs>('/v1/me/notification-preferences'),
  saveReminderPrefs: (body: Partial<ReminderPrefs>) => send<ReminderPrefs>('put', '/v1/me/notification-preferences', body),
};
