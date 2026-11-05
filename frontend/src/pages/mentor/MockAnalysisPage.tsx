import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { CircleAlert, Lightbulb, ThumbsUp } from 'lucide-react';
import { Badge, Button, ButtonLink, Card, CardBody, CardHeader, LoadingSkeleton, MarksLeak, MitraSays, PageHeader, type BadgeTone } from '@/components/ui';
import { NeedsBackend } from '@/components/mentor/MentorUi';
import { marks, mmss, pct, useMentorT, type MentorKey } from '@/components/mentor/format';
import { mentorService, type TimeBand } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

const LEAK_COLOR: Record<string, string> = {
  incorrect_answers: 'bg-red-500', negative_marking: 'bg-orange-400', unattempted: 'bg-stone-400', partially_correct: 'bg-amber-300',
};
const BAND_TONE: Record<TimeBand, BadgeTone> = {
  efficient: 'success', slow_correct: 'warning', time_sink: 'danger', rushed_wrong: 'danger', wrong: 'danger',
  skipped_after_time: 'warning', skipped: 'neutral', unseen: 'neutral',
};

export function MockAnalysisPage() {
  const t = useMentorT();
  useDocumentTitle(t('analysisTitle'));
  const { attemptId = '' } = useParams();
  const a = useAsync(() => mentorService.analysis(attemptId), [attemptId]);
  const note = useAsync(() => mentorService.coachNote(attemptId), [attemptId]);
  const [all, setAll] = useState(false);

  if (a.loading && !a.data) return <LoadingSkeleton variant="page" />;
  if (a.error || !a.data) return <NeedsBackend error={a.error} />;
  const d = a.data;
  const lost = d.marks_lost;
  const penalty = lost.items.find((i) => i.reason === 'negative_marking')?.marks ?? 0;
  // Biggest time problems first: slow-and-wrong, rushed, skipped after time, then everything else by time spent.
  const rank: Record<TimeBand, number> = { time_sink: 0, rushed_wrong: 1, skipped_after_time: 2, slow_correct: 3, wrong: 4, skipped: 5, efficient: 6, unseen: 7 };
  const qs = [...d.time.questions].sort((x, y) => rank[x.band] - rank[y.band] || y.time_sec - x.time_sec);
  const shown = all ? qs : qs.slice(0, 12);

  return (
    <div className="space-y-6">
      <PageHeader eyebrow={<span className="text-sm text-muted">{d.exam.name}</span>} title={t('analysisTitle')} description={t('analysisDesc')}
        actions={d.report_id ? <ButtonLink to={`/reports/${d.report_id}`} variant="outline">{t('fullReport')}</ButtonLink> : undefined} />

      <div className="grid gap-6 xl:grid-cols-[1fr_1.2fr]">
        <div className="space-y-4">
          <Card className="p-5">
            <p className="text-sm text-muted">{t('scoredOf', { score: marks(d.score), max: marks(d.max_score) })}</p>
            <p className="mt-1 font-display text-4xl font-extrabold">{marks(d.score)}<span className="text-xl text-muted"> / {marks(d.max_score)}</span></p>
            <p className="mt-1 text-sm text-muted">{t('accuracy')}: {pct(d.accuracy)} · {d.counts.correct}✓ {d.counts.wrong}✗ {d.counts.unanswered}–{d.percentile !== null && ` · P${Math.round(d.percentile)}`}</p>
          </Card>
          <MarksLeak title={t('whereMarksWent', { n: marks(lost.total_lost) })}
            items={lost.items.map((i) => ({ label: `${t(`r_${i.reason}` as MentorKey)} (${i.questions})`, marks: i.marks, color: LEAK_COLOR[i.reason] ?? 'bg-stone-300' }))}
            note={d.negative_marking && penalty > 0 ? <p className="text-sm text-muted">{t('grossNote', { n: marks(lost.gross_lost_before_penalty), p: marks(penalty) })}</p> : undefined} />
        </div>
        <div className="space-y-4">
          {note.data?.note && <MitraSays>{note.data.note}</MitraSays>}
          <Card>
            <CardHeader title={t('sectionTable')} />
            <div className="overflow-x-auto">
              <table className="w-full min-w-[480px] text-sm">
                <thead className="text-left text-xs uppercase tracking-wide text-muted">
                  <tr className="border-b border-line">
                    <th className="px-5 py-2 font-medium">{t('colSubject')}</th>
                    <th className="px-3 py-2 text-right font-medium">{t('colTotal')}</th>
                    <th className="px-3 py-2 text-right font-medium">{t('colScored')}</th>
                    <th className="px-3 py-2 text-right font-medium">{t('colLost')}</th>
                    <th className="px-5 py-2 text-right font-medium">{t('accuracy')}</th>
                  </tr>
                </thead>
                <tbody>
                  {d.sections.map((s) => (
                    <tr key={s.key} className="border-b border-line">
                      <td className="px-5 py-2.5 font-medium">{s.name}</td>
                      <td className="px-3 py-2.5 text-right tabular-nums">{marks(s.total_marks)}</td>
                      <td className="px-3 py-2.5 text-right tabular-nums">{marks(s.scored)}</td>
                      <td className="px-3 py-2.5 text-right tabular-nums text-danger" title={`${marks(s.lost_incorrect)} + ${marks(s.lost_negative)} + ${marks(s.lost_unattempted)}`}>{marks(s.lost)}</td>
                      <td className="px-5 py-2.5 text-right tabular-nums">{pct(s.accuracy)}</td>
                    </tr>
                  ))}
                  <tr className="font-semibold">
                    <td className="px-5 py-2.5">{t('total')}</td>
                    <td className="px-3 py-2.5 text-right tabular-nums">{marks(d.max_score)}</td>
                    <td className="px-3 py-2.5 text-right tabular-nums">{marks(d.score)}</td>
                    <td className="px-3 py-2.5 text-right tabular-nums text-danger">{marks(lost.total_lost)}</td>
                    <td className="px-5 py-2.5 text-right tabular-nums">{pct(d.accuracy)}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </Card>
          <Card>
            <CardHeader title={t('topicLoss')} />
            <CardBody>
              <ul className="space-y-1.5 text-sm">
                {d.topics.filter((x) => x.marks_lost > 0).slice(0, 8).map((x) => (
                  <li key={x.topic_id} className="flex items-center justify-between gap-3">
                    <span className="min-w-0 truncate">{x.topic}</span>
                    <span className="shrink-0 tabular-nums text-muted">{x.correct}/{x.questions} · <b className="text-danger">−{marks(x.marks_lost)}</b></span>
                  </li>
                ))}
              </ul>
            </CardBody>
          </Card>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader title={t('observations')} />
          <CardBody>
            <ul className="space-y-2.5 text-sm">
              {d.time.observations.map((o, i) => (
                <li key={i} className="flex gap-2">
                  {o.severity === 'positive' ? <ThumbsUp className="mt-0.5 h-4 w-4 shrink-0 text-success" aria-hidden /> : <CircleAlert className={cn('mt-0.5 h-4 w-4 shrink-0', o.severity === 'high' ? 'text-danger' : 'text-amber-600')} aria-hidden />}
                  <span>{o.text}</span>
                </li>
              ))}
            </ul>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={t('aiRecs')} />
          <CardBody>
            <ul className="space-y-2.5 text-sm">
              {d.recommendations.map((r) => (
                <li key={r.text} className="flex gap-2"><Lightbulb className="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden /><span>{r.text}</span></li>
              ))}
            </ul>
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardHeader title={t('timeTitle')} description={t('timeDesc')} />
        <div className="overflow-x-auto">
          <table className="w-full min-w-[560px] text-sm">
            <thead className="text-left text-xs uppercase tracking-wide text-muted">
              <tr className="border-b border-line">
                <th className="px-5 py-2 font-medium">{t('colQ')}</th>
                <th className="px-3 py-2 font-medium">{t('colTopic')}</th>
                <th className="px-3 py-2 text-right font-medium">{t('colTime')}</th>
                <th className="px-3 py-2 text-right font-medium">{t('colTarget')}</th>
                <th className="px-5 py-2 font-medium">{t('colResult')}</th>
              </tr>
            </thead>
            <tbody>
              {shown.map((q) => (
                <tr key={q.ref} className="border-b border-line last:border-0">
                  <td className="px-5 py-2 tabular-nums">Q{q.ref}</td>
                  <td className="px-3 py-2">{q.topic} <span className="text-xs text-muted">· {q.difficulty}</span></td>
                  <td className={cn('px-3 py-2 text-right tabular-nums', (q.time_ratio ?? 0) > 1.5 && 'font-semibold text-danger')}>{mmss(q.time_sec)}</td>
                  <td className="px-3 py-2 text-right tabular-nums text-muted">{mmss(q.target_sec)}</td>
                  <td className="px-5 py-2"><Badge tone={BAND_TONE[q.band]}>{t(`b_${q.band}` as MentorKey)}</Badge></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {qs.length > 12 && <div className="p-4"><Button variant="ghost" size="sm" onClick={() => setAll((v) => !v)}>{all ? t('showLess') : t('showAll', { n: qs.length })}</Button></div>}
      </Card>
    </div>
  );
}
