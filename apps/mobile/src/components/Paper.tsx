import type { ReactNode } from 'react';
import { StyleSheet, Text, View, type StyleProp, type ViewStyle } from 'react-native';
import Svg, { Circle, Path } from 'react-native-svg';
import { fonts, paper } from '@/theme';

/**
 * Concept B building blocks for native screens: the answer sheet and the blackboard.
 * Paper + red pen = results and feedback. Chalkboard = Mitra (the AI coach) and focus mode.
 * Handwriting is for short notes only; important numbers keep the regular type scale.
 */

/** Mitra, the AI coach. Decorative unless a label is given. */
export function Mitra({ size = 48, label }: { size?: number; label?: string }) {
  return (
    <View accessible={!!label} accessibilityRole={label ? 'image' : undefined} accessibilityLabel={label} importantForAccessibility={label ? 'yes' : 'no-hide-descendants'}>
      <Svg width={size} height={size} viewBox="0 0 48 48">
        <Circle cx={24} cy={24} r={22} fill="#F28C28" />
        <Circle cx={24} cy={24} r={16.5} fill="none" stroke="#C2410C" strokeWidth={2} strokeDasharray="3 4" />
        <Circle cx={18} cy={21} r={2.6} fill="#1C2321" />
        <Circle cx={30} cy={21} r={2.6} fill="#1C2321" />
        <Path d="M17 29q7 6 14 0" stroke="#1C2321" strokeWidth={2.4} fill="none" strokeLinecap="round" />
      </Svg>
    </View>
  );
}

/** Mitra with a speech bubble. `tone="chalk"` writes on the blackboard. */
export function MitraSays({ children, tone = 'paper', size = 48, style }: { children: ReactNode; tone?: 'paper' | 'chalk'; size?: number; style?: StyleProp<ViewStyle> }) {
  const chalk = tone === 'chalk';
  return (
    <View style={[styles.saysRow, style]}>
      <Mitra size={size} />
      <View style={[styles.bubble, chalk ? styles.bubbleChalk : styles.bubblePaper]}>
        <Text style={[styles.hand, { color: chalk ? paper.chalkText : paper.ink }]} maxFontSizeMultiplier={1.4}>{children}</Text>
      </View>
    </View>
  );
}

/** Ruled notebook paper with the red margin line, drawn behind a screen's content. */
export function NotebookBackground({ margin = 30, spacing = 32, lines = 40 }: { margin?: number; spacing?: number; lines?: number }) {
  return (
    <View style={StyleSheet.absoluteFill} pointerEvents="none" importantForAccessibility="no-hide-descendants">
      {Array.from({ length: lines }, (_, i) => (
        <View key={i} style={[styles.rule, { top: (i + 1) * spacing - 1 }]} />
      ))}
      <View style={[styles.margin, { left: margin }]} />
    </View>
  );
}

/** A score circled in red pen. */
export function PenScore({ score, total, size = 52 }: { score: string; total?: string | number; size?: number }) {
  return (
    <View style={[styles.penRing, { borderRadius: size * 2, paddingHorizontal: size * 0.42, paddingTop: size * 0.18, paddingBottom: size * 0.06 }]} accessible accessibilityLabel={total !== undefined ? `Score ${score} out of ${total}` : `Score ${score}`}>
      <Text style={[styles.penText, { fontSize: size, lineHeight: size * 1.15 }]} maxFontSizeMultiplier={1.2}>
        {score}
        {total !== undefined ? <Text style={{ fontSize: size * 0.46 }}>/{total}</Text> : null}
      </Text>
    </View>
  );
}

/** A rubber stamp, e.g. percentile. */
export function Stamp({ value, label, color = '#1E5E47' }: { value: string; label: string; color?: string }) {
  return (
    <View style={[styles.stamp, { borderColor: color }]} accessible accessibilityLabel={`${label} ${value}`}>
      <Text style={[styles.stampValue, { color }]} maxFontSizeMultiplier={1.2}>{value}</Text>
      <Text style={[styles.stampLabel, { color }]} maxFontSizeMultiplier={1.2}>{label.toUpperCase()}</Text>
    </View>
  );
}

/** A short handwritten note. */
export function PenNote({ children, color = paper.pen, size = 16, align }: { children: ReactNode; color?: string; size?: number; align?: 'left' | 'center' }) {
  return <Text style={[styles.hand, { color, fontSize: size, lineHeight: size * 1.4, textAlign: align }]} maxFontSizeMultiplier={1.4}>{children}</Text>;
}

