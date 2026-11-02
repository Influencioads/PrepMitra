import type { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store';

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
