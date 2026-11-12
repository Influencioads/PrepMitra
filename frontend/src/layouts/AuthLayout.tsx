import { Outlet } from 'react-router-dom';
import { Logo } from '@/components/ui';
import { StudyDeskArt } from '@/components/marketing/StudyDeskArt';
import { useT } from '@/i18n';
import { LanguageSwitcher } from '@/i18n/LanguageSwitcher';
import { layoutMessages } from '@/i18n/messages/layout';
import { PageTransition } from '@/components/motion';

/** 3×3 saffron dot grid (one dot missing), decorative. */
function DotGrid({ className }: { className?: string }) {
  return (
    <div className={className} aria-hidden>
      <div className="grid grid-cols-3 gap-4 sm:gap-6">
        {Array.from({ length: 8 }, (_, i) => (
          <span key={i} className="h-7 w-7 rounded-full bg-accent sm:h-11 sm:w-11" />
        ))}
      </div>
    </div>
  );
}

/**
 * Auth screens: split page background (cream | soft green), saffron dots, and one card with a
 * thick green border across the split — illustration on the left, the form on a dark green
 * panel on the right. Pages inside use the `auth-dark` colour scope (see styles/index.css).
 */
export function AuthLayout() {
  const t = useT(layoutMessages);
  return (
    <div className="relative min-h-screen overflow-hidden bg-background">
      <div className="absolute inset-y-0 right-0 w-1/2 bg-[#a9cdbd]" aria-hidden />
      <DotGrid className="absolute left-10 top-10 hidden opacity-90 lg:block" />

      <div className="absolute right-3 top-3 z-10 sm:right-8 sm:top-8">
        <LanguageSwitcher />
      </div>

      <div className="relative flex min-h-screen flex-col items-stretch px-3 pt-14 sm:items-center sm:justify-center sm:px-8 sm:py-20 lg:py-16">
        <div className="grid w-full max-w-[1000px] flex-1 grid-rows-[auto_1fr] overflow-hidden rounded-t-[32px] border-[6px] border-b-0 sm:flex-none sm:grid-rows-none sm:rounded-[32px] sm:border-b-[6px] lg:grid-cols-2 border-secondary-hover bg-secondary-hover shadow-[0_40px_80px_-40px_rgb(16_36_28/0.55)]">
          {/* Illustration side */}
          <section className="flex flex-col bg-background px-6 pb-4 pt-6 sm:px-10 sm:pt-8 lg:pb-10">
            <Logo />
            <div className="flex flex-1 items-center justify-center py-4 lg:py-8">
              <StudyDeskArt className="h-36 w-auto sm:h-48 lg:h-auto lg:w-full lg:max-w-[440px]" />
            </div>
            <p className="hidden text-center font-display text-xl font-bold leading-snug text-secondary-hover lg:block">
              {t('authHeadline')} <span className="text-primary">{t('authHeadlineAccent')}</span>
            </p>
            <p className="mx-auto mt-2 hidden max-w-sm text-center text-sm text-muted lg:block">{t('authSub')}</p>
          </section>

          {/* Form side */}
          <main id="main" className="auth-dark bg-secondary-hover px-6 py-9 sm:px-12 sm:py-12 lg:px-14 lg:py-14">
            <div className="mx-auto w-full max-w-[360px]">
              <PageTransition><Outlet /></PageTransition>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
