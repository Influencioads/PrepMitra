import type { ReactNode } from 'react';
import { KeyboardAvoidingView, Platform, Pressable, ScrollView, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { colors, radii, spacing } from '@/theme';
import { AppText } from './AppText';
import { StudyDeskArt } from './StudyDeskArt';

/** Website auth palette: dark green card border, soft green split, saffron dots. */
export const authColors = {
  panel: '#174A38',
  split: '#A9CDBD',
  dot: '#F28C28',
  text: colors.text,
  muted: colors.textSecondary,
  line: colors.border,
};

/**
 * The website's auth header, sized for a phone: cream | soft-green split, saffron dot grid,
 * and a green-bordered card with the logo, study-desk illustration and the brand headline.
 */
function AuthHero() {
  return (
    <View style={hero.wrap} accessibilityRole="image" accessibilityLabel="PrepMitra AI. Practise like the real exam. Walk in ready.">
      <View style={hero.split} />
      <View style={hero.dots}>
        {Array.from({ length: 8 }, (_, i) => <View key={i} style={hero.dot} />)}
      </View>
      <View style={hero.card}>
        <View style={hero.logoRow}>
          <View style={hero.logo}>
            <Ionicons name="school" size={16} color={colors.white} />
          </View>
          <AppText style={hero.logoText}>
            PrepMitra <AppText style={[hero.logoText, { color: colors.primary }]}>AI</AppText>
          </AppText>
        </View>
        <StudyDeskArt height={118} />
        <AppText align="center" style={hero.headline}>
          {'Practise like the real exam.\n'}<AppText style={[hero.headline, { color: colors.primary }]}>Walk in ready.</AppText>
        </AppText>
      </View>
    </View>
  );
}

export interface AuthShellProps {
  title: string;
  subtitle?: string;
  /** e.g. "Step 1 of 2" — shown as a pill next to the back button. */
  step?: string;
  /** Show the website-style brand header above the title (first screen of a flow). */
  art?: boolean;
  /** Sticky bottom action bar (primary button). */
  footer?: ReactNode;
  children: ReactNode;
}

/**
 * App-style auth screen: back button + step pill on top, big title, form, and the main
 * action pinned to the bottom like a native sign-in flow.
 */
export function AuthShell({ title, subtitle, step, art, footer, children }: AuthShellProps) {
  const insets = useSafeAreaInsets();
  const goBack = () => (router.canGoBack() ? router.back() : router.replace('/welcome'));
  return (
    <View style={[styles.root, { paddingTop: insets.top }]}>
      <View style={styles.topBar}>
        <Pressable
          onPress={goBack}
          accessibilityRole="button"
          accessibilityLabel="Go back"
          hitSlop={8}
          style={({ pressed }) => [styles.back, pressed && styles.pressed]}
        >
          <Ionicons name="chevron-back" size={22} color={colors.text} />
        </Pressable>
        {step ? (
          <View style={styles.step}>
            <AppText variant="caption" weight="600" color={colors.primary}>{step}</AppText>
          </View>
        ) : null}
        <View style={styles.backSpacer} />
      </View>
      <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <ScrollView
          style={styles.flex}
          contentContainerStyle={styles.content}
          keyboardShouldPersistTaps="handled"
          keyboardDismissMode={Platform.OS === 'ios' ? 'interactive' : 'on-drag'}
          showsVerticalScrollIndicator={false}
        >
          {art ? <AuthHero /> : null}
          <View style={styles.head}>
            <AppText variant="h1" accessibilityRole="header">{title}</AppText>
            {subtitle ? <AppText variant="body" color={colors.textSecondary}>{subtitle}</AppText> : null}
          </View>
          {children}
        </ScrollView>
        {footer ? (
          <View style={[styles.footer, { paddingBottom: Math.max(insets.bottom, spacing.md) }]}>{footer}</View>
        ) : null}
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  topBar: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: spacing.lg, paddingVertical: spacing.sm },
  back: {
    width: 44, height: 44, borderRadius: 22, alignItems: 'center', justifyContent: 'center',
    backgroundColor: colors.card, borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border,
  },
  backSpacer: { width: 44, height: 44 },
  pressed: { opacity: 0.7 },
  step: { paddingHorizontal: spacing.md, paddingVertical: 6, borderRadius: radii.full, backgroundColor: colors.primarySoft },
  content: { flexGrow: 1, paddingHorizontal: spacing.lg, paddingBottom: spacing.xl, gap: spacing.lg },
  head: { gap: spacing.sm },
  footer: {
    paddingHorizontal: spacing.lg, paddingTop: spacing.md, gap: spacing.sm, backgroundColor: colors.background,
    borderTopWidth: StyleSheet.hairlineWidth, borderTopColor: colors.border,
  },
});

const hero = StyleSheet.create({
  wrap: {
    borderRadius: 28, overflow: 'hidden', backgroundColor: colors.background, padding: 14, paddingTop: 30,
    borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border,
  },
  split: { position: 'absolute', top: 0, bottom: 0, right: 0, width: '50%', backgroundColor: authColors.split },
  dots: { position: 'absolute', top: 8, left: 12, width: 54, flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  dot: { width: 12, height: 12, borderRadius: 6, backgroundColor: authColors.dot },
  card: {
    alignItems: 'center', gap: spacing.sm, backgroundColor: colors.background, borderRadius: 22,
    borderWidth: 5, borderColor: authColors.panel, paddingHorizontal: spacing.md, paddingTop: spacing.md, paddingBottom: spacing.lg,
  },
  logoRow: { alignSelf: 'flex-start', flexDirection: 'row', alignItems: 'center', gap: 8 },
  logo: { width: 28, height: 28, borderRadius: 8, backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center' },
  logoText: { fontSize: 15, fontWeight: '800', color: colors.text },
  headline: { fontSize: 17, lineHeight: 23, fontWeight: '800', color: authColors.panel },
});
