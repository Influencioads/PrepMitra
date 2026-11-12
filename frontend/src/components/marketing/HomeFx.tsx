import { useRef, type ReactNode } from 'react';
import { motion, useMotionValue, useReducedMotion, useScroll, useSpring, useTransform, type MotionValue } from 'framer-motion';
import { cn } from '@/utils/cn';

/** Small motion helpers used only by the marketing home page. All respect reduced motion. */

const EASE = [0.22, 1, 0.36, 1] as const;

/** Splits a line into words that rise in one after another (screen readers get the plain text). */
export function WordsReveal({ text, className, delay = 0, inView = false, step = 0.06 }: { text: string; className?: string; delay?: number; inView?: boolean; step?: number }) {
  const words = text.split(' ');
  const trigger = inView ? { whileInView: 'show', viewport: { once: true, amount: 0.6 } } : { animate: 'show' };
  return (
    <span className={cn('inline', className)}>
    <span className="sr-only">{text}</span>
    <motion.span initial="hidden" {...trigger} aria-hidden>
      {words.map((w, i) => (
        <span key={`${w}-${i}`} className="inline-block overflow-hidden pb-[0.08em] align-bottom">
          <motion.span
            className="inline-block"
            variants={{ hidden: { y: '105%' }, show: { y: 0, transition: { duration: 0.55, ease: EASE, delay: delay + i * step } } }}
          >
            {w}
            {i < words.length - 1 ? ' ' : ''}
          </motion.span>
        </span>
      ))}
    </motion.span>
    </span>
  );
}

/** Card that tilts a little toward the pointer (mouse only; flat for touch and reduced motion). */
export function TiltCard({ children, className, max = 6 }: { children: ReactNode; className?: string; max?: number }) {
  const reduce = useReducedMotion();
  const rx = useMotionValue(0);
  const ry = useMotionValue(0);
  const srx = useSpring(rx, { stiffness: 180, damping: 18 });
  const sry = useSpring(ry, { stiffness: 180, damping: 18 });
  const onMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (reduce || e.pointerType !== 'mouse') return;
    const r = e.currentTarget.getBoundingClientRect();
    ry.set(((e.clientX - r.left) / r.width - 0.5) * max * 2);
    rx.set(-((e.clientY - r.top) / r.height - 0.5) * max * 2);
  };
  const reset = () => {
    rx.set(0);
    ry.set(0);
  };
  return (
    <motion.div className={cn('[perspective:1000px]', className)} onPointerMove={onMove} onPointerLeave={reset}>
      <motion.div style={{ rotateX: srx, rotateY: sry, transformStyle: 'preserve-3d' }} className="h-full">
        {children}
      </motion.div>
    </motion.div>
  );
}

/** Pulls its child a few pixels toward the pointer — used on the main call-to-action. */
export function Magnetic({ children, className, strength = 0.25 }: { children: ReactNode; className?: string; strength?: number }) {
  const reduce = useReducedMotion();
  const x = useSpring(0, { stiffness: 220, damping: 15 });
  const y = useSpring(0, { stiffness: 220, damping: 15 });
  return (
    <motion.div
      className={cn('inline-block', className)}
      style={{ x, y }}
      onPointerMove={(e) => {
        if (reduce || e.pointerType !== 'mouse') return;
        const r = e.currentTarget.getBoundingClientRect();
        x.set((e.clientX - r.left - r.width / 2) * strength);
        y.set((e.clientY - r.top - r.height / 2) * strength);
      }}
      onPointerLeave={() => {
        x.set(0);
        y.set(0);
      }}
    >
      {children}
    </motion.div>
  );
}

/**
 * A red-pen scribble that draws itself under a word. The stroke keeps its width at any size
 * (non-scaling stroke), so it is drawn with a long dash offset in screen pixels rather than pathLength.
 */
