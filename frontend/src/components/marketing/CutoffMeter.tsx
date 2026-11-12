import { useEffect, useRef, useState } from 'react';
import { AnimatePresence, motion, useInView, useReducedMotion, useSpring, useTransform } from 'framer-motion';
import { Check, Clock, LayoutGrid, RotateCcw, Target } from 'lucide-react';
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

/** On the dark chalkboard band: soft red for "short", bright green for "cleared". */
const SHORT = '#FF8A95';
const CLEAR = '#5EE0A0';
const TONE: Record<(typeof LEAKS)[number]['tone'], { chip: string; text: string }> = {
  pen: { chip: 'bg-[#FF8A95]/15 text-[#FF8A95]', text: 'text-[#FF8A95]' },
  accent: { chip: 'bg-accent/20 text-[#FFB066]', text: 'text-[#FFB066]' },
  purple: { chip: 'bg-[#C084FC]/15 text-[#D8B4FE]', text: 'text-[#D8B4FE]' },
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
    <section id="cutoff" className="relative isolate scroll-mt-20 overflow-hidden bg-chalkboard py-16 text-chalk-text lg:py-24">
      {/* torn paper edges, chalk light, faint grid, giant 0.25 */}
      <svg viewBox="0 0 1200 24" preserveAspectRatio="none" className="absolute inset-x-0 top-0 h-4 w-full text-background" aria-hidden>
        <path d="M0 0h1200v8c-40 10-80-6-120 4s-80 10-120 0-80-8-120 2-80 10-120 0-80-8-120 2-80 10-120 0-80-6-120 4-80 8-120 0-80-6-120 4S40 18 0 8Z" fill="currentColor" />
      </svg>
      <svg viewBox="0 0 1200 24" preserveAspectRatio="none" className="absolute inset-x-0 bottom-0 h-4 w-full rotate-180 text-background" aria-hidden>
        <path d="M0 0h1200v8c-40 10-80-6-120 4s-80 10-120 0-80-8-120 2-80 10-120 0-80-8-120 2-80 10-120 0-80-6-120 4-80 8-120 0-80-6-120 4S40 18 0 8Z" fill="currentColor" />
      </svg>
      <span className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_20%_0%,rgba(255,255,255,0.10),transparent_55%)]" aria-hidden />
      <span className="pointer-events-none absolute inset-0 -z-10 opacity-[0.07] [background-image:linear-gradient(rgba(255,255,255,0.6)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.6)_1px,transparent_1px)] [background-size:44px_44px]" aria-hidden />
      <motion.span
        className="pointer-events-none absolute -right-6 top-6 -z-10 select-none font-display text-[38vw] font-extrabold leading-none tracking-tighter text-white/[0.035] lg:text-[22rem]"
        initial={{ opacity: 0, x: 40 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 1 }}
        aria-hidden
      >
        0.25
      </motion.span>
      <motion.span
        className="pointer-events-none absolute -left-32 bottom-0 -z-10 h-96 w-96 rounded-full blur-3xl"
        animate={{ backgroundColor: after ? 'rgba(94,224,160,0.14)' : 'rgba(255,138,149,0.12)' }}
        transition={{ duration: 0.8 }}
        aria-hidden
      />

      <div ref={ref} className="container-page">
        {/* ---------- Heading + controls ---------- */}
        <div className="grid items-end gap-6 lg:grid-cols-[1.3fr_1fr] lg:gap-12">
          <div>
            <p className="font-hand text-lg text-marigold sm:text-xl">{t('cutEyebrow')} —</p>
            <h2 className="mt-1 text-balance font-display text-[2rem] font-extrabold leading-[1.08] tracking-tight text-chalk-text sm:text-6xl">
              <span style={{ color: SHORT }}>{t('cutTitle1')}</span>
              <br />
              <span style={{ color: CLEAR }}>{t('cutTitle2')}</span>
            </h2>
          </div>
          <div className="lg:justify-self-end">
            <p className="max-w-md text-lg leading-relaxed text-white/75">{t('cutBody')}</p>
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <div role="group" aria-label={t('cutToggle')} className="inline-flex rounded-full border border-white/25 bg-white/10 p-1 backdrop-blur">
                {[false, true].map((v) => (
                  <button
                    key={String(v)}
                    type="button"
                    aria-pressed={after === v}
                    onClick={() => pick(v)}
                    className={cn('relative rounded-full px-4 py-2 text-sm font-bold transition-colors', after === v ? 'text-chalk-deep' : 'text-white/80 hover:text-white')}
                  >
                    {after === v && (
                      <motion.span layoutId="cut-pill" className="absolute inset-0 rounded-full" style={{ backgroundColor: v ? CLEAR : SHORT }} transition={{ type: 'spring', stiffness: 400, damping: 32 }} />
                    )}
                    <span className="relative">{v ? t('cutAfter') : t('cutBefore')}</span>
                  </button>
                ))}
              </div>
              <button type="button" onClick={replay} className="inline-flex items-center gap-1.5 rounded-full px-3 py-2 text-sm font-bold text-white/70 transition-colors hover:text-white">
                <RotateCcw className="h-4 w-4" aria-hidden />
                {t('cutReplay')}
              </button>
            </div>
          </div>
        </div>

        {/* ---------- Score + stamp ---------- */}
        <div className="mt-12 flex flex-wrap items-end justify-between gap-4 border-t border-white/15 pt-8">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.18em] text-white/55">{t('cutYou')}</p>
            <p className="font-display text-7xl font-extrabold leading-none tabular-nums tracking-tight sm:text-8xl">
              <motion.span>{label}</motion.span>
              <span className="ml-1 text-2xl text-white/40 sm:text-3xl">/100</span>
            </p>
          </div>
          <AnimatePresence mode="wait" initial={false}>
            <motion.span
              key={after ? 'clear' : 'short'}
              initial={{ opacity: 0, scale: 1.5, rotate: after ? -14 : 10 }}
              animate={{ opacity: 1, scale: 1, rotate: after ? -5 : 3 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ type: 'spring', stiffness: 380, damping: 17 }}
              className="relative mb-2 rounded-xl border-[3px] px-4 py-2 text-lg font-extrabold uppercase tracking-wide sm:text-xl"
              style={{ borderColor: after ? CLEAR : SHORT, color: after ? CLEAR : SHORT }}
              aria-live="polite"
            >
              {after ? t('cutClear', { n: fmt(gap) }) : t('cutShort', { n: fmt(gap) })}
              {after && <SparkBurst color="bg-[#5EE0A0]" />}
            </motion.span>
          </AnimatePresence>
        </div>

        {/* ---------- Track (full container width) ---------- */}
        <div className="relative mt-10 pb-16 pt-12" aria-hidden>
          <div className="absolute bottom-16 top-0 -translate-x-1/2" style={{ left: `${pct(CUTOFF)}%` }}>
            <span className="absolute left-1/2 top-0 -translate-x-1/2 whitespace-nowrap rounded-md bg-pen px-2.5 py-1 text-xs font-extrabold text-white shadow-[0_4px_14px_rgba(215,38,61,0.45)]">
              {t('cutLine', { n: fmt(CUTOFF) })}
            </span>
            <span className="absolute bottom-[-8px] left-1/2 top-7 w-0.5 -translate-x-1/2 bg-pen" />
          </div>

          <div className="relative h-6 overflow-hidden rounded-full border border-white/30 bg-white/10">
            <motion.div className="absolute inset-y-0 left-0 rounded-full transition-colors duration-500" style={{ width: left, backgroundColor: after ? CLEAR : '#F28C28' }} />
            <motion.div
              className="absolute inset-y-0"
              style={{
                backgroundImage: `repeating-linear-gradient(45deg, ${after ? 'rgba(16,36,28,0.35)' : 'rgba(255,138,149,0.45)'} 0 6px, transparent 6px 12px)`,
              }}
              initial={false}
              animate={{ left: `${pct(lo)}%`, width: `${pct(hi) - pct(lo)}%`, opacity: seen ? 1 : 0 }}
              transition={{ type: 'spring', stiffness: 60, damping: 17 }}
            />
          </div>

          <motion.div className="absolute top-[74px] -translate-x-1/2" style={{ left }}>
            <span className="mx-auto block h-0 w-0 border-x-[7px] border-b-[9px] border-x-transparent transition-colors duration-500" style={{ borderBottomColor: after ? CLEAR : '#F28C28' }} />
            <span className="block whitespace-nowrap rounded-full px-3 py-1 text-xs font-extrabold text-chalk-deep transition-colors duration-500" style={{ backgroundColor: after ? CLEAR : '#F28C28' }}>
              {t('cutYouTag')}
            </span>
          </motion.div>

          <div className="absolute inset-x-0 bottom-0 flex justify-between text-xs font-semibold tabular-nums text-white/45">
            {[40, 45, 50, 55, 60, 65, 70, 75, 80].map((n) => (
              <span key={n} className={cn('relative', n % 10 && 'hidden sm:inline')}>
                <span className="absolute -top-2 left-1/2 h-1.5 w-px -translate-x-1/2 bg-white/30" />
                {n}
              </span>
            ))}
          </div>
        </div>

        {/* ---------- Leak tickets ---------- */}
        <div className="mt-4 flex flex-wrap items-baseline justify-between gap-3">
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-white/55">{t('cutLeaksTitle')}</p>
          <p className="text-sm font-bold">
            <span className="text-white/60">{t('cutRecovered')}: </span>
            <motion.span key={after ? 'a' : 'b'} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} style={{ color: after ? CLEAR : 'rgba(255,255,255,0.45)' }}>
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
                  'relative flex items-center gap-3 overflow-hidden rounded-2xl border p-4 backdrop-blur transition-colors duration-500 sm:p-5',
                  after ? 'border-[#5EE0A0]/40 bg-[#5EE0A0]/10' : 'border-white/15 bg-white/[0.06]',
                )}
                animate={after ? { y: [0, -6, 0] } : { y: 0 }}
                transition={{ duration: 0.45, delay: 0.25 + i * 0.15 }}
              >
                <span className={cn('relative flex h-11 w-11 shrink-0 items-center justify-center rounded-xl transition-colors duration-500', after ? 'bg-[#5EE0A0] text-chalk-deep' : tone.chip)}>
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
                <span className="min-w-0 flex-1 text-sm font-semibold leading-snug text-white/90">{t(l.key)}</span>
                <span className={cn('shrink-0 text-right font-display text-2xl font-extrabold tabular-nums transition-colors duration-500', !after && tone.text)} style={after ? { color: CLEAR } : undefined}>
                  {after ? `+${fmt(l.marks)}` : `−${fmt(l.marks)}`}
                  <span className="block text-[10px] font-bold uppercase tracking-wide">{after ? t('cutPlugged') : '\u00a0'}</span>
                </span>
              </motion.li>
            );
          })}
        </ul>

        <p className="mt-6 text-xs text-white/50">{t('cutSample')}</p>
      </div>
    </section>
  );
}
