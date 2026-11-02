import type {
  DayPlan, InterviewConfig, InterviewQuestionFeedback, InterviewReport, InterviewRole, InterviewScores,
  InterviewSession, InterviewTurn, ScriptedQuestion,
} from '../types/core';
import { INTERVIEW_SCRIPTS } from '../mocks/interviews';

const MAX_FOLLOW_UPS = 2;
const FILLERS = ['um', 'uh', 'like', 'basically', 'actually', 'you know', 'so yeah', 'kind of'];
const STRUCTURE_MARKERS = ['first', 'second', 'then', 'finally', 'because', 'for example', 'result', 'situation', 'task', 'action', 'so that', 'which led'];

export const getScript = (roleId: string): ScriptedQuestion[] => INTERVIEW_SCRIPTS[roleId] ?? INTERVIEW_SCRIPTS['software-developer']!;

const turnId = (session: Pick<InterviewSession, 'id' | 'turns'>) => `${session.id}-t${session.turns.length + 1}`;

/** Starts a scripted demo interview with the interviewer's first question. */
export function startInterview(config: InterviewConfig, opts: { id: string; now?: number }): InterviewSession {
  const now = new Date(opts.now ?? Date.now()).toISOString();
  const script = getScript(config.roleId);
  const queue = script.map((q) => q.id);
  const first = script[0]!;
  const greeting =
    config.level === 'fresher'
      ? 'Hello, and thanks for joining. This is a practice interview for a fresher position. '
      : 'Hello, and thanks for joining. This is a practice interview for an experienced position. ';
  const session: InterviewSession = {
    id: opts.id,
    config,
    status: 'in-progress',
    turns: [],
    questionQueue: queue,
    askedCount: 1,
    followUpsAsked: 0,
    startedAt: now,
  };
  session.turns.push({
    id: turnId(session), speaker: 'interviewer', stage: first.stage, questionId: first.id, at: now,
    text: greeting + first.text,
  });
  return session;
}

export const currentInterviewerTurn = (session: InterviewSession): InterviewTurn | undefined =>
  [...session.turns].reverse().find((t) => t.speaker === 'interviewer');

/** True once the closing question has been answered (the farewell turn has no questionId). */
export function isInterviewFinished(session: InterviewSession): boolean {
  if (session.status === 'completed') return true;
  const last = session.turns[session.turns.length - 1];
  return !!last && last.speaker === 'interviewer' && last.stage === 'closing' && !last.questionId;
}

export const wordCount = (text: string) => text.trim().split(/\s+/).filter(Boolean).length;

/**
 * Records the candidate's answer and appends the next scripted interviewer
 * turn. Follow-ups are triggered by keywords in the answer (or by a very short
 * technical answer), capped at two per interview.
 */
export function submitAnswer(
  session: InterviewSession,
  answer: string,
  opts: { now?: number; durationSec?: number } = {},
): InterviewSession {
  if (session.status === 'completed') return session;
  const now = new Date(opts.now ?? Date.now()).toISOString();
  const script = getScript(session.config.roleId);
  const asked = currentInterviewerTurn(session);
  const askedQ = script.find((q) => q.id === asked?.questionId);
  const next: InterviewSession = { ...session, turns: [...session.turns] };
  next.turns.push({
    id: turnId(next), speaker: 'candidate', text: answer.trim(), stage: asked?.stage ?? 'introduction',
    questionId: asked?.questionId, at: now, durationSec: opts.durationSec,
  });

  if (asked?.stage === 'closing') {
    next.turns.push({
      id: turnId(next), speaker: 'interviewer', stage: 'closing', at: now,
      text: 'Thank you for your time today. That concludes the interview. Select “End interview” to see your report.',
    });
    return next;
  }

  const lower = answer.toLowerCase();
  if (askedQ && !asked?.isFollowUp && next.followUpsAsked < MAX_FOLLOW_UPS) {
    const triggered = askedQ.followUp && askedQ.followUp.trigger.some((t) => lower.includes(t));
    const tooShort = (askedQ.stage === 'technical' || askedQ.stage === 'situational') && wordCount(answer) < 20;
    if (triggered || tooShort) {
      const text = triggered
        ? askedQ.followUp!.text
        : 'That is a good start. Could you make it more specific with a concrete example from your own experience?';
      next.followUpsAsked += 1;
      next.turns.push({
        id: turnId(next), speaker: 'interviewer', stage: askedQ.stage, questionId: askedQ.id, isFollowUp: true, at: now, text,
      });
      return next;
    }
  }

  const idx = askedQ ? script.findIndex((q) => q.id === askedQ.id) : -1;
  const nextQ = script[idx + 1];
  if (!nextQ) return next;
  next.askedCount += 1;
  const bridge = wordCount(answer) > 40 ? 'Thanks, that was detailed. ' : 'Thank you. ';
  next.turns.push({
    id: turnId(next), speaker: 'interviewer', stage: nextQ.stage, questionId: nextQ.id, at: now, text: bridge + nextQ.text,
  });
  return next;
}

