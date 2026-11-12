import { describe, expect, it } from 'vitest';
import { classifyAiError, aiError } from '../ai/errors';
import { flowOrder, parseMermaid } from '../ai/mermaid';
import { createMockAiApi, isSupportReply, toChatReply, toCoachReply, toMistakeSummary } from '../ai';

describe('parseMermaid', () => {
  it('reads flowcharts with labels and edge text', () => {
    const p = parseMermaid('```mermaid\ngraph TD\n  A[Original 100] -->|falls 20%| B[80]\n  B --> C(Back to 100)\n```');
    expect(p.kind).toBe('flow');
    if (p.kind !== 'flow') return;
    expect(p.nodes.map((n) => n.label)).toEqual(['Original 100', '80', 'Back to 100']);
    expect(p.edges[0]).toEqual({ from: 'A', to: 'B', label: 'falls 20%' });
    expect(flowOrder(p).map((n) => n.id)).toEqual(['A', 'B', 'C']);
  });

  it('reads one-line graphs and fan-out', () => {
    const p = parseMermaid('graph LR; A & B --> C');
    expect(p.kind === 'flow' && p.direction).toBe('LR');
    expect(p.kind === 'flow' && p.edges.length).toBe(2);
  });

  it('reads mind maps by indentation', () => {
    const p = parseMermaid('mindmap\n  root((Time and work))\n    Rates\n      Add when together\n    LCM method');
    expect(p.kind).toBe('mindmap');
    if (p.kind !== 'mindmap') return;
    expect(p.root.label).toBe('Time and work');
    expect(p.root.children.map((c) => c.label)).toEqual(['Rates', 'LCM method']);
    expect(p.root.children[0]!.children[0]!.label).toBe('Add when together');
  });

  it('returns unknown for other diagrams', () => {
    expect(parseMermaid('pie title X\n "a": 1').kind).toBe('unknown');
    expect(parseMermaid('').kind).toBe('unknown');
  });
});

describe('classifyAiError', () => {
  it('maps backend codes to screen reactions', () => {
    expect(classifyAiError({ status: 402, code: 'ALLOWANCE_EXHAUSTED', message: 'x' }).kind).toBe('upgrade');
    expect(classifyAiError({ status: 402, code: 'plan_required', message: 'x' }).upgradePath).toBe('/subscription');
    expect(classifyAiError({ status: 422, code: 'OFF_TOPIC', message: 'x' }).kind).toBe('off_topic');
    expect(classifyAiError({ status: 503, code: 'AI_UNAVAILABLE', message: '' }).retryable).toBe(true);
    expect(classifyAiError(new Error('boom')).kind).toBe('other');
  });
});

describe('AI adapters', () => {
  it('normalises distress variants', () => {
    expect(isSupportReply({ support: 'call 14416', answer: null })).toBe(true);
    expect(isSupportReply({ answer: 'B', solution: {} })).toBe(false);
    expect(toChatReply({ session_id: 's', reply: 'help text', follow_ups: [], support: true }).support).toBe('help text');
    expect(toCoachReply({ session_id: 's', coach: 'help', step: 'shape', support: true }).support).toBe('help');
  });

  it('reads both mistake-summary shapes', () => {
    const facts = { week: '2026-W46', groups: [], ai: { summary: 'none', patterns: [], this_week: [] } };
    expect(toMistakeSummary(facts).artifactId).toBeUndefined();
    expect(toMistakeSummary({ id: 'a1', title: 'T', payload: facts }).artifactId).toBe('a1');
  });
});

describe('mock AI api', () => {
  const ai = createMockAiApi(0);
  it('solves doubts, returns support on distress and rejects off-topic', async () => {
    const r = await ai.solveDoubt({ text: 'A price falls 20%. What rise restores it?' });
    expect(isSupportReply(r)).toBe(false);
    expect(isSupportReply(await ai.solveDoubt({ text: 'I want to die, nothing works' }))).toBe(true);
    await expect(ai.solveDoubt({ text: 'give me a movie recipe please' })).rejects.toMatchObject({ code: 'OFF_TOPIC' });
  });

  it('meters allowances and returns 402 when one runs out', async () => {
    const before = (await ai.allowances()).limits.find((l) => l.feature === 'doubts')!.remaining;
    await ai.solveDoubt({ text: 'What is 12.5% of 640 exactly?' });
    expect((await ai.allowances()).limits.find((l) => l.feature === 'doubts')!.remaining).toBe(before - 1);
    await expect(ai.ultraReview()).rejects.toMatchObject({ status: 402, code: 'ALLOWANCE_EXHAUSTED' });
  });

  it('runs the cheat code coach end to end', async () => {
    const s = await ai.coachStart(101);
    const r = await ai.coachReply(s.session_id, 'rise = x ÷ (100 − x)');
    expect(r.step).toBe('test');
    const t = await ai.coachTest(s.session_id);
    expect(t.step).toBe('lock');
    const card = await ai.coachLock(s.session_id, true);
    expect((await ai.coachCards())[0]!.id).toBe(card.id);
  });

  it('error helper upper-cases codes like the web client', () => {
    expect(aiError(503, 'ai_unavailable', 'x').code).toBe('AI_UNAVAILABLE');
  });
});
