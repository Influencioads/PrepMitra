import { useEffect, useState } from 'react';
import { StyleSheet, TextInput, View } from 'react-native';
import Svg, { Circle, Text as SvgText } from 'react-native-svg';
import type { TeachResult } from '@prepmitra/shared';
import { AppText, Button, LoadingSkeleton, NotebookBackground, ProgressBar, ScoreRing, Screen } from '@/components';
import { AiErrorNotice, useAiAction, useAiQuery } from '@/features/ai/AiUi';
import {
  AiNote, Chalkboard, ChipScroller, CoachBubble, Hand, Label, OptionRow, Pill, SeatingDiagram, SectionHead, Sticky, boardStyles,
} from '@/features/ai/Board';
import { aiService } from '@/services/aiService';
import { colors, paper, radii, spacing } from '@/theme';

/** "All A are B. Some B are C." — A inside B, C touching B away from A. */
function VennAllSome() {
  const w = 230, h = 150;
  return (
    <View accessible accessibilityRole="image" accessibilityLabel="Diagram: circle A inside circle B; circle C overlaps B but not A. Case 1, no A is C.">
      <Svg width={w} height={h}>
        <Circle cx={90} cy={72} r={56} stroke={paper.chalkText} strokeWidth={2} fill="none" />
        <Circle cx={72} cy={74} r={22} stroke={paper.chalkText} strokeWidth={2} fill="none" />
        <Circle cx={162} cy={72} r={32} stroke={paper.chalkText} strokeWidth={2} fill="none" />
        <SvgText x={72} y={79} fontSize={14} fill={paper.chalkText} textAnchor="middle">A</SvgText>
        <SvgText x={112} y={26} fontSize={14} fill={paper.chalkText} textAnchor="middle">B</SvgText>
        <SvgText x={172} y={77} fontSize={14} fill={paper.chalkText} textAnchor="middle">C</SvgText>
        <SvgText x={20} y={144} fontSize={11} fill={paper.chalkMuted}>case 1 · no A is C</SvgText>
      </Svg>
    </View>
  );
}

const MOOD_TONE: Record<string, { bg: string; fg: string }> = {
  curious: { bg: colors.secondarySoft, fg: colors.secondary },
  confused: { bg: colors.warningSoft, fg: colors.warningText },
  happy: { bg: colors.successSoft, fg: colors.success },
  doubtful: { bg: colors.errorSoft, fg: paper.pen },
};

function Chotu({ kind, mood, text }: { kind: string; mood: string; text: string }) {
  const t = MOOD_TONE[mood.toLowerCase()] ?? MOOD_TONE.curious!;
  return (
    <View style={styles.chotuRow}>
      <View style={{ alignItems: 'center', gap: 2 }}>
        <View style={styles.avatar}><AppText variant="h3" color={colors.secondary}>CH</AppText></View>
        <View style={styles.desk} />
        <AppText variant="caption" weight="700" color={colors.text}>Chotu</AppText>
        <View style={styles.aiStudent}><AppText variant="caption" color={colors.secondary} weight="700">AI STUDENT</AppText></View>
      </View>
      <View style={styles.chotuBubble} accessibilityLiveRegion="polite">
        <View style={styles.rowBetween}>
          <Label style={styles.flex}>Chotu asks · {kind}</Label>
          <View style={[styles.mood, { backgroundColor: t.bg }]}><Label color={t.fg}>{mood}</Label></View>
        </View>
        <AppText variant="bodyStrong">{text}</AppText>
      </View>
    </View>
  );
}