export function endInterview(session: InterviewSession, now: number = Date.now()): InterviewSession {
  return { ...session, status: 'completed', endedAt: new Date(now).toISOString() };
}

export const interviewProgress = (session: InterviewSession): { asked: number; total: number } => ({
  asked: Math.min(session.askedCount, getScript(session.config.roleId).length),
  total: getScript(session.config.roleId).length,
});

const clamp10 = (n: number) => Math.max(1, Math.min(10, Math.round(n * 10) / 10));

function scoreAnswer(q: ScriptedQuestion, answer: string) {
  const lower = answer.toLowerCase();
  const words = wordCount(answer);
  const hits = q.keywords.filter((k) => lower.includes(k)).length;
  const keywordRatio = q.keywords.length ? hits / q.keywords.length : 0;
  const structure = STRUCTURE_MARKERS.filter((m) => lower.includes(m)).length;
  const lengthScore = words < 10 ? 2 : words < 25 ? 5 : words < 120 ? 8.5 : 7;
  return { words, hits, keywordRatio, structure, lengthScore };
}

/** Builds the demo interview report from the transcript using transparent rules. */
export function buildInterviewReport(
  session: InterviewSession,
  role: InterviewRole,
  opts: { id: string; now?: number },
): InterviewReport {
  const script = getScript(session.config.roleId);
  const answers = session.turns.filter((t) => t.speaker === 'candidate' && t.questionId);
  const byQuestion = new Map<string, string>();
  for (const a of answers) byQuestion.set(a.questionId!, `${byQuestion.get(a.questionId!) ?? ''} ${a.text}`.trim());

  const feedback: InterviewQuestionFeedback[] = [];
  let kw = 0, st = 0, len = 0, n = 0;
  for (const q of script) {
    const answer = byQuestion.get(q.id);
    if (!answer) continue;
    const s = scoreAnswer(q, answer);
    kw += s.keywordRatio; st += Math.min(s.structure, 4) / 4; len += s.lengthScore; n += 1;
    const missingKeywords = q.keywords.filter((k) => !answer.toLowerCase().includes(k)).slice(0, 3);
    feedback.push({
      questionId: q.id,
      question: q.text,
      answer,
      score: clamp10(2 + s.keywordRatio * 5 + Math.min(s.structure, 3) * 0.6 + (s.lengthScore / 10) * 1.5),
      good:
        s.hits > 0
          ? `You covered ${s.hits} key point(s)${s.structure > 0 ? ' and used clear signposting' : ''}.`
          : s.words >= 25
            ? 'You gave a complete answer with enough detail to follow.'
            : 'You stayed on topic.',
      missing:
        missingKeywords.length > 0
          ? `Consider mentioning: ${missingKeywords.join(', ')}.${s.words < 25 ? ' Add a specific example to make it credible.' : ''}`
          : 'Strong coverage — tighten the answer to under 90 seconds.',
      modelAnswer: q.modelAnswer,
    });
  }

  const avgKw = n ? kw / n : 0;
  const avgSt = n ? st / n : 0;
  const avgLen = n ? len / n : 0;
  const totalWords = answers.reduce((s, a) => s + wordCount(a.text), 0);
  const allText = answers.map((a) => a.text.toLowerCase()).join(' ');
  const fillerCount = FILLERS.reduce((s, f) => s + (allText.match(new RegExp(`\\b${f}\\b`, 'g'))?.length ?? 0), 0);
  const resumeAnswered = byQuestion.has(script.find((q) => q.stage === 'resume')?.id ?? '');
  const completion = n / script.length;

  const scores: InterviewScores = {
    roleKnowledge: clamp10(2 + avgKw * 10 + completion * 1.5),
    answerStructure: clamp10(3 + avgSt * 6 + (avgLen / 10) * 1.5),
    communication: clamp10(3 + (avgLen / 10) * 5 - Math.min(fillerCount, 10) * 0.2 + completion),
    confidence: clamp10(3.5 + (avgLen / 10) * 4 + completion * 1.5 - Math.min(fillerCount, 10) * 0.15),
    resumeConsistency: clamp10(session.config.resumeFileName ? (resumeAnswered ? 7.5 : 4) : resumeAnswered ? 6 : 3),
  };
  const overall = clamp10(
    (scores.roleKnowledge + scores.answerStructure + scores.communication + scores.confidence + scores.resumeConsistency) / 5,
  );

  const strengths: string[] = [];
  const weaknesses: string[] = [];
  const redFlags: string[] = [];
  if (scores.roleKnowledge >= 6.5) strengths.push('Good command of role-specific concepts and terminology.');
  else weaknesses.push(`Role knowledge needs depth — revise ${role.themes.slice(0, 2).join(' and ')}.`);
  if (scores.answerStructure >= 6.5) strengths.push('Answers were structured and easy to follow.');
  else weaknesses.push('Use the STAR format (Situation, Task, Action, Result) for experience-based questions.');
  if (scores.communication >= 6.5) strengths.push('Clear communication with appropriate answer length.');
  else weaknesses.push('Several answers were too short to show your thinking — aim for 45–90 seconds each.');
  if (fillerCount > 4) weaknesses.push(`Frequent filler words (${fillerCount}) can reduce perceived confidence.`);
  if (completion < 0.6) redFlags.push('Interview ended before most questions were answered.');
  if (answers.some((a) => wordCount(a.text) < 5)) redFlags.push('One-line answers would be noticed by a panel as lack of preparation.');
  if (!session.config.resumeFileName) weaknesses.push('No resume attached — resume-based questions were generic. Attach one next time.');
  if (strengths.length === 0) strengths.push('You completed a timed practice interview — a solid baseline for improvement.');

  const startedMs = new Date(session.startedAt).getTime();
  const endedMs = new Date(session.endedAt ?? new Date(opts.now ?? Date.now()).toISOString()).getTime();
  const durationSec = Math.max(0, Math.round((endedMs - startedMs) / 1000));
  const speakingSec = answers.reduce((s, a) => s + (a.durationSec ?? 0), 0);

  return {
    id: opts.id,
    sessionId: session.id,
    roleId: role.id,
    roleTitle: role.title,
    level: session.config.level,
    mode: session.config.mode,
    language: session.config.language,
    createdAt: new Date(opts.now ?? Date.now()).toISOString(),
    isDemo: true,
    scores,
    overall,
    voiceMetrics:
      session.config.mode === 'voice'
        ? { wordsPerMinute: speakingSec > 0 ? Math.round((totalWords / speakingSec) * 60) : 0, fillerWords: fillerCount }
        : undefined,
    strengths,
    weaknesses,
    redFlags,
    questionFeedback: feedback,
    plan: buildInterviewPlan(role, scores),
    durationSec,
  };
}

