import type { Answer, Attempt, PaletteStatus, QuestionState } from '../types/core';

export const emptyState = (): QuestionState => ({ visited: false, marked: false, timeSpentSec: 0 });

/** True when the answer has a usable value for its question type. */
export function isAnswered(answer?: Answer): boolean {
  if (!answer) return false;
  if (answer.selectedOptionIds && answer.selectedOptionIds.length > 0) return true;
  if (answer.numericValue !== undefined && answer.numericValue.trim() !== '' && answer.numericValue.trim() !== '-')
    return !Number.isNaN(Number(answer.numericValue));
  return false;
}

/** Maps a question's state to the five CBT palette statuses. */
export function getPaletteStatus(state?: QuestionState): PaletteStatus {
  if (!state || !state.visited) return 'not-visited';
  const answered = isAnswered(state.answer);
  if (state.marked && answered) return 'answered-marked';
  if (state.marked) return 'marked';
  if (answered) return 'answered';
  return 'not-answered';
}

export type PaletteCounts = Record<PaletteStatus, number>;

export function countPaletteStatuses(questionIds: string[], states: Record<string, QuestionState>): PaletteCounts {
  const counts: PaletteCounts = { 'not-visited': 0, 'not-answered': 0, answered: 0, marked: 0, 'answered-marked': 0 };
  for (const id of questionIds) counts[getPaletteStatus(states[id])] += 1;
  return counts;
}

/** Answered includes answered-and-marked (those are evaluated on submit, per CBT convention). */
export function answeredCount(questionIds: string[], states: Record<string, QuestionState>): number {
  return questionIds.filter((id) => isAnswered(states[id]?.answer)).length;
}

// ---- Pure state transitions (used by web + mobile stores) ----
const withState = (attempt: Attempt, qid: string, patch: Partial<QuestionState>): Attempt => ({
  ...attempt,
  states: { ...attempt.states, [qid]: { ...(attempt.states[qid] ?? emptyState()), ...patch } },
});

export function visitQuestion(attempt: Attempt, index: number): Attempt {
  const item = attempt.paper[index];
  if (!item) return attempt;
  return { ...withState(attempt, item.questionId, { visited: true }), currentIndex: index };
}

export function setAnswer(attempt: Attempt, qid: string, answer: Answer | undefined): Attempt {
  return withState(attempt, qid, { visited: true, answer });
}

/** Toggles an option. Single-correct replaces; multiple-correct adds/removes. */
export function toggleOption(current: Answer | undefined, optionId: string, multiple: boolean): Answer {
  const selected = current?.selectedOptionIds ?? [];
  if (!multiple) return { selectedOptionIds: [optionId] };
  return {
    selectedOptionIds: selected.includes(optionId) ? selected.filter((o) => o !== optionId) : [...selected, optionId],
  };
}

export function clearResponse(attempt: Attempt, qid: string): Attempt {
  return withState(attempt, qid, { answer: undefined });
}

export function toggleMarkForReview(attempt: Attempt, qid: string): Attempt {
  const current = attempt.states[qid] ?? emptyState();
  return withState(attempt, qid, { visited: true, marked: !current.marked });
}

export function addTimeSpent(attempt: Attempt, qid: string, seconds: number): Attempt {
  const current = attempt.states[qid] ?? emptyState();
  return withState(attempt, qid, { timeSpentSec: current.timeSpentSec + seconds });
}

/** Seconds remaining for a demo attempt based on its client-side end time. */
export function remainingSeconds(attempt: Pick<Attempt, 'endsAt'>, now: number = Date.now()): number {
  return Math.max(0, Math.round((new Date(attempt.endsAt).getTime() - now) / 1000));
}
