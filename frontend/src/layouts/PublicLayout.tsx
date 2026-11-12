import { useEffect, useState } from 'react';
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom';
import { ArrowRight, ArrowUp, Menu, X } from 'lucide-react';
import { AnimatePresence, motion, useMotionValueEvent, useReducedMotion, useScroll } from 'framer-motion';
import { EXAM_CATEGORIES, SUPPORT_EMAIL } from '@prepmitra/shared';
import { ButtonLink, Logo } from '@/components/ui';
import { ScrollToTop } from '@/components/layout/ScrollToTop';
import { InstallAppButton } from '@/components/pwa/InstallAppButton';
import { UserMenu } from '@/components/layout/UserMenu';
import { useAuthStore } from '@/store';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { LanguageSwitcher } from '@/i18n/LanguageSwitcher';
import { interviewsEnabled, isCategoryOpen } from '@/config/launch';
import { layoutMessages } from '@/i18n/messages/layout';
import { catalogMessages, categoryText } from '@/i18n/messages/catalog';
import { PageTransition } from '@/components/motion';

const NAV = [
  { to: '/exams', key: 'navExams' },
  { to: '/interviews', key: 'navInterviews' },
  { to: '/#features', key: 'navFeatures' },
  { to: '/pricing', key: 'navPricing' },
] as const;

