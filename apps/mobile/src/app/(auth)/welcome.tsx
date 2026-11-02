import { StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import { APP_TAGLINE, DISCLAIMERS, HERO_HEADLINE } from '@prepmitra/shared';
import { AppText, Button, Screen } from '@/components';
import { BrandMark } from '@/features/brand/BrandMark';
import { colors, radii, spacing } from '@/theme';
import type { IoniconName } from '@/utils/icons';

const FEATURES: { icon: IoniconName; title: string; body: string }[] = [
  { icon: 'document-text-outline', title: 'Real-pattern mock exams', body: 'SSC, banking, railway, UPSC, CAT, GATE and placement papers.' },
  { icon: 'chatbubbles-outline', title: 'Mock interviews', body: 'Text or voice practice with model answers and a score card.' },
  { icon: 'analytics-outline', title: 'Reports that teach', body: 'Topic accuracy, marks lost, shortcuts and a 7-day plan.' },
  { icon: 'language-outline', title: '23 Indian languages', body: 'Switch any question to English when you need to.' },
];

export default function Welcome() {
  return (
    <Screen
      edges={['top', 'left', 'right', 'bottom']}
      footer={
        <>
          <Button title="Get started" size="lg" fullWidth rightIcon="arrow-forward" onPress={() => router.push('/signup')} />
          <Button title="I already have an account — Log in" variant="ghost" fullWidth onPress={() => router.push('/login')} />
        </>
      }
    >
      <View style={styles.hero}>
        <BrandMark size={44} />
        <AppText variant="smallStrong" color={colors.primary} style={styles.tagline}>{APP_TAGLINE}</AppText>
        <AppText variant="display" accessibilityRole="header">{HERO_HEADLINE}</AppText>
        <AppText variant="body" color={colors.textSecondary}>
          Practise with exam-pattern mocks and mock interviews, then follow a personal plan built from your own answers.
        </AppText>
      </View>
      <View style={styles.features}>
        {FEATURES.map((f) => (
          <View key={f.title} style={styles.feature}>
            <View style={styles.icon}>
              <Ionicons name={f.icon} size={22} color={colors.primary} />
            </View>
            <View style={styles.flex}>
              <AppText variant="bodyStrong">{f.title}</AppText>
              <AppText variant="small">{f.body}</AppText>
            </View>
          </View>
        ))}
      </View>
      <AppText variant="caption" align="center">{DISCLAIMERS.examAffiliation}</AppText>
    </Screen>
  );
}

const styles = StyleSheet.create({
  hero: { gap: spacing.md, paddingTop: spacing.xl },
  tagline: { marginTop: spacing.md },
  features: { gap: spacing.md, marginTop: spacing.sm },
  feature: { flexDirection: 'row', gap: spacing.md, alignItems: 'center' },
  icon: { width: 44, height: 44, borderRadius: radii.md, backgroundColor: colors.primarySoft, alignItems: 'center', justifyContent: 'center' },
  flex: { flex: 1 },
});
