import axios, { AxiosError } from 'axios';
import type { ApiError } from '@prepmitra/shared';
import { STORAGE_KEYS } from '@prepmitra/shared';
import { env } from '@/utils/env';

/**
 * Axios client for the `/v1` backend. Mock services are used while
 * `VITE_USE_MOCK_API` is not "false". No secrets are stored in the frontend.
 * Every request carries the Firebase ID token (Authorization: Bearer …); when
 * Firebase is enabled a fresh token is fetched from the SDK so it never expires mid-session.
 */
export const http = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: 15_000,
  headers: { 'Content-Type': 'application/json' },
});

type TokenProvider = () => Promise<string | null>;
let tokenProvider: TokenProvider | null = null;
/** Registered by the Firebase adapter so requests always use a fresh ID token. */
export const setTokenProvider = (fn: TokenProvider | null) => {
  tokenProvider = fn;
};

http.interceptors.request.use(async (config) => {
  if (tokenProvider) {
    const fresh = await tokenProvider().catch(() => null);
    if (fresh) {
      config.headers.Authorization = `Bearer ${fresh}`;
      return config;
    }
  }
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.auth);
    const token = raw ? JSON.parse(raw)?.state?.session?.tokens?.accessToken : undefined;
    if (token) config.headers.Authorization = `Bearer ${token}`;
  } catch {
    /* storage unavailable — continue unauthenticated */
  }
  return config;
});

http.interceptors.response.use(
  (r) => r,
  (error: AxiosError<{ code?: string; message?: string }>) => {
    const apiError: ApiError = {
      status: error.response?.status ?? 0,
      code: error.response?.data?.code ?? (error.code || 'NETWORK_ERROR'),
      message: error.response?.data?.message ?? 'Unable to reach the server. Check your connection and try again.',
    };
    return Promise.reject(apiError);
  },
);
