import { useState } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import { Stack, router, useLocalSearchParams } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { InterviewScores } from '@prepmitra/shared';
import { DISCLAIMERS, EXPERIENCE_LEVELS, formatDate, formatDuration, languageName } from '@prepmitra/shared';
import {
  AppText, Badge, Button, Card, CardHeader, DemoBadge, EmptyState, Notice, ProgressBar, ScoreRing, Screen, SegmentedControl, toast,
} from '@/components';
import { errorMessage, reportService } from '@/services';
import { useInterviewStore } from '@/store';
import { accuracyTone, colors, radii, spacing, TOUCH } from '@/theme';

const SCORE_LABELS: Record<keyof InterviewScores, string> = {
  roleKnowledge: 'Role knowledge',
  answerStructure: 'Answer structure',
  communication: 'Communication',
  confidence: 'Confidence',
  resumeConsistency: 'Resume consistency',
};

type Tab = 'summary' | 'answers' | 'plan';

export default function InterviewReportScreen() {
  const { reportId = '' } = useLocalSearchParams<{ reportId: string }>();
  const report = useInterviewStore((s) => s.reports[reportId]);
  const [tab, setTab] = useState<Tab>('summary');
  const [open, setOpen] = useState<string | null>(null);

  if (!report) {
    return (
      <Screen>
        <EmptyState icon="document-outline" title="Report not found" description="This interview report isn’t available on this device." actionLabel="All reports" onAction={() => router.replace('/reports')} />
      </Screen>
    );
  }

  const share = async () => {
    try {
      await reportService.shareInterviewReport(report);
    } catch (e) {
      toast.error(errorMessage(e, 'Could not open the share sheet.'));
    }
  };
  const level = EXPERIENCE_LEVELS.find((l) => l.value === report.level)?.label ?? report.level;

  return (
    <Screen>
      <Stack.Screen
        options={{
          headerRight: () => (
            <Pressable onPress={share} accessibilityRole="button" accessibilityLabel="Share report" style={styles.headerBtn} hitSlop={6}>
              <Ionicons name="share-outline" size={22} color={colors.primary} />
            </Pressable>
          ),
        }}
      />
      <View style={styles.top}>
        <ScoreRing percent={report.overall * 10} label={`${report.overall}`} sublabel="out of 10" size={110} stroke={10} />
        <View style={styles.flex}>
          <AppText variant="h3">{report.roleTitle}</AppText>
          <AppText variant="small">{formatDate(report.createdAt)} · {level}</AppText>
          <AppText variant="small">{report.mode === 'voice' ? 'Voice' : 'Text'} · {languageName(report.language)} · {formatDuration(report.durationSec)}</AppText>
          <DemoBadge label="Demo analysis" />
        </View>
      </View>
      <Notice tone="warning">{DISCLAIMERS.demoAi}</Notice>

      <SegmentedControl<Tab>
        value={tab}
        onChange={setTab}
        accessibilityLabel="Report sections"
        segments={[
          { value: 'summary', label: 'Summary' },
          { value: 'answers', label: `Answers (${report.questionFeedback.length})` },
          { value: 'plan', label: '7-day plan' },
        ]}
      />

      {tab === 'summary' && (
        <>
          <Card>
            <CardHeader title="Scores" subtitle="Each skill is scored from 1 to 10" />
            <View style={styles.gap}>
              {(Object.keys(SCORE_LABELS) as (keyof InterviewScores)[]).map((k) => (
                <ProgressBar
                  key={k}
                  label={SCORE_LABELS[k]}
                  value={report.scores[k]}
                  max={10}
                  showValue
                  valueLabel={`${report.scores[k]}/10`}
                  tone={accuracyTone(report.scores[k] * 10)}
                />
              ))}
            </View>
          </Card>

          {report.voiceMetrics && (
            <View style={styles.row}>
              <Card style={styles.metric}>
                <AppText variant="caption">Speaking pace</AppText>
                <AppText variant="h2">{report.voiceMetrics.wordsPerMinute}</AppText>
                <AppText variant="caption">words / min (ideal 120–160)</AppText>
              </Card>
              <Card style={styles.metric}>
                <AppText variant="caption">Filler words</AppText>
                <AppText variant="h2" color={report.voiceMetrics.fillerWords > 4 ? colors.warningText : colors.text}>{report.voiceMetrics.fillerWords}</AppText>
                <AppText variant="caption">um, like, basically…</AppText>
              </Card>
            </View>
          )}

          <ListCard title="Strengths" icon="trophy-outline" color={colors.success} items={report.strengths} />
          <ListCard title="To improve" icon="trending-up-outline" color={colors.warningText} items={report.weaknesses} empty="No major gaps found." />
          <ListCard title="Red flags" icon="flag-outline" color={colors.error} items={report.redFlags} empty="No red flags — nothing a panel would worry about." />
          <Button title="Share report" variant="outline" leftIcon="share-outline" onPress={share} />
        </>
      )}

      {tab === 'answers' &&
        (report.questionFeedback.length === 0 ? (
          <EmptyState compact icon="chatbubble-ellipses-outline" title="No answers recorded" description="The interview ended before any question was answered." />
        ) : (
          report.questionFeedback.map((f, i) => {
            const isOpen = open === f.questionId;
            return (
              <Card key={f.questionId} padded={false}>
                <Pressable
                  onPress={() => setOpen(isOpen ? null : f.questionId)}
                  accessibilityRole="button"
                  accessibilityState={{ expanded: isOpen }}
                  accessibilityLabel={`Question ${i + 1}, score ${f.score} out of 10. ${f.question}`}
                  style={styles.qHead}
                >
                  <Badge label={`${f.score}/10`} tone={accuracyTone(f.score * 10)} />
                  <AppText variant="smallStrong" style={styles.flex} numberOfLines={isOpen ? undefined : 2}>{f.question}</AppText>
                  <Ionicons name={isOpen ? 'chevron-up' : 'chevron-down'} size={18} color={colors.textMuted} />
                </Pressable>
                {isOpen && (
                  <View style={styles.qBody}>
                    <Block title="Your answer" text={f.answer} />
                    <Block title="What was good" text={f.good} tone="success" />
                    <Block title="What was missing" text={f.missing} tone="warning" />
                    <Block title="Model answer" text={f.modelAnswer} tone="primary" />
                  </View>
                )}
              </Card>
            );
          })
        ))}

      {tab === 'plan' && (
        <>
          {report.plan.map((d) => (
            <Card key={d.day} style={styles.gapSm}>
              <View style={styles.rowCenter}>
                <View style={styles.day}><AppText variant="smallStrong" color={colors.white}>D{d.day}</AppText></View>
                <AppText variant="bodyStrong" style={styles.flex}>{d.title}</AppText>
                <Badge label={`${d.minutes} min`} icon="time-outline" />
              </View>
              {d.tasks.map((t) => (
                <AppText key={t} variant="small" color={colors.text}>• {t}</AppText>
              ))}
            </Card>
          ))}
          <Button title="Practise again" leftIcon="refresh" onPress={() => router.push(`/interviews/${report.roleId}`)} />
        </>
      )}
    </Screen>
  );
}

