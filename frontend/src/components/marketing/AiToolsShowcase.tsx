import { useEffect, useRef, useState, type KeyboardEvent, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { AnimatePresence, motion, useInView, useReducedMotion } from 'framer-motion';
import { Bot, Camera, ChevronLeft, ChevronRight, ClipboardCheck, Gauge, KeyRound, Lock, Pause, Play, Presentation, Sparkles, Unlock, type LucideIcon } from 'lucide-react';
import { PenUnderline, TypingDots, WordsReveal } from '@/components/marketing/HomeFx';
import { useT } from '@/i18n';
import { aiShowcaseMessages } from '@/i18n/messages/aiShowcase';
import { cn } from '@/utils/cn';

/**
 * Home page band: the six most important AI tools. A tab list on the left, a short sample demo of the selected
 * tool on the right (every demo is labelled "Sample"; nothing here calls the AI). Tours itself every few seconds
 * while on screen, stops when the visitor picks a tool, hovers the panel or turns the tour off.
 */

type Key = 'doubt' | 'tutor' | 'board' | 'codes' | 'persona' | 'report';
type T = (key: keyof typeof aiShowcaseMessages.en, vars?: Record<string, string | number>) => string;

const TOOLS: { key: Key; icon: LucideIcon }[] = [
  { key: 'doubt', icon: Sparkles },
  { key: 'tutor', icon: Bot },
  { key: 'board', icon: Presentation },
  { key: 'codes', icon: KeyRound },
  { key: 'persona', icon: Gauge },
  { key: 'report', icon: ClipboardCheck },
];
const STEP_MS = 7000;
const EASE = [0.22, 1, 0.36, 1] as const;

/** Child that fades up after `d` seconds (used to build each demo line by line). */
function Up({ d = 0, className, children }: { d?: number; className?: string; children: ReactNode }) {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, ease: EASE, delay: d }} className={className}>
      {children}
    </motion.div>
  );
}

function DoubtDemo({ t }: { t: T }) {
  return (
    <div className="space-y-3">
      <Up className="rounded-xl border-[1.5px] border-ink bg-card p-4">
        <p className="font-semibold leading-snug">{t('doubtQ')}</p>
        <div className="mt-3 grid grid-cols-2 gap-2 text-sm sm:grid-cols-4">
          {['20', '60', '72', '90'].map((o, i) => (
            <motion.span
              key={o}
              className="flex items-center gap-1.5 rounded-lg border border-line px-2 py-1"
              initial={false}
              animate={i === 2 ? { backgroundColor: 'rgba(30,94,71,0.12)', borderColor: '#1E5E47' } : {}}
              transition={{ delay: 2.4, duration: 0.3 }}
            >
              <span className={cn('h-3 w-3 rounded-full border-[1.5px] border-subtle', i === 2 && 'border-secondary')} />
              {o}
            </motion.span>
          ))}
        </div>
      </Up>
      <Up d={0.8} className="flex items-baseline gap-2 font-hand text-lg"><span className="text-primary">1.</span>{t('doubtS1')}</Up>
      <Up d={1.6} className="flex items-baseline gap-2 font-hand text-lg"><span className="text-primary">2.</span><span>{t('doubtS2')}</span></Up>
      <div className="flex flex-wrap gap-2 pt-1">
        <Up d={2.6} className="rounded-full bg-secondary-soft px-3 py-1 text-sm font-semibold text-secondary">{t('doubtShortcut')}</Up>
        <Up d={3.2} className="rounded-full bg-[#fdeeec] px-3 py-1 text-sm font-semibold text-pen">{t('doubtTrap')}</Up>
      </div>
      <Up d={3.8} className="inline-flex items-center gap-1.5 text-sm text-muted"><Camera className="h-4 w-4" /> {t('doubtPhoto')}</Up>
    </div>
  );
}

function TutorDemo({ t }: { t: T }) {
  const [typing, setTyping] = useState(true);
  useEffect(() => {
    const id = setTimeout(() => setTyping(false), 1500);
    return () => clearTimeout(id);
  }, []);
  return (
    <div className="flex flex-col gap-3">
      <Up className="max-w-[80%] self-end rounded-2xl rounded-br-sm bg-ink px-4 py-2.5 text-paper">{t('tutorUser')}</Up>
      <Up d={0.5} className="flex max-w-[88%] items-end gap-2">
        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-chalk text-marigold"><Bot className="h-4 w-4" /></span>
        <div className="rounded-2xl rounded-bl-sm bg-chalk px-4 py-3 text-chalk-text">
          {typing ? <TypingDots /> : <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="leading-relaxed">{t('tutorBot')}</motion.p>}
        </div>
      </Up>
      <div className="ml-10 flex flex-wrap gap-2">
        {[t('tutorChip1'), t('tutorChip2')].map((c, i) => (
          <Up key={c} d={2.1 + i * 0.25} className="rounded-full border-[1.5px] border-ink px-3 py-1 text-sm font-semibold">{c}</Up>
        ))}
      </div>
    </div>
  );
}

