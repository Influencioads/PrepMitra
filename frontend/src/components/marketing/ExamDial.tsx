import { useCallback, useEffect, useState, type KeyboardEvent, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { AnimatePresence, motion, useReducedMotion, type PanInfo } from 'framer-motion';
import { ArrowRight, ChevronLeft, ChevronRight } from 'lucide-react';
import type { Exam } from '@prepmitra/shared';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { useContentT } from '@/i18n/content';
import { homeMessages } from '@/i18n/messages/home';

const EASE = [0.22, 1, 0.36, 1] as const;
/** PrepMitra theme only: saffron and green, alternating, in a few depths. */
const COLORS = ['#C2410C', '#1E5E47', '#A6370A', '#174A38', '#9A3412', '#17392C'];

const mod = (n: number, m: number) => ((n % m) + m) % m;

function useWide() {
  const q = '(min-width: 640px)';
  const [wide, setWide] = useState(() => typeof window !== 'undefined' && !!window.matchMedia?.(q).matches);
  useEffect(() => {
    const m = window.matchMedia?.(q);
    if (!m) return;
    const on = () => setWide(m.matches);
    m.addEventListener('change', on);
    return () => m.removeEventListener('change', on);
  }, []);
  return wide;
}

/**
 * "Turn the dial" exam picker, laid out like a turntable: exam names run along a wide arc,
 * the chosen one stops under the marker, a big paper disc rises from the bottom edge and spins in,
 * and the whole scene takes that exam's colour. Arrows, ← →, a drag on the disc or a tap on a name turn it.
 */
export function ExamDial({ exams, eyebrow, title, heading, tall = false, allHref = '/exams?category=banking', className }: { exams: Exam[]; eyebrow?: string; title?: string; heading?: ReactNode; tall?: boolean; allHref?: string; className?: string }) {
  const t = useT(homeMessages);
  const ct = useContentT();
  const reduce = useReducedMotion();
  const wide = useWide();
  const step = wide ? 21 : 27; // degrees between names on the arc
  const reach = wide ? 3 : 2; // how many names show on each side
  // `turn` keeps counting past the ends so the arc always moves the short way round.
  const [turn, setTurn] = useState(0);
  const [dir, setDir] = useState(1);
  const n = exams.length;
  const active = n ? mod(turn, n) : 0;
  const exam = exams[active];

  const go = useCallback((delta: number) => {
    setDir(delta >= 0 ? 1 : -1);
    setTurn((v) => v + delta);
  }, []);
  const goTo = (i: number) => {
    let d = mod(i - active, n);
    if (d > n / 2) d -= n;
    if (d) go(d);
  };
  const onKey = (e: KeyboardEvent) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
  };
  const onDragEnd = (_: unknown, info: PanInfo) => {
    if (info.offset.x < -50) go(1);
    else if (info.offset.x > 50) go(-1);
  };

  const color = COLORS[active % COLORS.length]!;
  const sizes = cn(
    tall ? '[--H:540px] sm:[--H:720px]' : '[--H:500px] sm:[--H:660px]',
    '[--R:222px] [--D:350px] [--cy:calc(var(--H)-4px)]',
    'sm:[--R:440px] sm:[--D:640px] sm:[--cy:calc(var(--H)+24px)]',
  );
  const head = heading ?? (
    <>
      <p className="font-hand text-lg text-marigold sm:text-xl">{eyebrow ?? t('dialEyebrow')} —</p>
      <h2 className="mt-1 text-balance font-display text-3xl font-extrabold tracking-tight text-chalk-text sm:text-5xl">{title ?? t('dialTitle')}</h2>
    </>
  );

  // Exams still loading (or none): keep the scene and heading on screen, with an empty ring and disc.
  if (!exam) {
    return (
      <div className={cn('relative isolate h-[var(--H)] overflow-hidden rounded-[32px] text-chalk-text', sizes, className)} style={{ backgroundColor: color }}>
        <div className="relative z-20 px-6 pt-8 text-center sm:pt-10">{head}</div>
        <div className="absolute left-1/2 top-[var(--cy)] h-0 w-0" aria-hidden>
          <span className="absolute left-0 top-0 h-[calc(var(--R)*2)] w-[calc(var(--R)*2)] -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/30" />
          <span className="absolute left-0 top-0 h-[var(--D)] w-[var(--D)] -translate-x-1/2 -translate-y-1/2 animate-pulse rounded-full border-[3px] border-ink bg-paper/90" />
        </div>
      </div>
    );
  }

  return (
    <motion.div
      role="group"
      aria-roledescription="carousel"
      aria-label={t('dialLabel')}
      tabIndex={0}
      onKeyDown={onKey}
      animate={{ backgroundColor: color }}
      transition={{ duration: 0.7, ease: EASE }}
      className={cn(
        // H = scene height, R = arc radius, D = disc diameter, cy = where the shared centre sits (below the middle).
        'relative isolate h-[var(--H)] overflow-hidden rounded-[32px] text-chalk-text outline-none ring-offset-4 ring-offset-background focus-visible:ring-2 focus-visible:ring-primary',
        sizes,
        className,
      )}
    >
      {/* light, vignette and grain */}
      <span className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_50%_0%,rgba(255,255,255,0.18),transparent_60%)]" aria-hidden />
      <span className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_50%_100%,transparent_40%,rgba(0,0,0,0.35))]" aria-hidden />
      <span className="pointer-events-none absolute inset-0 -z-10 opacity-[0.06] [background-image:radial-gradient(rgba(255,255,255,0.9)_1px,transparent_1px)] [background-size:4px_4px]" aria-hidden />

      {/* ---------- Heading ---------- */}
      <div className="relative z-20 px-6 pt-8 text-center sm:pt-10">
        {head}
        <p className="mt-2 text-xs font-bold uppercase tracking-[0.18em] text-white/55" aria-live="polite">
          {t('dialOf', { i: active + 1, n })} · <Link to={allHref} className="underline decoration-white/40 underline-offset-4 hover:text-white">{t('dialAll', { n })}</Link>
        </p>
      </div>

      {/* ---------- Shared centre: arc, names, marker, disc ---------- */}
      <div className="absolute left-1/2 top-[var(--cy)] h-0 w-0">
        {/* arc */}
        <span className="absolute left-0 top-0 h-[calc(var(--R)*2)] w-[calc(var(--R)*2)] -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/30" aria-hidden />
        <span className="absolute left-0 top-0 h-[calc(var(--R)*2+36px)] w-[calc(var(--R)*2+36px)] -translate-x-1/2 -translate-y-1/2 rounded-full border border-dashed border-white/10" aria-hidden />
        {/* marker */}
        <motion.span
          className="absolute left-0 top-[calc(var(--R)*-1)] z-20 h-3.5 w-3.5 -translate-x-1/2 -translate-y-1/2 rounded-full bg-marigold"
          animate={reduce ? undefined : { boxShadow: ['0 0 0 4px rgba(255,210,122,0.35)', '0 0 0 10px rgba(255,210,122,0)'] }}
          transition={{ duration: 1.6, repeat: Infinity }}
          aria-hidden
        />

        {/* names on the arc */}
        {exams.map((e, i) => {
          let d = mod(i - active, n);
          if (d > n / 2) d -= n;
          const far = Math.abs(d);
          const hidden = far > reach;
          return (
            <motion.button
              key={e.id}
              type="button"
              tabIndex={-1}
              onClick={() => goTo(i)}
              aria-label={ct(e.shortTitle)}
              className="absolute left-0 top-0 z-10 h-0 w-0"
              initial={false}
              animate={{ rotate: d * step, opacity: hidden ? 0 : far === 0 ? 1 : 0.8 - far * 0.15 }}
              transition={reduce ? { duration: 0 } : { type: 'spring', stiffness: 90, damping: 18 }}
              style={{ pointerEvents: hidden ? 'none' : 'auto' }}
            >
              <span
                className={cn(
                  'absolute left-0 top-0 block whitespace-nowrap px-2 py-1 text-[11px] font-bold uppercase tracking-[0.16em] transition-colors sm:text-sm',
                  far === 0 ? 'text-marigold' : 'text-white/85 hover:text-white',
                )}
                style={{ transform: 'translate(-50%, calc(var(--R) * -1 - 34px))' }}
              >
                {ct(e.shortTitle)}
              </span>
            </motion.button>
          );
        })}

        {/* disc */}
        <motion.div
          className="absolute left-0 top-0 z-10 h-[var(--D)] w-[var(--D)] -translate-x-1/2 -translate-y-1/2 cursor-grab touch-pan-y active:cursor-grabbing"
          drag="x"
          dragConstraints={{ left: 0, right: 0 }}
          dragElastic={0.2}
          onDragEnd={onDragEnd}
        >
          <AnimatePresence initial={false} custom={dir} mode="popLayout">
            <motion.div
              key={exam.id}
              className="absolute inset-0"
              initial={reduce ? { opacity: 0 } : { rotate: dir * 75, opacity: 0.4 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={reduce ? { opacity: 0 } : { rotate: dir * -75, opacity: 0 }}
              transition={{ type: 'spring', stiffness: 70, damping: 16 }}
            >
              <Disc exam={exam} index={active} label={ct(exam.shortTitle)} take={t('dialTake')} meta={`${t('dialQs', { n: exam.totalQuestions })} · ${t('dialMin', { n: exam.durationMin })} · ${t('dialMarks', { n: exam.totalMarks })}`} />
            </motion.div>
          </AnimatePresence>
        </motion.div>
      </div>

      {/* ---------- Arrows ---------- */}
      {(['prev', 'next'] as const).map((k) => (
        <motion.button
          key={k}
          type="button"
          onClick={() => go(k === 'prev' ? -1 : 1)}
          whileHover={{ scale: 1.06 }}
          whileTap={{ scale: 0.92 }}
          aria-label={k === 'prev' ? t('dialPrev') : t('dialNext')}
          className={cn(
            'absolute top-[calc(var(--cy)-var(--R)-64px)] sm:top-[calc(var(--cy)-var(--R)*0.62)] z-30 flex h-11 w-11 items-center justify-center rounded-full border border-white/35 bg-white/10 backdrop-blur transition-colors hover:bg-white/20 sm:h-14 sm:w-14',
            k === 'prev' ? 'left-3 sm:left-[calc(50%-var(--R)-90px)]' : 'right-3 sm:right-[calc(50%-var(--R)-90px)]',
          )}
        >
          {k === 'prev' ? <ChevronLeft className="h-5 w-5 sm:h-6 sm:w-6" /> : <ChevronRight className="h-5 w-5 sm:h-6 sm:w-6" />}
        </motion.button>
      ))}
      <p className="sr-only">{t('dialHint')}</p>
    </motion.div>
  );
}

