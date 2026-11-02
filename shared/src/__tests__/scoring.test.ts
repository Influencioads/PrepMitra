import { describe, expect, it } from 'vitest';
import type { Attempt, PaperQuestion, QuestionState } from '../types/core';
import { evaluateAnswer, estimatePercentile, scoreAttempt } from '../logic/scoring';
import { createDemoAttempt, buildDemoPaper } from '../logic/paper';
import { buildExamReport } from '../logic/report';
import { getExamById } from '../mocks/exams';
import { getQuestionById, QUESTION_BANK } from '../mocks/questions';

const single = getQuestionById('q-quant-2')!; // correct: b
const multi = getQuestionById('q-quant-8')!; // correct: a, c
const numeric = getQuestionById('q-quant-7')!; // 3200
const numericTol = getQuestionById('q-ece-2')!; // 2 ± 0.01

describe('evaluateAnswer', () => {
  it('handles single-correct MCQs', () => {
    expect(evaluateAnswer(single, { selectedOptionIds: ['q-quant-2-b'] })).toBe('correct');
    expect(evaluateAnswer(single, { selectedOptionIds: ['q-quant-2-a'] })).toBe('incorrect');
    expect(evaluateAnswer(single, undefined)).toBe('unanswered');
    expect(evaluateAnswer(single, { selectedOptionIds: [] })).toBe('unanswered');
  });

  it('scores multiple-correct as all-or-nothing, order independent', () => {
    expect(evaluateAnswer(multi, { selectedOptionIds: ['q-quant-8-c', 'q-quant-8-a'] })).toBe('correct');
    expect(evaluateAnswer(multi, { selectedOptionIds: ['q-quant-8-a'] })).toBe('incorrect');
    expect(evaluateAnswer(multi, { selectedOptionIds: ['q-quant-8-a', 'q-quant-8-b', 'q-quant-8-c'] })).toBe('incorrect');
  });

  it('scores numeric answers with tolerance', () => {
    expect(evaluateAnswer(numeric, { numericValue: '3200' })).toBe('correct');
    expect(evaluateAnswer(numeric, { numericValue: '3200.0' })).toBe('correct');
    expect(evaluateAnswer(numeric, { numericValue: '3201' })).toBe('incorrect');
    expect(evaluateAnswer(numeric, { numericValue: '' })).toBe('unanswered');
    expect(evaluateAnswer(numeric, { numericValue: 'abc' })).toBe('unanswered');
    expect(evaluateAnswer(numericTol, { numericValue: '2.005' })).toBe('correct');
    expect(evaluateAnswer(numericTol, { numericValue: '2.05' })).toBe('incorrect');
  });
});

describe('scoreAttempt', () => {
  const paper: PaperQuestion[] = [
    { questionId: single.id, sectionId: 's1', marks: 2, negativeMarks: 0.5 },
    { questionId: multi.id, sectionId: 's1', marks: 2, negativeMarks: 0.5 },
    { questionId: numeric.id, sectionId: 's2', marks: 2, negativeMarks: 0.5 },
    { questionId: 'q-reas-1', sectionId: 's2', marks: 2, negativeMarks: 0.5 },
  ];
  const st = (answer?: QuestionState['answer'], time = 30): QuestionState => ({ visited: true, marked: false, answer, timeSpentSec: time });
  const states: Record<string, QuestionState> = {
    [single.id]: st({ selectedOptionIds: ['q-quant-2-b'] }),
    [multi.id]: st({ selectedOptionIds: ['q-quant-8-a'] }),
    [numeric.id]: st({ numericValue: '100' }),
    'q-reas-1': st(undefined),
  };

  it('applies marks and negative marking only to single-correct MCQs', () => {
    const r = scoreAttempt(paper, states, getQuestionById, { s1: 'Section 1', s2: 'Section 2' });
    expect(r.correct).toBe(1);
    expect(r.incorrect).toBe(2);
    expect(r.unanswered).toBe(1);
    // +2 (single) + 0 (wrong MSQ, no negative) + 0 (wrong NAT, no negative)
    expect(r.score).toBe(2);
    expect(r.negativeMarksLost).toBe(0);
    expect(r.maxScore).toBe(8);
    expect(r.accuracy).toBe(33);
    expect(r.sections.find((s) => s.sectionId === 's1')?.name).toBe('Section 1');
  });

  it('deducts negative marks for a wrong single-correct answer', () => {
    const r = scoreAttempt(paper, { ...states, [single.id]: st({ selectedOptionIds: ['q-quant-2-a'] }) }, getQuestionById);
    expect(r.score).toBe(-0.5);
    expect(r.negativeMarksLost).toBe(0.5);
    expect(r.percentage).toBe(0);
  });

  it('computes topic accuracy', () => {
    const r = scoreAttempt(paper, states, getQuestionById);
    expect(r.topics.find((t) => t.topic === 'Profit and Loss')?.accuracy).toBe(100);
    expect(r.topics.find((t) => t.topic === 'Number Series')?.attempted).toBe(0);
  });
});

