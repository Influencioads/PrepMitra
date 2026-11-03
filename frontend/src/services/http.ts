import axios, { AxiosError } from 'axios';
import type { InternalAxiosRequestConfig } from 'axios';
import type { ApiError } from '@prepmitra/shared';
import { STORAGE_KEYS, toApiErrorBody } from '@prepmitra/shared';
import { env } from '@/utils/env';

/**
 * Axios client for the `/v1` backend. Mock services are used while
 * `VITE_USE_MOCK_API` is not "false". No secrets are stored in the frontend.
 * Requests carry the backend access token (phone OTP login) or, with Firebase on,
 * a fresh Firebase ID token. An expired access token is refreshed once with the
 * refresh token (POST /v1/auth/refresh) and the request is retried.
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

interface StoredTokens {
  accessToken?: string;
  refreshToken?: string;
  expiresAt?: string;
}

/** Tokens live in the persisted auth store (zustand `pm.auth`); read/written here to avoid an import cycle. */
const readTokens = (): StoredTokens | undefined => {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.auth);
    return raw ? JSON.parse(raw)?.state?.session?.tokens : undefined;
  } catch {
    return undefined;
  }
};

let onTokensRefreshed: ((t: Required<StoredTokens>) => void) | null = null;
let onSessionExpired: (() => void) | null = null;
/** Wired by the auth store: save rotated tokens, or sign out when the refresh token is no longer valid. */
export const setAuthHandlers = (h: { refreshed: (t: Required<StoredTokens>) => void; expired: () => void }) => {
  onTokensRefreshed = h.refreshed;
  onSessionExpired = h.expired;
};

http.interceptors.request.use(async (config) => {
  if (config.headers.Authorization) return config; // explicit token (e.g. Firebase exchange)
  if (tokenProvider) {
    const fresh = await tokenProvider().catch(() => null);
    if (fresh) {
      config.headers.Authorization = `Bearer ${fresh}`;
      return config;
    }
  }
  const token = readTokens()?.accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

let refreshing: Promise<string | null> | null = null;
async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = readTokens()?.refreshToken;
  if (!refreshToken) return null;
  refreshing ??= axios
    .post(`${env.apiBaseUrl}/v1/auth/refresh`, { refresh_token: refreshToken }, { timeout: 15_000 })
    .then(({ data }) => {
      const tokens = {
        accessToken: data.access_token as string,
        refreshToken: data.refresh_token as string,
        expiresAt: new Date(Date.now() + data.expires_in * 1000).toISOString(),
      };
      onTokensRefreshed?.(tokens);
      return tokens.accessToken;
    })
    .catch(() => null)
    .finally(() => {
      refreshing = null;
    });
  return refreshing;
}

http.interceptors.response.use(
  (r) => r,
  async (error: AxiosError) => {
    const config = error.config as (InternalAxiosRequestConfig & { _retried?: boolean }) | undefined;
    const isAuthCall = config?.url?.startsWith('/v1/auth/');
    if (error.response?.status === 401 && config && !config._retried && !isAuthCall && !tokenProvider) {
      config._retried = true;
      const token = await refreshAccessToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
        return http(config);
      }
      onSessionExpired?.();
    }
    const body = toApiErrorBody(error.response?.data);
    const apiError: ApiError = {
      status: error.response?.status ?? 0,
      code: body.code ?? (error.code || 'NETWORK_ERROR'),
      message: body.message ?? (error.response ? 'Something went wrong. Please try again.' : 'Unable to reach the server. Check your connection and try again.'),
    };
    return Promise.reject(apiError);
  },
);
