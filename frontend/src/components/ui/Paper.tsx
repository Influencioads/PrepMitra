import type { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/utils/cn';

/**
 * Concept B building blocks: the answer sheet and the blackboard.
 * - Paper surfaces and red-pen marks are for results and feedback.
 * - Chalkboard surfaces are for Mitra (the AI coach) and focus mode.
 * Handwriting (font-hand) is reserved for short notes; numbers that matter stay in the display font.
 */

/** Mitra, the AI coach. A friendly saffron face; purely decorative unless a label is given. */
export function Mitra({ size = 48, className, label }: { size?: number; className?: string; label?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      className={cn('shrink-0', className)}
      role={label ? 'img' : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
    >
      <circle cx="24" cy="24" r="22" fill="#F28C28" />
      <circle cx="24" cy="24" r="16.5" fill="none" stroke="#C2410C" strokeWidth="2" strokeDasharray="3 4" />
      <circle cx="18" cy="21" r="2.6" fill="#1C2321" />
      <circle cx="30" cy="21" r="2.6" fill="#1C2321" />
      <path d="M17 29q7 6 14 0" stroke="#1C2321" strokeWidth="2.4" fill="none" strokeLinecap="round" />
    </svg>
  );
}

/** Mitra with a speech bubble. `tone="chalk"` puts the words on a blackboard. */
export function MitraSays({ children, tone = 'paper', size = 48, className }: { children: ReactNode; tone?: 'paper' | 'chalk'; size?: number; className?: string }) {
  return (
    <div className={cn('flex items-start gap-3', className)}>
      <Mitra size={size} />
      <p
        className={cn(
          'min-w-0 rounded-[4px_18px_18px_18px] px-4 py-2.5 font-hand text-base leading-snug sm:text-lg',
          tone === 'chalk' ? 'bg-chalkboard text-chalk-text shadow-wood' : 'border-[1.5px] border-ink bg-card text-ink',
        )}
      >
        {children}
      </p>
    </div>
  );
}

/** A score circled in red pen, like a teacher's marks on a checked copy. The ellipse always wraps the text. */
export function PenScore({ score, total, size = 'md', className }: { score: string; total?: string | number; size?: 'sm' | 'md' | 'lg'; className?: string }) {
  const sizes = {
    sm: 'text-4xl px-4 pt-2 pb-1 border-[3px]',
    md: 'text-5xl sm:text-6xl px-5 pt-3 pb-1.5 border-[3.5px]',
    lg: 'text-6xl sm:text-7xl px-7 pt-4 pb-2 border-4',
  };
  return (
    <p className={cn('inline-block -rotate-3 whitespace-nowrap rounded-[50%] border-pen font-hand font-bold leading-none text-pen', sizes[size], className)}>
      {score}
      {total !== undefined && <span className="text-[0.45em]">/{total}</span>}
    </p>
  );
}

/** A rubber stamp, e.g. a percentile. */
export function Stamp({ value, label, tone = 'green', className }: { value: string; label: string; tone?: 'green' | 'saffron' | 'pen'; className?: string }) {
  const tones = { green: 'border-secondary text-secondary', saffron: 'border-primary text-primary', pen: 'border-pen text-pen' };
  return (
    <div className={cn('inline-block -rotate-6 rounded-lg border-[2.5px] bg-paper/90 px-3 py-1.5 text-center', tones[tone], className)}>
      <p className="font-display text-xl font-extrabold leading-none sm:text-2xl">{value}</p>
      <p className="mt-0.5 text-[9px] font-bold uppercase tracking-[0.14em]">{label}</p>
    </div>
  );
}

/** A short handwritten note in red pen (or green for praise). */
export function PenNote({ children, tone = 'pen', className }: { children: ReactNode; tone?: 'pen' | 'green'; className?: string }) {
  return <p className={cn('font-hand text-base leading-snug sm:text-lg', tone === 'pen' ? 'text-pen' : 'text-secondary', className)}>{children}</p>;
}

/** A tilted sticky note. */
export function StickyNote({ children, color = 'yellow', tilt = 0, className }: { children: ReactNode; color?: 'yellow' | 'saffron' | 'green' | 'purple'; tilt?: number; className?: string }) {
  const colors = { yellow: 'bg-sticky-yellow', saffron: 'bg-primary-soft', green: 'bg-sticky-green', purple: 'bg-sticky-purple' };
  return (
    <div className={cn('p-6 shadow-sticky', colors[color], className)} style={{ transform: tilt ? `rotate(${tilt}deg)` : undefined }}>
      {children}
    </div>
  );
}

/** A small handwritten eyebrow above a heading, e.g. "the real problem —". */
export function HandEyebrow({ children, tone = 'primary', className }: { children: ReactNode; tone?: 'primary' | 'green' | 'pen' | 'accent'; className?: string }) {
  const tones = { primary: 'text-primary', green: 'text-secondary', pen: 'text-pen', accent: 'text-accent' };
  return <p className={cn('font-hand text-lg sm:text-xl', tones[tone], className)}>{children} —</p>;
}

/** An OMR bubble. Filled bubbles read as the student's choice. */
export function Bubble({ filled, size = 18, className }: { filled?: boolean; size?: number; className?: string }) {
  return (
    <span
      aria-hidden
      className={cn('inline-block shrink-0 rounded-full', filled ? 'bg-ink' : 'border-[1.5px] border-subtle', className)}
      style={{ width: size, height: size }}
    />
  );
}

export interface LeakItem {
  label: string;
  marks: number;
  /** Tailwind background class for the swatch and bar segment. */
  color: string;
}

/** "Where your marks leaked": a stacked bar plus a legend. Marks are computed by code, never by AI. */
/** `animated` (marketing pages): the bar fills in when scrolled into view. Reports and PDFs stay static. */
export function MarksLeak({ items, title, note, className, animated = false }: { items: LeakItem[]; title: string; note?: ReactNode; className?: string; animated?: boolean }) {
  const total = items.reduce((s, i) => s + i.marks, 0);
  const fmt = (n: number) => `−${Number.isInteger(n) ? n : n.toFixed(2)}`;
  return (
    <section className={cn('rounded-[20px] border-[1.5px] border-ink bg-card p-5', className)}>
      <div className="flex items-baseline justify-between gap-3">
        <h3 className="text-lg font-bold sm:text-xl">{title}</h3>
        <span className="font-display text-xl font-extrabold tabular-nums text-pen">{total > 0 ? fmt(total) : '0'}</span>
      </div>
      {total > 0 && (
        <div className="mt-4 flex h-4 overflow-hidden rounded-full sm:h-5" aria-hidden>
          {items.filter((i) => i.marks > 0).map((i, n) => !animated ? (
            <span key={i.label} className={i.color} style={{ flex: i.marks }} />
          ) : (
            // Each leak fills in from the left, one after another, when the card scrolls into view.
            <motion.span
              key={i.label}
              className={cn(i.color, 'origin-left')}
              style={{ flex: i.marks }}
              initial={{ scaleX: 0 }}
              whileInView={{ scaleX: 1 }}
              viewport={{ once: true, amount: 0.6 }}
              transition={{ duration: 0.5, delay: 0.15 + n * 0.25, ease: [0.22, 1, 0.36, 1] }}
            />
          ))}
        </div>
      )}
      <ul className="mt-4 space-y-2.5 text-sm sm:text-base">
        {items.map((i) => (
          <li key={i.label} className="flex items-center gap-3">
            <span className={cn('h-3 w-3 shrink-0 rounded-[3px]', i.color)} aria-hidden />
            <span className="min-w-0 flex-1">{i.label}</span>
            <b className="tabular-nums">{i.marks > 0 ? fmt(i.marks) : '0'}</b>
          </li>
        ))}
      </ul>
      {note && <div className="mt-4">{note}</div>}
    </section>
  );
}