function BoardDemo({ t }: { t: T }) {
  const seats = ['A', 'B', 'C', 'D', 'E', 'F'];
  const R = 62;
  return (
    <div className="rounded-xl border-[6px] border-wood bg-chalkboard p-4 text-chalk-text">
      <p className="font-hand text-lg text-marigold">{t('boardTitle')}</p>
      <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-around">
        <svg viewBox="-90 -90 180 180" className="h-44 w-44" aria-hidden>
          <motion.circle r={R} fill="none" stroke="currentColor" strokeWidth="2.5" strokeDasharray="4 6" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeInOut' }} />
          <motion.line x1={0} y1={-R} x2={0} y2={R} stroke="#FFD27A" strokeWidth="2.5" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ delay: 2.4, duration: 0.6 }} />
          {seats.map((s, i) => {
            const a = (i / 6) * Math.PI * 2 - Math.PI / 2;
            const x = Math.cos(a) * R;
            const y = Math.sin(a) * R;
            return (
              <motion.g key={s} initial={{ opacity: 0, scale: 0.4 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 1 + i * 0.18, duration: 0.3 }} style={{ originX: `${x}px`, originY: `${y}px` }}>
                <circle cx={x} cy={y} r={13} fill={i === 0 || i === 3 ? '#FFD27A' : '#17392C'} stroke="currentColor" strokeWidth="2" />
                <text x={x} y={y + 5} textAnchor="middle" className="font-hand" fontSize="15" fill={i === 0 || i === 3 ? '#10241C' : 'currentColor'}>{s}</text>
              </motion.g>
            );
          })}
        </svg>
        <Up d={2.8} className="text-center sm:text-left">
          <p className="font-hand text-xl">{t('boardQ')}</p>
          <div className="mt-2 flex justify-center gap-2 sm:justify-start">
            {['B', 'C', 'D'].map((o) => (
              <span key={o} className={cn('flex h-9 w-9 items-center justify-center rounded-full border-2 font-bold', o === 'D' ? 'border-marigold bg-marigold text-chalk-deep' : 'border-white/40')}>{o}</span>
            ))}
          </div>
        </Up>
      </div>
    </div>
  );
}

function CodesDemo({ t }: { t: T }) {
  const rows = [['12.5%', '1⁄8'], ['16.66%', '1⁄6'], ['37.5%', '3⁄8'], ['83.33%', '5⁄6']];
  return (
    <div className="relative rounded-xl border-[1.5px] border-ink bg-sticky-yellow p-4 shadow-[4px_5px_0_#1c2321]">
      <p className="font-hand text-xl">{t('codesTitle')}</p>
      <div className="mt-2 grid grid-cols-2 gap-x-6 gap-y-1.5 font-mono text-lg">
        {rows.map(([a, b], i) => (
          <Up key={a} d={0.3 + i * 0.3} className="flex items-center justify-between border-b border-dashed border-ink/25 pb-1">
            <span>{a}</span><span className="font-bold text-primary">{b}</span>
          </Up>
        ))}
      </div>
      <div className="mt-4 flex items-center gap-3">
        <span className="text-sm font-semibold text-muted">{t('codesDrill')}</span>
        {[0, 1, 2].map((i) => (
          <motion.span
            key={i}
            className="h-5 w-5 rounded-full border-[1.5px] border-ink"
            initial={{ backgroundColor: 'rgba(0,0,0,0)' }}
            animate={{ backgroundColor: i < 2 ? '#1E5E47' : 'rgba(0,0,0,0)' }}
            transition={{ delay: 1.8 + i * 0.4, duration: 0.2 }}
          />
        ))}
        <motion.span initial={{ opacity: 0, scale: 1.6, rotate: -12 }} animate={{ opacity: 1, scale: 1, rotate: -6 }} transition={{ delay: 2.9, type: 'spring', stiffness: 260, damping: 14 }}
          className="ml-auto inline-flex items-center gap-1.5 rounded-md border-2 border-secondary px-2 py-0.5 text-sm font-extrabold uppercase tracking-wide text-secondary">
          <Unlock className="h-4 w-4" /> {t('codesUnlocked')}
        </motion.span>
      </div>
      <Lock className="absolute -top-3 right-4 h-7 w-7 rounded-full bg-ink p-1.5 text-marigold" aria-hidden />
    </div>
  );
}

