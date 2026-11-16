import { useEffect, useMemo, useState } from 'react';
import { Pressable, ScrollView, Share, StyleSheet, Switch, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  backendIds, formatDate, formatMarks, getExamById, type DeepPersona, type ExamPersonaProfile, type MistakeSummary, type PersonaKey,
  type PersonaSnapshot, type PersonaTrait, type RankPrediction,
} from '@prepmitra/shared';
import { AppText, Button, Card, CardHeader, LoadingSkeleton, ProgressBar, Screen, SegmentedControl, Select, StatCard, toast } from '@/components';
import { AiErrorNotice, AllowanceBadge, useAiAction, useAiQuery } from '@/features/ai/AiUi';
import { Bullets, MistakeSummaryView, Section } from '@/features/ai/AiViews';
import {
  AiNote, Chalkboard, ChalkChip, ChipScroller, CoachBubble, Hand, Label, Medal, MitraTag, Pill, SectionHead, Sticky, TRAIT_LABEL, TraitRadar,
  board, boardStyles, personaIcon,
} from '@/features/ai/Board';
import { aiService } from '@/services/aiService';
import { USE_MOCK } from '@/services';
import { useProfileStore } from '@/store';
import { colors, paper, radii, spacing } from '@/theme';

const PLAN_KEY = 'pm.persona.plan';
const tone = (v: number) => (v >= 75 ? 'success' : v >= 50 ? 'warning' : 'error') as 'success' | 'warning' | 'error';
const SPEED = { slow: 'Slower than target', mixed: 'Mixed', on_time: 'On time' } as const;
const TRAIT_TONE: Record<PersonaTrait, { bg: string; fg: string }> = {
  speed: { bg: board.saffronSoft, fg: colors.primary },
  risk: { bg: '#FDF0D5', fg: colors.warningText },
  recovery: { bg: colors.errorSoft, fg: paper.pen },
  stamina: { bg: colors.secondarySoft, fg: colors.secondary },
  consistency: { bg: paper.stickyPurple, fg: '#7E22CE' },
  accuracy: { bg: colors.successSoft, fg: colors.success },
};
const shortName = (name: string) => name.replace(/^The\s+/i, '').split(' ').slice(-1)[0] ?? name;

// ---------- existing deep persona / rank / mistakes (kept, lower on the screen) ----------
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

/** Deep persona, ultra review, topic mastery, where marks go, rank and mistakes — the tools from before the redesign. */
function MoreFromMitra({ persona }: { persona: ReturnType<typeof useAiQuery<PersonaSnapshot>> }) {
  const [deep, setDeep] = useState<DeepPersona | null>(null);
  const deepRun = useAiAction(aiService.deepPersona);
  const ultraRun = useAiAction(aiService.ultraReview);
  const p = persona.data;
  return (
    <View>
      <SectionHead kicker="go deeper —" title="Deep persona & rank" caption="Longer reads, topic mastery and where your rank lands." />
      <View style={[styles.row, styles.gapSm]}>
        <Button title="Deep persona" size="sm" variant="outline" leftIcon="sparkles-outline" loading={deepRun.busy} onPress={async () => { const r = await deepRun.run(); if (r) setDeep(r); }} />
        <Button title="Ultra review" size="sm" variant="outline" leftIcon="rocket-outline" loading={ultraRun.busy} onPress={async () => { const r = await ultraRun.run(); if (r) setDeep(r); }} />
      </View>
      <View style={styles.gapSm}><AllowanceBadge feature="ultra_credits" label="Ultra credits" /></View>
      <AiErrorNotice error={deepRun.error ?? ultraRun.error} />
      {deep ? <DeepCard p={deep} /> : null}
      {persona.loading ? <LoadingSkeleton variant="card" /> : persona.error ? <AiErrorNotice error={persona.error} onRetry={persona.reload} /> : p ? (
        <>
          <Card style={styles.gap}>
            {p.ai.one_habit_to_change ? <AppText variant="small" color={colors.text}>One habit to change: {p.ai.one_habit_to_change}</AppText> : null}
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
        </>
      ) : null}
      <Rank />
      <Mistakes />
    </View>
  );
}

