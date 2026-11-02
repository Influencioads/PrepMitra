import { StyleSheet, View } from 'react-native';
import { colors, radii, toneColors, type Tone } from '@/theme';
import { AppText } from './AppText';

export interface ProgressBarProps {
  value: number;
  max?: number;
  tone?: Tone;
  label?: string;
  showValue?: boolean;
  valueLabel?: string;
  size?: 'sm' | 'md';
}

export function ProgressBar({ value, max = 100, tone = 'primary', label, showValue, valueLabel, size = 'md' }: ProgressBarProps) {
  const pct = max > 0 ? Math.max(0, Math.min(100, (value / max) * 100)) : 0;
  const fill = tone === 'neutral' ? colors.textSecondary : tone === 'warning' ? colors.warning : toneColors[tone].fg;
  return (
    <View
      accessible
      accessibilityRole="progressbar"
      accessibilityLabel={label}
      accessibilityValue={{ min: 0, max, now: Math.round(value), text: valueLabel }}
      style={styles.wrap}
    >
      {(label || showValue) && (
        <View style={styles.row}>
          {label ? <AppText variant="small" color={colors.text} style={styles.label} numberOfLines={1}>{label}</AppText> : <View />}
          {showValue && <AppText variant="smallStrong">{valueLabel ?? `${Math.round(value)}%`}</AppText>}
        </View>
      )}
      <View style={[styles.track, { height: size === 'sm' ? 6 : 10 }]}>
        <View style={[styles.fill, { width: `${pct}%`, backgroundColor: fill }]} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 6 },
  row: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', gap: 8 },
  label: { flex: 1 },
  track: { backgroundColor: '#E2E8F0', borderRadius: radii.full, overflow: 'hidden' },
  fill: { height: '100%', borderRadius: radii.full },
});
