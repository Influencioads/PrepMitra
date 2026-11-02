import { Alert, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import {
  EDUCATION_LEVELS, PLANS, formatDate, getExamById, getRoleById, languageName, maskPhone,
} from '@prepmitra/shared';
import {
  AppText, Avatar, Badge, Button, Card, CardHeader, Divider, ListRow, Screen, TabHeader,
} from '@/components';
import { authService } from '@/services';
import { useAuthStore, useProfileStore, useSubscriptionStore, useUnreadCount } from '@/store';
import { colors, spacing } from '@/theme';

function Row({ label, value }: { label: string; value?: string }) {
  return (
    <View style={styles.row}>
      <AppText variant="small" style={styles.rowKey}>{label}</AppText>
      <AppText variant="smallStrong" style={styles.flex}>{value || '—'}</AppText>
    </View>
  );
}

export default function Profile() {
  const user = useAuthStore((s) => s.session?.user);
  const signOut = useAuthStore((s) => s.signOut);
  const profile = useProfileStore((s) => s.profile);
  const sub = useSubscriptionStore((s) => s.sub);
  const unread = useUnreadCount();
  const plan = PLANS.find((p) => p.id === sub.planId);

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

  if (!user) return null;
  const targets = [
    ...profile.targetExamIds.map((id) => getExamById(id)?.shortTitle ?? id),
  ];
  const roles = profile.targetRoleIds.map((id) => getRoleById(id)?.shortTitle ?? id);

  return (
    <Screen edges={['top', 'left', 'right']}>
      <TabHeader title="Profile" />
      <Card style={styles.identity}>
        <Avatar name={user.name} size={64} />
        <View style={styles.flex}>
          <AppText variant="h2" numberOfLines={1}>{user.name}</AppText>
          <AppText variant="small">{maskPhone(user.phone)}</AppText>
          {user.email ? <AppText variant="small" numberOfLines={1}>{user.email}</AppText> : null}
        </View>
      </Card>
      <Button title="Edit profile" variant="outline" leftIcon="create-outline" onPress={() => router.push('/edit-profile')} />

      <Card onPress={() => router.push('/subscription')} style={styles.plan} accessibilityLabel={`${plan?.name ?? 'Plan'}, ${sub.credits} credits. Manage credits and plans.`}>
        <View style={styles.flex}>
          <AppText variant="caption">Current plan</AppText>
          <AppText variant="h3">{plan?.name ?? sub.planId}</AppText>
          <AppText variant="small">
            {sub.renewsAt ? `${sub.autoRenew ? 'Renews' : 'Ends'} ${formatDate(sub.renewsAt)}` : sub.freeMiniMockUsed ? 'Pay as you go' : 'Free mini mock available'}
          </AppText>
        </View>
        <View style={styles.credits}>
          <AppText variant="h1" color={colors.primary}>{sub.credits}</AppText>
          <AppText variant="caption">credits</AppText>
        </View>
      </Card>

      <Card style={styles.links}>
        <ListRow icon="notifications-outline" title="Notifications" onPress={() => router.push('/notifications')} right={unread > 0 ? <Badge label={`${unread} new`} tone="error" /> : undefined} />
        <Divider />
        <ListRow icon="wallet-outline" title="Credits & subscriptions" onPress={() => router.push('/subscription')} />
        <Divider />
        <ListRow icon="analytics-outline" title="Progress analytics" onPress={() => router.push('/progress')} />
        <Divider />
        <ListRow icon="settings-outline" title="Settings & privacy" onPress={() => router.push('/settings')} />
      </Card>

      <Card>
        <CardHeader title="Personal details" action={<Button title="Edit" size="sm" variant="ghost" onPress={() => router.push('/edit-profile')} accessibilityLabel="Edit personal details" />} />
        <Row label="Date of birth" value={user.dob ? formatDate(user.dob) : undefined} />
        <Row label="State" value={user.state} />
        <Row label="Preferred language" value={languageName(user.preferredLanguage)} />
        <Row label="Second language" value={profile.secondaryLanguage ? languageName(profile.secondaryLanguage) : undefined} />
      </Card>
      <Card>
        <CardHeader title="Education" />
        <Row label="Highest" value={EDUCATION_LEVELS.find((e) => e.value === profile.educationLevel)?.label} />
        <Row label="Stream" value={profile.stream} />
        <Row label="Institution" value={profile.institution} />
        <Row label="Year of passing" value={profile.graduationYear ? String(profile.graduationYear) : undefined} />
        <Row label="Experience" value={`${profile.experienceYears} ${profile.experienceYears === 1 ? 'year' : 'years'}`} />
      </Card>
      <Card>
        <CardHeader title="Targets" />
        <AppText variant="label">Exams</AppText>
        <View style={styles.badges}>
          {targets.length ? targets.map((t) => <Badge key={t} label={t} tone="primary" />) : <AppText variant="small">None selected</AppText>}
        </View>
        <AppText variant="label" style={styles.gapTop}>Job roles</AppText>
        <View style={styles.badges}>
          {roles.length ? roles.map((t) => <Badge key={t} label={t} tone="secondary" />) : <AppText variant="small">None selected</AppText>}
        </View>
      </Card>
      <Card>
        <CardHeader title="Resume" />
        {profile.resume ? (
          <ListRow icon="document-text-outline" title={profile.resume.fileName} subtitle={`${profile.resume.sizeKb} KB · added ${formatDate(profile.resume.uploadedAt)}`} />
        ) : (
          <AppText variant="small">No resume added. Adding one makes interview questions specific to your experience.</AppText>
        )}
        <Button title={profile.resume ? 'Replace resume' : 'Add resume'} variant="soft" size="sm" style={styles.gapTop} onPress={() => router.push('/edit-profile')} />
      </Card>

      <Button title="Log out" variant="outline" leftIcon="log-out-outline" onPress={logout} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  identity: { flexDirection: 'row', alignItems: 'center', gap: spacing.lg },
  flex: { flex: 1 },
  plan: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  credits: { alignItems: 'center' },
  links: { paddingVertical: 4 },
  row: { flexDirection: 'row', gap: spacing.md, paddingVertical: 6 },
  rowKey: { width: 130 },
  badges: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, marginTop: 6 },
  gapTop: { marginTop: spacing.md },
});
