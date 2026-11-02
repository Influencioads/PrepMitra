import { describe, expect, it } from 'vitest';
import {
  answeredCount, clearResponse, countPaletteStatuses, getPaletteStatus, isAnswered, remainingSeconds, setAnswer,
  toggleMarkForReview, toggleOption, visitQuestion,
} from '../logic/questionState';
import { createDemoAttempt } from '../logic/paper';
import { getExamById } from '../mocks/exams';

describe('palette status', () => {
  it('maps the five CBT states', () => {
    expect(getPaletteStatus(undefined)).toBe('not-visited');
    expect(getPaletteStatus({ visited: false, marked: false, timeSpentSec: 0 })).toBe('not-visited');
    expect(getPaletteStatus({ visited: true, marked: false, timeSpentSec: 0 })).toBe('not-answered');
    expect(getPaletteStatus({ visited: true, marked: false, timeSpentSec: 0, answer: { selectedOptionIds: ['a'] } })).toBe('answered');
    expect(getPaletteStatus({ visited: true, marked: true, timeSpentSec: 0 })).toBe('marked');
    expect(getPaletteStatus({ visited: true, marked: true, timeSpentSec: 0, answer: { numericValue: '4' } })).toBe('answered-marked');
  });

  it('treats blank or invalid numeric input as unanswered', () => {
    expect(isAnswered({ numericValue: '' })).toBe(false);
    expect(isAnswered({ numericValue: '-' })).toBe(false);
    expect(isAnswered({ numericValue: '-2.5' })).toBe(true);
  });
});

describe('attempt transitions', () => {
  const exam = getExamById('general-aptitude')!;
  const base = createDemoAttempt(exam, { id: 'qs', language: 'en', now: 0 });
  const ids = base.paper.map((p) => p.questionId);

  it('visiting marks a question as visited and moves the cursor', () => {
    const a = visitQuestion(base, 2);
    expect(a.currentIndex).toBe(2);
    expect(getPaletteStatus(a.states[ids[2]!])).toBe('not-answered');
  });

  it('answer, mark, clear update palette counts', () => {
    let a = setAnswer(base, ids[0]!, { selectedOptionIds: ['x'] });
    a = toggleMarkForReview(a, ids[1]!);
    let counts = countPaletteStatuses(ids, a.states);
    expect(counts.answered).toBe(1);
    expect(counts.marked).toBe(1);
    expect(counts['not-visited']).toBe(ids.length - 2);
    a = toggleMarkForReview(a, ids[0]!);
    expect(getPaletteStatus(a.states[ids[0]!])).toBe('answered-marked');
    a = clearResponse(a, ids[0]!);
    expect(getPaletteStatus(a.states[ids[0]!])).toBe('marked');
    counts = countPaletteStatuses(ids, a.states);
    expect(counts.marked).toBe(2);
    expect(answeredCount(ids, a.states)).toBe(0);
  });

  it('toggleOption replaces for single and toggles for multiple', () => {
    expect(toggleOption({ selectedOptionIds: ['a'] }, 'b', false).selectedOptionIds).toEqual(['b']);
    expect(toggleOption({ selectedOptionIds: ['a'] }, 'b', true).selectedOptionIds).toEqual(['a', 'b']);
    expect(toggleOption({ selectedOptionIds: ['a', 'b'] }, 'a', true).selectedOptionIds).toEqual(['b']);
  });

  it('remainingSeconds never goes negative', () => {
    expect(remainingSeconds({ endsAt: new Date(10_000).toISOString() }, 4_000)).toBe(6);
    expect(remainingSeconds({ endsAt: new Date(10_000).toISOString() }, 20_000)).toBe(0);
  });
});
