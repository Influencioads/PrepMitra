/**
 * lib/api — the single entry point for talking to the backend (folder layout from the 15-day plan).
 *
 * - `http`: the axios client (base URL from VITE_API_BASE_URL, Firebase ID token in the Authorization header).
 * - `API_ENDPOINTS`: every /v1 route from the API Plan sheet, shared with the mobile app.
 * - Services: one per area. Each one returns mock data while VITE_USE_MOCK_API=true and calls the
 *   real endpoint otherwise, so a screen switches to the real API without changing its code.
 *
 * Contract details: docs/API_CONTRACT.md. Mock responses: src/mocks/api/*.json.
 */
export { http, setTokenProvider } from '@/services/http';
export { API_ENDPOINTS } from '@prepmitra/shared';
export * from '@/services';