function PersonaDemo({ t }: { t: T }) {
  const traits = [
    { label: t('personaSpeed'), v: 82, c: 'bg-accent' },
    { label: t('personaAccuracy'), v: 58, c: 'bg-pen' },
    { label: t('personaRisk'), v: 74, c: 'bg-primary' },
    { label: t('personaStamina'), v: 66, c: 'bg-secondary' },
  ];
  return (
    <div>
      <Up className="flex items-center gap-3">
        <span className="flex h-12 w-12 items-center justify-center rounded-full bg-accent-soft text-2xl" aria-hidden>⚡</span>
        <p className="text-2xl font-extrabold">{t('personaType')}</p>
      </Up>
      <div className="mt-4 space-y-3">
        {traits.map((tr, i) => (
          <div key={tr.label}>
            <div className="flex justify-between text-sm font-semibold"><span>{tr.label}</span><span className="tabular-nums">{tr.v}</span></div>
            <div className="mt-1 h-2.5 overflow-hidden rounded-full bg-surface">
              <motion.div className={cn('h-full rounded-full', tr.c)} initial={{ width: 0 }} animate={{ width: `${tr.v}%` }} transition={{ delay: 0.4 + i * 0.2, duration: 0.8, ease: EASE }} />
            </div>
          </div>
        ))}
      </div>
      <Up d={1.8} className="mt-4 font-hand text-lg text-pen">{t('personaPlan')}</Up>
    </div>
  );
}

function ReportDemo({ t }: { t: T }) {
  const leaks = [{ l: t('reportLeak1'), m: 4 }, { l: t('reportLeak2'), m: 2.5 }, { l: t('reportLeak3'), m: 1.25 }];
  return (
    <div>
      <div className="flex items-end justify-between gap-4">
        <Up>
          <p className="text-sm font-semibold text-muted">{t('reportScore')}</p>
          <p className="text-4xl font-extrabold tabular-nums">61.25<span className="text-lg text-muted">/100</span></p>
        </Up>
        <Up d={0.4} className="rounded-md border-2 border-pen px-2 py-1 text-sm font-extrabold text-pen [transform:rotate(-4deg)]">{t('reportShortBy')}</Up>
      </div>
      <div className="relative mt-4 h-3 rounded-full bg-surface">
        <motion.div className="h-full rounded-full bg-accent" initial={{ width: 0 }} animate={{ width: '61.25%' }} transition={{ duration: 0.9, ease: EASE }} />
        <span className="absolute -top-2 bottom-[-8px] left-[63%] w-0.5 bg-ink" aria-hidden />
        <span className="absolute -top-7 left-[63%] -translate-x-1/2 text-xs font-bold">{t('reportCutoff')} 63</span>
      </div>
      <ul className="mt-5 space-y-2">
        {leaks.map((x, i) => (
          <Up key={x.l} d={1 + i * 0.3} className="flex items-center justify-between rounded-lg border border-line bg-card px-3 py-2">
            <span className="font-medium">{x.l}</span><span className="font-bold tabular-nums text-pen">−{x.m}</span>
          </Up>
        ))}
      </ul>
      <Up d={2.1} className="mt-3 inline-flex items-center gap-1.5 rounded-full bg-secondary-soft px-3 py-1 text-sm font-semibold text-secondary">✓ {t('reportPlan')}</Up>
    </div>
  );
}

const DEMOS: Record<Key, (p: { t: T }) => ReactNode> = {
  doubt: DoubtDemo, tutor: TutorDemo, board: BoardDemo, codes: CodesDemo, persona: PersonaDemo, report: ReportDemo,
};

