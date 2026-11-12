import { useEffect, useRef, useState } from 'react';
import { AnimatePresence, motion, useInView, useReducedMotion, useSpring, useTransform } from 'framer-motion';
import { Check, Clock, LayoutGrid, RotateCcw, Target } from 'lucide-react';
import { HandEyebrow } from '@/components/ui';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { homeMessages } from '@/i18n/messages/home';
import { SparkBurst } from './HomeFx';


/** Sample numbers (labelled on screen): IBPS PO Prelims, out of 100. */
const BEFORE = 61.25;
const CUTOFF = 63.75;
const LEAKS = [
  { key: 'leak1', marks: 4, Icon: LayoutGrid, tone: 'pen' },
  { key: 'leak2', marks: 2, Icon: Clock, tone: 'accent' },
  { key: 'leak3', marks: 1.25, Icon: Target, tone: 'purple' },
] as const;
const RECOVERED = LEAKS.reduce((s, l) => s + l.marks, 0); // 7.25
const AFTER = BEFORE + RECOVERED; // 68.5

/** The track shows 40–80 so the gap to the cut-off is easy to see. */
const MIN = 40;
const MAX = 80;
const pct = (v: number) => ((v - MIN) / (MAX - MIN)) * 100;
const fmt = (v: number) => (Number.isInteger(v) ? String(v) : v.toFixed(2).replace(/0$/, ''));

const TONE: Record<(typeof LEAKS)[number]['tone'], { chip: string; text: string }> = {
  pen: { chip: 'bg-[#FCE7EC] text-pen', text: 'text-pen' },
  accent: { chip: 'bg-accent-soft text-[#B45309]', text: 'text-[#B45309]' },
  purple: { chip: 'bg-sticky-purple text-[#7E22CE]', text: 'text-[#7E22CE]' },
};

/**
 * "The 0.25 game": the same student's score after mock 1 and after the 7-day plan, on one track
 * against the cut-off flag. Plays once when scrolled into view; the viewer can flip or replay it.
 */
