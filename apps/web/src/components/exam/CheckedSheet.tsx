import type { ExamReport } from '@prepmitra/shared';
import { formatDate, formatDuration } from '@prepmitra/shared';
import { Button, MarksLeak, MitraSays, PenNote, PenScore, Stamp } from '@/components/ui';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { reportMessages } from '@/i18n/messages/report';

const trim = (n: number) => Math.round(n * 100) / 100;

/** Marks-leak breakdown from the code-computed result (never from AI text). */
export function leakItems(report: ExamReport, t: ReturnType<typeof useT<typeof reportMessages.en>>) {
  const r = report.result;
  const wrong = r.questions.filter((q) => q.outcome === 'incorrect');
  const skipped = r.questions.filter((q) => q.outcome === 'unanswered');
  return [
    { label: t('leakSkipped', { n: skipped.length }), marks: trim(skipped.reduce((s, q) => s + q.maxMarks, 0)), color: 'bg-pen' },
    { label: t('leakWrong', { n: wrong.length }), marks: trim(wrong.reduce((s, q) => s + q.maxMarks, 0)), color: 'bg-accent' },
    { label: t('leakNegative'), marks: trim(r.negativeMarksLost), color: 'bg-[#7E22CE]' },
  ].sort((a, b) => b.marks - a.marks);
}

function heatClass(accuracy: number) {
  if (accuracy >= 90) return 'bg-success text-white';
  if (accuracy >= 70) return 'bg-sticky-green text-ink';
  if (accuracy >= 50) return 'bg-[#FFD9A8] text-ink';
  if (accuracy >= 30) return 'bg-accent text-ink';
  return 'bg-pen text-white';
}

/**
 * The report as a teacher-checked answer sheet: red-pen score, percentile stamp,
 * margin notes, then where the marks leaked and a topic heat strip.
 */
export function CheckedSheet({ report, studentName, onOpenPlan, className }: { report: ExamReport; studentName?: string; onOpenPlan?: () => void; className?: string }) {
  const t = useT(reportMessages);
  const r = report.result;
  const praise = r.percentage >= 75 ? t('praiseHigh') : r.percentage >= 50 ? t('praiseMid') : t('praiseLow');
  const items = leakItems(report, t);
  const anyLeak = items.some((i) => i.marks > 0);
  const weak = report.weaknesses[0];
  const loophole = report.loopholes[0];
  const strength = report.strengths[0];
  const day1 = report.improvementPlan[0];
  const topics = [...r.topics].sort((a, b) => a.accuracy - b.accuracy).slice(0, 8);

  return (
    <section aria-label={t('sheetTitle')} className={cn('grid gap-6 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,1fr)]', className)}>
      {/* Checked sheet */}
      <div className="relative overflow-hidden rounded-[10px] border-[1.5px] border-ink bg-ruled p-5 shadow-hard [--margin-x:22px] sm:p-8 sm:pl-14">
        <span className="absolute inset-y-0 left-[22px] hidden w-[1.5px] bg-pen/30 sm:block sm:left-10" aria-hidden />
        <p className="text-xs uppercase tracking-[0.14em] text-muted">{formatDate(report.createdAt)} · {formatDuration(report.timeTakenSec)}</p>
        <h2 className="mt-1 text-2xl font-extrabold sm:text-3xl">{studentName ? `${studentName} · ` : ''}{report.examTitle}</h2>

        <div className="mt-6 flex flex-wrap items-center justify-between gap-x-6 gap-y-4">
          <PenScore score={`${r.score}`} total={r.maxScore} size="lg" />
          <div className="flex flex-col items-center gap-3">
            <p className="-rotate-6 font-hand text-2xl font-bold text-pen sm:text-3xl">{praise}</p>
            <Stamp value={`${report.percentile}`} label={t('percentileEst')} />
          </div>
        </div>
        <p className="mt-5 text-base">
          <b className="text-lg text-success">{r.correct}</b> {t('correct').toLowerCase()} · <b className="text-lg text-pen">{r.incorrect}</b> {t('incorrect').toLowerCase()} · <b className="text-lg">{r.unanswered}</b> {t('unanswered').toLowerCase()} · <b className="text-lg">{r.accuracy}%</b> {t('accuracy').toLowerCase()}
        </p>

        <ol className="mt-6 space-y-4">
          {weak && (
            <li className="flex gap-3">
              <span className="mt-1 flex h-7 w-7 shrink-0 items-center justify-center rounded-full border-[2.5px] border-pen text-xs font-extrabold text-pen" aria-hidden>1</span>
              <PenNote><b>{weak.topic}:</b> {weak.note}</PenNote>
            </li>
          )}
          {loophole && (
            <li className="flex gap-3">
              <span className="mt-1 flex h-7 w-7 shrink-0 items-center justify-center rounded-full border-[2.5px] border-pen text-xs font-extrabold text-pen" aria-hidden>{weak ? 2 : 1}</span>
              <PenNote><b>{loophole.title}:</b> {loophole.detail}</PenNote>
            </li>
          )}
          {strength && (
            <li className="flex gap-3">
              <span className="mt-1 flex h-7 w-7 shrink-0 items-center justify-center rounded-full border-[2.5px] border-secondary text-xs font-extrabold text-secondary" aria-hidden>✓</span>
              <PenNote tone="green">{strength}</PenNote>
            </li>
          )}
        </ol>
        <p className="mt-6 text-xs text-subtle">{t('codeNote')}</p>
      </div>

      {/* Leak + heat + Mitra */}
      <div className="flex min-w-0 flex-col gap-6">
        <MarksLeak
          title={t('leakTitle')}
          items={items}
          note={<p className="rounded-xl bg-primary-soft px-4 py-2.5 font-hand text-lg text-primary-hover">{anyLeak ? t('leakTip') : t('noLeak')}</p>}
        />
        {topics.length > 0 && (
          <section className="rounded-[20px] border border-line bg-card p-5">
            <h3 className="text-lg font-bold">{t('heatTitle')}</h3>
            <p className="mt-0.5 text-sm text-muted">{t('heatDesc')}</p>
            <ul className="mt-4 grid grid-cols-[repeat(auto-fill,minmax(92px,1fr))] gap-2">
              {topics.map((tp) => (
                <li key={tp.topic} className={cn('rounded-xl px-2 py-3 text-center', heatClass(tp.accuracy))}>
                  <p className="font-display text-xl font-extrabold leading-none">{tp.correct}/{tp.total}</p>
                  <p className="mt-1.5 line-clamp-2 text-[11px] font-semibold leading-tight">{tp.topic}</p>
                </li>
              ))}
            </ul>
          </section>
        )}
        {day1 && (
          <div className="rounded-[20px] bg-chalkboard p-5 shadow-wood">
            <MitraSays tone="chalk" size={44} className="[&>p]:bg-transparent [&>p]:p-0 [&>p]:shadow-none">{t('mitraPlanNote', { title: day1.title })}</MitraSays>
            {onOpenPlan && (
              <Button onClick={onOpenPlan} className="mt-4 bg-accent text-chalk-deep hover:bg-[#F7A04A]">{t('openPlan')}</Button>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
