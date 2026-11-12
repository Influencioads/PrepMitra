import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Database, Languages, LogOut, ShieldCheck, UserX } from 'lucide-react';
import type { NotificationPreferences, PrivacySettings } from '@prepmitra/shared';
import { STORAGE_KEYS } from '@prepmitra/shared';
import { Button, Card, CardBody, CardHeader, ConfirmationDialog, Input, Notice, PageHeader, Switch } from '@/components/ui';
import { authService, errorMessage, profileService } from '@/services';
import {
  useAuthStore, useExamStore, useInterviewStore, useNotificationStore, useProfileStore, useSubscriptionStore, wipeLocalData,
} from '@/store';
import { downloadBlob } from '@/features/account/download';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT } from '@/i18n';
import { LanguageSwitcher } from '@/i18n/LanguageSwitcher';
import { accountMessages } from '@/i18n/messages/account';
import { ReminderSettingsCard } from '@/components/mentor/ReminderSettingsCard';
import { USE_MOCK } from '@/services/mock';

type AKey = keyof typeof accountMessages.en;
const NOTIF: { key: keyof NotificationPreferences; label: AKey; description: AKey }[] = [
  { key: 'push', label: 'pushLabel', description: 'pushDesc' },
  { key: 'email', label: 'emailLabel', description: 'emailDesc' },
  { key: 'resultReady', label: 'resultReadyLabel', description: 'resultReadyDesc' },
  { key: 'practiceReminders', label: 'remindersLabel', description: 'remindersDesc' },
  { key: 'planExpiry', label: 'expiryLabel', description: 'expiryDesc' },
  { key: 'offers', label: 'offersLabel', description: 'offersDesc' },
];

