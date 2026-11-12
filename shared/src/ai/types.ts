/**
 * Student AI features (`/v1/ai/*`, backend `app/routers/ai.py`, Nov 2026 blueprint).
 *
 * These mirror the backend JSON as-is (snake_case): the AI payloads are deep and model-shaped, so the screens read
 * them directly and `adapters.ts` only smooths the variants (distress replies, the two mistake-summary shapes, …).
 */

export type AiLang = string;
export type AiMode = 'smart' | 'master' | 'ultra';

export interface AiOption {
  key: string;
  text: string;
}

/** Diagram or table attached to a deep dive (`visual_note`), a notes section or a deck slide. */
export interface AiVisual {
  type: 'mermaid' | 'table' | 'none';
  mermaid?: string;
  table?: string[][];
  caption?: string;
}

/** `engine.artifact_out`: the envelope for notes, decks, deep dives, summaries, evaluations and cards. */
export interface AiArtifact<P = unknown, K extends string = string> {
  id: string;
  kind: K;
  title: string;
  language: AiLang;
  created_at: string;
  payload: P;
  shared: boolean;
  from_cache?: boolean;
}

export interface PracticeQuestion {
  level?: 'easy' | 'medium' | 'exam_hard' | string;
  text: string;
  options: AiOption[];
  answer: string;
  explanation: string;
}

// ---------- doubts ----------
export interface DoubtSolution {
  answer_text: string;
  steps: string[];
  shortcut: string;
  memory_hook: string;
  real_life_example: string;
  common_trap: string;
  practice_question?: PracticeQuestion;
  method?: string;
  numeric_check?: string;
  answer?: string;
}

export interface DoubtAnswer {
  solution_id: string | null;
  source: 'exact' | 'meaning' | 'method' | 'solved';
  verified: boolean;
  verification: 'code_checked' | 'two_models' | 'human' | 'unverified';
  premium_used: boolean;
  language: AiLang;
  answer: string;
  solution: DoubtSolution;
  personal_note: string;
  notice: string;
  /** Photo doubts: what the vision model read from the picture. */
  read_question?: { text: string; options: AiOption[] };
}

/** Distress early return: show `support` prominently, nothing else. */
export interface SupportReply {
  support: string;
  read_question?: { text: string; options: AiOption[] };
}

export type DoubtResult = DoubtAnswer | SupportReply;

export interface DoubtRequest {
  text: string;
  options?: AiOption[];
  chosen?: string | null;
  language?: AiLang;
  escalate?: boolean;
}

export interface ExplainAgainResult {
  solution_id: string;
  answer: string;
  solution: DoubtSolution;
  premium_used: boolean;
  language: AiLang;
}

export interface DoubtFeedbackResult {
  solution_id: string;
  status: 'live' | 'hidden' | 'disputed';
  error_flags: number;
}

// ---------- tutor ----------
export interface DeepDivePayload {
  title: string;
  visual_note: AiVisual;
  concept_from_zero: string[];
  the_trap: string;
  why_students_get_it_wrong: string;
  never_again_checklist: string[];
  worked_solution: string[];
  shortcut: string;
  practice_questions: PracticeQuestion[];
}

export type DeepDive = AiArtifact<DeepDivePayload> & {
  mode?: AiMode;
  credit_used?: string;
  personal_note?: string;
};

export type DeepDiveResult = DeepDive | SupportReply;

export interface DeepDiveRequest {
  mode: AiMode;
  question_id?: string;
  solution_id?: string;
  text?: string;
  options?: AiOption[];
  chosen?: string | null;
  language?: AiLang;
}

export interface DeepDiveListItem {
  id: string;
  mode: AiMode;
  title: string;
  language: AiLang;
  saved_at: string;
}

export interface TutorChatRequest {
  message: string;
  session_id?: string;
  style?: 'normal' | 'story';
  explain_differently?: boolean;
  language?: AiLang;
}

/** `support` is normalised to the distress text (the backend sends `support: true` with the text in `reply`). */
export interface TutorChatReply {
  session_id: string;
  reply: string;
  follow_ups: string[];
  premium_used?: boolean;
  language?: AiLang;
  support?: string;
}