export function PenUnderline({ className, delay = 0.2, inView = true }: { className?: string; delay?: number; inView?: boolean }) {
  const trigger = inView ? { whileInView: { strokeDashoffset: 0 }, viewport: { once: true, amount: 0.8 } } : { animate: { strokeDashoffset: 0 } };
  return (
    <svg viewBox="0 0 300 20" preserveAspectRatio="none" className={cn('pointer-events-none absolute -bottom-2 left-0 h-3.5 w-full overflow-visible text-pen', className)} aria-hidden>
      <motion.path
        d="M3 13 C 60 5, 120 4, 180 8 S 270 15, 297 7"
        fill="none" stroke="currentColor" strokeWidth="3.5" strokeLinecap="round" vectorEffect="non-scaling-stroke"
        strokeDasharray="3000" initial={{ strokeDashoffset: 3000 }} {...trigger} transition={{ duration: 0.8, ease: 'easeInOut', delay }}
      />
    </svg>
  );
}

/** Three chalk dots, as if Mitra is writing. */
export function TypingDots({ className }: { className?: string }) {
  return (
    <span className={cn('inline-flex items-center gap-1', className)} aria-hidden>
      {[0, 1, 2].map((i) => (
        <motion.span
          key={i}
          className="h-2 w-2 rounded-full bg-chalk-text/70"
          animate={{ y: [0, -4, 0], opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 0.9, repeat: Infinity, delay: i * 0.15, ease: 'easeInOut' }}
        />
      ))}
    </span>
  );
}

