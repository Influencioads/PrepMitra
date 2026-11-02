import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ChevronDown, LayoutDashboard, LogOut, Settings, ShieldCheck, User } from 'lucide-react';
import toast from 'react-hot-toast';
import { Avatar } from '@/components/ui';
import { authService } from '@/services';
import { useAuthStore } from '@/store';
import { useT } from '@/i18n';
import { commonMessages } from '@/i18n/messages/common';
import { layoutMessages } from '@/i18n/messages/layout';

export function UserMenu() {
  const user = useAuthStore((s) => s.session?.user);
  const signOut = useAuthStore((s) => s.signOut);
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const t = useT(layoutMessages);
  const tc = useT(commonMessages);

  useEffect(() => {
    if (!open) return;
    const onDoc = (e: MouseEvent) => !ref.current?.contains(e.target as Node) && setOpen(false);
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false);
    document.addEventListener('mousedown', onDoc);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDoc);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  if (!user) return null;

  const logout = async () => {
    setOpen(false);
    await authService.logout();
    signOut();
    toast.success(t('loggedOut'));
    navigate('/');
  };

  const item = 'flex w-full items-center gap-2.5 rounded-md px-3 py-2 text-sm text-ink hover:bg-stone-100';
  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-haspopup="menu"
        aria-expanded={open}
        className="flex items-center gap-2 rounded-full p-1 pr-2 hover:bg-stone-100"
      >
        <Avatar name={user.name} size="sm" />
        <span className="hidden max-w-[120px] truncate text-sm font-medium md:block">{user.name.split(' ')[0]}</span>
        <ChevronDown className="hidden h-4 w-4 text-muted md:block" aria-hidden />
        <span className="sr-only">{t('openAccountMenu')}</span>
      </button>
      {open && (
        <div role="menu" className="absolute right-0 z-40 mt-2 w-60 rounded-xl border border-line bg-card p-1.5 shadow-raised animate-fade-in">
          <div className="border-b border-line px-3 pb-2 pt-1.5">
            <p className="truncate text-sm font-semibold">{user.name}</p>
            <p className="truncate text-xs text-muted">{user.email ?? `+91 ${user.phone}`}</p>
          </div>
          <div className="pt-1">
            {user.role === 'admin' ? (
              <Link role="menuitem" to="/admin/dashboard" className={item} onClick={() => setOpen(false)}>
                <ShieldCheck className="h-4 w-4 text-muted" /> {t('adminConsole')}
              </Link>
            ) : (
              <Link role="menuitem" to="/dashboard" className={item} onClick={() => setOpen(false)}>
                <LayoutDashboard className="h-4 w-4 text-muted" /> {tc('dashboard')}
              </Link>
            )}
            <Link role="menuitem" to="/profile" className={item} onClick={() => setOpen(false)}>
              <User className="h-4 w-4 text-muted" /> {tc('profile')}
            </Link>
            <Link role="menuitem" to="/settings" className={item} onClick={() => setOpen(false)}>
              <Settings className="h-4 w-4 text-muted" /> {tc('settings')}
            </Link>
            <button role="menuitem" type="button" onClick={logout} className={`${item} text-danger`}>
              <LogOut className="h-4 w-4" /> {tc('logout')}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
