import { useEffect, useRef, useState } from 'react';
import { AnimatePresence, motion, useInView, useReducedMotion, useSpring, useTransform } from 'framer-motion';
import { Check } from 'lucide-react';
import { HandEyebrow } from '@/components/ui';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { homeMessages } from '@/i18n/messages/home';

const EASE = [0.22, 1, 0.36, 1] as const;

/** Sample numbers (labelled on screen): IBPS PO Prelims, out of 100. */
const BEFORE = 61.25;
const CUTOFF = 63.75;
const LEAKS = [
  { key: 'leak1', marks: 4, dot: 'bg-pen' },
  { key: 'leak2', marks: 2, dot: 'bg-accent' },
  { key: 'leak3', marks: 1.25, dot: 'bg-[#7E22CE]' },
] as const;
const AFTER = BEFORE + LEAKS.reduce((s, l) => s + l.marks, 0); // 68.5

/** The bar shows 40–80 so the gap to the cut-off is easy to see. */
const MIN = 40;
const MAX = 80;
const pct = (v: number) => ((v - MIN) / (MAX - MIN)) * 100;
const fmt = (v: number) => (Number.isInteger(v) ? String(v) : v.toFixed(2).replace(/0$/, ''));

/**
 * "The 0.25 game": one student's score before and after plugging the leaks, against the cut-off line.
 * Plays once when scrolled into view (before → after), then the viewer can flip between the two.
 */
