import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Bell, BellOff, CalendarClock, CheckCheck, CreditCard, FileText, Mail, MailOpen, MessageSquare, Sparkles, Trash2 } from 'lucide-react';
import type { AppNotification, NotificationType } from '@prepmitra/shared';
import { formatDateTime, relativeTime } from '@prepmitra/shared';
import { Button, Card, ConfirmationDialog, EmptyState, PageHeader, Tabs } from '@/components/ui';
import { notificationService } from '@/services';
import { useNotificationStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { accountMessages } from '@/i18n/messages/account';

const TYPE_ICON: Record<NotificationType, typeof Bell> = {
  result: FileText, payment: CreditCard, reminder: Bell, plan: CalendarClock, system: Sparkles, interview: MessageSquare,
};
const TYPE_TONE: Record<NotificationType, string> = {
  result: 'bg-primary-soft text-primary', payment: 'bg-success-soft text-success', reminder: 'bg-warning-soft text-warning-ink',
  plan: 'bg-secondary-soft text-secondary', system: 'bg-info-soft text-info', interview: 'bg-secondary-soft text-secondary',
};

export function NotificationsPage() {
  const t = useT(accountMessages);
  useDocumentTitle(t('notifTitle'));
  const navigate = useNavigate();
  const items = useNotificationStore((s) => s.items);
  const { markRead, markUnread, markAllRead, remove, clearAll } = useNotificationStore.getState();
  const [tab, setTab] = useState<'all' | 'unread'>('all');
  const [confirmClear, setConfirmClear] = useState(false);
  const unread = items.filter((n) => !n.read);
  const list = tab === 'all' ? items : unread;

  const open = (n: AppNotification) => {
    if (!n.read) {
      markRead(n.id);
      void notificationService.markRead([n.id]);
    }
    if (n.link) navigate(n.link);
  };

  return (
    <div className="mx-auto max-w-3xl">
      <PageHeader
        title={t('notifTitle')}
        description={t('notifDesc')}
        actions={
          <>
            <Button
              variant="outline"
              size="sm"
              leftIcon={<CheckCheck className="h-4 w-4" />}
              disabled={unread.length === 0}
              onClick={() => {
                markAllRead();
                void notificationService.markRead(unread.map((n) => n.id));
                toast.success(t('allMarkedRead'));
              }}
            >
              {t('markAllRead')}
            </Button>
            <Button variant="ghost" size="sm" leftIcon={<Trash2 className="h-4 w-4" />} disabled={items.length === 0} onClick={() => setConfirmClear(true)}>
              {t('clearAll')}
            </Button>
          </>
        }
      />
      <Tabs
        ariaLabel={t('filterNotif')}
        value={tab}
        onChange={setTab}
        items={[
          { value: 'all', label: t('tabAll'), count: items.length },
          { value: 'unread', label: t('tabUnread'), count: unread.length },
        ]}
      />

      <div className="mt-4">
        {list.length === 0 ? (
          <EmptyState
            icon={<BellOff className="h-6 w-6" />}
            title={tab === 'unread' ? t('caughtUp') : t('noNotif')}
            description={tab === 'unread' ? t('caughtUpDesc') : t('noNotifDesc')}
          />
        ) : (
          <Card>
            <ul className="divide-y divide-line">
              {list.map((n) => {
                const Icon = TYPE_ICON[n.type];
                return (
                  <li key={n.id} className={cn('flex gap-3 p-4 transition-colors', !n.read && 'bg-primary-soft/40')}>
                    <span className={cn('flex h-10 w-10 shrink-0 items-center justify-center rounded-full', TYPE_TONE[n.type])}>
                      <Icon className="h-5 w-5" aria-hidden />
                    </span>
                    <button type="button" onClick={() => open(n)} className="min-w-0 flex-1 text-left">
                      <span className="flex items-center gap-2">
                        {!n.read && <span className="h-2 w-2 shrink-0 rounded-full bg-primary" aria-hidden />}
                        <span className={cn('text-sm', n.read ? 'font-medium' : 'font-semibold')}>{n.title}</span>
                        <span className="sr-only">{n.read ? t('readSr') : t('unreadSr')}</span>
                      </span>
                      <span className="mt-0.5 block text-sm text-muted">{n.body}</span>
                      <time dateTime={n.createdAt} title={formatDateTime(n.createdAt)} className="mt-1 block text-xs text-subtle">{relativeTime(n.createdAt)}</time>
                    </button>
                    <div className="flex shrink-0 flex-col gap-1 sm:flex-row sm:items-start">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8"
                        aria-label={n.read ? t('markUnreadAria', { title: n.title }) : t('markReadAria', { title: n.title })}
                        title={n.read ? t('markUnread') : t('markRead')}
                        onClick={() => (n.read ? markUnread(n.id) : markRead(n.id))}
                      >
                        {n.read ? <Mail className="h-4 w-4" /> : <MailOpen className="h-4 w-4" />}
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 text-muted hover:text-danger"
                        aria-label={t('deleteAria', { title: n.title })}
                        title={t('delete')}
                        onClick={() => {
                          remove(n.id);
                          toast.success(t('notifDeleted'));
                        }}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </li>
                );
              })}
            </ul>
          </Card>
        )}
      </div>

      <ConfirmationDialog
        open={confirmClear}
        onOpenChange={setConfirmClear}
        title={t('clearTitle')}
        description={t('clearDesc')}
        confirmLabel={t('clearAll')}
        variant="danger"
        onConfirm={() => {
          clearAll();
          setConfirmClear(false);
          toast.success(t('cleared'));
        }}
      />
    </div>
  );
}
