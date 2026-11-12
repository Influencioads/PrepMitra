import { useCallback, useEffect, useState, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { HeartHandshake, Lock, RefreshCw, Sparkles } from 'lucide-react';
import { classifyAiError, type Allowances } from '@prepmitra/shared';
import { Badge, Button, Notice } from '@/components/ui';
import { aiService } from '@/services/aiService';
import { cn } from '@/utils/cn';

/** Shows `support` (a distress reply from the backend) above everything else on the screen. */
export function SupportBanner({ message, className }: { message?: string | null; className?: string }) {
  if (!message) return null;
  return (
    <div role="alert" className={cn('flex gap-3 rounded-xl border-2 border-secondary bg-secondary-soft p-4 text-ink', className)}>
      <HeartHandshake className="mt-0.5 h-6 w-6 shrink-0 text-secondary" aria-hidden />
      <div>
        <p className="font-semibold text-secondary">You are not alone</p>
        <p className="mt-1 text-sm leading-relaxed">{message}</p>
        <a href="tel:14416" className="mt-3 inline-flex rounded-lg bg-secondary px-3 py-1.5 text-sm font-semibold text-white hover:bg-secondary-hover">
          Call Tele-MANAS 14416
        </a>
      </div>
    </div>
  );
}

/** 402 → upgrade prompt (links to /subscription), 422 off_topic, 503 "try again", anything else → message. */
export function AiErrorNotice({ error, onRetry, className }: { error: unknown; onRetry?: () => void; className?: string }) {
  if (!error) return null;
  const info = classifyAiError(error);
  if (info.kind === 'upgrade') {
    return (
      <Notice tone="warning" title={info.title} className={className}
        action={<Link to={info.upgradePath ?? '/subscription'} className="self-center whitespace-nowrap rounded-lg bg-primary px-3 py-1.5 text-xs font-semibold text-white hover:bg-primary-hover">See plans</Link>}>
        {info.message}
      </Notice>
    );
  }
  return (
    <Notice tone={info.kind === 'off_topic' ? 'info' : 'danger'} title={info.title} className={className}
      action={info.retryable && onRetry ? (
        <Button size="sm" variant="outline" onClick={onRetry} leftIcon={<RefreshCw className="h-3.5 w-3.5" />}>Try again</Button>
      ) : undefined}>
      {info.message}
    </Notice>
  );
}

// ---------- allowances (GET /v1/me/allowances) ----------
let cache: { at: number; data: Allowances } | null = null;
const listeners = new Set<(a: Allowances) => void>();

/** Re-read after any AI call so the "left this month" chips stay current. */
export async function refreshAllowances(): Promise<Allowances | null> {
  try {
    const data = await aiService.allowances();
    cache = { at: Date.now(), data };
    listeners.forEach((l) => l(data));
    return data;
  } catch {
    return null;
  }
}

export function useAllowances() {
  const [data, setData] = useState<Allowances | null>(cache?.data ?? null);
  useEffect(() => {
    listeners.add(setData);
    if (!cache || Date.now() - cache.at > 60_000) void refreshAllowances();
    return () => { listeners.delete(setData); };
  }, []);
  const remaining = useCallback((feature: string) => data?.limits.find((l) => l.feature === feature), [data]);
  return { data, remaining };
}

/** "12 of 50 left" for one metered feature; "Not in your plan" when the plan has none. */
export function AllowanceChip({ feature, label, className }: { feature: string; label?: string; className?: string }) {
  const { data, remaining } = useAllowances();
  if (!data) return null;
  const l = remaining(feature);
  if (!l || l.limit <= 0) return <Badge tone="neutral" className={className} icon={<Lock className="h-3 w-3" />}>{label ? `${label}: ` : ''}not in your plan</Badge>;
  return (
    <Badge tone={l.remaining === 0 ? 'danger' : l.remaining <= Math.max(1, l.limit * 0.2) ? 'warning' : 'success'} className={className}>
      {label ? `${label}: ` : ''}{l.remaining} of {l.limit} left
    </Badge>
  );
}

export function hasFlag(a: Allowances | null, flag: string) {
  const v = a?.flags[flag];
  return v !== undefined && v !== false && v !== 'none';
}

/** Small header pill + description used across the AI screens. */
export function AiPill({ children = 'AI' }: { children?: ReactNode }) {
  return <Badge tone="primary" icon={<Sparkles className="h-3 w-3" />}>{children}</Badge>;
}

/** Runs one AI request with busy / error state, refreshing allowances afterwards. */
export function useAiAction<A extends unknown[], R>(fn: (...args: A) => Promise<R>) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const run = useCallback(async (...args: A): Promise<R | undefined> => {
    setBusy(true);
    setError(null);
    try {
      return await fn(...args);
    } catch (e) {
      setError(e);
      return undefined;
    } finally {
      setBusy(false);
      void refreshAllowances();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return { run, busy, error, setError };
}

/** Loads data on mount / when `key` changes, keeping the raw error for classifyAiError. */
export function useAiQuery<T>(loader: () => Promise<T>, key: string) {
  const [data, setData] = useState<T>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown>(null);
  const [tick, setTick] = useState(0);
  useEffect(() => {
    let alive = true;
    setLoading(true);
    setError(null);
    loader().then((d) => alive && setData(d)).catch((e) => alive && setError(e)).finally(() => alive && setLoading(false));
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, tick]);
  return { data, setData, loading, error, reload: () => setTick((t) => t + 1) };
}
