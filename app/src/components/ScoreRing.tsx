import { StyleSheet, View } from 'react-native';
import Svg, { Circle } from 'react-native-svg';
import { colors, toneColors, accuracyTone } from '@/theme';
import { AppText } from './AppText';

export interface ScoreRingProps {
  /** 0–100 */
  percent: number;
  size?: number;
  stroke?: number;
  label?: string;
  sublabel?: string;
  color?: string;
}

/** Circular progress drawn with react-native-svg. */
export function ScoreRing({ percent, size = 148, stroke = 12, label, sublabel, color }: ScoreRingProps) {
  const pct = Math.max(0, Math.min(100, percent));
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const tone = accuracyTone(pct);
  const ringColor = color ?? (tone === 'warning' ? colors.warning : toneColors[tone].fg);
  return (
    <View
      style={{ width: size, height: size }}
      accessible
      accessibilityRole="image"
      accessibilityLabel={`${label ?? `${Math.round(pct)}%`}${sublabel ? `, ${sublabel}` : ''}`}
    >
      <Svg width={size} height={size}>
        <Circle cx={size / 2} cy={size / 2} r={r} stroke="#E2E8F0" strokeWidth={stroke} fill="none" />
        <Circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          stroke={ringColor}
          strokeWidth={stroke}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={`${c} ${c}`}
          strokeDashoffset={c * (1 - pct / 100)}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
      </Svg>
      <View style={[StyleSheet.absoluteFill, styles.center]}>
        <AppText variant="h1" style={{ fontSize: size * 0.2, lineHeight: size * 0.25 }}>{label ?? `${Math.round(pct)}%`}</AppText>
        {sublabel ? <AppText variant="caption" align="center">{sublabel}</AppText> : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  center: { alignItems: 'center', justifyContent: 'center', padding: 16 },
});
