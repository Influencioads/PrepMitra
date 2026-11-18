import type { ReactNode } from 'react';
import { Alert, Platform, Pressable, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import {
  EDUCATION_LEVELS, PLANS, formatDate, getExamById, getRoleById, languageName, maskPhone,
} from '@prepmitra/shared';
import { AppText, Avatar, Badge, Divider, ListRow, Screen } from '@/components';
import { authService } from '@/services';
import { useAuthStore, useProfileStore, useSubscriptionStore, useUnreadCount } from '@/store';
import { colors, radii, spacing } from '@/theme';

/** iOS/Android settings-style group: a small caps label above a rounded list. */
function Group({ title, children }: { title?: string; children: ReactNode }) {
  return (
    <View style={styles.group}>
      {title ? <AppText variant="caption" weight="600" style={styles.groupTitle}>{title.toUpperCase()}</AppText> : null}
      <View style={styles.groupCard}>{children}</View>
    </View>
  );
}

/** Read-only setting row: label on the left, value on the right. */
function ValueRow({ icon, label, value, onPress }: { icon: React.ComponentProps<typeof Ionicons>['name']; label: string; value?: string; onPress?: () => void }) {
  return (
    <Pressable
      onPress={onPress}
      disabled={!onPress}
      accessibilityRole={onPress ? 'button' : undefined}
      accessibilityLabel={`${label}: ${value || 'not set'}`}
      style={({ pressed }) => [styles.valueRow, pressed && styles.pressed]}
    >
      <Ionicons name={icon} size={20} color={colors.textSecondary} />
      <AppText variant="body" style={styles.flex}>{label}</AppText>
      <AppText variant="small" numberOfLines={1} style={styles.value}>{value || 'Add'}</AppText>
      {onPress && <Ionicons name="chevron-forward" size={16} color={colors.textMuted} />}
    </Pressable>
  );
}

export default function Profile() {
  const user = useAuthStore((s) => s.session?.user);
  const signOut = useAuthStore((s) => s.signOut);
  const profile = useProfileStore((s) => s.profile);
  const sub = useSubscriptionStore((s) => s.sub);
  const unread = useUnreadCount();
  const plan = PLANS.find((p) => p.id === sub.planId);

  const doLogout = () => {
    void authService.logout();
    signOut();
  };
  const logout = () => {
    const message = 'Your demo data stays on this device for the next time you log in.';
    // Alert.alert is a no-op on react-native-web, so use the browser's confirm there.
    if (Platform.OS === 'web') {
      if (window.confirm(`Log out?\n\n${message}`)) doLogout();
      return;
    }
    Alert.alert('Log out?', message, [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Log out', style: 'destructive', onPress: doLogout },
    ]);
  };

  if (!user) return null;
  const targets = profile.targetExamIds.map((id) => getExamById(id)?.shortTitle ?? id);
  const roles = profile.targetRoleIds.map((id) => getRoleById(id)?.shortTitle ?? id);
  const edit = () => router.push('/edit-profile');

  return (
    <Screen edges={['top', 'left', 'right']}>
      <View style={styles.topBar}>
        <AppText variant="h1" accessibilityRole="header">Profile</AppText>
        <Pressable onPress={() => router.push('/settings')} accessibilityRole="button" accessibilityLabel="Settings" style={({ pressed }) => [styles.iconBtn, pressed && styles.pressed]}>
          <Ionicons name="settings-outline" size={22} color={colors.text} />
        </Pressable>
      </View>

      {/* Identity header */}
      <View style={styles.identity}>
        <Pressable onPress={edit} accessibilityRole="button" accessibilityLabel="Edit profile photo and details">
          <Avatar name={user.name} size={88} />
          <View style={styles.editBadge}><Ionicons name="pencil" size={14} color={colors.white} /></View>
        </Pressable>
        <AppText variant="h2" numberOfLines={1}>{user.name}</AppText>
        <AppText variant="small">{maskPhone(user.phone)}{user.email ? ` · ${user.email}` : ''}</AppText>
      </View>

      {/* Plan + credits tile */}
      <Pressable
        onPress={() => router.push('/subscription')}
        accessibilityRole="button"
        accessibilityLabel={`${plan?.name ?? 'Plan'}, ${sub.credits} credits. Manage credits and plans.`}
        style={({ pressed }) => [styles.planTile, pressed && styles.pressed]}
      >
        <View style={styles.flex}>
          <AppText variant="caption" color="rgba(255,255,255,0.8)">Current plan</AppText>
          <AppText variant="h3" color={colors.white} numberOfLines={2}>{plan?.name ?? sub.planId}</AppText>
          <AppText variant="caption" color="rgba(255,255,255,0.8)">
            {sub.renewsAt ? `${sub.autoRenew ? 'Renews' : 'Ends'} ${formatDate(sub.renewsAt)}` : sub.freeMiniMockUsed ? 'Pay as you go' : 'Free mini mock available'}
          </AppText>
        </View>
        <View style={styles.creditsBubble}>
          <AppText variant="h2" color={colors.primary}>{sub.credits}</AppText>
          <AppText variant="caption" color={colors.primary}>credits</AppText>
        </View>
      </Pressable>

      <Group>
        <ListRow icon="notifications-outline" title="Notifications" onPress={() => router.push('/notifications')} right={unread > 0 ? <Badge label={`${unread}`} tone="error" /> : undefined} />
        <Divider />
        <ListRow icon="bar-chart-outline" title="My reports" onPress={() => router.push('/reports')} />
        <Divider />
        <ListRow icon="analytics-outline" title="Progress analytics" onPress={() => router.push('/progress')} />
        <Divider />
        <ListRow icon="wallet-outline" title="Credits & plans" onPress={() => router.push('/subscription')} />
      </Group>

      <Group title="Personal details">
        <ValueRow icon="calendar-outline" label="Date of birth" value={user.dob ? formatDate(user.dob) : undefined} onPress={edit} />
        <Divider />
        <ValueRow icon="location-outline" label="State" value={user.state} onPress={edit} />
        <Divider />
        <ValueRow icon="language-outline" label="Language" value={languageName(user.preferredLanguage)} onPress={edit} />
      </Group>

      <Group title="Education">
        <ValueRow icon="school-outline" label="Highest" value={EDUCATION_LEVELS.find((e) => e.value === profile.educationLevel)?.label} onPress={edit} />
        <Divider />
        <ValueRow icon="business-outline" label="Institution" value={profile.institution} onPress={edit} />
        <Divider />
        <ValueRow icon="briefcase-outline" label="Experience" value={`${profile.experienceYears} ${profile.experienceYears === 1 ? 'year' : 'years'}`} onPress={edit} />
        <Divider />
        <ValueRow icon="document-text-outline" label="Resume" value={profile.resume?.fileName} onPress={edit} />
      </Group>

      <Group title="My targets">
        <View style={styles.targets}>
          <AppText variant="caption">Exams</AppText>
          <View style={styles.badges}>
            {targets.length ? targets.map((t) => <Badge key={t} label={t} tone="primary" />) : <AppText variant="small">None selected</AppText>}
          </View>
          <AppText variant="caption" style={styles.gapTop}>Job roles</AppText>
          <View style={styles.badges}>
            {roles.length ? roles.map((t) => <Badge key={t} label={t} tone="secondary" />) : <AppText variant="small">None selected</AppText>}
          </View>
        </View>
      </Group>

      <Group>
        <ListRow icon="settings-outline" title="Settings & privacy" onPress={() => router.push('/settings')} />
        <Divider />
        <ListRow icon="log-out-outline" title="Log out" destructive onPress={logout} chevron={false} />
      </Group>
    </Screen>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  pressed: { opacity: 0.75 },
  topBar: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  iconBtn: { width: 44, height: 44, borderRadius: 22, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card, borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border },
  identity: { alignItems: 'center', gap: 4 },
  editBadge: {
    position: 'absolute', right: 0, bottom: 0, width: 28, height: 28, borderRadius: 14, backgroundColor: colors.text,
    alignItems: 'center', justifyContent: 'center', borderWidth: 2, borderColor: colors.background,
  },
  planTile: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.lg, borderRadius: radii.xl, backgroundColor: colors.primary },
  creditsBubble: { width: 72, height: 72, borderRadius: 36, backgroundColor: colors.white, alignItems: 'center', justifyContent: 'center' },
  group: { gap: 6 },
  groupTitle: { marginLeft: spacing.md, letterSpacing: 0.6 },
  groupCard: {
    backgroundColor: colors.card, borderRadius: radii.xl, paddingHorizontal: spacing.md, paddingVertical: 2,
    borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border,
  },
  valueRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, minHeight: 52 },
  value: { maxWidth: '45%', textAlign: 'right' },
  targets: { paddingVertical: spacing.md },
  badges: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, marginTop: 6 },
  gapTop: { marginTop: spacing.md },
});