export function SettingsPage() {
  const t = useT(accountMessages);
  useDocumentTitle(t('settingsTitle'));
  const navigate = useNavigate();
  const settings = useProfileStore((s) => s.settings);
  const updateSettings = useProfileStore((s) => s.updateSettings);
  const signOut = useAuthStore((s) => s.signOut);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [confirmText, setConfirmText] = useState('');
  const [deleting, setDeleting] = useState(false);
  const [logoutAll, setLogoutAll] = useState(false);

  const setNotif = (key: keyof NotificationPreferences, v: boolean) => {
    updateSettings({ notifications: { ...settings.notifications, [key]: v } });
    toast.success(t('notifSaved'));
  };

  const setPrivacy = async (key: keyof PrivacySettings, v: boolean) => {
    updateSettings({ privacy: { ...settings.privacy, [key]: v } });
    try {
      await profileService.recordConsent(key === 'shareWithRecruiters' ? 'recruiter-sharing' : key, v);
      toast.success(key === 'shareWithRecruiters' ? (v ? t('recruiterOn') : t('recruiterOff')) : t('privacySaved'));
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  const exportData = () => {
    const data = {
      exportedAt: new Date().toISOString(),
      note: 'PrepMitra AI prototype — data stored in this browser only.',
      account: useAuthStore.getState().session?.user,
      profile: useProfileStore.getState().profile,
      settings: useProfileStore.getState().settings,
      examReports: Object.values(useExamStore.getState().reports),
      attempts: Object.values(useExamStore.getState().attempts),
      interviews: Object.values(useInterviewStore.getState().reports),
      subscription: useSubscriptionStore.getState().sub,
      orders: useSubscriptionStore.getState().orders,
      notifications: useNotificationStore.getState().items,
      storageKeys: STORAGE_KEYS,
    };
    downloadBlob(`prepmitra-my-data-${new Date().toISOString().slice(0, 10)}.json`, JSON.stringify(data, null, 2), 'application/json');
    toast.success(t('dataDownloaded'));
  };

  const deleteAccount = async () => {
    setDeleting(true);
    try {
      await profileService.deleteAccount();
      wipeLocalData();
      toast.success(t('accountDeleted'), { duration: 6000 });
      navigate('/', { replace: true });
    } catch (e) {
      toast.error(errorMessage(e));
      setDeleting(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <PageHeader title={t('settingsTitle')} description={t('settingsDesc')} />

      <Card>
        <CardBody className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex gap-3">
            <Languages className="mt-0.5 h-5 w-5 shrink-0 text-muted" aria-hidden />
            <div>
              <h2 className="text-sm font-semibold">{t('websiteLanguage')}</h2>
              <p className="text-xs text-muted">{t('websiteLanguageHint')}</p>
            </div>
          </div>
          <LanguageSwitcher size="md" className="self-start sm:self-auto" />
        </CardBody>
      </Card>

      <Card>
        <CardHeader title={t('notifPrefs')} />
        <CardBody className="divide-y divide-line py-1">
          {NOTIF.map((n) => (
            <Switch key={n.key} label={t(n.label)} description={t(n.description)} checked={settings.notifications[n.key]} onChange={(v) => setNotif(n.key, v)} />
          ))}
        </CardBody>
      </Card>

      {!USE_MOCK && <ReminderSettingsCard />}

      <Card>
        <CardHeader title={t('privacy')} description={t('privacyDesc')} />
        <CardBody className="divide-y divide-line py-1">
          <Switch
            label={t('shareRecruiters')}
            description={t('shareRecruitersDesc')}
            checked={settings.privacy.shareWithRecruiters}
            onChange={(v) => void setPrivacy('shareWithRecruiters', v)}
          />
          <Switch label={t('analytics')} description={t('analyticsDescSetting')} checked={settings.privacy.productAnalytics} onChange={(v) => void setPrivacy('productAnalytics', v)} />
          <Switch label={t('leaderboard')} description={t('leaderboardDesc')} checked={settings.privacy.showOnLeaderboard} onChange={(v) => void setPrivacy('showOnLeaderboard', v)} />
        </CardBody>
      </Card>

      <Card>
        <CardHeader title={t('examPrefs')} />
        <CardBody className="divide-y divide-line py-1">
          <Switch
            label={t('langToggle')}
            description={t('langToggleDesc')}
            checked={settings.examLanguageToggle}
            onChange={(v) => { updateSettings({ examLanguageToggle: v }); toast.success(t('examPrefSaved')); }}
          />
          <Switch
            label={t('reduceMotion')}
            description={t('reduceMotionDesc')}
            checked={settings.reduceMotion}
            onChange={(v) => { updateSettings({ reduceMotion: v }); toast.success(t('displayPrefSaved')); }}
          />
        </CardBody>
      </Card>

      <Card>
        <CardHeader title={t('accountMgmt')} />
        <CardBody className="space-y-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex gap-3">
              <Database className="mt-0.5 h-5 w-5 text-muted" aria-hidden />
              <div>
                <p className="text-sm font-medium">{t('downloadData')}</p>
                <p className="text-xs text-muted">{t('downloadDataDesc')}</p>
              </div>
            </div>
            <Button variant="outline" size="sm" onClick={exportData}>{t('download')}</Button>
          </div>
          <div className="flex flex-col gap-3 border-t border-line pt-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex gap-3">
              <LogOut className="mt-0.5 h-5 w-5 text-muted" aria-hidden />
              <div>
                <p className="text-sm font-medium">{t('logoutAll')}</p>
                <p className="text-xs text-muted">{t('logoutAllDesc')}</p>
              </div>
            </div>
            <Button variant="outline" size="sm" onClick={() => setLogoutAll(true)}>{t('logoutEverywhere')}</Button>
          </div>
          <div className="flex flex-col gap-3 border-t border-line pt-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex gap-3">
              <UserX className="mt-0.5 h-5 w-5 text-danger" aria-hidden />
              <div>
                <p className="text-sm font-medium text-danger">{t('deleteAccount')}</p>
                <p className="text-xs text-muted">{t('deleteAccountDesc')}</p>
              </div>
            </div>
            <Button variant="danger" size="sm" onClick={() => { setConfirmText(''); setDeleteOpen(true); }}>{t('deleteAccount')}</Button>
          </div>
        </CardBody>
      </Card>

      <Notice tone="info" title={t('aboutPrototype')}>
        <span className="inline-flex items-start gap-1.5"><ShieldCheck className="mt-0.5 h-4 w-4 shrink-0" aria-hidden />{t('demoDataNotice')}</span>
      </Notice>

      <ConfirmationDialog
        open={logoutAll}
        onOpenChange={setLogoutAll}
        title={t('logoutAllTitle')}
        description={t('logoutAllConfirm')}
        confirmLabel={t('logoutEverywhere')}
        onConfirm={async () => {
          await authService.logout();
          signOut();
          toast.success(t('loggedOutAll'));
          navigate('/login', { replace: true });
        }}
      />

      <ConfirmationDialog
        open={deleteOpen}
        onOpenChange={setDeleteOpen}
        title={t('deleteTitle')}
        description={t('deleteDesc')}
        confirmLabel={t('deleteMyAccount')}
        variant="danger"
        loading={deleting}
        onConfirm={() => {
          if (confirmText !== 'DELETE') {
            toast.error(t('typeDeleteToast'));
            return;
          }
          return deleteAccount();
        }}
      >
        <Input label={<>{t('typeDeletePre')} <b>DELETE</b> {t('typeDeletePost')}</>} value={confirmText} onChange={(e) => setConfirmText(e.target.value)} autoComplete="off" aria-describedby="delete-hint" />
        <p id="delete-hint" className="mt-2 text-xs text-muted">{t('noRefund')}</p>
      </ConfirmationDialog>
    </div>
  );
}