describe('demo papers and reports', () => {
  it('builds papers that follow the exam sections and allowed question types', () => {
    const exam = getExamById('ssc-cgl')!;
    const paper = buildDemoPaper(exam, 'seed-x');
    expect(paper).toHaveLength(exam.sections.length * exam.demo.questionsPerSection);
    for (const item of paper) {
      const q = getQuestionById(item.questionId)!;
      expect(exam.questionTypes).toContain(q.type);
      expect(exam.sections.find((s) => s.id === item.sectionId)?.subject).toBe(q.subject);
    }
    expect(new Set(paper.map((p) => p.questionId)).size).toBe(paper.length);
  });

  it('every exam can produce a non-empty demo paper', () => {
    for (const id of ['ssc-cgl', 'ssc-chsl', 'rrb-ntpc', 'ibps-po', 'ibps-clerk', 'sbi-po', 'upsc-prelims', 'cat', 'gate-cse', 'gate-ece', 'cuet-pg', 'general-aptitude', 'it-placement']) {
      const exam = getExamById(id)!;
      expect(buildDemoPaper(exam, 's').length, id).toBeGreaterThan(0);
    }
  });

  it('creates an attempt with a demo end time', () => {
    const exam = getExamById('general-aptitude')!;
    const a: Attempt = createDemoAttempt(exam, { id: 'a1', language: 'en', now: 0 });
    expect(new Date(a.endsAt).getTime()).toBe(exam.demo.durationMin * 60_000);
    expect(a.states[a.paper[0]!.questionId]?.visited).toBe(true);
  });

  it('report weaknesses cite evidence questions', () => {
    const exam = getExamById('general-aptitude')!;
    const a = createDemoAttempt(exam, { id: 'a2', language: 'en', now: 0 });
    const report = buildExamReport(exam, { ...a, submittedAt: new Date(600_000).toISOString() }, { id: 'r1' });
    expect(report.isDemo).toBe(true);
    expect(report.result.unanswered).toBe(a.paper.length);
    for (const w of report.weaknesses) expect(w.evidenceQuestionIds.length).toBeGreaterThan(0);
    expect(report.improvementPlan).toHaveLength(7);
    expect(report.timeTakenSec).toBe(600);
  });

  it('percentile is monotonic and bounded', () => {
    expect(estimatePercentile(10)).toBeLessThan(estimatePercentile(50));
    expect(estimatePercentile(100)).toBeLessThanOrEqual(99.9);
    expect(estimatePercentile(0)).toBeGreaterThanOrEqual(1);
  });

  it('every option question has valid answer keys', () => {
    for (const q of QUESTION_BANK) {
      if (q.type === 'numeric') expect(q.correctNumeric, q.id).toBeTypeOf('number');
      else {
        expect(q.correctOptionIds!.length, q.id).toBeGreaterThan(0);
        for (const c of q.correctOptionIds!) expect(q.options!.some((o) => o.id === c), q.id).toBe(true);
        if (q.type === 'single') expect(q.correctOptionIds).toHaveLength(1);
      }
    }
  });
});

describe('mini mock', () => {
  it('caps the paper at 10 questions across all sections and 30 minutes', async () => {
    const { MINI_MOCK } = await import('../logic/paper');
    const exam = getExamById('ssc-cgl')!;
    const a = createDemoAttempt(exam, { id: 'mini1', language: 'en', now: 0, mini: true });
    expect(a.paper).toHaveLength(MINI_MOCK.maxQuestions);
    expect(a.isMini).toBe(true);
    expect(a.durationSec).toBe(30 * 60);
    expect(new Set(a.paper.map((p) => p.sectionId)).size).toBe(exam.sections.length);
    const full = createDemoAttempt(exam, { id: 'mini1', language: 'en', now: 0 });
    expect(full.paper.length).toBeGreaterThan(a.paper.length);
    expect(full.isMini).toBeUndefined();
  });
});