export function AiToolsShowcase({ className }: { className?: string }) {
  const t = useT(aiShowcaseMessages);
  const reduce = useReducedMotion();
  const [active, setActive] = useState(0);
  const [dir, setDir] = useState(1);
  const [touring, setTouring] = useState(!reduce);
  const [hover, setHover] = useState(false);
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { amount: 0.35 });
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);
  const running = touring && inView && !hover;

  const go = (i: number, stopTour = true) => {
    const n = (i + TOOLS.length) % TOOLS.length;
    setActive((a) => {
      setDir(n > a || (a === TOOLS.length - 1 && n === 0) ? 1 : -1);
      return n;
    });
    if (stopTour) setTouring(false);
  };

  useEffect(() => {
    if (!running) return;
    const id = setTimeout(() => go(active + 1, false), STEP_MS);
    return () => clearTimeout(id);
  }, [running, active]);

  // Keep the selected tab visible in the sideways-scrolling row on phones. Scrolls only that row, never the page.
  const listRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const list = listRef.current;
    const tab = tabRefs.current[active];
    if (!list || !tab || list.scrollWidth <= list.clientWidth) return;
    const left = tab.offsetLeft - list.offsetLeft;
    if (left < list.scrollLeft || left + tab.offsetWidth > list.scrollLeft + list.clientWidth) {
      list.scrollTo?.({ left: Math.max(0, left - 16), behavior: reduce ? 'auto' : 'smooth' });
    }
  }, [active, reduce]);

  const onKey = (e: KeyboardEvent<HTMLDivElement>) => {
    const d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
    if (!d) return;
    e.preventDefault();
    const n = (active + d + TOOLS.length) % TOOLS.length;
    go(n);
    tabRefs.current[n]?.focus();
  };

  const tool = TOOLS[active];
  const Demo = DEMOS[tool.key];
  const slide = { enter: (d: number) => ({ opacity: 0, x: d * 28 }), center: { opacity: 1, x: 0 }, exit: (d: number) => ({ opacity: 0, x: d * -28 }) };

  return (
    <section ref={ref} id="ai-tools" aria-labelledby="ai-tools-title" className={cn('relative scroll-mt-20 overflow-hidden py-16 lg:py-24', className)}>
      <span className="pointer-events-none absolute left-1/2 top-0 -z-10 h-[420px] w-[900px] -translate-x-1/2 rounded-full bg-accent/15 blur-3xl" aria-hidden />

      <div className="container-page">
        {/* heading */}
        <div className="mx-auto max-w-3xl text-center">
          <h2 id="ai-tools-title" className="text-balance font-display text-4xl font-extrabold leading-[1.05] tracking-tight sm:text-6xl">
            <WordsReveal text={t('title1')} inView />{' '}
            <span className="relative inline-block whitespace-nowrap text-primary">
              {t('title2')}
              <PenUnderline delay={0.5} />
            </span>
          </h2>
        </div>

        <div className="mt-10 grid gap-4 lg:grid-cols-[15rem_minmax(0,1fr)] lg:gap-6">
        {/* tool tabs: a row on phones, a narrow column on the left from lg */}
        <div ref={listRef} role="tablist" aria-label={t('tabsLabel')} aria-orientation="vertical" onKeyDown={onKey}
          className="-mx-4 flex snap-x scroll-px-4 gap-2.5 overflow-x-auto px-4 pb-3 pt-1 [scrollbar-width:none] sm:mx-0 sm:px-0 lg:h-full lg:flex-col lg:gap-3 lg:overflow-visible lg:p-0">
          {TOOLS.map((tl, i) => {
            const on = i === active;
            const TIcon = tl.icon;
            return (
              <button
                key={tl.key}
                ref={(el) => { tabRefs.current[i] = el; }}
                type="button" role="tab" id={`ai-tab-${tl.key}`} aria-selected={on} aria-controls="ai-tools-panel" tabIndex={on ? 0 : -1}
                onClick={() => go(i)}
                className={cn(
                  'group relative flex shrink-0 snap-start items-center gap-2.5 overflow-hidden rounded-xl border-[1.5px] py-2 pl-2 pr-3.5 text-left transition-[transform,box-shadow,border-color] duration-200 lg:w-full lg:flex-1 lg:px-4',
                  on ? 'z-10 -translate-y-0.5 border-ink bg-card shadow-[3px_4px_0_#1c2321] lg:translate-x-1 lg:translate-y-0' : 'border-line-strong bg-card/60 hover:-translate-y-0.5 hover:border-ink',
                )}
              >
                <span className={cn('flex h-8 w-8 shrink-0 items-center justify-center rounded-lg transition-colors',
                  on ? 'bg-accent text-chalk-deep' : 'bg-accent-soft text-primary group-hover:bg-accent/30')}>
                  <TIcon className="h-4 w-4" />
                </span>
                <span className="whitespace-nowrap text-sm font-bold leading-tight">{t(`${tl.key}Name`)}</span>
                <span className="absolute inset-x-0 bottom-0 h-[3px] bg-line" aria-hidden />
                {on && (
                  <motion.span
                    key={`bar-${active}-${running}`}
                    className="absolute bottom-0 left-0 h-[3px] bg-accent"
                    initial={{ width: running ? '0%' : '100%' }}
                    animate={{ width: '100%' }}
                    transition={{ duration: running ? STEP_MS / 1000 : 0, ease: 'linear' }}
                    aria-hidden
                  />
                )}
              </button>
            );
          })}
        </div>

        {/* stage */}
        <div
          id="ai-tools-panel" role="tabpanel" aria-labelledby={`ai-tab-${tool.key}`}
          onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
          className="relative overflow-hidden rounded-[28px] border-[1.5px] border-ink bg-chalkboard text-chalk-text shadow-[8px_9px_0_#1c2321]"
        >
          <span className="pointer-events-none absolute -left-24 -top-24 h-80 w-80 rounded-full bg-accent/20 blur-3xl" aria-hidden />
          <span className="pointer-events-none absolute -bottom-32 right-10 h-80 w-80 rounded-full bg-marigold/10 blur-3xl" aria-hidden />
          <div className="relative p-5 pt-7 sm:px-10 sm:pb-8 sm:pt-10">
            {/* sample */}
            <div className="relative mx-auto min-w-0 max-w-2xl">
              <span className="pointer-events-none absolute -top-3 left-1/2 z-10 h-6 w-28 -translate-x-1/2 rotate-[-2deg] bg-marigold/80" aria-hidden />
              <div className="overflow-hidden rounded-[22px] border-[1.5px] border-ink bg-paper text-ink shadow-[0_24px_60px_-20px_rgba(0,0,0,0.6)] lg:rotate-[0.6deg]">
                <div className="flex items-center gap-2 border-b-[1.5px] border-ink bg-card px-4 py-2.5">
                  <span className="h-2.5 w-2.5 rounded-full bg-pen/70" aria-hidden />
                  <span className="h-2.5 w-2.5 rounded-full bg-marigold" aria-hidden />
                  <span className="h-2.5 w-2.5 rounded-full bg-secondary/70" aria-hidden />
                  <span className="ml-auto rounded-full bg-sticky-yellow px-2.5 py-0.5 text-xs font-bold uppercase tracking-wide text-warning-ink">{t('sample')}</span>
                </div>
                <div className="bg-ruled flex min-h-[260px] flex-col justify-center p-4 sm:min-h-[290px] sm:p-5">
                  <AnimatePresence mode="wait" initial={false} custom={dir}>
                    <motion.div key={tool.key} custom={dir} variants={slide} initial="enter" animate="center" exit="exit" transition={{ duration: 0.3, ease: EASE }} className="w-full">
                      <Demo t={t} />
                    </motion.div>
                  </AnimatePresence>
                </div>
              </div>
            </div>
          </div>

          {/* controls */}
          <div className="relative flex items-center justify-between gap-3 border-t border-white/10 px-5 py-3 sm:px-8">
            <div className="flex items-center gap-4"><div className="hidden items-center gap-1.5 sm:flex" aria-hidden>
              {TOOLS.map((tl, i) => (
                <span key={tl.key} className={cn('h-1.5 rounded-full transition-all duration-300', i === active ? 'w-6 bg-marigold' : 'w-1.5 bg-white/30')} />
              ))}
            </div>
            <Link to="/ai" className="whitespace-nowrap text-sm font-semibold text-marigold underline-offset-4 hover:underline">{t('seeAll')}</Link></div>
            <div className="flex items-center gap-1">
              {!reduce && (
                <button type="button" onClick={() => setTouring((v) => !v)} aria-label={touring ? t('pause') : t('play')} className="flex h-9 w-9 items-center justify-center rounded-full text-white/70 hover:bg-white/10 hover:text-white">
                  {touring ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                </button>
              )}
              <button type="button" onClick={() => go(active - 1)} aria-label={t('prev')} className="flex h-9 w-9 items-center justify-center rounded-full border border-white/25 hover:bg-white hover:text-ink"><ChevronLeft className="h-4 w-4" /></button>
              <button type="button" onClick={() => go(active + 1)} aria-label={t('next')} className="flex h-9 w-9 items-center justify-center rounded-full border border-white/25 hover:bg-white hover:text-ink"><ChevronRight className="h-4 w-4" /></button>
            </div>
          </div>
        </div>
        </div>
      </div>
    </section>
  );
}
