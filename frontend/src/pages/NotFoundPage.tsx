import { ButtonLink } from '@/components/ui';
import { useT } from '@/i18n';
import { layoutMessages } from '@/i18n/messages/layout';

export function NotFoundPage() {
  const t = useT(layoutMessages);
  return (
    <div className="container-page flex flex-col items-center py-24 text-center">
      <p className="text-sm font-semibold text-primary">404</p>
      <h1 className="mt-2 text-3xl font-bold">{t('notFoundTitle')}</h1>
      <p className="mt-2 max-w-md text-muted">{t('notFoundBody')}</p>
      <div className="mt-6 flex gap-3">
        <ButtonLink to="/exams" variant="outline">{t('browseExams')}</ButtonLink>
        <ButtonLink to="/">{t('goHome')}</ButtonLink>
      </div>
    </div>
  );
}
