import type { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { isProfileReady } from '@prepmitra/shared';
import { useAuthStore, useProfileStore } from '@/store';

/**
 * UI-only route guards. They decide what the interface shows; they are NOT a
 * security boundary. The backend must authorize every request (JWT + RBAC).
 */
export function RequireAuth({ children, allowIncompleteOnboarding = false }: { children: ReactNode; allowIncompleteOnboarding?: boolean }) {
  const user = useAuthStore((s) => s.session?.user);
  const location = useLocation();
  if (!user) return <Navigate to={`/login?redirect=${encodeURIComponent(location.pathname + location.search)}`} replace />;
  if (!allowIncompleteOnboarding && !user.onboardingComplete && user.role !== 'admin') return <Navigate to="/onboarding" replace />;
  return <>{children}</>;
}

export function RequireAdmin({ children }: { children: ReactNode }) {
  const user = useAuthStore((s) => s.session?.user);
  const location = useLocation();
  if (!user) return <Navigate to={`/login?redirect=${encodeURIComponent(location.pathname)}`} replace />;
  if (user.role !== 'admin') return <Navigate to="/dashboard" replace />;
  return <>{children}</>;
}

export function GuestOnly({ children }: { children: ReactNode }) {
  const user = useAuthStore((s) => s.session?.user);
  if (user) return <Navigate to={user.role === 'admin' ? '/admin/dashboard' : user.onboardingComplete ? '/dashboard' : '/onboarding'} replace />;
  return <>{children}</>;
}

/**
 * Exams and interviews unlock only when the profile has a name, a preferred language and at least
 * one target exam or role (15-day plan, Day 2). Not finished onboarding → /onboarding; finished but a
 * required field was later cleared → /profile with a note. UI only; the backend checks this too.
 */
export function RequireReadyProfile({ children }: { children: ReactNode }) {
  const user = useAuthStore((s) => s.session?.user);
  const profile = useProfileStore((s) => s.profile);
  const location = useLocation();
  if (!user || user.role === 'admin') return <>{children}</>;
  if (isProfileReady(user, profile)) return <>{children}</>;
  if (!user.onboardingComplete) return <Navigate to="/onboarding" replace />;
  return <Navigate to={`/profile?complete=1&redirect=${encodeURIComponent(location.pathname + location.search)}`} replace />;
}
