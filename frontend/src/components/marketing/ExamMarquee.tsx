import { useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, useAnimationFrame, useMotionValue, useReducedMotion } from 'framer-motion';
import type { Exam } from '@prepmitra/shared';
import { useContentT } from '@/i18n/content';
import { cn } from '@/utils/cn';

/**
 * The chalkboard ribbon of exams, scrolling slowly sideways. It pauses while the pointer or keyboard
 * focus is on it, and stays still (scrollable by hand) for people who reduce motion.
 */
export function ExamMarquee({ exams, label }: { exams: Exam[]; label: string }) {
  const ct = useContentT();
  const reduce = useReducedMotion();
  const track = useRef<HTMLDivElement>(null);
  const x = useMotionValue(0);
  const [paused, setPaused] = useState(false);
  const moving = !reduce && exams.length > 2;

  useAnimationFrame((_, delta) => {
    if (!moving || paused || !track.current) return;
    const half = track.current.scrollWidth / 2;
    if (half <= 0) return;
    let next = x.get() - delta * 0.04; // ~40 px a second
    if (next <= -half) next += half;
    x.set(next);
  });

  // Two identical copies side by side; when the first has scrolled out, the strip jumps back by exactly one copy.
  const copyOf = (copy: number) => (
    <div className="flex shrink-0 items-center gap-6 pr-6" aria-hidden={copy === 1 || undefined}>
      {exams.map((e) => (
      <span key={e.id} className="flex shrink-0 items-center gap-6">
        <Link
          to={`/exams/${e.id}`}
          tabIndex={copy === 1 ? -1 : undefined}
          className="font-hand text-xl text-chalk-text transition-colors hover:text-marigold sm:text-2xl"
        >
          {ct(e.shortTitle)}
        </Link>
        <span className="text-accent" aria-hidden>✦</span>
      </span>
      ))}
    </div>
  );

  return (
    <nav
      aria-label={label}
      className={cn('bg-chalkboard', moving ? 'overflow-hidden' : 'overflow-x-auto scrollbar-thin')}
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
      onFocus={() => setPaused(true)}
      onBlur={() => setPaused(false)}
    >
      <motion.div ref={track} className={cn('flex w-max items-center py-5', !moving && 'px-6')} style={{ x: moving ? x : 0 }} data-testid="exam-marquee">
        {copyOf(0)}
        {moving && copyOf(1)}
      </motion.div>
    </nav>
  );
}
