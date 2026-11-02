import { useState } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import { Stack, router, useLocalSearchParams } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { QuestionOutcome } from '@prepmitra/shared';
import { DISCLAIMERS, formatDate, formatDuration, getExamById, getQuestionById } from '@prepmitra/shared';
import {
  AppText, Badge, Button, Card, CardHeader, Chip, DemoBadge, EmptyState, Notice, ProgressBar, ScoreRing, Screen, SegmentedControl, toast,
} from '@/components';
import { errorMessage, reportService } from '@/services';
import { useExamStore } from '@/store';
import { accuracyTone, colors, radii, spacing, TOUCH } from '@/theme';

type Tab = 'overview' | 'strengths' | 'lost' | 'review' | 'plan';
const TABS: { value: Tab; label: string }[] = [
  { value: 'overview', label: 'Overview' },
  { value: 'strengths', label: 'Strengths & gaps' },
  { value: 'lost', label: 'Marks lost' },
  { value: 'review', label: 'Questions' },
  { value: 'plan', label: '7-day plan' },
];
const OUTCOME = {
  correct: { label: 'Correct', tone: 'success', icon: 'checkmark-circle' },
  incorrect: { label: 'Incorrect', tone: 'error', icon: 'close-circle' },
  unanswered: { label: 'Skipped', tone: 'neutral', icon: 'remove-circle' },
} as const;
const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];

