import type { ReactNode } from 'react';
import { CircleAlert, Inbox, Info, RefreshCw, TriangleAlert, CircleCheck } from 'lucide-react';
import { cn } from '@/utils/cn';
import { Button } from './Button';

// ---------- Badge ----------
export type BadgeTone = 'neutral' | 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info';

const badgeTones: Record<BadgeTone, string> = {
  neutral: 'bg-stone-100 text-stone-700',
  primary: 'bg-primary-soft text-primary',
  secondary: 'bg-secondary-soft text-secondary',
  success: 'bg-success-soft text-green-700',
  warning: 'bg-warning-soft text-warning-ink',
  danger: 'bg-danger-soft text-red-700',
  info: 'bg-info-soft text-secondary',
};

export function Badge({ tone = 'neutral', children, className, icon }: { tone?: BadgeTone; children: ReactNode; className?: string; icon?: ReactNode }) {
  return (
    <span className={cn('inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium whitespace-nowrap', badgeTones[tone], className)}>
      {icon}
      {children}
    </span>
  );
}

// ---------- ProgressBar ----------
export function ProgressBar({
  value, max = 100, tone = 'primary', label, showValue, className, size = 'md',
}: { value: number; max?: number; tone?: 'primary' | 'success' | 'warning' | 'danger' | 'secondary'; label?: string; showValue?: boolean; className?: string; size?: 'sm' | 'md' }) {
  const pct = Math.max(0, Math.min(100, max > 0 ? (value / max) * 100 : 0));
  const tones = { primary: 'bg-primary', success: 'bg-success', warning: 'bg-warning', danger: 'bg-danger', secondary: 'bg-secondary' };
  return (
    <div className={className}>
      {(label || showValue) && (
        <div className="mb-1 flex justify-between text-xs">
          {label && <span className="font-medium text-ink">{label}</span>}
          {showValue && <span className="text-muted">{Math.round(pct)}%</span>}
        </div>
      )}
      <div
        className={cn('w-full overflow-hidden rounded-full bg-stone-100', size === 'sm' ? 'h-1.5' : 'h-2.5')}
        role="progressbar"
        aria-valuenow={Math.round(pct)}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={label}
      >
        <div className={cn('h-full rounded-full transition-[width] duration-500', tones[tone])} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export const accuracyTone = (v: number) => (v >= 75 ? 'success' : v >= 50 ? 'warning' : 'danger') as 'success' | 'warning' | 'danger';

// ---------- Skeleton ----------
export function Skeleton({ className }: { className?: string }) {
  return <div className={cn('animate-pulse rounded-md bg-stone-200/70', className)} aria-hidden />;
}

export function LoadingSkeleton({ variant = 'cards', count = 3 }: { variant?: 'cards' | 'list' | 'page' | 'table'; count?: number }) {
  if (variant === 'page')
    return (
      <div className="space-y-6" role="status" aria-label="Loading">
        <Skeleton className="h-8 w-1/3" />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-24" />)}
        </div>
        <Skeleton className="h-64" />
      </div>
    );
  if (variant === 'list' || variant === 'table')
    return (
      <div className="space-y-3" role="status" aria-label="Loading">
        {Array.from({ length: count }).map((_, i) => <Skeleton key={i} className="h-14" />)}
      </div>
    );
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" role="status" aria-label="Loading">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="space-y-3 rounded-[var(--radius-card)] border border-line bg-card p-5">
          <Skeleton className="h-5 w-2/3" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-9 w-32" />
        </div>
      ))}
    </div>
  );
}

// ---------- Empty / Error ----------
export function EmptyState({
  icon, title, description, action, className,
}: { icon?: ReactNode; title: string; description?: string; action?: ReactNode; className?: string }) {
  return (
    <div className={cn('flex flex-col items-center justify-center rounded-[var(--radius-card)] border border-dashed border-line-strong bg-card px-6 py-12 text-center', className)}>
      <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-primary-soft text-primary">
        {icon ?? <Inbox className="h-6 w-6" aria-hidden />}
      </div>
      <h3 className="text-base font-semibold">{title}</h3>
      {description && <p className="mt-1 max-w-md text-sm text-muted">{description}</p>}
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}

export function ErrorState({
  title = 'Something went wrong', description = 'We could not load this content. Check your connection and try again.', onRetry, className,
}: { title?: string; description?: string; onRetry?: () => void; className?: string }) {
  return (
    <div role="alert" className={cn('flex flex-col items-center justify-center rounded-[var(--radius-card)] border border-red-200 bg-danger-soft px-6 py-10 text-center', className)}>
      <CircleAlert className="mb-3 h-8 w-8 text-danger" aria-hidden />
      <h3 className="text-base font-semibold">{title}</h3>
      <p className="mt-1 max-w-md text-sm text-muted">{description}</p>
      {onRetry && (
        <Button variant="outline" className="mt-5" onClick={onRetry} leftIcon={<RefreshCw className="h-4 w-4" />}>
          Try again
        </Button>
      )}
    </div>
  );
}

// ---------- Alert / Notice ----------
export function Notice({
  tone = 'info', title, children, className, action,
}: { tone?: 'info' | 'warning' | 'success' | 'danger'; title?: ReactNode; children?: ReactNode; className?: string; action?: ReactNode }) {
  const map = {
    info: { cls: 'border-secondary/25 bg-info-soft text-secondary-hover', Icon: Info },
    warning: { cls: 'border-amber-200 bg-warning-soft text-amber-900', Icon: TriangleAlert },
    success: { cls: 'border-green-200 bg-success-soft text-green-900', Icon: CircleCheck },
    danger: { cls: 'border-red-200 bg-danger-soft text-red-900', Icon: CircleAlert },
  }[tone];
  return (
    <div className={cn('flex gap-3 rounded-lg border px-4 py-3 text-sm', map.cls, className)} role={tone === 'danger' ? 'alert' : 'note'}>
      <map.Icon className="mt-0.5 h-4 w-4 shrink-0" aria-hidden />
      <div className="min-w-0 flex-1">
        {title && <p className="font-semibold">{title}</p>}
        {children && <div className={cn(title && 'mt-0.5', 'opacity-90')}>{children}</div>}
      </div>
      {action}
    </div>
  );
}

/** Small, consistent label marking demo-only data and simulated features. */
export function DemoBadge({ children = 'Demo data', className }: { children?: ReactNode; className?: string }) {
  return (
    <Badge tone="warning" className={className}>
      {children}
    </Badge>
  );
}

export function Spinner({ className, label = 'Loading' }: { className?: string; label?: string }) {
  return (
    <span role="status" aria-label={label} className={cn('inline-block h-5 w-5 animate-spin rounded-full border-2 border-primary/30 border-t-primary', className)} />
  );
}
