import { useState } from 'react';
import { Alert, FlatList, Pressable, StyleSheet, View } from 'react-native';
import { Stack, router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { AppNotification } from '@prepmitra/shared';
import { relativeTime } from '@prepmitra/shared';
import { AppText, BottomSheet, Button, EmptyState, IconTile, ListRow, SegmentedControl, toast } from '@/components';
import { notificationService } from '@/services';
import { useNotificationStore } from '@/store';
import { colors, spacing, TOUCH } from '@/theme';
import { NOTIFICATION_ICONS } from '@/utils/icons';
import { toMobileHref } from '@/utils/links';

type Filter = 'all' | 'unread';

export default function Notifications() {
  const items = useNotificationStore((s) => s.items);
  const markRead = useNotificationStore((s) => s.markRead);
  const markUnread = useNotificationStore((s) => s.markUnread);
  const markAllRead = useNotificationStore((s) => s.markAllRead);
  const remove = useNotificationStore((s) => s.remove);
  const [filter, setFilter] = useState<Filter>('all');
  const [menu, setMenu] = useState<AppNotification | null>(null);
  const unread = items.filter((n) => !n.read).length;
  const list = filter === 'unread' ? items.filter((n) => !n.read) : items;

  const open = (n: AppNotification) => {
    if (!n.read) {
      markRead(n.id);
      void notificationService.markRead([n.id]);
    }
    const href = toMobileHref(n.link);
    if (href) router.push(href);
  };
  const readAll = () => {
    const ids = items.filter((n) => !n.read).map((n) => n.id);
    markAllRead();
    void notificationService.markRead(ids);
    toast.success('All notifications marked as read.');
  };
  const del = (n: AppNotification) => {
    setMenu(null);
    remove(n.id);
    void notificationService.remove(n.id);
    toast.info('Notification deleted.');
  };
  const confirmDelete = (n: AppNotification) =>
    Alert.alert('Delete notification?', n.title, [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Delete', style: 'destructive', onPress: () => del(n) },
    ]);

  return (
    <SafeAreaView style={styles.flex} edges={['left', 'right']}>
      <Stack.Screen
        options={{
          headerRight: () =>
            unread > 0 ? (
              <Pressable onPress={readAll} accessibilityRole="button" accessibilityLabel="Mark all as read" style={styles.headerBtn} hitSlop={6}>
                <Ionicons name="checkmark-done" size={22} color={colors.primary} />
              </Pressable>
            ) : null,
        }}
      />
      <FlatList
        data={list}
        keyExtractor={(n) => n.id}
        contentContainerStyle={styles.list}
        ListHeaderComponent={
          <View style={styles.header}>
            <SegmentedControl<Filter>
              accessibilityLabel="Filter notifications"
              value={filter}
              onChange={setFilter}
              segments={[
                { value: 'all', label: `All (${items.length})` },
                { value: 'unread', label: `Unread (${unread})` },
              ]}
            />
            {unread > 0 && <Button title="Mark all as read" variant="ghost" size="sm" leftIcon="checkmark-done" onPress={readAll} style={styles.self} />}
            <AppText variant="caption">Tap to open. Long-press or use ⋯ for more options.</AppText>
          </View>
        }
        ListEmptyComponent={
          <EmptyState
            icon="notifications-off-outline"
            title={filter === 'unread' ? 'You’re all caught up' : 'No notifications'}
            description={filter === 'unread' ? 'No unread notifications.' : 'Results, reminders and receipts will appear here.'}
            actionLabel={filter === 'unread' && items.length > 0 ? 'Show all' : undefined}
            onAction={() => setFilter('all')}
          />
        }
        renderItem={({ item: n }) => (
          <View style={[styles.item, !n.read && styles.unread]}>
            <Pressable
              onPress={() => open(n)}
              onLongPress={() => setMenu(n)}
              accessibilityRole="button"
              accessibilityLabel={`${n.read ? '' : 'Unread. '}${n.title}. ${n.body}. ${relativeTime(n.createdAt)}`}
              accessibilityHint="Opens the related screen. Long-press for options."
              accessibilityActions={[{ name: 'longpress', label: 'More options' }]}
              onAccessibilityAction={(e) => e.nativeEvent.actionName === 'longpress' && setMenu(n)}
              style={({ pressed }) => [styles.itemMain, pressed && styles.pressed]}
            >
              <IconTile name={NOTIFICATION_ICONS[n.type]} tone={n.read ? 'neutral' : 'primary'} size={40} />
              <View style={styles.flex}>
                <View style={styles.titleRow}>
                  <AppText variant={n.read ? 'body' : 'bodyStrong'} style={styles.flex}>{n.title}</AppText>
                  {!n.read && <View style={styles.dot} />}
                </View>
                <AppText variant="small" numberOfLines={3}>{n.body}</AppText>
                <AppText variant="caption">{relativeTime(n.createdAt)}</AppText>
              </View>
            </Pressable>
            <Pressable onPress={() => setMenu(n)} accessibilityRole="button" accessibilityLabel={`More options for ${n.title}`} style={styles.more}>
              <Ionicons name="ellipsis-vertical" size={18} color={colors.textSecondary} />
            </Pressable>
          </View>
        )}
      />

      <BottomSheet visible={!!menu} onClose={() => setMenu(null)} title={menu?.title}>
        {menu && (
          <>
            {toMobileHref(menu.link) && (
              <ListRow icon="open-outline" title="Open" onPress={() => { const n = menu; setMenu(null); open(n); }} />
            )}
            <ListRow
              icon={menu.read ? 'mail-unread-outline' : 'mail-open-outline'}
              title={menu.read ? 'Mark as unread' : 'Mark as read'}
              onPress={() => {
                if (menu.read) markUnread(menu.id);
                else {
                  markRead(menu.id);
                  void notificationService.markRead([menu.id]);
                }
                setMenu(null);
              }}
            />
            <ListRow icon="trash-outline" title="Delete" destructive onPress={() => confirmDelete(menu)} />
          </>
        )}
      </BottomSheet>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  headerBtn: { width: TOUCH, height: TOUCH, alignItems: 'center', justifyContent: 'center' },
  list: { padding: spacing.lg, gap: spacing.sm, paddingBottom: spacing['3xl'] },
  header: { gap: spacing.sm, marginBottom: spacing.sm },
  self: { alignSelf: 'flex-start' },
  item: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: colors.card,
    borderRadius: 14,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: colors.border,
  },
  unread: { backgroundColor: '#FFF6EE', borderColor: '#F6C9A6' },
  itemMain: { flex: 1, flexDirection: 'row', gap: spacing.md, padding: spacing.md },
  pressed: { opacity: 0.7 },
  titleRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  dot: { width: 9, height: 9, borderRadius: 5, backgroundColor: colors.primary },
  more: { width: TOUCH, height: TOUCH + 8, alignItems: 'center', justifyContent: 'center' },
});
