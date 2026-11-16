import type { ReactNode } from 'react';
import { CircleHelp, Shuffle, Sprout, Target, TrendingUp, Zap, type LucideIcon } from 'lucide-react';
import type { PersonaTrait } from '@prepmitra/shared';
import { Mitra } from '@/components/ui';
import { cn } from '@/utils/cn';

/**
 * Building blocks for the redesigned AI screens (persona, blackboard tutor, doubt solver, teach-back, cheat codes):
 * a chalkboard in a wooden frame, small uppercase labels, Mitra's speech bubbles and the shared SVG drawings.
 */

/** Dark green chalkboard in a brown wooden frame. */
export function Chalkboard({ children, className, as: Tag = 'section', ariaLabel }: { children: ReactNode; className?: string; as?: 'section' | 'div' | 'aside'; ariaLabel?: string }) {
  return (
    <Tag aria-label={ariaLabel} className={cn('rounded-[22px] border-[7px] border-wood bg-chalkboard text-chalk-text shadow-[0_4px_0_rgb(28_35_33/0.25)]', className)}>
      {children}
    </Tag>
  );
}

/** Small uppercase label, e.g. "MITRA · AI COACH". `tone="chalk"` for use on a chalkboard. */
export function Eyebrow({ children, tone = 'muted', dot, className }: { children: ReactNode; tone?: 'muted' | 'chalk' | 'primary' | 'pen' | 'green'; dot?: boolean; className?: string }) {
  const tones = { muted: 'text-muted', chalk: 'text-marigold', primary: 'text-primary', pen: 'text-pen', green: 'text-secondary' };
  return (
    <p className={cn('inline-flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-[0.14em] sm:text-[11px]', tones[tone], className)}>
      {dot && <span aria-hidden className="h-2 w-2 rounded-full bg-accent ring-2 ring-accent/30" />}
      {children}
    </p>
  );
}

/** Handwritten eyebrow above a page heading ("the evidence —"). */
export function HandLine({ children, tone = 'green', className }: { children: ReactNode; tone?: 'green' | 'pen' | 'primary' | 'chalk'; className?: string }) {
  const tones = { green: 'text-secondary', pen: 'text-pen', primary: 'text-primary', chalk: 'text-marigold' };
  return <p className={cn('font-hand text-base sm:text-lg', tones[tone], className)}>{children}</p>;
}

/** Mitra coach bubble: avatar plus a dark card with the "MITRA · AI COACH" label. */
export function CoachBubble({ children, label = 'Mitra · AI coach', className, tone = 'chalk' }: { children: ReactNode; label?: string; className?: string; tone?: 'chalk' | 'paper' }) {
  return (
    <div className={cn('flex items-start gap-3', className)}>
      <Mitra size={36} className="mt-1" />
      <div className={cn('min-w-0 rounded-[4px_16px_16px_16px] px-4 py-2.5',
        tone === 'chalk' ? 'border border-white/10 bg-chalk-deep text-chalk-text shadow-[0_4px_0_var(--color-wood)]' : 'border-[1.5px] border-ink bg-card text-ink')}>
        <Eyebrow tone={tone === 'chalk' ? 'chalk' : 'primary'}>{label}</Eyebrow>
        <div className="mt-0.5 font-hand text-base leading-snug sm:text-[17px]">{children}</div>
      </div>
    </div>
  );
}

/** Small pill note: the AI / calculated-by-code disclaimers. */
export function AiNote({ children, className, tone = 'paper' }: { children: ReactNode; className?: string; tone?: 'paper' | 'green' | 'chalk' }) {
  const tones = { paper: 'border border-line-strong bg-card text-muted', green: 'bg-secondary-soft text-secondary', chalk: 'text-chalk-text/70' };
  return <p className={cn('rounded-full px-3 py-1 text-[11px] font-medium leading-snug sm:text-xs', tones[tone], className)}>{children}</p>;
}

/** Card with the hard ink shadow used for "selected" surfaces in the design. */
export const hardCard = 'rounded-[18px] border-[1.5px] border-ink bg-card shadow-[4px_5px_0_#1c2321]';
export const softCard = 'rounded-[18px] border border-line bg-card';

