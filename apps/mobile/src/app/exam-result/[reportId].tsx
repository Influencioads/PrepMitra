import { StyleSheet, View } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { formatDuration, getExamById } from '@prepmitra/shared';
import {
  AppText, Button, Card, CardHeader, DemoBadge, EmptyState, MarksLeak, MitraSays, NotebookBackground, Notice, PenNote, PenScore, ProgressBar,
  RatingStars, Screen, Stamp, toast,
} from '@/components';
import Svg, { Circle, Path } from 'react-native-svg';
import { errorMessage, reportService } from '@/services';
import { useExamStore } from '@/store';
import { accuracyTone, colors, paper, radii, spacing } from '@/theme';

/** A marigold garland across the top of the score sheet. Decorative. */
function Garland() {
  const xs = [6, 14, 23, 32, 41, 50, 59, 68, 77, 86, 94];
  return (
    <Svg width="100%" height={44} viewBox="0 0 100 22" preserveAspectRatio="none" pointerEvents="none">
      <Path d="M0 3 Q50 26 100 3" stroke={colors.secondary} strokeWidth={0.6} fill="none" />
      {xs.map((x, i) => {
        const y = 3 + 23 * (1 - Math.pow((x - 50) / 50, 2)) * 0.46;
        return <Circle key={x} cx={x} cy={y} r={2.6} fill={i % 2 ? '#C2410C' : '#F28C28'} />;
      })}
    </Svg>
  );
}

export default function ExamResult() {
  const { reportId = '' } = useLocalSearchParams<{ reportId: string }>();
  const report = useExamStore((s) => s.reports[reportId]);
  const rateReport = useExamStore((s) => s.rateReport);

  if (!report) {
    return (
      <Screen>
        <EmptyState icon="document-outline" title="Result not found" description="This result isn’t available on this device." actionLabel="Go home" onAction={() => router.dismissTo('/home')} />
      </Screen>
    );
  }
  const r = report.result;
  const next = getExamById(report.recommendedNextExamId);
  const praise = r.percentage >= 75 ? 'शाबाश!' : r.percentage >= 50 ? 'Good effort!' : 'Keep going!';
  // Leaks come from the code-computed result, never from AI text.
  const trim = (n: number) => Math.round(n * 100) / 100;
  const wrong = r.questions.filter((q) => q.outcome === 'incorrect');
  const skipped = r.questions.filter((q) => q.outcome === 'unanswered');
  const leaks = [
    { label: `Skipped (${skipped.length})`, marks: trim(skipped.reduce((t, q) => t + q.maxMarks, 0)), color: paper.pen },
    { label: `Wrong answers (${wrong.length})`, marks: trim(wrong.reduce((t, q) => t + q.maxMarks, 0)), color: '#F28C28' },
    { label: 'Negative marking', marks: trim(r.negativeMarksLost), color: '#7E22CE' },
  ].sort((x, y) => y.marks - x.marks);

  const rate = async (n: number) => {
    rateReport(report.id, n);
    try {
      await reportService.rate(report.id, n);
      toast.success('Thanks for rating this report.');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };
  const share = async () => {
    try {
      await reportService.shareExamReport(report);
    } catch (e) {
      toast.error(errorMessage(e, 'Could not open the share sheet.'));
    }
  };

  return (
    <Screen
      footer={
        <>
          <Button title="View detailed report" rightIcon="arrow-forward" onPress={() => router.push(`/reports/${report.id}`)} fullWidth />
          <View style={styles.row}>
            <Button title="Share" variant="outline" leftIcon="share-outline" onPress={share} style={styles.flex} />
            <Button title="Home" variant="outline" leftIcon="home-outline" onPress={() => router.dismissTo('/home')} style={styles.flex} />
          </View>
        </>
      }
    >
      <View style={styles.sheet} accessibilityLabel="Your checked answer sheet">
        <NotebookBackground margin={26} />
        <Garland />
        <View style={styles.sheetBody}>
          <View style={styles.sheetTop}>
            <AppText variant="caption" style={styles.flex} numberOfLines={2}>{report.examTitle.toUpperCase()}</AppText>
            <DemoBadge label="Demo scoring" />
          </View>
          <View style={styles.scoreRow}>
            <PenScore score={`${r.score}`} total={r.maxScore} size={42} />
            <View style={styles.stampCol}>
              <PenNote size={22}>{praise}</PenNote>
              <Stamp value={`${report.percentile}`} label="Percentile" />
            </View>
          </View>
          <AppText variant="small" color={colors.text}>
            {r.correct} right · {r.incorrect} wrong · {r.unanswered} skipped · {r.accuracy}% accuracy · {formatDuration(report.timeTakenSec)}
          </AppText>
        </View>
      </View>
      {report.autoSubmitted && <Notice tone="warning" title="Submitted automatically">Time ran out, so your saved answers were submitted for you.</Notice>}

      <MarksLeak
        title="Where your marks leaked"
        items={leaks}
        note={<PenNote size={15}>{leaks.some((l) => l.marks > 0) ? 'Plug the biggest leak first — your plan starts there.' : 'Full marks. Nothing leaked!'}</PenNote>}
      />
      {report.improvementPlan[0] ? (
        <MitraSays tone="chalk">{`Start with Day 1: ${report.improvementPlan[0].title}. One focused week.`}</MitraSays>
      ) : null}

      <Card>
        <CardHeader title="Section breakdown" />
        <View style={styles.sections}>
          {r.sections.map((s) => (
            <View key={s.sectionId} style={styles.section}>
              <View style={styles.sectionHead}>
                <AppText variant="smallStrong" style={styles.flex}>{s.name}</AppText>
                <AppText variant="smallStrong">{s.score}/{s.maxScore}</AppText>
              </View>
              <ProgressBar value={s.accuracy} tone={accuracyTone(s.accuracy)} size="sm" label={`${s.name} accuracy`} />
              <AppText variant="caption">{s.correct} correct · {s.incorrect} incorrect · {s.unanswered} skipped · {s.accuracy}% accuracy</AppText>
            </View>
          ))}
        </View>
      </Card>

      <Card>
        <CardHeader title="How useful was this result?" subtitle="Your rating helps us improve the analysis." />
        <RatingStars value={report.rating ?? 0} onChange={(n) => void rate(n)} />
      </Card>

      {next && (
        <Card onPress={() => router.push(`/exams/${next.id}`)} accessibilityLabel={`Recommended next: ${next.title}`} style={styles.next}>
          <AppText variant="caption">Recommended next</AppText>
          <AppText variant="bodyStrong">{next.id === report.examId ? `Retake ${next.shortTitle}` : next.title}</AppText>
          <AppText variant="small" color={colors.primary}>Open exam details</AppText>
        </Card>
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  sheet: { overflow: 'hidden', borderRadius: radii.xl, borderWidth: 1.5, borderColor: paper.ink, backgroundColor: paper.paper },
  sheetBody: { paddingHorizontal: spacing.lg, paddingLeft: 40, paddingBottom: spacing.lg, gap: spacing.md },
  sheetTop: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  scoreRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, flexWrap: 'wrap' },
  stampCol: { alignItems: 'center', gap: 8 },
  row: { flexDirection: 'row', gap: spacing.sm },
  flex: { flex: 1 },
  sections: { gap: spacing.lg },
  section: { gap: 6 },
  sectionHead: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  next: { gap: 4 },
});