/** The paper disc: a ring of OMR bubbles round the edge, the exam in the visible top half. */
function Disc({ exam, index, label, take, meta }: { exam: Exam; index: number; label: string; take: string; meta: string }) {
  const bubbles = 40;
  return (
    <div className="relative h-full w-full rounded-full border-[3px] border-ink bg-paper text-ink shadow-[0_-20px_60px_-10px_rgba(0,0,0,0.5)]">
      <span className="absolute inset-[9%] rounded-full border-2 border-dashed border-line-strong" aria-hidden />
      {Array.from({ length: bubbles }, (_, i) => {
        const filled = (i * 7 + index * 3) % 6 === 0;
        return (
          <span key={i} className="absolute left-1/2 top-1/2 h-0 w-0" style={{ transform: `rotate(${(360 / bubbles) * i}deg)` }} aria-hidden>
            <span
              className={cn('absolute block rounded-full', filled ? 'bg-ink' : 'border-[1.5px] border-subtle')}
              style={{ width: 'calc(var(--D) * 0.032)', height: 'calc(var(--D) * 0.032)', transform: 'translate(-50%, calc(var(--D) * -0.465))' }}
            />
          </span>
        );
      })}
      {/* content sits in the top half, the part above the scene's bottom edge */}
      <div className="absolute inset-x-[16%] top-[13%] flex flex-col items-center text-center">
        <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-muted sm:text-xs">{exam.conductingBody}</span>
        <span className="mt-1 font-display text-[1.9rem] font-extrabold leading-none tracking-tight sm:mt-2 sm:text-6xl">{label}</span>
        <span className="mt-2 text-[11px] font-semibold text-muted sm:mt-3 sm:text-sm">{meta}</span>
        <Link
          to={`/exams/${exam.id}`}
          onPointerDownCapture={(e) => e.stopPropagation()}
          className="group mt-3 inline-flex items-center gap-2 rounded-xl bg-primary px-4 py-2 text-sm font-extrabold text-white shadow-[0_4px_0_#8A2E07] transition-transform hover:-translate-y-0.5 sm:mt-5 sm:rounded-2xl sm:px-6 sm:py-3 sm:text-base"
        >
          {take}
          <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" aria-hidden />
        </Link>
      </div>
    </div>
  );
}
