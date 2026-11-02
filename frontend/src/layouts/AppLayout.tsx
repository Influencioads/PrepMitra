import { useEffect, useState } from 'react';
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom';
import {
  Bell, BookOpen, ClipboardList, Coins, CreditCard, LayoutDashboard, Menu, MessageSquare, Settings, TrendingUp, User, X,
} from 'lucide-react';
import { Logo } from '@/components/ui';
import { ScrollToTop } from '@/components/layout/ScrollToTop';
import { UserMenu } from '@/components/layout/UserMenu';
import { useSubscriptionStore, useUnreadCount } from '@/store';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { LanguageSwitcher } from '@/i18n/LanguageSwitcher';
import { layoutMessages } from '@/i18n/messages/layout';

const NAV_GROUPS = [
  {
    label: 'groupPractice',
    items: [
      { to: '/dashboard', label: 'navDashboard', icon: LayoutDashboard },
      { to: '/exams', label: 'navMockExams', icon: BookOpen },
      { to: '/interviews', label: 'navMockInterviews', icon: MessageSquare },
      { to: '/my-tests', label: 'navMyTests', icon: ClipboardList },
      { to: '/progress', label: 'navProgress', icon: TrendingUp },
    ],
  },
  {
    label: 'groupAccount',
    items: [
      { to: '/subscription', label: 'navCredits', icon: CreditCard },
      { to: '/notifications', label: 'navNotifications', icon: Bell },
      { to: '/profile', label: 'navProfile', icon: User },
      { to: '/settings', label: 'navSettings', icon: Settings },
    ],
  },
] as const;

function SidebarNav({ onNavigate }: { onNavigate?: () => void }) {
  const unread = useUnreadCount();
  const t = useT(layoutMessages);
  return (
    <nav aria-label={t('appNav')} className="flex flex-col gap-6">
      {NAV_GROUPS.map((g) => (
        <div key={g.label}>
          <p className="px-3 text-xs font-semibold uppercase tracking-wider text-subtle">{t(g.label)}</p>
          <ul className="mt-2 space-y-0.5">
            {g.items.map(({ to, label, icon: Icon }) => (
              <li key={to}>
                <NavLink
                  to={to}
                  onClick={onNavigate}
                  end={to === '/exams'}
                  className={({ isActive }) =>
                    cn(
                      'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                      isActive ? 'bg-primary-soft text-primary' : 'text-ink/80 hover:bg-stone-100 hover:text-ink',
                    )
                  }
                >
                  <Icon className="h-[18px] w-[18px]" aria-hidden />
                  <span className="flex-1">{t(label)}</span>
                  {to === '/notifications' && unread > 0 && (
                    <span className="rounded-full bg-danger px-1.5 text-xs font-semibold text-white" aria-label={t('unread', { count: unread })}>
                      {unread}
                    </span>
                  )}
                </NavLink>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </nav>
  );
}

function CreditsCard() {
  const credits = useSubscriptionStore((s) => s.sub.credits);
  const planId = useSubscriptionStore((s) => s.sub.planId);
  const freeUsed = useSubscriptionStore((s) => s.sub.freeMiniMockUsed);
  const t = useT(layoutMessages);
  return (
    <div className="rounded-xl bg-secondary p-4 text-white">
      <p className="text-xs font-medium text-white/80">{t('availableCredits')}</p>
      <p className="mt-1 text-2xl font-bold">{credits}</p>
      <p className="mt-1 text-xs text-white/80">
        {planId === 'free' ? (freeUsed ? t('freeTrialUsed') : t('freeMiniAvailable')) : planId === 'monthly' ? t('planMonthly') : planId === 'yearly' ? t('planYearly') : t('planPayPerMock')}
      </p>
      <Link to="/subscription" className="mt-3 inline-flex rounded-md bg-white/15 px-3 py-1.5 text-xs font-semibold hover:bg-white/25">
        {credits === 0 ? t('getCredits') : t('managePlan')}
      </Link>
    </div>
  );
}

export function AppTopbar({ onMenu }: { onMenu?: () => void }) {
  const unread = useUnreadCount();
  const credits = useSubscriptionStore((s) => s.sub.credits);
  const t = useT(layoutMessages);
  return (
    <header className="sticky top-0 z-20 flex h-16 items-center gap-3 border-b border-line bg-card/95 px-4 backdrop-blur sm:px-6">
      {onMenu && (
        <button type="button" onClick={onMenu} className="rounded-md p-2 hover:bg-stone-100 lg:hidden" aria-label={t('openNavigation')}>
          <Menu className="h-5 w-5" />
        </button>
      )}
      <div className="lg:hidden">
        <Logo to="/dashboard" />
      </div>
      <div className="ml-auto flex items-center gap-1.5 sm:gap-3">
        <LanguageSwitcher className="hidden sm:inline-flex" />
        <Link
          to="/subscription"
          className="hidden items-center gap-1.5 rounded-full border border-line px-3 py-1.5 text-sm font-medium hover:bg-stone-50 sm:inline-flex"
          aria-label={t('creditsAvailable', { count: credits })}
        >
          <Coins className="h-4 w-4 text-warning" aria-hidden /> {t('creditsChip', { count: credits })}
        </Link>
        <Link to="/notifications" className="relative rounded-full p-2 hover:bg-stone-100" aria-label={t('notificationsAria', { count: unread })}>
          <Bell className="h-5 w-5" />
          {unread > 0 && <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-danger" aria-hidden />}
        </Link>
        <UserMenu />
      </div>
    </header>
  );
}

export function AppLayout() {
  const [drawer, setDrawer] = useState(false);
  const location = useLocation();
  const t = useT(layoutMessages);
  useEffect(() => setDrawer(false), [location.pathname]);

  useEffect(() => {
    if (!drawer) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setDrawer(false);
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [drawer]);

  return (
    <div className="min-h-screen bg-background">
      <ScrollToTop />
      <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-3 focus:z-50 focus:rounded-md focus:bg-card focus:px-3 focus:py-2 focus:shadow">
        {t('skipToContent')}
      </a>
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-64 flex-col border-r border-line bg-card lg:flex">
        <div className="flex h-16 items-center px-5">
          <Logo to="/dashboard" />
        </div>
        <div className="flex flex-1 flex-col justify-between overflow-y-auto px-3 pb-4 pt-2 scrollbar-thin">
          <SidebarNav />
          <CreditsCard />
        </div>
      </aside>

      {drawer && (
        <div className="fixed inset-0 z-40 lg:hidden" role="dialog" aria-modal="true" aria-label={t('navigation')}>
          <div className="absolute inset-0 bg-stone-900/40" onClick={() => setDrawer(false)} />
          <div className="absolute inset-y-0 left-0 flex w-72 max-w-[85vw] flex-col bg-card shadow-overlay animate-fade-in">
            <div className="flex h-16 items-center justify-between px-5">
              <Logo to="/dashboard" />
              <button type="button" onClick={() => setDrawer(false)} className="rounded-md p-2 hover:bg-stone-100" aria-label={t('closeNavigation')}>
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="flex flex-1 flex-col justify-between gap-6 overflow-y-auto px-3 pb-4">
              <SidebarNav onNavigate={() => setDrawer(false)} />
              <div className="space-y-4">
                <LanguageSwitcher size="md" />
                <CreditsCard />
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="lg:pl-64">
        <AppTopbar onMenu={() => setDrawer(true)} />
        <main id="main" className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
