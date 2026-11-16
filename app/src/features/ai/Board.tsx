import type { ReactNode } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View, type StyleProp, type TextStyle, type ViewStyle } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import Svg, { Circle, G, Line, Path, Polygon, Text as SvgText } from 'react-native-svg';
import type { McqOption, PersonaTrait, TraitScores } from '@prepmitra/shared';
import { AppText, Mitra } from '@/components';
import { colors, fonts, paper, radii, spacing, TOUCH } from '@/theme';
import type { IoniconName } from '@/utils/icons';

/**
 * Redesign building blocks shared by the AI screens (persona, blackboard tutor, doubt solver, teach-back, cheat codes):
 * the chalkboard in its wooden frame, Mitra's small uppercase labels, sticky notes, handwritten kickers and the
 * seating diagram. Handwriting (Kalam) is for short notes only; numbers that matter keep the regular type.
 */

export const board = {
  saffron: '#E8590C',
  saffronSoft: '#FDE7D3',
  stickyPink: '#FDE4E4',
  dashed: 'rgba(245,243,234,0.35)',
};

/** Dark green chalkboard with a brown wooden frame. */
export function Chalkboard({ children, style, innerStyle }: { children: ReactNode; style?: StyleProp<ViewStyle>; innerStyle?: StyleProp<ViewStyle> }) {
  return (
    <View style={[styles.frame, style]}>
      <View style={[styles.board, innerStyle]}>{children}</View>
    </View>
  );
}

/** "MITRA · AI COACH" style label. `onDark` for the chalkboard. */
export function MitraTag({ label, onDark = true, avatar = true }: { label: string; onDark?: boolean; avatar?: boolean }) {
  return (
    <View style={styles.tagRow}>
      {avatar ? <Mitra size={18} /> : null}
      <Text style={[styles.tag, { color: onDark ? paper.marigold : colors.secondary }]} maxFontSizeMultiplier={1.3}>{label.toUpperCase()}</Text>
    </View>
  );
}

/** Small uppercase caption label. */
export function Label({ children, color = colors.textSecondary, style }: { children: ReactNode; color?: string; style?: StyleProp<TextStyle> }) {
  return <Text style={[styles.label, { color }, style]} maxFontSizeMultiplier={1.3}>{children}</Text>;
}

/** Handwritten text (chalk or pen). */
export function Hand({ children, color = paper.chalkText, size = 17, bold, style }: { children: ReactNode; color?: string; size?: number; bold?: boolean; style?: StyleProp<TextStyle> }) {
  return (
    <Text style={[{ fontFamily: bold ? fonts.handBold : fonts.hand, color, fontSize: size, lineHeight: Math.round(size * 1.38) }, style]} maxFontSizeMultiplier={1.4}>
      {children}
    </Text>
  );
}

/** Handwritten kicker above a section title, e.g. "the evidence —". */
export function Kicker({ children, color = colors.secondary }: { children: ReactNode; color?: string }) {
  return <Hand color={color} size={16}>{children}</Hand>;
}

/** Kicker + bold title + optional caption. */
export function SectionHead({ kicker, title, caption, kickerColor, style }: { kicker?: string; title: string; caption?: string; kickerColor?: string; style?: StyleProp<ViewStyle> }) {
  return (
    <View style={[{ gap: 2 }, style]}>
      {kicker ? <Kicker color={kickerColor}>{kicker}</Kicker> : null}
      <AppText variant="h2" accessibilityRole="header">{title}</AppText>
      {caption ? <AppText variant="caption">{caption}</AppText> : null}
    </View>
  );
}

/** The green "AI-generated…" disclaimer pill. */
export function AiNote({ children, style }: { children: ReactNode; style?: StyleProp<ViewStyle> }) {
  return (
    <View style={[styles.aiNote, style]}>
      <Ionicons name="sparkles-outline" size={13} color={colors.secondary} />
      <AppText variant="caption" color={colors.secondary} style={styles.flex}>{children}</AppText>
    </View>
  );
}

