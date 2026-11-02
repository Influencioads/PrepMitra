import { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import { EXPERIENCE_LEVELS, formatDuration, formatShortDate } from '@prepmitra/shared';
import {
  AppText, Badge, Card, Divider, EmptyState, IconTile, ListRow, Screen, SegmentedControl, TabHeader,
} from '@/components';
import { useProgress } from '@/hooks/useProgress';
import { selectInterviewReports, useInterviewStore } from '@/store';
import { accuracyTone, colors, spacing } from '@/theme';

type Tab = 'exams' | 'interviews';

export default function Reports() {
  const p = useProgress();
  const interviewReports = selectInterviewReports(useInterviewStore((s) => s.reports));
  const [tab, setTab] = useState<Tab>('exams');

  return (
    <Screen edges={['top', 'left', 'right']}>
      <TabHeader title="Reports" subtitle="Every mock and interview, with detailed feedback." />

      <Card onPress={() => router.push('/progress')} style={styles.progress} accessibilityLabel={`Progress analytics. Average score ${p.avg} percent across ${p.history.length} mocks.`}>
        <IconTile name="analytics-outline" tone="primary" size={44} />
        <View style={styles.flex}>
          <AppText variant="bodyStrong">Progress analytics</AppText>
          <AppText variant="small">
            {p.history.length > 0 ? `Avg ${p.avg}% · best ${p.best}% · ${p.streakDays}-day streak` : 'Trends, topic mastery and weekly practice'}
          </AppText>
        </View>
        <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
      </Card>

      <SegmentedControl<Tab>
        accessibilityLabel="Report type"
        value={tab}
        onChange={setTab}
        segments={[
          { value: 'exams', label: `Exams (${p.history.length})` },
          { value: 'interviews', label: `Interviews (${interviewReports.length})` },
        ]}
      />

      {tab === 'exams' ? (
        p.history.length === 0 ? (
          <EmptyState
            icon="document-text-outline"
            title="No exam reports yet"
            description="Finish a mock exam to get a score, topic analysis and a 7-day plan."
            actionLabel="Browse exams"
            onAction={() => router.push('/explore')}
          />
        ) : (
          <Card style={styles.list}>
            {p.history.map((h, i) => (
              <View key={h.reportId}>
                {i > 0 && <Divider />}
                <ListRow
                  title={h.examTitle}
                  subtitle={`${formatShortDate(h.submittedAt)} · ${h.score}/${h.maxScore} · ${formatDuration(h.timeTakenSec)} · ${h.percentile} %ile`}
                  right={<Badge label={`${h.accuracy}%`} tone={accuracyTone(h.accuracy)} />}
                  onPress={() => router.push(`/reports/${h.reportId}`)}
                  accessibilityHint="Opens the performance report"
                />
              </View>
            ))}
          </Card>
        )
      ) : interviewReports.length === 0 ? (
        <EmptyState
          icon="chatbubbles-outline"
          title="No interview reports yet"
          description="Take a mock interview to get scores, model answers and red flags."
          actionLabel="Choose a role"
          onAction={() => router.push('/interviews')}
        />
      ) : (
        <Card style={styles.list}>
          {interviewReports.map((r, i) => (
            <View key={r.id}>
              {i > 0 && <Divider />}
              <ListRow
                icon={r.mode === 'voice' ? 'mic-outline' : 'chatbubbles-outline'}
                iconTone="secondary"
                title={r.roleTitle}
                subtitle={`${formatShortDate(r.createdAt)} · ${EXPERIENCE_LEVELS.find((l) => l.value === r.level)?.label ?? r.level} · ${r.mode === 'voice' ? 'Voice' : 'Text'}`}
                right={<Badge label={`${r.overall}/10`} tone={accuracyTone(r.overall * 10)} />}
                onPress={() => router.push(`/interview/report/${r.id}`)}
              />
            </View>
          ))}
        </Card>
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  progress: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  flex: { flex: 1 },
  list: { paddingVertical: 4 },
});