const DOODLES: { d: string; cls: string; depth: number; rot: number; dur: number }[] = [
  // star
  { d: 'M12 2l2.6 6.6L21 9.3l-5 4.4 1.5 6.8L12 17l-5.5 3.5L8 13.7 3 9.3l6.4-.7Z', cls: 'left-[46%] top-[9%] h-6 w-6 text-accent', depth: -40, rot: 18, dur: 7 },
  // paper plane
  { d: 'M2 11 22 3l-6 18-4-7-10-3Zm10 3 4-6', cls: 'right-[4%] top-[4%] h-9 w-9 text-secondary/70', depth: -70, rot: -8, dur: 9 },
  // squiggle
  { d: 'M2 12c3-6 5 6 8 0s5 6 8 0 4 4 4 4', cls: 'left-[2%] bottom-[12%] h-8 w-14 text-primary/50', depth: 50, rot: 6, dur: 8 },
  // circle (OMR bubble)
  { d: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18Z', cls: 'right-[42%] bottom-[6%] h-7 w-7 text-pen/50', depth: 30, rot: 0, dur: 6 },
  // plus
  { d: 'M12 4v16M4 12h16', cls: 'left-[53%] top-[34%] h-5 w-5 text-secondary/50', depth: -25, rot: 45, dur: 10 },
];

/** Soft colour blobs and hand-drawn doodles behind the hero; doodles drift with scroll. */
export function HeroBackdrop() {
  const reduce = useReducedMotion();
  const ref = useRef<HTMLDivElement>(null);
  const { scrollY } = useScroll();
  return (
    <div ref={ref} className="pointer-events-none absolute inset-0 -z-10 overflow-hidden" aria-hidden>
      <motion.div
        className="absolute -left-24 top-10 h-72 w-72 rounded-full bg-primary/15 blur-3xl sm:h-96 sm:w-96"
        animate={reduce ? undefined : { x: [0, 40, 0], y: [0, 24, 0] }}
        transition={{ duration: 16, repeat: Infinity, ease: 'easeInOut' }}
      />
      <motion.div
        className="absolute -right-20 top-32 h-72 w-72 rounded-full bg-secondary/15 blur-3xl sm:h-[28rem] sm:w-[28rem]"
        animate={reduce ? undefined : { x: [0, -30, 0], y: [0, -20, 0] }}
        transition={{ duration: 18, repeat: Infinity, ease: 'easeInOut' }}
      />
      <motion.div
        className="absolute bottom-0 left-1/3 h-56 w-56 rounded-full bg-marigold/30 blur-3xl"
        animate={reduce ? undefined : { scale: [1, 1.15, 1] }}
        transition={{ duration: 12, repeat: Infinity, ease: 'easeInOut' }}
      />
      {DOODLES.map((d, i) => (
        <Doodle key={i} {...d} scrollY={scrollY} reduce={!!reduce} index={i} />
      ))}
    </div>
  );
}

function Doodle({ d, cls, depth, rot, dur, scrollY, reduce, index }: (typeof DOODLES)[number] & { scrollY: MotionValue<number>; reduce: boolean; index: number }) {
  const y = useTransform(scrollY, [0, 600], [0, reduce ? 0 : depth]);
  return (
    <motion.svg
      viewBox="0 0 24 24"
      className={cn('absolute hidden sm:block', cls)}
      style={{ y }}
      initial={{ opacity: 0, scale: 0.6 }}
      animate={{ opacity: 1, scale: 1, rotate: reduce ? rot : [rot, rot + 10, rot] }}
      transition={{ opacity: { delay: 0.8 + index * 0.12, duration: 0.5 }, scale: { delay: 0.8 + index * 0.12, duration: 0.5 }, rotate: { duration: dur, repeat: Infinity, ease: 'easeInOut' } }}
    >
      <path d={d} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    </motion.svg>
  );
}

/** Empty and filled OMR bubbles floating slowly — background of the final call-to-action. */
export function FloatingBubbles({ count = 14, className }: { count?: number; className?: string }) {
  const reduce = useReducedMotion();
  const items = Array.from({ length: count }, (_, i) => ({
    left: (i * 37) % 100,
    top: (i * 53) % 100,
    size: 10 + ((i * 7) % 22),
    filled: i % 3 === 0,
    dur: 6 + (i % 5) * 1.5,
    delay: (i % 7) * 0.4,
  }));
  return (
    <div className={cn('pointer-events-none absolute inset-0 overflow-hidden', className)} aria-hidden>
      {items.map((b, i) => (
        <motion.span
          key={i}
          className={cn('absolute rounded-full', b.filled ? 'bg-marigold/25' : 'border-2 border-white/15')}
          style={{ left: `${b.left}%`, top: `${b.top}%`, width: b.size, height: b.size }}
          animate={reduce ? undefined : { y: [0, -18, 0], opacity: [0.5, 1, 0.5] }}
          transition={{ duration: b.dur, repeat: Infinity, delay: b.delay, ease: 'easeInOut' }}
        />
      ))}
    </div>
  );
}

/** A short burst of sparks, e.g. when a score clears the cut-off. Re-runs whenever `play` changes key. */
export function SparkBurst({ className, color = 'bg-secondary' }: { className?: string; color?: string }) {
  const reduce = useReducedMotion();
  if (reduce) return null;
  return (
    <span className={cn('pointer-events-none absolute inset-0', className)} aria-hidden>
      {Array.from({ length: 10 }, (_, i) => {
        const a = (i / 10) * Math.PI * 2;
        return (
          <motion.span
            key={i}
            className={cn('absolute left-1/2 top-1/2 h-1.5 w-1.5 rounded-full', i % 2 ? color : 'bg-accent')}
            initial={{ x: 0, y: 0, opacity: 1, scale: 1 }}
            animate={{ x: Math.cos(a) * 56, y: Math.sin(a) * 40, opacity: 0, scale: 0.4 }}
            transition={{ duration: 0.75, ease: 'easeOut', delay: 0.05 }}
          />
        );
      })}
    </span>
  );
}

/** Dashed hand-drawn arrow that draws itself (used between the loop's sticky notes). */
export function DrawnArrow({ className, delay = 0 }: { className?: string; delay?: number }) {
  return (
    <svg viewBox="0 0 80 40" className={cn('pointer-events-none text-ink/50', className)} aria-hidden>
      <motion.path
        d="M4 30 C 24 4, 52 4, 72 22"
        fill="none" stroke="currentColor" strokeWidth="2" strokeDasharray="4 5" strokeLinecap="round"
        initial={{ pathLength: 0, opacity: 0 }} whileInView={{ pathLength: 1, opacity: 1 }} viewport={{ once: true, amount: 0.8 }}
        transition={{ duration: 0.6, ease: 'easeInOut', delay }}
      />
      <motion.path
        d="M64 14 L73 23 L61 26"
        fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
        initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true, amount: 0.8 }}
        transition={{ duration: 0.2, delay: delay + 0.55 }}
      />
    </svg>
  );
}