/** A slightly rotated sticky note. */
export function Sticky({ title, children, tone = 'yellow', titleColor, tilt = 0, style }: {
  title?: string; children?: ReactNode; tone?: 'yellow' | 'green' | 'pink'; titleColor?: string; tilt?: number; style?: StyleProp<ViewStyle>;
}) {
  const bg = tone === 'green' ? paper.stickyGreen : tone === 'pink' ? board.stickyPink : paper.stickyYellow;
  return (
    <View style={[styles.sticky, { backgroundColor: bg, transform: [{ rotate: `${tilt}deg` }] }, style]}>
      {title ? <Hand bold color={titleColor ?? paper.pen} size={18}>{title}</Hand> : null}
      {typeof children === 'string' ? <AppText variant="small" color={colors.text}>{children}</AppText> : children}
    </View>
  );
}

/** Mitra's speech on the chalkboard: avatar + dark bubble with the "MITRA · AI COACH" label. */
export function CoachBubble({ children, label = 'Mitra · AI coach', style }: { children: ReactNode; label?: string; style?: StyleProp<ViewStyle> }) {
  return (
    <View style={[styles.coachRow, style]}>
      <Mitra size={34} />
      <View style={styles.coachBubble}>
        <MitraTag label={label} avatar={false} />
        <Hand size={16}>{children}</Hand>
      </View>
    </View>
  );
}

/** A pill on the chalkboard. */
export function ChalkChip({ label }: { label: string }) {
  return (
    <View style={styles.chalkChip}>
      <AppText variant="caption" color={paper.chalkText} weight="600">{label}</AppText>
    </View>
  );
}

/** Horizontally scrolling row of filter chips. */
export function ChipScroller({ children, style }: { children: ReactNode; style?: StyleProp<ViewStyle> }) {
  return (
    <ScrollView horizontal showsHorizontalScrollIndicator={false} style={style} contentContainerStyle={styles.chipScroll}>
      {children}
    </ScrollView>
  );
}

/** Pill chip in the redesign style (dark when selected). Optional count after the label. */
export function Pill({ label, count, selected, onPress, onDark, accessibilityLabel }: {
  label: string; count?: number; selected?: boolean; onPress: () => void; onDark?: boolean; accessibilityLabel?: string;
}) {
  const fg = selected ? (onDark ? paper.ink : colors.white) : onDark ? paper.chalkText : colors.text;
  return (
    <Pressable onPress={onPress} accessibilityRole="button" accessibilityState={{ selected: !!selected }} accessibilityLabel={accessibilityLabel ?? label}
      style={({ pressed }) => [styles.pill, onDark ? styles.pillDark : null, selected ? (onDark ? styles.pillDarkOn : styles.pillOn) : null, pressed && { opacity: 0.8 }]}>
      <AppText variant="small" weight="600" color={fg} numberOfLines={1}>
        {label}{count !== undefined ? <AppText variant="small" color={fg} weight="400">{`  ${count}`}</AppText> : null}
      </AppText>
    </Pressable>
  );
}

export type OptionState = 'idle' | 'selected' | 'correct' | 'wrong' | 'answer';

