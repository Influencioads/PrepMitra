import type { ExamReport, InterviewReport, User, UserProfile, UserSettings, AttemptSummary } from '@prepmitra/shared';
import {
  APP_NAME, DISCLAIMERS, EXPERIENCE_LEVELS, formatDate, formatDuration, getExamById, getRoleById, languageName,
} from '@prepmitra/shared';

/**
 * Plain-text report summaries for the native Share sheet. Production would
 * share a server-generated PDF link instead.
 */
export function examReportText(r: ExamReport): string {
  const lines = [
    `${APP_NAME} — ${r.examTitle}`,
    `Date: ${formatDate(r.createdAt)}`,
    '',
    `Score: ${r.result.score}/${r.result.maxScore} (${r.result.percentage}%)`,
    `Accuracy: ${r.result.accuracy}% · Percentile (est.): ${r.percentile}`,
    `Correct ${r.result.correct} · Incorrect ${r.result.incorrect} · Unanswered ${r.result.unanswered}`,
    `Time taken: ${formatDuration(r.timeTakenSec)} of ${formatDuration(r.durationSec)}`,
    '',
    'Sections:',
    ...r.result.sections.map((s) => `• ${s.name}: ${s.score}/${s.maxScore} (${s.accuracy}% accuracy)`),
    '',
    'Strengths:',
    ...r.strengths.map((s) => `• ${s}`),
    '',
    'Needs work:',
    ...(r.weaknesses.length ? r.weaknesses.map((w) => `• ${w.topic} (${w.accuracy}%): ${w.note}`) : ['• No weak topics detected.']),
    '',
    '7-day plan:',
    ...r.improvementPlan.map((d) => `Day ${d.day}: ${d.title} — ${d.tasks.join('; ')}`),
    '',
    DISCLAIMERS.demoAi,
  ];
  return lines.join('\n');
}

export function interviewReportText(r: InterviewReport): string {
  const s = r.scores;
  const level = EXPERIENCE_LEVELS.find((l) => l.value === r.level)?.label ?? r.level;
  const lines = [
    `${APP_NAME} — ${r.roleTitle} mock interview`,
    `${formatDate(r.createdAt)} · ${level} · ${r.mode === 'voice' ? 'Voice' : 'Text'} · ${languageName(r.language)}`,
    '',
    `Overall: ${r.overall}/10`,
    `Role knowledge ${s.roleKnowledge} · Structure ${s.answerStructure} · Communication ${s.communication} · Confidence ${s.confidence} · Resume consistency ${s.resumeConsistency}`,
    ...(r.voiceMetrics ? [`Pace: ${r.voiceMetrics.wordsPerMinute} wpm · Filler words: ${r.voiceMetrics.fillerWords}`] : []),
    '',
    'Strengths:',
    ...r.strengths.map((x) => `• ${x}`),
    '',
    'To improve:',
    ...r.weaknesses.map((x) => `• ${x}`),
    ...(r.redFlags.length ? ['', 'Red flags:', ...r.redFlags.map((x) => `• ${x}`)] : []),
    '',
    '7-day plan:',
    ...r.plan.map((d) => `Day ${d.day}: ${d.title} — ${d.tasks.join('; ')}`),
    '',
    DISCLAIMERS.demoInterview,
  ];
  return lines.join('\n');
}

/** "Download my data" export (DPDP data-portability). Shared as JSON text. */
export function personalDataExport(input: {
  user: User | null;
  profile: UserProfile;
  settings: UserSettings;
  history: AttemptSummary[];
  interviewReports: InterviewReport[];
  credits: number;
}): string {
  return JSON.stringify(
    {
      exportedAt: new Date().toISOString(),
      note: 'Prototype export generated on this device from demo data.',
      user: input.user,
      profile: {
        ...input.profile,
        targetExams: input.profile.targetExamIds.map((id) => getExamById(id)?.shortTitle ?? id),
        targetRoles: input.profile.targetRoleIds.map((id) => getRoleById(id)?.shortTitle ?? id),
      },
      settings: input.settings,
      credits: input.credits,
      examHistory: input.history,
      interviews: input.interviewReports.map((r) => ({ id: r.id, role: r.roleTitle, overall: r.overall, date: r.createdAt })),
    },
    null,
    2,
  );
}
