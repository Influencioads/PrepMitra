import type { SectionResult } from '@prepmitra/shared';
import { formatDuration } from '@prepmitra/shared';
import { Badge } from '@/components/ui';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { reportMessages } from '@/i18n/messages/report';

const trim = (n: number) => Math.round(n * 100) / 100;
const attemptedOf = (s: SectionResult) => s.attempted ?? s.correct + s.incorrect;

function AccuracyCell({ s }: { s: SectionResult }) {
  const t = useT(reportMessages);
  if (attemptedOf(s) === 0) return <span className="text-xs text-subtle">{t('notAttemptedShort')}</span>;
  return <Badge tone={s.accuracy >= 75 ? 'success' : s.accuracy >= 50 ? 'warning' : 'danger'}>{s.accuracy}%</Badge>;
}

/**
 * Section-wise table (report part 1): attempted, correct, wrong, skipped, score, accuracy and time
 * per section, with a total row. A stacked list replaces the table on phones.
 */
export function SectionTable({ sections, className }: { sections: SectionResult[]; className?: string }) {
  const t = useT(reportMessages);
  const sum = (f: (s: SectionResult) => number) => trim(sections.reduce((a, s) => a + f(s), 0));
  const total = {
    attempted: sum(attemptedOf), correct: sum((s) => s.correct), incorrect: sum((s) => s.incorrect), unanswered: sum((s) => s.unanswered),
    score: sum((s) => s.score), maxScore: sum((s) => s.maxScore), time: sum((s) => s.timeSpentSec),
  };
  const head = 'px-3 py-2 text-right font-medium first:pl-0 first:text-left';
  const cell = 'px-3 py-2.5 text-right tabular-nums';
  return (
    <div className={className}>
      <div className="hidden overflow-x-auto sm:block">
        <table className="w-full min-w-[560px] text-sm" data-testid="section-table">
          <thead>
            <tr className="border-b border-line text-muted">
              <th scope="col" className={head}>{t('colSection')}</th>
              <th scope="col" className={head}>{t('colAttempted')}</th>
              <th scope="col" className={head}>{t('colCorrect')}</th>
              <th scope="col" className={head}>{t('colWrong')}</th>
              <th scope="col" className={head}>{t('colSkipped')}</th>
              <th scope="col" className={head}>{t('colScore')}</th>
              <th scope="col" className={head}>{t('colAccuracy')}</th>
              <th scope="col" className={cn(head, 'pr-0')}>{t('colTime')}</th>
            </tr>
          </thead>
          <tbody>
            {sections.map((s) => (
              <tr key={s.sectionId} className="border-b border-line">
                <th scope="row" className="py-2.5 pr-3 text-left font-medium">{s.name}</th>
                <td className={cell}>{attemptedOf(s)}</td>
                <td className={cn(cell, 'text-success')}>{s.correct}</td>
                <td className={cn(cell, 'text-danger')}>{s.incorrect}</td>
                <td className={cn(cell, 'text-muted')}>{s.unanswered}</td>
                <td className={cn(cell, 'font-semibold')}>{trim(s.score)}/{trim(s.maxScore)}</td>
                <td className={cell}><AccuracyCell s={s} /></td>
                <td className={cn(cell, 'pr-0 text-muted')}>{formatDuration(s.timeSpentSec)}</td>
              </tr>
            ))}
          </tbody>
          {sections.length > 1 && (
            <tfoot>
              <tr className="font-semibold">
                <th scope="row" className="py-2.5 pr-3 text-left">{t('sectionTotal')}</th>
                <td className={cell}>{total.attempted}</td>
                <td className={cn(cell, 'text-success')}>{total.correct}</td>
                <td className={cn(cell, 'text-danger')}>{total.incorrect}</td>
                <td className={cn(cell, 'text-muted')}>{total.unanswered}</td>
                <td className={cell}>{total.score}/{total.maxScore}</td>
                <td className={cell} />
                <td className={cn(cell, 'pr-0 text-muted')}>{formatDuration(total.time)}</td>
              </tr>
            </tfoot>
          )}
        </table>
      </div>
      <ul className="space-y-2 sm:hidden">
        {sections.map((s) => (
          <li key={s.sectionId} className="rounded-xl border border-line p-3">
            <div className="flex items-center justify-between gap-2">
              <p className="text-sm font-semibold">{s.name}</p>
              <AccuracyCell s={s} />
            </div>
            <p className="mt-1 text-sm"><b>{trim(s.score)}</b><span className="text-muted">/{trim(s.maxScore)} · {formatDuration(s.timeSpentSec)}</span></p>
            <dl className="mt-2 grid grid-cols-4 gap-1 text-center text-xs">
              {[
                [t('colAttempted'), attemptedOf(s), ''],
                [t('colCorrect'), s.correct, 'text-success'],
                [t('colWrong'), s.incorrect, 'text-danger'],
                [t('colSkipped'), s.unanswered, 'text-muted'],
              ].map(([label, v, tone]) => (
                <div key={String(label)} className="rounded-lg bg-surface px-1 py-1.5">
                  <dt className="text-subtle">{label}</dt>
                  <dd className={cn('font-semibold tabular-nums', String(tone))}>{v}</dd>
                </div>
              ))}
            </dl>
          </li>
        ))}
      </ul>
    </div>
  );
}
