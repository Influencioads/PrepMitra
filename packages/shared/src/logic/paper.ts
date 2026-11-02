import type { Attempt, Exam, LanguageCode, PaperQuestion, Question } from '../types/core';
import { QUESTION_BANK } from '../mocks/questions';
import { seededRandom, shuffle } from './random';

/**
 * Assembles a demo paper from the question bank following the exam's sections.
 * Production papers are pre-generated server-side from the exam blueprint and
 * never repeat a question the user has already seen (MVP doc §6.1).
 */
export function buildDemoPaper(exam: Exam, seed: string, bank: Question[] = QUESTION_BANK): PaperQuestion[] {
  const rand = seededRandom(seed);
  const paper: PaperQuestion[] = [];
  const used = new Set<string>();
  for (const section of exam.sections) {
    const pool = bank.filter(
      (q) => q.subject === section.subject && exam.questionTypes.includes(q.type) && !used.has(q.id),
    );
    const picked = shuffle(pool, rand).slice(0, exam.demo.questionsPerSection);
    for (const q of picked) {
      used.add(q.id);
      paper.push({
        questionId: q.id,
        sectionId: section.id,
        marks: section.marksPerQuestion,
        negativeMarks: section.negativeMarks,
      });
    }
  }
  return paper;
}

export const MINI_MOCK = { maxQuestions: 10, durationMin: 30 } as const;

/** Picks questions round-robin across sections so a capped paper still covers every section. */
export function capPaper(paper: PaperQuestion[], max: number): PaperQuestion[] {
  if (paper.length <= max) return paper;
  const bySection = new Map<string, PaperQuestion[]>();
  for (const p of paper) bySection.set(p.sectionId, [...(bySection.get(p.sectionId) ?? []), p]);
  const queues = [...bySection.values()];
  const picked = new Set<PaperQuestion>();
  while (picked.size < max) {
    for (const q of queues) {
      const next = q.shift();
      if (next && picked.size < max) picked.add(next);
    }
  }
  // Keep original section order.
  return paper.filter((p) => picked.has(p));
}

export function createDemoAttempt(
  exam: Exam,
  opts: { id: string; language: LanguageCode; now?: number; mini?: boolean },
): Attempt {
  const now = opts.now ?? Date.now();
  const durationSec = (opts.mini ? MINI_MOCK.durationMin : exam.demo.durationMin) * 60;
  const full = buildDemoPaper(exam, opts.id);
  const paper = opts.mini ? capPaper(full, MINI_MOCK.maxQuestions) : full;
  const firstId = paper[0]?.questionId;
  return {
    id: opts.id,
    examId: exam.id,
    language: opts.language,
    startedAt: new Date(now).toISOString(),
    endsAt: new Date(now + durationSec * 1000).toISOString(),
    durationSec,
    paper,
    states: firstId ? { [firstId]: { visited: true, marked: false, timeSpentSec: 0 } } : {},
    currentIndex: 0,
    status: 'in-progress',
    tabSwitches: 0,
    isMini: opts.mini || undefined,
  };
}

/** Returns the localized question text/options, falling back to English. */
export function localizeQuestion(q: Question, language: LanguageCode): Question {
  const t = q.translations?.[language];
  if (!t || language === 'en') return q;
  return {
    ...q,
    text: t.text,
    options: q.options?.map((o, i) => ({ ...o, text: t.options?.[i] ?? o.text })),
  };
}

export const hasTranslation = (q: Question, language: LanguageCode) => language === 'en' || !!q.translations?.[language];
