import type { ReactNode } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import { useUnreadCount } from '@/store/notificationStore';
import { colors, spacing, TOUCH } from '@/theme';
import { AppText } from './AppText';

/** Large title header for tab screens, with a notifications bell. */
export function TabHeader({ title, subtitle, right, eyebrow }: { title: string; subtitle?: string; right?: ReactNode; eyebrow?: ReactNode }) {
  const unread = useUnreadCount();
  return (
    <View style={styles.row}>
      <View style={styles.text}>
        {eyebrow}
        <AppText variant="h1" accessibilityRole="header" numberOfLines={2}>{title}</AppText>
        {subtitle ? <AppText variant="small">{subtitle}</AppText> : null}
      </View>
      {right}
      <Pressable
        onPress={() => router.push('/notifications')}
        accessibilityRole="button"
        accessibilityLabel={unread ? `Notifications, ${unread} unread` : 'Notifications'}
        style={({ pressed }) => [styles.bell, pressed && styles.pressed]}
      >
        <Ionicons name="notifications-outline" size={24} color={colors.text} />
        {unread > 0 && (
          <View style={styles.badge}>
            <AppText style={styles.badgeText}>{unread > 9 ? '9+' : unread}</AppText>
          </View>
        )}
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'flex-start', gap: spacing.sm },
  text: { flex: 1, gap: 4 },
  bell: { width: TOUCH, height: TOUCH, alignItems: 'center', justifyContent: 'center', borderRadius: TOUCH / 2, backgroundColor: colors.card, borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border },
  pressed: { opacity: 0.7 },
  badge: { position: 'absolute', top: 4, right: 2, minWidth: 18, height: 18, borderRadius: 9, backgroundColor: colors.error, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 4 },
  badgeText: { color: colors.white, fontSize: 10, fontWeight: '700' },
});
