import { useEffect, useState, type ReactNode } from 'react';
import { AccessibilityInfo, Animated, Pressable, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Ionicons from '@expo/vector-icons/Ionicons';
import { colors, radii, shadows, spacing } from '@/theme';
import type { IoniconName } from '@/utils/icons';
import { AppText } from './AppText';

type ToastType = 'success' | 'error' | 'info';
interface ToastItem {
  id: number;
  type: ToastType;
  message: string;
}

let nextId = 1;
const listeners = new Set<(t: ToastItem) => void>();
const emit = (type: ToastType, message: string) => {
  const item = { id: nextId++, type, message };
  listeners.forEach((l) => l(item));
};

/** Fire-and-forget in-app toasts. Rendered by <ToastProvider> at the app root. */
export const toast = {
  success: (message: string) => emit('success', message),
  error: (message: string) => emit('error', message),
  info: (message: string) => emit('info', message),
};

const STYLE: Record<ToastType, { icon: IoniconName; bg: string; fg: string }> = {
  success: { icon: 'checkmark-circle', bg: '#14532D', fg: '#DCFCE7' },
  error: { icon: 'alert-circle', bg: '#7F1D1D', fg: '#FEE2E2' },
  info: { icon: 'information-circle', bg: colors.text, fg: '#E2E8F0' },
};

function ToastView({ item, onDone }: { item: ToastItem; onDone: (id: number) => void }) {
  const [anim] = useState(() => new Animated.Value(0));
  useEffect(() => {
    AccessibilityInfo.announceForAccessibility(item.message);
    Animated.timing(anim, { toValue: 1, duration: 200, useNativeDriver: true }).start();
    const t = setTimeout(() => {
      Animated.timing(anim, { toValue: 0, duration: 200, useNativeDriver: true }).start(() => onDone(item.id));
    }, item.type === 'error' ? 4500 : 3000);
    return () => clearTimeout(t);
  }, [anim, item, onDone]);
  const s = STYLE[item.type];
  return (
    <Animated.View
      style={[
        styles.toast,
        { backgroundColor: s.bg, opacity: anim, transform: [{ translateY: anim.interpolate({ inputRange: [0, 1], outputRange: [-16, 0] }) }] },
      ]}
    >
      <Pressable onPress={() => onDone(item.id)} accessibilityRole="button" accessibilityLabel={`${item.message}. Dismiss`} style={styles.row}>
        <Ionicons name={s.icon} size={20} color={s.fg} />
        <AppText variant="smallStrong" color={colors.white} style={styles.flex}>{item.message}</AppText>
      </Pressable>
    </Animated.View>
  );
}

export function ToastProvider({ children }: { children: ReactNode }) {
  const insets = useSafeAreaInsets();
  const [items, setItems] = useState<ToastItem[]>([]);
  useEffect(() => {
    const l = (t: ToastItem) => setItems((prev) => [...prev.slice(-2), t]);
    listeners.add(l);
    return () => {
      listeners.delete(l);
    };
  }, []);
  const remove = (id: number) => setItems((prev) => prev.filter((t) => t.id !== id));
  return (
    <View style={styles.flex}>
      {children}
      <View pointerEvents="box-none" style={[styles.host, { top: insets.top + spacing.sm }]} accessibilityLiveRegion="polite">
        {items.map((t) => (
          <ToastView key={t.id} item={t} onDone={remove} />
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  host: { position: 'absolute', left: spacing.lg, right: spacing.lg, gap: spacing.sm, zIndex: 1000, elevation: 1000 },
  toast: { borderRadius: radii.md, ...shadows.raised },
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, paddingHorizontal: spacing.lg, paddingVertical: spacing.md, minHeight: 48 },
});
