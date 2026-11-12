import { useMemo, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { BookX, CalendarDays, ClipboardCheck, Gauge, MessageCircle, Plus, Target, TrendingUp, Trophy } from 'lucide-react';
import {
  Button, ButtonLink, Card, CardBody, CardHeader, LoadingSkeleton, MitraSays, Modal, Notice, PageHeader,
  ProgressBar, Select, StatCard, Tabs,
} from '@/components/ui';
import { NeedsBackend, PriorityBadge, StatusBadge, TaskRow } from '@/components/mentor/MentorUi';
import { pct, useMentorT } from '@/components/mentor/format';
import { CountdownLine, GoalForm } from '@/components/mentor/GoalForm';
import { mentorService, type Overview, type TopicBrief } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

function TopicTable({ topics }: { topics: TopicBrief[] }) {
  const t = useMentorT();
  if (!topics.length) return <p className="px-5 pb-5 text-sm text-muted">—</p>;
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[640px] text-sm">
        <thead className="text-left text-xs uppercase tracking-wide text-muted">
          <tr className="border-b border-line">
            <th className="px-5 py-2 font-medium">{t('colTopic')}</th>
            <th className="px-3 py-2 text-right font-medium">{t('colAccuracy')}</th>
            <th className="px-3 py-2 text-right font-medium">{t('colQuestions')}</th>
            <th className="px-3 py-2 font-medium">{t('colStatus')}</th>
            <th className="px-3 py-2 font-medium">{t('colPriority')}</th>
            <th className="px-5 py-2 font-medium">{t('colAction')}</th>
          </tr>
        </thead>
        <tbody>
          {topics.map((x) => (
            <tr key={x.topic_id} className="border-b border-line last:border-0 align-top">
              <td className="px-5 py-2.5 font-medium text-ink">{x.name}</td>
              <td className="px-3 py-2.5 text-right tabular-nums">{pct(x.effective_accuracy)}</td>
              <td className="px-3 py-2.5 text-right tabular-nums">{x.attempted}</td>
              <td className="px-3 py-2.5"><StatusBadge topic={x} /></td>
              <td className="px-3 py-2.5"><PriorityBadge priority={x.priority} /></td>
              <td className="px-5 py-2.5 text-muted">{x.action}{x.tradeoff && <span className="mt-1 block text-xs text-amber-800">{x.tradeoff}</span>}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function OverviewView({ o, reload }: { o: Overview; reload: () => void }) {
  const t = useMentorT();
  const [tab, setTab] = useState<'all' | 'weak' | 'strong' | 'pending'>('all');
  const ex = o.exam;
  const m = o.mock_tests;
  const rec = o.recommendations;
  const wk = o.weekly_progress;
  const shown = tab === 'all' ? o.topics.all : o.topics[tab];
  return (
    <div className="space-y-6">
      <Card className="overflow-hidden">
        <div className="grid gap-6 p-5 sm:p-6 lg:grid-cols-[1.1fr_2fr]">
          <div>
            <p className="text-sm font-medium text-muted">{ex.exam_name}</p>
            <p className="mt-1 font-display text-4xl font-extrabold tracking-tight text-primary"><CountdownLine c={ex} /></p>
            <p className="mt-1 text-sm text-muted">
              {new Date(ex.exam_date).toLocaleDateString(undefined, { day: 'numeric', month: 'long', year: 'numeric' })}
              {ex.days_remaining > 0 && ` · ${t('weeksDays', { w: ex.weeks_remaining, d: ex.extra_days })}`}
            </p>
            {ex.phase === 'final_revision' && <p className="mt-2 text-sm font-semibold text-amber-800">{t('finalRevision')}</p>}
          </div>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <div><ProgressBar value={o.coverage.syllabus_completion_pct} label={t('syllabus')} showValue tone="secondary" /></div>
            <div><ProgressBar value={o.coverage.preparation_pct} label={t('preparation')} showValue tone="success" /></div>
            <div className="text-sm"><p className="text-muted">{t('topicsCompleted')}</p><p className="text-xl font-bold">{o.coverage.topics_completed}/{o.coverage.topics_total}</p></div>
            <div className="text-sm"><p className="text-muted">{t('topicsPending')} · {t('weakTopics')}</p><p className="text-xl font-bold">{o.coverage.topics_pending} · <span className="text-danger">{o.coverage.topics_weak}</span></p></div>
          </div>
        </div>
      </Card>

      {o.plan.note?.note && <MitraSays>{o.plan.note.note}</MitraSays>}

      <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
        <Card>
          <CardHeader title={t('todayPlan')} action={<ButtonLink to={`/mentor/plan?goal=${ex.goal_id}`} variant="outline" size="sm" leftIcon={<CalendarDays className="h-4 w-4" />}>{t('openPlan')}</ButtonLink>} />
          <CardBody>
            {o.plan.today.length === 0 ? <p className="text-sm text-muted">{t('noTasksToday')}</p> : (
              <ul className="space-y-2">{o.plan.today.map((task) => <TaskRow key={task.id} task={task} examSlug={ex.exam_slug} onChanged={reload} />)}</ul>
            )}
            <p className="mt-4 text-sm text-muted">
              {t('weekProgress')}: {t('weekTasks', { done: o.plan.week.done, total: o.plan.week.total })}
              {o.plan.week.missed > 0 && <span className="text-danger"> · {t('weekMissed', { n: o.plan.week.missed })}</span>}
              {wk.accuracy_change !== null && <> · {t('vsLastWeek', { n: `${wk.accuracy_change >= 0 ? '+' : ''}${Math.round(wk.accuracy_change * 100)}` })}</>}
            </p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={t('recommendations')} />
          <CardBody className="space-y-4 text-sm">
            {rec.more_attention.length > 0 && (
              <section>
                <h4 className="font-semibold text-danger">{t('moreAttention')}</h4>
                <ul className="mt-1 space-y-1">{rec.more_attention.map((x) => <li key={x.topic_id}><b>{x.name}</b> <span className="text-muted">— {pct(x.effective_accuracy)} · {x.action}</span></li>)}</ul>
              </section>
            )}
            {rec.practise.length > 0 && (
              <section>
                <h4 className="font-semibold">{t('practise')}</h4>
                <ul className="mt-1 space-y-1">{rec.practise.map((x) => <li key={x.topic_id}>{x.name} <span className="text-muted">— {x.action}</span></li>)}</ul>
              </section>
            )}
            {rec.revise.length > 0 && (
              <section>
                <h4 className="font-semibold">{t('revise')}</h4>
                <ul className="mt-1 space-y-1">{rec.revise.map((x) => <li key={x.title}>{x.kind === 'notebook' ? <Link className="text-primary underline" to="/mentor/notebook?filter=due">{x.title}</Link> : x.title}</li>)}</ul>
              </section>
            )}
            {rec.less_time.length > 0 && (
              <section>
                <h4 className="font-semibold text-success">{t('lessTime')}</h4>
                <ul className="mt-1 space-y-1">{rec.less_time.map((x) => <li key={x.topic_id}>{x.name} <span className="text-muted">— {x.tradeoff ?? x.action}</span></li>)}</ul>
              </section>
            )}
            <section className="rounded-lg bg-stone-50 p-3">
              <h4 className="font-semibold">{t('mockAdvice')}: {t(rec.mock_test.advice === 'yes' ? 'mockYes' : rec.mock_test.advice === 'no' ? 'mockNo' : 'mockNotYet')}</h4>
              <p className="mt-0.5 text-muted">{rec.mock_test.reason}</p>
            </section>
          </CardBody>
        </Card>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label={t('mocksDone')} value={m.tests_completed} icon={<ClipboardCheck className="h-5 w-5" />}
          hint={m.last_attempt_id ? <Link className="text-primary underline" to={`/mentor/analysis/${m.last_attempt_id}`}>{t('viewAnalysis')}</Link> : t('noMocksYet')} />
        <StatCard label={t('highestScore')} value={m.highest_score ?? '—'} icon={<Trophy className="h-5 w-5" />} hint={m.max_score ? `/ ${m.max_score}` : undefined} />
        <StatCard label={`${t('averageScore')} · ${t('recentScore')}`} value={m.average_score !== null ? `${m.average_score} · ${m.recent_score}` : '—'} icon={<TrendingUp className="h-5 w-5" />} />
        <StatCard label={`${t('accuracy')} · ${t('timeEfficient')}`} value={`${pct(m.accuracy)} · ${pct(m.time_management?.efficient_share)}`} icon={<Gauge className="h-5 w-5" />} />
      </div>

      <Card>
        <CardHeader title={t('subjects')} />
        <CardBody className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {o.subjects.map((s) => (
            <div key={s.subject} className="rounded-lg border border-line p-4">
              <div className="flex items-baseline justify-between"><p className="font-semibold">{s.name}</p><p className="text-lg font-bold tabular-nums">{pct(s.accuracy)}</p></div>
              <ProgressBar className="mt-2" value={(s.accuracy ?? 0) * 100} tone={s.accuracy === null ? 'secondary' : s.accuracy >= 0.75 ? 'success' : s.accuracy >= 0.55 ? 'warning' : 'danger'} size="sm" />
              <p className="mt-2 text-xs text-muted">{t('weakTopics')}: {s.weak} · {t('st_strong')}: {s.strong} · {t('st_not_started')}: {s.not_started}</p>
            </div>
          ))}
        </CardBody>
      </Card>

      <Card>
        <CardHeader title={t('topicAnalysis')} description={t('minEvidence', { n: o.coverage.min_evidence })} />
        <div className="px-5 pt-3">
          <Tabs ariaLabel={t('topicAnalysis')} value={tab} onChange={setTab} items={[
            { value: 'all', label: t('f_all'), count: o.topics.all.length },
            { value: 'weak', label: t('weakTopics'), count: o.topics.weak.length },
            { value: 'strong', label: t('st_strong'), count: o.topics.strong.length },
            { value: 'pending', label: t('topicsPending'), count: o.topics.pending.length },
          ]} />
        </div>
        <TopicTable topics={shown} />
      </Card>

      {o.plan.tradeoffs.length > 0 && (
        <Notice tone="warning" title={t('tradeoffs')}>
          <ul className="list-disc space-y-1 pl-4">{o.plan.tradeoffs.map((x) => <li key={x.topic}><b>{x.topic}:</b> {x.note}</li>)}</ul>
        </Notice>
      )}
    </div>
  );
}

export function MentorDashboardPage() {
  const t = useMentorT();
  useDocumentTitle(t('docTitle'));
  const [params, setParams] = useSearchParams();
  const goalId = params.get('goal') ? Number(params.get('goal')) : undefined;
  const dash = useAsync(() => mentorService.dashboard(goalId), [goalId]);
  const [adding, setAdding] = useState(false);
  const goals = useMemo(() => dash.data?.goals ?? [], [dash.data]);
  const selected = dash.data?.selected;
  const goalOptions = useMemo(() => goals.map((g) => ({ value: String(g.goal_id), label: `${g.exam_name} (${g.exam_date})` })), [goals]);
  const onCreated = (id: number) => { setAdding(false); setParams({ goal: String(id) }); dash.reload(); };

  return (
    <div className="space-y-6">
      <PageHeader title={t('title')} description={t('desc')} actions={selected ? (
        <>
          {goals.length > 1 && <Select aria-label={t('exam')} value={String(selected.exam.goal_id)} onChange={(e) => setParams({ goal: e.target.value })} options={goalOptions} />}
          <ButtonLink to="/mentor/notebook" variant="outline" leftIcon={<BookX className="h-4 w-4" />}>
            {t('navNotebook')}{selected.revision.notebook_due > 0 && <span className="ml-1 rounded-full bg-danger px-1.5 text-xs text-white">{selected.revision.notebook_due}</span>}
          </ButtonLink>
          <ButtonLink to="/mentor/chat" variant="outline" leftIcon={<MessageCircle className="h-4 w-4" />}>{t('navChat')}</ButtonLink>
          <Button variant="ghost" onClick={() => setAdding(true)} leftIcon={<Plus className="h-4 w-4" />}>{t('addExam')}</Button>
        </>
      ) : undefined} />

      {dash.loading && !dash.data ? <LoadingSkeleton variant="page" /> : dash.error ? <NeedsBackend error={dash.error} /> : !selected ? (
        <Card className={cn('mx-auto max-w-2xl')}>
          <CardHeader title={<span className="flex items-center gap-2"><Target className="h-5 w-5 text-primary" />{t('setupTitle')}</span>} description={t('setupDesc')} />
          <CardBody><GoalForm onCreated={onCreated} /></CardBody>
        </Card>
      ) : <OverviewView o={selected} reload={dash.reload} />}

      <Modal open={adding} onOpenChange={setAdding} title={t('addExam')} description={t('setupDesc')} size="lg">
        <GoalForm onCreated={onCreated} onCancel={() => setAdding(false)} />
      </Modal>
    </div>
  );
}
