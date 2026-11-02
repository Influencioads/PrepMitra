import { useEffect, useState, type ReactNode } from 'react';
import {
  Animated, Easing, KeyboardAvoidingView, Modal, Pressable, ScrollView, StyleSheet, useWindowDimensions, View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Ionicons from '@expo/vector-icons/Ionicons';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import { colors, radii, shadows, spacing, TOUCH } from '@/theme';
import { AppText } from './AppText';

export interface BottomSheetProps {
  visible: boolean;
  onClose: () => void;
  title?: string;
  subtitle?: string;
  children: ReactNode;
  footer?: ReactNode;
  /** Max height as a fraction of the window (default 0.85). */
  maxHeightRatio?: number;
  /** Set false when the content manages its own scrolling (e.g. a FlatList). */
  scroll?: boolean;
  dismissable?: boolean;
}

/**
 * Modal-based bottom sheet: dimmed backdrop, slide-up animation and
 * safe-area bottom padding. Works in Expo Go without extra native modules.
 */
export function BottomSheet({
  visible, onClose, title, subtitle, children, footer, maxHeightRatio = 0.85, scroll = true, dismissable = true,
}: BottomSheetProps) {
  const insets = useSafeAreaInsets();
  const { height } = useWindowDimensions();
  const [mounted, setMounted] = useState(visible);
  const [progress] = useState(() => new Animated.Value(0));
  const reduceMotion = useReducedMotion();

  useEffect(() => {
    if (visible) {
      setMounted(true);
      Animated.timing(progress, { toValue: 1, duration: reduceMotion ? 0 : 260, easing: Easing.out(Easing.cubic), useNativeDriver: true }).start();
    } else if (mounted) {
      Animated.timing(progress, { toValue: 0, duration: reduceMotion ? 0 : 200, easing: Easing.in(Easing.cubic), useNativeDriver: true }).start(
        ({ finished }) => {
          if (finished) setMounted(false);
        },
      );
    }
  }, [visible, mounted, progress, reduceMotion]);

  const close = () => {
    if (dismissable) onClose();
  };
  const translateY = progress.interpolate({ inputRange: [0, 1], outputRange: [height, 0] });

  return (
    <Modal visible={mounted} transparent animationType="none" onRequestClose={close} statusBarTranslucent navigationBarTranslucent>
      <KeyboardAvoidingView behavior="padding" style={styles.fill}>
        <Animated.View style={[StyleSheet.absoluteFill, styles.backdrop, { opacity: progress }]}>
          <Pressable
            style={styles.fill}
            onPress={close}
            accessibilityRole="button"
            accessibilityLabel="Close"
            importantForAccessibility={dismissable ? 'yes' : 'no'}
          />
        </Animated.View>
        <View style={styles.anchor} pointerEvents="box-none">
          <Animated.View
            accessibilityViewIsModal
            style={[styles.sheet, { maxHeight: height * maxHeightRatio, paddingBottom: Math.max(insets.bottom, spacing.lg), transform: [{ translateY }] }]}
          >
            <View style={styles.handle} />
            {(title || dismissable) && (
              <View style={styles.header}>
                <View style={styles.headerText}>
                  {title ? <AppText variant="h3" accessibilityRole="header">{title}</AppText> : null}
                  {subtitle ? <AppText variant="small">{subtitle}</AppText> : null}
                </View>
                {dismissable && (
                  <Pressable onPress={onClose} accessibilityRole="button" accessibilityLabel="Close" style={styles.close} hitSlop={6}>
                    <Ionicons name="close" size={22} color={colors.textSecondary} />
                  </Pressable>
                )}
              </View>
            )}
            {scroll ? (
              <ScrollView
                style={styles.content}
                contentContainerStyle={styles.contentInner}
                keyboardShouldPersistTaps="handled"
                showsVerticalScrollIndicator={false}
              >
                {children}
              </ScrollView>
            ) : (
              <View style={[styles.content, styles.contentInner, styles.flexShrink]}>{children}</View>
            )}
            {footer ? <View style={styles.footer}>{footer}</View> : null}
          </Animated.View>
        </View>
      </KeyboardAvoidingView>
    </Modal>
  );
}

const styles = StyleSheet.create({
  fill: { flex: 1 },
  backdrop: { backgroundColor: 'rgba(15, 23, 42, 0.5)' },
  anchor: { flex: 1, justifyContent: 'flex-end' },
  sheet: {
    backgroundColor: colors.card,
    borderTopLeftRadius: radii.xl,
    borderTopRightRadius: radii.xl,
    paddingTop: spacing.sm,
    ...shadows.overlay,
  },
  handle: { alignSelf: 'center', width: 40, height: 4, borderRadius: 2, backgroundColor: colors.borderStrong, marginBottom: spacing.sm },
  header: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing.lg, gap: spacing.sm },
  headerText: { flex: 1, gap: 2 },
  close: { width: TOUCH, height: TOUCH, alignItems: 'center', justifyContent: 'center', marginRight: -10 },
  content: { flexGrow: 0 },
  flexShrink: { flexShrink: 1 },
  contentInner: { paddingHorizontal: spacing.lg, paddingTop: spacing.sm, paddingBottom: spacing.md, gap: spacing.md },
  footer: { paddingHorizontal: spacing.lg, paddingTop: spacing.sm, gap: spacing.sm },
});
