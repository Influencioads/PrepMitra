import type { ResumeInfo, User, UserProfile, UserSettings } from '@prepmitra/shared';
import { API_ENDPOINTS, validateResumeFile } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';

export interface MeResponse {
  user: User;
  profile: UserProfile;
  settings: UserSettings;
}

/** A file picked with expo-document-picker. */
export interface PickedFile {
  uri: string;
  name: string;
  size: number;
  mimeType?: string;
}

export const profileService = {
  /** PATCH /v1/me */
  async updateMe(patch: Partial<MeResponse>): Promise<Partial<MeResponse>> {
    if (!USE_MOCK) return (await http.patch<MeResponse>(API_ENDPOINTS.me, patch)).data;
    await delay(500);
    return patch;
  },

  /** Simulated upload; production stores the file in object storage and returns a reference. */
  async uploadResume(file: PickedFile): Promise<ResumeInfo> {
    const check = validateResumeFile({ name: file.name, size: file.size, type: file.mimeType });
    if (!check.ok) throw mockError(422, 'RESUME_INVALID', check.error);
    if (!USE_MOCK) {
      const form = new FormData();
      // React Native's FormData accepts { uri, name, type } file descriptors.
      form.append('resume', { uri: file.uri, name: file.name, type: file.mimeType ?? 'application/pdf' } as unknown as Blob);
      return (
        await http.post<ResumeInfo>(API_ENDPOINTS.uploadResume, form, { headers: { 'Content-Type': 'multipart/form-data' } })
      ).data;
    }
    await delay(900);
    return {
      fileName: file.name,
      sizeKb: Math.max(1, Math.round(file.size / 1024)),
      mimeType: file.mimeType ?? 'application/pdf',
      uploadedAt: new Date().toISOString(),
    };
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
