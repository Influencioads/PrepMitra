import type { Allowances } from '../types/core';
import { METERED_FEATURES } from '../constants';
import { aiError } from './errors';
import type { AiApi } from './client';
import type {
  AiVisual, CheatCard, CheatCardPayload, CoachSolvedQuestion, CoachTopic, CurrentAffairs, DeckLibraryItem, DeckPayload, DeepDive,
  DeepDiveListItem, DeepDivePayload, DeepPersona, DoubtAnswer, DoubtSolution, MistakeSummary, Notes, NotesPayload, PersonaSnapshot,
  PracticeQuestion, RankPrediction, RevisionToday, ShortcutCard, TopicDeck, TutorChatMessage, WritingEvaluation,
} from './types';

/**
 * Demo data for the AI screens (mock mode: `VITE_USE_MOCK_API` / `EXPO_PUBLIC_USE_MOCK_API` not "false").
 * The demo student holds Pro + AI Tutor Lite, so most features work; Ultra credits are 0 so the upgrade prompt
 * can be seen, and a distress message or an off-topic question behaves like the backend.
 */

const now = () => new Date().toISOString();
let seq = 1;
const uid = () => `00000000-0000-4000-8000-${String(seq++).padStart(12, '0')}`;
const wait = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

const DISTRESS = /\b(kill myself|suicid|end my life|want to die|no point living|can'?t go on|hurt myself|self[- ]harm)\b/i;
const OFF_TOPIC = /\b(recipe|movie|cricket score|write (me )?(a )?(code|program)|python|javascript|joke|girlfriend|boyfriend)\b/i;
export const MOCK_SUPPORT_TEXT =
  "It sounds like this is weighing on you. You are not alone: India's free Tele-MANAS helpline (14416 or 1-800-891-4416) has trained " +
  'counsellors 24x7, in many languages. A score is never the measure of you. When you feel ready, we can take one small step together.';

// ---------- allowances ----------
const START: Record<string, number> = {
  sectional_tests: 100, doubts: 150, premium_doubts: 50, personal_notes: 20, topic_decks: 5, cheat_code_sessions: 13,
  descriptive_evals: 4, text_interviews: 2, voice_interviews: 0, smart_credits: 20, master_credits: 0, tutor_chat_turns: 150,
  photo_doubts: 15, ultra_credits: 0,
};
const USED: Record<string, number> = { doubts: 12, premium_doubts: 3, smart_credits: 2, tutor_chat_turns: 9, personal_notes: 1, cheat_code_sessions: 1 };
const FLAGS: Allowances['flags'] = {
  topic_library: true, shortcut_library: true, leaderboard: true, persona: 'full', study_planner: true, revision_ai: true,
  mistake_notebook: true, deep_persona: true, current_affairs: true, rank_predictor: true,
};

function spend(feature: string, units = 1) {
  const left = (START[feature] ?? 0) - (USED[feature] ?? 0);
  if (left < units) {
    throw aiError(402, 'allowance_exhausted', `You have no ${METERED_FEATURES[feature]?.toLowerCase() ?? feature} left this month. Upgrade or add a top-up pack to keep going.`);
  }
  USED[feature] = (USED[feature] ?? 0) + units;
}
function guard(text: string) {
  if (OFF_TOPIC.test(text)) throw aiError(422, 'off_topic', 'Mitra only helps with exam preparation. Ask about a question from your syllabus.');
}

const flow = (src: string): AiVisual => ({ type: 'mermaid', mermaid: src, table: [], caption: '' });
const table = (rows: string[][], caption = ''): AiVisual => ({ type: 'table', mermaid: '', table: rows, caption });

const pq = (text: string, options: string[], answer: string, explanation: string, level: PracticeQuestion['level'] = 'medium'): PracticeQuestion => ({
  level, text, options: options.map((o, i) => ({ key: 'ABCD'[i]!, text: o })), answer, explanation,
});

// ---------- doubts ----------
const PERCENT_SOLUTION: DoubtSolution = {
  answer_text: 'The price must rise by 25% to get back to the original value.',
  steps: [
    'Let the original price be 100.',
    'After a 20% fall it becomes 80.',
    'To return to 100 it must rise by 20 on a base of 80.',
    '20 ÷ 80 × 100 = 25%.',
  ],
  shortcut: 'Fall of x% needs a rise of x ÷ (100 − x) × 100%. Here 20 ÷ 80 = 25%.',
  memory_hook: '"Down 1/5, up 1/4": the denominator drops by one.',
  real_life_example: 'A ₹1,000 phone on 20% sale costs ₹800; the shop needs ₹200 more, which is 25% of ₹800.',
  common_trap: 'Answering 20% because the fall was 20%: the base changed.',
  practice_question: pq('A salary is cut by 25%. By what percent must it rise to get back to the original?', ['25%', '30%', '33.33%', '40%'], 'C', '25 ÷ 75 = 1/3 = 33.33%.'),
  method: 'percentage_change_reversal',
  answer: 'B',
};

function doubtAnswer(text: string, chosen?: string | null): DoubtAnswer {
  return {
    solution_id: uid(), source: /percent|%/.test(text) ? 'meaning' : 'solved', verified: true, verification: 'two_models',
    premium_used: false, language: 'en', answer: PERCENT_SOLUTION.answer!, solution: PERCENT_SOLUTION,
    personal_note: chosen && chosen !== 'B' ? `You chose ${chosen}; the answer is B. The trap: ${PERCENT_SOLUTION.common_trap}` : '',
    notice: '',
  };
}

// ---------- tutor ----------
const DEEP_DIVE: DeepDivePayload = {
  title: 'Percentage change reversal',
  visual_note: flow('graph TD\n  A[Original 100] -->|falls 20%| B[80]\n  B -->|needs +20| C[Back to 100]\n  C --> D[20 / 80 = 25%]'),
  concept_from_zero: [
    'A percentage is always "of" some base.',
    'After a change, the base is the new value, not the old one.',
    'So undoing a fall needs a bigger percentage than the fall itself.',
  ],
  the_trap: 'Reusing the old base: "it fell 20%, so it must rise 20%".',
  why_students_get_it_wrong: 'Under time pressure we copy the number from the question instead of re-reading which value is the base.',
  never_again_checklist: ['Name the base before every percentage step.', 'Write the new value after each change.', 'Check by applying your answer.'],
  worked_solution: ['Original = 100', 'After −20%: 80', 'Needed rise = 20', '20 ÷ 80 = 25%'],
  shortcut: 'x ÷ (100 − x): 10% → 11.1%, 20% → 25%, 25% → 33.3%, 50% → 100%.',
  practice_questions: [
    pq('A price falls 10%. What rise restores it?', ['10%', '11.11%', '9.09%', '12.5%'], 'B', '10 ÷ 90 = 11.11%.', 'easy'),
    pq('A price rises 25%. What fall restores it?', ['25%', '20%', '33.33%', '15%'], 'B', '25 ÷ 125 = 20%.', 'medium'),
    pq('Successive falls of 20% and 10%. What single rise restores the original?', ['30%', '38.89%', '35%', '40%'], 'B', '100 → 72; 28 ÷ 72 = 38.89%.', 'exam_hard'),
  ],
};
const deepDives: DeepDiveListItem[] = [{ id: 'dd-demo-1', mode: 'smart', title: 'Deep dive (smart)', language: 'en', saved_at: new Date(Date.now() - 2 * 864e5).toISOString() }];
const deepDiveArtifact = (id: string, mode: DeepDive['mode'] = 'smart'): DeepDive => ({
  id, kind: `deep_dive_${mode}`, title: `Deep dive (${mode})`, language: 'en', created_at: now(), payload: DEEP_DIVE, shared: true,
  from_cache: false, mode, credit_used: `${mode}_credits`,
});

const chat: TutorChatMessage[] = [];

// ---------- persona ----------
const topic = (subject: string, name: string, mastery: number, attempted: number, status: string, trend: 'improving' | 'declining' | null = null, ratio = 1) => ({
  subject, topic: name, mastery, attempted, status, trend, avg_seconds: Math.round(45 * ratio), time_ratio: ratio,
});
const MASTERY = [
  topic('quant', 'Time and work', 34, 18, 'weak', 'improving', 1.5),
  topic('reasoning', 'Seating arrangement', 41, 22, 'weak', null, 1.6),
  topic('quant', 'Percentages', 52, 30, 'needs_improvement', 'improving'),
  topic('english', 'Error spotting', 58, 25, 'needs_improvement', 'declining'),
  topic('general-awareness', 'Static GK', 66, 40, 'good'),
  topic('reasoning', 'Coding-decoding', 78, 20, 'good', 'improving', 0.8),
  topic('english', 'Synonyms', 86, 24, 'strong', null, 0.6),
];
const COMPUTED = {
  mocks_taken: 6, latest_attempt_id: null, recent_score_percent: [64, 58, 61, 52, 49],
  weak_topics: MASTERY.slice(0, 4), strong_topics: MASTERY.slice(-3).reverse(), topic_mastery: MASTERY,
  error_mix_percent: { concept: 31, calculation: 24, misread: 18, time_pressure: 14, guessing: 8, option_confusion: 5 },
  speed_profile: 'mixed' as const, slow_topics: ['Time and work', 'Seating arrangement'], consistency_score: 72,
};
const PERSONA: PersonaSnapshot = {
  ...COMPUTED, id: 'persona-demo', kind: 'snapshot', version: 3, created_at: now(),
  ai: {
    summary: 'You are steadily improving: your last three mocks average 61%, up from 49%. Most lost marks are concept gaps in Quant, not speed.',
    learning_style: 'You learn best from worked examples followed by two quick practice questions.',
    one_habit_to_change: 'Skip seating-arrangement sets on the first pass; come back with the time you save.',
  },
};
const deepPersona = (kind: 'deep' | 'ultra'): DeepPersona => ({
  ...COMPUTED, id: `persona-${kind}`, kind, version: 1, created_at: now(),
  ai: {
    summary: 'A consistent, accuracy-first student whose ceiling today is Quant concepts and long reasoning sets.',
    strengths: ['Vocabulary and synonyms (86%)', 'Coding-decoding under time', 'Steady upward trend across mocks'],
    risks: ['Time and work below 40%', 'Seating sets eat 4+ minutes each', 'Error spotting slipping last two weeks'],
    strategy: ['Two 25-minute Time and work drills a week', 'One seating set a day, timed at 3 minutes', 'Revise error-spotting rules every Sunday'],
    exam_day_plan: 'English first (12 min), then Reasoning except seating, then Quant easy-first; seating last.',
    learning_style: 'Worked example → two questions → one-line rule.',
  },
});

// ---------- notes and decks ----------
const NOTES: NotesPayload = {
  title: 'Time and work',
  summary: 'Work = rate × time. Turn every person into a rate (work per day), add rates when people work together.',
  sections: [
    { heading: 'Core idea', bullets: ['If A finishes in 10 days, A does 1/10 of the work a day.', 'Together, rates add: 1/10 + 1/15 = 1/6, so 6 days.'], visual: flow('graph LR\n  A[A: 10 days] --> R[Rate 1/10]\n  B[B: 15 days] --> S[Rate 1/15]\n  R --> T[Together 1/6]\n  S --> T\n  T --> D[6 days]') },
    { heading: 'LCM method', bullets: ['Take total work = LCM of the days (30 units).', 'A = 3 units/day, B = 2 units/day, together 5 → 6 days.'], visual: table([['Person', 'Days', 'Units/day'], ['A', '10', '3'], ['B', '15', '2'], ['A + B', '6', '5']], 'Total work = 30 units') },
  ],
  formulas: [
    { name: 'Combined time', formula: 'T = (a × b) ÷ (a + b)', when_to_use: 'Two people, both working throughout' },
    { name: 'Efficiency', formula: 'Efficiency ∝ 1 ÷ time', when_to_use: 'Comparing workers or "x% more efficient" questions' },
  ],
  mind_map_mermaid: 'mindmap\n  root((Time and work))\n    Rates\n      Add when together\n      Subtract for leaks\n    LCM method\n      Total = LCM of days\n    Pipes and cisterns\n      Outlet = negative rate\n    Wages\n      Share by work done',
  one_page_revision: ['Convert days → rate first.', 'LCM of days = total units.', 'Leaks and outlets are negative rates.', 'Wages split by work, not by days.'],
};
const notesArtifact = (topicName: string, personal: boolean): Notes => ({
  id: uid(), kind: personal ? 'notes' : 'master_notes', title: personal ? `My notes: ${topicName}` : topicName, language: 'en', created_at: now(),
  payload: { ...NOTES, title: topicName || NOTES.title }, shared: !personal, from_cache: !personal,
});

const DECK: DeckPayload = {
  title: 'Percentages', why_it_matters: '6–8 questions in every SSC and banking prelims lean on percentages: profit and loss, DI and interest all reuse it.',
  slides: [
    { title: 'What a percent is', points: ['"Per cent" = per hundred.', 'x% of y = x × y ÷ 100.'], visual: { type: 'none', mermaid: '', table: [], caption: '' } },
    { title: 'Fractions to remember', points: ['1/8 = 12.5%', '1/6 = 16.67%', '1/3 = 33.33%'], visual: table([['Fraction', 'Percent'], ['1/2', '50%'], ['1/4', '25%'], ['1/8', '12.5%'], ['1/6', '16.67%']]) },
    { title: 'Change and reversal', points: ['Base changes after every step.', 'Undo x% fall with x ÷ (100 − x).'], visual: flow('graph TD\n  A[100] -->|−20%| B[80]\n  B -->|+25%| C[100]') },
    { title: 'Successive changes', points: ['a% then b% = a + b + ab/100.', '+10% then −10% = −1%.'], visual: { type: 'none', mermaid: '', table: [], caption: '' } },
  ],
  worked_examples: [{ level: 'exam', question: 'A number is increased by 20% and then decreased by 20%. Net change?', fastest_method: '20 − 20 − 400/100 = −4%', steps: ['Use a + b + ab/100', '20 + (−20) + (−400/100) = −4'] }],
  traps: [{ wrong: '+20% then −20% = 0', right: '−4%', why: 'The second change is on a bigger base.' }],
  cheat_codes: [{ code: 'x ÷ (100 − x)', works_when: 'Undoing a fall', fails_when: 'Undoing a rise (use x ÷ (100 + x))' }],
  summary_sheet: ['Name the base first.', 'Learn the fraction table to 1/12.', 'Successive: a + b + ab/100.'],
  practice_questions: [pq('What is 12.5% of 640?', ['72', '80', '84', '64'], 'B', '640 ÷ 8 = 80.', 'easy')],
};
const LIBRARY: DeckLibraryItem[] = [
  { id: 'deck-percentages', title: 'Percentages', level: 'exam', language: 'en' },
  { id: 'deck-profit-loss', title: 'Profit and loss', level: 'exam', language: 'en' },
  { id: 'deck-syllogism', title: 'Syllogism', level: 'basic', language: 'en' },
  { id: 'deck-tenses', title: 'Tenses for error spotting', level: 'exam', language: 'en' },
];
const deckArtifact = (id: string, title: string, kind = 'topic_deck_library'): TopicDeck => ({
  id, kind, title, language: 'en', created_at: now(), payload: { ...DECK, title }, shared: true, from_cache: kind === 'topic_deck_library',
  personal_note: 'You lose most marks here on base changes; slide 3 is for you.',
});

// ---------- coach ----------
const COACH_TOPICS: CoachTopic[] = [
  { id: 101, name: 'Percentages', section: 'quant' },
  { id: 102, name: 'Time and work', section: 'quant' },
  { id: 201, name: 'Coding-decoding', section: 'reasoning' },
  { id: 202, name: 'Number series', section: 'reasoning' },
];
const SOLVED: CoachSolvedQuestion[] = [
  { question_id: 'cq1', text: 'A price falls 20%. What rise restores it?', options: [{ key: 'A', text: '20%' }, { key: 'B', text: '25%' }], answer: 'B', explanation: '20 ÷ 80 = 25%.' },
  { question_id: 'cq2', text: 'A price falls 50%. What rise restores it?', options: [{ key: 'A', text: '50%' }, { key: 'B', text: '100%' }], answer: 'B', explanation: '50 ÷ 50 = 100%.' },
  { question_id: 'cq3', text: 'A price falls 25%. What rise restores it?', options: [{ key: 'A', text: '25%' }, { key: 'B', text: '33.33%' }], answer: 'B', explanation: '25 ÷ 75 = 33.33%.' },
];
const coachSessions = new Map<string, { topic: string; topicId: number; turns: number; rule: string; step: string; passRate: number }>();
const CARD = (p: Partial<CheatCardPayload> = {}): CheatCardPayload => ({
  name: 'Fall-reversal rule', rule: 'To undo a fall of x%, rise by x ÷ (100 − x) × 100%.', mnemonic: '"Down a fifth, up a quarter"',
  example: '20% fall → 20 ÷ 80 = 25% rise', works_when: 'A single percentage fall is undone', fails_when: 'Successive changes (combine them first)',
  topic: 'Percentages', topic_id: 101, pass_rate: 0.8, ...p,
});
const cards: CheatCard[] = [{ id: 'card-demo-1', kind: 'cheat_card', title: 'Fall-reversal rule', language: 'en', created_at: now(), payload: CARD(), shared: false }];
const SHORTCUTS: ShortcutCard[] = [
  { id: 'sc-1', title: 'Digit-sum check', language: 'en', payload: { name: 'Digit-sum check', rule: 'Check a product by multiplying digit sums.', mnemonic: 'Nines never lie', example: '23 × 14: 5 × 5 = 25 → 7; 322 → 7 ✓', works_when: 'Checking multiplication', fails_when: 'Two options share the digit sum', topic: 'Simplification', pass_rate: 0.95 } },
  { id: 'sc-2', title: 'Successive change', language: 'en', payload: { name: 'Successive change', rule: 'a% then b% = a + b + ab/100.', mnemonic: 'Add, then add the product', example: '+10, −10 → −1%', works_when: 'Two successive percentage changes', fails_when: 'Changes on different bases', topic: 'Percentages', pass_rate: 0.9 } },
  { id: 'sc-3', title: 'Opposite letters', language: 'en', payload: { name: 'Opposite letters', rule: 'Opposite pairs sum to 27 (A+Z = 1+26).', mnemonic: 'EJOTY for 5,10,15,20,25', example: 'Opposite of G (7) is T (20)', works_when: 'Coding-decoding with reversed alphabets', fails_when: 'Shift-based codes', topic: 'Coding-decoding', pass_rate: 0.88 } },
];

// ---------- practice ----------
const CA: CurrentAffairs = {
  id: 'ca-demo', kind: 'current_affairs', title: 'Current affairs (demo)', language: 'en', created_at: now(), shared: true, from_cache: true,
  payload: {
    date: new Date().toISOString().slice(0, 10),
    items: [
      { headline: 'RBI keeps the repo rate unchanged', summary: 'The Monetary Policy Committee held the policy repo rate and kept its stance neutral.', category: 'banking', exam_angle: 'Know the current repo, SDF and MSF rates for banking awareness.', source: 'Demo' },
      { headline: 'New national scheme for rooftop solar', summary: 'A subsidy scheme aims to bring rooftop solar to one crore households.', category: 'schemes', exam_angle: 'Scheme name, ministry and target are common questions.', source: 'Demo' },
      { headline: 'India wins a bronze at the world championships', summary: 'An Indian athlete won bronze in the 3,000 m steeplechase.', category: 'sports', exam_angle: 'Event, venue and medal are asked in SSC GA.', source: 'Demo' },
    ],
    quiz: [
      pq('Which body decides the policy repo rate in India?', ['SEBI', 'Monetary Policy Committee', 'Finance Commission', 'NITI Aayog'], 'B', 'The six-member MPC sets the repo rate.'),
      pq('Rooftop solar subsidy schemes fall under which ministry?', ['Power', 'New and Renewable Energy', 'Rural Development', 'Finance'], 'B', 'MNRE runs rooftop solar programmes.'),
    ],
    dropped_after_fact_check: 1,
  },
};

const REVISION = (): RevisionToday => ({
  id: uid(), kind: 'mistake_review', status: 'open', created_at: now(),
  questions: [
    { question_id: 'rq1', entry_id: 1, type: 'single', difficulty: 'medium', topic: 'Time and work', text: 'A can do a job in 12 days and B in 18 days. In how many days will they finish it together?', options: [{ key: 'A', text: '6' }, { key: 'B', text: '7.2' }, { key: 'C', text: '8' }, { key: 'D', text: '15' }], target_time_sec: 60, hint: 'Turn each into a rate: 1/12 + 1/18. Use LCM 36.' },
    { question_id: 'rq2', entry_id: 2, type: 'single', difficulty: 'easy', topic: 'Error spotting', text: 'Find the error: "Each of the students have submitted their forms."', options: [{ key: 'A', text: 'Each of the students' }, { key: 'B', text: 'have submitted' }, { key: 'C', text: 'their forms' }, { key: 'D', text: 'No error' }], target_time_sec: 30, hint: '"Each" takes a singular verb.' },
    { question_id: 'rq3', entry_id: 3, type: 'single', difficulty: 'medium', topic: 'Percentages', text: 'A price falls 20%. By what percent must it rise to return to the original?', options: [{ key: 'A', text: '20%' }, { key: 'B', text: '25%' }, { key: 'C', text: '30%' }, { key: 'D', text: '16.67%' }], target_time_sec: 40, hint: null },
  ],
  flashcards: cards,
});

/** Correct option keys for the demo revision quiz (the backend checks answers through the practice endpoints). */
export const MOCK_REVISION_ANSWERS: Record<string, string> = { rq1: 'B', rq2: 'B', rq3: 'B' };

function writingEval(answer: string, limit?: number | null, rewrite?: boolean): WritingEvaluation {
  const words = answer.trim().split(/\s+/).filter(Boolean).length;
  const over = !!limit && words > limit * 1.1;
  const scores = [
    { criterion: 'content', score: 7, comment: 'Relevant points, but the second paragraph needs one concrete example.' },
    { criterion: 'structure', score: 6, comment: 'Add a one-line conclusion that answers the question directly.' },
    { criterion: 'language', score: 7, comment: 'Mostly correct; watch subject-verb agreement.' },
    { criterion: 'vocabulary', score: 6, comment: 'Replace repeated "very" with precise words.' },
    { criterion: 'relevance', score: 8, comment: 'Stays on topic throughout.' },
  ];
  const total = Math.max(0, scores.reduce((s, x) => s + x.score, 0) * 2 - (over ? 10 : 0));
  return {
    id: uid(), kind: 'writing_eval', title: 'Writing evaluation', language: 'en', created_at: now(), shared: false,
    payload: {
      word_count: words, word_limit: limit ?? null, over_limit: over, total_score: total, out_of: 100,
      evaluation: {
        scores,
        corrections: [{ original: 'The students was late.', corrected: 'The students were late.', why: 'Plural subject takes "were".' }],
        strengths: ['Clear opening line', 'Good use of a statistic'],
        improvements: ['One example per argument', 'Shorter sentences in the conclusion'],
        model_answer: 'A model answer opens with the issue in one line, gives two reasons with one example each, and closes with a balanced suggestion.',
        overall_feedback: 'A solid answer. Two small fixes (an example and a sharper conclusion) would add 8–10 marks.',
      },
      ...(rewrite ? { topper_rewrite: { topper_version: 'A topper would open with a striking fact, keep each paragraph to one idea and end with a forward-looking line.', what_changed: ['Sharper opening', 'One idea per paragraph', 'Concrete closing suggestion'] } } : {}),
    },
  };
}

// ---------- the mock API ----------
export function createMockAiApi(latencyMs = 400): AiApi {
  const d = () => wait(latencyMs);
  const api: AiApi = {
    async allowances() {
      await wait(Math.min(latencyMs, 150));
      return {
        plans: ['pro_monthly', 'tutor_lite_monthly'], flags: { ...FLAGS },
        limits: Object.keys(START).map((f) => ({ feature: f, label: METERED_FEATURES[f] ?? f, limit: START[f]!, used: USED[f] ?? 0, remaining: Math.max(START[f]! - (USED[f] ?? 0), 0) })),
        resetsAt: new Date(new Date().getFullYear(), new Date().getMonth() + 1, 1).toISOString(),
      };
    },

    async solveDoubt(b) {
      await d();
      if (DISTRESS.test(b.text)) return { support: MOCK_SUPPORT_TEXT };
      guard(b.text);
      if (b.text.trim().length < 8) throw aiError(422, 'question_too_short', 'Type the full question so Mitra can solve it.');
      spend('doubts');
      if (b.escalate) spend('premium_doubts');
      return { ...doubtAnswer(b.text, b.chosen), premium_used: !!b.escalate };
    },
    async photoDoubt(b) {
      await d();
      if (!/^data:image\//.test(b.image)) throw aiError(422, 'invalid_image', 'Send a JPEG, PNG or WebP photo.');
      spend('photo_doubts');
      const read = { text: 'A shirt’s price falls by 20%. By what percent must it rise to return to the original price?', options: [{ key: 'A', text: '20%' }, { key: 'B', text: '25%' }, { key: 'C', text: '30%' }, { key: 'D', text: '15%' }] };
      return { ...doubtAnswer(read.text, b.chosen), read_question: read };
    },
    async explainAgain(id) {
      await d();
      spend('doubts');
      return {
        solution_id: id, answer: 'B', premium_used: true, language: 'en',
        solution: {
          ...PERCENT_SOLUTION, numeric_check: '80 × 1.25 = 100 ✓',
          answer_text: 'Think of it as money: you lost ₹20 from ₹100 and now hold ₹80. Getting ₹20 back is 20 out of 80, which is 25%.',
          steps: ['You have ₹80 after the fall.', 'You need ₹20 more.', '₹20 out of ₹80 = one quarter = 25%.'],
        },
      };
    },
    async doubtFeedback(id, b) {
      await wait(150);
      return { solution_id: id, status: 'live', error_flags: b.report_error ? 1 : 0 };
    },

    async deepDive(b) {
      await d();
      if (b.text && DISTRESS.test(b.text)) return { support: MOCK_SUPPORT_TEXT };
      if (!b.text && !b.question_id && !b.solution_id) throw aiError(422, 'question_required', 'Paste a question or pick one from your mocks.');
      if (b.text) guard(b.text);
      spend(`${b.mode}_credits`);
      const id = uid();
      deepDives.unshift({ id, mode: b.mode, title: `Deep dive (${b.mode})`, language: 'en', saved_at: now() });
      return { ...deepDiveArtifact(id, b.mode), personal_note: b.chosen ? `You chose ${b.chosen}: that is the "same percentage back" trap.` : undefined };
    },
    async myDeepDives() {
      await wait(150);
      return [...deepDives];
    },
    async tutorChat(b) {
      await d();
      const session_id = b.session_id ?? `demo${Date.now().toString(16)}`;
      chat.push({ id: chat.length + 1, session_id, role: 'user', content: b.message, created_at: now() });
      if (DISTRESS.test(b.message)) {
        chat.push({ id: chat.length + 1, session_id, role: 'assistant', content: MOCK_SUPPORT_TEXT, created_at: now() });
        return { session_id, reply: MOCK_SUPPORT_TEXT, follow_ups: [], support: MOCK_SUPPORT_TEXT };
      }
      guard(b.message);
      spend('tutor_chat_turns');
      const reply = b.style === 'story'
        ? 'Imagine Riya and Arjun painting a wall. Riya alone takes 10 days, Arjun 15. Each day Riya paints 3 of 30 bricks, Arjun 2. Together 5 bricks a day, so 30 bricks take 6 days. That is the whole trick: turn people into bricks per day.'
        : b.explain_differently
          ? 'Another way: give the job 30 units (LCM of 10 and 15). A does 3 a day, B does 2. Together 5 a day → 6 days.'
          : 'Turn each worker into a rate. A does 1/10 of the job a day, B 1/15. Together 1/10 + 1/15 = 1/6, so 6 days. In your last mock you added the days instead of the rates; that is the trap to watch.';
      chat.push({ id: chat.length + 1, session_id, role: 'assistant', content: reply, created_at: now() });
      return { session_id, reply, follow_ups: ['Give me a practice question', 'What if a pipe is leaking?', 'Explain the LCM method'], premium_used: !!b.explain_differently, language: 'en' };
    },
    async tutorHistory(sessionId) {
      await wait(150);
      return chat.filter((m) => !sessionId || m.session_id === sessionId);
    },

    async persona() {
      await d();
      return PERSONA;
    },
    async deepPersona() {
      await d();
      return deepPersona('deep');
    },
    async ultraReview() {
      await d();
      spend('ultra_credits');
      return deepPersona('ultra');
    },
    async rank(): Promise<RankPrediction> {
      await d();
      return {
        exam: 'SSC CGL Tier 1', average_score_percent_last_3: 61, prepmitra_test_takers: 4820, expected_rank_band: [1350, 1900], percentile: 68.4,
        last_year_cutoff_percent: 67, gap_to_cutoff_points: 12, weak_topics: ['Time and work', 'Seating arrangement', 'Error spotting'],
        ai: {
          explanation: 'At 61% you sit around the 68th percentile of PrepMitra test-takers. Last year’s cutoff needs about 6 percentage points (12 marks) more.',
          next_steps: ['Fix Time and work: worth ~4 marks', 'Attempt seating sets last: saves ~5 minutes', 'Revise error-spotting rules weekly'],
        },
        note: 'Estimated from PrepMitra mocks only; the real rank depends on the official paper and normalisation.',
      };
    },
    async mistakeSummary(): Promise<MistakeSummary> {
      await d();
      return {
        artifactId: 'ms-demo', title: 'Mistake summary (demo week)', week: '2026-W46',
        groups: [
          { type: 'concept', count: 9, topics: { 'Time and work': 5, Percentages: 4 } },
          { type: 'calculation', count: 6, topics: { 'Data interpretation': 4, Simplification: 2 } },
          { type: 'misread', count: 4, topics: { 'Error spotting': 3, Other: 1 } },
        ],
        ai: {
          summary: 'Concept gaps in Time and work and Percentages cost you the most this week; calculation slips cluster in DI.',
          patterns: [
            { type: 'concept', advice: 'Re-learn rates (work per day) before more practice.' },
            { type: 'calculation', advice: 'Write intermediate values in DI instead of holding them in your head.' },
          ],
          this_week: ['One Time and work deep dive', '15 DI questions with written steps', 'Underline "not/except" in every question'],
        },
      };
    },

    async notes(b) {
      await d();
      guard(b.topic);
      if (b.personal) spend('personal_notes');
      return notesArtifact(b.topic, !!b.personal);
    },
    async deckLibrary(topicQ) {
      await wait(200);
      const t = (topicQ ?? '').toLowerCase();
      return LIBRARY.filter((x) => !t || x.title.toLowerCase().includes(t));
    },
    async libraryDeck(id) {
      await d();
      const item = LIBRARY.find((x) => x.id === id);
      if (!item) throw aiError(404, 'not_found', 'Deck not found.');
      return deckArtifact(id, item.title);
    },
    async topicDeck(b) {
      await d();
      guard(b.topic);
      const mode = b.mode ?? 'library';
      if (mode === 'library') {
        const hit = LIBRARY.find((x) => x.title.toLowerCase() === b.topic.toLowerCase());
        if (!hit) throw aiError(404, 'not_in_library', 'No library deck for this topic yet. Make a custom deck instead.');
        return deckArtifact(hit.id, hit.title);
      }
      if (mode === 'ultra') spend('ultra_credits', 4);
      else if (mode === 'master') spend('master_credits', 3);
      else if ((START.topic_decks ?? 0) - (USED.topic_decks ?? 0) > 0) spend('topic_decks');
      else spend('smart_credits', 3);
      return { ...deckArtifact(uid(), b.topic, `topic_deck_${mode}`), paid_with: mode === 'smart' ? 'topic_decks' : `${mode}_credits` };
    },
    async artifact(id) {
      await d();
      if (id.startsWith('dd-')) return deepDiveArtifact(id);
      const lib = LIBRARY.find((x) => x.id === id);
      if (lib) return deckArtifact(id, lib.title);
      const dd = deepDives.find((x) => x.id === id);
      if (dd) return deepDiveArtifact(id, dd.mode);
      throw aiError(404, 'not_found', 'Item not found.');
    },

    async revisionToday() {
      await d();
      return REVISION();
    },
    async submitRevision(sessionId, answers) {
      await d();
      const qs = REVISION().questions;
      const results = qs.map((q) => {
        const a = answers.find((x) => x.question_id === q.question_id);
        const right = MOCK_REVISION_ANSWERS[q.question_id]!;
        const status = !a?.answer ? 'skipped' : a.answer === right ? 'correct' : 'wrong';
        return { question_id: q.question_id, status, your_answer: a?.answer ?? null, correct_answer: right, explanation: q.hint ?? '', shortcut: '', time_sec: a?.time_spent_sec ?? 0, target_sec: q.target_time_sec };
      });
      const correct = results.filter((r) => r.status === 'correct').length;
      return { id: sessionId, correct, total: results.length, accuracy: Math.round((correct / results.length) * 1000) / 10, results };
    },
    async currentAffairs() {
      await d();
      return CA;
    },
    async evaluateWriting(b) {
      await d();
      if (b.answer.trim().split(/\s+/).length < 30) throw aiError(422, 'answer_too_short', 'Write at least 30 words to get a useful evaluation.');
      spend('descriptive_evals');
      if (b.topper_rewrite) spend('master_credits');
      return writingEval(b.answer, b.word_limit, b.topper_rewrite);
    },

    async coachTopics() {
      await wait(150);
      return COACH_TOPICS;
    },
    async coachStart(topicId) {
      await d();
      const t = COACH_TOPICS.find((x) => x.id === topicId);
      if (!t) throw aiError(404, 'not_found', 'Topic not found.');
      spend('cheat_code_sessions');
      const session_id = `coach${Date.now().toString(16)}`;
      coachSessions.set(session_id, { topic: t.name, topicId, turns: 0, rule: '', step: 'shape', passRate: 0 });
      return {
        session_id, step: 'shape', topic: t.name, solved_questions: SOLVED,
        coach: 'Here are three solved questions of one type. Look at the fall and the rise in each. What rule connects them? Write it in your own words.',
      };
    },
    async coachReply(sid, message) {
      await d();
      const s = coachSessions.get(sid);
      if (!s) throw aiError(404, 'not_found', 'Coach session not found.');
      if (DISTRESS.test(message)) return { session_id: sid, coach: MOCK_SUPPORT_TEXT, step: 'shape', support: MOCK_SUPPORT_TEXT };
      s.turns += 1;
      s.rule = message;
      const exact = /100\s*[-−]\s*x|divide.*(new|remaining)|÷\s*\(?100/i.test(message) || s.turns >= 3;
      if (exact) s.step = 'test';
      return {
        session_id: sid, step: exact ? 'test' : 'shape', rule_draft: message, turns_left: 6 - s.turns,
        coach: exact
          ? 'That is exact. Let’s test your rule on five new questions.'
          : 'Close! Which value do you divide by: the old price or the new one? Try saying it with "x" for the fall.',
      };
    },
    async coachTest(sid, rule) {
      await d();
      const s = coachSessions.get(sid);
      if (!s) throw aiError(404, 'not_found', 'Coach session not found.');
      const r = rule || s.rule || 'rise = x ÷ (100 − x)';
      s.rule = r;
      s.passRate = 0.8;
      s.step = 'lock';
      const mk = (text: string, ans: string, works: boolean, working: string, applies = true) => ({
        question: { question_id: text.slice(0, 6), text, options: [], answer: ans, explanation: '' }, applies, rule_answer: works ? ans : '—', works, working,
      });
      return {
        session_id: sid, step: 'lock', rule: r, pass_rate: 0.8, advice: 'Your rule works for single falls. For two falls in a row, combine them first.',
        results: [
          mk('Price falls 10%; rise to restore?', '11.11%', true, '10 ÷ 90 = 11.11%'),
          mk('Price falls 40%; rise to restore?', '66.67%', true, '40 ÷ 60 = 66.67%'),
          mk('Price falls 5%; rise to restore?', '5.26%', true, '5 ÷ 95 = 5.26%'),
          mk('Price falls 75%; rise to restore?', '300%', true, '75 ÷ 25 = 300%'),
          mk('Two falls of 10%; rise to restore?', '23.46%', false, 'The rule needs one combined fall (19%) first.'),
        ],
      };
    },
    async coachLock(sid, share) {
      await d();
      const s = coachSessions.get(sid);
      if (!s) throw aiError(404, 'not_found', 'Coach session not found.');
      if (s.step !== 'lock') throw aiError(409, 'wrong_step', 'Test your rule before locking it.');
      s.step = 'done';
      const card: CheatCard = { id: uid(), kind: 'cheat_card', title: `${s.topic} rule`, language: 'en', created_at: now(), payload: CARD({ topic: s.topic, topic_id: s.topicId, rule: s.rule, pass_rate: s.passRate }), shared: !!share && s.passRate >= 0.8 };
      cards.unshift(card);
      return card;
    },
    async coachCards() {
      await wait(150);
      return [...cards];
    },
    async shortcuts(topicQ) {
      await wait(150);
      const t = (topicQ ?? '').toLowerCase();
      return SHORTCUTS.filter((x) => !t || x.payload.topic.toLowerCase().includes(t) || x.title.toLowerCase().includes(t));
    },
  };
  return api;
}

export { DEEP_DIVE as MOCK_DEEP_DIVE, NOTES as MOCK_NOTES, DECK as MOCK_DECK };
