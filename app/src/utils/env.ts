/**
 * Runtime configuration. Only non-secret values belong here — every
 * EXPO_PUBLIC_* variable is inlined into the JavaScript bundle at build time.
 */
export const env = {
  apiBaseUrl: process.env.EXPO_PUBLIC_API_BASE_URL ?? 'http://localhost:8080',
  /** Mock services are used unless EXPO_PUBLIC_USE_MOCK_API is exactly "false". */
  useMockApi: process.env.EXPO_PUBLIC_USE_MOCK_API !== 'false',
};