export default function ReportScreen() {
  const { reportId = '' } = useLocalSearchParams<{ reportId: string }>();
  const report = useExamStore((s) => s.reports[reportId]);
  const attempt = useExamStore((s) => (report ? s.attempts[report.attemptId] : undefined));
  const [tab, setTab] = useState<Tab>('overview');
  const [filter, setFilter] = useState<QuestionOutcome | 'all'>('all');
  const [expanded, setExpanded] = useState<string | null>(null);

  if (!report) {
    return (
      <Screen>
        <EmptyState icon="document-outline" title="Report not found" description="This report isn’t available on this device." actionLabel="All reports" onAction={() => router.replace('/reports')} />
      </Screen>
    );
  }
  const r = report.result;
  const share = async () => {
    try {
      await reportService.shareExamReport(report);
    } catch (e) {
      toast.error(errorMessage(e, 'Could not open the share sheet.'));
    }
  };
  const numberOf = (qid: string) => r.questions.findIndex((q) => q.questionId === qid) + 1;
  const openQuestion = (qid: string) => {
    setFilter('all');
    setExpanded(qid);
    setTab('review');
  };
  const nextExam = getExamById(report.recommendedNextExamId);
  const questions = r.questions.filter((q) => filter === 'all' || q.outcome === filter);

  return (
    <Screen>
      <Stack.Screen
        options={{
          title: getExamById(report.examId)?.shortTitle ?? 'Report',
          headerRight: () => (
            <Pressable onPress={share} accessibilityRole="button" accessibilityLabel="Share report" style={styles.headerBtn} hitSlop={6}>
              <Ionicons name="share-outline" size={22} color={colors.primary} />
            </Pressable>
          ),
        }}
      />
      <View style={styles.top}>
        <ScoreRing percent={r.percentage} size={96} stroke={9} />
        <View style={styles.flex}>
          <AppText variant="h3" numberOfLines={2}>{report.examTitle}</AppText>
          <AppText variant="small">{formatDate(report.createdAt)} · {formatDuration(report.timeTakenSec)}</AppText>
          <AppText variant="smallStrong">{r.score}/{r.maxScore} · {r.accuracy}% accuracy · {report.percentile} %ile</AppText>
          <DemoBadge label="Demo analysis" />
        </View>
      </View>
      <Notice tone="warning">{DISCLAIMERS.demoAi}</Notice>

      <SegmentedControl<Tab> scrollable segments={TABS} value={tab} onChange={setTab} accessibilityLabel="Report sections" />

      {tab === 'overview' && (
        <>
          <Card>
            <CardHeader title="Sections" />
            <View style={styles.gap}>
              {r.sections.map((s) => (
                <ProgressBar key={s.sectionId} label={`${s.name} · ${s.score}/${s.maxScore}`} value={s.accuracy} showValue tone={accuracyTone(s.accuracy)} size="sm" />
              ))}
            </View>
          </Card>
          <Card>
            <CardHeader title="Topic accuracy" subtitle="Share of questions answered correctly in each topic" />
            <View style={styles.gap}>
              {r.topics.map((t) => (
                <ProgressBar key={t.topic} label={`${t.topic} (${t.correct}/${t.total})`} value={t.accuracy} showValue tone={accuracyTone(t.accuracy)} size="sm" />
              ))}
            </View>
          </Card>
          <Button title="Share report" variant="outline" leftIcon="share-outline" onPress={share} />
        </>
      )}

      {tab === 'strengths' && (
        <>
          <Card>
            <CardHeader title="Strengths" />
            {report.strengths.map((s) => (
              <View key={s} style={styles.bullet}>
                <Ionicons name="trophy-outline" size={18} color={colors.success} />
                <AppText variant="small" color={colors.text} style={styles.flex}>{s}</AppText>
              </View>
            ))}
          </Card>
          <Card>
            <CardHeader title="Weaknesses with evidence" subtitle="Tap a question number to review it" />
            {report.weaknesses.length === 0 && <AppText variant="small">No topic fell below 60% accuracy. Nice work.</AppText>}
            {report.weaknesses.map((w) => (
              <View key={w.topic} style={styles.weak}>
                <View style={styles.rowCenter}>
                  <AppText variant="bodyStrong" style={styles.flex}>{w.topic}</AppText>
                  <Badge label={`${w.accuracy}%`} tone={accuracyTone(w.accuracy)} />
                </View>
                <AppText variant="small">{w.note}</AppText>
                {w.evidenceQuestionIds.length > 0 && (
                  <View style={styles.chips}>
                    {w.evidenceQuestionIds.map((qid) => (
                      <Chip key={qid} label={`Q${numberOf(qid)}`} onPress={() => openQuestion(qid)} accessibilityLabel={`Review question ${numberOf(qid)}`} />
                    ))}
                  </View>
                )}
              </View>
            ))}
          </Card>
        </>
      )}

      {tab === 'lost' && (
        <>
          <View style={styles.row}>
            <Card style={styles.metric}>
              <AppText variant="caption">Marks lost in total</AppText>
              <AppText variant="h2" color={colors.error}>{r.marksLostTotal}</AppText>
            </Card>
            <Card style={styles.metric}>
              <AppText variant="caption">Negative marking</AppText>
              <AppText variant="h2" color={colors.warningText}>−{r.negativeMarksLost}</AppText>
            </Card>
          </View>
          {report.loopholes.length === 0 ? (
            <EmptyState compact icon="shield-checkmark-outline" title="No loopholes found" description="No careless errors, guesses or time sinks were detected." />
          ) : (
            report.loopholes.map((l) => (
              <Card key={l.title} style={styles.gapSm}>
                <View style={styles.rowCenter}>
                  <AppText variant="bodyStrong" style={styles.flex}>{l.title}</AppText>
                  {l.marksImpact > 0 && <Badge label={`−${l.marksImpact} marks`} tone="error" />}
                </View>
                <AppText variant="small">{l.detail}</AppText>
              </Card>
            ))
          )}
        </>
      )}

      {tab === 'review' && (
        <>
          <View style={styles.chips} accessibilityRole="radiogroup">
            {(['all', 'correct', 'incorrect', 'unanswered'] as const).map((f) => (
              <Chip
                key={f}
                role="radio"
                label={f === 'all' ? `All (${r.questions.length})` : `${OUTCOME[f].label} (${r.questions.filter((q) => q.outcome === f).length})`}
                selected={filter === f}
                onPress={() => setFilter(f)}
              />
            ))}
          </View>
          {questions.length === 0 && <EmptyState compact icon="filter-outline" title="Nothing here" description="No questions match this filter." />}
          {questions.map((qr) => {
            const q = getQuestionById(qr.questionId);
            if (!q) return null;
            const n = numberOf(qr.questionId);
            const open = expanded === qr.questionId;
            const answer = attempt?.states[qr.questionId]?.answer;
            const o = OUTCOME[qr.outcome];
            return (
              <Card key={qr.questionId} padded={false}>
                <Pressable
                  onPress={() => setExpanded(open ? null : qr.questionId)}
                  accessibilityRole="button"
                  accessibilityState={{ expanded: open }}
                  accessibilityLabel={`Question ${n}, ${o.label}. ${q.text}`}
                  style={styles.qHead}
                >
                  <Ionicons name={o.icon} size={22} color={o.tone === 'neutral' ? colors.textMuted : o.tone === 'success' ? colors.success : colors.error} />
                  <View style={styles.flex}>
                    <AppText variant="smallStrong">Q{n} · {q.topic}</AppText>
                    <AppText variant="small" numberOfLines={open ? undefined : 2}>{q.text}</AppText>
                  </View>
                  <Ionicons name={open ? 'chevron-up' : 'chevron-down'} size={18} color={colors.textMuted} />
                </Pressable>
                {open && (
                  <View style={styles.qBody}>
                    {q.type === 'numeric' ? (
                      <>
                        <AppText variant="small">Your answer: <AppText variant="smallStrong">{answer?.numericValue || '—'}</AppText></AppText>
                        <AppText variant="small">Correct answer: <AppText variant="smallStrong" color={colors.success}>{q.correctNumeric}</AppText></AppText>
                      </>
                    ) : (
                      q.options?.map((opt, i) => {
                        const isCorrect = q.correctOptionIds?.includes(opt.id);
                        const chosen = answer?.selectedOptionIds?.includes(opt.id);
                        return (
                          <View
                            key={opt.id}
                            style={[styles.opt, isCorrect && styles.optCorrect, chosen && !isCorrect && styles.optWrong]}
                            accessible
                            accessibilityLabel={`Option ${LETTERS[i]}: ${opt.text}${isCorrect ? ', correct answer' : ''}${chosen ? ', your choice' : ''}`}
                          >
                            <AppText variant="smallStrong" color={colors.textSecondary}>{LETTERS[i]}</AppText>
                            <AppText variant="small" color={colors.text} style={styles.flex}>{opt.text}</AppText>
                            {chosen && <Badge label="You" tone={isCorrect ? 'success' : 'error'} />}
                          </View>
                        );
                      })
                    )}
                    <View style={styles.explain}>
                      <AppText variant="smallStrong">Explanation</AppText>
                      <AppText variant="small" color={colors.text}>{q.explanation}</AppText>
                    </View>
                    {q.shortcut ? (
                      <View style={[styles.explain, styles.shortcut]}>
                        <AppText variant="smallStrong" color={colors.secondary}>Shortcut</AppText>
                        <AppText variant="small" color={colors.text}>{q.shortcut}</AppText>
                      </View>
                    ) : null}
                    <AppText variant="caption">
                      Time: {formatDuration(qr.timeSpentSec)} (expected ~{formatDuration(q.expectedTimeSec)}) · Marks: {qr.marksAwarded > 0 ? '+' : ''}{qr.marksAwarded}
                    </AppText>
                  </View>
                )}
              </Card>
            );
          })}
        </>
      )}

      {tab === 'plan' && (
        <>
          {report.improvementPlan.map((d) => (
            <Card key={d.day} style={styles.gapSm}>
              <View style={styles.rowCenter}>
                <View style={styles.day}><AppText variant="smallStrong" color={colors.white}>D{d.day}</AppText></View>
                <AppText variant="bodyStrong" style={styles.flex}>{d.title}</AppText>
                <Badge label={`${d.minutes} min`} icon="time-outline" />
              </View>
              {d.tasks.map((t) => (
                <View key={t} style={styles.bullet}>
                  <Ionicons name="ellipse" size={6} color={colors.primary} style={styles.dot} />
                  <AppText variant="small" color={colors.text} style={styles.flex}>{t}</AppText>
                </View>
              ))}
            </Card>
          ))}
          {nextExam && (
            <Button
              title={nextExam.id === report.examId ? `Retake ${nextExam.shortTitle}` : `Try ${nextExam.shortTitle} next`}
              leftIcon="play"
              onPress={() => router.push(`/exams/${nextExam.id}`)}
            />
          )}
        </>
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  headerBtn: { width: TOUCH, height: TOUCH, alignItems: 'center', justifyContent: 'center' },
  top: { flexDirection: 'row', alignItems: 'center', gap: spacing.lg },
  gap: { gap: spacing.md },
  gapSm: { gap: spacing.sm },
  bullet: { flexDirection: 'row', gap: spacing.sm, alignItems: 'flex-start', paddingVertical: 4 },
  dot: { marginTop: 7 },
  weak: { gap: 6, paddingVertical: spacing.sm, borderTopWidth: StyleSheet.hairlineWidth, borderTopColor: colors.border },
  rowCenter: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  row: { flexDirection: 'row', gap: spacing.sm },
  metric: { flex: 1, gap: 4 },
  qHead: { flexDirection: 'row', gap: spacing.md, alignItems: 'center', padding: spacing.md, minHeight: 56 },
  qBody: { paddingHorizontal: spacing.md, paddingBottom: spacing.md, gap: spacing.sm },
  opt: { flexDirection: 'row', gap: spacing.sm, alignItems: 'center', padding: spacing.sm, borderRadius: radii.md, borderWidth: 1, borderColor: colors.border },
  optCorrect: { borderColor: colors.success, backgroundColor: colors.successSoft },
  optWrong: { borderColor: colors.error, backgroundColor: colors.errorSoft },
  explain: { gap: 4, padding: spacing.md, borderRadius: radii.md, backgroundColor: colors.background },
  shortcut: { backgroundColor: colors.secondarySoft },
  day: { width: 34, height: 34, borderRadius: 17, backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center' },
});
