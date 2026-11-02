import type { ReactNode } from 'react';
import { CircleCheck, TriangleAlert } from 'lucide-react';
import { Badge, Card, ErrorState, LoadingSkeleton, Skeleton, type BadgeTone } from '@/components/ui';
import { cn } from '@/utils/cn';
import type { AdminLoadState } from './useAdminLoad';

// ---------- DataTable ----------
export interface Column<T> {
  key: string;
  header: ReactNode;
  cell: (row: T) => ReactNode;
  className?: string;
  /** Visually hidden header (e.g. for the actions column). */
  srHeader?: boolean;
}

/** Plain semantic table that scrolls horizontally inside its card on small screens. */
export function DataTable<T>({
  columns, rows, rowKey, caption, empty, minWidth = 720, className, rowClassName,
}: {
  columns: Column<T>[];
  rows: T[];
  rowKey: (row: T) => string;
  caption: string;
  empty?: ReactNode;
  minWidth?: number;
  className?: string;
  rowClassName?: (row: T) => string | undefined;
}) {
  if (rows.length === 0 && empty) return <>{empty}</>;
  return (
    <Card className={cn('overflow-hidden', className)}>
      <div className="relative overflow-x-auto scrollbar-thin" tabIndex={0} role="region" aria-label={caption}>
        <table className="w-full text-left text-sm" style={{ minWidth }}>
          <caption className="sr-only">{caption}</caption>
          <thead className="border-b border-line bg-stone-50/80 text-xs font-semibold uppercase tracking-wide text-muted">
            <tr>
              {columns.map((c) => (
                <th key={c.key} scope="col" className={cn('px-4 py-3 whitespace-nowrap', c.className)}>
                  {c.srHeader ? <span className="sr-only">{c.header}</span> : c.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {rows.map((row) => (
              <tr key={rowKey(row)} className={cn('align-middle hover:bg-stone-50/60', rowClassName?.(row))}>
                {columns.map((c) => (
                  <td key={c.key} className={cn('px-4 py-3', c.className)}>
                    {c.cell(row)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

// ---------- Small controls ----------
export function StatusBadge({ map, value, className }: { map: Record<string, { label: string; tone: BadgeTone }>; value: string; className?: string }) {
  const m = map[value] ?? { label: value, tone: 'neutral' as const };
  return <Badge tone={m.tone} className={className}>{m.label}</Badge>;
}

/** Compact switch for table cells. `label` is announced to screen readers. */
export function ToggleSwitch({
  checked, onChange, label, disabled, showLabel,
}: { checked: boolean; onChange: (v: boolean) => void; label: string; disabled?: boolean; showLabel?: ReactNode }) {
  return (
    <span className="inline-flex items-center gap-2">
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        aria-label={label}
        title={label}
        disabled={disabled}
        onClick={() => onChange(!checked)}
        className={cn(
          'relative inline-flex h-5 w-9 shrink-0 items-center rounded-full transition-colors disabled:cursor-not-allowed disabled:opacity-50',
          checked ? 'bg-primary' : 'bg-stone-300',
        )}
      >
        <span className={cn('inline-block h-4 w-4 rounded-full bg-card shadow transition-transform', checked ? 'translate-x-[18px]' : 'translate-x-0.5')} />
      </button>
      {showLabel && <span className="text-xs text-muted">{showLabel}</span>}
    </span>
  );
}

export function IconButton({
  label, onClick, children, tone = 'default', disabled,
}: { label: string; onClick: () => void; children: ReactNode; tone?: 'default' | 'danger' | 'success'; disabled?: boolean }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={label}
      title={label}
      disabled={disabled}
      className={cn(
        'inline-flex h-8 w-8 items-center justify-center rounded-md transition-colors disabled:pointer-events-none disabled:opacity-40',
        tone === 'danger' ? 'text-danger hover:bg-danger-soft' : tone === 'success' ? 'text-success hover:bg-success-soft' : 'text-muted hover:bg-stone-100 hover:text-ink',
      )}
    >
      {children}
    </button>
  );
}

/** Filters row: stacks on phones, grid on larger screens. */
export function FilterBar({ children, className }: { children: ReactNode; className?: string }) {
  return <div className={cn('grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4', className)}>{children}</div>;
}

export function ResultCount({ count, noun, onClear }: { count: number; noun: string; onClear?: () => void }) {
  return (
    <div className="flex items-center justify-between text-sm" aria-live="polite">
      <p className="text-muted">
        {count} {count === 1 ? noun : `${noun}s`}
      </p>
      {onClear && (
        <button type="button" onClick={onClear} className="font-medium text-primary hover:underline">
          Clear filters
        </button>
      )}
    </div>
  );
}

// ---------- Loading gate ----------
export function AdminLoadGate({
  state, children, variant = 'table',
}: { state: AdminLoadState; children: ReactNode; variant?: 'table' | 'page' | 'cards' }) {
  if (state.loading) {
    if (variant === 'table')
      return (
        <div className="space-y-4" role="status" aria-label="Loading">
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-10" />)}
          </div>
          <LoadingSkeleton variant="table" count={6} />
        </div>
      );
    return <LoadingSkeleton variant={variant === 'page' ? 'page' : 'cards'} count={6} />;
  }
  if (state.error) return <ErrorState title="Could not load admin data" description={state.error} onRetry={state.reload} />;
  return <>{children}</>;
}

// ---------- Metric vs target ----------
/**
 * A KPI against a target. `higherIsBetter` decides whether value above target is good.
 * Status is shown with an icon + text, never colour alone.
 */
export function TargetCard({
  label, value, target, format, higherIsBetter = true, max, hint,
}: {
  label: string;
  value: number;
  target: number;
  format: (v: number) => string;
  higherIsBetter?: boolean;
  max?: number;
  hint?: ReactNode;
}) {
  const ok = higherIsBetter ? value >= target : value <= target;
  const scaleMax = max ?? Math.max(value, target) * 1.25;
  return (
    <Card className="p-5">
      <div className="flex items-start justify-between gap-2">
        <p className="text-sm font-medium text-muted">{label}</p>
        <Badge tone={ok ? 'success' : 'warning'} icon={ok ? <CircleCheck className="h-3 w-3" aria-hidden /> : <TriangleAlert className="h-3 w-3" aria-hidden />}>
          {ok ? 'On target' : 'Below target'}
        </Badge>
      </div>
      <p className="mt-1.5 text-2xl font-bold tracking-tight text-ink">{format(value)}</p>
      <div className="relative mt-3">
        <div
          className="h-1.5 w-full overflow-hidden rounded-full bg-stone-100"
          role="meter"
          aria-valuenow={value}
          aria-valuemin={0}
          aria-valuemax={scaleMax}
          aria-label={`${label}: ${format(value)}, target ${format(target)}`}
        >
          <div className={cn('h-full rounded-full', ok ? 'bg-success' : 'bg-warning')} style={{ width: `${Math.min(100, (value / scaleMax) * 100)}%` }} />
        </div>
        <span
          className="absolute -top-1 h-3.5 w-0.5 rounded bg-ink/70"
          style={{ left: `${Math.min(100, (target / scaleMax) * 100)}%` }}
          aria-hidden
        />
      </div>
      <p className="mt-2 text-xs text-muted">
        Target {higherIsBetter ? '≥' : '≤'} {format(target)}
        {hint && <> · {hint}</>}
      </p>
    </Card>
  );
}
