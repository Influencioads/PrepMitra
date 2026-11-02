import { useState } from 'react';
import { Alert, Share, StyleSheet, View } from 'react-native';
import Constants from 'expo-constants';
import type { NotificationPreferences, PrivacySettings } from '@prepmitra/shared';
import { APP_NAME, DISCLAIMERS, SUPPORT_EMAIL } from '@prepmitra/shared';
import { AppText, Card, CardHeader, ConfirmDialog, Divider, Input, ListRow, Notice, Screen, SwitchRow, toast } from '@/components';
import { authService, errorMessage, profileService, USE_MOCK } from '@/services';
import {
  selectHistory, selectInterviewReports, useAuthStore, useExamStore, useInterviewStore, useProfileStore, useSubscriptionStore, wipeLocalData,
} from '@/store';
import { colors, spacing } from '@/theme';
import { personalDataExport } from '@/utils/reportText';

const NOTIFICATION_ROWS: { key: keyof NotificationPreferences; label: string; description: string }[] = [
  { key: 'push', label: 'Push notifications', description: 'Alerts on this device' },
  { key: 'email', label: 'Email', description: 'Receipts and weekly summaries' },
  { key: 'resultReady', label: 'Report ready', description: 'When an exam or interview report is ready' },
  { key: 'practiceReminders', label: 'Practice reminders', description: 'Keep your streak going' },
  { key: 'planExpiry', label: 'Plan and credit expiry', description: 'Before credits or your plan expire' },
  { key: 'offers', label: 'Offers', description: 'Discounts and new exam launches' },
];

const PRIVACY_ROWS: { key: keyof PrivacySettings; label: string; description: string }[] = [
  { key: 'shareWithRecruiters', label: 'Share my results with recruiters', description: 'Off by default. Only scores and your profile summary are shared, never answers.' },
  { key: 'productAnalytics', label: 'Product analytics', description: 'Anonymous usage data that helps us improve the app' },
  { key: 'showOnLeaderboard', label: 'Show me on leaderboards', description: 'Your first name and percentile only' },
];

