import { useState, type ComponentProps } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import { Stack, router, useLocalSearchParams } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import { DISCLAIMERS, categoryLabel, languageName, pluralize } from '@prepmitra/shared';
import {
  AppText, Badge, Button, Card, CardHeader, Divider, ErrorState, IconTile, LoadingSkeleton, Notice, Screen,
} from '@/components';
import { useAsync } from '@/hooks/useAsync';
import { examService } from '@/services';
import { examCreditCost, selectInProgress, useExamStore, useSubscriptionStore } from '@/store';
import { colors, radii, spacing } from '@/theme';
import { CATEGORY_ICONS } from '@/utils/icons';

const TYPE_LABEL = { single: 'Single correct', multiple: 'Multiple correct (MSQ)', numeric: 'Numeric answer (NAT)' } as const;
const LETTERS = ['A', 'B', 'C', 'D', 'E'];

export default function ExamDetails() {
  const { id = '' } = useLocalSearchParams<{ id: string }>();
  const { data: exam, loading, error, reload } = useAsync(() => examService.get(id), id);
  const sub = useSubscriptionStore((s) => s.sub);
  const attempts = useExamStore((s) => s.attempts);
  const [picked, setPicked] = useState<number | null>(null);

  if (loading) return <Screen><LoadingSkeleton /></Screen>;
  if (error || !exam) return <Screen><ErrorState title="Exam not available" description={error ?? 'This exam could not be loaded.'} onRetry={reload} /></Screen>;

  const { cost, usesFreeTrial } = examCreditCost(exam, sub);
  const resumable = selectInProgress(attempts).find((a) => a.examId === exam.id);
  const demoQs = exam.sections.length * exam.demo.questionsPerSection;
  const sample = exam.sampleQuestion;
  const correct = picked !== null && picked === sample.answerIndex;

  return (
    <Screen
      footer={
        <View style={styles.footer}>
          <View style={styles.flex}>
            <AppText variant="bodyStrong">{usesFreeTrial ? 'Free trial' : pluralize(cost, 'credit')}</AppText>
            <AppText variant="caption">You have {pluralize(sub.credits, 'credit')}</AppText>
          </View>
          {resumable ? (
            <Button title="Resume attempt" leftIcon="play" onPress={() => router.push(`/exam/${resumable.id}`)} />
          ) : (
            <Button title="Start mock" leftIcon="play" onPress={() => router.push(`/exams/${exam.id}/instructions`)} />
          )}
        </View>
      }
    >
      <Stack.Screen options={{ title: exam.shortTitle }} />
      <View style={styles.head}>
        <IconTile name={CATEGORY_ICONS[exam.category]} size={52} />
        <View style={styles.flex}>
          <AppText variant="caption">{categoryLabel(exam.category)} · {exam.conductingBody}</AppText>
          <AppText variant="h2" accessibilityRole="header">{exam.title}</AppText>
        </View>
      </View>
      <View style={styles.badges}>
        <Badge label={exam.difficulty} tone={exam.difficulty === 'Easy' ? 'success' : exam.difficulty === 'Hard' ? 'error' : 'warning'} />
        <Badge label={`${exam.sections.length} sections`} icon="layers-outline" />
        {exam.isFree && <Badge label="Free mini mock" tone="success" />}
      </View>
      <AppText variant="body" color={colors.textSecondary}>{exam.description}</AppText>
      {[`${exam.sections.length} sections · ${exam.totalQuestions} questions`, 'Section-wise report after you submit', `Available in ${exam.languages.length} languages`].map((h) => (
        <View key={h} style={styles.highlight}>
          <Ionicons name="checkmark-circle" size={18} color={colors.success} />
          <AppText variant="small" color={colors.text} style={styles.flex}>{h}</AppText>
        </View>
      ))}

      <Card>
        <CardHeader title="Exam pattern" subtitle={`Full exam: ${exam.totalQuestions} questions · ${exam.totalMarks} marks · ${exam.durationMin} min`} />
        <View style={styles.facts}>
          <Fact icon="time-outline" label="Demo duration" value={`${exam.demo.durationMin} min`} />
          <Fact icon="help-circle-outline" label="Demo questions" value={String(demoQs)} />
          <Fact icon="language-outline" label="Languages" value={String(exam.languages.length)} />
          <Fact icon="calculator-outline" label="Calculator" value={exam.calculatorAllowed ? 'Allowed' : 'No'} />
        </View>
        <AppText variant="small" style={styles.gapTop}>Question types: {exam.questionTypes.map((t) => TYPE_LABEL[t]).join(', ')}</AppText>
      </Card>

      <Card>
        <CardHeader title="Sections and marking" />
        {exam.sections.map((s, i) => (
          <View key={s.id}>
            {i > 0 && <Divider />}
            <View style={styles.section}>
              <View style={styles.flex}>
                <AppText variant="bodyStrong">{s.name}</AppText>
                <AppText variant="caption">{s.questionCount} questions in the full exam · {exam.demo.questionsPerSection} in demo</AppText>
              </View>
              <View style={styles.marks}>
                <AppText variant="smallStrong" color={colors.success}>+{s.marksPerQuestion}</AppText>
                <AppText variant="smallStrong" color={s.negativeMarks > 0 ? colors.error : colors.textSecondary}>
                  {s.negativeMarks > 0 ? `−${s.negativeMarks}` : '0'}
                </AppText>
              </View>
            </View>
          </View>
        ))}
        <Notice tone="info" style={styles.gapTop}>{`${exam.negativeMarking}. Multiple-correct and numeric answers have no negative marking.`}</Notice>
      </Card>

      <Card>
        <CardHeader title="Try a sample question" subtitle="Tap an option to check your answer" />
        <AppText variant="body">{sample.text}</AppText>
        <View style={styles.options}>
          {sample.options.map((o, i) => {
            const isPicked = picked === i;
            const isAnswer = picked !== null && i === sample.answerIndex;
            const bg = isAnswer ? colors.successSoft : isPicked ? colors.errorSoft : colors.white;
            const border = isAnswer ? colors.success : isPicked ? colors.error : colors.border;
            return (
              <Pressable
                key={o}
                onPress={() => setPicked(i)}
                accessibilityRole="radio"
                accessibilityState={{ checked: isPicked }}
                accessibilityLabel={`Option ${LETTERS[i]}: ${o}${isAnswer ? ', correct answer' : isPicked ? ', incorrect' : ''}`}
                style={[styles.option, { backgroundColor: bg, borderColor: border }]}
              >
                <AppText variant="smallStrong" color={colors.textSecondary}>{LETTERS[i]}</AppText>
                <AppText variant="body" style={styles.flex}>{o}</AppText>
                {isAnswer && <Ionicons name="checkmark-circle" size={20} color={colors.success} />}
                {isPicked && !isAnswer && <Ionicons name="close-circle" size={20} color={colors.error} />}
              </Pressable>
            );
          })}
        </View>
        {picked !== null && (
          <AppText variant="smallStrong" color={correct ? colors.success : colors.error} accessibilityLiveRegion="polite">
            {correct ? 'Correct! Full mocks include a detailed explanation and a shortcut.' : `Not quite — the answer is ${LETTERS[sample.answerIndex]}.`}
          </AppText>
        )}
      </Card>

      <Card>
        <CardHeader title="Available languages" />
        <AppText variant="small">{exam.languages.map((l) => languageName(l)).join(' · ')}</AppText>
      </Card>

      <AppText variant="caption">{DISCLAIMERS.examAffiliation}</AppText>
    </Screen>
  );
}

function Fact({ icon, label, value }: { icon: ComponentProps<typeof Ionicons>['name']; label: string; value: string }) {
  return (
    <View style={styles.fact} accessible accessibilityLabel={`${label}: ${value}`}>
      <View style={styles.factLabel}>
        <Ionicons name={icon} size={14} color={colors.textSecondary} />
        <AppText variant="caption">{label}</AppText>
      </View>
      <AppText variant="h3">{value}</AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', gap: spacing.md, alignItems: 'center' },
  flex: { flex: 1 },
  badges: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  highlight: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  facts: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  fact: { flexGrow: 1, flexBasis: '45%', padding: spacing.md, borderRadius: radii.md, backgroundColor: colors.background, gap: 4 },
  factLabel: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  gapTop: { marginTop: spacing.md },
  section: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, paddingVertical: spacing.sm },
  marks: { alignItems: 'flex-end' },
  options: { gap: spacing.sm, marginVertical: spacing.md },
  option: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, minHeight: 52, paddingHorizontal: spacing.md, borderRadius: radii.md, borderWidth: 1.5 },
  footer: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
});
