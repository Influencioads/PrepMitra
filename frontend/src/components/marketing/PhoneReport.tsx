import { useEffect } from 'react';
import { animate, motion, useMotionValue, useReducedMotion, useTransform } from 'framer-motion';
import { Check, TrendingUp } from 'lucide-react';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { homeMessages } from '@/i18n/messages/home';

const EASE = [0.22, 1, 0.36, 1] as const;
/** Sample numbers, labelled "Sample" on screen. Bar shows 40–80. */
const SCORE = 68.5;
const CUTOFF = 63.75;
const pct = (v: number) => ((v - 40) / 40) * 100;

/** Hero visual: a phone showing a sample report — score, cut-off line and the one thing to fix first. */
export function PhoneReport({ className }: { className?: string }) {
  const t = useT(homeMessages);
  const reduce = useReducedMotion();
  const score = useMotionValue(reduce ? SCORE : 40);
  const label = useTransform(score, (v) => v.toFixed(2));
  const width = useTransform(score, (v) => `${pct(v)}%`);
  useEffect(() => {
    if (reduce) return;
    const c = animate(score, SCORE, { duration: 1.4, ease: EASE, delay: 0.7 });
    return () => c.stop();
  }, [score, reduce]);

  return (
    <div className={cn('relative mx-auto w-full max-w-[280px] sm:max-w-[320px]', className)} aria-hidden>
      {/* soft glow behind the phone */}
      <div className="absolute inset-x-6 top-10 bottom-4 -z-10 rounded-full bg-primary/20 blur-3xl" />

      <motion.div
        initial={{ opacity: 0, y: 40, rotate: 4 }}
        animate={{ opacity: 1, y: 0, rotate: 2 }}
        transition={{ duration: 0.8, ease: EASE, delay: 0.2 }}
      >
        <motion.div
          animate={reduce ? undefined : { y: [0, -8, 0] }}
          transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut', delay: 1.4 }}
          className="rounded-[2.6rem] border-[3px] border-ink bg-ink p-2.5 shadow-[14px_14px_0_rgba(28,35,33,0.12)]"
        >
          <div className="relative overflow-hidden rounded-[2.1rem] bg-paper px-5 pb-6 pt-9">
            {/* notch */}
            <span className="absolute left-1/2 top-2.5 h-5 w-24 -translate-x-1/2 rounded-full bg-ink" />

            <div className="flex items-center justify-between text-[11px] font-bold">
              <span className="text-ink">{t('phoneExam')}</span>
              <span className="rounded-full bg-sticky-yellow px-2 py-0.5 text-[#92400E]">{t('sampleLabel')}</span>
            </div>

            <p className="mt-5 text-[11px] font-bold uppercase tracking-[0.14em] text-muted">{t('phoneScore')}</p>
            <div className="mt-1 flex items-end justify-between gap-2">
              <motion.p className="font-display text-[2.5rem] font-extrabold tabular-nums leading-none tracking-tight text-ink sm:text-5xl">{label}</motion.p>
              <motion.span
                initial={{ opacity: 0, scale: 1.5, rotate: -16 }}
                animate={{ opacity: 1, scale: 1, rotate: -6 }}
                transition={{ type: 'spring', stiffness: 380, damping: 16, delay: 2.1 }}
                className="mb-1.5 whitespace-nowrap rounded-md border-2 border-secondary px-1.5 py-0.5 text-[9px] sm:text-[10px] font-extrabold uppercase text-secondary"
              >
                {t('phoneClear', { n: '4.75' })}
              </motion.span>
            </div>

            {/* score bar with cut-off line */}
            <div className="relative mt-7">
              <span className="absolute -top-5 -translate-x-1/2 whitespace-nowrap font-hand text-sm font-bold text-pen" style={{ left: `${pct(CUTOFF)}%` }}>
                {t('phoneCut', { n: '63.75' })}
              </span>
              <div className="h-3 overflow-hidden rounded-full bg-line">
                <motion.div className="h-full rounded-full bg-secondary" style={{ width }} />
              </div>
              <span className="absolute -top-1 bottom-[-4px] w-0.5 border-l-2 border-dashed border-pen" style={{ left: `${pct(CUTOFF)}%` }} />
            </div>

            {/* fix first */}
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, ease: EASE, delay: 2.4 }}
              className="mt-7 rounded-2xl border-[1.5px] border-ink bg-card p-3.5"
            >
              <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-primary">{t('phoneFix')}</p>
              <div className="mt-1.5 flex items-center justify-between gap-2">
                <span className="whitespace-nowrap text-[13px] font-bold text-ink">{t('phoneFixItem')}</span>
                <span className="flex items-center gap-1 whitespace-nowrap text-[13px] font-extrabold text-secondary">
                  <TrendingUp className="h-4 w-4" />
                  {t('phoneFixGain')}
                </span>
              </div>
            </motion.div>

            {/* tiny day strip */}
            <div className="mt-4 flex items-center gap-1.5">
              {[0, 1, 2, 3, 4, 5, 6].map((d) => (
                <motion.span
                  key={d}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring', stiffness: 500, damping: 20, delay: 2.7 + d * 0.06 }}
                  className={cn('flex h-6 flex-1 items-center justify-center rounded-md text-[10px] font-bold', d < 2 ? 'bg-secondary text-white' : d === 2 ? 'bg-primary text-white' : 'bg-line text-muted')}
                >
                  {d < 2 ? <Check className="h-3 w-3" strokeWidth={3} /> : d + 1}
                </motion.span>
              ))}
            </div>
          </div>
        </motion.div>
      </motion.div>

      {/* one floating tag */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: EASE, delay: 1.2 }}
        className="absolute inset-x-0 -bottom-5 flex justify-center"
      >
        <motion.span
          animate={reduce ? undefined : { y: [0, 6, 0] }}
          transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
          className="flex items-center gap-2 rounded-full border-[1.5px] border-ink bg-card px-3 py-1.5 text-xs font-bold text-ink shadow-hard-sm"
        >
          <span className="h-2 w-2 rounded-full bg-success" />
          {t('phoneTag')}
        </motion.span>
      </motion.div>
    </div>
  );
}
