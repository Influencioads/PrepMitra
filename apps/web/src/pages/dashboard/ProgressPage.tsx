import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowDown, ArrowRight, ArrowUp, Award, Clock, Flame, Minus, Target, TrendingUp } from 'lucide-react';
import type { ExamCategory } from '@prepmitra/shared';
import { EXAM_CATEGORIES, computeProgress, getExamById } from '@prepmitra/shared';
import {
  ButtonLink, Card, CardBody, CardHeader, DemoBadge, EmptyState, PageHeader, ProgressBar, Select, StatCard, accuracyTone,
} from '@/components/ui';
import { ScoreChart, TopicAccuracyChart, WeeklyBarChart } from '@/components/charts/Charts';
import { useExamStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { accountMessages } from '@/i18n/messages/account';
import { catalogMessages, categoryText } from '@/i18n/messages/catalog';

const RANGES = [
  { value: '7', key: 'range7' },
  { value: '30', key: 'range30' },
  { value: '90', key: 'range90' },
  { value: 'all', key: 'rangeAll' },
] as const;
const DAY = 86_400_000;

const masteryClass = (m: number) =>
  m >= 75 ? 'bg-green-100 border-green-200 text-green-900' : m >= 60 ? 'bg-amber-50 border-amber-200 text-amber-900' : m >= 40 ? 'bg-orange-100 border-orange-200 text-orange-900' : 'bg-red-100 border-red-200 text-red-900';

export function ProgressPage() {
  const t = useT(accountMessages);
  const tcat = useT(catalogMessages);
  useDocumentTitle(t('progressDocTitle'));
  const reports = useExamStore((s) => s.reports);
  const log = useExamStore((s) => s.practiceLog);
  const [category, setCategory] = useState<ExamCategory | 'all'>('all');
  const [range, setRange] = useState('all');

  const data = useMemo(() => {
    const now = Date.now();
    const filtered = Object.values(reports).filter((r) => {
      const exam = getExamById(r.examId);
      if (category !== 'all' && exam?.category !== category) return false;
      if (range !== 'all' && now - new Date(r.createdAt).getTime() > Number(range) * DAY) return false;
      return true;
    });
    const p = computeProgress(filtered, log, now);
    const scores = filtered.map((r) => r.result.percentage);
    const acc = filtered.map((r) => r.result.accuracy);
    const avg = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0;
    const best = scores.length ? Math.max(...scores) : 0;
    const avgAcc = acc.length ? Math.round(acc.reduce((a, b) => a + b, 0) / acc.length) : 0;
    const meaningful = p.topics.filter((x) => x.attempts >= 2);
    const strong = meaningful.filter((x) => x.mastery >= 75).sort((a, b) => b.mastery - a.mastery);
    const weak = meaningful.filter((x) => x.mastery < 60).sort((a, b) => a.mastery - b.mastery);
    const bestReport = filtered.find((r) => r.result.percentage === best);
    return { ...p, filtered, avg, best, avgAcc, strong, weak, bestReport };
  }, [reports, log, category, range]);

  const hasData = data.filtered.length > 0;
  const anyData = Object.keys(reports).length > 0;

  const plan = data.weak.slice(0, 4).map((w, i) => {
    const examId = data.filtered.find((r) => r.result.topics.some((x) => x.topic === w.topic))?.examId;
    return { day: i * 2 + 1, topic: w.topic, mastery: w.mastery, examId };
  });

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow={<DemoBadge>{t('demoData')}</DemoBadge>}
        title={t('analyticsTitle')}
        description={t('analyticsDesc')}
        actions={
          <div className="grid w-full grid-cols-2 gap-2 sm:w-auto">
            <Select aria-label={t('examCategory')} value={category} onChange={(e) => setCategory(e.target.value as ExamCategory | 'all')} options={[{ value: 'all', label: t('allCategories') }, ...EXAM_CATEGORIES.map((c) => ({ value: c.id, label: categoryText(tcat, c.id).label }))]} />
            <Select aria-label={t('dateRange')} value={range} onChange={(e) => setRange(e.target.value)} options={RANGES.map((r) => ({ value: r.value, label: t(r.key) }))} />
          </div>
        }
      />

      {!anyData ? (
        <EmptyState
          icon={<TrendingUp className="h-6 w-6" />}
          title={t('analyticsEmptyTitle')}
          description={t('analyticsEmptyDesc')}
          action={<ButtonLink to="/exams/general-aptitude">{t('takeFreeMini')}</ButtonLink>}
        />
      ) : (
        <>
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
            <StatCard label={t('avgScore')} value={`${data.avg}%`} icon={<Target className="h-5 w-5" />} hint={t('attemptsCount', { n: data.filtered.length })} />
            <StatCard label={t('highestScore')} value={`${data.best}%`} icon={<Award className="h-5 w-5" />} hint={data.bestReport ? getExamById(data.bestReport.examId)?.shortTitle : '—'} />
            <StatCard label={t('avgAccuracy')} value={`${data.avgAcc}%`} icon={<TrendingUp className="h-5 w-5" />} hint={t('accuracyHint')} />
            <StatCard label={t('practiceWeek')} value={t('minValue', { n: data.totalMinutes })} icon={<Clock className="h-5 w-5" />} hint={t('range7')} />
            <StatCard label={t('streak')} value={data.streakDays === 1 ? t('dayOne') : t('dayMany', { n: data.streakDays })} icon={<Flame className="h-5 w-5" />} hint={t('streakHint')} />
          </div>

          {!hasData ? (
            <EmptyState title={t('noRangeTitle')} description={t('noRangeDesc')} />
          ) : (
            <div className="grid gap-6 lg:grid-cols-2">
              <Card>
                <CardHeader title={t('scoreTrend')} description={t('scoreTrendDesc')} />
                <CardBody><ScoreChart data={data.trend} showAccuracy={false} /></CardBody>
              </Card>
              <Card>
                <CardHeader title={t('accuracyTrend')} description={t('accuracyTrendDesc')} />
                <CardBody><ScoreChart data={data.trend.map((x) => ({ label: x.label, score: x.accuracy }))} showAccuracy={false} /></CardBody>
              </Card>
            </div>
          )}

          <div className="grid gap-6 lg:grid-cols-[1fr_1.4fr]">
            <Card>
              <CardHeader title={t('weeklyTime')} description={t('weeklyTimeDesc', { n: data.totalMinutes })} />
              <CardBody><WeeklyBarChart data={data.weekly} /></CardBody>
            </Card>
            <Card>
              <CardHeader title={t('topicMastery')} description={t('topicMasteryDesc')} />
              <CardBody>
                {data.topics.length === 0 ? (
                  <p className="text-sm text-muted">{t('noTopicData')}</p>
                ) : (
                  <ul className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                    {data.topics.slice(0, 15).map((tp) => (
                      <li key={tp.topic} className={cn('rounded-lg border p-3', masteryClass(tp.mastery))}>
                        <p className="truncate text-xs font-medium" title={tp.topic}>{tp.topic}</p>
                        <p className="mt-1 flex items-center gap-1 text-lg font-bold">
                          {tp.mastery}%
                          {tp.trend > 0 ? <ArrowUp className="h-4 w-4" aria-label={t('trendUp', { n: tp.trend })} /> : tp.trend < 0 ? <ArrowDown className="h-4 w-4" aria-label={t('trendDown', { n: -tp.trend })} /> : <Minus className="h-4 w-4 opacity-50" aria-label={t('noChange')} />}
                        </p>
                        <p className="text-[11px] opacity-80">{t('questionsCount', { n: tp.attempts })}</p>
                      </li>
                    ))}
                  </ul>
                )}
              </CardBody>
            </Card>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader title={t('strongWeak')} description={t('strongWeakDesc')} />
              <CardBody className="grid gap-6 sm:grid-cols-2">
                <div>
                  <p className="text-sm font-semibold text-success">{t('strong')}</p>
                  <ul className="mt-3 space-y-3">
                    {data.strong.slice(0, 5).map((tp) => <li key={tp.topic}><ProgressBar label={tp.topic} value={tp.mastery} showValue tone="success" size="sm" /></li>)}
                    {data.strong.length === 0 && <li className="text-sm text-muted">{t('noStrong')}</li>}
                  </ul>
                </div>
                <div>
                  <p className="text-sm font-semibold text-danger">{t('weak')}</p>
                  <ul className="mt-3 space-y-3">
                    {data.weak.slice(0, 5).map((tp) => <li key={tp.topic}><ProgressBar label={tp.topic} value={tp.mastery} showValue tone={accuracyTone(tp.mastery)} size="sm" /></li>)}
                    {data.weak.length === 0 && <li className="text-sm text-muted">{t('noWeak')}</li>}
                  </ul>
                </div>
              </CardBody>
            </Card>
            <Card>
              <CardHeader title={t('topicAccuracy')} />
              <CardBody>
                {data.topics.length ? <TopicAccuracyChart data={data.topics.slice(0, 8).map((tp) => ({ topic: tp.topic, accuracy: tp.mastery }))} /> : <p className="text-sm text-muted">{t('noData')}</p>}
              </CardBody>
            </Card>
          </div>

          <Card>
            <CardHeader title={t('recPlan')} description={t('recPlanDesc')} />
            <CardBody>
              {plan.length === 0 ? (
                <p className="text-sm text-muted">{t('noWeakPlan')}</p>
              ) : (
                <ol className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                  {plan.map((p) => (
                    <li key={p.topic} className="rounded-lg border border-line p-4">
                      <p className="text-xs font-semibold text-primary">{t('daysRange', { a: p.day, b: p.day + 1 })}</p>
                      <p className="mt-1 font-semibold">{p.topic}</p>
                      <p className="mt-1 text-sm text-muted">{t('masteryTask', { n: p.mastery })}</p>
                      {p.examId && (
                        <Link to={`/exams/${p.examId}`} className="mt-2 inline-flex items-center gap-1 text-sm font-medium text-primary hover:underline">
                          {t('practiseIn', { exam: getExamById(p.examId)?.shortTitle ?? '' })} <ArrowRight className="h-4 w-4" aria-hidden />
                        </Link>
                      )}
                    </li>
                  ))}
                </ol>
              )}
            </CardBody>
          </Card>
        </>
      )}
    </div>
  );
}