// ---------- redesign sections ----------
function Hero({ prof, coach }: { prof: ExamPersonaProfile; coach?: string }) {
  const me = prof.personas.find((x) => x.key === prof.persona);
  const last = prof.history[prof.history.length - 1];
  if (!me) return null;
  return (
    <Chalkboard>
      <MitraTag label="Mitra · AI persona read" />
      <Hand color={paper.marigold} size={18}>after {prof.answers} answers, I think you are —</Hand>
      <View style={styles.heroTitle}>
        <View style={styles.flex}>
          <AppText variant="display" color={paper.chalkText} accessibilityRole="header">{me.name}</AppText>
          <View style={styles.underline} />
        </View>
        <Medal icon={personaIcon(me.icon)} size={68} />
      </View>
      <AppText variant="small" color={paper.chalkMuted}>{me.description}</AppText>
      <View style={boardStyles.wrap}>
        {prof.confidence ? <ChalkChip label={`Confidence: ${prof.confidence} · based on ${prof.mocks_taken} mock${prof.mocks_taken === 1 ? '' : 's'}, ${prof.answers} answers`} /> : null}
        {prof.same_persona_streak && prof.same_persona_streak > 1 ? <ChalkChip label={`Same persona ${prof.same_persona_streak} mocks in a row`} /> : null}
      </View>
      {coach ? <CoachBubble style={styles.gapSm}>{coach}</CoachBubble> : null}
      {last ? <Hand color={paper.marigold} size={15} style={{ alignSelf: 'flex-end' }}>badge earned · Mock {prof.history.length}</Hand> : null}
    </Chalkboard>
  );
}

function EmptyHero() {
  return (
    <Chalkboard>
      <MitraTag label="Mitra · AI persona read" />
      <Hand color={paper.marigold} size={18}>after your first mock, I will tell you who you are —</Hand>
      <AppText variant="h1" color={paper.chalkText}>Take a mock to meet your exam persona</AppText>
      <AppText variant="small" color={paper.chalkMuted}>
        Mitra reads how you answer — speed, risk, recovery after a miss — and matches you to one of six exam-takers. It needs one full mock first.
      </AppText>
      <Button title="Take a mock" variant="accent" rightIcon="arrow-forward" onPress={() => router.push('/practice')} style={styles.gapSm} />
    </Chalkboard>
  );
}

function Personas({ prof, selected, onSelect }: { prof: ExamPersonaProfile; selected: PersonaKey | null; onSelect: (k: PersonaKey) => void }) {
  const p = prof.personas.find((x) => x.key === selected) ?? prof.personas[0];
  const other = p && p.key !== prof.persona ? p : null;
  const match = prof.matches.find((m) => m.key === p?.key)?.match;
  return (
    <View style={{ gap: spacing.md }}>
      <SectionHead kicker="the six exam-takers —" title="Which one are you? Tap to compare." caption="Your shape stays saffron. The persona you pick is drawn dashed." />
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: spacing.sm, paddingVertical: 4, paddingRight: 4 }}>
        {prof.personas.map((x) => {
          const on = x.key === p?.key;
          return (
            <Pressable key={x.key} onPress={() => onSelect(x.key)} accessibilityRole="button" accessibilityState={{ selected: on }}
              accessibilityLabel={`${x.name}${x.key === prof.persona ? ', you' : ''}`}
              style={[styles.pCard, on && styles.pCardOn]}>
              <View style={styles.row}>
                <Ionicons name={personaIcon(x.icon)} size={20} color={on ? colors.primary : colors.text} />
                {x.key === prof.persona ? <View style={styles.you}><AppText variant="caption" color={colors.white} weight="700">YOU</AppText></View> : null}
              </View>
              <AppText variant="smallStrong" numberOfLines={2}>{x.name}</AppText>
            </Pressable>
          );
        })}
      </ScrollView>
      {p ? (
        <View style={[boardStyles.paperCard, { gap: spacing.sm }]}>
          <View style={styles.row}>
            <View style={styles.iconRing}><Ionicons name={personaIcon(p.icon)} size={22} color={colors.primary} /></View>
            <View style={styles.flex}>
              <AppText variant="h3">{p.name}</AppText>
              <Hand color={paper.pen} size={16}>{p.tagline}</Hand>
            </View>
          </View>
          <AppText variant="small" color={colors.text}>{p.description}</AppText>
          <Label>How Mitra spots it</Label>
          {p.signals.map((s) => (
            <View key={s} style={styles.row}>
              <Ionicons name="checkmark" size={16} color={colors.secondary} />
              <AppText variant="small" color={colors.text} style={styles.flex}>{s}</AppText>
            </View>
          ))}
          {match !== undefined ? (
            <View style={styles.matchBanner}>
              <AppText variant="smallStrong" color={colors.primary}>
                {p.key === prof.persona ? `This is you — ${match}% trait match across ${prof.answers} answers.` : `${match}% trait match with you.`}
              </AppText>
            </View>
          ) : null}
        </View>
      ) : null}
      {prof.traits ? (
        <View style={[styles.radarCard]}>
          <View style={styles.rowBetween}>
            <AppText variant="h3">Trait shape</AppText>
            <View style={styles.row}>
              <View style={[styles.legend, { backgroundColor: colors.primary }]} /><AppText variant="caption">You</AppText>
              {other ? <><View style={[styles.legend, styles.legendDash]} /><AppText variant="caption" numberOfLines={1}>{other.name}</AppText></> : null}
            </View>
          </View>
          <View style={{ alignItems: 'center' }}><TraitRadar you={prof.traits} other={other?.shape ?? null} size={280} /></View>
          <AppText variant="caption" align="center">Traits are scored 0–100 by code from your answers.</AppText>
        </View>
      ) : null}
    </View>
  );
}

