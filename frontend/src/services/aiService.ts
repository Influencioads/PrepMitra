import { aiArtifactPdfPath, createAiApi, createMockAiApi, type AiApi } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, mockError } from './mock';

/**
 * Student AI features (`/v1/ai/*`). The client itself lives in `@prepmitra/shared` so the app uses the same calls;
 * this file only plugs in the website's authenticated axios instance, or the shared demo data in mock mode.
 */
const live = () =>
  createAiApi({
    get: async (path, params) => (await http.get(path, { params, timeout: 90_000 })).data,
    // AI work can take a while (two models check every new solution).
    post: async (path, body) => (await http.post(path, body ?? {}, { timeout: 120_000 })).data,
  });

export const aiService: AiApi = USE_MOCK ? createMockAiApi(import.meta.env.MODE === 'test' ? 0 : 500) : live();

/** Opens an artifact (notes, deck, deep dive, mistake summary) as a PDF in a new tab. */
export async function openArtifactPdf(id: string): Promise<void> {
  if (USE_MOCK) throw mockError(501, 'NEEDS_BACKEND', 'PDF downloads need the live backend. They are not available in demo mode.');
  const { data } = await http.get<Blob>(aiArtifactPdfPath(id), { responseType: 'blob', timeout: 60_000 });
  const url = URL.createObjectURL(data);
  window.open(url, '_blank', 'noopener');
  setTimeout(() => URL.revokeObjectURL(url), 60_000);
}

/** Reads an image file as a data URL for `POST /ai/doubts/photo`, shrinking big phone photos first. */
export async function imageFileToDataUrl(file: File, maxSide = 1600): Promise<string> {
  const raw = await new Promise<string>((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => resolve(String(r.result));
    r.onerror = () => reject(r.error);
    r.readAsDataURL(file);
  });
  if (typeof document === 'undefined' || file.size < 900_000) return raw;
  try {
    const img = await new Promise<HTMLImageElement>((resolve, reject) => {
      const i = new Image();
      i.onload = () => resolve(i);
      i.onerror = reject;
      i.src = raw;
    });
    const scale = Math.min(1, maxSide / Math.max(img.width, img.height));
    const c = document.createElement('canvas');
    c.width = Math.round(img.width * scale);
    c.height = Math.round(img.height * scale);
    c.getContext('2d')?.drawImage(img, 0, 0, c.width, c.height);
    return c.toDataURL('image/jpeg', 0.85);
  } catch {
    return raw;
  }
}