export function PublicHeader() {
  const [open, setOpen] = useState(false);
  const [hover, setHover] = useState<string | null>(null);
  const user = useAuthStore((s) => s.session?.user);
  const location = useLocation();
  const t = useT(layoutMessages);
  const { scrollY } = useScroll();
  const [scrolled, setScrolled] = useState(false);
  useMotionValueEvent(scrollY, 'change', (v) => setScrolled(v > 12));
  useEffect(() => setOpen(false), [location.pathname, location.hash]);
  const nav = NAV.filter((n) => n.to !== '/interviews' || interviewsEnabled());

  return (
    <header
      className={cn(
        'sticky top-0 z-30 border-b transition-[background-color,box-shadow,border-color] duration-300',
        scrolled || open ? 'border-line/80 bg-background/90 shadow-[0_6px_24px_-12px_rgba(28,35,33,0.25)] backdrop-blur-md' : 'border-transparent bg-background/60 backdrop-blur-sm',
      )}
    >
      <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-3 focus:z-50 focus:rounded-md focus:bg-card focus:px-3 focus:py-2 focus:shadow">
        {t('skipToContent')}
      </a>
      <div className={cn('container-page flex items-center justify-between gap-4 transition-[height] duration-300', scrolled ? 'h-14' : 'h-16')}>
        <motion.div whileHover={{ rotate: -2, scale: 1.03 }} transition={{ type: 'spring', stiffness: 400, damping: 15 }}>
          <Logo />
        </motion.div>
        <nav aria-label={t('mainNav')} className="hidden items-center gap-1 rounded-full border border-line/70 bg-card/60 p-1 md:flex" onMouseLeave={() => setHover(null)}>
          {nav.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              onMouseEnter={() => setHover(n.to)}
              onFocus={() => setHover(n.to)}
              className={({ isActive }) =>
                cn('relative rounded-full px-4 py-1.5 text-sm font-semibold transition-colors', isActive && !n.to.includes('#') ? 'text-primary' : 'text-ink/80 hover:text-ink')
              }
            >
              {hover === n.to && <motion.span layoutId="nav-pill" className="absolute inset-0 rounded-full bg-primary-soft" transition={{ type: 'spring', stiffness: 420, damping: 34 }} />}
              <span className="relative">{t(n.key)}</span>
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
              <ButtonLink to="/signup" size="sm" className="shadow-[0_3px_0_#8A2E07] transition-transform hover:-translate-y-0.5">{t('startFreeMock')}</ButtonLink>
            </>
          )}
        </div>
        <div className="flex items-center gap-2 md:hidden">
          <LanguageSwitcher />
          <button
            type="button"
            className="relative h-10 w-10 rounded-md text-ink hover:bg-stone-100"
            aria-label={open ? t('closeMenu') : t('openMenu')}
            aria-expanded={open}
            aria-controls="mobile-nav"
            onClick={() => setOpen((o) => !o)}
          >
            <AnimatePresence initial={false} mode="wait">
              <motion.span
                key={open ? 'x' : 'menu'}
                className="absolute inset-0 flex items-center justify-center"
                initial={{ rotate: -90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: 90, opacity: 0 }}
                transition={{ duration: 0.15 }}
              >
                {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </motion.span>
            </AnimatePresence>
          </button>
        </div>
      </div>
      <AnimatePresence initial={false}>
        {open && (
          <motion.nav
            id="mobile-nav"
            aria-label={t('mobileNav')}
            className="overflow-hidden border-t border-line bg-card md:hidden"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
          >
            <motion.div
              className="container-page flex flex-col gap-1 py-3"
              initial="hidden"
              animate="show"
              variants={{ show: { transition: { staggerChildren: 0.04, delayChildren: 0.05 } } }}
            >
              {nav.map((n) => (
                <motion.div key={n.to} variants={{ hidden: { opacity: 0, x: -10 }, show: { opacity: 1, x: 0 } }}>
                  <Link to={n.to} className="flex items-center justify-between rounded-md px-3 py-2.5 text-base font-semibold text-ink hover:bg-stone-50">
                    {t(n.key)}
                    <ArrowRight className="h-4 w-4 text-primary" aria-hidden />
                  </Link>
                </motion.div>
              ))}
              <motion.div variants={{ hidden: { opacity: 0, y: 6 }, show: { opacity: 1, y: 0 } }} className="mt-2 grid grid-cols-2 gap-2">
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
              </motion.div>
            </motion.div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}

const FOOT_LINK = 'group inline-flex items-center gap-1.5 text-chalk-text/75 transition-colors hover:text-marigold';

export function PublicFooter() {
  const t = useT(layoutMessages);
  const tc = useT(catalogMessages);
  const user = useAuthStore((s) => s.session?.user);
  const reduce = useReducedMotion();
  const toTop = () => window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  return (
    <footer className="relative overflow-hidden bg-chalkboard text-chalk-text">
      {/* torn-paper edge */}
      <svg viewBox="0 0 1200 24" preserveAspectRatio="none" className="absolute inset-x-0 top-0 h-4 w-full text-background" aria-hidden>
        <path d="M0 0h1200v8c-40 10-80-6-120 4s-80 10-120 0-80-8-120 2-80 10-120 0-80-8-120 2-80 10-120 0-80-6-120 4-80 8-120 0-80-6-120 4S40 18 0 8Z" fill="currentColor" />
      </svg>
      <div className="container-page pb-6 pt-16">
        {/* Big line + CTA */}
        <div className="flex flex-col items-start justify-between gap-6 border-b border-white/10 pb-10 md:flex-row md:items-end">
          <motion.p
            className="max-w-2xl font-display text-4xl font-extrabold leading-[1.05] tracking-tight sm:text-5xl lg:text-6xl"
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.6 }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          >
            {t('footerBigLine')}
          </motion.p>
          {!user && (
            <ButtonLink to="/signup" size="lg" className="shrink-0 bg-accent text-chalk-deep shadow-[0_5px_0_#A6370A] transition-transform hover:-translate-y-0.5 hover:bg-[#F7A04A]">
              {t('startFreeMock')}
            </ButtonLink>
          )}
        </div>

        <div className="grid gap-10 py-10 sm:grid-cols-2 md:grid-cols-[1.4fr_1fr_1fr_1fr]">
          <div>
            <Logo light />
            <p className="mt-3 max-w-xs text-sm leading-relaxed text-chalk-text/70">
              {interviewsEnabled() ? t('footerTagline', { tagline: t('authTagline') }) : t('footerTaglineExams')}
            </p>
            <p className="mt-4 text-sm text-chalk-text/70">
              {t('footerQuestions')}{' '}
              <a className="font-semibold text-marigold underline-offset-4 hover:underline" href={`mailto:${SUPPORT_EMAIL}`}>{SUPPORT_EMAIL}</a>
            </p>
          </div>
          <div>
            <h2 className="font-hand text-lg text-marigold">{t('footerExams')}</h2>
            <ul className="mt-3 space-y-2 text-sm">
              {EXAM_CATEGORIES.map((c) => (
                <li key={c.id}>
                  <Link className={FOOT_LINK} to={`/exams?category=${c.id}`}>
                    {categoryText(tc, c.id).label}
                    {!isCategoryOpen(c.id) && <span className="rounded-full bg-white/10 px-1.5 py-px text-[10px] font-bold uppercase tracking-wide text-chalk-text/60">{t('footerSoon')}</span>}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h2 className="font-hand text-lg text-marigold">{t('footerProduct')}</h2>
            <ul className="mt-3 space-y-2 text-sm">
              {interviewsEnabled() && <li><Link className={FOOT_LINK} to="/interviews">{t('mockInterviews')}</Link></li>}
              <li><Link className={FOOT_LINK} to="/pricing">{t('pricing')}</Link></li>
              <li><Link className={FOOT_LINK} to="/#how-it-works">{t('howItWorks')}</Link></li>
              <li><Link className={FOOT_LINK} to="/#faq">{t('faqs')}</Link></li>
            </ul>
          </div>
          <div>
            <h2 className="font-hand text-lg text-marigold">{t('footerCompany')}</h2>
            <ul className="mt-3 space-y-2 text-sm">
              <li><Link className={FOOT_LINK} to="/privacy">{t('privacy')}</Link></li>
              <li><Link className={FOOT_LINK} to="/terms">{t('terms')}</Link></li>
              <li><Link className={FOOT_LINK} to="/refund-policy">{t('refund')}</Link></li>
              <li><Link className={FOOT_LINK} to="/contact">{t('contact')}</Link></li>
            </ul>
          </div>
        </div>

        {/* Giant outlined wordmark */}
        <motion.p
          aria-hidden
          className="select-none whitespace-nowrap text-center font-display text-[17vw] font-extrabold leading-none tracking-tighter text-transparent [-webkit-text-stroke:1.5px_rgba(245,243,234,0.18)] lg:text-[11.5rem]"
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
        >
          PrepMitra
        </motion.p>

        <div className="mt-4 flex flex-col gap-3 border-t border-white/10 pt-5 text-xs text-chalk-text/60 md:flex-row md:items-center md:justify-between">
          <div className="flex flex-wrap items-center gap-3">
            <p>{t('copyright', { year: new Date().getFullYear() })}</p>
            <InstallAppButton className="border-white/30 bg-transparent text-chalk-text hover:bg-white/10" />
          </div>
          <p className="max-w-2xl md:text-right">{t('affiliation')}</p>
          <motion.button
            type="button"
            onClick={toTop}
            whileHover={{ y: -3 }}
            whileTap={{ scale: 0.95 }}
            className="inline-flex shrink-0 items-center gap-1.5 self-start rounded-full border border-white/20 px-3 py-1.5 font-semibold text-chalk-text transition-colors hover:bg-white/10 md:self-auto"
          >
            <ArrowUp className="h-3.5 w-3.5" aria-hidden />
            {t('backToTop')}
          </motion.button>
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
        <PageTransition><Outlet /></PageTransition>
      </main>
      <PublicFooter />
    </div>
  );
}
