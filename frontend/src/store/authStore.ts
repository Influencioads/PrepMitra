import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { AuthSession, User } from '@prepmitra/shared';
import { STORAGE_KEYS } from '@prepmitra/shared';
import { demoStorage } from './storage';
import { setAuthHandlers } from '@/services/http';

export interface PendingOtp {
  phone: string;
  requestId: string;
  purpose: 'login' | 'signup' | 'recovery';
  signup?: { name: string; email?: string };
  demoCode?: string;
  redirectTo?: string;
}

interface AuthState {
  session: AuthSession | null;
  pending: PendingOtp | null;
  setPending: (p: PendingOtp | null) => void;
  signIn: (session: AuthSession) => void;
  updateUser: (patch: Partial<User>) => void;
  signOut: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      session: null,
      pending: null,
      setPending: (pending) => set({ pending }),
      signIn: (session) => set({ session, pending: null }),
      updateUser: (patch) =>
        set((s) => (s.session ? { session: { ...s.session, user: { ...s.session.user, ...patch } } } : s)),
      signOut: () => set({ session: null, pending: null }),
    }),
    { name: STORAGE_KEYS.auth, storage: demoStorage },
  ),
);

// Rotated tokens from the HTTP client are saved here; an expired refresh token signs the user out.
setAuthHandlers({
  refreshed: (tokens) =>
    useAuthStore.setState((s) => (s.session ? { session: { ...s.session, tokens } } : s)),
  expired: () => useAuthStore.getState().signOut(),
});

export const useCurrentUser = () => useAuthStore((s) => s.session?.user ?? null);
export const useIsAuthenticated = () => useAuthStore((s) => !!s.session);