function Evidence({ prof }: { prof: ExamPersonaProfile }) {
  const [filter, setFilter] = useState<PersonaTrait | null>(null);
  const traits = Array.from(new Set(prof.evidence.map((e) => e.trait)));
  const shown = prof.evidence.filter((e) => !filter || e.trait === filter);
  if (!prof.evidence.length) return null;
  return (
    <View style={{ gap: spacing.md }}>
      <SectionHead kicker="the evidence —" kickerColor={paper.pen} title="What your answers actually did" caption="Counts and timings are measured by code from your attempts." />
      <ChipScroller>
        <Pill label="All" selected={!filter} onPress={() => setFilter(null)} />
        {traits.map((t) => <Pill key={t} label={TRAIT_LABEL[t]} selected={filter === t} onPress={() => setFilter(filter === t ? null : t)} />)}
      </ChipScroller>
      {shown.map((e, i) => {
        const t = TRAIT_TONE[e.trait];
        return (
          <View key={`${e.trait}-${i}`} style={[boardStyles.paperCard, { gap: 6 }]}>
            <View style={styles.rowBetween}>
              <View style={[styles.traitTag, { backgroundColor: t.bg }]}><Label color={t.fg}>{TRAIT_LABEL[e.trait]}</Label></View>
              <Hand color={paper.pen} size={19} bold>{e.stat}</Hand>
            </View>
            <AppText variant="bodyStrong">{e.title}</AppText>
            <AppText variant="small">{e.body}</AppText>
          </View>
        );
      })}
    </View>
  );
}

function Notes({ prof }: { prof: ExamPersonaProfile }) {
  if (!prof.superpowers.length && !prof.blind_spots.length) return null;
  return (
    <View style={{ gap: spacing.md }}>
      {prof.superpowers.length ? (
        <View style={{ gap: spacing.sm }}>
          <View style={styles.row}><Ionicons name="flash-outline" size={20} color={colors.secondary} /><AppText variant="h3">Superpowers</AppText></View>
          {prof.superpowers.map((n, i) => <Sticky key={n.title} tone="green" title={n.title} titleColor={colors.secondary} tilt={i % 2 ? 0.6 : -0.6}>{n.body}</Sticky>)}
        </View>
      ) : null}
      {prof.blind_spots.length ? (
        <View style={{ gap: spacing.sm }}>
          <View style={styles.row}><Ionicons name="eye-off-outline" size={20} color={paper.pen} /><AppText variant="h3">Blind spots</AppText></View>
          {prof.blind_spots.map((n, i) => <Sticky key={n.title} tone="yellow" title={n.title} tilt={i % 2 ? -0.6 : 0.6}>{n.body}</Sticky>)}
        </View>
      ) : null}
    </View>
  );
}

