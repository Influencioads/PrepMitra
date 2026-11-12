import type { ApiError } from '../types/core';

/**
 * How an AI screen should react to a failed `/v1/ai/*` call (backend `app/routers/ai.py`):
 *  - 402 `allowance_exhausted` / `plan_required` → upgrade prompt linking to the subscription screen;
 *  - 422 `off_topic` → "PrepMitra only helps with exam preparation";
 *  - 503 `ai_unavailable` → "try again" (nothing was spent);
 *  - anything else → the server's message.
 */
export type AiErrorKind = 'upgrade' | 'off_topic' | 'unavailable' | 'rate_limited' | 'not_found' | 'other';

export interface AiErrorInfo {
  kind: AiErrorKind;
  /** Lower-case backend code (`allowance_exhausted`, `plan_required`, …). */
  code: string;
  title: string;
  message: string;
  /** Upgrade prompts link here (the website path; the app uses its own `/subscription` screen). */
  upgradePath?: string;
  retryable: boolean;
}

const isErr = (e: unknown): e is ApiError => typeof e === 'object' && e !== null && 'code' in e && 'message' in e;

export function classifyAiError(e: unknown): AiErrorInfo {
  const status = isErr(e) ? Number((e as ApiError).status) || 0 : 0;
  const code = isErr(e) ? String(e.code).toLowerCase() : 'error';
  const serverMsg = isErr(e) && e.message ? e.message : e instanceof Error ? e.message : '';
  if (status === 402 || code === 'allowance_exhausted' || code === 'plan_required') {
    const exhausted = code === 'allowance_exhausted';
    return {
      kind: 'upgrade',
      code: exhausted ? 'allowance_exhausted' : 'plan_required',
      title: exhausted ? 'You have used this month’s allowance' : 'Part of a paid plan',
      message: serverMsg || (exhausted ? 'Upgrade or add a top-up pack to keep going.' : 'Upgrade your plan to unlock this feature.'),
      upgradePath: '/subscription',
      retryable: false,
    };
  }
  if (code === 'off_topic') {
    return {
      kind: 'off_topic', code, title: 'Let’s stick to exam prep',
      message: serverMsg || 'Mitra only helps with exam preparation. Try a question from your syllabus.', retryable: false,
    };
  }
  if (status === 503 || code === 'ai_unavailable') {
    return {
      kind: 'unavailable', code: 'ai_unavailable', title: 'The AI tutor is busy',
      message: serverMsg || 'Please try again in a minute. Nothing was used from your allowance.', retryable: true,
    };
  }
  if (status === 429 || code === 'rate_limited' || code === 'too_many_requests') {
    return { kind: 'rate_limited', code, title: 'Slow down a little', message: serverMsg || 'Too many requests. Wait a minute and try again.', retryable: true };
  }
  if (status === 404) return { kind: 'not_found', code, title: 'Not found', message: serverMsg || 'This item is no longer available.', retryable: false };
  return { kind: 'other', code, title: 'Something went wrong', message: serverMsg || 'Something went wrong. Please try again.', retryable: true };
}

/** Builds an ApiError (used by the mock AI client so screens see the same errors as with the backend). */
export const aiError = (status: number, code: string, message: string): ApiError => ({ status, code: code.toUpperCase(), message });
