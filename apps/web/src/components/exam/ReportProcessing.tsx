import { useEffect, useState } from 'react';
import { CircleCheck, LoaderCircle } from 'lucide-react';
import { ProgressBar } from '@/components/ui';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { examMessages } from '@/i18n/messages/exam';


const STEPS = ['stepScoring', 'stepStrengths', 'stepPlan'] as const;

/**
 * Shown between submit and the result (15-day plan, Day 6). In real mode the report
 * is polled every 3 s; the steps advance on a timer so the screen always shows movement.
 */
export function ReportProcessing({ examTitle, done, stepMs = 800 }: { examTitle: string; done: boolean; stepMs?: number }) {
  const t = useT(examMessages);
  const [step, setStep] = useState(0);
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const started = Date.now();
    const t = window.setInterval(() => {
      const ms = Date.now() - started;
      setElapsed(ms);
      setStep(Math.min(STEPS.length - 1, Math.floor(ms / stepMs)));
    }, 150);
    return () => window.clearInterval(t);
  }, [stepMs]);

  // Ease towards 92% while waiting; jump to 100% when the report is ready.
  const progress = done ? 100 : Math.min(92, Math.round(92 * (1 - Math.exp(-elapsed / (stepMs * 2)))));
  const current = done ? STEPS.length : step;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/95 p-4 backdrop-blur-sm" role="dialog" aria-modal="true" aria-labelledby="processing-title">
      <div className="w-full max-w-md rounded-2xl border border-line bg-card p-6 shadow-overlay sm:p-8">
        <p className="text-sm font-medium text-muted">{examTitle}</p>
        <h2 id="processing-title" className="mt-1 text-2xl font-bold">{t('preparingReport')}</h2>
        <ProgressBar value={progress} className="mt-6" label={t('reportProgress')} showValue />
        <ol className="mt-6 space-y-3" aria-live="polite">
          {STEPS.map((s, i) => {
            const state = i < current ? 'done' : i === current ? 'active' : 'todo';
            return (
              <li key={s} className={cn('flex items-center gap-3 text-sm', state === 'todo' ? 'text-subtle' : 'text-ink')}>
                {state === 'done' ? (
                  <CircleCheck className="h-5 w-5 text-success" aria-label={t('stepDone')} />
                ) : state === 'active' ? (
                  <LoaderCircle className="h-5 w-5 animate-spin text-primary" aria-label={t('stepInProgress')} />
                ) : (
                  <span className="h-5 w-5 rounded-full border-2 border-line-strong" aria-hidden />
                )}
                <span className={cn(state === 'active' && 'font-semibold')}>{t(s)}</span>
              </li>
            );
          })}
        </ol>
        <p className="mt-6 text-xs text-muted">{t('processingNote')}</p>
      </div>
    </div>
  );
}
