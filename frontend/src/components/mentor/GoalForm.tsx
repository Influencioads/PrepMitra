import { useState } from 'react';
import toast from 'react-hot-toast';
import { Button, Input, Notice, Select } from '@/components/ui';
import { useMentorT, type MentorKey } from '@/components/mentor/format';
import { errorMessage, mentorService, type Countdown } from '@/services';
import { useAsync } from '@/hooks/useAsync';

const isoToday = () => new Date(Date.now() - new Date().getTimezoneOffset() * 60_000).toISOString().slice(0, 10);

export function GoalForm({ onCreated, onCancel }: { onCreated: (goalId: number) => void; onCancel?: () => void }) {
  const t = useMentorT();
  const exams = useAsync(() => mentorService.examOptions(), []);
  const [exam, setExam] = useState('');
  const [date, setDate] = useState('');
  const [minutes, setMinutes] = useState(120);
  const [rest, setRest] = useState('');
  const [busy, setBusy] = useState(false);
  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      const g = await mentorService.createGoal({ exam_id: exam, exam_date: date, daily_minutes: minutes, rest_weekday: rest === '' ? null : Number(rest) });
      onCreated(g.goal_id);
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setBusy(false);
    }
  };
  if (exams.error) return <Notice tone="danger">{exams.error}</Notice>;
  return (
    <form onSubmit={submit} className="grid gap-4 sm:grid-cols-2">
      <Select label={t('exam')} required value={exam} onChange={(e) => setExam(e.target.value)} placeholder="—"
        options={(exams.data ?? []).map((x) => ({ value: x.slug, label: x.name }))} />
      <Input label={t('examDate')} type="date" required min={isoToday()} value={date} onChange={(e) => setDate(e.target.value)} />
      <Input label={t('dailyMinutes')} type="number" min={15} max={720} step={15} required value={minutes}
        onChange={(e) => setMinutes(Number(e.target.value))} />
      <Select label={t('restDay')} value={rest} onChange={(e) => setRest(e.target.value)}
        options={[{ value: '', label: t('noRestDay') }, ...[0, 1, 2, 3, 4, 5, 6].map((d) => ({ value: String(d), label: t(`weekday${d}` as MentorKey) }))]} />
      <div className="flex gap-2 sm:col-span-2">
        <Button type="submit" loading={busy} disabled={!exam || !date}>{t('createPlan')}</Button>
        {onCancel && <Button variant="ghost" onClick={onCancel}>{t('cancel')}</Button>}
      </div>
    </form>
  );
}

export function CountdownLine({ c }: { c: Countdown }) {
  const t = useMentorT();
  if (c.days_remaining < 0) return <>{t('examPassed')}</>;
  if (c.days_remaining === 0) return <>{t('examToday')}</>;
  return <>{c.days_remaining === 1 ? t('dayLeft') : t('daysLeft', { n: c.days_remaining })}</>;
}
