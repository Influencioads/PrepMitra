import { StyleSheet, View } from 'react-native';
import { AppText, ProgressBar } from '@/components';
import { colors, spacing } from '@/theme';

export function Stepper({ steps, current }: { steps: string[]; current: number }) {
  return (
    <View style={styles.wrap} accessible accessibilityLabel={`Step ${current + 1} of ${steps.length}: ${steps[current]}`}>
      <View style={styles.row}>
        <AppText variant="smallStrong" color={colors.primary}>Step {current + 1} of {steps.length}</AppText>
        <AppText variant="small">{steps[current]}</AppText>
      </View>
      <ProgressBar value={current + 1} max={steps.length} size="sm" />
      <View style={styles.dots}>
        {steps.map((s, i) => (
          <View key={s} style={[styles.dot, i <= current && styles.dotOn]} />
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: spacing.sm },
  row: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  dots: { flexDirection: 'row', gap: 6, justifyContent: 'center' },
  dot: { width: 6, height: 6, borderRadius: 3, backgroundColor: colors.borderStrong },
  dotOn: { backgroundColor: colors.primary },
});
