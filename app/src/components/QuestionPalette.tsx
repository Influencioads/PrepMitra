import { Pressable, StyleSheet, View } from 'react-native';
import type { PaletteStatus, PaperQuestion, QuestionState } from '@prepmitra/shared';
import { PALETTE_LEGEND, countPaletteStatuses, getPaletteStatus } from '@prepmitra/shared';
import { colors, paletteColors, radii, spacing } from '@/theme';
import { AppText } from './AppText';

const ORDER: PaletteStatus[] = ['answered', 'not-answered', 'not-visited', 'marked', 'answered-marked'];

export function PaletteLegend({ counts }: { counts?: Record<PaletteStatus, number> }) {
  return (
    <View style={styles.legend}>
      {ORDER.map((s) => (
        <View key={s} style={styles.legendItem} accessible accessibilityLabel={`${PALETTE_LEGEND[s]}${counts ? `: ${counts[s]}` : ''}`}>
          <View style={[styles.swatch, { backgroundColor: paletteColors[s].bg, borderColor: paletteColors[s].border }]}>
            {counts ? <AppText variant="caption" weight="700" color={paletteColors[s].fg}>{counts[s]}</AppText> : null}
          </View>
          <AppText variant="caption" color={colors.text} style={styles.legendText}>{PALETTE_LEGEND[s]}</AppText>
        </View>
      ))}
    </View>
  );
}

export interface QuestionPaletteProps {
  paper: PaperQuestion[];
  states: Record<string, QuestionState>;
  currentIndex: number;
  sectionNames: Record<string, string>;
  onJump: (index: number) => void;
}

/** CBT-style palette: five statuses, legend with counts, grouped by section. */
export function QuestionPalette({ paper, states, currentIndex, sectionNames, onJump }: QuestionPaletteProps) {
  const counts = countPaletteStatuses(paper.map((p) => p.questionId), states);
  const sections: { id: string; items: { index: number; qid: string }[] }[] = [];
  paper.forEach((p, index) => {
    const last = sections[sections.length - 1];
    if (last && last.id === p.sectionId) last.items.push({ index, qid: p.questionId });
    else sections.push({ id: p.sectionId, items: [{ index, qid: p.questionId }] });
  });

  return (
    <View style={styles.wrap}>
      <PaletteLegend counts={counts} />
      {sections.map((sec) => (
        <View key={sec.id} style={styles.section}>
          <AppText variant="smallStrong" accessibilityRole="header">{sectionNames[sec.id] ?? sec.id}</AppText>
          <View style={styles.grid}>
            {sec.items.map(({ index, qid }) => {
              const status = getPaletteStatus(states[qid]);
              const p = paletteColors[status];
              const current = index === currentIndex;
              return (
                <Pressable
                  key={qid}
                  onPress={() => onJump(index)}
                  accessibilityRole="button"
                  accessibilityLabel={`Question ${index + 1}, ${PALETTE_LEGEND[status]}${current ? ', current' : ''}`}
                  accessibilityState={{ selected: current }}
                  style={[styles.cell, { backgroundColor: p.bg, borderColor: current ? colors.text : p.border }, current && styles.current]}
                >
                  <AppText variant="smallStrong" color={p.fg}>{index + 1}</AppText>
                  {status === 'answered-marked' && <View style={styles.tick} />}
                </Pressable>
              );
            })}
          </View>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: spacing.lg },
  legend: { flexDirection: 'row', flexWrap: 'wrap', rowGap: spacing.sm, columnGap: spacing.md },
  legendItem: { flexDirection: 'row', alignItems: 'center', gap: 6, width: '46%' },
  legendText: { flex: 1 },
  swatch: { minWidth: 26, height: 26, borderRadius: radii.sm, borderWidth: 1, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 4 },
  section: { gap: spacing.sm },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  cell: { width: 48, height: 48, borderRadius: radii.md, borderWidth: 1.5, alignItems: 'center', justifyContent: 'center' },
  current: { borderWidth: 3 },
  tick: { position: 'absolute', top: 4, right: 4, width: 8, height: 8, borderRadius: 4, backgroundColor: colors.success, borderWidth: 1, borderColor: colors.white },
});
