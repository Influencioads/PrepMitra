import toast from 'react-hot-toast';
import { Card, CardBody, CardHeader, Input, Select, Switch } from '@/components/ui';
import { NeedsBackend } from '@/components/mentor/MentorUi';
import { useMentorT, type MentorKey } from '@/components/mentor/format';
import { errorMessage, mentorService, type ReminderPrefs } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useEffect, useState } from 'react';

const SLOTS: { on: keyof ReminderPrefs; at: keyof ReminderPrefs; label: MentorKey }[] = [
  { on: 'morning_enabled', at: 'morning_time', label: 'morning' },
  { on: 'afternoon_enabled', at: 'afternoon_time', label: 'afternoon' },
  { on: 'evening_enabled', at: 'evening_time', label: 'evening' },
];

/** Mentor reminder times, channels and the daily cap (saved on the backend; the scheduler reads them). */
export function ReminderSettingsCard() {
  const t = useMentorT();
  const loaded = useAsync(() => mentorService.reminderPrefs(), []);
  const [p, setP] = useState<ReminderPrefs>();
  useEffect(() => setP(loaded.data), [loaded.data]);
  const save = async (patch: Partial<ReminderPrefs>) => {
    if (!p) return;
    const prev = p;
    setP({ ...p, ...patch });
    try {
      setP(await mentorService.saveReminderPrefs(patch));
      toast.success(t('saved'));
    } catch (e) {
      setP(prev);
      toast.error(errorMessage(e));
    }
  };
  return (
    <Card>
      <CardHeader title={t('remindersTitle')} description={t('remindersDesc')} />
      <CardBody>
        {loaded.error ? <NeedsBackend error={loaded.error} /> : !p ? null : (
          <div className="divide-y divide-line">
            {SLOTS.map((s) => (
              <div key={s.on} className="flex items-center gap-3">
                <div className="flex-1"><Switch label={t(s.label)} checked={Boolean(p[s.on])} onChange={(v) => save({ [s.on]: v })} /></div>
                <Input type="time" aria-label={t(s.label)} className="w-28" value={String(p[s.at])} disabled={!p[s.on]}
                  onChange={(e) => e.target.value && save({ [s.at]: e.target.value })} />
              </div>
            ))}
            <Switch label={t('countdown')} checked={p.countdown_enabled} onChange={(v) => save({ countdown_enabled: v })} />
            <Switch label={t('mockReminders')} checked={p.mock_reminders_enabled} onChange={(v) => save({ mock_reminders_enabled: v })} />
            <Switch label={t('pushChannel')} checked={p.push_enabled} onChange={(v) => save({ push_enabled: v })} />
            <Switch label={t('emailChannel')} checked={p.email_enabled} onChange={(v) => save({ email_enabled: v })} />
            <div className="flex items-center justify-between gap-3 py-3">
              <span className="text-sm font-medium text-ink">{t('maxPerDay')}</span>
              <Select aria-label={t('maxPerDay')} className="w-20" value={String(p.max_per_day)} onChange={(e) => save({ max_per_day: Number(e.target.value) })}
                options={[1, 2, 3, 4, 5].map((n) => ({ value: String(n), label: String(n) }))} />
            </div>
          </div>
        )}
      </CardBody>
    </Card>
  );
}
