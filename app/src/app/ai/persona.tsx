import { useMemo, useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { backendIds, formatDate, getExamById, type DeepPersona, type MistakeSummary, type RankPrediction } from '@prepmitra/shared';
import { AppText, Button, Card, CardHeader, LoadingSkeleton, ProgressBar, Screen, Select, StatCard } from '@/components';
import { AiErrorNotice, AllowanceBadge, useAiAction, useAiQuery } from '@/features/ai/AiUi';
import { Bullets, MistakeSummaryView, Section } from '@/features/ai/AiViews';
import { aiService } from '@/services/aiService';
import { USE_MOCK } from '@/services';
import { useProfileStore } from '@/store';
import { colors, spacing } from '@/theme';

const tone = (v: number) => (v >= 75 ? 'success' : v >= 50 ? 'warning' : 'error') as 'success' | 'warning' | 'error';
const SPEED = { slow: 'Slower than target', mixed: 'Mixed', on_time: 'On time' } as const;

function DeepCard({ p }: { p: DeepPersona }) {
  return (
    <Card style={styles.gap}>
      <AppText variant="h3">{p.kind === 'ultra' ? 'Ultra strategy review' : 'Deep persona'}</AppText>
      <AppText variant="caption">{formatDate(p.created_at)}{p.next_available_at ? ` · next refresh ${formatDate(p.next_available_at)}` : ''}</AppText>
      <AppText variant="body" style={styles.gapSm}>{p.ai.summary}</AppText>
      <Section title="Strengths"><Bullets items={p.ai.strengths} /></Section>
      <Section title="Risks"><Bullets items={p.ai.risks} /></Section>
      <Section title="Strategy"><Bullets items={p.ai.strategy} ordered /></Section>
      <Section title="Exam-day plan"><AppText variant="small" color={colors.text}>{p.ai.exam_day_plan}</AppText></Section>
    </Card>
  );
}

function Rank() {
  const targets = useProfileStore((s) => s.profile.targetExamIds);
  const exams = useMemo(() => targets.map((id) => getExamById(id)).filter((e): e is NonNullable<typeof e> => !!e), [targets]);
  const [examId, setExamId] = useState(exams[0]?.id ?? '');
  const [rank, setRank] = useState<RankPrediction | null>(null);
  const run = useAiAction(aiService.rank);
  const uuid = backendIds.exams.get(examId) ?? (USE_MOCK ? examId : '');
  return (
    <Card style={styles.gap}>
      <CardHeader title="Rank & cutoff predictor" subtitle="Where your last three mocks put you." />
      {exams.length === 0 ? <AppText variant="small">Add a target exam in your profile to see a prediction.</AppText> : (
        <>
          <Select label="Exam" value={examId} onChange={setExamId} options={exams.map((e) => ({ value: e.id, label: e.shortTitle }))} />
          <Button title="Predict my rank" leftIcon="trophy-outline" style={styles.gapSm} loading={run.busy} disabled={!uuid}
            onPress={async () => { const r = await run.run(uuid); if (r) setRank(r); }} />
          {!uuid ? <AppText variant="caption">Open this exam’s page once so its details load.</AppText> : null}
        </>
      )}
      <AiErrorNotice error={run.error} />
      {rank ? (
        <View style={styles.gapSm}>
          <View style={styles.stats}>
            <StatCard icon="trophy-outline" label="Rank band" value={`${rank.expected_rank_band[0]}–${rank.expected_rank_band[1]}`} />
            <StatCard icon="podium-outline" label="Percentile" value={rank.percentile != null ? String(rank.percentile) : '—'} />
            <StatCard icon="flag-outline" label="Gap to cutoff" value={rank.gap_to_cutoff_points != null ? `${rank.gap_to_cutoff_points}` : '—'} />
          </View>
          <AppText variant="body" style={styles.gapSm}>{rank.ai.explanation}</AppText>
          <Section title="Next steps"><Bullets items={rank.ai.next_steps} ordered /></Section>
          <AppText variant="caption" style={styles.gapSm}>{rank.note}</AppText>
        </View>
      ) : null}
    </Card>
  );
}

function Mistakes() {
  const [s, setS] = useState<MistakeSummary | null>(null);
  const run = useAiAction(aiService.mistakeSummary);
  return (
    <Card style={styles.gap}>
      <CardHeader title="Weekly mistake summary" subtitle="Your open mistakes by error type." />
      {s ? <MistakeSummaryView s={s} /> : (
        <Button title="Show this week’s summary" variant="outline" loading={run.busy} onPress={async () => { const r = await run.run(); if (r) setS(r); }} />
      )}
      <AiErrorNotice error={run.error} />
    </Card>
  );
}

export default function Persona() {
  const persona = useAiQuery(() => aiService.persona(), 'persona');
  const [deep, setDeep] = useState<DeepPersona | null>(null);
  const deepRun = useAiAction(aiService.deepPersona);
  const ultraRun = useAiAction(aiService.ultraReview);
  const p = persona.data;
  return (
    <Screen>
      <View style={styles.row}>
        <Button title="Deep persona" size="sm" variant="outline" leftIcon="sparkles-outline" loading={deepRun.busy} onPress={async () => { const r = await deepRun.run(); if (r) setDeep(r); }} />
        <Button title="Ultra review" size="sm" variant="outline" leftIcon="rocket-outline" loading={ultraRun.busy} onPress={async () => { const r = await ultraRun.run(); if (r) setDeep(r); }} />
      </View>
      <View style={styles.gapSm}><AllowanceBadge feature="ultra_credits" label="Ultra credits" /></View>
      <AiErrorNotice error={deepRun.error ?? ultraRun.error} />
      {deep ? <DeepCard p={deep} /> : null}
      {persona.loading ? <LoadingSkeleton /> : persona.error ? <AiErrorNotice error={persona.error} onRetry={persona.reload} /> : p ? (
        <>
          <Card style={styles.gap}>
            <AppText variant="body">{p.ai.summary}</AppText>
            {p.ai.one_habit_to_change ? <AppText variant="small" style={styles.gapSm}>One habit to change: {p.ai.one_habit_to_change}</AppText> : null}
            <View style={[styles.stats, styles.gapSm]}>
              <StatCard icon="document-text-outline" label="Mocks" value={String(p.mocks_taken)} />
              <StatCard icon="timer-outline" label="Speed" value={SPEED[p.speed_profile] ?? p.speed_profile} />
              <StatCard icon="pulse-outline" label="Consistency" value={p.consistency_score != null ? `${p.consistency_score}` : '—'} />
            </View>
          </Card>
          <Card style={styles.gap}>
            <CardHeader title="Topic mastery" subtitle="Weakest first." />
            <View style={{ gap: spacing.sm }}>
              {p.topic_mastery.slice(0, 10).map((t) => (
                <ProgressBar key={`${t.subject}-${t.topic}`} label={t.topic} value={t.mastery} tone={tone(t.mastery)} showValue valueLabel={String(t.mastery)} />
              ))}
            </View>
          </Card>
          <Card style={styles.gap}>
            <CardHeader title="Where marks go" />
            <View style={{ gap: spacing.sm }}>
              {Object.entries(p.error_mix_percent).map(([k, v]) => (
                <ProgressBar key={k} label={k.replace(/_/g, ' ')} value={v} tone="warning" showValue valueLabel={`${v}%`} />
              ))}
            </View>
          </Card>
          <Rank />
          <Mistakes />
        </>
      ) : null}
    </Screen>
  );
}

const styles = StyleSheet.create({
  gap: { marginTop: spacing.md },
  gapSm: { marginTop: spacing.sm },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  stats: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
});
