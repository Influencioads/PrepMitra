import { useId, useRef, type KeyboardEvent, type ReactNode } from 'react';
import {
  Award, Banknote, Brain, Briefcase, Calculator, ChartColumn, Clock, Code, FileText, GraduationCap, Landmark,
  Languages, Mic, Scale, Search, Shield, Sparkles, Target, TrainFront, TrendingUp, Users, type LucideIcon,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import type { IconKey } from '@prepmitra/shared';
import { initials } from '@prepmitra/shared';
import { cn } from '@/utils/cn';
import { Card } from './Card';

export const ICONS: Record<IconKey, LucideIcon> = {
  landmark: Landmark, banknote: Banknote, train: TrainFront, scale: Scale, graduation: GraduationCap, briefcase: Briefcase,
  code: Code, users: Users, trending: TrendingUp, calculator: Calculator, brain: Brain, mic: Mic, file: FileText,
  target: Target, languages: Languages, chart: ChartColumn, sparkles: Sparkles, shield: Shield, clock: Clock, award: Award,
};

export function AppIcon({ name, className }: { name: IconKey; className?: string }) {
  const Icon = ICONS[name] ?? Sparkles;
  return <Icon className={className} aria-hidden />;
}

export function IconTile({ name, tone = 'primary', className }: { name: IconKey; tone?: 'primary' | 'secondary' | 'success' | 'warning'; className?: string }) {
  const tones = {
    primary: 'bg-primary-soft text-primary',
    secondary: 'bg-secondary-soft text-secondary',
    success: 'bg-success-soft text-success',
    warning: 'bg-warning-soft text-warning-ink',
  };
  return (
    <span className={cn('inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-xl', tones[tone], className)}>
      <AppIcon name={name} className="h-5 w-5" />
    </span>
  );
}

export function Logo({ className, to = '/', light }: { className?: string; to?: string; light?: boolean }) {
  return (
    <Link to={to} className={cn('inline-flex items-center gap-2 font-bold tracking-tight', className)} aria-label="PrepMitra AI home">
      <span className={cn('flex h-8 w-8 items-center justify-center rounded-lg', light ? 'bg-card text-primary' : 'bg-primary text-white')}>
        <svg viewBox="0 0 64 64" className="h-5 w-5" aria-hidden>
          <path d="M20 46V18h13.5c6.4 0 10.5 3.9 10.5 9.6 0 5.8-4.1 9.7-10.5 9.7H27V46h-7Zm7-14.6h5.9c2.6 0 4.1-1.4 4.1-3.8 0-2.3-1.5-3.7-4.1-3.7H27v7.5Z" fill="currentColor" />
          <circle cx="47" cy="44" r="4" fill="#FCD9A8" />
        </svg>
      </span>
      <span className={cn('text-lg', light ? 'text-white' : 'text-ink')}>
        PrepMitra <span className={light ? 'text-white/70' : 'text-primary'}>AI</span>
      </span>
    </Link>
  );
}

export function Avatar({ name, size = 'md', className }: { name: string; size?: 'sm' | 'md' | 'lg'; className?: string }) {
  const s = { sm: 'h-8 w-8 text-xs', md: 'h-10 w-10 text-sm', lg: 'h-16 w-16 text-xl' }[size];
  return (
    <span className={cn('inline-flex shrink-0 items-center justify-center rounded-full bg-secondary font-semibold text-white', s, className)} aria-hidden>
      {initials(name) || 'U'}
    </span>
  );
}

export function StatCard({
  label, value, hint, icon, trend, className,
}: { label: string; value: ReactNode; hint?: ReactNode; icon?: ReactNode; trend?: { value: number; label?: string }; className?: string }) {
  return (
    <Card className={cn('p-5', className)}>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-sm font-medium text-muted">{label}</p>
          <p className="mt-1.5 text-2xl font-bold tracking-tight text-ink">{value}</p>
        </div>
        {icon && <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-soft text-primary">{icon}</span>}
      </div>
      {(hint || trend) && (
        <p className="mt-2 text-xs text-muted">
          {trend && (
            <span className={cn('mr-1 font-semibold', trend.value >= 0 ? 'text-success' : 'text-danger')}>
              {trend.value >= 0 ? '▲' : '▼'} {Math.abs(trend.value)}
              {trend.label ?? ''}
            </span>
          )}
          {hint}
        </p>
      )}
    </Card>
  );
}

export function PageHeader({
  title, description, actions, eyebrow, className,
}: { title: ReactNode; description?: ReactNode; actions?: ReactNode; eyebrow?: ReactNode; className?: string }) {
  return (
    <div className={cn('mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between', className)}>
      <div className="min-w-0">
        {eyebrow && <div className="mb-1.5">{eyebrow}</div>}
        <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">{title}</h1>
        {description && <p className="mt-1.5 max-w-2xl text-sm text-muted sm:text-base">{description}</p>}
      </div>
      {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
    </div>
  );
}

export interface TabItem<T extends string> {
  value: T;
  label: ReactNode;
  count?: number;
}

/** Accessible tabs with arrow-key navigation. Renders only the tab list; the parent renders the panel. */
export function Tabs<T extends string>({
  items, value, onChange, className, ariaLabel,
}: { items: TabItem<T>[]; value: T; onChange: (v: T) => void; className?: string; ariaLabel: string }) {
  const refs = useRef<(HTMLButtonElement | null)[]>([]);
  const id = useId();
  const onKey = (e: KeyboardEvent, i: number) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    e.preventDefault();
    const next = (i + (e.key === 'ArrowRight' ? 1 : -1) + items.length) % items.length;
    refs.current[next]?.focus();
    onChange(items[next]!.value);
  };
  return (
    <div role="tablist" aria-label={ariaLabel} className={cn('flex gap-1 overflow-x-auto border-b border-line scrollbar-thin', className)}>
      {items.map((t, i) => (
        <button
          key={t.value}
          ref={(el) => { refs.current[i] = el; }}
          id={`${id}-${t.value}`}
          role="tab"
          type="button"
          aria-selected={value === t.value}
          tabIndex={value === t.value ? 0 : -1}
          onKeyDown={(e) => onKey(e, i)}
          onClick={() => onChange(t.value)}
          className={cn(
            '-mb-px inline-flex items-center gap-2 whitespace-nowrap border-b-2 px-3 py-2.5 text-sm font-medium transition-colors',
            value === t.value ? 'border-primary text-primary' : 'border-transparent text-muted hover:text-ink',
          )}
        >
          {t.label}
          {t.count !== undefined && (
            <span className={cn('rounded-full px-1.5 text-xs', value === t.value ? 'bg-primary-soft' : 'bg-stone-100')}>{t.count}</span>
          )}
        </button>
      ))}
    </div>
  );
}

export function SearchInput({
  value, onChange, placeholder = 'Search', className, label = 'Search',
}: { value: string; onChange: (v: string) => void; placeholder?: string; className?: string; label?: string }) {
  return (
    <div className={cn('relative', className)}>
      <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" aria-hidden />
      <input
        type="search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        aria-label={label}
        className="h-10 w-full rounded-lg border border-line-strong bg-card pl-9 pr-3 text-sm placeholder:text-subtle focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/30"
      />
    </div>
  );
}

export function Stepper({ steps, current, className }: { steps: string[]; current: number; className?: string }) {
  return (
    <nav aria-label="Progress" className={className}>
      <p className="mb-2 text-sm font-medium text-muted">
        Step {current + 1} of {steps.length}: <span className="text-ink">{steps[current]}</span>
      </p>
      <ol className="flex gap-1.5">
        {steps.map((s, i) => (
          <li key={s} className="flex-1" aria-current={i === current ? 'step' : undefined}>
            <span className={cn('block h-1.5 rounded-full', i < current ? 'bg-primary' : i === current ? 'bg-primary/60' : 'bg-stone-200')} />
            <span className="sr-only">{s}{i < current ? ' (completed)' : ''}</span>
          </li>
        ))}
      </ol>
    </nav>
  );
}

export function KeyValue({ label, value, className }: { label: ReactNode; value: ReactNode; className?: string }) {
  return (
    <div className={cn('flex items-center justify-between gap-4 py-2 text-sm', className)}>
      <dt className="text-muted">{label}</dt>
      <dd className="text-right font-medium text-ink">{value}</dd>
    </div>
  );
}

export function ScoreRing({ value, size = 120, label, sublabel }: { value: number; size?: number; label?: ReactNode; sublabel?: ReactNode }) {
  const stroke = 10;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const pct = Math.max(0, Math.min(100, value));
  const color = pct >= 75 ? '#15803D' : pct >= 50 ? '#D97706' : '#DC2626';
  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90" aria-hidden>
        <circle cx={size / 2} cy={size / 2} r={r} stroke="#E3E2D8" strokeWidth={stroke} fill="none" />
        <circle cx={size / 2} cy={size / 2} r={r} stroke={color} strokeWidth={stroke} fill="none" strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c - (pct / 100) * c} />
      </svg>
      <div className="absolute text-center">
        <div className="text-2xl font-bold text-ink">{label ?? `${Math.round(pct)}%`}</div>
        {sublabel && <div className="text-xs text-muted">{sublabel}</div>}
      </div>
    </div>
  );
}