export function buildInterviewPlan(role: InterviewRole, scores: InterviewScores): DayPlan[] {
  const weakest = (Object.entries(scores) as [keyof InterviewScores, number][]).sort((a, b) => a[1] - b[1])[0]![0];
  const label: Record<keyof InterviewScores, string> = {
    roleKnowledge: 'role knowledge', answerStructure: 'answer structure', communication: 'communication',
    confidence: 'confidence', resumeConsistency: 'resume storytelling',
  };
  return [
    { day: 1, title: `Focus on ${label[weakest]}`, minutes: 30, tasks: ['Re-read the model answers in this report', `Write 3 answers that fix your ${label[weakest]} gaps`] },
    { day: 2, title: 'Build your STAR bank', minutes: 40, tasks: ['Prepare 5 STAR stories: challenge, failure, teamwork, leadership, conflict', 'Keep each under 90 seconds'] },
    { day: 3, title: `${role.themes[0]} deep-dive`, minutes: 45, tasks: [`Revise core ${role.themes[0]} concepts`, 'Explain two concepts aloud as if to a panel'] },
    { day: 4, title: 'Record and review', minutes: 30, tasks: ['Record yourself answering 3 questions', 'Count filler words and pauses'] },
    { day: 5, title: `${role.themes[1] ?? 'Role'} practice`, minutes: 40, tasks: [`Practise 5 ${role.themes[1] ?? 'role'} questions`, 'Add numbers or outcomes to every answer'] },
    { day: 6, title: 'Mock interview', minutes: role.durationMin, tasks: [`Take another ${role.shortTitle} mock interview`, 'Try voice mode if you used text'] },
    { day: 7, title: 'Compare and plan', minutes: 20, tasks: ['Compare both reports', 'Pick the next two improvement areas'] },
  ];
}
