import { isRouteErrorResponse, Link, useRouteError } from 'react-router-dom';
import { buttonClasses } from '@/components/ui';
import { useT } from '@/i18n';
import { layoutMessages } from '@/i18n/messages/layout';

export function RouteError() {
  const error = useRouteError();
  const t = useT(layoutMessages);
  const message = isRouteErrorResponse(error) ? `${error.status} — ${error.statusText}` : error instanceof Error ? error.message : t('errorEyebrow');
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background px-4 text-center">
      <p className="text-sm font-semibold text-danger">{t('errorEyebrow')}</p>
      <h1 className="mt-2 text-2xl font-bold">{t('errorTitle')}</h1>
      <p className="mt-2 max-w-md text-sm text-muted">{message}</p>
      <div className="mt-6 flex gap-3">
        <button type="button" className={buttonClasses('outline')} onClick={() => window.location.reload()}>{t('reload')}</button>
        <Link to="/" className={buttonClasses('primary')}>{t('goHome')}</Link>
      </div>
    </div>
  );
}
