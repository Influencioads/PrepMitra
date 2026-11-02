import type { Exam, Recommendation, SubscriptionState, UserProfile } from '@prepmitra/shared';
import { EXAMS, getExamById, getRoleById } from '@prepmitra/shared';
import type { useProgress } from '@/hooks/useProgress';

type Progress = ReturnType<typeof useProgress>;

/** Personalised next steps — same rules as the web dashboard. */
export function buildRecommendations(p: Progress, sub: SubscriptionState, profile: UserProfile): Recommendation[] {
  const recs: Recommendation[] = [];
  if (!sub.freeMiniMockUsed)
    recs.push({ id: 'free', title: 'Take your free mini mock', reason: '30 minutes, full report — see where you stand today.', examId: 'general-aptitude', minutes: 30 });
  for (const w of p.weak.slice(0, 2)) {
    const exam = p.reports.find((r) => r.result.topics.some((t) => t.topic === w.topic));
    recs.push({ id: `w-${w.topic}`, title: `${w.topic} practice`, reason: `Mastery ${w.mastery}% across ${w.attempts} questions — your biggest opportunity.`, topic: w.topic, examId: exam?.examId, minutes: 20 });
  }
  const last = p.history[0];
  if (last) {
    const next = p.reports.find((r) => r.id === last.reportId)?.recommendedNextExamId;
    if (next)
      recs.push({ id: 'next', title: `${getExamById(next)?.shortTitle ?? 'Next'} full mock`, reason: 'Recommended by your latest report.', examId: next, minutes: getExamById(next)?.durationMin ?? 60 });
  }
  for (const roleId of profile.targetRoleIds.slice(0, 1)) {
    recs.push({ id: `r-${roleId}`, title: `${getRoleById(roleId)?.shortTitle ?? 'Role'} mock interview`, reason: 'Matches your target role.', roleId, minutes: getRoleById(roleId)?.durationMin ?? 20 });
  }
  return recs.slice(0, 4);
}

export const recommendationHref = (r: Recommendation) =>
  r.roleId ? `/interviews/${r.roleId}` : r.examId ? `/exams/${r.examId}` : '/explore';

/** Target exams first, then the most popular published exams. */
export function recommendedExams(profile: UserProfile, count = 3): Exam[] {
  const targets = profile.targetExamIds.map((id) => getExamById(id)).filter((e): e is Exam => !!e && e.status === 'published');
  const fallback = EXAMS.filter((e) => e.status === 'published').sort((a, b) => b.popularity - a.popularity);
  return [...targets, ...fallback.filter((e) => !targets.includes(e))].slice(0, count);
}
