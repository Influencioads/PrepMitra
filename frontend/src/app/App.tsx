import { useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { router } from './router';
import { AppErrorBoundary, initErrorReporting } from '@/lib/observability';
import { OfflineBanner } from '@/components/common/OfflineBanner';
import { useSyncHtmlLang } from '@/i18n';
import { USE_MOCK } from '@/services/mock';
import { syncFromBackend, useAuthStore } from '@/store';

export function App() {
  useSyncHtmlLang();
  useEffect(() => {
    void initErrorReporting();
    // Real API: refresh the signed-in user's data (credits, reports, notifications) on every start.
    if (!USE_MOCK && useAuthStore.getState().session) void syncFromBackend();
  }, []);

  return (
    <AppErrorBoundary>
      <OfflineBanner />
      <RouterProvider router={router} />
      <Toaster
        position="top-center"
        toastOptions={{
          duration: 3500,
          style: { borderRadius: '10px', background: '#1C2321', color: '#fff', fontSize: '14px' },
          success: { iconTheme: { primary: '#15803D', secondary: '#fff' } },
          error: { iconTheme: { primary: '#DC2626', secondary: '#fff' } },
        }}
      />
    </AppErrorBoundary>
  );
}
