import type { ApiError } from '@prepmitra/shared';
import { env } from '@/utils/env';

export const USE_MOCK = env.useMockApi;

/** Simulated network latency for mock services. */
export const delay = (ms = 450) => new Promise<void>((resolve) => setTimeout(resolve, ms));

export function mockError(status: number, code: string, message: string): ApiError {
  return { status, code, message };
}

export const isApiError = (e: unknown): e is ApiError =>
  typeof e === 'object' && e !== null && 'message' in e && 'code' in e;

export const errorMessage = (e: unknown, fallback = 'Something went wrong. Please try again.') =>
  isApiError(e) ? e.message : e instanceof Error ? e.message : fallback;
