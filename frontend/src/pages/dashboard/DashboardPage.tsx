import { useMemo } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight, BookOpen, ClipboardList, Coins, Flame, Lightbulb, MessageSquare, Play, Target, TrendingDown, TrendingUp, Trophy,
} from 'lucide-react';
import type { Recommendation } from '@prepmitra/shared';
import { EXAMS, formatDuration, formatShortDate, getExamById, getRoleById, relativeTime } from '@prepmitra/shared';
import {
  Badge, ButtonLink, Card, CardBody, CardHeader, DemoBadge, EmptyState, Mitra, PageHeader, ProgressBar, StatCard, accuracyTone,
} from '@/components/ui';
import { ScoreChart, TopicAccuracyChart } from '@/components/charts/Charts';
import { ExamCard } from '@/components/exam/ExamCard';
import { selectInProgress, useAuthStore, useExamStore, useInterviewStore, useProfileStore, useSubscriptionStore } from '@/store';
import { InterviewScoresCard } from '@/components/common/InterviewScoresCard';
import { interviewsEnabled, isExamOpen } from '@/config/launch';
import { cn } from '@/utils/cn';
import { useProgress } from '@/hooks/useProgress';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useContentT } from '@/i18n/content';
import { useT } from '@/i18n';
import { dashboardMessages } from '@/i18n/messages/dashboard';
import { Stagger } from '@/components/motion';

const greetingKey = () => {
  const h = new Date().getHours();
  return h < 12 ? 'morning' : h < 17 ? 'afternoon' : 'evening';
};