export function CutoffMeter() {
  const t = useT(homeMessages);
  const ref = useRef<HTMLDivElement>(null);
  const seen = useInView(ref, { once: true, amount: 0.45 });
  const reduce = useReducedMotion();
  const [after, setAfter] = useState(false);
  const [touched, setTouched] = useState(false);

  // Autoplay once: show the "before" score, then the plan's effect.
  useEffect(() => {
    if (!seen || touched) return;
    const id = window.setTimeout(() => setAfter(true), reduce ? 600 : 1800);
    return () => window.clearTimeout(id);
  }, [seen, touched, reduce]);

  const target = !seen ? MIN : after ? AFTER : BEFORE;
  const score = useSpring(MIN, { stiffness: 70, damping: 18 });
  useEffect(() => score.set(target), [score, target]);
  const width = useTransform(score, (v) => `${pct(v)}%`);
  const label = useTransform(score, (v) => v.toFixed(2));

  const gap = Math.abs((after ? AFTER : BEFORE) - CUTOFF);
  const pick = (v: boolean) => {
    setTouched(true);
    setAfter(v);
  };

  return (
    <section id="cutoff" className="container-page scroll-mt-20 pb-16 lg:pb-24">
      <div ref={ref} className="grid items-center gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:gap-14">
        <div className="min-w-0">
          <HandEyebrow tone="pen">{t('cutEyebrow')}</HandEyebrow>
          <h2 className="mt-1 text-3xl font-extrabold leading-tight sm:text-[2.6rem]">
            {t('cutTitle1')}
            <br />
            <span className="text-secondary">{t('cutTitle2')}</span>
          </h2>
          <p className="mt-5 text-lg leading-relaxed text-muted">{t('cutBody')}</p>

          {/* Before / after switch */}
          <div role="group" aria-label={t('cutToggle')} className="mt-7 inline-flex rounded-full border-[1.5px] border-ink bg-card p-1">
            {[false, true].map((v) => (
              <button
                key={String(v)}
                type="button"
                aria-pressed={after === v}
                onClick={() => pick(v)}
                className={cn('relative rounded-full px-4 py-2 text-sm font-bold transition-colors sm:px-5', after === v ? 'text-white' : 'text-ink hover:text-primary')}
              >
                {after === v && (
                  <motion.span layoutId="cut-pill" className={cn('absolute inset-0 rounded-full', v ? 'bg-secondary' : 'bg-ink')} transition={{ type: 'spring', stiffness: 400, damping: 32 }} />
                )}
                <span className="relative">{v ? t('cutAfter') : t('cutBefore')}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="min-w-0 rounded-[24px] border-2 border-ink bg-card p-5 shadow-hard sm:p-8">
          {/* Score readout */}
          <div className="flex items-end justify-between gap-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.14em] text-muted">{t('cutYou')}</p>
              <p className="font-display text-5xl font-extrabold tabular-nums tracking-tight sm:text-6xl">
                <motion.span>{label}</motion.span>
              </p>
            </div>
            <AnimatePresence mode="wait" initial={false}>
              <motion.span
                key={after ? 'clear' : 'short'}
                initial={{ opacity: 0, scale: 1.4, rotate: after ? -14 : 8 }}
                animate={{ opacity: 1, scale: 1, rotate: after ? -6 : 3 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ type: 'spring', stiffness: 380, damping: 18 }}
                className={cn(
                  'mb-2 rounded-lg border-[2.5px] px-3 py-1 text-sm font-extrabold uppercase tracking-wide',
                  after ? 'border-secondary text-secondary' : 'border-pen text-pen',
                )}
                aria-live="polite"
              >
                {after ? t('cutClear', { n: fmt(gap) }) : t('cutShort', { n: fmt(gap) })}
              </motion.span>
            </AnimatePresence>
          </div>

          {/* The meter */}
          <div className="relative mt-8 pb-7 pt-7">
            <div className="relative h-5 overflow-hidden rounded-full border-[1.5px] border-ink bg-paper">
              <motion.div className={cn('h-full rounded-full transition-colors duration-500', after ? 'bg-secondary' : 'bg-accent')} style={{ width }} />
            </div>
            {/* cut-off line */}
            <div className="absolute inset-y-0" style={{ left: `${pct(CUTOFF)}%` }} aria-hidden>
              <div className="absolute bottom-5 top-5 -ml-px w-0.5 border-l-2 border-dashed border-pen" />
              <span className="absolute -top-0 -translate-x-1/2 whitespace-nowrap font-hand text-base font-bold text-pen">{t('cutLine', { n: fmt(CUTOFF) })}</span>
            </div>
            {/* scale */}
            <div className="absolute inset-x-0 bottom-0 flex justify-between text-[11px] font-semibold text-muted" aria-hidden>
              {[40, 50, 60, 70, 80].map((n) => <span key={n}>{n}</span>)}
            </div>
          </div>

          {/* Leaks that get plugged */}
          <ul className="mt-6 space-y-2.5">
            {LEAKS.map((l, i) => (
              <li key={l.key} className="flex items-center justify-between gap-3 text-sm">
                <span className="flex min-w-0 items-start gap-2.5">
                  <span className="relative flex h-5 w-5 shrink-0 items-center justify-center">
                    <AnimatePresence initial={false}>
                      {after ? (
                        <motion.span
                          key="ok"
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          exit={{ scale: 0 }}
                          transition={{ type: 'spring', stiffness: 500, damping: 20, delay: 0.15 + i * 0.12 }}
                          className="absolute inset-0 flex items-center justify-center rounded-full bg-secondary text-white"
                        >
                          <Check className="h-3 w-3" strokeWidth={3} />
                        </motion.span>
                      ) : (
                        <motion.span key="dot" initial={{ scale: 0 }} animate={{ scale: 1 }} exit={{ scale: 0 }} className={cn('absolute inset-1 rounded-full', l.dot)} />
                      )}
                    </AnimatePresence>
                  </span>
                  <span className={cn('leading-snug transition-colors duration-300', after && 'text-muted line-through decoration-secondary decoration-2')}>{t(l.key)}</span>
                </span>
                <span className={cn('shrink-0 font-bold tabular-nums transition-colors duration-300', after ? 'text-secondary' : 'text-pen')}>
                  {after ? (<>+{fmt(l.marks)}<span className="hidden sm:inline"> · {t('cutPlugged')}</span></>) : `−${fmt(l.marks)}`}
                </span>
              </li>
            ))}
          </ul>
          <motion.p
            className="mt-5 border-t-2 border-dashed border-line-strong pt-3 text-xs text-muted"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, ease: EASE, delay: 0.3 }}
          >
            {t('cutSample')}
          </motion.p>
        </div>
      </div>
    </section>
  );
}
