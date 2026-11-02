import { env } from '@/utils/env';

/**
 * Product analytics (15-day plan, Day 12). Events from the MVP doc's analytics list.
 * Provider-agnostic: events go to window.gtag (GA4) when present, to any provider
 * registered with `setAnalyticsProvider` (e.g. PostHog), and to an in-memory queue
 * that tests and the dev console can inspect. No personal data (phone, email) is sent.
 */
export type AnalyticsEvent =
  | 'signup_completed'
  | 'login'
  | 'onboarding_completed'
  | 'purchase_started'
  | 'purchase_completed'
  | 'purchase_failed'
  | 'exam_started'
  | 'exam_submitted'
  | 'report_viewed'
  | 'report_rated'
  | 'interview_started'
  | 'interview_completed';

export type AnalyticsProps = Record<string, string | number | boolean | undefined>;

export interface TrackedEvent {
  event: AnalyticsEvent;
  props: AnalyticsProps;
  at: string;
}

type Provider = (event: AnalyticsEvent, props: AnalyticsProps) => void;

const MAX_QUEUE = 200;
const queue: TrackedEvent[] = [];
let provider: Provider | null = null;

declare global {
  interface Window {
    gtag?: (command: 'event', name: string, params?: Record<string, unknown>) => void;
  }
}

/** Plug in a vendor SDK, e.g. `setAnalyticsProvider((e, p) => posthog.capture(e, p))`. */
export function setAnalyticsProvider(fn: Provider | null) {
  provider = fn;
}

export function track(event: AnalyticsEvent, props: AnalyticsProps = {}) {
  const entry: TrackedEvent = { event, props, at: new Date().toISOString() };
  queue.push(entry);
  if (queue.length > MAX_QUEUE) queue.shift();
  try {
    if (typeof window !== 'undefined' && typeof window.gtag === 'function') window.gtag('event', event, props);
    provider?.(event, props);
  } catch {
    /* analytics must never break the app */
  }
  if (env.analyticsDebug && import.meta.env.MODE !== 'test') console.debug('[analytics]', event, props);
}

/** Recent events (newest last). Useful for tests and debugging. */
export const getTrackedEvents = (): readonly TrackedEvent[] => queue;
export const clearTrackedEvents = () => {
  queue.length = 0;
};
