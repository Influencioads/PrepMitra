import { Outlet } from 'react-router-dom';
import { useAuthStore } from '@/store';
import { AppLayout } from './AppLayout';
import { PublicFooter, PublicHeader } from './PublicLayout';
import { ScrollToTop } from '@/components/layout/ScrollToTop';

/** Catalog pages: app shell for signed-in learners, marketing shell for visitors. */
export function AdaptiveLayout() {
  const user = useAuthStore((s) => s.session?.user);
  if (user && user.role !== 'admin' && user.onboardingComplete) return <AppLayout />;
  return (
    <div className="flex min-h-screen flex-col">
      <ScrollToTop />
      <PublicHeader />
      <main id="main" className="container-page flex-1 py-8 lg:py-10">
        <Outlet />
      </main>
      <PublicFooter />
    </div>
  );
}
