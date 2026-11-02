import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { UserProfile, UserSettings } from '@prepmitra/shared';
import { DEFAULT_SETTINGS, EMPTY_PROFILE, STORAGE_KEYS } from '@prepmitra/shared';
import { demoStorage } from './storage';

export interface OnboardingDraft {
  step: number;
  data: Record<string, unknown>;
}

interface ProfileState {
  ownerId: string | null;
  profile: UserProfile;
  settings: UserSettings;
  draft: OnboardingDraft | null;
  reset: (ownerId: string, profile: UserProfile, settings?: UserSettings) => void;
  updateProfile: (patch: Partial<UserProfile>) => void;
  updateSettings: (patch: Partial<UserSettings>) => void;
  saveDraft: (draft: OnboardingDraft | null) => void;
}

export const useProfileStore = create<ProfileState>()(
  persist(
    (set) => ({
      ownerId: null,
      profile: EMPTY_PROFILE,
      settings: DEFAULT_SETTINGS,
      draft: null,
      reset: (ownerId, profile, settings = DEFAULT_SETTINGS) => set({ ownerId, profile, settings, draft: null }),
      updateProfile: (patch) => set((s) => ({ profile: { ...s.profile, ...patch } })),
      updateSettings: (patch) => set((s) => ({ settings: { ...s.settings, ...patch } })),
      saveDraft: (draft) => set({ draft }),
    }),
    { name: STORAGE_KEYS.profile, storage: demoStorage },
  ),
);