export function DashboardPage() {
  const t = useT(dashboardMessages);
  const ct = useContentT();
  useDocumentTitle(t('docTitle'));
  const user = useAuthStore((s) => s.session?.user);
  const profile = useProfileStore((s) => s.profile);
  const sub = useSubscriptionStore((s) => s.sub);
  const attempts = useExamStore((s) => s.attempts);
  const inProgress = selectInProgress(attempts)[0];
  const p = useProgress();
  const interviewReports = useInterviewStore((s) => s.reports);
  const interviewList = useMemo(() => Object.values(interviewReports), [interviewReports]);

  const recommendedExams = useMemo(() => {
    const targets = profile.targetExamIds.map((id) => getExamById(id)).filter((e): e is NonNullable<typeof e> => !!e);
    const fallback = EXAMS.filter((e) => e.status === 'published').sort((a, b) => b.popularity - a.popularity);
    const list = [...targets, ...fallback.filter((e) => !targets.includes(e))].filter(isExamOpen);
    return list.slice(0, 3);
  }, [profile.targetExamIds]);

  const recommendations: Recommendation[] = useMemo(() => {
    const recs: Recommendation[] = [];
    if (!sub.freeMiniMockUsed) recs.push({ id: 'free', title: t('recFreeTitle'), reason: t('recFreeReason'), examId: 'general-aptitude', minutes: 30 });
    for (const w of p.weak.slice(0, 2)) {
      const exam = p.reports.find((r) => r.result.topics.some((tp) => tp.topic === w.topic));
      recs.push({ id: `w-${w.topic}`, title: t('recTopicTitle', { topic: ct(w.topic) }), reason: t('recTopicReason', { mastery: w.mastery, count: w.attempts }), topic: w.topic, examId: exam?.examId, minutes: 20 });
    }
    const last = p.history[0];
    if (last) {
      const next = p.reports.find((r) => r.id === last.reportId)?.recommendedNextExamId;
      if (next) recs.push({ id: 'next', title: t('recNextTitle', { exam: getExamById(next)?.shortTitle ?? t('next') }), reason: t('recNextReason'), examId: next, minutes: getExamById(next)?.durationMin ?? 60 });
    }
    for (const roleId of interviewsEnabled() ? profile.targetRoleIds.slice(0, 1) : []) {
      recs.push({ id: `r-${roleId}`, title: t('recRoleTitle', { role: getRoleById(roleId)?.shortTitle ?? t('role') }), reason: t('recRoleReason'), roleId, minutes: getRoleById(roleId)?.durationMin ?? 20 });
    }
    // Only suggest exams that are open (others are "Coming soon").
    return recs.filter((r) => !r.examId || isExamOpen(getExamById(r.examId) ?? { category: 'banking', isFree: false })).slice(0, 4);
  }, [p, sub.freeMiniMockUsed, profile.targetRoleIds, t]);

  const firstName = user?.name.split(' ')[0] ?? t('there');
  // Next recommended test: from the latest report, else the free mini mock, else the first target exam.
  const latestReport = p.history[0] ? p.reports.find((r) => r.id === p.history[0]!.reportId) : undefined;
  const openExam = (id?: string) => {
    const e = id ? getExamById(id) : undefined;
    return e && isExamOpen(e) ? e : undefined;
  };
  const nextExam =
    openExam(latestReport?.recommendedNextExamId ?? (sub.freeMiniMockUsed ? profile.targetExamIds[0] ?? 'general-aptitude' : 'general-aptitude')) ??
    openExam(profile.targetExamIds.find((id) => openExam(id))) ??
    EXAMS.find((e) => e.status === 'published' && !e.isFree && isExamOpen(e));
  const nextReason = latestReport
    ? latestReport.weaknesses[0]
      ? t('nextReasonReportFocus', { exam: latestReport.examTitle, topic: ct(latestReport.weaknesses[0].topic) })
      : t('nextReasonReport', { exam: latestReport.examTitle })
    : sub.freeMiniMockUsed
      ? t('nextReasonTarget')
      : t('nextReasonFree');
  const hasHistory = p.history.length > 0;

  return (
    <div className="space-y-6">
      <PageHeader
        title={t('greeting', { greeting: t(greetingKey()), name: firstName })}
        description={hasHistory ? t('descHistory') : t('descNew')}
        actions={
          <>
            <ButtonLink to="/exams" variant="outline" leftIcon={<BookOpen className="h-4 w-4" />}>{t('browseExams')}</ButtonLink>
            <ButtonLink to={sub.freeMiniMockUsed ? '/exams' : '/exams/general-aptitude'} leftIcon={<Play className="h-4 w-4" />}>
              {sub.freeMiniMockUsed ? t('startMock') : t('startFreeMock')}
            </ButtonLink>
          </>
        }
        eyebrow={<DemoBadge>{t('demoData')}</DemoBadge>}
      />

      {inProgress && (
        <Card className="flex flex-col gap-3 border-primary/30 bg-primary-soft p-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="font-semibold text-primary">{t('unfinished')}</p>
            <p className="text-sm text-muted">{getExamById(inProgress.examId)?.title} · {t('started', { when: relativeTime(inProgress.startedAt) })}</p>
          </div>
          <ButtonLink to={`/exam/${inProgress.id}`} rightIcon={<ArrowRight className="h-4 w-4" />}>{t('resumeExam')}</ButtonLink>
        </Card>
      )}

      {nextExam && (
        <section aria-label={t('nextTest')} className="flex flex-col gap-5 rounded-[22px] bg-chalkboard p-5 text-chalk-text shadow-wood sm:flex-row sm:items-center sm:justify-between sm:p-6">
          <div className="flex min-w-0 items-start gap-4">
            <Mitra size={56} label={t('mitraLabel')} />
            <div className="min-w-0">
              <p className="text-xs font-bold uppercase tracking-wider text-accent">{t('nextTest')}</p>
              <p className="mt-0.5 font-display text-xl font-bold text-chalk-text">{nextExam.title}</p>
              <p className="mt-1 font-hand text-lg leading-snug text-chalk-text/85">{nextReason}</p>
            </div>
          </div>
          <ButtonLink to={`/exams/${nextExam.id}`} size="lg" className="shrink-0 bg-accent text-chalk-deep shadow-[0_5px_0_#A6370A] hover:bg-[#F7A04A]" rightIcon={<ArrowRight className="h-4 w-4" />}>{t('startNow')}</ButtonLink>
        </section>
      )}

      {latestReport && latestReport.improvementPlan.length > 0 && (
        <section aria-label={t('pathTitle')} className="rounded-[22px] border-[1.5px] border-ink bg-ruled p-5 shadow-hard-sm sm:p-6">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h2 className="text-lg font-bold sm:text-xl">{t('pathTitle')}</h2>
            <Link to={`/reports/${latestReport.id}?tab=plan`} className="text-sm font-semibold text-primary hover:underline">{t('pathOpen')}</Link>
          </div>
          <p className="mt-0.5 font-hand text-base text-muted">{t('pathFrom', { exam: latestReport.examTitle })}</p>
          <ol className="relative mt-5 flex gap-3 overflow-x-auto pb-2 scrollbar-thin">
            {latestReport.improvementPlan.map((d, i) => (
              <li key={d.day} className="flex w-40 shrink-0 flex-col items-center text-center">
                <span className="relative flex w-full items-center justify-center">
                  {i > 0 && <span className="absolute right-1/2 top-1/2 w-full border-t-[3px] border-dotted border-ink/60" aria-hidden />}
                  {i === 0 ? (
                    <Link to={`/reports/${latestReport.id}?tab=plan`} className="relative flex h-16 w-16 items-center justify-center rounded-full bg-primary text-xs font-extrabold uppercase text-white shadow-[0_5px_0_#8A2E07,0_0_0_8px_rgb(242_140_40/0.22)]">{t('pathStart')}</Link>
                  ) : (
                    <span className="relative flex h-12 w-12 items-center justify-center rounded-full border-2 border-line-strong bg-card font-bold text-subtle">{d.day}</span>
                  )}
                </span>
                <span className="mt-3 text-xs font-bold uppercase tracking-wider text-primary">{t('pathDay', { n: d.day })}</span>
                <span className="mt-0.5 line-clamp-2 text-sm font-semibold leading-snug">{d.title}</span>
                <span className="text-xs text-muted">{t('pathMinutes', { n: d.minutes })}</span>
              </li>
            ))}
          </ol>
        </section>
      )}

      <Stagger className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label={t('statTaken')} value={p.history.length} icon={<ClipboardList className="h-5 w-5" />} hint={hasHistory ? t('statLast', { date: formatShortDate(p.history[0]!.submittedAt) }) : t('statNoAttempts')} />
        <StatCard label={t('statAvg')} value={`${p.avg}%`} icon={<Target className="h-5 w-5" />} trend={hasHistory ? { value: p.delta, label: t('statVsPrev') } : undefined} hint={hasHistory ? '' : t('statTakeMock')} />
        <StatCard label={t('statStreak')} value={t(p.streakDays === 1 ? 'day' : 'days', { count: p.streakDays })} icon={<Flame className="h-5 w-5" />} hint={t('minThisWeek', { count: p.totalMinutes })} />
        <StatCard label={t('statCredits')} value={sub.credits} icon={<Coins className="h-5 w-5" />} hint={sub.freeMiniMockUsed ? <Link to="/subscription" className="font-medium text-primary hover:underline">{t('manageCredits')}</Link> : t('freeMiniAvailable')} />
      </Stagger>

      <div className={cn('grid gap-3 sm:grid-cols-2', interviewsEnabled() ? 'lg:grid-cols-4' : 'lg:grid-cols-3')} aria-label={t('quickPractice')}>
        {[
          { to: '/exams/general-aptitude', icon: Lightbulb, title: t('qAptitude'), sub: sub.freeMiniMockUsed ? t('oneCredit') : t('freeTrial') },
          { to: '/exams?category=banking', icon: BookOpen, title: t('qBanking'), sub: 'IBPS · SBI' },
          { to: '/interviews', icon: MessageSquare, title: t('qInterview'), sub: t('qInterviewSub') },
          { to: '/progress', icon: TrendingUp, title: t('qProgress'), sub: t('qProgressSub') },
        ].filter((q) => q.to !== '/interviews' || interviewsEnabled()).map(({ to, icon: Icon, title, sub: s }) => (
          <Link key={to} to={to} className="group flex items-center gap-3 rounded-[var(--radius-card)] border border-line bg-card p-4 shadow-card transition-colors hover:border-primary/40">
            <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary-soft text-secondary"><Icon className="h-5 w-5" aria-hidden /></span>
            <span className="min-w-0 flex-1">
              <span className="block text-sm font-semibold">{title}</span>
              <span className="block text-xs text-muted">{s}</span>
            </span>
            <ArrowRight className="h-4 w-4 text-muted transition-transform group-hover:translate-x-0.5" aria-hidden />
          </Link>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.6fr_1fr]">
        <Card>
          <CardHeader title={t('scoreTrend')} description={t('scoreTrendDesc')} action={hasHistory ? <ButtonLink to="/progress" variant="ghost" size="sm">{t('details')}</ButtonLink> : undefined} />
          <CardBody>
            {p.trend.length > 0 ? (
              <ScoreChart data={p.trend.slice(-8)} />
            ) : (
              <EmptyState title={t('noScores')} description={t('noScoresDesc')} className="border-0" />
            )}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={t('recommended')} description={t('recommendedDesc')} />
          <CardBody className="space-y-3">
            {recommendations.length === 0 && <p className="text-sm text-muted">{t('noRecs')}</p>}
            {recommendations.map((r) => (
              <Link
                key={r.id}
                to={r.roleId ? `/interviews/${r.roleId}` : r.examId ? `/exams/${r.examId}` : '/exams'}
                className="flex gap-3 rounded-lg border border-line p-3 transition-colors hover:border-primary/40 hover:bg-primary-soft/40"
              >
                <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary-soft text-primary">
                  {r.roleId ? <MessageSquare className="h-4 w-4" aria-hidden /> : <Target className="h-4 w-4" aria-hidden />}
                </span>
                <span className="min-w-0">
                  <span className="block text-sm font-semibold">{r.title}</span>
                  <span className="block text-xs text-muted">{r.reason}</span>
                  <span className="mt-1 block text-xs font-medium text-primary">{t('min', { count: r.minutes })}</span>
                </span>
              </Link>
            ))}
          </CardBody>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader title={t('topicAccuracy')} description={t('topicAccuracyDesc')} />
          <CardBody>
            {p.topics.length > 0 ? (
              <TopicAccuracyChart data={p.topics.slice(0, 8).map((tp) => ({ topic: tp.topic, accuracy: tp.mastery }))} />
            ) : (
              <EmptyState title={t('noTopic')} description={t('noTopicDesc')} className="border-0" />
            )}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={t('strengthsWeak')} />
          <CardBody className="grid gap-5 sm:grid-cols-2">
            <div>
              <p className="flex items-center gap-1.5 text-sm font-semibold text-success"><Trophy className="h-4 w-4" aria-hidden />{t('strengths')}</p>
              <ul className="mt-3 space-y-3">
                {p.strong.slice(0, 4).map((tp) => (
                  <li key={tp.topic}><ProgressBar label={ct(tp.topic)} value={tp.mastery} showValue tone="success" size="sm" /></li>
                ))}
                {p.strong.length === 0 && <li className="text-sm text-muted">{t('strengthsEmpty')}</li>}
              </ul>
            </div>
            <div>
              <p className="flex items-center gap-1.5 text-sm font-semibold text-danger"><TrendingDown className="h-4 w-4" aria-hidden />{t('needsWork')}</p>
              <ul className="mt-3 space-y-3">
                {p.weak.slice(0, 4).map((tp) => (
                  <li key={tp.topic}><ProgressBar label={ct(tp.topic)} value={tp.mastery} showValue tone={accuracyTone(tp.mastery)} size="sm" /></li>
                ))}
                {p.weak.length === 0 && <li className="text-sm text-muted">{t('needsWorkEmpty')}</li>}
              </ul>
            </div>
          </CardBody>
        </Card>
      </div>

      {interviewsEnabled() && <InterviewScoresCard reports={interviewList} />}

      <Card>
        <CardHeader title={t('recentAttempts')} action={hasHistory ? <ButtonLink to="/my-tests" variant="ghost" size="sm">{t('viewAll')}</ButtonLink> : undefined} />
        <CardBody className="p-0">
          {hasHistory ? (
            <div className="relative overflow-x-auto">
              <table className="w-full min-w-[600px] text-sm">
                <thead>
                  <tr className="border-b border-line text-left text-muted">
                    <th scope="col" className="px-5 py-2.5 font-medium">{t('colExam')}</th>
                    <th scope="col" className="px-5 py-2.5 font-medium">{t('colDate')}</th>
                    <th scope="col" className="px-5 py-2.5 font-medium">{t('colScore')}</th>
                    <th scope="col" className="px-5 py-2.5 font-medium">{t('colAccuracy')}</th>
                    <th scope="col" className="px-5 py-2.5 font-medium">{t('colTime')}</th>
                    <th scope="col" className="px-5 py-2.5"><span className="sr-only">{t('colActions')}</span></th>
                  </tr>
                </thead>
                <tbody>
                  {p.history.slice(0, 5).map((h) => (
                    <tr key={h.reportId} className="border-b border-line last:border-0">
                      <td className="px-5 py-3 font-medium">{h.examTitle}</td>
                      <td className="px-5 py-3 text-muted">{formatShortDate(h.submittedAt)}</td>
                      <td className="px-5 py-3">{h.score}/{h.maxScore}</td>
                      <td className="px-5 py-3"><Badge tone={accuracyTone(h.accuracy)}>{h.accuracy}%</Badge></td>
                      <td className="px-5 py-3 text-muted">{formatDuration(h.timeTakenSec)}</td>
                      <td className="px-5 py-3 text-right"><ButtonLink to={`/reports/${h.reportId}`} variant="ghost" size="sm">{t('report')}</ButtonLink></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-5">
              <EmptyState
                icon={<ClipboardList className="h-6 w-6" />}
                title={t('noAttempts')}
                description={t('noAttemptsDesc')}
                action={<ButtonLink to="/exams/general-aptitude">{t('takeFreeMini')}</ButtonLink>}
              />
            </div>
          )}
        </CardBody>
      </Card>

      <section aria-labelledby="rec-exams">
        <div className="mb-4 flex items-center justify-between">
          <h2 id="rec-exams" className="text-lg font-semibold">{t('recExams')}</h2>
          <ButtonLink to="/exams" variant="ghost" size="sm" rightIcon={<ArrowRight className="h-4 w-4" />}>{t('allExams')}</ButtonLink>
        </div>
        <Stagger className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {recommendedExams.map((e) => <ExamCard key={e.id} exam={e} />)}
        </Stagger>
      </section>
    </div>
  );
}
