import { useEffect, useState } from 'react';
import { Download, Share } from 'lucide-react';
import { Button } from '@/components/ui';
import { useT } from '@/i18n';
import { layoutMessages } from '@/i18n/messages/layout';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

const isStandalone = () =>
  typeof window !== 'undefined' &&
  (window.matchMedia?.('(display-mode: standalone)').matches || (navigator as Navigator & { standalone?: boolean }).standalone === true);

const isIosSafari = () => {
  if (typeof navigator === 'undefined') return false;
  const ua = navigator.userAgent;
  return /iPhone|iPad|iPod/.test(ua) && /Safari/.test(ua) && !/CriOS|FxiOS|EdgiOS/.test(ua);
};

/** "Install app" for the PWA: uses the browser prompt where available, a Share tip on iOS Safari. */
export function InstallAppButton({ className }: { className?: string }) {
  const [deferred, setDeferred] = useState<BeforeInstallPromptEvent | null>(null);
  const [installed, setInstalled] = useState(isStandalone);
  const [showIosTip, setShowIosTip] = useState(false);
  const t = useT(layoutMessages);

  useEffect(() => {
    const onPrompt = (e: Event) => {
      e.preventDefault();
      setDeferred(e as BeforeInstallPromptEvent);
    };
    const onInstalled = () => {
      setInstalled(true);
      setDeferred(null);
    };
    window.addEventListener('beforeinstallprompt', onPrompt);
    window.addEventListener('appinstalled', onInstalled);
    return () => {
      window.removeEventListener('beforeinstallprompt', onPrompt);
      window.removeEventListener('appinstalled', onInstalled);
    };
  }, []);

  if (installed) return null;

  if (deferred) {
    return (
      <Button
        size="sm"
        variant="outline"
        className={className}
        leftIcon={<Download className="h-4 w-4" />}
        onClick={async () => {
          await deferred.prompt();
          const choice = await deferred.userChoice;
          if (choice.outcome === 'accepted') setInstalled(true);
          setDeferred(null);
        }}
      >
        {t('installApp')}
      </Button>
    );
  }

  if (isIosSafari()) {
    return (
      <span className={className}>
        <Button size="sm" variant="outline" leftIcon={<Download className="h-4 w-4" />} onClick={() => setShowIosTip((v) => !v)} aria-expanded={showIosTip}>
          {t('installApp')}
        </Button>
        {showIosTip && (
          <span role="status" className="ml-2 inline-flex items-center gap-1 text-xs text-muted">
            {t('iosTipBefore')} <Share className="h-3.5 w-3.5" aria-label={t('share')} /> {t('iosTipAfter')}
          </span>
        )}
      </span>
    );
  }

  return null;
}
