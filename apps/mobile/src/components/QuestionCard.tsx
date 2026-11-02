import { Pressable, StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { Answer, Question } from '@prepmitra/shared';
import { colors, paper, radii, spacing } from '@/theme';
import { AppText } from './AppText';
import { Badge } from './Badge';
import { NumericKeypad } from './NumericKeypad';

export interface QuestionCardProps {
  question: Question;
  number: number;
  total: number;
  sectionName?: string;
  marks?: number;
  negativeMarks?: number;
  answer?: Answer;
  onToggleOption: (optionId: string) => void;
  onNumericChange: (value: string) => void;
  marked?: boolean;
  /** `chalk` renders the question on the blackboard (exam focus mode) with OMR-style option bubbles. */
  tone?: 'paper' | 'chalk';
}

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];

/** Renders one exam question with large, accessible option rows or a numeric keypad. */
export function QuestionCard({
  question, number, total, sectionName, marks, negativeMarks, answer, onToggleOption, onNumericChange, marked, tone = 'paper',
}: QuestionCardProps) {
  const chalk = tone === 'chalk';
  const multiple = question.type === 'multiple';
  const selected = answer?.selectedOptionIds ?? [];
  return (
    <View style={styles.wrap}>
      <View style={styles.metaRow}>
        <AppText variant="smallStrong" color={chalk ? colors.warning : colors.primary}>Question {number} of {total}</AppText>
        {marked && <Badge label="Marked" tone="secondary" icon="bookmark" />}
      </View>
      {sectionName ? <AppText variant="caption" numberOfLines={1} color={chalk ? paper.chalkMuted : undefined}>{sectionName}</AppText> : null}
      <View style={styles.badges}>
        <Badge
          label={question.type === 'single' ? 'Single correct' : question.type === 'multiple' ? 'One or more correct' : 'Numeric answer'}
          tone="neutral"
        />
        {marks !== undefined && <Badge label={`+${marks}`} tone="success" />}
        {negativeMarks !== undefined && question.type === 'single' && negativeMarks > 0 && <Badge label={`−${negativeMarks}`} tone="error" />}
      </View>
      <AppText variant="body" style={[styles.text, chalk && styles.textChalk]} accessibilityRole="header" selectable>
        {question.text}
      </AppText>

      {question.type === 'numeric' ? (
        <NumericKeypad value={answer?.numericValue ?? ''} onChange={onNumericChange} />
      ) : (
        <View style={styles.options} accessibilityRole={multiple ? undefined : 'radiogroup'}>
          {question.options?.map((o, i) => {
            const isSel = selected.includes(o.id);
            return (
              <Pressable
                key={o.id}
                onPress={() => onToggleOption(o.id)}
                accessibilityRole={multiple ? 'checkbox' : 'radio'}
                accessibilityState={{ checked: isSel }}
                accessibilityLabel={`Option ${LETTERS[i]}: ${o.text}`}
                style={({ pressed }) => [
                  styles.option,
                  chalk && styles.optionChalk,
                  isSel && (chalk ? styles.optionSelChalk : styles.optionSel),
                  pressed && !isSel && (chalk ? styles.pressedChalk : styles.pressed),
                ]}
              >
                <View style={[styles.letter, chalk && styles.letterChalk, multiple && styles.square, isSel && (chalk ? styles.letterSelChalk : styles.letterSel)]}>
                  {isSel && multiple ? (
                    <Ionicons name="checkmark" size={16} color={colors.white} />
                  ) : (
                    <AppText variant="smallStrong" weight="800" color={isSel ? (chalk ? paper.chalk : colors.white) : chalk ? paper.chalkText : colors.textSecondary}>{LETTERS[i]}</AppText>
                  )}
                </View>
                <AppText variant="body" style={[styles.optionText, chalk && { fontSize: 17 }]} weight={isSel ? '600' : undefined} color={chalk ? (isSel ? colors.white : paper.chalkText) : colors.text}>{o.text}</AppText>
              </Pressable>
            );
          })}
          {multiple && <AppText variant="caption" color={chalk ? paper.chalkMuted : undefined}>Select all options that apply. No negative marking for multiple-correct questions.</AppText>}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: spacing.sm },
  metaRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm },
  badges: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  text: { fontSize: 17, lineHeight: 26, marginTop: spacing.sm, marginBottom: spacing.sm },
  options: { gap: spacing.sm },
  option: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    minHeight: 56,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.md,
    borderRadius: radii.md,
    borderWidth: 1.5,
    borderColor: colors.border,
    backgroundColor: colors.white,
  },
  optionSel: { borderColor: colors.primary, backgroundColor: colors.primarySoft },
  pressed: { backgroundColor: '#F4F3EC' },
  letter: {
    width: 32,
    height: 32,
    borderRadius: 16,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    alignItems: 'center',
    justifyContent: 'center',
  },
  square: { borderRadius: radii.sm },
  letterSel: { backgroundColor: colors.primary, borderColor: colors.primary },
  optionText: { flex: 1 },
  textChalk: { color: paper.chalkText, fontSize: 19, lineHeight: 30 },
  optionChalk: { borderRadius: 16, borderColor: 'rgba(245,243,234,0.25)', backgroundColor: 'rgba(255,255,255,0.03)', minHeight: 58 },
  optionSelChalk: { borderColor: '#F28C28', borderWidth: 2, backgroundColor: 'rgba(242,140,40,0.14)' },
  pressedChalk: { backgroundColor: 'rgba(255,255,255,0.08)' },
  letterChalk: { borderWidth: 2, borderColor: 'rgba(245,243,234,0.6)' },
  letterSelChalk: { backgroundColor: '#F28C28', borderColor: '#F28C28' },
});
