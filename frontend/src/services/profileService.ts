import type { ResumeInfo, User, UserProfile, UserSettings } from '@prepmitra/shared';
import { API_ENDPOINTS, CONSENT_KEYS, toMe, toMePatch, validateResumeFile } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';

export interface MeResponse {
  user: User;
  profile: UserProfile;
  settings: UserSettings;
}

/** PATCH /v1/me input: any subset of user, profile and settings fields. */
export interface MePatch {
  user?: Partial<User>;
  profile?: Partial<UserProfile>;
  settings?: Partial<UserSettings>;
}

/** POST /v1/me/consents takes the full set, so merge one change into the current consents. */
async function setConsent(key: string, granted: boolean): Promise<void> {
  const current = (await http.get(API_ENDPOINTS.me)).data.consents ?? {};
  await http.post(API_ENDPOINTS.consents, { data_processing: !!current.data_processing, recruiter_sharing: !!current.recruiter_sharing, marketing: !!current.marketing, [key]: granted });
}

export const profileService = {
  /** GET /v1/me */
  async getMe(): Promise<MeResponse | null> {
    if (USE_MOCK) return null;
    return toMe((await http.get(API_ENDPOINTS.me)).data);
  },

  /** PATCH /v1/me — settings other than recruiter sharing / offers are kept on this device. */
  async updateMe(patch: MePatch): Promise<MePatch> {
    if (!USE_MOCK) {
      const body = toMePatch(patch);
      const privacy = patch.settings?.privacy;
      if (privacy && 'shareWithRecruiters' in privacy) await setConsent('recruiter_sharing', privacy.shareWithRecruiters);
      const notifications = patch.settings?.notifications;
      if (notifications && 'offers' in notifications) await setConsent('marketing', notifications.offers);
      if (!Object.keys(body).length) return patch;
      const me = toMe((await http.patch(API_ENDPOINTS.me, body)).data);
      return { user: me.user, profile: { ...me.profile, ...(patch.profile?.resume ? { resume: patch.profile.resume } : {}) } };
    }
    await delay(500);
    return patch;
  },

  /** POST /v1/uploads/resume — PDF/DOCX ≤ 5 MB; the server extracts text and strips phone numbers/emails before AI use. */
  async uploadResume(file: File): Promise<ResumeInfo> {
    const check = validateResumeFile(file);
    if (!check.ok) throw mockError(422, 'RESUME_INVALID', check.error);
    if (!USE_MOCK) {
      const form = new FormData();
      form.append('file', file);
      const { data } = await http.post(API_ENDPOINTS.uploadResume, form, { headers: { 'Content-Type': 'multipart/form-data' } });
      return { fileName: data.filename ?? file.name, sizeKb: Math.max(1, Math.round(file.size / 1024)), mimeType: file.type, uploadedAt: new Date().toISOString() };
    }
    await delay(900);
    return { fileName: file.name, sizeKb: Math.max(1, Math.round(file.size / 1024)), mimeType: file.type, uploadedAt: new Date().toISOString() };
  },

  /** POST /v1/me/consents — only consents the backend records; the rest are device settings. */
  async recordConsent(consentType: string, granted: boolean): Promise<void> {
    if (!USE_MOCK) {
      const key = CONSENT_KEYS[consentType];
      if (key) await setConsent(key, granted);
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
