import { Pressable, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import { useUnreadCount } from '@/store/notificationStore';
import { colors, radii, spacing, TOUCH } from '@/theme';
import { AppText } from './AppText';
import { Avatar } from './Avatar';

/**
 * Compact app bar for the Home tab: avatar (opens Profile), a two-line greeting,
 * a credits pill and the notifications bell, like the top of a native app.
 */
export function AppTopBar({ name, greeting, credits }: { name: string; greeting: string; credits?: number }) {
  const unread = useUnreadCount();
  return (
    <View style={styles.row}>
      <Pressable onPress={() => router.push('/profile')} accessibilityRole="button" accessibilityLabel="Open profile" style={({ pressed }) => pressed && styles.pressed}>
        <Avatar name={name} size={42} />
      </Pressable>
      <View style={styles.text}>
        <AppText variant="caption">{greeting}</AppText>
        <AppText variant="h3" numberOfLines={1} accessibilityRole="header">{name.split(' ')[0]}</AppText>
      </View>
      {credits !== undefined && (
        <Pressable
          onPress={() => router.push('/subscription')}
          accessibilityRole="button"
          accessibilityLabel={`${credits} credits. Manage credits.`}
          style={({ pressed }) => [styles.pill, pressed && styles.pressed]}
        >
          <Ionicons name="wallet" size={14} color={colors.primary} />
          <AppText variant="smallStrong" color={colors.primary}>{credits}</AppText>
        </Pressable>
      )}
      <Pressable
        onPress={() => router.push('/notifications')}
        accessibilityRole="button"
        accessibilityLabel={unread ? `Notifications, ${unread} unread` : 'Notifications'}
        style={({ pressed }) => [styles.bell, pressed && styles.pressed]}
      >
        <Ionicons name="notifications-outline" size={22} color={colors.text} />
        {unread > 0 && <View style={styles.dot} />}
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  text: { flex: 1 },
  pill: {
    flexDirection: 'row', alignItems: 'center', gap: 4, height: 34, paddingHorizontal: 12,
    borderRadius: radii.full, backgroundColor: colors.primarySoft,
  },
  bell: {
    width: TOUCH, height: TOUCH, borderRadius: TOUCH / 2, alignItems: 'center', justifyContent: 'center',
    backgroundColor: colors.card, borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border,
  },
  dot: { position: 'absolute', top: 10, right: 11, width: 9, height: 9, borderRadius: 5, backgroundColor: colors.error, borderWidth: 1.5, borderColor: colors.card },
  pressed: { opacity: 0.7 },
});