export default function TeachBack() {
  const list = useAiQuery(() => aiService.teachConcepts(), 'teach-concepts');
  const [conceptId, setConceptId] = useState<string | null>(null);
  const id = conceptId ?? list.data?.[0]?.id ?? null;
  const concept = useAiQuery(() => (id ? aiService.teachConcept(id) : Promise.resolve(null)), `teach-${id}`);
  const [round, setRound] = useState(0);
  const [results, setResults] = useState<TeachResult[]>([]);
  const [text, setText] = useState('');
  const [picked, setPicked] = useState<string | null>(null);
  const answer = useAiAction(aiService.teachAnswer);

  const reset = () => { setRound(0); setResults([]); setText(''); setPicked(null); answer.setError(null); };
  useEffect(reset, [id]); // eslint-disable-line react-hooks/exhaustive-deps

  const C = concept.data;
  const R = C?.rounds[round];
  const res = results[round];
  const latest = res ?? results[results.length - 1];
  const done = !!results[results.length - 1]?.done && results.length === C?.rounds.length;

  const teach = async (body: { choice?: string; text?: string }) => {
    if (!id || answer.busy || res) return;
    if (body.choice) setPicked(body.choice);
    const r = await answer.run(id, { round, ...body });
    if (r) { setResults((s) => { const n = [...s]; n[round] = r; return n; }); setText(''); }
  };
  const next = () => { setRound((x) => x + 1); setPicked(null); };
  const grand = results.reduce((s, r) => s + r.total, 0);
  const grandMax = results.reduce((s, r) => s + r.max_total, 0);

  return (
    <Screen keyboard>
      <View style={{ gap: spacing.lg }}>
        <View style={{ gap: spacing.xs }}>
          <SectionHead kicker="teach-back — new" kickerColor={paper.pen} title="Teaching is the fastest way to learn — explain it to Chotu" />
          <AppText variant="small">Chotu is an AI junior aspirant. He asks the questions an examiner would. Answer three of them, and Mitra marks how well you taught.</AppText>
        </View>

        {list.loading ? <LoadingSkeleton /> : null}
        <AiErrorNotice error={list.error} onRetry={list.reload} />
        {list.data && list.data.length > 1 ? (
          <ChipScroller>
            {list.data.map((c) => <Pill key={c.id} label={c.topic} selected={c.id === id} onPress={() => setConceptId(c.id)} accessibilityLabel={`${c.topic}: ${c.ask}`} />)}
          </ChipScroller>
        ) : null}

        {concept.loading && !C ? <LoadingSkeleton variant="card" /> : null}
        <AiErrorNotice error={concept.error} onRetry={concept.reload} />

        {C && R ? (
          <>
            <ChipScroller>
              {C.rounds.map((_, i) => (
                <Pill key={i} label={`${results[i] ? '✓ ' : i === round ? '● ' : ''}Round ${i + 1}`} selected={i === round}
                  onPress={() => { if (i <= results.length) { setRound(i); setPicked(null); } }}
                  accessibilityLabel={`Round ${i + 1}${results[i] ? ', answered' : i > results.length ? ', locked' : ''}`} />
              ))}
            </ChipScroller>

            <Chalkboard>
              <Label color={paper.chalkMuted}>Today’s concept · {C.topic}</Label>
              {C.board.map((l) => <Hand key={l} size={20}>{l}</Hand>)}
              <View style={boardStyles.dashedRule} />
              <Hand size={19} color={paper.marigold}>{C.ask}</Hand>
              <View style={{ alignItems: 'center' }}>
                {C.diagram === 'venn-all-some' ? <VennAllSome /> : C.diagram === 'circle-6' ? <SeatingDiagram seats={6} size={190} /> : null}
              </View>
              <View style={boardStyles.dashedRule} />
              <Label color={paper.chalkMuted}>Your lesson so far · written by you</Label>
              {results.length ? results.map((r, i) => (
                <Hand key={i} size={16} color={r.good ? paper.chalkText : paper.chalkMuted}>{`${i + 1}. ${r.written}`}</Hand>
              )) : <Hand size={16} color={paper.chalkMuted}>(empty board — pick an explanation below and it gets written here)</Hand>}
            </Chalkboard>

            <Chotu kind={R.kind} mood={res ? (res.good ? 'happy' : 'confused') : R.mood} text={res ? res.chotu_reply : R.chotu} />

            <View style={[boardStyles.paperCard, { gap: spacing.sm }]}>
              <View style={styles.rowBetween}>
                <AppText variant="h3">Your explanation · round {round + 1} of {C.rounds.length}</AppText>
                <AppText variant="caption">Pick one, or write your own</AppText>
              </View>
              {R.options.map((o) => (
                <OptionRow key={o.key} option={o} disabled={!!res || answer.busy}
                  state={picked === o.key ? (res ? (res.good ? 'correct' : 'wrong') : 'selected') : 'idle'}
                  onPress={() => teach({ choice: o.key })} />
              ))}
              {!res ? (
                <>
                  <AppText variant="smallStrong" style={{ marginTop: spacing.xs }}>Or explain in your own words</AppText>
                  <TextInput value={text} onChangeText={setText} placeholder="e.g. Draw B big, A inside it, C on the other side…" placeholderTextColor={colors.textMuted}
                    multiline maxLength={1000} style={styles.input} accessibilityLabel="Your explanation" />
                  <Button title="Teach this" variant="secondary" loading={answer.busy && !picked} disabled={text.trim().length < 3 || answer.busy} onPress={() => teach({ text: text.trim() })} />
                </>
              ) : !res.done ? (
                <Button title={`Next round · round ${round + 2}`} rightIcon="arrow-forward" onPress={next} />
              ) : null}
              <AiErrorNotice error={answer.error} />
            </View>

            {done ? (
              <Chalkboard>
                <Hand color={paper.marigold} size={18}>lesson complete —</Hand>
                <AppText variant="h2" color={paper.chalkText}>You taught {grand} of {grandMax}</AppText>
                <AppText variant="small" color={paper.chalkMuted}>Scores come from a fixed rubric calculated by code.</AppText>
                <Button title="Teach it again" variant="accent" leftIcon="refresh" onPress={reset} style={{ marginTop: spacing.sm }} />
              </Chalkboard>
            ) : null}

            <View style={[styles.scoreCard]}>
              <View style={styles.row}>
                <ScoreRing percent={latest ? (latest.total / latest.max_total) * 100 : 0} size={84} stroke={9} color={colors.secondary}
                  label={latest ? String(latest.total) : '–'} />
                <View style={styles.flex}>
                  <AppText variant="h3">Teaching score</AppText>
                  <AppText variant="small" accessibilityLabel={latest ? `${latest.total} out of ${latest.max_total}` : undefined}>
                    {latest ? `${latest.total} out of ${latest.max_total} · round ${latest.round + 1}` : 'Updates after each answer'}
                  </AppText>
                </View>
              </View>
              {(['clarity', 'correctness', 'examples'] as const).map((k) => (
                <ProgressBar key={k} label={k[0]!.toUpperCase() + k.slice(1)} value={latest?.scores[k] ?? 0} max={10} tone="secondary" showValue
                  valueLabel={latest ? `${latest.scores[k]}/10` : '–'} size="sm" />
              ))}
              <AppText variant="caption">Scores come from a fixed rubric calculated by code. Mitra only writes the notes.</AppText>
            </View>

            <View style={styles.margin}>
              <NotebookBackground margin={22} spacing={28} lines={14} />
              <View style={styles.marginBody}>
                <Label>Mitra’s margin notes · AI</Label>
                <AppText variant="caption">AI-generated — check with your teacher if unsure.</AppText>
                {results.length ? results.map((r, i) => (
                  <Hand key={i} color={paper.pen} size={16}>{`R${i + 1}: ${r.note}`}</Hand>
                )) : <Hand color={paper.pen} size={16}>Red pen is ready. Teach your first answer.</Hand>}
              </View>
            </View>

            {R.coach_hint ? <CoachBubble style={styles.coachWrap}>{R.coach_hint}</CoachBubble> : null}
          </>
        ) : null}

        <Sticky title="why teach-back?" titleColor={paper.ink} tilt={-1}>
          If you can explain it simply, you can solve it under pressure. Chotu finds the gaps before the exam does.
        </Sticky>
        <AiNote>Chotu and Mitra's notes are AI-generated. Teaching scores are calculated by code.</AiNote>
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  rowBetween: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, flexWrap: 'wrap' },
  chotuRow: { flexDirection: 'row', gap: spacing.md, alignItems: 'flex-start' },
  avatar: { width: 64, height: 64, borderRadius: 32, borderWidth: 2, borderColor: paper.ink, backgroundColor: colors.secondarySoft, alignItems: 'center', justifyContent: 'center' },
  desk: { width: 72, height: 8, backgroundColor: paper.woodLight, borderRadius: 2, marginTop: -4 },
  aiStudent: { backgroundColor: colors.secondarySoft, borderRadius: radii.sm, paddingHorizontal: 6 },
  chotuBubble: { flex: 1, backgroundColor: paper.paper, borderWidth: 1.5, borderColor: paper.ink, borderRadius: radii.lg, borderTopLeftRadius: 4, padding: spacing.md, gap: 6 },
  mood: { borderRadius: radii.full, paddingHorizontal: 8, paddingVertical: 2 },
  input: { minHeight: 64, borderWidth: 1.5, borderColor: colors.borderStrong, borderRadius: radii.md, padding: spacing.md, color: colors.text, backgroundColor: colors.background, textAlignVertical: 'top' },
  scoreCard: { backgroundColor: colors.card, borderRadius: radii.lg, borderWidth: 1, borderColor: colors.border, padding: spacing.lg, gap: spacing.md },
  margin: { overflow: 'hidden', borderRadius: radii.md, borderWidth: 1, borderColor: colors.border, backgroundColor: paper.paper, minHeight: 140 },
  marginBody: { paddingLeft: 34, paddingRight: spacing.md, paddingVertical: spacing.md, gap: 6 },
  coachWrap: { backgroundColor: 'transparent' },
});
