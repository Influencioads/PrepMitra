import { Outlet } from 'react-router-dom';
import { CircleCheck } from 'lucide-react';
import { Logo } from '@/components/ui';
import { OmrSheet } from '@/components/marketing/Illustrations';
import { useT } from '@/i18n';
import { LanguageSwitcher } from '@/i18n/LanguageSwitcher';
import { layoutMessages } from '@/i18n/messages/layout';

const POINTS = ['authPoint1', 'authPoint2', 'authPoint3', 'authPoint4'] as const;

export function AuthLayout() {
  const t = useT(layoutMessages);
  return (
    <div className="grid min-h-screen lg:grid-cols-[1fr_1.1fr]">
      <aside className="relative hidden flex-col justify-between overflow-hidden bg-secondary p-10 text-white lg:flex">
        <div className="absolute -right-24 -top-24 h-80 w-80 rounded-full bg-accent/25 blur-3xl" aria-hidden />
        <OmrSheet className="pointer-events-none absolute -bottom-10 -right-10 w-72 rotate-[8deg] opacity-95" />
        <Logo light className="relative" />
        <div className="relative max-w-md">
          <h2 className="text-3xl font-bold leading-tight text-white">{t('authTagline')}</h2>
          <ul className="mt-8 space-y-4">
            {POINTS.map((p) => (
              <li key={p} className="flex gap-3 text-white/90">
                <CircleCheck className="mt-0.5 h-5 w-5 shrink-0 text-accent" aria-hidden />
                {t(p)}
              </li>
            ))}
          </ul>
        </div>
        <p className="relative max-w-xs text-sm text-white/70">{t('authFooter')}</p>
      </aside>
      <main id="main" className="flex flex-col px-4 py-6 sm:px-8">
        <div className="flex items-center justify-between gap-3">
          <div className="lg:invisible">
            <Logo />
          </div>
          <LanguageSwitcher />
        </div>
        <div className="mx-auto flex w-full max-w-md flex-1 flex-col justify-center py-10">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