// ---------- personas ----------
const PERSONA_ICONS: Record<string, LucideIcon> = {
  zap: Zap, target: Target, shuffle: Shuffle, sunrise: Sprout, 'trending-up': TrendingUp, 'help-circle': CircleHelp,
};
export function PersonaIcon({ name, className }: { name: string; className?: string }) {
  const Icon = PERSONA_ICONS[name] ?? Zap;
  return <Icon className={className} aria-hidden />;
}

export const TRAITS: { key: PersonaTrait; label: string }[] = [
  { key: 'speed', label: 'Speed' },
  { key: 'accuracy', label: 'Accuracy' },
  { key: 'risk', label: 'Risk-taking' },
  { key: 'stamina', label: 'Stamina' },
  { key: 'recovery', label: 'Recovery' },
  { key: 'consistency', label: 'Consistency' },
];

/** Six-axis trait shape. Values 0–100. */
export function RadarChart({ series, size = 260, className }: {
  series: { values: Record<PersonaTrait, number>; color: string; dashed?: boolean; fill?: boolean; label: string }[];
  size?: number;
  className?: string;
}) {
  const c = size / 2;
  const R = size / 2 - 34;
  const pt = (i: number, v: number) => {
    const a = (Math.PI * 2 * i) / TRAITS.length - Math.PI / 2;
    return [c + Math.cos(a) * R * (v / 100), c + Math.sin(a) * R * (v / 100)] as const;
  };
  const ring = (v: number) => TRAITS.map((_, i) => pt(i, v).join(',')).join(' ');
  return (
    <svg viewBox={`0 0 ${size} ${size}`} className={cn('h-auto w-full max-w-[320px]', className)} role="img"
      aria-label={`Trait shape: ${series.map((s) => `${s.label} — ${TRAITS.map((t) => `${t.label} ${Math.round(s.values[t.key])}`).join(', ')}`).join('; ')}`}>
      {[25, 50, 75, 100].map((v) => <polygon key={v} points={ring(v)} fill="none" stroke="#e3e2d8" strokeWidth={1} />)}
      {TRAITS.map((t, i) => {
        const [x, y] = pt(i, 100);
        const [lx, ly] = pt(i, 122);
        return (
          <g key={t.key}>
            <line x1={c} y1={c} x2={x} y2={y} stroke="#e3e2d8" strokeWidth={1} />
            <text x={lx} y={ly} textAnchor={Math.abs(lx - c) < 4 ? 'middle' : lx > c ? 'start' : 'end'} dominantBaseline="middle" fontSize={10.5} fill="#5b6661">{t.label}</text>
          </g>
        );
      })}
      {series.map((s) => {
        const pts = TRAITS.map((t, i) => pt(i, Math.max(0, Math.min(100, s.values[t.key]))));
        return (
          <g key={s.label}>
            <polygon points={pts.map((p) => p.join(',')).join(' ')} fill={s.fill ? s.color : 'none'} fillOpacity={s.fill ? 0.22 : 0}
              stroke={s.color} strokeWidth={s.dashed ? 2 : 2.5} strokeDasharray={s.dashed ? '5 4' : undefined} strokeLinejoin="round" />
            {!s.dashed && pts.map(([x, y], i) => <circle key={i} cx={x} cy={y} r={3.5} fill={s.color} stroke="#1c2321" strokeWidth={0.8} />)}
          </g>
        );
      })}
    </svg>
  );
}