function GamePlan({ prof, codeTitles }: { prof: ExamPersonaProfile; codeTitles: Record<string, string> }) {
  const me = prof.personas.find((x) => x.key === prof.persona);
  const [onPlan, setOnPlan] = useState<string[] | null>(null);
  useEffect(() => {
    AsyncStorage.getItem(PLAN_KEY).then((v) => setOnPlan(v ? JSON.parse(v) : prof.plan.slice(0, 1).map((s) => s.code_id))).catch(() => setOnPlan([]));
  }, [prof.plan]);
  const toggle = (id: string) => {
    const next = (onPlan ?? []).includes(id) ? (onPlan ?? []).filter((x) => x !== id) : [...(onPlan ?? []), id];
    setOnPlan(next);
    AsyncStorage.setItem(PLAN_KEY, JSON.stringify(next)).catch(() => undefined);
  };
  if (!me || !prof.plan.length) return null;
  const count = prof.plan.filter((s) => onPlan?.includes(s.code_id)).length;
  return (
    <Chalkboard>
      <Hand color={paper.marigold} size={17}>Mitra's game plan —</Hand>
      <AppText variant="h2" color={paper.chalkText}>How to beat {me.name}</AppText>
      <AppText variant="caption" color={paper.chalkMuted}>{count} of {prof.plan.length} strategies on your plan</AppText>
      {prof.plan.map((s, i) => {
        const mine = !!onPlan?.includes(s.code_id);
        return (
          <View key={s.code_id} style={[styles.planCard, mine && styles.planCardOn]}>
            <Hand color={board.saffron} size={30} bold>{i + 1}</Hand>
            <AppText variant="bodyStrong" color={paper.chalkText}>{s.title}</AppText>
            <Hand size={16}>{s.body}</Hand>
            <View style={styles.codeChip}>
              <Ionicons name="lock-closed-outline" size={12} color={paper.ink} />
              <AppText variant="caption" color={paper.ink} weight="700">Cheat code · {codeTitles[s.code_id] ?? s.code_id.replace(/-/g, ' ')}</AppText>
            </View>
            <View style={styles.row}>
              <Button title="Start 3-Q drill" size="sm" rightIcon="arrow-forward" style={styles.flex}
                onPress={() => router.push({ pathname: '/ai/cheat-codes', params: { code: s.code_id } })} />
              <Button title={mine ? 'On my plan ✓' : 'Add to my plan'} size="sm" variant={mine ? 'outline' : 'outlineLight'} style={styles.flex} onPress={() => toggle(s.code_id)} />
            </View>
          </View>
        );
      })}
      <AppText variant="caption" color={paper.chalkMuted}>AI-generated suggestions — check with your teacher if unsure.</AppText>
    </Chalkboard>
  );
}

function Timeline({ prof }: { prof: ExamPersonaProfile }) {
  const h = prof.history;
  const [sel, setSel] = useState(h.length - 1);
  if (!h.length) return null;
  const item = h[Math.min(sel, h.length - 1)]!;
  const best = Math.max(...h.map((x) => x.score));
  return (
    <View style={[boardStyles.paperCard, { gap: spacing.md }]}>
      <SectionHead kicker="persona over time —" title={h.length > 1 ? `Mock 1 → Mock ${h.length}` : 'Mock 1'} />
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.timeline}>
        {h.map((x, i) => {
          const on = i === sel;
          return (
            <View key={x.attempt_id} style={styles.tlItem}>
              {i > 0 ? <View style={styles.tlLine} /> : null}
              <Pressable onPress={() => setSel(i)} accessibilityRole="button" accessibilityState={{ selected: on }}
                accessibilityLabel={`Mock ${i + 1}: ${formatMarks(x.score)} marks, ${x.persona_name}`}
                style={[styles.tlDot, on ? styles.tlDotOn : i === 0 ? styles.tlDotFirst : null]}>
                <AppText variant="smallStrong" color={on ? colors.white : colors.text}>{formatMarks(x.score)}</AppText>
              </Pressable>
              <AppText variant="caption" weight="700" color={colors.text}>Mock {i + 1}</AppText>
              <AppText variant="caption">{shortName(x.persona_name)}</AppText>
            </View>
          );
        })}
      </ScrollView>
      <View style={styles.tlDetail}>
        <View style={styles.rowBetween}>
          <AppText variant="smallStrong">Mock {sel + 1} · {formatDate(item.date)}</AppText>
          <AppText variant="caption" color={paper.pen} weight="700">{item.persona_name}</AppText>
        </View>
        <Hand color={paper.pen} size={17}>
          {`${item.score === best && h.length > 1 ? 'Best yet. ' : ''}${item.rushed ? `${item.rushed} rushed answers, and ${item.rushed_wrong} of them were wrong.` : 'No rushed answers in this mock.'}`}
        </Hand>
        <AppText variant="caption">{item.attempted} attempted · {item.right} right · {item.wrong} wrong → {formatMarks(item.score)} marks</AppText>
      </View>
    </View>
  );
}

