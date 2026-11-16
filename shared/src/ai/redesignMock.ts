import { aiError } from './errors';
import type {
  BlackboardLesson, CheatCode, CheatCodeCatalogue, CheatCodeDrill, CheatCodeDrillResult, CodeCheck, ExamPersonaProfile, ExamPersonaType,
  LessonIndex, PersonaKey, PersonaPlanStep, TeachConcept, TeachResult, TeachScores,
} from './types';
import { MOCK_CHEAT_CODES, MOCK_LESSONS, MOCK_PERSONA_PLANS, MOCK_PERSONA_TYPES, MOCK_TEACH_CONCEPTS } from './redesignFixtures';

/** Mock-mode versions of the redesign endpoints (persona profile, cheat codes, lessons, teach-back). */

type Drill = { text: string; options: { key: string; text: string }[]; answer: string; explanation: string };
const CODES = MOCK_CHEAT_CODES as unknown as (Omit<CheatCode, 'unlocked' | 'drill_size'> & { drill: Drill[] })[];
const LESSONS = MOCK_LESSONS as unknown as (Omit<BlackboardLesson, 'check'> & { check: Drill[] })[];
type Opt = { key: string; text: string; scores: TeachScores; note: string; good: boolean };
const CONCEPTS = MOCK_TEACH_CONCEPTS as unknown as (Omit<TeachConcept, 'rounds'> & {
  rounds: { kind: string; mood: string; chotu: string; coach_hint: string; keywords: string[]; options: Opt[] }[];
})[];

const iso = (daysAgo: number) => new Date(Date.now() - daysAgo * 86_400_000).toISOString();

export const MOCK_PERSONA_PROFILE: ExamPersonaProfile = {
  mocks_taken: 4,
  answers: 380,
  persona: 'fast_guesser',
  traits: { speed: 92, accuracy: 71, risk: 95, stamina: 70, recovery: 48, consistency: 68 },
  matches: [
    { key: 'fast_guesser', match: 96 }, { key: 'section_hopper', match: 78 }, { key: 'steady_climber', match: 71 },
    { key: 'late_bloomer', match: 64 }, { key: 'overthinker', match: 49 }, { key: 'perfectionist', match: 47 },
  ],
  match_percent: 96,
  same_persona_streak: 3,
  confidence: 'high',
  personas: MOCK_PERSONA_TYPES as unknown as ExamPersonaType[],
  evidence: [
    { trait: 'speed', stat: '11 in <15s', title: 'Answered 11 questions in under 15 seconds — 6 wrong', body: 'Five of the six wrong ones were long word problems you skimmed. 5 of the rushed answers were right.' },
    { trait: 'risk', stat: '380 / 400', title: 'Attempted 95% of all questions across 4 mocks', body: 'With 5 options and −0.25 per wrong answer, a blind guess is worth exactly 0 marks on average (+1 × 1/5 − 0.25 × 4/5). Guess only after crossing out at least one option.' },
    { trait: 'recovery', stat: '58% vs 71%', title: 'After a wrong answer, your next 3 answers are 58% right', body: 'Your overall accuracy is 71% (268 of 380). A miss makes you rush the next few questions to win the time back.' },
    { trait: 'stamina', stat: '70%', title: 'Last quarter of the paper held at 70% accuracy', body: 'Close to your 71% average. Stamina is not your problem.' },
    { trait: 'consistency', stat: '54 → 68', title: 'Scores 54, 56, 62, 68 across 4 mocks', body: 'A clear climb.' },
    { trait: 'accuracy', stat: '52% vs 83%', title: 'Long questions: 52% accuracy at 38s per question', body: 'Questions under two lines: 83%. The gap is reading, not maths.' },
  ],
  superpowers: [
    { title: 'Fearless start', body: 'First-quarter accuracy is 74%, at or above your 71% average.' },
    { title: 'Full-paper stamina', body: 'Accuracy holds at 70% in the last quarter of the paper.' },
    { title: 'Percentages on autopilot', body: '92% mastery. Use it to bank time for harder sections.' },
  ],
  blind_spots: [
    { title: 'Half-read questions', body: '6 wrong answers came in under 15 seconds.' },
    { title: 'Chasing lost time', body: 'After a miss, the next 3 answers fall to 58%. Speeding up is the wrong reflex.' },
    { title: 'Weak spot: Seating Arrangement', body: '25% mastery across 16 questions.' },
  ],
  plan: (MOCK_PERSONA_PLANS as unknown as Record<PersonaKey, PersonaPlanStep[]>).fast_guesser,
  history: [
    { attempt_id: 'mock-1', date: iso(30), score: 54, max_score: 100, persona: 'section_hopper', persona_name: 'The Section Hopper', attempted: 92, right: 61, wrong: 31, rushed: 7, rushed_wrong: 4 },
    { attempt_id: 'mock-2', date: iso(21), score: 56, max_score: 100, persona: 'fast_guesser', persona_name: 'The Fast Guesser', attempted: 97, right: 64, wrong: 33, rushed: 14, rushed_wrong: 8 },
    { attempt_id: 'mock-3', date: iso(10), score: 62, max_score: 100, persona: 'fast_guesser', persona_name: 'The Fast Guesser', attempted: 98, right: 70, wrong: 28, rushed: 12, rushed_wrong: 7 },
    { attempt_id: 'mock-4', date: iso(2), score: 68, max_score: 100, persona: 'fast_guesser', persona_name: 'The Fast Guesser', attempted: 93, right: 73, wrong: 20, rushed: 11, rushed_wrong: 6 },
  ],
};

