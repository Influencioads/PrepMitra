import { StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { Exam } from '@prepmitra/shared';
import { categoryLabel, pluralize } from '@prepmitra/shared';
import { colors, spacing } from '@/theme';
import { CATEGORY_ICONS } from '@/utils/icons';
import { AppText } from './AppText';
import { Badge } from './Badge';
import { Card } from './Card';
import { IconTile } from './IconTile';

const DIFFICULTY_TONE = { Easy: 'success', Moderate: 'warning', Hard: 'error' } as const;

export function ExamCard({ exam, onPress, freeTrialAvailable }: { exam: Exam; onPress: () => void; freeTrialAvailable?: boolean }) {
  const demoQs = exam.sections.length * exam.demo.questionsPerSection;
  const free = exam.isFree && freeTrialAvailable;
  return (
    <Card
      onPress={onPress}
      accessibilityLabel={`${exam.title}. ${exam.difficulty}. ${exam.durationMin} minutes. ${free ? 'Free trial' : pluralize(exam.creditCost, 'credit')}.`}
      accessibilityHint="Opens exam details"
      style={styles.card}
    >
      <View style={styles.top}>
        <IconTile name={CATEGORY_ICONS[exam.category]} tone="primary" size={44} />
        <View style={styles.titleWrap}>
          <AppText variant="caption">{categoryLabel(exam.category)} · {exam.conductingBody}</AppText>
          <AppText variant="bodyStrong" numberOfLines={2}>{exam.title}</AppText>
        </View>
        <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
      </View>
      <AppText variant="small" numberOfLines={2}>{exam.description}</AppText>
      <View style={styles.badges}>
        <Badge label={exam.difficulty} tone={DIFFICULTY_TONE[exam.difficulty]} />
        <Badge label={`${exam.durationMin} min`} icon="time-outline" />
        <Badge label={`${exam.totalQuestions} Qs`} icon="help-circle-outline" />
        <Badge label={free ? 'Free trial' : pluralize(exam.creditCost, 'credit')} tone={free ? 'success' : 'primary'} icon="wallet-outline" />
      </View>
      <View style={styles.meta}>
        <Ionicons name="star" size={14} color={colors.warning} />
        <AppText variant="caption" color={colors.text}>{exam.rating.toFixed(1)}</AppText>
        <AppText variant="caption">· {exam.attemptsCount.toLocaleString('en-IN')} attempts · demo {demoQs} Qs / {exam.demo.durationMin} min</AppText>
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  card: { gap: spacing.md },
  top: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  titleWrap: { flex: 1, gap: 2 },
  badges: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  meta: { flexDirection: 'row', alignItems: 'center', gap: 4, flexWrap: 'wrap' },
});
