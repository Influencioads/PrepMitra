import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ChevronLeft, ChevronRight, RefreshCw, Settings2 } from 'lucide-react';
import { Button, Card, CardBody, CardHeader, Input, LoadingSkeleton, MitraSays, Modal, Notice, PageHeader, ProgressBar, Select } from '@/components/ui';
import { NeedsBackend, TaskRow } from '@/components/mentor/MentorUi';
import { useMentorT, type MentorKey } from '@/components/mentor/format';
import { CountdownLine } from '@/components/mentor/GoalForm';
import { errorMessage, mentorService, type Countdown } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

const addDays = (iso: string, n: number) => {
  const d = new Date(`${iso}T00:00:00`);
  d.setDate(d.getDate() + n);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};
const dayLabel = (iso: string) => new Date(`${iso}T00:00:00`).toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'short' });

function EditGoal({ goal, onSaved, onClose }: { goal: Countdown; onSaved: () => void; onClose: () => void }) {
  const t = useMentorT();
  const [date, setDate] = useState(goal.exam_date);
  const [minutes, setMinutes] = useState(goal.daily_minutes);
  const [rest, setRest] = useState(goal.rest_weekday === null ? '' : String(goal.rest_weekday));
  const [busy, setBusy] = useState(false);
  const save = async () => {
    setBusy(true);
    try {
      await mentorService.updateGoal(goal.goal_id, {
        exam_date: date, daily_minutes: minutes, ...(rest === '' ? { clear_rest_day: true } : { rest_weekday: Number(rest) }),
      });
      toast.success(t('regenerated'));
      onSaved();
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };
  const archive = async () => {
    await mentorService.archiveGoal(goal.goal_id).then(() => { toast.success(t('archived')); window.location.assign('/mentor'); }, (e) => toast.error(errorMessage(e)));
  };
  return (
    <Modal open onOpenChange={(o) => !o && onClose()} title={t('changeDate')} footer={(
      <div className="flex w-full flex-wrap justify-between gap-2">
        <Button variant="ghost" className="text-danger" onClick={archive}>{t('archiveGoal')}</Button>
        <div className="flex gap-2"><Button variant="outline" onClick={onClose}>{t('cancel')}</Button><Button onClick={save} loading={busy}>{t('save')}</Button></div>
      </div>
    )}>
      <div className="grid gap-4">
        <Input label={t('examDate')} type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        <Input label={t('dailyMinutes')} type="number" min={15} max={720} step={15} value={minutes} onChange={(e) => setMinutes(Number(e.target.value))} />
        <Select label={t('restDay')} value={rest} onChange={(e) => setRest(e.target.value)}
          options={[{ value: '', label: t('noRestDay') }, ...[0, 1, 2, 3, 4, 5, 6].map((d) => ({ value: String(d), label: t(`weekday${d}` as MentorKey) }))]} />
      </div>
    </Modal>
  );
}

export function StudyPlanPage() {
  const t = useMentorT();
  useDocumentTitle(t('navPlan'));
  const [params] = useSearchParams();
  const wanted = params.get('goal') ? Number(params.get('goal')) : undefined;
  const goals = useAsync(() => mentorService.goals(), []);
  const goal = goals.data?.find((g) => g.goal_id === wanted) ?? goals.data?.find((g) => g.days_remaining >= 0) ?? goals.data?.[0];
  const [offset, setOffset] = useState(0);
  const [editing, setEditing] = useState(false);
  const [rebuilding, setRebuilding] = useState(false);
  const plan = useAsync(async () => {
    if (!goal) return undefined;
    const start = addDays(goal.today, offset * 7 - 1);
    return mentorService.plan(goal.goal_id, start, addDays(start, 13));
  }, [goal?.goal_id, offset, goals.data]);

  const rebuild = async () => {
    if (!goal) return;
    setRebuilding(true);
    try {
      await mentorService.regenerate(goal.goal_id);
      toast.success(t('regenerated'));
      plan.reload();
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setRebuilding(false);
    }
  };

  if (goals.loading && !goals.data) return <LoadingSkeleton variant="page" />;
  if (goals.error) return <NeedsBackend error={goals.error} />;
  if (!goal) return <Notice tone="info">{t('setupDesc')}</Notice>;
  const p = plan.data;
  const meta = p?.meta;

  return (
    <div className="space-y-6">
      <PageHeader title={t('planTitle')} description={t('planDesc', { exam: goal.exam_name })} eyebrow={<span className="text-sm font-semibold text-primary"><CountdownLine c={goal} /></span>}
        actions={<>
          <Button variant="outline" onClick={() => setEditing(true)} leftIcon={<Settings2 className="h-4 w-4" />}>{t('changeDate')}</Button>
          <Button onClick={rebuild} loading={rebuilding} leftIcon={<RefreshCw className="h-4 w-4" />}>{t('regenerate')}</Button>
        </>} />

      {meta?.note?.note && <MitraSays>{meta.note.note}</MitraSays>}
      {meta?.tradeoffs && meta.tradeoffs.length > 0 && (
        <Notice tone="warning" title={t('tradeoffs')}>
          <ul className="list-disc space-y-1 pl-4">{meta.tradeoffs.map((x) => <li key={x.topic}><b>{x.topic}:</b> {x.note}</li>)}</ul>
        </Notice>
      )}

      {p && (
        <Card>
          <CardHeader title={t('weekProgress')} description={t('weekTasks', { done: p.week.done, total: p.week.total })} />
          <CardBody>
            <ProgressBar value={p.week.done} max={Math.max(1, p.week.total)} tone="success" />
            {p.week.missed > 0 && <p className="mt-2 text-sm text-danger">{t('weekMissed', { n: p.week.missed })}</p>}
          </CardBody>
        </Card>
      )}

      <div className="flex items-center justify-between">
        <Button variant="outline" size="sm" onClick={() => setOffset((o) => o - 1)} leftIcon={<ChevronLeft className="h-4 w-4" />}>{t('prev')}</Button>
        {offset !== 0 && <Button variant="ghost" size="sm" onClick={() => setOffset(0)}>{t('today')}</Button>}
        <Button variant="outline" size="sm" onClick={() => setOffset((o) => o + 1)} rightIcon={<ChevronRight className="h-4 w-4" />}>{t('next')}</Button>
      </div>

      {plan.loading && !p ? <LoadingSkeleton variant="list" /> : plan.error ? <NeedsBackend error={plan.error} /> : p && (
        <div className="grid gap-4 lg:grid-cols-2">
          {p.days.map((d) => {
            const isToday = d.date === p.today;
            return (
              <Card key={d.date} className={cn(isToday && 'ring-2 ring-primary')}>
                <CardHeader title={<span>{isToday ? `${t('today')} · ` : ''}{dayLabel(d.date)}</span>}
                  description={d.days_to_exam > 0 ? t('daysToExam', { n: d.days_to_exam }) : undefined}
                  action={d.total > 0 ? <span className="text-sm text-muted">{d.done}/{d.total} · {t('min', { n: d.minutes })}</span> : undefined} />
                <CardBody><ul className="space-y-2">{d.tasks.map((task) => <TaskRow key={task.id} task={task} examSlug={goal.exam_slug} onChanged={plan.reload} compact={!isToday} />)}</ul></CardBody>
              </Card>
            );
          })}
        </div>
      )}
      {meta?.horizon_end && <p className="text-xs text-muted">{t('planEnd', { date: meta.horizon_end })}</p>}
      {editing && <EditGoal goal={goal} onClose={() => setEditing(false)} onSaved={() => { setEditing(false); goals.reload(); }} />}
    </div>
  );
}