const unlocked = new Set<string>(['ci-1331', 'unit-digit', 'round-two-figures']);
const YOURS = ['ci-1331', 'unit-digit', 'round-two-figures', 'pin-one-both-cases', 'lcm-work', 'two-changes'];
const pub = (c: (typeof CODES)[number]): CheatCode => {
  const { drill, ...rest } = c;
  return { ...rest, unlocked: unlocked.has(c.id), drill_size: drill.length };
};
const code = (id: string) => {
  const c = CODES.find((x) => x.id === id);
  if (!c) throw aiError(404, 'not_found', 'Cheat code not found');
  return c;
};
const lessonOf = (id: string) => {
  const l = LESSONS.find((x) => x.id === id);
  if (!l) throw aiError(404, 'not_found', 'Lesson not found');
  return l;
};

function rubric(text: string, keywords: string[]): TeachScores {
  const t = text.toLowerCase();
  const words = (t.match(/\w+/g) ?? []).length;
  const hits = keywords.filter((k) => t.includes(k)).length;
  const clarity = words < 6 ? 3 : words <= 45 ? 9 : words <= 80 ? 7 : 5;
  const correctness = Math.min(10, hits * 3 + (words >= 8 ? 1 : 0));
  const examples = Math.min(10, (/\b(e\.?g\.?|for example|like|suppose|draw|imagine)\b/.test(t) ? 5 : 0) + (/\d/.test(t) ? 3 : 0) + (/\b[a-f]\b/.test(t) ? 2 : 0));
  return { clarity, correctness, examples };
}

export function createRedesignMock(wait: (ms?: number) => Promise<void>) {
  return {
    async personaProfile(): Promise<ExamPersonaProfile> {
      await wait();
      return MOCK_PERSONA_PROFILE;
    },
    async cheatCodes(): Promise<CheatCodeCatalogue> {
      await wait();
      const topics: Record<string, number> = {};
      CODES.forEach((c) => { topics[c.topic] = (topics[c.topic] ?? 0) + 1; });
      return {
        total: CODES.length, unlocked_count: unlocked.size,
        topics: Object.entries(topics).map(([name, count]) => ({ name, count })),
        yours: YOURS.map((id) => pub(code(id))),
        items: CODES.map(pub),
      };
    },
    async cheatCodeDrill(codeId: string): Promise<CheatCodeDrill> {
      await wait();
      const c = code(codeId);
      return { code_id: c.id, title: c.title, questions: c.drill.map(({ text, options }) => ({ text, options })) };
    },
    async checkCheatCodeDrill(codeId: string, answers: (string | null)[]): Promise<CheatCodeDrillResult> {
      await wait();
      const c = code(codeId);
      const results = c.drill.map((q, i) => ({ correct: (answers[i] ?? '').toUpperCase() === q.answer, answer: q.answer, explanation: q.explanation }));
      const right = results.filter((r) => r.correct).length;
      const newly = right >= 2 && !unlocked.has(codeId);
      if (right >= 2) unlocked.add(codeId);
      return { code_id: codeId, right, of: results.length, results, unlocked: unlocked.has(codeId), newly_unlocked: newly };
    },
    async lessons(): Promise<LessonIndex> {
      await wait();
      return {
        recommended: 'circular-seating', why: { topic: 'Seating Arrangement', mastery: 25 },
        items: LESSONS.map((l) => ({ id: l.id, subject: l.subject, topic: l.topic, steps: l.steps.length })),
      };
    },
    async lesson(id: string): Promise<BlackboardLesson> {
      await wait();
      const l = lessonOf(id);
      return { ...l, check: l.check.map(({ text, options }) => ({ text, options })) };
    },
    async checkLesson(id: string, index: number, answer: string): Promise<CodeCheck> {
      await wait(150);
      const q = lessonOf(id).check[index];
      if (!q) throw aiError(404, 'not_found', 'Question not found');
      return { correct: answer.toUpperCase() === q.answer, answer: q.answer, explanation: q.explanation };
    },
    async teachConcepts() {
      await wait(150);
      return CONCEPTS.map((c) => ({ id: c.id, topic: c.topic, ask: c.ask }));
    },
    async teachConcept(id: string): Promise<TeachConcept> {
      await wait();
      const c = CONCEPTS.find((x) => x.id === id);
      if (!c) throw aiError(404, 'not_found', 'Concept not found');
      return { ...c, rounds: c.rounds.map(({ kind, mood, chotu, coach_hint, options }) => ({ kind, mood, chotu, coach_hint, options: options.map(({ key, text }) => ({ key, text })) })) };
    },
    async teachAnswer(id: string, body: { round: number; choice?: string; text?: string }): Promise<TeachResult> {
      await wait();
      const c = CONCEPTS.find((x) => x.id === id);
      const r = c?.rounds[body.round];
      if (!c || !r) throw aiError(404, 'not_found', 'Round not found');
      let scores: TeachScores; let note: string; let good: boolean; let written: string;
      if (body.choice) {
        const o = r.options.find((x) => x.key === body.choice!.toUpperCase());
        if (!o) throw aiError(422, 'bad_choice', 'Pick one of the options');
        ({ scores, note, good } = o); written = o.text;
      } else {
        written = (body.text ?? '').trim();
        if (written.length < 3) throw aiError(422, 'empty_answer', 'Write your explanation');
        scores = rubric(written, r.keywords);
        good = scores.correctness >= 6;
        note = good ? 'Good — you named the key idea. Add a quick drawing or example so it sticks.' : `Not quite. ${r.coach_hint}`;
      }
      const last = body.round === c.rounds.length - 1;
      const reply = last ? (good ? 'Thank you bhaiya, now I can do these!' : 'I think I need one more try…') : (good ? 'Ohh, samajh gaya! Next one…' : "Hmm, I'm still confused…");
      return { round: body.round, scores, total: scores.clarity + scores.correctness + scores.examples, max_total: 30, good, note, written, chotu_reply: reply, done: last };
    },
  };
}
