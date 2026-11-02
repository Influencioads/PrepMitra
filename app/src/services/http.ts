import axios, { type AxiosError } from 'axios';
import type { ApiError } from '@prepmitra/shared';
import { useAuthStore } from '@/store/authStore';
import { env } from '@/utils/env';

/**
 * Axios client for the future `/v1` backend. Mock services are used while
 * `EXPO_PUBLIC_USE_MOCK_API` is not "false". No secrets live in the app; the
 * access token is the short-lived JWT issued by the backend.
 */
export const http = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: 15_000,
  headers: { 'Content-Type': 'application/json' },
});

http.interceptors.request.use((config) => {
  const token = useAuthStore.getState().session?.tokens.accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
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