function ListCard({ title, icon, color, items, empty }: { title: string; icon: 'trophy-outline' | 'trending-up-outline' | 'flag-outline'; color: string; items: string[]; empty?: string }) {
  return (
    <Card>
      <View style={styles.listHead}>
        <Ionicons name={icon} size={18} color={color} />
        <AppText variant="h3">{title}</AppText>
      </View>
      {items.length === 0 ? <AppText variant="small">{empty}</AppText> : items.map((it) => (
        <AppText key={it} variant="small" color={colors.text} style={styles.item}>• {it}</AppText>
      ))}
    </Card>
  );
}

function Block({ title, text, tone }: { title: string; text: string; tone?: 'success' | 'warning' | 'primary' }) {
  const bg = tone === 'success' ? colors.successSoft : tone === 'warning' ? colors.warningSoft : tone === 'primary' ? colors.primarySoft : colors.background;
  return (
    <View style={[styles.block, { backgroundColor: bg }]}>
      <AppText variant="smallStrong">{title}</AppText>
      <AppText variant="small" color={colors.text} selectable>{text}</AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  headerBtn: { width: TOUCH, height: TOUCH, alignItems: 'center', justifyContent: 'center' },
  top: { flexDirection: 'row', alignItems: 'center', gap: spacing.lg },
  gap: { gap: spacing.md },
  gapSm: { gap: spacing.sm },
  row: { flexDirection: 'row', gap: spacing.sm },
  rowCenter: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  metric: { flex: 1, gap: 2 },
  listHead: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.sm },
  item: { paddingVertical: 3 },
  qHead: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.md, minHeight: 56 },
  qBody: { paddingHorizontal: spacing.md, paddingBottom: spacing.md, gap: spacing.sm },
  block: { padding: spacing.md, borderRadius: radii.md, gap: 4 },
  day: { width: 34, height: 34, borderRadius: 17, backgroundColor: colors.secondary, alignItems: 'center', justifyContent: 'center' },
});
