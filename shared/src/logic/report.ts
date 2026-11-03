import type { Attempt, DayPlan, Exam, ExamReport, Loophole, Question, ScoreResult, WeaknessItem } from '../types/core';
import { EXAMS } from '../mocks/exams';
import { getQuestionById } from '../mocks/questions';
import { estimatePercentile, scoreAttempt, sectionNameMap } from './scoring';

const DIFFICULTY_TIME_FACTOR = 2;

/**
 * Builds the demo exam report. All numbers come from deterministic code;
 * the narrative text uses rule-based templates in place of the LLM writer
 * that production will use (MVP doc §6.2).
 */
export function buildExamReport(
  exam: Exam,
  attempt: Attempt,
  opts: { id: string; now?: number; lookup?: (id: string) => Question | undefined } = { id: 'report' },
): ExamReport {
  const lookup = opts.lookup ?? getQuestionById;
  const result = scoreAttempt(attempt.paper, attempt.states, lookup, sectionNameMap(exam));
  const submittedAt = attempt.submittedAt ?? new Date(opts.now ?? Date.now()).toISOString();
  const timeTakenSec = Math.min(
    attempt.durationSec,
    Math.max(0, Math.round((new Date(submittedAt).getTime() - new Date(attempt.startedAt).getTime()) / 1000)),
  );

  return {
    id: opts.id,
    attemptId: attempt.id,
    examId: exam.id,
    examTitle: exam.title,
    createdAt: submittedAt,
    language: attempt.language,
    isDemo: true,
    result,
    timeTakenSec,
    durationSec: attempt.durationSec,
    percentile: estimatePercentile(result.percentage),
    strengths: deriveStrengths(result, lookup),
    weaknesses: deriveWeaknesses(result, lookup),
    loopholes: deriveLoopholes(result, lookup),
    recommendedNextExamId: recommendNextExam(exam, result),
    improvementPlan: buildImprovementPlan(exam, result),
    autoSubmitted: attempt.autoSubmitted,
    isMini: attempt.isMini,
  };
}

export function deriveStrengths(result: ScoreResult, lookup: (id: string) => Question | undefined): string[] {
  const strengths: string[] = [];
  for (const t of result.topics) {
    if (t.total > 0 && t.accuracy >= 75) {
      const qs = result.questions.filter((q) => lookup(q.questionId)?.topic === t.topic);
      const avgTime = qs.reduce((s, q) => s + q.timeSpentSec, 0) / Math.max(qs.length, 1);
      const expected = qs.reduce((s, q) => s + (lookup(q.questionId)?.expectedTimeSec ?? 45), 0) / Math.max(qs.length, 1);
      strengths.push(
        avgTime > 0 && avgTime <= expected
          ? `${t.topic}: ${t.correct}/${t.total} correct and faster than the expected time — keep this as a scoring area.`
          : `${t.topic}: ${t.correct}/${t.total} correct. Accuracy is strong; work on speed to save time for harder sections.`,
      );
    }
  }
  for (const s of result.sections) {
    if (s.correct + s.incorrect >= 2 && s.accuracy >= 80) strengths.push(`${s.name}: ${s.accuracy}% accuracy across attempted questions.`);
  }
  if (strengths.length === 0)
    strengths.push('You attempted the paper under timed conditions — that baseline is what the next mocks will improve on.');
  return strengths.slice(0, 5);
}

export function deriveWeaknesses(result: ScoreResult, lookup: (id: string) => Question | undefined): WeaknessItem[] {
  return result.topics
    .filter((t) => t.accuracy < 60)
    .sort((a, b) => a.accuracy - b.accuracy)
    .slice(0, 5)
    .map((t) => {
      const evidence = result.questions
        .filter((q) => lookup(q.questionId)?.topic === t.topic && q.outcome !== 'correct')
        .map((q) => q.questionId);
      const skipped = result.questions.filter(
        (q) => lookup(q.questionId)?.topic === t.topic && q.outcome === 'unanswered',
      ).length;
      return {
        topic: t.topic,
        accuracy: t.accuracy,
        evidenceQuestionIds: evidence,
        note:
          skipped === t.total
            ? `All ${t.total} ${t.topic} question(s) were skipped. Revise the core formulae and attempt at least the easy ones next time.`
            : `${t.correct}/${t.total} correct. Review the explanations for the linked questions and practise 15 targeted questions.`,
      };
    });
}

