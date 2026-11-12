import { useMemo, useState } from 'react';
import { Gauge, Sparkles, Target } from 'lucide-react';
import { backendIds, formatDate, getExamById, type DeepPersona, type MistakeSummary, type RankPrediction } from '@prepmitra/shared';
import { Badge, Button, Card, CardBody, CardHeader, LoadingSkeleton, PageHeader, ProgressBar, Select, StatCard } from '@/components/ui';
import { AiErrorNotice, AllowanceChip, hasFlag, useAiAction, useAiQuery, useAllowances } from '@/components/ai/AiUi';
import { Bullets, MistakeSummaryView, PdfButton, Section } from '@/components/ai/AiViews';
import { aiService } from '@/services/aiService';
import { USE_MOCK } from '@/services/mock';
import { useProfileStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

const tone = (v: number) => (v >= 75 ? 'success' : v >= 50 ? 'warning' : 'danger') as 'success' | 'warning' | 'danger';
const SPEED = { slow: 'Slower than target', mixed: 'Mixed', on_time: 'On time' };

function DeepPersonaCard({ p }: { p: DeepPersona }) {
  return (
    <Card className="mt-4 border-primary/30"><CardBody>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="text-lg font-bold">{p.kind === 'ultra' ? 'Ultra strategy review' : 'Deep persona'}</h3>
        <span className="text-xs text-muted">{formatDate(p.created_at)}{p.next_available_at ? ` · next refresh ${formatDate(p.next_available_at)}` : ''}</span>
      </div>
      <p className="mt-2 text-sm leading-relaxed">{p.ai.summary}</p>
      <div className="grid gap-4 md:grid-cols-2">
        <Section title="Strengths"><Bullets items={p.ai.strengths} /></Section>
        <Section title="Risks"><Bullets items={p.ai.risks} /></Section>
      </div>
      <Section title="Strategy"><Bullets items={p.ai.strategy} ordered /></Section>
      <Section title="Exam-day plan"><p className="text-sm">{p.ai.exam_day_plan}</p></Section>
      {p.ai.learning_style && <p className="mt-3 text-xs text-muted">Learning style: {p.ai.learning_style}</p>}
    </CardBody></Card>
  );
}

function RankCard() {
  const targets = useProfileStore((s) => s.profile.targetExamIds);
  const exams = useMemo(() => targets.map((id) => getExamById(id)).filter((e): e is NonNullable<typeof e> => !!e), [targets]);
  const [examId, setExamId] = useState(exams[0]?.id ?? '');
  const [rank, setRank] = useState<RankPrediction | null>(null);
  const run = useAiAction(aiService.rank);
  const uuid = backendIds.exams.get(examId) ?? (USE_MOCK ? examId : '');
  return (
    <Card>
      <CardHeader title="Rank & cutoff predictor" description="Where your last three mocks put you among PrepMitra test-takers." />
      <CardBody>
        {exams.length === 0 ? <p className="text-sm text-muted">Add a target exam in your profile to see a prediction.</p> : (
          <div className="flex flex-wrap items-end gap-3">
            <Select label="Exam" value={examId} onChange={(e) => setExamId(e.target.value)} options={exams.map((e) => ({ value: e.id, label: e.shortTitle }))} containerClassName="min-w-48 flex-1" />
            <Button loading={run.busy} disabled={!uuid} leftIcon={<Target className="h-4 w-4" />} onClick={async () => { const r = await run.run(uuid); if (r) setRank(r); }}>Predict</Button>
          </div>
        )}
        {examId && !uuid && <p className="mt-2 text-xs text-muted">Open the exam’s page once so its details load, then predict.</p>}
        <AiErrorNotice error={run.error} className="mt-3" onRetry={() => run.run(uuid).then((r) => r && setRank(r))} />
        {rank && (
          <div className="mt-4">
            <div className="grid gap-3 sm:grid-cols-3">
              <StatCard label="Expected rank band" value={`${rank.expected_rank_band[0].toLocaleString('en-IN')}–${rank.expected_rank_band[1].toLocaleString('en-IN')}`} />
              <StatCard label="Percentile" value={rank.percentile != null ? `${rank.percentile}` : '—'} />
              <StatCard label="Gap to last cutoff" value={rank.gap_to_cutoff_points != null ? `${rank.gap_to_cutoff_points} marks` : '—'} />
            </div>
            <p className="mt-3 text-sm leading-relaxed">{rank.ai.explanation}</p>
            <Section title="Next steps"><Bullets items={rank.ai.next_steps} ordered /></Section>
            <p className="mt-3 text-xs text-muted">{rank.note} Based on {rank.prepmitra_test_takers.toLocaleString('en-IN')} test-takers; your last-3 average is {rank.average_score_percent_last_3}%.</p>
          </div>
        )}
      </CardBody>
    </Card>
  );
}

function MistakesCard() {
  const { data: allow } = useAllowances();
  const [s, setS] = useState<MistakeSummary | null>(null);
  const run = useAiAction(aiService.mistakeSummary);
  const locked = allow && !hasFlag(allow, 'mistake_notebook');
  return (
    <Card>
      <CardHeader title="Weekly mistake summary" description="Your open mistakes grouped by error type, with what to do this week."
        action={s?.artifactId ? <PdfButton id={s.artifactId} /> : undefined} />
      <CardBody>
        {!s && <Button variant="outline" loading={run.busy} onClick={async () => { const r = await run.run(); if (r) setS(r); }}>{locked ? 'Starter plan feature: see why' : 'Show this week’s summary'}</Button>}
        <AiErrorNotice error={run.error} className="mt-3" />
        {s && <MistakeSummaryView s={s} />}
        {s?.artifactId && <p className="mt-3 text-xs text-muted">The visual PDF is part of AI Tutor Pro and the Topper Combo.</p>}
      </CardBody>
    </Card>
  );
}

export function PersonaPage() {
  useDocumentTitle('Persona & rank');
  const persona = useAiQuery(() => aiService.persona(), 'persona');
  const { data: allow } = useAllowances();
  const [deep, setDeep] = useState<DeepPersona | null>(null);
  const deepRun = useAiAction(aiService.deepPersona);
  const ultraRun = useAiAction(aiService.ultraReview);
  const p = persona.data;

  return (
    <div>
      <PageHeader title="Your study persona" description="How you learn, where marks leak and what to fix first, from your own mocks."
        actions={<>
          <Button variant="outline" loading={deepRun.busy} leftIcon={<Sparkles className="h-4 w-4" />} onClick={async () => { const r = await deepRun.run(); if (r) setDeep(r); }}>
            Deep persona {allow && !hasFlag(allow, 'deep_persona') && <Badge tone="neutral">Pro</Badge>}
          </Button>
          <Button variant="outline" loading={ultraRun.busy} leftIcon={<Gauge className="h-4 w-4" />} onClick={async () => { const r = await ultraRun.run(); if (r) setDeep(r); }}>
            Ultra review
          </Button>
        </>} />
      <div className="-mt-3 mb-4"><AllowanceChip feature="ultra_credits" label="Ultra credits" /></div>
      <AiErrorNotice error={deepRun.error ?? ultraRun.error} className="mb-4" />
      {deep && <DeepPersonaCard p={deep} />}

      {persona.loading ? <LoadingSkeleton variant="page" /> : persona.error ? <AiErrorNotice error={persona.error} onRetry={persona.reload} /> : p && (
        <div className="mt-4 grid gap-6 lg:grid-cols-2">
          <Card className="lg:col-span-2"><CardBody>
            <p className="text-sm leading-relaxed">{p.ai.summary}</p>
            {p.ai.one_habit_to_change && <p className="mt-2 text-sm"><span className="font-semibold">One habit to change:</span> {p.ai.one_habit_to_change}</p>}
            <div className="mt-4 grid gap-3 sm:grid-cols-4">
              <StatCard label="Mocks analysed" value={String(p.mocks_taken)} />
              <StatCard label="Latest score" value={p.recent_score_percent[0] != null ? `${p.recent_score_percent[0]}%` : '—'} />
              <StatCard label="Speed" value={SPEED[p.speed_profile] ?? p.speed_profile} />
              <StatCard label="Consistency" value={p.consistency_score != null ? `${p.consistency_score}/100` : 'Needs 3 mocks'} />
            </div>
          </CardBody></Card>
          <Card>
            <CardHeader title="Topic mastery" description="Weakest first." />
            <CardBody className="space-y-3">
              {p.topic_mastery.length === 0 && <p className="text-sm text-muted">Take a mock to see your topics.</p>}
              {p.topic_mastery.slice(0, 10).map((t) => (
                <div key={`${t.subject}-${t.topic}`}>
                  <div className="mb-1 flex justify-between text-sm"><span>{t.topic} {t.trend && <span className="text-xs text-muted">({t.trend})</span>}</span><span className="font-medium">{t.mastery}</span></div>
                  <ProgressBar value={t.mastery} tone={tone(t.mastery)} />
                </div>
              ))}
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Where marks go" description="Share of your mistakes by type." />
            <CardBody className="space-y-3">
              {Object.entries(p.error_mix_percent).map(([k, v]) => (
                <div key={k}>
                  <div className="mb-1 flex justify-between text-sm"><span className="capitalize">{k.replace(/_/g, ' ')}</span><span>{v}%</span></div>
                  <ProgressBar value={v} tone="warning" />
                </div>
              ))}
              {p.slow_topics.length > 0 && <p className="pt-2 text-sm text-muted">Slow on: {p.slow_topics.join(', ')}</p>}
            </CardBody>
          </Card>
          <RankCard />
          <MistakesCard />
        </div>
      )}
    </div>
  );
}