function ShareCard({ prof }: { prof: ExamPersonaProfile }) {
  const [look, setLook] = useState<'chalk' | 'paper'>('chalk');
  const [showScore, setShowScore] = useState(true);
  const me = prof.personas.find((x) => x.key === prof.persona);
  if (!me) return null;
  const h = prof.history;
  const last = h[h.length - 1];
  const first = h[0];
  const up = last && first && h.length > 1 ? last.score - first.score : 0;
  const scoreLine = last ? `Mock ${h.length} · ${formatMarks(last.score)}/${formatMarks(last.max_score)}${up > 0 ? ` · up ${formatMarks(up)} since Mock 1` : ''}` : '';
  const chalk = look === 'chalk';
  const share = async () => {
    try {
      await Share.share({
        message: `My exam persona on PrepMithra is ${me.name} — ${me.tagline}.${showScore && scoreLine ? `\n${scoreLine}` : ''}\nWhich one are you? 6 personas, read by Mitra.`,
      });
    } catch {
      toast.error('Could not open the share sheet.');
    }
  };
  return (
    <View style={{ gap: spacing.md }}>
      <View style={styles.rowBetween}>
        <AppText variant="h3">Share card</AppText>
        <View style={{ width: 160 }}>
          <SegmentedControl value={look} onChange={setLook} accessibilityLabel="Card style" segments={[{ value: 'chalk', label: 'Chalk' }, { value: 'paper', label: 'Paper' }]} />
        </View>
      </View>
      <View style={chalk ? styles.shareFrame : null}>
        <View style={[styles.shareCard, chalk ? styles.shareChalk : styles.sharePaper]} accessible accessibilityLabel={`Share card: my exam persona is ${me.name}`}>
          <View style={styles.flex}>
            <AppText variant="smallStrong" color={chalk ? paper.chalkText : paper.ink}>Prep<AppText variant="smallStrong" color={colors.accent}>Mithra</AppText> AI</AppText>
            <Hand color={chalk ? paper.marigold : paper.pen} size={15}>my exam persona is</Hand>
            <AppText variant="h2" color={chalk ? paper.chalkText : paper.ink}>{me.name}</AppText>
            {showScore && scoreLine ? <AppText variant="caption" weight="700" color={chalk ? paper.chalkText : paper.ink}>{scoreLine}</AppText> : null}
            <AppText variant="caption" color={chalk ? paper.chalkMuted : colors.textSecondary}>Which one are you? 6 personas, read by Mitra</AppText>
          </View>
          <Medal icon={personaIcon(me.icon)} size={56} />
        </View>
      </View>
      <View style={styles.rowBetween}>
        <View style={styles.row}>
          <Switch value={showScore} onValueChange={setShowScore} accessibilityLabel={`Show my Mock ${h.length} score`} trackColor={{ true: colors.primary, false: colors.borderStrong }} />
          <AppText variant="small" color={colors.text}>Show my Mock {h.length} score</AppText>
        </View>
      </View>
      <Button title="Share my persona" leftIcon="share-social-outline" onPress={share} />
      <AiNote>AI-generated from your attempts. Scores themselves are calculated by code.</AiNote>
    </View>
  );
}

export default function Persona() {
  const profile = useAiQuery(() => aiService.personaProfile(), 'persona-profile');
  const snapshot = useAiQuery(() => aiService.persona(), 'persona-coach');
  const codes = useAiQuery(() => aiService.cheatCodes(), 'persona-codes');
  const [selected, setSelected] = useState<PersonaKey | null>(null);
  const prof = profile.data;
  const ready = !!prof && prof.mocks_taken > 0 && !!prof.persona && !!prof.traits;
  const codeTitles = useMemo(() => Object.fromEntries((codes.data?.items ?? []).map((c) => [c.id, c.title])), [codes.data]);
  const nextMock = (prof?.mocks_taken ?? 0) + 1;

  return (
    <Screen>
      <View style={{ gap: spacing.xl }}>
        <View style={{ gap: spacing.xs }}>
          <Kick>{prof ? `after ${prof.mocks_taken} mock${prof.mocks_taken === 1 ? '' : 's'}` : 'your exam persona'}</Kick>
          <AppText variant="h1" accessibilityRole="header">Your exam persona</AppText>
          <AiNote>AI-generated from your attempts. Scores themselves are calculated by code.</AiNote>
        </View>

        {profile.loading ? <LoadingSkeleton /> : null}
        <AiErrorNotice error={profile.error} onRetry={profile.reload} />

        {prof ? (ready ? (
          <>
            <Hero prof={prof} coach={snapshot.data?.ai.summary} />
            <Personas prof={prof} selected={selected ?? prof.persona} onSelect={setSelected} />
            <Evidence prof={prof} />
            <Notes prof={prof} />
            <GamePlan prof={prof} codeTitles={codeTitles} />
            <Timeline prof={prof} />
            <ShareCard prof={prof} />
          </>
        ) : (
          <>
            <EmptyHero />
            {prof.personas.length ? <Personas prof={prof} selected={selected ?? prof.personas[0]!.key} onSelect={setSelected} /> : null}
          </>
        )) : null}

        <Sticky tone="green" title="Next persona check" titleColor={colors.secondary}>
          <AppText variant="small" color={colors.text}>Mitra re-reads your persona after every mock. Next check after Mock {nextMock}.</AppText>
          <AppText variant="smallStrong" color={colors.primary} onPress={() => router.push('/practice')} accessibilityRole="link">Take Mock {nextMock} →</AppText>
        </Sticky>

        <MoreFromMitra persona={snapshot} />
      </View>
    </Screen>
  );
}

