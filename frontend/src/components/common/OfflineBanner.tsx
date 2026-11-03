import { useEffect, useState } from 'react';
import { WifiOff } from 'lucide-react';
import { useT } from '@/i18n';
import { layoutMessages } from '@/i18n/messages/layout';

export function useOnline() {
  const [online, setOnline] = useState(() => (typeof navigator === 'undefined' ? true : navigator.onLine));
  useEffect(() => {
    const on = () => setOnline(true);
    const off = () => setOnline(false);
    window.addEventListener('online', on);
    window.addEventListener('offline', off);
    return () => {
      window.removeEventListener('online', on);
      window.removeEventListener('offline', off);
    };
  }, []);
  return online;
}

/** Global banner shown while the device is offline (15-day plan, Day 12). */
export function OfflineBanner() {
  const online = useOnline();
  const t = useT(layoutMessages);
  if (online) return null;
  return (
    <div role="status" className="fixed inset-x-0 top-0 z-[60] flex items-center justify-center gap-2 bg-ink px-4 py-2 text-sm font-medium text-white">
      <WifiOff className="h-4 w-4" aria-hidden />
      {t('offline')}
    </div>
  );
}
