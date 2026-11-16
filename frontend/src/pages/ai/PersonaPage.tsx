import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Check, EyeOff, Gauge, Lock, Share2, Sparkles, Target, Zap } from 'lucide-react';
import {
  backendIds, formatDate, formatMarks, formatShortDate, getExamById,
  type CheatCode, type DeepPersona, type ExamPersonaProfile, type MistakeSummary, type PersonaHistoryItem, type PersonaKey, type PersonaTrait, type RankPrediction,
} from '@prepmitra/shared';
import { Badge, Button, ButtonLink, Card, CardBody, CardHeader, LoadingSkeleton, Mitra, ProgressBar, Select, StatCard } from '@/components/ui';
import { AiErrorNotice, AllowanceChip, hasFlag, useAiAction, useAiQuery, useAllowances } from '@/components/ai/AiUi';
import { Bullets, MistakeSummaryView, PdfButton, Section } from '@/components/ai/AiViews';
import { AiNote, Chalkboard, CoachBubble, Eyebrow, HandLine, PersonaIcon, RadarChart, TRAITS, hardCard, softCard } from '@/components/ai/Board';
import { aiService } from '@/services/aiService';
import { USE_MOCK } from '@/services/mock';
import { useProfileStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

const tone = (v: number) => (v >= 75 ? 'success' : v >= 50 ? 'warning' : 'danger') as 'success' | 'warning' | 'danger';
const SPEED = { slow: 'Slower than target', mixed: 'Mixed', on_time: 'On time' };
const short = (name: string) => name.replace(/^The\s+/i, '').split(' ').slice(-1)[0] ?? name;

const TRAIT_CHIP: Record<PersonaTrait, string> = {
  speed: 'bg-primary-soft text-primary',
  risk: 'bg-accent-soft text-warning-ink',
  recovery: 'bg-danger-soft text-pen',
  stamina: 'bg-secondary-soft text-secondary',
  consistency: 'bg-sticky-purple text-[#7e3fa8]',
  accuracy: 'bg-success-soft text-success',
};

// ---------- kept from the previous persona screen (deep persona, ultra review, rank, mistakes) ----------
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
              <StatCard label="Gap to last cutoff" value={rank.gap_to_cutoff_points != null ? `${formatMarks(rank.gap_to_cutoff_points)} marks` : '—'} />
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

/** Topic mastery, error mix, deep persona, ultra review, rank and mistakes — the study-persona tools under the exam persona. */
function MoreFromMitra() {
  const persona = useAiQuery(() => aiService.persona(), 'persona');
  const { data: allow } = useAllowances();
  const [deep, setDeep] = useState<DeepPersona | null>(null);
  const deepRun = useAiAction(aiService.deepPersona);
  const ultraRun = useAiAction(aiService.ultraReview);
  const p = persona.data;
  return (
    <section aria-labelledby="more-persona" className="mt-12">
      <HandLine tone="green">your study persona —</HandLine>
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 id="more-persona" className="text-xl font-bold sm:text-2xl">Deeper reads, rank & mistakes</h2>
          <p className="mt-1 text-sm text-muted">How you learn, where marks leak and what to fix first.</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" loading={deepRun.busy} leftIcon={<Sparkles className="h-4 w-4" />} onClick={async () => { const r = await deepRun.run(); if (r) setDeep(r); }}>
            Deep persona {allow && !hasFlag(allow, 'deep_persona') && <Badge tone="neutral">Pro</Badge>}
          </Button>
          <Button variant="outline" loading={ultraRun.busy} leftIcon={<Gauge className="h-4 w-4" />} onClick={async () => { const r = await ultraRun.run(); if (r) setDeep(r); }}>
            Ultra review
          </Button>
        </div>
      </div>
      <div className="mt-2"><AllowanceChip feature="ultra_credits" label="Ultra credits" /></div>
      <AiErrorNotice error={deepRun.error ?? ultraRun.error} className="mt-4" />
      {deep && <DeepPersonaCard p={deep} />}
      {persona.loading ? <div className="mt-4"><LoadingSkeleton variant="cards" count={2} /></div> : persona.error ? <AiErrorNotice error={persona.error} onRetry={persona.reload} className="mt-4" /> : p && (
        <div className="mt-4 grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Topic mastery" description="Weakest first." />
            <CardBody className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <StatCard label="Speed" value={SPEED[p.speed_profile] ?? p.speed_profile} />
                <StatCard label="Consistency" value={p.consistency_score != null ? `${p.consistency_score}/100` : 'Needs 3 mocks'} />
              </div>
              {p.topic_mastery.length === 0 && <p className="text-sm text-muted">Take a mock to see your topics.</p>}
              {p.topic_mastery.slice(0, 10).map((t) => (
                <div key={`${t.subject}-${t.topic}`}>
                  <div className="mb-1 flex justify-between gap-2 text-sm"><span className="min-w-0">{t.topic} {t.trend && <span className="text-xs text-muted">({t.trend})</span>}</span><span className="font-medium">{t.mastery}</span></div>
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
    </section>
  );
}

// ---------- the exam persona ----------
const PLAN_KEY = 'pm-persona-plan';
function readPlan(): string[] | null {
  try { const v = localStorage.getItem(PLAN_KEY); return v ? (JSON.parse(v) as string[]) : null; } catch { return null; }
}

function Hero({ profile, coach }: { profile: ExamPersonaProfile; coach?: string }) {
  const me = profile.personas.find((p) => p.key === profile.persona)!;
  const last = profile.history[profile.history.length - 1];
  return (
    <Chalkboard className="relative overflow-hidden p-5 sm:p-8" ariaLabel="Your exam persona">
      <div className="flex flex-col gap-6 md:flex-row md:items-center">
        <div className="min-w-0 flex-1">
          <Eyebrow tone="chalk" dot>Mitra · AI persona read</Eyebrow>
          <p className="mt-3 font-hand text-lg text-marigold sm:text-xl">after {profile.answers} answers, I think you are —</p>
          <h2 className="mt-1 text-4xl font-extrabold leading-tight !text-chalk-text sm:text-5xl lg:text-6xl">{me.name}</h2>
          <svg viewBox="0 0 240 12" className="mt-1 h-3 w-48 sm:w-60" aria-hidden><path d="M2 8 Q 60 2 120 7 T 238 5" stroke="#f28c28" strokeWidth={3} fill="none" strokeLinecap="round" /></svg>
          <p className="mt-3 max-w-xl text-sm leading-relaxed text-chalk-text/85 sm:text-base">{me.description}</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {profile.confidence && (
              <span className="rounded-full border border-white/15 bg-chalk-deep px-3 py-1 text-xs font-semibold">
                Confidence: {profile.confidence} · based on {profile.mocks_taken} mock{profile.mocks_taken === 1 ? '' : 's'}, {profile.answers} answers
              </span>
            )}
            {(profile.same_persona_streak ?? 0) > 1 && (
              <span className="rounded-full border border-white/15 bg-chalk-deep px-3 py-1 text-xs font-semibold">Same persona {profile.same_persona_streak} mocks in a row</span>
            )}
          </div>
          {coach && <CoachBubble className="mt-5 max-w-xl">{coach}</CoachBubble>}
        </div>
        <div className="flex shrink-0 flex-col items-center gap-2 self-center">
          <div className="flex h-36 w-36 items-center justify-center rounded-full border-4 border-dashed border-chalk-deep bg-marigold text-pen ring-[6px] ring-marigold sm:h-44 sm:w-44">
            <PersonaIcon name={me.icon} className="h-16 w-16 stroke-[1.8] sm:h-20 sm:w-20" />
          </div>
          {last && <p className="font-hand text-base text-marigold">badge earned · Mock {profile.history.length}</p>}
        </div>
      </div>
    </Chalkboard>
  );
}

function PersonaCompare({ profile }: { profile: ExamPersonaProfile }) {
  const [sel, setSel] = useState<PersonaKey>(profile.persona!);
  const p = profile.personas.find((x) => x.key === sel) ?? profile.personas[0]!;
  const match = profile.matches.find((m) => m.key === sel)?.match;
  const mine = sel === profile.persona;
  return (
    <section aria-labelledby="compare" className="mt-10">
      <HandLine>the six exam-takers —</HandLine>
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <h2 id="compare" className="text-xl font-bold sm:text-2xl">Which one are you? Tap to compare.</h2>
        <p className="text-xs text-muted">Your shape stays saffron. The persona you pick is drawn dashed.</p>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-2.5 sm:grid-cols-3 lg:grid-cols-6" role="tablist" aria-label="Personas">
        {profile.personas.map((x) => (
          <button key={x.key} type="button" role="tab" aria-selected={sel === x.key} onClick={() => setSel(x.key)}
            className={cn('relative flex min-h-[84px] flex-col items-start justify-between gap-2 rounded-xl border p-3 text-left text-sm font-semibold transition',
              sel === x.key ? 'border-[1.5px] border-ink bg-sticky-yellow shadow-[3px_4px_0_#1c2321]' : 'border-line bg-card hover:border-ink')}>
            <PersonaIcon name={x.icon} className={cn('h-5 w-5', x.key === profile.persona ? 'text-primary' : 'text-secondary')} />
            <span>{x.name}</span>
            {x.key === profile.persona && <span className="absolute right-2 top-2 rounded-full bg-primary px-2 py-0.5 text-[10px] font-bold text-white">YOU</span>}
          </button>
        ))}
      </div>
      <div className="mt-4 grid gap-4 lg:grid-cols-2">
        <div className={cn(hardCard, 'flex flex-col p-5')} role="tabpanel" aria-label={p.name}>
          <div className="flex items-center gap-3">
            <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border-[1.5px] border-ink bg-marigold"><PersonaIcon name={p.icon} className="h-5 w-5 text-pen" /></span>
            <div>
              <h3 className="text-xl font-bold">{p.name}</h3>
              <p className="font-hand text-pen">{p.tagline}</p>
            </div>
          </div>
          <p className="mt-3 text-sm leading-relaxed">{p.description}</p>
          <Eyebrow className="mt-4">How Mitra spots it</Eyebrow>
          <ul className="mt-2 space-y-1.5 text-sm">
            {p.signals.map((s) => <li key={s} className="flex gap-2"><Check className="mt-0.5 h-4 w-4 shrink-0 text-secondary" aria-hidden />{s}</li>)}
          </ul>
          {match != null && (
            <p className={cn('mt-5 rounded-lg px-3 py-2 text-sm font-semibold', mine ? 'bg-primary-soft text-primary' : 'bg-surface text-muted')}>
              {mine ? `This is you — ${match}% trait match across ${profile.answers} answers.` : `${match}% trait match with you.`}
            </p>
          )}
        </div>
        <div className={cn(softCard, 'p-5')}>
          <div className="flex flex-wrap items-center justify-between gap-2">
            <h3 className="font-bold">Trait shape</h3>
            <div className="flex flex-wrap gap-3 text-xs text-muted">
              <span className="inline-flex items-center gap-1.5"><span className="h-0.5 w-4 bg-primary" aria-hidden />You</span>
              <span className="inline-flex items-center gap-1.5"><span className="w-4 border-t-2 border-dashed border-secondary" aria-hidden />{p.name}</span>
            </div>
          </div>
          <div className="mt-2 flex justify-center">
            <RadarChart series={[
              { label: 'You', values: profile.traits!, color: '#c2410c', fill: true },
              { label: p.name, values: p.shape, color: '#1e5e47', dashed: true },
            ]} />
          </div>
        </div>
      </div>
    </section>
  );
}

function Evidence({ profile }: { profile: ExamPersonaProfile }) {
  const [filter, setFilter] = useState<PersonaTrait | 'all'>('all');
  const items = profile.evidence.filter((e) => filter === 'all' || e.trait === filter);
  const label = (t: PersonaTrait) => TRAITS.find((x) => x.key === t)?.label ?? t;
  return (
    <section aria-labelledby="evidence" className="mt-10">
      <HandLine tone="pen">the evidence —</HandLine>
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <h2 id="evidence" className="text-xl font-bold sm:text-2xl">What your answers actually did</h2>
        <p className="text-xs text-muted">Counts and timings are measured by code from your attempts.</p>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {(['all', ...TRAITS.map((t) => t.key)] as const).map((k) => (
          <button key={k} type="button" aria-pressed={filter === k} onClick={() => setFilter(k)}
            className={cn('rounded-full border px-3.5 py-1.5 text-sm font-semibold transition', filter === k ? 'border-ink bg-ink text-white' : 'border-line-strong bg-card hover:border-ink')}>
            {k === 'all' ? 'All' : label(k)}
          </button>
        ))}
      </div>
      <div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {items.map((e) => (
          <article key={e.title} className="rounded-[16px] border-[1.5px] border-ink bg-card p-4">
            <div className="flex items-start justify-between gap-2">
              <span className={cn('rounded-full px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider', TRAIT_CHIP[e.trait])}>{label(e.trait)}</span>
              <span className="text-right font-hand text-lg leading-tight text-pen sm:text-xl">{e.stat}</span>
            </div>
            <h3 className="mt-3 font-bold leading-snug">{e.title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted">{e.body}</p>
          </article>
        ))}
        {items.length === 0 && <p className="text-sm text-muted">No evidence for this trait yet.</p>}
      </div>
    </section>
  );
}

function Notes({ profile }: { profile: ExamPersonaProfile }) {
  const tilt = [-0.6, 0.5, -0.3];
  return (
    <section className="mt-10 grid gap-6 md:grid-cols-2">
      <div>
        <h2 className="flex items-center gap-2 text-lg font-bold"><Zap className="h-5 w-5 text-secondary" aria-hidden /> Superpowers</h2>
        <div className="mt-3 space-y-3">
          {profile.superpowers.map((n, i) => (
            <div key={n.title} className="bg-sticky-green p-4 shadow-sticky" style={{ transform: `rotate(${tilt[i % 3]}deg)` }}>
              <h3 className="font-hand text-lg font-bold text-secondary">{n.title}</h3>
              <p className="mt-1 text-sm">{n.body}</p>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 className="flex items-center gap-2 text-lg font-bold"><EyeOff className="h-5 w-5 text-pen" aria-hidden /> Blind spots</h2>
        <div className="mt-3 space-y-3">
          {profile.blind_spots.map((n, i) => (
            <div key={n.title} className="bg-sticky-yellow p-4 shadow-sticky" style={{ transform: `rotate(${-tilt[i % 3]!}deg)` }}>
              <h3 className="font-hand text-lg font-bold text-pen">{n.title}</h3>
              <p className="mt-1 text-sm">{n.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function GamePlan({ profile, codes }: { profile: ExamPersonaProfile; codes: CheatCode[] }) {
  const me = profile.personas.find((p) => p.key === profile.persona)!;
  const [onPlan, setOnPlan] = useState<string[]>(() => readPlan() ?? profile.plan.slice(0, 1).map((s) => s.code_id));
  useEffect(() => { try { localStorage.setItem(PLAN_KEY, JSON.stringify(onPlan)); } catch { /* storage unavailable */ } }, [onPlan]);
  const count = profile.plan.filter((s) => onPlan.includes(s.code_id)).length;
  return (
    <Chalkboard className="mt-10 p-5 sm:p-7" ariaLabel="Mitra's game plan">
      <HandLine tone="chalk">Mitra’s game plan —</HandLine>
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <h2 className="text-xl font-bold !text-chalk-text sm:text-2xl">How to beat {me.name}</h2>
        <p className="text-xs font-semibold text-chalk-text/80">{count} of {profile.plan.length} strategies on your plan</p>
      </div>
      <div className="mt-5 grid gap-4 md:grid-cols-3">
        {profile.plan.map((s, i) => {
          const code = codes.find((c) => c.id === s.code_id);
          const added = onPlan.includes(s.code_id);
          return (
            <div key={s.title} className={cn('flex flex-col rounded-xl border border-dashed border-white/35 p-4', added && 'bg-white/[0.06]')}>
              <p className="font-hand text-4xl leading-none text-accent">{i + 1}</p>
              <h3 className="mt-3 font-bold !text-chalk-text">{s.title}</h3>
              <p className="mt-2 flex-1 font-hand text-base leading-snug text-chalk-text/90">{s.body}</p>
              <span className="mt-3 inline-flex w-fit items-center gap-1.5 rounded-md bg-marigold px-2 py-1 text-xs font-semibold text-ink">
                <Lock className="h-3 w-3" aria-hidden /> Cheat code · {code?.title ?? s.code_id.replace(/-/g, ' ')}
              </span>
              <div className="mt-4 flex flex-wrap gap-2">
                <ButtonLink to={`/ai/cheat-codes?drill=${encodeURIComponent(s.code_id)}`} size="sm" className="rounded-full">Start 3-Q drill →</ButtonLink>
                <button type="button" aria-pressed={added} onClick={() => setOnPlan((x) => (added ? x.filter((c) => c !== s.code_id) : [...x, s.code_id]))}
                  className={cn('h-8 rounded-full border px-3 text-sm font-semibold transition', added ? 'border-paper bg-paper text-ink' : 'border-white/60 text-chalk-text hover:bg-white/10')}>
                  {added ? 'On my plan ✓' : 'Add to my plan'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
      <p className="mt-4 text-xs text-chalk-text/70">AI-generated suggestions — check with your teacher if unsure.</p>
    </Chalkboard>
  );
}

function rushedNote(h: PersonaHistoryItem, best: boolean) {
  const parts = [best ? 'Best yet.' : ''];
  if (h.rushed > 0) parts.push(`${best ? 'Still ' : ''}${h.rushed} rushed answers, and ${h.rushed_wrong} of them ${h.rushed_wrong === 1 ? 'was' : 'were'} wrong.`);
  else parts.push('No rushed answers in this mock.');
  return parts.filter(Boolean).join(' ');
}

function Timeline({ profile }: { profile: ExamPersonaProfile }) {
  const h = profile.history;
  const [sel, setSel] = useState(h.length - 1);
  const cur = h[sel];
  if (!cur) return null;
  const best = Math.max(...h.map((x) => x.score));
  const deducted = cur.right - cur.score;
  return (
    <section className={cn(softCard, 'p-5')} aria-labelledby="timeline">
      <HandLine>persona over time —</HandLine>
      <h2 id="timeline" className="text-lg font-bold sm:text-xl">Mock 1 → Mock {h.length}</h2>
      <ol className="relative mt-5 grid" style={{ gridTemplateColumns: `repeat(${h.length}, minmax(0, 1fr))` }}>
        <span aria-hidden className="absolute left-[12%] right-[12%] top-5 h-0.5 bg-primary" />
        {h.map((x, i) => (
          <li key={x.attempt_id} className="relative flex flex-col items-center text-center">
            <button type="button" onClick={() => setSel(i)} aria-pressed={sel === i} aria-label={`Mock ${i + 1}: ${formatMarks(x.score)} marks, ${x.persona_name}`}
              className={cn('flex h-10 w-10 items-center justify-center rounded-full border-2 border-ink text-sm font-bold transition',
                i === h.length - 1 ? 'bg-primary text-white' : i === 0 ? 'bg-secondary-soft' : 'bg-card', sel === i && 'ring-4 ring-accent/40')}>
              {formatMarks(x.score)}
            </button>
            <span className="mt-1.5 text-xs font-semibold">Mock {i + 1}</span>
            <span className="text-[11px] text-muted">{short(x.persona_name)}</span>
          </li>
        ))}
      </ol>
      <div className="mt-5 rounded-xl border border-line bg-paper p-4">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <p className="font-bold">Mock {sel + 1} · {formatShortDate(cur.date)}</p>
          <p className="text-xs font-semibold text-primary">{cur.persona_name}</p>
        </div>
        <p className="mt-1 font-hand text-lg leading-snug text-pen">{rushedNote(cur, cur.score === best && h.length > 1)}</p>
        <p className="mt-2 text-xs text-muted">
          {cur.attempted} attempted · {cur.right} right · {cur.wrong} wrong → {cur.right} − {formatMarks(deducted)} = {formatMarks(cur.score)} marks
        </p>
      </div>
    </section>
  );
}

function ShareCard({ profile }: { profile: ExamPersonaProfile }) {
  const [style, setStyle] = useState<'chalk' | 'paper'>('chalk');
  const [showScore, setShowScore] = useState(true);
  const me = profile.personas.find((p) => p.key === profile.persona)!;
  const h = profile.history;
  const last = h[h.length - 1];
  const up = last && h.length > 1 ? last.score - h[0]!.score : 0;
  const scoreLine = last ? `Mock ${h.length} · ${formatMarks(last.score)}/${formatMarks(last.max_score)}${up > 0 ? ` · up ${formatMarks(up)} since Mock 1` : ''}` : '';
  const share = async () => {
    const text = `My exam persona is ${me.name} — ${me.tagline}.${showScore && scoreLine ? ` ${scoreLine}.` : ''} Which one are you? 6 personas, read by Mitra on PrepMithra.`;
    try {
      if (navigator.share) await navigator.share({ title: 'My exam persona', text });
      else { await navigator.clipboard.writeText(text); toast.success('Copied — paste it anywhere.'); }
    } catch { /* cancelled */ }
  };
  const chalk = style === 'chalk';
  return (
    <section aria-labelledby="share">
      <div className="flex items-center justify-between gap-3">
        <h2 id="share" className="text-lg font-bold sm:text-xl">Share card</h2>
        <div className="flex rounded-full bg-surface p-1 text-sm font-semibold" role="group" aria-label="Card style">
          {(['chalk', 'paper'] as const).map((s) => (
            <button key={s} type="button" aria-pressed={style === s} onClick={() => setStyle(s)}
              className={cn('rounded-full px-3.5 py-1.5 capitalize', style === s ? 'bg-ink text-white' : 'text-muted')}>{s}</button>
          ))}
        </div>
      </div>
      <div className={cn('mt-4 flex items-center gap-4 rounded-[20px] p-5 sm:p-6', chalk ? 'border-[7px] border-wood bg-chalkboard text-chalk-text' : 'border-[1.5px] border-ink bg-notebook text-ink shadow-[4px_5px_0_#1c2321]')}>
        <div className="min-w-0 flex-1">
          <p className="text-sm font-bold">Prep<span className="text-accent">Mithra</span> <span className={cn('rounded px-1 text-[10px]', chalk ? 'bg-secondary text-white' : 'bg-secondary-soft text-secondary')}>AI</span></p>
          <p className={cn('mt-1 font-hand', chalk ? 'text-marigold' : 'text-pen')}>my exam persona is</p>
          <p className={cn('font-display text-2xl font-extrabold leading-tight sm:text-3xl')}>{me.name}</p>
          {showScore && scoreLine && <p className="mt-1 text-xs font-semibold">{scoreLine}</p>}
          <p className={cn('mt-1 text-xs', chalk ? 'text-chalk-text/75' : 'text-muted')}>Which one are you? 6 personas, read by Mitra</p>
        </div>
        <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full border-2 border-ink bg-marigold text-pen sm:h-20 sm:w-20"><PersonaIcon name={me.icon} className="h-8 w-8 sm:h-10 sm:w-10" /></span>
      </div>
      <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
        <label className="inline-flex cursor-pointer items-center gap-2 text-sm font-semibold">
          <button type="button" role="switch" aria-checked={showScore} aria-label={`Show my Mock ${h.length} score`} onClick={() => setShowScore((v) => !v)}
            className={cn('relative inline-flex h-6 w-11 items-center rounded-full border-[1.5px] border-ink transition-colors', showScore ? 'bg-primary' : 'bg-stone-300')}>
            <span className={cn('inline-block h-4 w-4 rounded-full bg-card shadow transition-transform', showScore ? 'translate-x-5' : 'translate-x-1')} />
          </button>
          Show my Mock {h.length} score
        </label>
        <Button onClick={share} className="rounded-full shadow-[3px_3px_0_#1c2321]" leftIcon={<Share2 className="h-4 w-4" />}>Share my persona</Button>
      </div>
      <AiNote tone="green" className="mt-3 inline-block">AI-generated from your attempts. Scores themselves are calculated by code.</AiNote>
    </section>
  );
}

export function PersonaPage() {
  useDocumentTitle('Your exam persona');
  const profile = useAiQuery(() => aiService.personaProfile(), 'persona-profile');
  const snapshot = useAiQuery(() => aiService.persona(), 'persona-coach');
  const codes = useAiQuery(() => aiService.cheatCodes(), 'persona-codes');
  const p = profile.data;
  const coach = snapshot.data?.ai.one_habit_to_change || snapshot.data?.ai.summary;
  const ready = p && p.persona && p.traits && p.personas.some((x) => x.key === p.persona);

  return (
    <div className="min-w-0">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          {p && p.mocks_taken > 0 && <HandLine>after {p.mocks_taken} mock{p.mocks_taken === 1 ? '' : 's'}</HandLine>}
          <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">Your exam persona</h1>
        </div>
        <AiNote className="inline-flex w-fit items-center gap-1.5"><Sparkles className="h-3 w-3" aria-hidden /> AI-generated from your attempts. Scores themselves are calculated by code.</AiNote>
      </div>

      {profile.loading ? <LoadingSkeleton variant="page" /> : profile.error ? <AiErrorNotice error={profile.error} onRetry={profile.reload} /> : !ready ? (
        <Chalkboard className="p-6 sm:p-10" ariaLabel="No persona yet">
          <div className="flex flex-col items-start gap-5 sm:flex-row sm:items-center">
            <Mitra size={64} />
            <div className="min-w-0 flex-1">
              <Eyebrow tone="chalk" dot>Mitra · AI persona read</Eyebrow>
              <h2 className="mt-2 text-2xl font-bold !text-chalk-text sm:text-3xl">Take one mock and I will read your exam persona</h2>
              <p className="mt-2 max-w-xl font-hand text-lg text-chalk-text/85">Fast Guesser? Perfectionist? Section Hopper? I need your answers and timings from one full mock to tell.</p>
            </div>
            <ButtonLink to="/exams" className="rounded-full">Take a mock →</ButtonLink>
          </div>
        </Chalkboard>
      ) : (
        <>
          <Hero profile={p} coach={coach} />
          <PersonaCompare profile={p} />
          {p.evidence.length > 0 && <Evidence profile={p} />}
          {(p.superpowers.length > 0 || p.blind_spots.length > 0) && <Notes profile={p} />}
          {p.plan.length > 0 && <GamePlan profile={p} codes={codes.data?.items ?? []} />}
          {p.history.length > 0 && (
            <div className="mt-10 grid gap-6 lg:grid-cols-2">
              <Timeline profile={p} />
              <ShareCard profile={p} />
            </div>
          )}
          <div className="mt-6 flex flex-wrap items-center gap-3 rounded-xl bg-secondary-soft p-4 text-sm">
            <Eyebrow tone="green">Next persona check</Eyebrow>
            <span className="text-secondary">Mitra re-reads your persona after every mock. Next check after Mock {p.mocks_taken + 1}.</span>
            <Link to="/exams" className="font-semibold text-primary underline-offset-4 hover:underline">Take Mock {p.mocks_taken + 1} →</Link>
          </div>
        </>
      )}

      <MoreFromMitra />
    </div>
  );
}