function Kick({ children }: { children: string }) {
  return <Hand color={colors.secondary} size={16}>{children}</Hand>;
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  gap: { marginTop: spacing.md },
  gapSm: { marginTop: spacing.sm },
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, flexWrap: 'wrap' },
  rowBetween: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, flexWrap: 'wrap' },
  stats: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  heroTitle: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  underline: { height: 3, width: 140, backgroundColor: colors.accent, borderRadius: 2, marginTop: 4, transform: [{ rotate: '-1deg' }] },
  pCard: { width: 132, minHeight: 84, padding: spacing.md, borderRadius: radii.md, borderWidth: 1.5, borderColor: colors.border, backgroundColor: colors.card, gap: spacing.sm, justifyContent: 'space-between' },
  pCardOn: { borderColor: paper.ink, backgroundColor: paper.stickyYellow },
  you: { backgroundColor: colors.primary, borderRadius: radii.full, paddingHorizontal: 8, paddingVertical: 1 },
  iconRing: { width: 44, height: 44, borderRadius: 22, borderWidth: 1.5, borderColor: paper.ink, backgroundColor: paper.stickyYellow, alignItems: 'center', justifyContent: 'center' },
  matchBanner: { backgroundColor: board.saffronSoft, borderRadius: radii.md, padding: spacing.md, marginTop: spacing.xs },
  radarCard: { backgroundColor: colors.card, borderRadius: radii.lg, borderWidth: 1, borderColor: colors.border, padding: spacing.lg, gap: spacing.sm },
  legend: { width: 16, height: 3, borderRadius: 2 },
  legendDash: { borderTopWidth: 2, borderStyle: 'dashed', borderColor: colors.secondary, height: 0 },
  traitTag: { borderRadius: radii.full, paddingHorizontal: 8, paddingVertical: 3 },
  planCard: { borderWidth: 1.5, borderStyle: 'dashed', borderColor: board.dashed, borderRadius: radii.md, padding: spacing.md, gap: spacing.sm },
  planCardOn: { backgroundColor: 'rgba(255,255,255,0.06)' },
  codeChip: { flexDirection: 'row', alignItems: 'center', gap: 4, alignSelf: 'flex-start', backgroundColor: paper.marigold, borderRadius: radii.full, paddingHorizontal: 10, paddingVertical: 3 },
  timeline: { paddingVertical: 4, gap: 0 },
  tlItem: { width: 84, alignItems: 'center', gap: 2 },
  tlLine: { position: 'absolute', top: 21, left: -20, width: 40, height: 3, backgroundColor: colors.primary },
  tlDot: { width: 44, height: 44, borderRadius: 22, borderWidth: 2, borderColor: paper.ink, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center' },
  tlDotFirst: { backgroundColor: colors.secondarySoft },
  tlDotOn: { backgroundColor: colors.primary, borderColor: colors.primary },
  tlDetail: { backgroundColor: colors.background, borderRadius: radii.md, borderWidth: 1, borderColor: colors.border, padding: spacing.md, gap: 4 },
  shareFrame: { backgroundColor: paper.wood, borderRadius: 16, padding: 6 },
  shareCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.lg, borderRadius: 12 },
  shareChalk: { backgroundColor: paper.chalk },
  sharePaper: { backgroundColor: paper.paper, borderWidth: 1.5, borderColor: paper.ink },
});
