import { useEffect, useState } from 'react';
import { Link, NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import {
  BookOpenCheck, ChartColumn, ClipboardCheck, CreditCard, ExternalLink, FileStack, Languages, LayoutDashboard, LogOut,
  Menu, MessageSquare, Settings, ShieldAlert, Sparkles, Users, X,
} from 'lucide-react';
import toast from 'react-hot-toast';
import { DISCLAIMERS } from '@prepmitra/shared';
import { Avatar, Badge, Logo } from '@/components/ui';
import { ScrollToTop } from '@/components/layout/ScrollToTop';
import { authService } from '@/services';
import { useAuthStore } from '@/store';
import { selectOpenReviewCount, useAdminStore } from '@/store/adminStore';
import { TEAM_ROLE_LABELS } from '@/components/admin/labels';
import { cn } from '@/utils/cn';

const NAV_GROUPS = [
  {
    label: 'Overview',
    items: [
      { to: '/admin/dashboard', label: 'Dashboard', icon: LayoutDashboard },
      { to: '/admin/reports', label: 'Reports', icon: ChartColumn },
    ],
  },
  {
    label: 'Content',
    items: [
      { to: '/admin/exams', label: 'Exams & blueprints', icon: FileStack },
      { to: '/admin/questions', label: 'Question bank', icon: BookOpenCheck },
      { to: '/admin/review-queue', label: 'Review queue', icon: ClipboardCheck },
      { to: '/admin/ai-lessons', label: 'AI lessons & glossary', icon: Sparkles },
      { to: '/admin/languages', label: 'Languages', icon: Languages },
      { to: '/admin/interview-roles', label: 'Interview roles', icon: MessageSquare },
    ],
  },
  {
    label: 'Business',
    items: [
      { to: '/admin/users', label: 'Users', icon: Users },
      { to: '/admin/payments', label: 'Payments', icon: CreditCard },
    ],
  },
  {
    label: 'System',
    items: [{ to: '/admin/settings', label: 'Settings', icon: Settings }],
  },
];

function AdminNav({ onNavigate }: { onNavigate?: () => void }) {
  const openReviews = useAdminStore(selectOpenReviewCount);
  return (
    <nav aria-label="Admin" className="flex flex-col gap-5">
      {NAV_GROUPS.map((g) => (
        <div key={g.label}>
          <p className="px-3 text-xs font-semibold uppercase tracking-wider text-stone-400">{g.label}</p>
          <ul className="mt-1.5 space-y-0.5">
            {g.items.map(({ to, label, icon: Icon }) => (
              <li key={to}>
                <NavLink
                  to={to}
                  onClick={onNavigate}
                  className={({ isActive }) =>
                    cn(
                      'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                      isActive ? 'bg-white/10 text-white' : 'text-stone-300 hover:bg-white/5 hover:text-white',
                    )
                  }
                >
                  <Icon className="h-[18px] w-[18px]" aria-hidden />
                  <span className="flex-1">{label}</span>
                  {to === '/admin/review-queue' && openReviews > 0 && (
                    <span className="rounded-full bg-warning px-1.5 text-xs font-semibold text-stone-900" aria-label={`${openReviews} open`}>
                      {openReviews}
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

function SidebarBrand() {
  return (
    <div className="flex items-center gap-2">
      <Logo to="/admin/dashboard" light />
      <Badge tone="warning" className="ml-1">Admin</Badge>
    </div>
  );
}

export function AdminLayout() {
  const [drawer, setDrawer] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.session?.user);
  const signOut = useAuthStore((s) => s.signOut);
  const memberRole = useAdminStore((s) => s.team.find((m) => m.email === user?.email)?.role);

  useEffect(() => setDrawer(false), [location.pathname]);
  useEffect(() => {
    if (!drawer) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setDrawer(false);
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [drawer]);

  const logout = async () => {
    try {
      await authService.logout();
    } catch {
      /* demo logout never fails; continue clearing the local session */
    }
    signOut();
    toast.success('Signed out of the admin console');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-background">
      <ScrollToTop />
      <a href="#admin-main" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-3 focus:z-50 focus:rounded-md focus:bg-card focus:px-3 focus:py-2 focus:shadow">
        Skip to content
      </a>

      <aside className="fixed inset-y-0 left-0 z-30 hidden w-64 flex-col bg-stone-900 lg:flex">
        <div className="flex h-16 items-center px-5">
          <SidebarBrand />
        </div>
        <div className="flex-1 overflow-y-auto px-3 pb-4 pt-2 scrollbar-thin">
          <AdminNav />
        </div>
        <p className="border-t border-white/10 px-5 py-3 text-xs text-stone-400">Demo console · mock data only</p>
      </aside>

      {drawer && (
        <div className="fixed inset-0 z-40 lg:hidden" role="dialog" aria-modal="true" aria-label="Admin navigation">
          <div className="absolute inset-0 bg-stone-900/50" onClick={() => setDrawer(false)} />
          <div className="absolute inset-y-0 left-0 flex w-72 max-w-[85vw] flex-col bg-stone-900 shadow-overlay animate-fade-in">
            <div className="flex h-16 items-center justify-between px-5">
              <SidebarBrand />
              <button type="button" onClick={() => setDrawer(false)} className="rounded-md p-2 text-stone-300 hover:bg-white/10" aria-label="Close navigation">
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto px-3 pb-4">
              <AdminNav onNavigate={() => setDrawer(false)} />
            </div>
          </div>
        </div>
      )}

      <div className="lg:pl-64">
        <header className="sticky top-0 z-20 flex h-16 items-center gap-2 border-b border-line bg-card/95 px-4 backdrop-blur sm:gap-3 sm:px-6">
          <button type="button" onClick={() => setDrawer(true)} className="rounded-md p-2 hover:bg-stone-100 lg:hidden" aria-label="Open admin navigation">
            <Menu className="h-5 w-5" />
          </button>
          <p className="truncate text-sm font-semibold text-ink">
            Admin console
          </p>
          <div className="ml-auto flex items-center gap-1 sm:gap-2">
            <Link
              to="/exams"
              className="inline-flex items-center gap-1.5 rounded-lg px-2 py-2 text-sm font-medium text-primary hover:bg-primary-soft sm:px-3"
              aria-label="View learner site"
            >
              <ExternalLink className="h-4 w-4" aria-hidden />
              <span className="hidden sm:inline">View learner site</span>
            </Link>
            {user && (
              <div className="flex items-center gap-2 border-l border-line pl-2 sm:pl-3">
                <Avatar name={user.name} size="sm" />
                <div className="hidden leading-tight md:block">
                  <p className="max-w-[160px] truncate text-sm font-medium">{user.name}</p>
                  <p className="text-xs text-muted">{memberRole ? TEAM_ROLE_LABELS[memberRole] : 'Admin'}</p>
                </div>
              </div>
            )}
            <button
              type="button"
              onClick={() => void logout()}
              className="inline-flex items-center gap-1.5 rounded-lg px-2 py-2 text-sm font-medium text-danger hover:bg-danger-soft sm:px-3"
              aria-label="Log out"
            >
              <LogOut className="h-4 w-4" aria-hidden />
              <span className="hidden sm:inline">Log out</span>
            </button>
          </div>
        </header>

        <div className="border-b border-amber-200 bg-warning-soft px-4 py-2 text-xs text-amber-900 sm:px-6" role="note">
          <p className="mx-auto flex max-w-7xl items-start gap-2">
            <ShieldAlert className="mt-0.5 h-3.5 w-3.5 shrink-0" aria-hidden />
            <span>
              <strong>Demo admin console</strong> — route guards are UI-only.{' '}
              <span className="sm:hidden">The backend must enforce RBAC on /v1/admin/*.</span>
              <span className="hidden sm:inline">{DISCLAIMERS.authorization.replace(/\.$/, '')} (RBAC on /v1/admin/*).</span>
            </span>
          </p>
        </div>

        <main id="admin-main" className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
