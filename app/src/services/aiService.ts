import { createAiApi, createMockAiApi, type AiApi } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK } from './mock';

/**
 * Student AI features (`/v1/ai/*`). The client lives in `@prepmitra/shared` (same calls as the website); this
 * file plugs in the app's authenticated axios instance, or the shared demo data in mock mode.
 */
const live = () =>
  createAiApi({
    get: async (path, params) => (await http.get(path, { params, timeout: 90_000 })).data,
    // AI work can take a while (two models check every new solution).
    post: async (path, body) => (await http.post(path, body ?? {}, { timeout: 120_000 })).data,
  });

export const aiService: AiApi = USE_MOCK ? createMockAiApi(500) : live();

/** Reads a picked image (file:// or blob: uri) as a data URL for `POST /ai/doubts/photo`. */
export async function uriToDataUrl(uri: string): Promise<string> {
  const blob = await (await fetch(uri)).blob();
  return new Promise<string>((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => resolve(String(r.result));
    r.onerror = () => reject(new Error('Could not read the photo.'));
    r.readAsDataURL(blob);
  });
}
