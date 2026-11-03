import type {
  Answer, Exam, PaperQuestion, Question, QuestionOutcome, QuestionResult, QuestionState, ScoreResult,
  SectionResult, TopicResult,
} from '../types/core';
import { isAnswered } from './questionState';

const round2 = (n: number) => Math.round(n * 100) / 100;

/** Evaluates one answer against the answer key. */
export function evaluateAnswer(question: Question, answer?: Answer): QuestionOutcome {
  if (!isAnswered(answer)) return 'unanswered';
  if (question.type === 'numeric') {
    const value = Number(answer!.numericValue);
    const tol = question.tolerance ?? 0;
    return question.correctNumeric !== undefined && Math.abs(value - question.correctNumeric) <= tol + 1e-9
      ? 'correct'
      : 'incorrect';
  }
  const selected = [...(answer!.selectedOptionIds ?? [])].sort();
  const correct = [...(question.correctOptionIds ?? [])].sort();
  if (question.type === 'single') return selected.length === 1 && selected[0] === correct[0] ? 'correct' : 'incorrect';
  // Multiple-correct (MSQ): all-or-nothing, as in GATE.
  return selected.length === correct.length && selected.every((s, i) => s === correct[i]) ? 'correct' : 'incorrect';
}

/**
 * Negative marking applies only to option-based single-correct questions
 * (GATE/CAT convention: no negative marking for MSQ and numeric answers).
 */
export function marksFor(question: Question, item: PaperQuestion, outcome: QuestionOutcome): number {
  if (outcome === 'correct') return item.marks;
  if (outcome === 'incorrect' && question.type === 'single') return -item.negativeMarks;
  return 0;
}

/** Scores an attempt. Pure, deterministic code — "numbers by code, words by AI". */
export function scoreAttempt(
  paper: PaperQuestion[],
  states: Record<string, QuestionState>,
  questionLookup: (id: string) => Question | undefined,
  sectionNames: Record<string, string> = {},
): ScoreResult {
  const questions: QuestionResult[] = [];
  const sectionMap = new Map<string, SectionResult>();
  const topicMap = new Map<string, TopicResult>();
  let negativeMarksLost = 0;

  for (const item of paper) {
    const q = questionLookup(item.questionId);
    if (!q) continue;
    const state = states[item.questionId];
    const outcome = evaluateAnswer(q, state?.answer);
    const marks = marksFor(q, item, outcome);
    if (marks < 0) negativeMarksLost += -marks;
    questions.push({
      questionId: q.id, sectionId: item.sectionId, outcome, marksAwarded: marks, maxMarks: item.marks,
      timeSpentSec: state?.timeSpentSec ?? 0,
    });

    const sec = sectionMap.get(item.sectionId) ?? {
      sectionId: item.sectionId, name: sectionNames[item.sectionId] ?? item.sectionId, score: 0, maxScore: 0,
      correct: 0, incorrect: 0, unanswered: 0, accuracy: 0, timeSpentSec: 0,
    };
    sec.score += marks;
    sec.maxScore += item.marks;
    sec[outcome] += 1;
    sec.timeSpentSec += state?.timeSpentSec ?? 0;
    sectionMap.set(item.sectionId, sec);

    const topic = topicMap.get(q.topic) ?? { topic: q.topic, subject: q.subject, correct: 0, total: 0, attempted: 0, accuracy: 0 };
    topic.total += 1;
    if (outcome !== 'unanswered') topic.attempted += 1;
    if (outcome === 'correct') topic.correct += 1;
    topicMap.set(q.topic, topic);
  }

  const correct = questions.filter((q) => q.outcome === 'correct').length;
  const incorrect = questions.filter((q) => q.outcome === 'incorrect').length;
  const unanswered = questions.length - correct - incorrect;
  const attempted = correct + incorrect;
  const score = round2(questions.reduce((s, q) => s + q.marksAwarded, 0));
  const maxScore = round2(questions.reduce((s, q) => s + q.maxMarks, 0));
  const sections = [...sectionMap.values()].map((s) => ({
    ...s,
    score: round2(s.score),
    maxScore: round2(s.maxScore),
    accuracy: s.correct + s.incorrect > 0 ? Math.round((s.correct / (s.correct + s.incorrect)) * 100) : 0,
  }));
  const topics = [...topicMap.values()]
    .map((t) => ({ ...t, accuracy: t.total > 0 ? Math.round((t.correct / t.total) * 100) : 0 }))
    .sort((a, b) => b.accuracy - a.accuracy);

  return {
    score,
    maxScore,
    percentage: maxScore > 0 ? Math.round((Math.max(score, 0) / maxScore) * 100) : 0,
    correct,
    incorrect,
    unanswered,
    attempted,
    accuracy: attempted > 0 ? Math.round((correct / attempted) * 100) : 0,
    negativeMarksLost: round2(negativeMarksLost),
    marksLostTotal: round2(maxScore - score),
    sections,
    topics,
    questions,
  };
}

export const sectionNameMap = (exam: Exam): Record<string, string> =>
  Object.fromEntries(exam.sections.map((s) => [s.id, s.name]));

/** Demo percentile estimate from percentage score (production uses platform-wide distribution). */
export function estimatePercentile(percentage: number): number {
  const p = Math.max(0, Math.min(100, percentage));
  const value = 100 / (1 + Math.exp(-(p - 50) / 11));
  return Math.round(Math.min(99.9, Math.max(1, value)) * 10) / 10;
}