/** Answer option: lettered circle + text. Correct is green, wrong red, the right answer (after a miss) outlined green. */
export function OptionRow({ option, state = 'idle', onPress, disabled }: { option: McqOption; state?: OptionState; onPress?: () => void; disabled?: boolean }) {
  const tone = state === 'correct' || state === 'answer' ? colors.success : state === 'wrong' ? colors.error : state === 'selected' ? colors.primary : colors.borderStrong;
  const bg = state === 'correct' ? colors.successSoft : state === 'wrong' ? colors.errorSoft : state === 'selected' ? colors.primarySoft : colors.card;
  const icon: IoniconName | null = state === 'correct' || state === 'answer' ? 'checkmark-circle' : state === 'wrong' ? 'close-circle' : null;
  return (
    <Pressable onPress={onPress} disabled={disabled || !onPress} accessibilityRole="radio" accessibilityState={{ selected: state !== 'idle', disabled: !!disabled }}
      accessibilityLabel={`Option ${option.key}: ${option.text}`}
      style={({ pressed }) => [styles.option, { borderColor: tone, backgroundColor: bg }, pressed && { opacity: 0.85 }]}>
      <View style={[styles.optionKey, { borderColor: tone }]}>
        <AppText variant="smallStrong" color={state === 'idle' ? colors.text : tone}>{option.key}</AppText>
      </View>
      <AppText variant="small" color={colors.text} style={styles.flex}>{option.text}</AppText>
      {icon ? <Ionicons name={icon} size={20} color={tone} /> : null}
    </Pressable>
  );
}

// ---------- seating diagram ----------
/** Seat (x, y) for index i of n, clockwise from the top seat 0. */
const seatAt = (i: number, n: number, cx: number, cy: number, r: number) => {
  const a = -Math.PI / 2 + (i * 2 * Math.PI) / n;
  return { x: cx + r * Math.cos(a), y: cy + r * Math.sin(a), a };
};

/**
 * Circular seating diagram. Seat indices go CLOCKWISE from the top seat (0); `placed` maps seat index → letter;
 * `arrow` [from, to] is drawn the short way round, just outside the seats.
 */
export function SeatingDiagram({ seats, placed, arrow, size = 220, onDark = true, center = 'centre' }: {
  seats: number; placed?: Record<string, string>; arrow?: [number, number]; size?: number; onDark?: boolean; center?: string;
}) {
  const cx = size / 2, cy = size / 2;
  const ring = size * 0.33;
  const seatR = size * 0.075;
  const line = onDark ? paper.chalkText : paper.ink;
  const faint = onDark ? 'rgba(245,243,234,0.45)' : colors.borderStrong;
  let arrowPath: string | null = null;
  let head: string | null = null;
  if (arrow && seats > 1) {
    const [from, to] = arrow;
    const diff = (((to - from) % seats) + seats) % seats;
    const clockwise = diff <= seats / 2;
    const R = ring + seatR + 10;
    const s = seatAt(from, seats, cx, cy, R);
    const e = seatAt(to, seats, cx, cy, R);
    arrowPath = `M ${s.x} ${s.y} A ${R} ${R} 0 0 ${clockwise ? 1 : 0} ${e.x} ${e.y}`;
    // Arrowhead along the tangent at the end point.
    const dir = clockwise ? 1 : -1;
    const tx = -Math.sin(e.a) * dir, ty = Math.cos(e.a) * dir;
    const nx = Math.cos(e.a), ny = Math.sin(e.a);
    const L = 9, W = 5;
    head = `${e.x + tx * 2},${e.y + ty * 2} ${e.x - tx * L + nx * W},${e.y - ty * L + ny * W} ${e.x - tx * L - nx * W},${e.y - ty * L - ny * W}`;
  }
  const people = Object.entries(placed ?? {}).map(([k, v]) => `${v} at seat ${Number(k) + 1}`).join(', ');
  return (
    <View accessible accessibilityRole="image" accessibilityLabel={`Round table with ${seats} seats${people ? `: ${people}` : ''}. Seats are numbered clockwise from the top.`}>
      <Svg width={size} height={size}>
        <Circle cx={cx} cy={cy} r={ring * 0.55} stroke={line} strokeWidth={2} fill="none" />
        <SvgText x={cx} y={cy + 4} fontSize={11} fill={onDark ? paper.chalkMuted : colors.textSecondary} textAnchor="middle">{center}</SvgText>
        {Array.from({ length: seats }, (_, i) => {
          const p = seatAt(i, seats, cx, cy, ring);
          const who = placed?.[String(i)];
          return (
            <G key={i}>
              {who ? (
                <>
                  <Circle cx={p.x} cy={p.y} r={seatR} fill={onDark ? paper.chalkText : colors.white} stroke={paper.marigold} strokeWidth={who && arrow && arrow[1] === i ? 3 : 0} />
                  <SvgText x={p.x} y={p.y + 5} fontSize={seatR * 1.05} fontWeight="700" fill={paper.ink} textAnchor="middle">{who}</SvgText>
                </>
              ) : (
                <Circle cx={p.x} cy={p.y} r={seatR} fill="none" stroke={faint} strokeWidth={1.5} strokeDasharray="3 3" />
              )}
            </G>
          );
        })}
        {arrowPath ? <Path d={arrowPath} stroke={paper.marigold} strokeWidth={2.5} fill="none" /> : null}
        {head ? <Polygon points={head} fill={paper.marigold} /> : null}
      </Svg>
    </View>
  );
}