export function CutoffMeter() {
  const t = useT(homeMessages);
  const ref = useRef<HTMLDivElement>(null);
  const seen = useInView(ref, { once: true, amount: 0.4 });
  const reduce = useReducedMotion();
  const [after, setAfter] = useState(false);
  const [touched, setTouched] = useState(false);
  const [run, setRun] = useState(0);

  // Autoplay: show the mock-1 score, then the plan's effect.
  useEffect(() => {
    if (!seen || touched) return;
    const id = window.setTimeout(() => setAfter(true), reduce ? 500 : 1700);
    return () => window.clearTimeout(id);
  }, [seen, touched, reduce, run]);

  const target = !seen ? MIN : after ? AFTER : BEFORE;
  const score = useSpring(MIN, { stiffness: 60, damping: 17 });
  useEffect(() => score.set(target), [score, target]);
  const left = useTransform(score, (v) => `${pct(v)}%`);
  const label = useTransform(score, (v) => v.toFixed(2));

  const gap = Math.abs((after ? AFTER : BEFORE) - CUTOFF);
  const lo = Math.min(after ? AFTER : BEFORE, CUTOFF);
  const hi = Math.max(after ? AFTER : BEFORE, CUTOFF);

  const pick = (v: boolean) => {
    setTouched(true);
    setAfter(v);
  };
  const replay = () => {
    setTouched(false);
    setAfter(false);
    setRun((r) => r + 1);
  };

  return (
    <section id="cutoff" className="container-page scroll-mt-20 pb-16 lg:pb-24">
      {/* ---------- Heading ---------- */}
      <div className="grid items-end gap-6 lg:grid-cols-[1.2fr_1fr] lg:gap-12">
        <div>
          <HandEyebrow tone="pen">{t('cutEyebrow')}</HandEyebrow>
          <h2 className="mt-1 text-balance text-3xl font-extrabold leading-tight sm:text-[2.6rem]">
            <span className="text-pen">{t('cutTitle1')}</span>
            <br />
            <span className="text-secondary">{t('cutTitle2')}</span>
          </h2>
        </div>
        <p className="max-w-md text-lg leading-relaxed text-muted lg:justify-self-end">{t('cutBody')}</p>
      </div>

      {/* ---------- The board ---------- */}
      <div
        ref={ref}
        className="relative mt-10 overflow-hidden rounded-[28px] border-2 border-ink bg-card bg-[radial-gradient(circle,rgba(28,35,33,0.06)_1px,transparent_1px)] p-5 shadow-hard [background-size:18px_18px] sm:p-8 lg:p-10"
      >
        <motion.span
          className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full blur-3xl"
          animate={{ backgroundColor: after ? 'rgba(30,94,71,0.16)' : 'rgba(215,38,61,0.12)' }}
          transition={{ duration: 0.7 }}
          aria-hidden
        />

        {/* top row: switch + replay */}
        <div className="relative flex flex-wrap items-center justify-between gap-3">
          <div role="group" aria-label={t('cutToggle')} className="inline-flex rounded-full border-[1.5px] border-ink bg-paper p-1">
            {[false, true].map((v) => (
              <button
                key={String(v)}
                type="button"
                aria-pressed={after === v}
                onClick={() => pick(v)}
                className={cn('relative rounded-full px-4 py-2 text-sm font-bold transition-colors sm:px-5', after === v ? 'text-white' : 'text-ink hover:text-primary')}
              >
                {after === v && (
                  <motion.span layoutId="cut-pill" className={cn('absolute inset-0 rounded-full', v ? 'bg-secondary' : 'bg-pen')} transition={{ type: 'spring', stiffness: 400, damping: 32 }} />
                )}
                <span className="relative">{v ? t('cutAfter') : t('cutBefore')}</span>
              </button>
            ))}
          </div>
          <button type="button" onClick={replay} className="inline-flex items-center gap-1.5 rounded-full px-3 py-2 text-sm font-bold text-muted transition-colors hover:text-ink">
            <RotateCcw className="h-4 w-4" aria-hidden />
            {t('cutReplay')}
          </button>
        </div>

        {/* score + stamp */}
        <div className="relative mt-7 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-muted">{t('cutYou')}</p>
            <p className="font-display text-6xl font-extrabold leading-none tabular-nums tracking-tight sm:text-7xl">
              <motion.span>{label}</motion.span>
              <span className="ml-1 text-2xl text-subtle sm:text-3xl">/100</span>
            </p>
          </div>
          <AnimatePresence mode="wait" initial={false}>
            <motion.span
              key={after ? 'clear' : 'short'}
              initial={{ opacity: 0, scale: 1.5, rotate: after ? -14 : 10 }}
              animate={{ opacity: 1, scale: 1, rotate: after ? -5 : 3 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ type: 'spring', stiffness: 380, damping: 17 }}
              className={cn(
                'relative mb-1 rounded-xl border-[3px] px-4 py-2 text-base font-extrabold uppercase tracking-wide sm:text-lg',
                after ? 'border-secondary text-secondary' : 'border-pen text-pen',
              )}
              aria-live="polite"
            >
              {after ? t('cutClear', { n: fmt(gap) }) : t('cutShort', { n: fmt(gap) })}
              {after && <SparkBurst />}
            </motion.span>
          </AnimatePresence>
        </div>

        {/* ---------- Track ---------- */}
        <div className="relative mt-10 pb-16 pt-12" aria-hidden>
          {/* cut-off flag (above the bar) */}
          <div className="absolute bottom-16 top-0 -translate-x-1/2" style={{ left: `${pct(CUTOFF)}%` }}>
            <span className="absolute left-1/2 top-0 -translate-x-1/2 whitespace-nowrap rounded-md bg-pen px-2 py-1 text-xs font-extrabold text-white shadow-sm">
              {t('cutLine', { n: fmt(CUTOFF) })}
            </span>
            <span className="absolute bottom-[-6px] left-1/2 top-7 w-0.5 -translate-x-1/2 bg-pen" />
          </div>

          {/* bar */}
          <div className="relative h-5 overflow-hidden rounded-full border-[1.5px] border-ink bg-paper">
            <motion.div className={cn('absolute inset-y-0 left-0 rounded-full transition-colors duration-500', after ? 'bg-secondary' : 'bg-accent')} style={{ width: left }} />
            {/* the gap to the cut-off, striped */}
            <motion.div
              className={cn(
                'absolute inset-y-0 transition-colors duration-500',
                after
                  ? 'bg-[repeating-linear-gradient(45deg,rgba(255,255,255,0.35)_0_6px,transparent_6px_12px)]'
                  : 'bg-[repeating-linear-gradient(45deg,rgba(215,38,61,0.35)_0_6px,transparent_6px_12px)]',
              )}
              initial={false}
              animate={{ left: `${pct(lo)}%`, width: `${pct(hi) - pct(lo)}%`, opacity: seen ? 1 : 0 }}
              transition={{ type: 'spring', stiffness: 60, damping: 17 }}
            />
          </div>

          {/* "you" marker (below the bar) */}
          <motion.div className="absolute top-[70px] -translate-x-1/2" style={{ left }}>
            <span className={cn('mx-auto block h-0 w-0 border-x-[7px] border-b-[9px] border-x-transparent transition-colors duration-500', after ? 'border-b-secondary' : 'border-b-accent')} />
            <span className={cn('block whitespace-nowrap rounded-full px-2.5 py-1 text-xs font-extrabold text-white shadow-sm transition-colors duration-500', after ? 'bg-secondary' : 'bg-accent')}>
              {t('cutYouTag')}
            </span>
          </motion.div>

          {/* scale */}
          <div className="absolute inset-x-0 bottom-0 flex justify-between text-[11px] font-semibold tabular-nums text-subtle">
            {[40, 50, 60, 70, 80].map((n) => (
              <span key={n} className="relative">
                <span className="absolute -top-2 left-1/2 h-1.5 w-px -translate-x-1/2 bg-line-strong" />
                {n}
              </span>
            ))}
          </div>
        </div>

        {/* ---------- Leak tickets ---------- */}
        <div className="mt-4 flex items-baseline justify-between gap-3 border-t-2 border-dashed border-line-strong pt-6">
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-muted">{t('cutLeaksTitle')}</p>
          <p className="text-sm font-bold">
            <span className="text-muted">{t('cutRecovered')}: </span>
            <motion.span key={after ? 'a' : 'b'} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className={after ? 'text-secondary' : 'text-subtle'}>
              {after ? `+${fmt(RECOVERED)}` : '0'}
            </motion.span>
          </p>
        </div>
        <ul className="mt-4 grid gap-3 sm:grid-cols-3">
          {LEAKS.map((l, i) => {
            const tone = TONE[l.tone];
            return (
              <motion.li
                key={l.key}
                className={cn(
                  'relative flex items-center gap-3 overflow-hidden rounded-2xl border-[1.5px] p-4 transition-colors duration-500',
                  after ? 'border-secondary/40 bg-secondary-soft' : 'border-line-strong bg-paper',
                )}
                animate={after ? { y: [0, -6, 0] } : { y: 0 }}
                transition={{ duration: 0.45, delay: 0.25 + i * 0.15 }}
              >
                <span className={cn('relative flex h-10 w-10 shrink-0 items-center justify-center rounded-xl transition-colors duration-500', after ? 'bg-secondary text-white' : tone.chip)}>
                  <AnimatePresence initial={false} mode="wait">
                    {after ? (
                      <motion.span key="ok" initial={{ scale: 0, rotate: -45 }} animate={{ scale: 1, rotate: 0 }} exit={{ scale: 0 }} transition={{ type: 'spring', stiffness: 500, damping: 18, delay: 0.25 + i * 0.15 }}>
                        <Check className="h-5 w-5" strokeWidth={3} />
                      </motion.span>
                    ) : (
                      <motion.span key="ic" initial={{ scale: 0 }} animate={{ scale: 1 }} exit={{ scale: 0 }}>
                        <l.Icon className="h-5 w-5" />
                      </motion.span>
                    )}
                  </AnimatePresence>
                </span>
                <span className="min-w-0 flex-1 text-sm font-semibold leading-snug">{t(l.key)}</span>
                <span className={cn('shrink-0 text-right font-display text-xl font-extrabold tabular-nums transition-colors duration-500', after ? 'text-secondary' : tone.text)}>
                  {after ? `+${fmt(l.marks)}` : `−${fmt(l.marks)}`}
                  <span className="block text-[10px] font-bold uppercase tracking-wide">{after ? t('cutPlugged') : ' '}</span>
                </span>
              </motion.li>
            );
          })}
        </ul>

        <p className="mt-6 text-xs text-muted">{t('cutSample')}</p>
      </div>
    </section>
  );
}
