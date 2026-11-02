import { use, type ReactElement, type ReactNode } from 'react';
import {
  KeyboardAvoidingView, Platform, ScrollView, StyleSheet, View, type RefreshControlProps, type StyleProp, type ViewStyle,
} from 'react-native';
import { SafeAreaView, useSafeAreaInsets, type Edge } from 'react-native-safe-area-context';
import { HeaderHeightContext } from 'expo-router/react-navigation';
import { colors, spacing } from '@/theme';

export interface ScreenProps {
  children: ReactNode;
  /** Wrap content in a ScrollView (default true). */
  scroll?: boolean;
  /** Safe-area edges to pad. Stack screens with a native header omit "top"; tab screens omit "bottom". */
  edges?: Edge[];
  /** Enable KeyboardAvoidingView for screens with text inputs. */
  keyboard?: boolean;
  padded?: boolean;
  contentStyle?: StyleProp<ViewStyle>;
  refreshControl?: ReactElement<RefreshControlProps>;
  /** Sticky footer (action bar) rendered below the scroll area. */
  footer?: ReactNode;
  /** Fixed content above the scroll area (e.g. search bar). */
  header?: ReactNode;
  backgroundColor?: string;
  testID?: string;
}

export function Screen({
  children, scroll = true, edges = ['left', 'right', 'bottom'], keyboard = false, padded = true, contentStyle, refreshControl,
  footer, header, backgroundColor = colors.background, testID,
}: ScreenProps) {
  const insets = useSafeAreaInsets();
  const headerHeight = use(HeaderHeightContext) ?? 0;
  const wantsBottom = edges.includes('bottom');
  const safeEdges = edges.filter((e) => e !== 'bottom');
  const bottomPad = wantsBottom && !footer ? insets.bottom : 0;

  const body = scroll ? (
    <ScrollView
      style={styles.flex}
      contentContainerStyle={[padded && styles.padded, { paddingBottom: (padded ? spacing['2xl'] : 0) + bottomPad }, contentStyle]}
      keyboardShouldPersistTaps="handled"
      keyboardDismissMode={Platform.OS === 'ios' ? 'interactive' : 'on-drag'}
      refreshControl={refreshControl}
      showsVerticalScrollIndicator={false}
    >
      {children}
    </ScrollView>
  ) : (
    <View style={[styles.flex, padded && styles.padded, { paddingBottom: (padded ? spacing.lg : 0) + bottomPad }, contentStyle]}>
      {children}
    </View>
  );

  const inner = (
    <>
      {header}
      {body}
      {footer ? (
        <View style={[styles.footer, { paddingBottom: wantsBottom ? Math.max(insets.bottom, spacing.md) : spacing.md }]}>{footer}</View>
      ) : null}
    </>
  );

  return (
    <SafeAreaView edges={safeEdges} style={[styles.flex, { backgroundColor }]} testID={testID}>
      {keyboard ? (
        <KeyboardAvoidingView
          style={styles.flex}
          behavior="padding"
          keyboardVerticalOffset={headerHeight}
        >
          {inner}
        </KeyboardAvoidingView>
      ) : (
        inner
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  padded: { padding: spacing.lg, gap: spacing.lg },
  footer: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    backgroundColor: colors.card,
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: colors.border,
    gap: spacing.sm,
  },
});
