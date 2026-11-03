import { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import type { LanguageCode } from '@prepmitra/shared';
import { DISCLAIMERS, formatClock, pluralize, relativeTime, remainingSeconds } from '@prepmitra/shared';
import {
  AppText, Badge, Button, Card, CardHeader, ErrorState, LanguageSelector, LoadingSkeleton, Notice, PaletteLegend, Screen, SwitchRow, toast,
} from '@/components';
import { CheckoutSheet } from '@/features/subscription/CheckoutSheet';
import { useAsync } from '@/hooks/useAsync';
import { attemptService, errorMessage, examService } from '@/services';
import { examCreditCost, useAuthStore, useExamStore, useSubscriptionStore } from '@/store';
import { colors, radii, spacing } from '@/theme';

const RULES = [
  'The clock starts when you press Start and cannot be paused. The test submits automatically when time runs out.',
  'Every answer is saved as you go. If you close the app, you can resume this attempt with the remaining time.',
  'Use Save & Next to move on, Mark for review to revisit later, and Clear to remove an answer.',
  'Questions marked for review that also have an answer are evaluated on submission.',
  'You can switch any question between your chosen language and English.',
  'Open the question palette to jump to any question or section at any time.',
];

export default function ExamInstructions() {
  const { id = '' } = useLocalSearchParams<{ id: string }>();
  const { data: exam, loading, error, reload } = useAsync(() => examService.get(id), id);
  const user = useAuthStore((s) => s.session?.user);
  const sub = useSubscriptionStore((s) => s.sub);
  const consume = useSubscriptionStore((s) => s.consume);
  const refund = useSubscriptionStore((s) => s.refund);
  const attempts = useExamStore((s) => s.attempts);
  const saveAttempt = useExamStore((s) => s.saveAttempt);
  const [language, setLanguage] = useState<LanguageCode | null>(null);
  const [agreed, setAgreed] = useState(false);
  const [agreeError, setAgreeError] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);
  const [buyOpen, setBuyOpen] = useState(false);

  if (loading) return <Screen><LoadingSkeleton /></Screen>;
  if (error || !exam) return <Screen><ErrorState title="Exam not available" description={error ?? 'This exam could not be loaded.'} onRetry={reload} /></Screen>;

  const resumable = Object.values(attempts).find((a) => a.examId === exam.id && a.status === 'in-progress' && remainingSeconds(a) > 0);
  const lang: LanguageCode = language ?? (user && exam.languages.includes(user.preferredLanguage) ? user.preferredLanguage : 'en');
  const { cost, usesFreeTrial } = examCreditCost(exam, sub);
  const enough = usesFreeTrial || sub.credits >= cost;
  const demoQs = exam.sections.length * exam.demo.questionsPerSection;

  const start = async () => {
    if (!agreed) {
      setAgreeError('Please confirm you have read the instructions.');
      return;
    }
    if (!enough) {
      setBuyOpen(true);
      return;
    }
    setStarting(true);
    const label = `${exam.shortTitle} mock`;
    if (!consume(cost, 'exam-attempt', label, usesFreeTrial)) {
      setStarting(false);
      setBuyOpen(true);
      return;
    }
    try {
      const attempt = await attemptService.start(exam, lang);
      saveAttempt(attempt);
      toast.success(usesFreeTrial ? 'Free mini mock started. All the best!' : `${pluralize(cost, 'credit')} used. All the best!`);
      router.replace(`/exam/${attempt.id}`);
    } catch (e) {
      if (!usesFreeTrial) refund(cost, `${label} — could not start`);
      toast.error(`${errorMessage(e)} Your credit was restored.`);
      setStarting(false);
    }
  };

  return (
    <Screen
      footer={
        <Button
          title={resumable ? 'Start a new attempt' : enough ? 'Start test' : 'Get credits to start'}
          size="lg"
          leftIcon={enough ? 'play' : 'wallet-outline'}
          loading={starting}
          onPress={start}
          fullWidth
        />
      }
    >
      <AppText variant="h2" accessibilityRole="header">{exam.title}</AppText>
      <AppText variant="small">Read these carefully before you begin.</AppText>

      {resumable && (
        <Notice
          tone="info"
          title="You have an unfinished attempt"
          action={<Button title="Resume" size="sm" leftIcon="refresh" onPress={() => router.replace(`/exam/${resumable.id}`)} />}
        >
          {`Started ${relativeTime(resumable.startedAt)} · ${formatClock(remainingSeconds(resumable))} remaining. Resuming does not use another credit.`}
        </Notice>
      )}

      <Card>
        <CardHeader title="Demo paper at a glance" subtitle={`Shortened prototype paper based on the ${exam.shortTitle} pattern.`} />
        <View style={styles.facts}>
          {[
            ['Questions', String(demoQs)],
            ['Duration', `${exam.demo.durationMin} min`],
            ['Sections', String(exam.sections.length)],
            ['Calculator', exam.calculatorAllowed ? 'Allowed' : 'No'],
          ].map(([k, v]) => (
            <View key={k} style={styles.fact} accessible accessibilityLabel={`${k}: ${v}`}>
              <AppText variant="caption">{k}</AppText>
              <AppText variant="h3">{v}</AppText>
            </View>
          ))}
        </View>
        {exam.sections.map((s) => (
          <View key={s.id} style={styles.sectionRow}>
            <AppText variant="small" color={colors.text} style={styles.flex}>{s.name}</AppText>
            <AppText variant="caption">{exam.demo.questionsPerSection} Qs</AppText>
            <AppText variant="smallStrong" color={colors.success}>+{s.marksPerQuestion}</AppText>
            <AppText variant="smallStrong" color={s.negativeMarks ? colors.error : colors.textSecondary}>{s.negativeMarks ? `−${s.negativeMarks}` : '0'}</AppText>
          </View>
        ))}
      </Card>

      <Card>
        <CardHeader title="General instructions" />
        {RULES.map((r, i) => (
          <View key={r} style={styles.rule}>
            <AppText variant="smallStrong" color={colors.primary} style={styles.ruleNo}>{i + 1}.</AppText>
            <AppText variant="small" color={colors.text} style={styles.flex}>{r}</AppText>
          </View>
        ))}
        <AppText variant="label" style={styles.gapTop}>Question palette</AppText>
        <View style={styles.gapTopSm}><PaletteLegend /></View>
      </Card>

      <Card>
        <LanguageSelector
          label="Exam language"
          value={lang}
          onChange={setLanguage}
          allowed={exam.languages}
          hint="You can switch to English for any question during the exam."
        />
        <View style={styles.cost}>
          <AppText variant="small" style={styles.flex}>Cost</AppText>
          <Badge label={usesFreeTrial ? 'Free trial' : pluralize(cost, 'credit')} tone={usesFreeTrial ? 'success' : 'primary'} icon="wallet-outline" />
        </View>
        <AppText variant="caption">You have {pluralize(sub.credits, 'credit')}. Credits are used only when you start.</AppText>
        {!enough && (
          <AppText variant="smallStrong" color={colors.error} accessibilityRole="alert">Not enough credits for this mock.</AppText>
        )}
      </Card>

      <Notice tone="warning" title="Demo timer">{DISCLAIMERS.demoTimer}</Notice>

      <Card>
        <SwitchRow
          label="I have read and understood the instructions"
          value={agreed}
          onValueChange={(v) => {
            setAgreed(v);
            setAgreeError(null);
          }}
          error={agreeError ?? undefined}
        />
      </Card>

      <CheckoutSheet
        visible={buyOpen}
        onClose={() => setBuyOpen(false)}
        reason={`This mock needs ${pluralize(cost, 'credit')} and you have ${sub.credits}.`}
      />
    </Screen>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  facts: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.md },
  fact: { flexGrow: 1, flexBasis: '45%', padding: spacing.md, borderRadius: radii.md, backgroundColor: colors.background, gap: 2 },
  sectionRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, paddingVertical: 6 },
  rule: { flexDirection: 'row', gap: spacing.sm, paddingVertical: 4 },
  ruleNo: { width: 20 },
  gapTop: { marginTop: spacing.md },
  gapTopSm: { marginTop: spacing.sm },
  cost: { flexDirection: 'row', alignItems: 'center', marginTop: spacing.md, marginBottom: 4 },
});