export function deriveLoopholes(result: ScoreResult, lookup: (id: string) => Question | undefined): Loophole[] {
  const loopholes: Loophole[] = [];
  const wrongEasy = result.questions.filter(
    (q) => q.outcome === 'incorrect' && lookup(q.questionId)?.difficulty === 'Easy',
  );
  if (wrongEasy.length > 0)
    loopholes.push({
      title: 'Careless errors on easy questions',
      detail: `${wrongEasy.length} easy question(s) were answered incorrectly. Re-read the question stem and verify units before confirming.`,
      marksImpact: wrongEasy.reduce((s, q) => s + q.maxMarks - q.marksAwarded, 0),
    });
  if (result.negativeMarksLost > 0)
    loopholes.push({
      title: 'Negative marking from guesses',
      detail: `You lost ${result.negativeMarksLost} mark(s) to negative marking. Guess only when you can eliminate at least two options.`,
      marksImpact: result.negativeMarksLost,
    });
  const timeSinks = result.questions.filter((q) => {
    const expected = lookup(q.questionId)?.expectedTimeSec ?? 45;
    return q.timeSpentSec > expected * DIFFICULTY_TIME_FACTOR;
  });
  if (timeSinks.length > 0)
    loopholes.push({
      title: 'Time sinks',
      detail: `${timeSinks.length} question(s) took more than twice the expected time. Use the two-pass strategy: skip after 90 seconds, return later.`,
      marksImpact: 0,
    });
  for (const s of result.sections) {
    if (s.unanswered > 0 && s.unanswered === s.correct + s.incorrect + s.unanswered)
      loopholes.push({
        title: `Skipped the entire ${s.name} section`,
        detail: 'Leaving a whole section blank risks the sectional cut-off. Attempt at least the easiest questions in every section.',
        marksImpact: s.maxScore,
      });
  }
  return loopholes;
}

export function recommendNextExam(exam: Exam, result: ScoreResult): string {
  if (result.percentage < 40) return exam.id;
  const sameCategory = EXAMS.filter((e) => e.category === exam.category && e.id !== exam.id && e.status === 'published');
  return sameCategory[0]?.id ?? exam.id;
}

export function buildImprovementPlan(exam: Exam, result: ScoreResult): DayPlan[] {
  const weak = result.topics.filter((t) => t.accuracy < 60).map((t) => t.topic);
  const strong = result.topics.filter((t) => t.accuracy >= 75).map((t) => t.topic);
  const w = (i: number) => weak[i % Math.max(weak.length, 1)] ?? 'mixed practice';
  return [
    { day: 1, title: `Fix ${w(0)}`, minutes: 45, tasks: [`Re-read explanations for every ${w(0)} question you missed`, `Solve 15 ${w(0)} questions untimed`, 'Write down the formula or rule you forgot'] },
    { day: 2, title: `Strengthen ${w(1)}`, minutes: 45, tasks: [`Learn 2 shortcuts for ${w(1)}`, `Solve 15 ${w(1)} questions with a 60-second limit each`] },
    { day: 3, title: 'Timed sectional test', minutes: 40, tasks: [`Take a 20-question sectional on ${exam.sections[0]?.name ?? 'your weakest section'}`, 'Mark questions taking more than 90 seconds'] },
    { day: 4, title: `Revise ${w(2)}`, minutes: 40, tasks: [`Practise 20 mixed-difficulty ${w(2)} questions`, 'Focus on elimination when unsure'] },
    { day: 5, title: 'Speed and accuracy drill', minutes: 30, tasks: [strong[0] ? `Maintain ${strong[0]}: 10 quick questions` : 'Solve 20 easy questions under 30 seconds each', 'Avoid guesses without eliminating two options'] },
    { day: 6, title: 'Full-length mock', minutes: exam.durationMin, tasks: [`Attempt a full ${exam.shortTitle} mock in one sitting`, 'Use the two-pass strategy'] },
    { day: 7, title: 'Review and plan', minutes: 30, tasks: ['Compare this week’s report with the previous one', 'Choose next week’s three focus topics'] },
  ];
}