// ---------- trait radar ----------
export const TRAITS: PersonaTrait[] = ['speed', 'accuracy', 'risk', 'stamina', 'recovery', 'consistency'];
export const TRAIT_LABEL: Record<PersonaTrait, string> = {
  speed: 'Speed', accuracy: 'Accuracy', risk: 'Risk-taking', stamina: 'Stamina', recovery: 'Recovery', consistency: 'Consistency',
};

/** Six-axis trait radar: you in saffron (filled), the compared persona dashed green. */
export function TraitRadar({ you, other, size = 260 }: { you?: TraitScores | null; other?: TraitScores | null; size?: number }) {
  const cx = size / 2, cy = size / 2;
  const R = size * 0.32;
  const pt = (i: number, v: number) => {
    const a = -Math.PI / 2 + (i * 2 * Math.PI) / TRAITS.length;
    return { x: cx + R * (v / 100) * Math.cos(a), y: cy + R * (v / 100) * Math.sin(a), a };
  };
  const poly = (s: TraitScores) => TRAITS.map((t, i) => { const p = pt(i, s[t]); return `${p.x},${p.y}`; }).join(' ');
  return (
    <Svg width={size} height={size}>
      {[25, 50, 75, 100].map((lvl) => (
        <Polygon key={lvl} points={TRAITS.map((_, i) => { const p = pt(i, lvl); return `${p.x},${p.y}`; }).join(' ')} fill="none" stroke={colors.border} strokeWidth={1} />
      ))}
      {TRAITS.map((t, i) => {
        const p = pt(i, 100);
        const l = pt(i, 128);
        return (
          <G key={t}>
            <Line x1={cx} y1={cy} x2={p.x} y2={p.y} stroke={colors.border} strokeWidth={1} />
            <SvgText x={l.x} y={l.y + 4} fontSize={11} fill={colors.textSecondary} textAnchor={Math.abs(Math.cos(l.a)) < 0.2 ? 'middle' : Math.cos(l.a) > 0 ? 'start' : 'end'}>
              {TRAIT_LABEL[t]}
            </SvgText>
          </G>
        );
      })}
      {other ? <Polygon points={poly(other)} fill="none" stroke={colors.secondary} strokeWidth={2} strokeDasharray="5 4" /> : null}
      {you ? (
        <>
          <Polygon points={poly(you)} fill="rgba(194,65,12,0.18)" stroke={colors.primary} strokeWidth={2.5} />
          {TRAITS.map((t, i) => { const p = pt(i, you[t]); return <Circle key={t} cx={p.x} cy={p.y} r={3.5} fill={colors.primary} />; })}
        </>
      ) : null}
    </Svg>
  );
}

/** Persona icon (backend sends lucide names) → Ionicons. */
export const PERSONA_ICON: Record<string, IoniconName> = {
  zap: 'flash-outline', target: 'locate-outline', shuffle: 'shuffle-outline', sunrise: 'sunny-outline',
  'trending-up': 'trending-up-outline', 'help-circle': 'help-circle-outline',
};
export const personaIcon = (name?: string): IoniconName => PERSONA_ICON[name ?? ''] ?? 'person-outline';