// ---------- seating diagram (blackboard tutor) ----------
/** Circular table. Seat indices go clockwise from the top seat 0; `placed` maps seat → letter; `arrow` is [from, to]. */
export function SeatingDiagram({ seats, placed = {}, arrow, size = 240, centre = 'facing centre', className }: {
  seats: number; placed?: Record<string, string>; arrow?: [number, number]; size?: number; centre?: string; className?: string;
}) {
  const c = size / 2;
  const R = size * 0.36;
  const r = size * 0.075;
  const pos = (i: number, rad = R) => {
    const a = (Math.PI * 2 * i) / seats - Math.PI / 2; // clockwise from the top in screen coordinates
    return [c + Math.cos(a) * rad, c + Math.sin(a) * rad] as const;
  };
  let arc: ReactNode = null;
  if (arrow && seats > 0) {
    const [from, to] = arrow;
    // Shortest way round; positive = clockwise.
    let delta = (((to - from) % seats) + seats) % seats;
    if (delta > seats / 2) delta -= seats;
    const ar = R + r + 10;
    const a0 = (Math.PI * 2 * from) / seats - Math.PI / 2;
    const a1 = a0 + (Math.PI * 2 * delta) / seats;
    const [x0, y0] = [c + Math.cos(a0) * ar, c + Math.sin(a0) * ar];
    const [x1, y1] = [c + Math.cos(a1) * ar, c + Math.sin(a1) * ar];
    const large = Math.abs(delta) > seats / 2 ? 1 : 0;
    const sweep = delta > 0 ? 1 : 0;
    arc = (
      <g>
        <path d={`M${x0},${y0} A${ar},${ar} 0 ${large} ${sweep} ${x1},${y1}`} fill="none" stroke="#ffd27a" strokeWidth={2.5} markerEnd="url(#seat-arrow)" />
        {Array.from({ length: Math.abs(delta) }, (_, k) => {
          const a = a0 + ((Math.PI * 2) / seats) * Math.sign(delta) * (k + 1) - ((Math.PI * 2) / seats) * Math.sign(delta) * 0.5;
          return <text key={k} x={c + Math.cos(a) * (ar + 12)} y={c + Math.sin(a) * (ar + 12)} fontSize={12} fill="#ffd27a" textAnchor="middle" dominantBaseline="middle" fontFamily="var(--font-hand)">{k + 1}</text>;
        })}
      </g>
    );
  }
  const label = `Circular table with ${seats} seats${Object.keys(placed).length ? `: ${Object.entries(placed).map(([s, l]) => `${l} in seat ${Number(s) + 1}`).join(', ')}` : ''}`;
  return (
    <svg viewBox={`-20 -20 ${size + 40} ${size + 40}`} className={cn('h-auto w-full', className)} role="img" aria-label={label}>
      <defs>
        <marker id="seat-arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="#ffd27a" />
        </marker>
      </defs>
      <circle cx={c} cy={c} r={R - r - 8} fill="none" stroke="#f5f3ea" strokeOpacity={0.85} strokeWidth={2.5} />
      <text x={c} y={c} textAnchor="middle" dominantBaseline="middle" fontSize={12} fill="#f5f3ea" fontFamily="var(--font-hand)">{centre}</text>
      {arc}
      {Array.from({ length: seats }, (_, i) => {
        const [x, y] = pos(i);
        const who = placed[String(i)];
        const isTarget = arrow && arrow[1] === i;
        return (
          <g key={i}>
            <circle cx={x} cy={y} r={r} fill={who ? (isTarget ? '#ffd27a' : '#f5f3ea') : 'none'} stroke={who ? (isTarget ? '#f28c28' : '#f5f3ea') : '#f5f3ea'}
              strokeOpacity={who ? 1 : 0.55} strokeWidth={who ? 2 : 1.5} strokeDasharray={who ? undefined : '3 3'} />
            {who && <text x={x} y={y + 1} textAnchor="middle" dominantBaseline="middle" fontSize={r * 1.05} fontWeight={700} fill="#17392c" fontFamily="var(--font-hand)">{who}</text>}
          </g>
        );
      })}
    </svg>
  );
}

/** Round score ring that fills up to `value` of `max` (teach-back score). */
export function Ring({ value, max, size = 92, label }: { value: number | null; max: number; size?: number; label?: string }) {
  const stroke = 9;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const pct = value == null ? 0 : Math.max(0, Math.min(1, value / max));
  return (
    <div className="relative inline-flex shrink-0 items-center justify-center" style={{ width: size, height: size }} role="img" aria-label={label ?? (value == null ? 'No score yet' : `${value} of ${max}`)}>
      <svg width={size} height={size} className="-rotate-90" aria-hidden>
        <circle cx={size / 2} cy={size / 2} r={r} stroke="#e3e2d8" strokeWidth={stroke} fill="none" />
        {value != null && <circle cx={size / 2} cy={size / 2} r={r} stroke="#c2410c" strokeWidth={stroke} fill="none" strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c - pct * c} />}
      </svg>
      {value != null && <span className="absolute font-display text-xl font-extrabold text-ink">{value}<span className="text-xs font-semibold text-muted">/{max}</span></span>}
    </div>
  );
}
