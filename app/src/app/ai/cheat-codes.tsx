import { useEffect, useMemo, useState } from 'react';
import { Pressable, StyleSheet, TextInput, View } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { CheatCode, CheatCodeDrill, CheatCodeDrillResult } from '@prepmitra/shared';
import { AppText, BottomSheet, Button, LoadingSkeleton, ProgressBar, Screen, toast } from '@/components';
import { AiErrorNotice, useAiAction, useAiQuery } from '@/features/ai/AiUi';
import {
  AiNote, Chalkboard, ChipScroller, CoachBubble, Hand, Label, MitraTag, OptionRow, Pill, SectionHead, board, boardStyles, type OptionState,
} from '@/features/ai/Board';
import { aiService } from '@/services/aiService';
import { colors, paper, radii, spacing } from '@/theme';

const TRY = ['1.331', 'unit digit', 'LCM'];

/** The 3-question drill for one code. Answers are marked by the API; 2 of 3 unlocks the code. */
function DrillSheet({ codeId, onClose, onUnlocked }: { codeId: string | null; onClose: () => void; onUnlocked?: () => void }) {
  const [drill, setDrill] = useState<CheatCodeDrill | null>(null);
  const [answers, setAnswers] = useState<(string | null)[]>([]);
  const [result, setResult] = useState<CheatCodeDrillResult | null>(null);
  const load = useAiAction(aiService.cheatCodeDrill);
  const check = useAiAction(aiService.checkCheatCodeDrill);

  useEffect(() => {
    setDrill(null); setResult(null); setAnswers([]);
    if (!codeId) return;
    void load.run(codeId).then((d) => { if (d) { setDrill(d); setAnswers(d.questions.map(() => null)); } });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [codeId]);

  const submit = async () => {
    if (!drill) return;
    const r = await check.run(drill.code_id, answers);
    if (!r) return;
    setResult(r);
    if (r.newly_unlocked) { toast.success('Code unlocked. It is yours now.'); onUnlocked?.(); }
  };
  const retry = () => { setResult(null); setAnswers((a) => a.map(() => null)); };
  const allAnswered = answers.length > 0 && answers.every((a) => a);

  return (
    <BottomSheet visible={!!codeId} onClose={onClose} title={drill?.title ?? 'Practise a code'} subtitle="Three questions, one code. Get 2 right and it's yours."
      footer={drill ? (result ? (
        <View style={styles.footerRow}>
          <Button title="Try again" variant="outline" leftIcon="refresh" onPress={retry} style={styles.flex} />
          <Button title="Done" onPress={onClose} style={styles.flex} />
        </View>
      ) : (
        <Button title={`Check my answers${allAnswered ? '' : ` (${answers.filter(Boolean).length}/${answers.length})`}`} loading={check.busy} disabled={!allAnswered} onPress={submit} fullWidth />
      )) : undefined}>
      <View style={{ gap: spacing.md }}>
        <MitraTag label="Mitra · AI drill" onDark={false} />
        {load.busy ? <LoadingSkeleton variant="card" /> : null}
        <AiErrorNotice error={load.error} onRetry={() => codeId && load.run(codeId).then((d) => { if (d) { setDrill(d); setAnswers(d.questions.map(() => null)); } })} />
        {result ? (
          <View style={[styles.resultBox, { borderColor: result.right >= 2 ? colors.success : paper.pen }]}>
            <AppText variant="h3" color={result.right >= 2 ? colors.success : paper.pen}>
              {result.right} of {result.of} right{result.unlocked ? ' · unlocked' : ''}
            </AppText>
            <AppText variant="small">
              {result.newly_unlocked ? 'You scored 2 of 3 — this code is now in your codes.' : result.unlocked ? 'This code is already yours. Keep it sharp.' : 'Get 2 of 3 right to unlock it. Read the trap side, then try again.'}
            </AppText>
          </View>
        ) : null}
        {drill?.questions.map((q, i) => {
          const res = result?.results[i];
          return (
            <View key={i} style={{ gap: spacing.xs }}>
              <Label>Question {i + 1} of {drill.questions.length}</Label>
              <AppText variant="bodyStrong">{q.text}</AppText>
              {q.options.map((o) => {
                let state: OptionState = answers[i] === o.key ? 'selected' : 'idle';
                if (res) state = o.key === res.answer ? (answers[i] === o.key ? 'correct' : 'answer') : answers[i] === o.key ? 'wrong' : 'idle';
                return <OptionRow key={o.key} option={o} state={state} disabled={!!result}
                  onPress={() => setAnswers((a) => a.map((x, j) => (j === i ? o.key : x)))} />;
              })}
              {res ? <AppText variant="small" color={res.correct ? colors.success : paper.pen}>{res.correct ? 'Right. ' : `Answer ${res.answer}. `}{res.explanation}</AppText> : null}
            </View>
          );
        })}
        <AiErrorNotice error={check.error} onRetry={submit} />
        <AiNote>Drill answers are checked by code. Mitra's explanations are AI-generated — check with your teacher if unsure.</AiNote>
      </View>
    </BottomSheet>
  );
}

function CodeCard({ c, onPractise }: { c: CheatCode; onPractise: () => void }) {
  const [flipped, setFlipped] = useState(false);
  return (
    <View style={[styles.card, flipped && styles.cardBack]}>
      {flipped ? (
        <View style={{ gap: spacing.sm }}>
          <Label color={paper.pen}>When not to use it</Label>
          <AppText variant="bodyStrong">{c.title}</AppText>
          <Hand color={paper.pen} size={18}>{c.trap}</Hand>
          <View style={styles.penLine} />
          <AppText variant="caption">If the trap applies, solve it the long way. A code that doesn't fit costs more time than it saves.</AppText>
        </View>
      ) : (
        <View style={{ gap: spacing.sm }}>
          <View style={boardStyles.row}>
            <Label style={styles.flex}>{c.topic}</Label>
            <AppText variant="caption" color={colors.primary} weight="700">saves ~{c.saves_seconds}s</AppText>
            {c.unlocked ? <Ionicons name="lock-open-outline" size={14} color={colors.success} accessibilityLabel="Unlocked" /> : <Ionicons name="lock-closed-outline" size={14} color={colors.textMuted} accessibilityLabel="Locked" />}
          </View>
          <AppText variant="h3">{c.title}</AppText>
          <Label>The trick</Label>
          <AppText variant="small" color={colors.text}>{c.trick}</AppText>
          <Label>Worked example</Label>
          <View style={styles.example}><AppText variant="small" color={colors.text}>{c.example}</AppText></View>
          <View style={boardStyles.wrap}>
            {c.exams.map((e) => <View key={e} style={styles.exam}><AppText variant="caption" weight="600">{e}</AppText></View>)}
          </View>
        </View>
      )}
      <View style={styles.cardActions}>
        <Button title={flipped ? 'Flip · the trick' : 'Flip · the trap'} size="sm" variant="outline" leftIcon="sync-outline" onPress={() => setFlipped((f) => !f)} style={styles.flex}
          accessibilityHint={flipped ? 'Shows the trick and example' : 'Shows when not to use this code'} />
        <Button title="Practise this code" size="sm" onPress={onPractise} style={styles.flex} />
      </View>
    </View>
  );
}

export default function CheatCodes() {
  const params = useLocalSearchParams<{ code?: string }>();
  const cat = useAiQuery(() => aiService.cheatCodes(), 'cheat-codes');
  const [query, setQuery] = useState('');
  const [topic, setTopic] = useState<string | null>(null);
  const [drillId, setDrillId] = useState<string | null>(params.code ?? null);

  useEffect(() => { if (params.code) setDrillId(params.code); }, [params.code]);

  const data = cat.data;
  const items = useMemo(() => {
    const q = query.trim().toLowerCase();
    return (data?.items ?? []).filter((c) => (!topic || c.topic === topic)
      && (!q || [c.title, c.trick, c.example, c.topic].some((s) => s.toLowerCase().includes(q))));
  }, [data, query, topic]);
  const start = data?.yours.find((c) => !c.unlocked) ?? data?.yours[0];

  return (
    <Screen keyboard>
      <View style={{ gap: spacing.lg }}>
        <Chalkboard>
          <Hand color={paper.marigold} size={17}>exam-safe shortcuts —</Hand>
          <AppText variant="display" color={paper.chalkText} accessibilityRole="header">Cheat codes</AppText>
          <AppText variant="small" color={paper.chalkMuted}>
            Elimination, approximation and unit-digit checks for every slow or wrong answer. Legal in every exam hall — no guessing, just less writing.
          </AppText>
          {start ? <CoachBubble>{`Start with ${start.title} — it alone saves about ${start.saves_seconds} seconds.`}</CoachBubble> : null}
          <View style={styles.search}>
            <Ionicons name="search" size={18} color={colors.textMuted} />
            <TextInput value={query} onChangeText={setQuery} placeholder="Search: 1.331, unit digit, LCM, 'some'…" placeholderTextColor={colors.textMuted}
              style={styles.searchInput} accessibilityLabel="Search cheat codes" returnKeyType="search" />
            {query ? <Pressable onPress={() => setQuery('')} accessibilityLabel="Clear search" hitSlop={8}><Ionicons name="close-circle" size={18} color={colors.textMuted} /></Pressable> : null}
          </View>
          <ChipScroller>
            <AppText variant="caption" color={paper.chalkMuted} style={{ alignSelf: 'center' }}>Try</AppText>
            {TRY.map((t) => <Pill key={t} label={t} onDark onPress={() => setQuery(t)} />)}
          </ChipScroller>
          {data ? (
            <ChipScroller>
              <Pill label="All" count={data.total} onDark selected={!topic} onPress={() => setTopic(null)} />
              {data.topics.map((t) => <Pill key={t.name} label={t.name} count={t.count} onDark selected={topic === t.name} onPress={() => setTopic(topic === t.name ? null : t.name)} />)}
            </ChipScroller>
          ) : null}
        </Chalkboard>

        {cat.loading && !data ? <LoadingSkeleton /> : null}
        <AiErrorNotice error={cat.error} onRetry={cat.reload} />

        {data ? (
          <>
            <View style={styles.unlocked}>
              <Label color={paper.marigold}>Codes unlocked</Label>
              <AppText variant="h2" color={paper.chalkText}>{data.unlocked_count} <AppText variant="small" color={paper.chalkMuted}>of {data.total}</AppText></AppText>
              <ProgressBar value={data.unlocked_count} max={Math.max(1, data.total)} size="sm" label="Codes unlocked" />
            </View>

            <View style={[boardStyles.paperCard, { gap: spacing.md }]}>
              <SectionHead kicker="from your mock reports —" kickerColor={paper.pen} title="Your codes" caption="Locked codes unlock when you score 2 of 3 in their drill." />
              <View style={styles.grid}>
                {data.yours.map((c) => (
                  <Pressable key={c.id} onPress={() => setDrillId(c.id)} accessibilityRole="button"
                    accessibilityLabel={`${c.title}. ${c.unlocked ? 'Unlocked' : 'Locked, score 2 of 3 in the drill to unlock'}. Opens the drill.`}
                    style={({ pressed }) => [styles.mini, c.unlocked ? styles.miniOn : styles.miniOff, pressed && { opacity: 0.85 }]}>
                    <View style={[styles.lock, { backgroundColor: c.unlocked ? paper.marigold : colors.background }]}>
                      <Ionicons name={c.unlocked ? 'lock-open-outline' : 'lock-closed-outline'} size={16} color={paper.ink} />
                    </View>
                    <View style={styles.flex}>
                      <AppText variant="smallStrong" numberOfLines={3}>{c.title}</AppText>
                      <AppText variant="caption" color={c.unlocked ? colors.success : colors.textSecondary}>{c.unlocked ? 'Unlocked' : 'Locked · drill 2 of 3 to unlock'}</AppText>
                    </View>
                  </Pressable>
                ))}
              </View>
            </View>

            <Chalkboard>
              <MitraTag label="Mitra · AI drill" />
              <AppText variant="h3" color={paper.chalkText}>Practise a code</AppText>
              <Hand size={16}>Pick any card and hit "Practise". Three questions, one code, instant feedback. Get 2 right and it's yours.</Hand>
            </Chalkboard>

            <SectionHead title={`${items.length} code${items.length === 1 ? '' : 's'}`} caption="Every example is worked out — check it yourself." />
            {items.length === 0 ? <AppText variant="small">No codes match “{query}”. Try another word or clear the topic.</AppText> : null}
            {items.map((c) => <CodeCard key={c.id} c={c} onPractise={() => setDrillId(c.id)} />)}
            <AiNote>Drill answers are checked by code. Mitra's explanations are AI-generated — check with your teacher if unsure.</AiNote>
          </>
        ) : null}
      </View>
      <DrillSheet codeId={drillId} onClose={() => setDrillId(null)} onUnlocked={cat.reload} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  footerRow: { flexDirection: 'row', gap: spacing.sm },
  resultBox: { borderWidth: 2, borderRadius: radii.md, padding: spacing.md, gap: 4, backgroundColor: paper.paper },
  search: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, backgroundColor: colors.card, borderRadius: radii.full, paddingHorizontal: spacing.md, minHeight: 46, marginTop: spacing.xs },
  searchInput: { flex: 1, color: colors.text, fontSize: 15, paddingVertical: 8 },
  unlocked: { backgroundColor: paper.chalk, borderRadius: radii.lg, padding: spacing.lg, gap: 6 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  mini: { flexBasis: '47%', flexGrow: 1, flexDirection: 'row', gap: spacing.sm, padding: spacing.sm, borderRadius: radii.md, minHeight: 72 },
  miniOn: { borderWidth: 1.5, borderColor: paper.ink, backgroundColor: colors.card },
  miniOff: { borderWidth: 1.5, borderStyle: 'dashed', borderColor: colors.borderStrong, backgroundColor: colors.background },
  lock: { width: 32, height: 32, borderRadius: 16, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: paper.ink },
  card: { backgroundColor: colors.card, borderWidth: 1.5, borderColor: paper.ink, borderRadius: radii.lg, padding: spacing.lg, gap: spacing.md },
  cardBack: { borderColor: paper.pen, borderWidth: 2.5, backgroundColor: paper.paper },
  penLine: { height: 2, width: 90, backgroundColor: paper.pen, borderRadius: 2, alignSelf: 'flex-end' },
  example: { backgroundColor: board.saffronSoft, borderRadius: radii.sm, padding: spacing.sm },
  exam: { borderWidth: 1, borderColor: colors.border, borderRadius: radii.full, paddingHorizontal: 8, paddingVertical: 2, backgroundColor: colors.background },
  cardActions: { flexDirection: 'row', gap: spacing.sm },
});
