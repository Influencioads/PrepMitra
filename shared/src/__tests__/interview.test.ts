import { describe, expect, it } from 'vitest';
import { buildInterviewReport, endInterview, isInterviewFinished, startInterview, submitAnswer } from '../logic/interview';
import { getRoleById, INTERVIEW_SCRIPTS } from '../mocks/interviews';
import { createSeedInterview } from '../mocks/user';

describe('scripted interview engine', () => {
  it('starts with the introduction question', () => {
    const s = startInterview({ roleId: 'software-developer', level: 'fresher', language: 'en', mode: 'text' }, { id: 'i1', now: 0 });
    expect(s.turns).toHaveLength(1);
    expect(s.turns[0]!.stage).toBe('introduction');
  });

  it('asks a follow-up when a trigger keyword appears, capped at two', () => {
    let s = startInterview({ roleId: 'software-developer', level: 'fresher', language: 'en', mode: 'text' }, { id: 'i2', now: 0 });
    s = submitAnswer(s, 'I built a project during my internship.', { now: 1000 });
    expect(s.turns.at(-1)!.isFollowUp).toBe(true);
    expect(s.followUpsAsked).toBe(1);
    s = submitAnswer(s, 'The hardest part was caching.', { now: 2000 });
    expect(s.turns.at(-1)!.isFollowUp).toBeFalsy();
    expect(s.turns.at(-1)!.stage).toBe('resume');
  });

  it('runs to completion and produces a bounded report', () => {
    const { session, report } = createSeedInterview();
    expect(isInterviewFinished(session)).toBe(true);
    expect(report.questionFeedback.length).toBeGreaterThan(4);
    for (const v of Object.values(report.scores)) {
      expect(v).toBeGreaterThanOrEqual(1);
      expect(v).toBeLessThanOrEqual(10);
    }
    expect(report.plan).toHaveLength(7);
    expect(session.followUpsAsked).toBeGreaterThanOrEqual(1);
  });

  it('ending early still produces a report with red flags', () => {
    const role = getRoleById('hr-executive')!;
    let s = startInterview({ roleId: role.id, level: 'fresher', language: 'en', mode: 'voice' }, { id: 'i3', now: 0 });
    s = submitAnswer(s, 'Hi', { now: 1000, durationSec: 2 });
    s = endInterview(s, 60_000);
    const r = buildInterviewReport(s, role, { id: 'r', now: 60_000 });
    expect(r.redFlags.length).toBeGreaterThan(0);
    expect(r.voiceMetrics).toBeDefined();
  });

  it('every role has a script ending in closing', () => {
    for (const [id, script] of Object.entries(INTERVIEW_SCRIPTS)) {
      expect(script.at(-1)!.stage, id).toBe('closing');
      expect(script[0]!.stage, id).toBe('introduction');
    }
  });
});
