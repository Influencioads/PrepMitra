import { Component, type ErrorInfo, type ReactNode } from 'react';
import { env } from '@/utils/env';

/**
 * Error reporting (15-day plan, Day 14: Sentry for the frontend).
 * The Sentry SDK is downloaded only when VITE_SENTRY_DSN is set.
 */
type Reporter = (error: unknown, context?: Record<string, unknown>) => void;
let reporter: Reporter | null = null;
let started = false;

export async function initErrorReporting(): Promise<void> {
  if (started || !env.sentryDsn) return;
  started = true;
  try {
    const Sentry = await import('@sentry/react');
    Sentry.init({ dsn: env.sentryDsn, environment: import.meta.env.MODE, tracesSampleRate: 0.1 });
    reporter = (error, context) => Sentry.captureException(error, context ? { extra: context } : undefined);
  } catch {
    started = false;
  }
}

export function reportError(error: unknown, context?: Record<string, unknown>) {
  if (reporter) reporter(error, context);
  else if (import.meta.env.DEV) console.error(error, context);
}

/** Catches render errors outside the router (the router has its own errorElement). */
export class AppErrorBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    reportError(error, { componentStack: info.componentStack ?? undefined });
  }

  render() {
    if (!this.state.failed) return this.props.children;
    return (
      <div role="alert" className="flex min-h-screen flex-col items-center justify-center gap-3 bg-background px-4 text-center">
        <h1 className="text-2xl font-bold">Something went wrong</h1>
        <p className="max-w-md text-sm text-muted">Your exam answers are saved on this device. Reload the page to continue.</p>
        <button type="button" onClick={() => window.location.reload()} className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white">
          Reload
        </button>
      </div>
    );
  }
}
