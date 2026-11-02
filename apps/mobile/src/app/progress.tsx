import { useMemo, useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { ExamCategory } from '@prepmitra/shared';
import { EXAM_CATEGORIES, computeProgress, getExamById } from '@prepmitra/shared';
import {
  AppText, BarChart, Card, CardHeader, Chip, EmptyState, LineChart, ProgressBar, Screen, SegmentedControl, StatCard,
} from '@/components';
import { useExamStore } from '@/store';
import { accuracyTone, chartColors, colors, spacing } from '@/theme';

type Range = '7' | '30' | '90' | 'all';
const DAY = 86_400_000;

export default function ProgressScreen() {
  const reports = useExamStore((s) => s.reports);
  const log = useExamStore((s) => s.practiceLog);
  const [category, setCategory] = useState<ExamCategory | 'all'>('all');
  const [range, setRange] = useState<Range>('all');

  const all = useMemo(() => Object.values(reports), [reports]);
  const categories = useMemo(() => {
    const present = new Set(all.map((r) => getExamById(r.examId)?.category).filter(Boolean));
    return EXAM_CATEGORIES.filter((c) => present.has(c.id));
  }, [all]);

  const data = useMemo(() => {
    const now = Date.now();
    const filtered = all.filter((r) => {
      if (category !== 'all' && getExamById(r.examId)?.category !== category) return false;
      if (range !== 'all' && now - new Date(r.createdAt).getTime() > Number(range) * DAY) return false;
      return true;
    });
    const p = computeProgress(filtered, log, now);
    const scores = filtered.map((r) => r.result.percentage);
    const acc = filtered.map((r) => r.result.accuracy);
    const avg = (xs: number[]) => (xs.length ? Math.round(xs.reduce((a, b) => a + b, 0) / xs.length) : 0);
    return { ...p, count: filtered.length, avg: avg(scores), best: scores.length ? Math.max(...scores) : 0, avgAccuracy: avg(acc) };
  }, [all, log, category, range]);

  const trend = data.trend.slice(-10);

  return (
    <Screen>
      <SegmentedControl<Range>
        accessibilityLabel="Date range"
        value={range}
        onChange={setRange}
        segments={[
          { value: '7', label: '7 days' },
          { value: '30', label: '30 days' },
          { value: '90', label: '90 days' },
          { value: 'all', label: 'All' },
        ]}
      />
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chips} accessibilityRole="radiogroup">
        <Chip label="All categories" role="radio" selected={category === 'all'} onPress={() => setCategory('all')} />
        {categories.map((c) => (
          <Chip key={c.id} role="radio" label={c.label} selected={category === c.id} onPress={() => setCategory(c.id)} />
        ))}
      </ScrollView>

      <View style={styles.row}>
        <StatCard label="Mocks" value={data.count} icon="clipboard-outline" />
        <StatCard label="Average score" value={`${data.avg}%`} icon="locate-outline" tone="success" />
      </View>
      <View style={styles.row}>
        <StatCard label="Best score" value={`${data.best}%`} icon="trophy-outline" tone="warning" />
        <StatCard label="Avg accuracy" value={`${data.avgAccuracy}%`} icon="checkmark-done-outline" tone="info" />
      </View>
      <View style={styles.row}>
        <StatCard label="Day streak" value={data.streakDays} icon="flame-outline" tone="error" />
        <StatCard label="Minutes this week" value={data.totalMinutes} icon="time-outline" tone="secondary" />
      </View>

      {data.count === 0 ? (
        <Card>
          <EmptyState
            icon="analytics-outline"
            title="No mocks in this view"
            description="Change the filters, or take a mock to start building your trends."
            actionLabel="Browse exams"
            onAction={() => router.push('/explore')}
          />
        </Card>
      ) : (
        <>
          <Card>
            <CardHeader title="Score trend" subtitle="Percentage score per mock" />
            <LineChart
              labels={trend.map((t) => t.label)}
              series={[{ name: 'Score %', values: trend.map((t) => t.score), color: chartColors[0] }]}
              accessibilityLabel={`Score trend across ${trend.length} mocks, from ${trend[0]?.score ?? 0} to ${trend[trend.length - 1]?.score ?? 0} percent`}
            />
          </Card>
          <Card>
            <CardHeader title="Accuracy trend" subtitle="Correct answers as a share of attempted" />
            <LineChart
              labels={trend.map((t) => t.label)}
              series={[{ name: 'Accuracy %', values: trend.map((t) => t.accuracy), color: chartColors[2] }]}
              accessibilityLabel={`Accuracy trend across ${trend.length} mocks, latest ${trend[trend.length - 1]?.accuracy ?? 0} percent`}
            />
          </Card>
        </>
      )}

      <Card>
        <CardHeader title="Weekly practice" subtitle="Minutes practised over the last 7 days" />
        <BarChart
          labels={data.weekly.map((d) => d.day)}
          values={data.weekly.map((d) => d.minutes)}
          highlightLast
          accessibilityLabel={`Weekly practice: ${data.weekly.map((d) => `${d.day} ${d.minutes} minutes`).join(', ')}`}
        />
      </Card>

      <Card>
        <CardHeader title="Topic mastery" subtitle="Accuracy across every question in each topic" />
        {data.topics.length === 0 ? (
          <AppText variant="small">Topic mastery appears after your first mock.</AppText>
        ) : (
          <View style={styles.topics}>
            {data.topics.map((t) => (
              <View key={t.topic} style={styles.topic}>
                <ProgressBar label={t.topic} value={t.mastery} showValue tone={accuracyTone(t.mastery)} size="sm" />
                <View style={styles.topicMeta}>
                  <AppText variant="caption">{t.attempts} questions</AppText>
                  {t.trend !== 0 && (
                    <View style={styles.trend} accessible accessibilityLabel={`${t.trend > 0 ? 'Up' : 'Down'} ${Math.abs(t.trend)} points since the previous mock`}>
                      <Ionicons name={t.trend > 0 ? 'arrow-up' : 'arrow-down'} size={12} color={t.trend > 0 ? colors.success : colors.error} />
                      <AppText variant="caption" color={t.trend > 0 ? colors.success : colors.error}>{Math.abs(t.trend)}</AppText>
                    </View>
                  )}
                </View>
              </View>
            ))}
          </View>
        )}
      </Card>
    </Screen>
  );
}

const styles = StyleSheet.create({
  chips: { gap: spacing.sm },
  row: { flexDirection: 'row', gap: spacing.sm },
  topics: { gap: spacing.md },
  topic: { gap: 4 },
  topicMeta: { flexDirection: 'row', justifyContent: 'space-between' },
  trend: { flexDirection: 'row', alignItems: 'center', gap: 2 },
});
