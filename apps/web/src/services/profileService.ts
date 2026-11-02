import type { ResumeInfo, User, UserProfile, UserSettings } from '@prepmitra/shared';
import { API_ENDPOINTS, validateResumeFile } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';

export interface MeResponse {
  user: User;
  profile: UserProfile;
  settings: UserSettings;
}

export const profileService = {
  /** GET /v1/me */
  async getMe(): Promise<MeResponse | null> {
    if (USE_MOCK) return null;
    return (await http.get<MeResponse>(API_ENDPOINTS.me)).data;
  },

  /** PATCH /v1/me */
  async updateMe(patch: Partial<MeResponse>): Promise<Partial<MeResponse>> {
    if (!USE_MOCK) return (await http.patch<MeResponse>(API_ENDPOINTS.me, patch)).data;
    await delay(500);
    return patch;
  },

  /** POST /v1/uploads/resume — PDF/DOCX ≤ 5 MB; the server extracts text and strips phone numbers/emails before AI use. */
  async uploadResume(file: File): Promise<ResumeInfo> {
    const check = validateResumeFile(file);
    if (!check.ok) throw mockError(422, 'RESUME_INVALID', check.error);
    if (!USE_MOCK) {
      const form = new FormData();
      form.append('resume', file);
      return (await http.post<ResumeInfo>(API_ENDPOINTS.uploadResume, form, { headers: { 'Content-Type': 'multipart/form-data' } })).data;
    }
    await delay(900);
    return { fileName: file.name, sizeKb: Math.max(1, Math.round(file.size / 1024)), mimeType: file.type, uploadedAt: new Date().toISOString() };
  },

  /** POST /v1/me/consents */
  async recordConsent(consentType: string, granted: boolean): Promise<void> {
    if (!USE_MOCK) {
      await http.post(API_ENDPOINTS.consents, { consentType, granted });
      return;
    }
    await delay(250);
  },

  /** DELETE /v1/me — backend deletes personal data within 30 days (DPDP). */
  async deleteAccount(): Promise<void> {
    if (!USE_MOCK) {
      await http.delete(API_ENDPOINTS.me);
      return;
    }
    await delay(800);
  },
};
