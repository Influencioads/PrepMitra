import { useCallback, useEffect, useRef, useState } from 'react';
import {
  ActivityIndicator, Alert, AppState, Modal, Pressable, ScrollView, StyleSheet, Switch, useWindowDimensions, View, type ScrollViewInstance,
} from 'react-native';
import { router, useLocalSearchParams, usePreventRemove } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { Attempt } from '@prepmitra/shared';
import {
  PALETTE_LEGEND, addTimeSpent, clearResponse, countPaletteStatuses, hasTranslation, languageName, localizeQuestion, relativeTime,
  sectionNameMap, setAnswer, toggleMarkForReview, toggleOption, visitQuestion,
} from '@prepmitra/shared';
import {
  AppText, BottomSheet, Button, ConfirmDialog, CountdownTimer, EmptyState, Notice, QuestionCard, QuestionPalette, Screen, toast,
} from '@/components';
import { attemptService, errorMessage, examService } from '@/services';
import { useExamStore, useProfileStore } from '@/store';
import { StatusBar } from 'expo-status-bar';
import { colors, fonts, paletteColors, paper, radii, spacing, TOUCH } from '@/theme';

/** Time on the current question is flushed to the persisted attempt at this interval. */
const FLUSH_EVERY_MS = 10_000;

export default function ExamSession() {
  const { attemptId = '' } = useLocalSearchParams<{ attemptId: string }>();
  const attempt = useExamStore((s) => s.attempts[attemptId]);
  const updateAttempt = useExamStore((s) => s.updateAttempt);
  const completeAttempt = useExamStore((s) => s.completeAttempt);
  const allowEnglishToggle = useProfileStore((s) => s.settings.examLanguageToggle);
  const exam = attempt ? examService.getSync(attempt.examId) : undefined;

  const [paletteOpen, setPaletteOpen] = useState(false);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [showEnglish, setShowEnglish] = useState(false);
  const [savedAt, setSavedAt] = useState<number | null>(null);
  const submittingRef = useRef(false);
  const enteredAt = useRef(Date.now());
  const scrollRef = useRef<ScrollViewInstance>(null);
  // Small phones (360dp): drop icons from the three-button row so labels fit on one line.
  const narrow = useWindowDimensions().width < 400;

  const active = !!attempt && attempt.status === 'in-progress' && !submitting;

  /** Adds the seconds spent on the current question since the last flush. */
  const flushTime = useCallback(() => {
    const now = Date.now();
    const secs = Math.round((now - enteredAt.current) / 1000);
    enteredAt.current = now;
    if (secs <= 0) return;
    updateAttempt(attemptId, (a) => {
      const qid = a.paper[a.currentIndex]?.questionId;
      return qid ? addTimeSpent(a, qid, secs) : a;
    });
  }, [attemptId, updateAttempt]);

  // Periodic + background flush so time spent survives the app being killed.
  useEffect(() => {
    if (!active) return;
    const id = setInterval(flushTime, FLUSH_EVERY_MS);
    const sub = AppState.addEventListener('change', (s) => {
      if (s !== 'active') flushTime();
      else enteredAt.current = Date.now();
    });
    return () => {
      clearInterval(id);
      sub.remove();
    };
  }, [active, flushTime]);

  // Leaving mid-exam (back gesture, Android back, header close) asks first.
  const disablePrevention = usePreventRemove(active, ({ repeat }) => {
    Alert.alert('Leave the exam?', 'Your answers are saved and the timer keeps running. You can resume from Home.', [
      { text: 'Stay', style: 'cancel' },
      {
        text: 'Leave',
        style: 'destructive',
        onPress: () => {
          flushTime();
          repeat();
        },
      },
    ]);
  });

  const persistRemote = (a: Attempt | undefined) => {
    if (!a) return;
    attemptService
      .saveAnswers(a)
      .then(() => setSavedAt(Date.now()))
      .catch(() => toast.error('Autosave failed. Your answers are kept on this device.'));
  };

  const submit = async (auto: boolean) => {
    if (submittingRef.current || !exam) return;
    submittingRef.current = true;
    setConfirmOpen(false);
    setPaletteOpen(false);
    flushTime();
    const latest = useExamStore.getState().attempts[attemptId];
    if (!latest || latest.status !== 'in-progress') return;
    setSubmitting(true);
    const final: Attempt = { ...latest, submittedAt: new Date().toISOString(), autoSubmitted: auto };
    try {
      const report = await attemptService.submit(exam, final);
      completeAttempt(final, report);
      disablePrevention();
      if (auto) toast.info('Time is up — your answers were submitted automatically.');
      else toast.success('Test submitted. Here is your result.');
      router.replace(`/exam-result/${report.id}`);
    } catch (e) {
      submittingRef.current = false;
      setSubmitting(false);
      if (auto) {
        Alert.alert('Time is up', `${errorMessage(e)} Your answers are saved — try submitting again.`, [
          { text: 'Submit now', onPress: () => void submit(true) },
        ]);
      } else {
        toast.error(errorMessage(e));
      }
    }
  };

  if (!attempt || !exam) {
    return (
      <Screen edges={['top', 'left', 'right', 'bottom']}>
        <EmptyState
          icon="alert-circle-outline"
          title="Attempt not found"
          description="This attempt isn’t on this device. Start a new mock from Explore."
          actionLabel="Go home"
          onAction={() => router.replace('/home')}
        />
      </Screen>
    );
  }
  if (attempt.status === 'submitted' && !submitting) {
    return (
      <Screen edges={['top', 'left', 'right', 'bottom']}>
        <EmptyState
          icon="checkmark-done-outline"
          title="This attempt was submitted"
          description="Your answers have been scored."
          actionLabel={attempt.reportId ? 'View result' : 'Go home'}
          onAction={() => router.replace(attempt.reportId ? `/exam-result/${attempt.reportId}` : '/home')}
        />
      </Screen>
    );
  }

  const total = attempt.paper.length;
  const index = Math.min(attempt.currentIndex, total - 1);
  const item = attempt.paper[index];
  const base = item ? examService.getQuestion(item.questionId) : undefined;
  const state = item ? attempt.states[item.questionId] : undefined;
  const sections = sectionNameMap(exam);
  const translated = !!base && attempt.language !== 'en' && hasTranslation(base, attempt.language);
  const question = base ? (showEnglish || !translated ? base : localizeQuestion(base, attempt.language)) : undefined;
  const counts = countPaletteStatuses(attempt.paper.map((p) => p.questionId), attempt.states);
  const answeredTotal = counts.answered + counts['answered-marked'];
  const isLast = index === total - 1;

  const go = (next: number) => {
    if (next < 0 || next >= total) return;
    flushTime();
    updateAttempt(attemptId, (a) => visitQuestion(a, next));
    persistRemote(useExamStore.getState().attempts[attemptId]);
    scrollRef.current?.scrollTo({ y: 0, animated: false });
  };
  const change = (fn: (a: Attempt) => Attempt) => updateAttempt(attemptId, fn);
  const saveAndNext = () => {
    if (!isLast) {
      go(index + 1);
      return;
    }
    flushTime();
    persistRemote(useExamStore.getState().attempts[attemptId]);
    setConfirmOpen(true);
  };
  const markAndNext = () => {
    if (!item) return;
    change((a) => toggleMarkForReview(a, item.questionId));
    if (isLast) {
      persistRemote(useExamStore.getState().attempts[attemptId]);
      setPaletteOpen(true);
    } else go(index + 1);
  };

  return (
    <SafeAreaView style={styles.board} edges={['top', 'left', 'right']}>
      <StatusBar style="light" />
      {/* Focus mode: the question sits on a chalkboard; the answer sheet slides up from the bottom. */}
      <View style={styles.header}>
        <Pressable onPress={() => router.back()} accessibilityRole="button" accessibilityLabel="Pause and leave exam" style={styles.iconBtn} hitSlop={4}>
          <Ionicons name="pause" size={22} color={paper.chalkText} />
        </Pressable>
        <View style={styles.flex}>
          <AppText variant="bodyStrong" numberOfLines={1} color={paper.chalkText}>{exam.shortTitle} mock</AppText>
          <AppText variant="caption" numberOfLines={1} color={paper.chalkMuted}>
            {savedAt ? `Saved ${relativeTime(new Date(savedAt).toISOString())}` : 'Answers save automatically'}
          </AppText>
        </View>
        <CountdownTimer endsAt={attempt.endsAt} onExpire={() => void submit(true)} paused={submitting} />
        <Pressable onPress={() => setConfirmOpen(true)} accessibilityRole="button" accessibilityLabel="Submit test" style={styles.submitBtn} hitSlop={4}>
          <AppText variant="smallStrong" color={paper.chalkText}>Submit</AppText>
        </Pressable>
      </View>

      <View style={styles.subHeader}>
        <Pressable
          onPress={() => setPaletteOpen(true)}
          accessibilityRole="button"
          accessibilityLabel={`Question palette. ${answeredTotal} of ${total} answered`}
          style={styles.paletteBtn}
        >
          <Ionicons name="grid-outline" size={18} color={colors.warning} />
          <AppText variant="smallStrong" color={colors.warning}>{answeredTotal}/{total} answered</AppText>
        </Pressable>
        {translated && allowEnglishToggle ? (
          <View style={styles.langToggle}>
            <AppText variant="caption" color={paper.chalkText}>English</AppText>
            <Switch
              value={showEnglish}
              onValueChange={setShowEnglish}
              accessibilityLabel={`Show this question in English instead of ${languageName(attempt.language)}`}
              trackColor={{ true: '#F28C28', false: 'rgba(245,243,234,0.3)' }}
              thumbColor={colors.white}
            />
          </View>
        ) : attempt.language !== 'en' && base && !translated ? (
          <AppText variant="caption" color={paper.chalkMuted} style={styles.langNote} numberOfLines={2}>Not yet in {languageName(attempt.language)} — showing English</AppText>
        ) : null}
      </View>

      <ScrollView ref={scrollRef} style={styles.flex} contentContainerStyle={styles.body} showsVerticalScrollIndicator={false}>
        {question && item ? (
          <QuestionCard
            question={question}
            number={index + 1}
            total={total}
            sectionName={sections[item.sectionId]}
            marks={item.marks}
            negativeMarks={item.negativeMarks}
            answer={state?.answer}
            marked={state?.marked}
            tone="chalk"
            onToggleOption={(optionId) =>
              change((a) => setAnswer(a, item.questionId, toggleOption(a.states[item.questionId]?.answer, optionId, question.type === 'multiple')))
            }
            onNumericChange={(v) => change((a) => setAnswer(a, item.questionId, v ? { numericValue: v } : undefined))}
          />
        ) : (
          <Notice tone="error" title="Question unavailable">This question could not be loaded. Use the palette to move on.</Notice>
        )}
        <AppText style={styles.hint} align="center">Not sure? Mark it for review and come back.</AppText>
      </ScrollView>

      <SafeAreaView edges={['bottom']} style={styles.footer}>
        <View style={styles.sheetHead}>
          <AppText style={styles.sheetTitle}>ANSWER SHEET</AppText>
          <AppText variant="caption">{answeredTotal} done · {counts.marked + counts['answered-marked']} marked</AppText>
        </View>
        <View style={styles.row}>
          <Button title="Previous" variant="outline" size="sm" leftIcon={narrow ? undefined : 'chevron-back'} onPress={() => go(index - 1)} disabled={index === 0} style={styles.flex} />
          <Button
            title="Clear"
            variant="outline"
            size="sm"
            onPress={() => item && change((a) => clearResponse(a, item.questionId))}
            disabled={!state?.answer}
            style={styles.flex}
            accessibilityLabel="Clear response"
          />
          <Button
            title={state?.marked ? 'Unmark & Next' : 'Mark & Next'}
            variant="soft"
            size="sm"
            leftIcon={narrow ? undefined : state?.marked ? 'bookmark' : 'bookmark-outline'}
            onPress={markAndNext}
            style={styles.flex2}
            accessibilityLabel={state?.marked ? 'Remove review mark and go to next question' : 'Mark for review and go to next question'}
          />
        </View>
        <Button title={isLast ? 'Save & finish' : 'Save & Next'} rightIcon={isLast ? 'checkmark' : 'chevron-forward'} onPress={saveAndNext} fullWidth />
      </SafeAreaView>

      <BottomSheet
        visible={paletteOpen}
        onClose={() => setPaletteOpen(false)}
        title="Question palette"
        subtitle={`${exam.shortTitle} · ${total} questions`}
        footer={<Button title="Submit test" variant="primary" onPress={() => { setPaletteOpen(false); setConfirmOpen(true); }} fullWidth />}
      >
        <QuestionPalette
          paper={attempt.paper}
          states={attempt.states}
          currentIndex={index}
          sectionNames={sections}
          onJump={(i) => {
            setPaletteOpen(false);
            go(i);
          }}
        />
      </BottomSheet>

      <ConfirmDialog
        visible={confirmOpen}
        title="Submit your test?"
        message="You can’t change answers after submitting. Answered questions marked for review are evaluated."
        confirmLabel="Submit"
        onCancel={() => setConfirmOpen(false)}
        onConfirm={() => void submit(false)}
      >
        <View style={styles.summary}>
          {(['answered', 'answered-marked', 'marked', 'not-answered', 'not-visited'] as const).map((s) => (
            <View key={s} style={styles.summaryRow} accessible accessibilityLabel={`${PALETTE_LEGEND[s]}: ${counts[s]}`}>
              <View style={[styles.swatch, { backgroundColor: paletteColors[s].bg, borderColor: paletteColors[s].border }]} />
              <AppText variant="small" color={colors.text} style={styles.flex}>{PALETTE_LEGEND[s]}</AppText>
              <AppText variant="smallStrong">{counts[s]}</AppText>
            </View>
          ))}
        </View>
        {total - answeredTotal > 0 && (
          <Notice tone="warning">{`${total - answeredTotal} question${total - answeredTotal === 1 ? ' is' : 's are'} unanswered.`}</Notice>
        )}
      </ConfirmDialog>

      <Modal visible={submitting} transparent animationType="fade" statusBarTranslucent>
        <View style={styles.overlay} accessibilityViewIsModal>
          <View style={styles.overlayCard}>
            <ActivityIndicator size="large" color={colors.primary} />
            <AppText variant="h3" align="center">Scoring your answers…</AppText>
            <AppText variant="small" align="center">Building your report. This takes a moment.</AppText>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  flex2: { flex: 1.6 },
  board: { flex: 1, backgroundColor: paper.chalk },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
  },
  submitBtn: { minHeight: 36, paddingHorizontal: 12, borderRadius: radii.md, borderWidth: 1.5, borderColor: paper.chalkLine, alignItems: 'center', justifyContent: 'center' },
  hint: { marginTop: spacing.lg, fontFamily: fonts.hand, fontSize: 15, color: paper.chalkMuted },
  sheetHead: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  sheetTitle: { fontSize: 13, fontWeight: '800', letterSpacing: 1.4, color: paper.ink },
  iconBtn: { width: TOUCH, height: TOUCH, alignItems: 'center', justifyContent: 'center', marginLeft: -6 },
  subHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.sm,
    paddingHorizontal: spacing.lg,
    paddingVertical: 4,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: paper.chalkLine,
  },
  paletteBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, minHeight: TOUCH },
  langToggle: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  langNote: { flex: 1, textAlign: 'right' },
  body: { padding: spacing.lg, paddingBottom: spacing['2xl'] },
  footer: {
    gap: spacing.sm,
    paddingHorizontal: spacing.md,
    paddingTop: spacing.sm,
    paddingBottom: spacing.sm,
    backgroundColor: paper.paper,
    borderTopLeftRadius: 26,
    borderTopRightRadius: 26,
  },
  row: { flexDirection: 'row', gap: spacing.sm },
  summary: { gap: 8 },
  summaryRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  swatch: { width: 18, height: 18, borderRadius: 4, borderWidth: 1 },
  overlay: { flex: 1, backgroundColor: 'rgba(15, 23, 42, 0.55)', alignItems: 'center', justifyContent: 'center', padding: spacing.xl },
  overlayCard: { backgroundColor: colors.card, borderRadius: radii.xl, padding: spacing.xl, gap: spacing.md, alignItems: 'center', width: '100%', maxWidth: 340 },
});