export interface TutorChatMessage {
  id: number;
  session_id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

// ---------- persona, rank, mistakes ----------
export interface PersonaTopic {
  subject: string;
  topic: string;
  mastery: number;
  attempted: number;
  status: string;
  trend: 'improving' | 'declining' | null;
  avg_seconds: number | null;
  time_ratio: number | null;
}

export interface PersonaComputed {
  mocks_taken: number;
  latest_attempt_id: string | null;
  recent_score_percent: number[];
  weak_topics: PersonaTopic[];
  strong_topics: PersonaTopic[];
  topic_mastery: PersonaTopic[];
  error_mix_percent: Record<string, number>;
  speed_profile: 'slow' | 'mixed' | 'on_time';
  slow_topics: string[];
  consistency_score: number | null;
}

export interface PersonaSnapshot extends PersonaComputed {
  id: string;
  kind: 'snapshot';
  version: number;
  created_at: string;
  ai: { summary: string; learning_style: string; one_habit_to_change: string };
}

export interface DeepPersona extends PersonaComputed {
  id: string;
  kind: 'deep' | 'ultra';
  version: number;
  created_at: string;
  ai: { summary: string; strengths: string[]; risks: string[]; strategy: string[]; exam_day_plan: string; learning_style: string };
  next_available_at?: string;
}

export interface RankPrediction {
  exam: string;
  average_score_percent_last_3: number;
  prepmitra_test_takers: number;
  expected_rank_band: [number, number];
  percentile: number | null;
  last_year_cutoff_percent: number | null;
  gap_to_cutoff_points: number | null;
  weak_topics: string[];
  ai: { explanation: string; next_steps: string[] };
  note: string;
}

export interface MistakeSummaryFacts {
  week: string;
  groups: { type: string; count: number; topics: Record<string, number> }[];
  ai: { summary: string; patterns: { type: string; advice: string }[]; this_week: string[] };
}

/** Normalised: `artifactId` is set when the summary is a stored artifact (and so has a PDF). */
export interface MistakeSummary extends MistakeSummaryFacts {
  artifactId?: string;
  title?: string;
}

// ---------- notes and decks ----------
export interface NotesPayload {
  title: string;
  summary: string;
  sections: { heading: string; bullets: string[]; visual?: AiVisual }[];
  formulas: { name: string; formula: string; when_to_use: string }[];
  mind_map_mermaid: string;
  one_page_revision: string[];
}
export type NotesKind = 'notes' | 'formula_sheet' | 'mind_map' | 'revision_sheet';
export type NotesLevel = 'basic' | 'exam' | 'advanced';
export interface NotesRequest {
  topic: string;
  kind?: NotesKind;
  level?: NotesLevel;
  personal?: boolean;
  language?: AiLang;
}
export type Notes = AiArtifact<NotesPayload>;

export interface DeckPayload {
  title: string;
  why_it_matters: string;
  slides: { title: string; points: string[]; visual?: AiVisual }[];
  worked_examples: { level: string; question: string; fastest_method: string; steps: string[] }[];
  traps: { wrong: string; right: string; why: string }[];
  cheat_codes: { code: string; works_when: string; fails_when: string }[];
  summary_sheet: string[];
  practice_questions: PracticeQuestion[];
}
export type TopicDeck = AiArtifact<DeckPayload> & { paid_with?: string; personal_note?: string };
export interface DeckRequest {
  topic: string;
  level?: NotesLevel;
  mode?: 'library' | AiMode;
  exam?: string;
  language?: AiLang;
}
export interface DeckLibraryItem {
  id: string;
  title: string;
  level: NotesLevel;
  language: AiLang;
}

// ---------- practice ----------
export interface CheatCardPayload {
  name: string;
  rule: string;
  mnemonic: string;
  example: string;
  works_when: string;
  fails_when: string;
  topic: string;
  topic_id?: number;
  pass_rate: number;
}
export type CheatCard = AiArtifact<CheatCardPayload>;

export interface RevisionQuestion {
  question_id: string;
  entry_id: number | null;
  type: string;
  difficulty: string;
  topic: string | null;
  text: string;
  options: AiOption[];
  target_time_sec: number;
  hint: string | null;
}
export interface RevisionToday {
  id: string;
  kind: string;
  status: string;
  created_at: string;
  questions: RevisionQuestion[];
  flashcards: CheatCard[];
}

/** `POST /v1/me/practice/{id}/submit` (the revision quiz is a practice session). */
export interface RevisionSubmitResult {
  id: string;
  correct: number;
  total: number;
  accuracy: number | null;
  results: { question_id: string; status: string; your_answer: unknown; correct_answer: unknown; explanation: string; shortcut: string; time_sec: number; target_sec: number }[];
}

export interface CurrentAffairsPayload {
  date: string;
  items: { headline: string; summary: string; category: string; exam_angle: string; source: string }[];
  quiz: PracticeQuestion[];
  dropped_after_fact_check: number;
}
export type CurrentAffairs = AiArtifact<CurrentAffairsPayload>;

export type WritingTaskType = 'essay' | 'formal_letter' | 'informal_letter' | 'precis' | 'report' | 'paragraph';
export interface WritingRequest {
  task_type: WritingTaskType;
  question: string;
  answer: string;
  word_limit?: number | null;
  topper_rewrite?: boolean;
  language?: AiLang;
}
export interface WritingPayload {
  word_count: number;
  word_limit: number | null;
  over_limit: boolean;
  total_score: number;
  out_of: number;
  evaluation: {
    scores: { criterion: string; score: number; comment: string }[];
    corrections: { original: string; corrected: string; why: string }[];
    strengths: string[];
    improvements: string[];
    model_answer: string;
    overall_feedback: string;
  };
  topper_rewrite?: { topper_version: string; what_changed: string[] };
}
export type WritingEvaluation = AiArtifact<WritingPayload>;

// ---------- cheat code coach ----------
export interface CoachSolvedQuestion {
  question_id: string;
  text: string;
  options: AiOption[];
  answer: unknown;
  explanation: string;
}
export interface CoachSession {
  session_id: string;
  step: 'shape';
  topic: string;
  solved_questions: CoachSolvedQuestion[];
  coach: string;
}
/** `support` is normalised to the distress text (backend: `support: true`, text in `coach`). */
export interface CoachReply {
  session_id: string;
  step: 'shape' | 'test';
  coach: string;
  rule_draft?: string;
  turns_left?: number;
  support?: string;
}
export interface CoachTestResult {
  session_id: string;
  step: 'lock' | 'shape';
  rule: string;
  pass_rate: number;
  results: { question: CoachSolvedQuestion; applies: boolean; rule_answer: string; works: boolean; working: string }[];
  advice: string;
}
export interface ShortcutCard {
  id: string;
  title: string;
  language: AiLang;
  payload: Omit<CheatCardPayload, 'topic_id'>;
}
/** A syllabus topic the coach can start on (`GET /v1/exams/{slug}` → `syllabus`). */
export interface CoachTopic {
  id: number;
  name: string;
  section?: string | null;
}