/** Round badge with an icon, e.g. the persona medal on the chalkboard. */
export function Medal({ icon, size = 72 }: { icon: IoniconName; size?: number }) {
  return (
    <View style={[styles.medal, { width: size, height: size, borderRadius: size / 2 }]} importantForAccessibility="no-hide-descendants">
      <View style={[styles.medalInner, { width: size - 12, height: size - 12, borderRadius: size }]}>
        <Ionicons name={icon} size={size * 0.48} color={colors.primary} />
      </View>
    </View>
  );
}

export const boardStyles = StyleSheet.create({
  dashedRule: { borderBottomWidth: 1, borderStyle: 'dashed', borderBottomColor: board.dashed, marginVertical: spacing.sm },
  paperCard: { backgroundColor: colors.card, borderWidth: 1.5, borderColor: paper.ink, borderRadius: radii.lg, padding: spacing.lg },
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  wrap: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.xs },
});

const styles = StyleSheet.create({
  flex: { flex: 1 },
  frame: { backgroundColor: paper.wood, borderRadius: 18, padding: 7 },
  board: { backgroundColor: paper.chalk, borderRadius: 12, padding: spacing.lg, gap: spacing.sm },
  tagRow: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  tag: { fontSize: 11, fontWeight: '700', letterSpacing: 1 },
  label: { fontSize: 11, fontWeight: '700', letterSpacing: 0.9, textTransform: 'uppercase' },
  aiNote: { flexDirection: 'row', alignItems: 'center', gap: 6, alignSelf: 'flex-start', backgroundColor: colors.secondarySoft, borderRadius: radii.full, paddingHorizontal: 12, paddingVertical: 6 },
  sticky: { padding: spacing.md, borderRadius: 4, gap: 4, shadowColor: '#000', shadowOpacity: 0.08, shadowRadius: 0, shadowOffset: { width: 3, height: 3 }, elevation: 1 },
  coachRow: { flexDirection: 'row', alignItems: 'flex-start', gap: spacing.sm },
  coachBubble: { flex: 1, backgroundColor: paper.chalkDeep, borderRadius: 14, borderTopLeftRadius: 4, padding: spacing.md, gap: 4, borderWidth: 1, borderColor: 'rgba(245,243,234,0.15)' },
  chalkChip: { borderWidth: 1, borderColor: 'rgba(245,243,234,0.3)', backgroundColor: 'rgba(0,0,0,0.18)', borderRadius: radii.full, paddingHorizontal: 10, paddingVertical: 5 },
  chipScroll: { gap: spacing.xs, paddingVertical: 2 },
  pill: { minHeight: TOUCH - 6, justifyContent: 'center', paddingHorizontal: 14, borderRadius: radii.full, borderWidth: 1.5, borderColor: colors.borderStrong, backgroundColor: colors.card },
  pillOn: { backgroundColor: paper.ink, borderColor: paper.ink },
  pillDark: { backgroundColor: 'transparent', borderColor: 'rgba(245,243,234,0.4)' },
  pillDarkOn: { backgroundColor: paper.marigold, borderColor: paper.marigold },
  option: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, borderWidth: 1.5, borderRadius: radii.md, padding: spacing.md, minHeight: TOUCH + 4 },
  optionKey: { width: 30, height: 30, borderRadius: 15, borderWidth: 1.5, alignItems: 'center', justifyContent: 'center' },
  medal: { backgroundColor: paper.marigold, alignItems: 'center', justifyContent: 'center' },
  medalInner: { borderWidth: 2, borderStyle: 'dashed', borderColor: 'rgba(28,35,33,0.5)', alignItems: 'center', justifyContent: 'center' },
});