/** An OMR bubble with a letter. */
export function OmrBubble({ letter, selected, onDark }: { letter: string; selected?: boolean; onDark?: boolean }) {
  const line = onDark ? 'rgba(245,243,234,0.6)' : '#8E9792';
  return (
    <View style={[styles.omr, selected ? styles.omrOn : { borderColor: line }]}>
      <Text style={[styles.omrText, { color: selected ? paper.chalk : onDark ? paper.chalkText : paper.ink }]}>{letter}</Text>
    </View>
  );
}

export interface LeakItem {
  label: string;
  marks: number;
  color: string;
}

/** "Where your marks leaked": stacked bar plus legend. Marks come from code, never from AI. */
export function MarksLeak({ title, items, note }: { title: string; items: LeakItem[]; note?: ReactNode }) {
  const total = items.reduce((s, i) => s + i.marks, 0);
  const fmt = (n: number) => `−${Number.isInteger(n) ? n : n.toFixed(2)}`;
  return (
    <View style={styles.leak}>
      <View style={styles.leakHead}>
        <Text style={styles.leakTitle} maxFontSizeMultiplier={1.4}>{title}</Text>
        <Text style={styles.leakTotal}>{total > 0 ? fmt(total) : '0'}</Text>
      </View>
      {total > 0 ? (
        <View style={styles.leakBar} importantForAccessibility="no-hide-descendants">
          {items.filter((i) => i.marks > 0).map((i) => <View key={i.label} style={{ flex: i.marks, backgroundColor: i.color }} />)}
        </View>
      ) : null}
      <View style={{ gap: 8 }}>
        {items.map((i) => (
          <View key={i.label} style={styles.leakRow}>
            <View style={[styles.swatch, { backgroundColor: i.color }]} />
            <Text style={styles.leakLabel} maxFontSizeMultiplier={1.4}>{i.label}</Text>
            <Text style={styles.leakMarks}>{i.marks > 0 ? fmt(i.marks) : '0'}</Text>
          </View>
        ))}
      </View>
      {note}
    </View>
  );
}

const styles = StyleSheet.create({
  saysRow: { flexDirection: 'row', alignItems: 'flex-start', gap: 10 },
  bubble: { flex: 1, paddingHorizontal: 14, paddingVertical: 10, borderTopLeftRadius: 4, borderTopRightRadius: 18, borderBottomLeftRadius: 18, borderBottomRightRadius: 18 },
  bubblePaper: { backgroundColor: '#FFFEFA', borderWidth: 1.5, borderColor: paper.ink },
  bubbleChalk: { backgroundColor: paper.chalk, borderBottomWidth: 5, borderBottomColor: paper.wood },
  hand: { fontFamily: fonts.hand, fontSize: 16, lineHeight: 22 },
  rule: { position: 'absolute', left: 0, right: 0, height: 1, backgroundColor: paper.rule },
  margin: { position: 'absolute', top: 0, bottom: 0, width: 1.5, backgroundColor: paper.margin },
  penRing: { alignSelf: 'flex-start', borderWidth: 3.5, borderColor: paper.pen, transform: [{ rotate: '-4deg' }] },
  penText: { fontFamily: fonts.handBold, color: paper.pen },
  stamp: { alignSelf: 'flex-start', borderWidth: 2.5, borderRadius: 8, paddingHorizontal: 10, paddingVertical: 5, alignItems: 'center', transform: [{ rotate: '-6deg' }], backgroundColor: 'rgba(251,248,239,0.9)' },
  stampValue: { fontSize: 20, fontWeight: '800', lineHeight: 22 },
  stampLabel: { fontSize: 9, fontWeight: '700', letterSpacing: 1.2 },
  omr: { width: 32, height: 32, borderRadius: 16, borderWidth: 2, alignItems: 'center', justifyContent: 'center' },
  omrOn: { backgroundColor: '#F28C28', borderColor: '#F28C28' },
  omrText: { fontSize: 14, fontWeight: '800' },
  leak: { backgroundColor: '#FFFEFA', borderWidth: 1.5, borderColor: paper.ink, borderRadius: 18, padding: 16, gap: 12 },
  leakHead: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'baseline', gap: 8 },
  leakTitle: { flex: 1, fontSize: 18, fontWeight: '700', color: paper.ink },
  leakTotal: { fontSize: 18, fontWeight: '800', color: paper.pen },
  leakBar: { flexDirection: 'row', height: 16, borderRadius: 8, overflow: 'hidden' },
  leakRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  swatch: { width: 12, height: 12, borderRadius: 3 },
  leakLabel: { flex: 1, fontSize: 14, color: paper.ink },
  leakMarks: { fontSize: 14, fontWeight: '700', color: paper.ink },
});
