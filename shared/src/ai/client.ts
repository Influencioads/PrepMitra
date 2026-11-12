import type { Allowances } from '../types/core';
import { toAllowances, type Json } from '../api/adapters';
import type {
  AiLang, CheatCard, CoachReply, CoachSession, CoachTestResult, CoachTopic, CurrentAffairs, DeckLibraryItem, DeckRequest, DeepDive,
  DeepDiveListItem, DeepDiveRequest, DeepDiveResult, DeepPersona, DoubtFeedbackResult, DoubtRequest, DoubtResult, ExplainAgainResult,
  MistakeSummary, Notes, RevisionSubmitResult, NotesRequest, PersonaSnapshot, RankPrediction, RevisionToday, ShortcutCard, SupportReply, TopicDeck,
  TutorChatMessage, TutorChatReply, TutorChatRequest, WritingEvaluation, WritingRequest, AiArtifact,
} from './types';

/**
 * One client for every `/v1/ai/*` endpoint, shared by the website and the app. Each app passes its own HTTP
 * transport (axios with auth and the error envelope already handled); `createMockAiApi()` in `mock.ts` is the
 * same interface with demo data, so the screens run without the backend.
 */
export interface AiTransport {
  get<T = Json>(path: string, params?: Record<string, string | number | boolean | undefined>): Promise<T>;
  post<T = Json>(path: string, body?: unknown): Promise<T>;
}

// ---------- adapters (variant smoothing) ----------
export const isSupportReply = (r: unknown): r is SupportReply =>
  typeof r === 'object' && r !== null && typeof (r as { support?: unknown }).support === 'string';

export function toChatReply(r: Json): TutorChatReply {
  // Distress variant: {support: true, reply: <helpline text>}.
  return { ...r, follow_ups: r.follow_ups ?? [], support: r.support === true ? r.reply : typeof r.support === 'string' ? r.support : undefined };
}

export function toCoachReply(r: Json): CoachReply {
  return { ...r, support: r.support === true ? r.coach : typeof r.support === 'string' ? r.support : undefined };
}

/** Two backend shapes: the raw facts (no open mistakes) or a stored artifact with them in `payload`. */
export function toMistakeSummary(r: Json): MistakeSummary {
  if (r && typeof r === 'object' && 'payload' in r) return { ...r.payload, artifactId: r.id, title: r.title };
  return { week: r?.week ?? '', groups: r?.groups ?? [], ai: r?.ai ?? { summary: '', patterns: [], this_week: [] } };
}

export function toCoachTopics(exam: Json): CoachTopic[] {
  const syllabus: Json[] = exam?.syllabus ?? [];
  const parents = new Set(syllabus.map((t) => t.parent_id).filter((x) => x != null));
  // Leaf topics only: the coach needs questions of one type, which live on leaves.
  return syllabus.filter((t) => !parents.has(t.id)).map((t) => ({ id: t.id, name: t.name, section: t.section_key ?? null }));
}

/** Reads an image file as `data:image/...;base64,...` is done by each app; this checks the result. */
export const isImageDataUrl = (s: string) => /^data:image\/(png|jpe?g|webp|heic|heif);base64,/i.test(s);

const q = (language?: AiLang) => (language ? { language } : undefined);

