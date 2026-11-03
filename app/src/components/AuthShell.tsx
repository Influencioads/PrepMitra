import type { ReactNode } from 'react';
import { KeyboardAvoidingView, Platform, Pressable, ScrollView, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { colors, spacing } from '@/theme';
import { StudyDeskArt } from './StudyDeskArt';

/** Auth palette: the dark green form panel and the soft green right half of the page. */
export const authColors = {
  panel: '#174A38',
  split: '#A9CDBD',
  text: '#F5F3EA',
  muted: 'rgba(245,243,234,0.74)',
  subtle: 'rgba(245,243,234,0.5)',
  line: 'rgba(255,255,255,0.32)',
  link: '#FFAD66',
  error: '#FDA4A4',
  accent: '#F26B1D',
};

/**
 * Auth screen frame (matches the website): split background (cream | soft green), one card
 * with a thick green border — illustration on top, the form on a dark green panel below.
 */
export function AuthShell({ children }: { children: ReactNode }) {
  const insets = useSafeAreaInsets();
  return (
    <View style={styles.root}>
      <View style={styles.split} pointerEvents="none" />
      <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <ScrollView
          style={styles.flex}
          contentContainerStyle={[styles.content, { paddingTop: insets.top + spacing.md }]}
          keyboardShouldPersistTaps="handled"
          keyboardDismissMode={Platform.OS === 'ios' ? 'interactive' : 'on-drag'}
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.card}>
            <View style={styles.art}>
              {router.canGoBack() ? (
                <Pressable
                  onPress={() => router.back()}
                  accessibilityRole="button"
                  accessibilityLabel="Go back"
                  hitSlop={8}
                  style={({ pressed }) => [styles.back, pressed && styles.backPressed]}
                >
                  <Ionicons name="arrow-back" size={20} color={authColors.panel} />
                </Pressable>
              ) : null}
              <StudyDeskArt height={170} />
            </View>
            <View style={[styles.panel, { paddingBottom: insets.bottom + spacing.xl }]}>{children}</View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: colors.background },
  split: { position: 'absolute', top: 0, bottom: 0, right: 0, width: '50%', backgroundColor: authColors.split },
  flex: { flex: 1 },
  content: { flexGrow: 1, paddingHorizontal: 14 },
  card: {
    flexGrow: 1,
    overflow: 'hidden',
    borderWidth: 6,
    borderBottomWidth: 0,
    borderColor: authColors.panel,
    borderTopLeftRadius: 32,
    borderTopRightRadius: 32,
    backgroundColor: authColors.panel,
  },
  art: { alignItems: 'center', justifyContent: 'center', backgroundColor: colors.background, paddingVertical: spacing.lg },
  back: {
    position: 'absolute',
    top: spacing.md,
    left: spacing.md,
    zIndex: 1,
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(23,74,56,0.08)',
  },
  backPressed: { backgroundColor: 'rgba(23,74,56,0.16)' },
  panel: { flexGrow: 1, backgroundColor: authColors.panel, paddingHorizontal: spacing.xl, paddingTop: spacing['2xl'], gap: spacing.lg },
});
