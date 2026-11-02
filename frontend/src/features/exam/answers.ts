import type { Answer, Question } from '@prepmitra/shared';
import { isAnswered } from '@prepmitra/shared';

const letter = (q: Question, optionId: string) => {
  const i = q.options?.findIndex((o) => o.id === optionId) ?? -1;
  return i >= 0 ? String.fromCharCode(65 + i) : '?';
};

/** Human-readable answer, e.g. "B" or "A, C" or "3200". */
export function describeAnswer(q: Question, answer?: Answer): string {
  if (!isAnswered(answer)) return 'Not answered';
  if (q.type === 'numeric') return answer!.numericValue!.trim();
  return (answer!.selectedOptionIds ?? []).map((id) => letter(q, id)).sort().join(', ');
}

export function describeCorrect(q: Question): string {
  if (q.type === 'numeric') return `${q.correctNumeric}${q.tolerance ? ` (±${q.tolerance})` : ''}`;
  return (q.correctOptionIds ?? []).map((id) => letter(q, id)).sort().join(', ');
}

/** Short axis label for charts, e.g. "General Intelligence & Reasoning" → "General Intel…". */
export const shortLabel = (name: string, max = 14) => (name.length > max ? `${name.slice(0, max - 1).trimEnd()}…` : name);