export function createAiApi(t: AiTransport) {
  return {
    allowances: async (): Promise<Allowances> => toAllowances(await t.get('/v1/me/allowances')),

    // doubts
    solveDoubt: (body: DoubtRequest) => t.post<DoubtResult>('/v1/ai/doubts', body),
    photoDoubt: (body: { image: string; chosen?: string | null; language?: AiLang }) => t.post<DoubtResult>('/v1/ai/doubts/photo', body),
    explainAgain: (solutionId: string, language?: AiLang) => t.post<ExplainAgainResult>(`/v1/ai/doubts/${solutionId}/explain-again`, { language }),
    doubtFeedback: (solutionId: string, body: { helpful?: boolean | null; report_error?: boolean }) =>
      t.post<DoubtFeedbackResult>(`/v1/ai/doubts/${solutionId}/feedback`, body),

    // tutor
    deepDive: (body: DeepDiveRequest) => t.post<DeepDiveResult>('/v1/ai/tutor/deep-dives', body),
    myDeepDives: async () => (await t.get<{ items: DeepDiveListItem[] }>('/v1/ai/tutor/deep-dives')).items,
    tutorChat: async (body: TutorChatRequest) => toChatReply(await t.post('/v1/ai/tutor/chat', body)),
    tutorHistory: async (sessionId?: string) =>
      (await t.get<{ items: TutorChatMessage[] }>('/v1/ai/tutor/chat', sessionId ? { session_id: sessionId } : undefined)).items,

    // persona, rank, mistakes
    persona: () => t.get<PersonaSnapshot>('/v1/ai/persona'),
    deepPersona: () => t.post<DeepPersona>('/v1/ai/persona/deep'),
    ultraReview: () => t.post<DeepPersona>('/v1/ai/persona/ultra-review'),
    rank: (examUuid: string) => t.get<RankPrediction>('/v1/ai/rank', { exam_id: examUuid }),
    mistakeSummary: async (language?: AiLang) => toMistakeSummary(await t.get('/v1/ai/mistakes/summary', q(language))),

    // notes and decks
    notes: (body: NotesRequest) => t.post<Notes>('/v1/ai/notes', body),
    deckLibrary: async (topic?: string, language = 'en') =>
      (await t.get<{ items: DeckLibraryItem[] }>('/v1/ai/topic-decks/library', { topic: topic || undefined, language })).items,
    libraryDeck: (deckId: string, language?: AiLang) => t.get<TopicDeck>(`/v1/ai/topic-decks/library/${deckId}`, q(language)),
    topicDeck: (body: DeckRequest) => t.post<TopicDeck>('/v1/ai/topic-decks', body),
    artifact: (id: string) => t.get<AiArtifact>(`/v1/ai/artifacts/${id}`),

    // practice
    revisionToday: (count = 10, language?: AiLang) => t.post<RevisionToday>('/v1/ai/revision/today', { count, language }),
    submitRevision: (sessionId: string, answers: { question_id: string; answer: string | null; time_spent_sec: number }[]) =>
      t.post<RevisionSubmitResult>(`/v1/me/practice/${sessionId}/submit`, { answers }),
    currentAffairs: (date?: string, language?: AiLang) => t.get<CurrentAffairs>('/v1/ai/current-affairs', { date, language }),
    evaluateWriting: (body: WritingRequest) => t.post<WritingEvaluation>('/v1/ai/writing/evaluate', body),

    // cheat code coach
    coachTopics: async (examSlug: string) => toCoachTopics(await t.get(`/v1/exams/${examSlug}`)),
    coachStart: (topicId: number, language?: AiLang) => t.post<CoachSession>('/v1/ai/coach/sessions', { topic_id: topicId, language }),
    coachReply: async (sid: string, message: string) => toCoachReply(await t.post(`/v1/ai/coach/sessions/${sid}/reply`, { message })),
    coachTest: (sid: string, rule?: string) => t.post<CoachTestResult>(`/v1/ai/coach/sessions/${sid}/test`, { rule: rule || undefined }),
    coachLock: (sid: string, share = false) => t.post<CheatCard>(`/v1/ai/coach/sessions/${sid}/lock`, { share }),
    coachCards: async () => (await t.get<{ items: CheatCard[] }>('/v1/ai/coach/cards')).items,
    shortcuts: async (topic?: string) => (await t.get<{ items: ShortcutCard[] }>('/v1/ai/shortcuts', { topic: topic || undefined })).items,
  };
}

export type AiApi = ReturnType<typeof createAiApi>;

/** Path of an artifact's PDF (each app fetches it with its own auth). */
export const aiArtifactPdfPath = (id: string) => `/v1/ai/artifacts/${id}/pdf`;

export type { DeepDive };
