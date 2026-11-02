import { useEffect, useState } from 'react';
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { EXAM_CATEGORIES, SUPPORT_EMAIL } from '@prepmitra/shared';
import { ButtonLink, Logo } from '@/components/ui';
import { ScrollToTop } from '@/components/layout/ScrollToTop';
import { InstallAppButton } from '@/components/pwa/InstallAppButton';
import { UserMenu } from '@/components/layout/UserMenu';
import { useAuthStore } from '@/store';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { LanguageSwitcher } from '@/i18n/LanguageSwitcher';
import { layoutMessages } from '@/i18n/messages/layout';
import { catalogMessages, categoryText } from '@/i18n/messages/catalog';

const NAV = [
  { to: '/exams', key: 'navExams' },
  { to: '/interviews', key: 'navInterviews' },
  { to: '/#features', key: 'navFeatures' },
  { to: '/pricing', key: 'navPricing' },
] as const;

export function PublicHeader() {
  const [open, setOpen] = useState(false);
  const user = useAuthStore((s) => s.session?.user);
  const location = useLocation();
  const t = useT(layoutMessages);
  useEffect(() => setOpen(false), [location.pathname, location.hash]);

  return (
    <header className="sticky top-0 z-30 border-b border-line/80 bg-background/85 backdrop-blur">
      <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-3 focus:z-50 focus:rounded-md focus:bg-card focus:px-3 focus:py-2 focus:shadow">
        {t('skipToContent')}
      </a>
      <div className="container-page flex h-16 items-center justify-between gap-4">
        <Logo />
        <nav aria-label={t('mainNav')} className="hidden items-center gap-1 md:flex">
          {NAV.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              className={({ isActive }) =>
                cn('rounded-md px-3 py-2 text-sm font-medium transition-colors hover:text-primary', isActive && !n.to.includes('#') ? 'text-primary' : 'text-ink/80')
              }
            >
              {t(n.key)}
            </NavLink>
          ))}
        </nav>
        <div className="hidden items-center gap-2 md:flex">
          <LanguageSwitcher />
          {user ? (
            <>
              <ButtonLink to={user.role === 'admin' ? '/admin/dashboard' : '/dashboard'} variant="secondary" size="sm">
                {user.role === 'admin' ? t('adminConsole') : t('goToDashboard')}
              </ButtonLink>
              <UserMenu />
            </>
          ) : (
            <>
              <ButtonLink to="/login" variant="ghost" size="sm">{t('logIn')}</ButtonLink>
              <ButtonLink to="/signup" size="sm">{t('startFreeMock')}</ButtonLink>
            </>
          )}
        </div>
        <div className="flex items-center gap-2 md:hidden">
        <LanguageSwitcher />
        <button
          type="button"
          className="rounded-md p-2 text-ink hover:bg-stone-100"
          aria-label={open ? t('closeMenu') : t('openMenu')}
          aria-expanded={open}
          aria-controls="mobile-nav"
          onClick={() => setOpen((o) => !o)}
        >
          {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
        </div>
      </div>
      {open && (
        <nav id="mobile-nav" aria-label={t('mobileNav')} className="border-t border-line bg-card md:hidden">
          <div className="container-page flex flex-col gap-1 py-3">
            {NAV.map((n) => (
              <Link key={n.to} to={n.to} className="rounded-md px-3 py-2.5 text-base font-medium text-ink hover:bg-stone-50">
                {t(n.key)}
              </Link>
            ))}
            <div className="mt-2 grid grid-cols-2 gap-2">
              {user ? (
                <ButtonLink to={user.role === 'admin' ? '/admin/dashboard' : '/dashboard'} className="col-span-2">
                  {user.role === 'admin' ? t('adminConsole') : t('goToDashboard')}
                </ButtonLink>
              ) : (
                <>
                  <ButtonLink to="/login" variant="outline">{t('logIn')}</ButtonLink>
                  <ButtonLink to="/signup">{t('startFree')}</ButtonLink>
                </>
              )}
            </div>
          </div>
        </nav>
      )}
    </header>
  );
}

export function PublicFooter() {
  const t = useT(layoutMessages);
  const tc = useT(catalogMessages);
  return (
    <footer className="border-t border-line bg-card">
      <div className="container-page grid gap-10 py-12 md:grid-cols-[1.4fr_1fr_1fr_1fr]">
        <div>
          <Logo />
          <p className="mt-3 max-w-xs text-sm text-muted">{t('footerTagline', { tagline: t('authTagline') })}</p>
          <p className="mt-4 text-sm text-muted">
            {t('footerQuestions')} <a className="font-medium text-primary hover:underline" href={`mailto:${SUPPORT_EMAIL}`}>{SUPPORT_EMAIL}</a>
          </p>
        </div>
        <div>
          <h2 className="text-sm font-semibold">{t('footerExams')}</h2>
          <ul className="mt-3 space-y-2 text-sm text-muted">
            {EXAM_CATEGORIES.map((c) => (
              <li key={c.id}><Link className="hover:text-primary" to={`/exams?category=${c.id}`}>{categoryText(tc, c.id).label}</Link></li>
            ))}
          </ul>
        </div>
        <div>
          <h2 className="text-sm font-semibold">{t('footerProduct')}</h2>
          <ul className="mt-3 space-y-2 text-sm text-muted">
            <li><Link className="hover:text-primary" to="/interviews">{t('mockInterviews')}</Link></li>
            <li><Link className="hover:text-primary" to="/pricing">{t('pricing')}</Link></li>
            <li><Link className="hover:text-primary" to="/#how-it-works">{t('howItWorks')}</Link></li>
            <li><Link className="hover:text-primary" to="/#faq">{t('faqs')}</Link></li>
          </ul>
        </div>
        <div>
          <h2 className="text-sm font-semibold">{t('footerCompany')}</h2>
          <ul className="mt-3 space-y-2 text-sm text-muted">
            <li><Link className="hover:text-primary" to="/privacy">{t('privacy')}</Link></li>
            <li><Link className="hover:text-primary" to="/terms">{t('terms')}</Link></li>
            <li><Link className="hover:text-primary" to="/refund-policy">{t('refund')}</Link></li>
            <li><Link className="hover:text-primary" to="/contact">{t('contact')}</Link></li>
          </ul>
        </div>
      </div>
      <div className="border-t border-line">
        <div className="container-page flex flex-col gap-2 py-5 text-xs text-muted md:flex-row md:items-center md:justify-between">
          <div className="flex flex-wrap items-center gap-3">
            <p>{t('copyright', { year: new Date().getFullYear() })}</p>
            <InstallAppButton />
          </div>
          <p className="max-w-2xl md:text-right">{t('affiliation')}</p>
        </div>
      </div>
    </footer>
  );
}

export function PublicLayout() {
  return (
    <div className="flex min-h-screen flex-col">
      <ScrollToTop />
      <PublicHeader />
      <main id="main" className="flex-1">
        <Outlet />
      </main>
      <PublicFooter />
    </div>
  );
}