export default function Settings() {
  const user = useAuthStore((s) => s.session?.user ?? null);
  const signOut = useAuthStore((s) => s.signOut);
  const settings = useProfileStore((s) => s.settings);
  const profile = useProfileStore((s) => s.profile);
  const updateSettings = useProfileStore((s) => s.updateSettings);
  const reports = useExamStore((s) => s.reports);
  const interviewReports = useInterviewStore((s) => s.reports);
  const credits = useSubscriptionStore((s) => s.sub.credits);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [confirmText, setConfirmText] = useState('');
  const [deleting, setDeleting] = useState(false);

  const setNotification = (key: keyof NotificationPreferences, value: boolean) => {
    updateSettings({ notifications: { ...settings.notifications, [key]: value } });
    void profileService.updateMe({ settings: { ...settings, notifications: { ...settings.notifications, [key]: value } } });
  };

  const applyPrivacy = (key: keyof PrivacySettings, value: boolean) => {
    updateSettings({ privacy: { ...settings.privacy, [key]: value } });
    void profileService.recordConsent(key, value).catch(() => toast.error('Could not record your consent. Try again.'));
    toast.success(value ? 'Preference turned on.' : 'Preference turned off.');
  };
  const setPrivacy = (key: keyof PrivacySettings, value: boolean) => {
    if (key === 'shareWithRecruiters' && value) {
      Alert.alert(
        'Share results with recruiters?',
        'Verified recruiters on PrepMitra AI could see your scores, percentiles and profile summary. You can turn this off at any time.',
        [
          { text: 'Not now', style: 'cancel' },
          { text: 'I agree', onPress: () => applyPrivacy(key, true) },
        ],
      );
      return;
    }
    applyPrivacy(key, value);
  };

  const exportData = async () => {
    try {
      await Share.share({
        title: `${APP_NAME} — my data`,
        message: personalDataExport({
          user,
          profile,
          settings,
          history: selectHistory(reports),
          interviewReports: selectInterviewReports(interviewReports),
          credits,
        }),
      });
    } catch (e) {
      toast.error(errorMessage(e, 'Could not open the share sheet.'));
    }
  };

  const logout = () =>
    Alert.alert('Log out?', 'Your demo data stays on this device for the next time you log in.', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Log out',
        style: 'destructive',
        onPress: () => {
          void authService.logout();
          signOut();
        },
      },
    ]);

  const deleteAccount = async () => {
    setDeleting(true);
    try {
      await profileService.deleteAccount();
      setDeleteOpen(false);
      toast.success('Your account and local data were deleted.');
      await wipeLocalData();
    } catch (e) {
      toast.error(errorMessage(e));
      setDeleting(false);
    }
  };

  return (
    <Screen>
      <Card>
        <CardHeader title="Notifications" />
        {NOTIFICATION_ROWS.map((r, i) => (
          <View key={r.key}>
            {i > 0 && <Divider />}
            <View style={styles.rowPad}>
              <SwitchRow label={r.label} description={r.description} value={settings.notifications[r.key]} onValueChange={(v) => setNotification(r.key, v)} />
            </View>
          </View>
        ))}
      </Card>

      <Card>
        <CardHeader title="Privacy" subtitle="Your choices under India’s DPDP Act. Changes are recorded as consent." />
        {PRIVACY_ROWS.map((r, i) => (
          <View key={r.key}>
            {i > 0 && <Divider />}
            <View style={styles.rowPad}>
              <SwitchRow label={r.label} description={r.description} value={settings.privacy[r.key]} onValueChange={(v) => setPrivacy(r.key, v)} />
            </View>
          </View>
        ))}
      </Card>

      <Card>
        <CardHeader title="Exam experience" />
        <SwitchRow
          label="Show English toggle during exams"
          description="Switch any translated question to English while you answer."
          value={settings.examLanguageToggle}
          onValueChange={(v) => updateSettings({ examLanguageToggle: v })}
        />
        <Divider />
        <View style={styles.rowPad}>
          <SwitchRow
            label="Reduce motion"
            description="Prefer fewer animations (your device setting also applies)."
            value={settings.reduceMotion}
            onValueChange={(v) => updateSettings({ reduceMotion: v })}
          />
        </View>
      </Card>

      <Card style={styles.links}>
        <CardHeader title="Your data" />
        <ListRow icon="share-outline" title="Download / share my data" subtitle="Profile, settings and history as JSON" onPress={exportData} />
        <Divider />
        <ListRow icon="log-out-outline" title="Log out" onPress={logout} />
        <Divider />
        <ListRow icon="trash-outline" title="Delete account" subtitle="Permanently remove your account and data" destructive onPress={() => setDeleteOpen(true)} />
      </Card>

      <Card style={styles.about}>
        <CardHeader title="About" />
        <AppText variant="small">{APP_NAME} · version {Constants.expoConfig?.version ?? '1.0.0'} · {USE_MOCK ? 'demo services' : 'live API'}</AppText>
        <AppText variant="small">Support: {SUPPORT_EMAIL}</AppText>
        <AppText variant="caption">{DISCLAIMERS.demoData}</AppText>
        <AppText variant="caption">{DISCLAIMERS.examAffiliation}</AppText>
      </Card>

      <ConfirmDialog
        visible={deleteOpen}
        title="Delete your account?"
        message="This removes your profile, attempts, reports and credits. In production your personal data is erased within 30 days. This cannot be undone."
        confirmLabel="Delete account"
        destructive
        loading={deleting}
        confirmDisabled={confirmText.trim().toUpperCase() !== 'DELETE'}
        onCancel={() => {
          setDeleteOpen(false);
          setConfirmText('');
        }}
        onConfirm={() => void deleteAccount()}
      >
        <Notice tone="error">Unused credits are forfeited.</Notice>
        <Input label='Type "DELETE" to confirm' value={confirmText} onChangeText={setConfirmText} autoCapitalize="characters" autoCorrect={false} />
      </ConfirmDialog>
      <AppText variant="caption" color={colors.textMuted} align="center">{DISCLAIMERS.authorization}</AppText>
    </Screen>
  );
}

const styles = StyleSheet.create({
  rowPad: { paddingVertical: spacing.sm },
  links: { paddingBottom: spacing.sm },
  about: { gap: spacing.sm },
});
