import { Pressable, StyleSheet, Text, View } from 'react-native';
import Svg, { Path } from 'react-native-svg';
import Ionicons from '@expo/vector-icons/Ionicons';
import { colors, paper } from '@/theme';

export interface PathStep {
  key: string;
  label: string;
  title: string;
  meta?: string;
  state: 'done' | 'today' | 'locked' | 'goal';
}

const ROW = 96;
const COL_A = 52; // node centre x for even rows
const COL_B = 128; // node centre x for odd rows
const LABEL_X = 176;

/**
 * A winding "prep path": one node per day of the improvement plan. Nodes alternate between two
 * columns on the left and labels sit in a column on the right, so the dotted line never crosses text.
 */
export function PrepPath({ steps, onStart }: { steps: PathStep[]; onStart: () => void }) {
  const cx = (i: number) => (i % 2 === 0 ? COL_A : COL_B);
  const cy = (i: number) => i * ROW + ROW / 2;
  let d = '';
  steps.forEach((_, i) => {
    if (i === 0) {
      d = `M${cx(0)} ${cy(0)}`;
      return;
    }
    const x0 = cx(i - 1), y0 = cy(i - 1), x1 = cx(i), y1 = cy(i);
    d += ` C ${x0} ${y0 + ROW * 0.55}, ${x1} ${y1 - ROW * 0.55}, ${x1} ${y1}`;
  });
  const height = steps.length * ROW;

  return (
    <View style={{ height }} accessibilityRole="list">
      <Svg width={LABEL_X} height={height} style={StyleSheet.absoluteFill} pointerEvents="none">
        <Path d={d} stroke={paper.ink} strokeWidth={3} strokeDasharray="2 10" strokeLinecap="round" fill="none" />
      </Svg>
      {steps.map((s, i) => {
        const today = s.state === 'today';
        const size = today ? 80 : 46;
        const nodeStyle = [
          styles.node,
          { width: size, height: size, borderRadius: size / 2, left: cx(i) - size / 2, top: cy(i) - size / 2 },
          s.state === 'done' && styles.done,
          today && styles.today,
          s.state === 'locked' && styles.locked,
          s.state === 'goal' && styles.goal,
        ];
        const content = (
          <>
            {s.state === 'done' && <Ionicons name="checkmark" size={22} color={colors.white} />}
            {today && <Text style={styles.startText}>START</Text>}
            {s.state === 'locked' && <Text style={styles.lockedText}>{i + 1}</Text>}
            {s.state === 'goal' && <Ionicons name="trophy-outline" size={20} color={colors.primary} />}
          </>
        );
        return (
          <View key={s.key} style={StyleSheet.absoluteFill} pointerEvents="box-none">
            {today ? (
              <Pressable onPress={onStart} accessibilityRole="button" accessibilityLabel={`${s.label}, ${s.title}. Start`} hitSlop={8} style={({ pressed }) => [...nodeStyle, pressed && { opacity: 0.85 }]}>
                {content}
              </Pressable>
            ) : (
              <View style={nodeStyle} importantForAccessibility="no-hide-descendants">{content}</View>
            )}
            <View style={[styles.label, { top: cy(i) - (today ? 34 : 20) }]} accessible accessibilityLabel={`${s.label}, ${s.title}${s.meta ? `, ${s.meta}` : ''}`}>
              <Text style={[styles.dayLabel, today && { color: colors.primary }]} maxFontSizeMultiplier={1.3}>{s.label.toUpperCase()}</Text>
              <Text style={[styles.title, s.state === 'locked' && { color: '#8E9792' }, today && styles.titleToday]} numberOfLines={2} maxFontSizeMultiplier={1.3}>{s.title}</Text>
              {s.meta ? <Text style={styles.meta} maxFontSizeMultiplier={1.3}>{s.meta}</Text> : null}
            </View>
          </View>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  node: { position: 'absolute', alignItems: 'center', justifyContent: 'center' },
  done: { backgroundColor: colors.success, borderBottomWidth: 4, borderBottomColor: '#116632' },
  today: { backgroundColor: colors.primary, borderBottomWidth: 6, borderBottomColor: '#8A2E07', borderWidth: 0 },
  locked: { backgroundColor: '#FFFEFA', borderWidth: 2, borderColor: '#CFCFC3' },
  goal: { backgroundColor: '#FFFEFA', borderWidth: 2, borderColor: colors.primary, borderStyle: 'dashed' },
  startText: { color: colors.white, fontWeight: '800', fontSize: 15 },
  lockedText: { color: '#8E9792', fontWeight: '700' },
  label: { position: 'absolute', left: LABEL_X, right: 0 },
  dayLabel: { fontSize: 11, fontWeight: '700', letterSpacing: 1, color: '#5B6661' },
  title: { fontSize: 14, fontWeight: '600', color: paper.ink, marginTop: 1 },
  titleToday: { fontSize: 17, fontWeight: '800' },
  meta: { fontSize: 12, color: '#5B6661', marginTop: 1 },
});
