import { useEffect, useRef, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, TextInput, View, type ScrollViewInstance } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import { formatDate, isSupportReply, type AiMode, type BlackboardLesson, type CodeCheck, type DeepDive } from '@prepmitra/shared';
import { AppText, Badge, Button, Card, Chip, Divider, Input, ListRow, LoadingSkeleton, Mitra, ProgressBar, Screen, SegmentedControl, SwitchRow } from '@/components';
import { AiErrorNotice, AllowanceBadge, SupportBanner, useAiAction, useAiQuery } from '@/features/ai/AiUi';
import { ArtifactHeader, DeepDiveView } from '@/features/ai/AiViews';
import {
  AiNote, Chalkboard, ChipScroller, Hand, Label, MitraTag, OptionRow, Pill, SeatingDiagram, Sticky, board, boardStyles, type OptionState,
} from '@/features/ai/Board';
import { aiService } from '@/services/aiService';
import { colors, paper, radii, spacing } from '@/theme';

interface Msg { id: string; role: 'user' | 'assistant'; content: string; support?: boolean }

/**
 * Ask Mitra. Full-screen on the "Ask Mitra" tab; `compact` puts it under the blackboard with quick replies.
 * `context` (the lesson and step on the board) is sent ahead of the student's message but not shown in the bubble.
 */
function Chat({ compact, context, quickReplies = [] }: { compact?: boolean; context?: string; quickReplies?: string[] }) {
  const history = useAiQuery(() => aiService.tutorHistory(), 'tutor-history');
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [sessionId, setSessionId] = useState<string>();
  const [text, setText] = useState('');
  const [story, setStory] = useState(false);
  const [followUps, setFollowUps] = useState<string[]>([]);
  const [support, setSupport] = useState<string | null>(null);
  const [last, setLast] = useState('');
  const scroll = useRef<ScrollViewInstance>(null);
  const chat = useAiAction(aiService.tutorChat);

  useEffect(() => {
    const items = history.data ?? [];
    if (!items.length) return;
    setMsgs(items.map((m) => ({ id: String(m.id), role: m.role, content: m.content })));
    setSessionId(items[items.length - 1]!.session_id);
  }, [history.data]);

  const send = async (message: string, opts: { differently?: boolean; language?: string } = {}) => {
    const m = message.trim();
    if (!m || chat.busy) return;
    setText('');
    setLast(m);
    if (!opts.differently) setMsgs((s) => [...s, { id: `u${Date.now()}`, role: 'user', content: m }]);
    const r = await chat.run({
      message: context ? `${context}\n\n${m}` : m, session_id: sessionId, style: story ? 'story' : 'normal', explain_differently: opts.differently, language: opts.language,
    });
    if (!r) return;
    setSessionId(r.session_id);
    setFollowUps(r.follow_ups);
    if (r.support) setSupport(r.support);
    setMsgs((s) => [...s, { id: `a${Date.now()}`, role: 'assistant', content: r.reply, support: !!r.support }]);
  };

  const shown = compact ? msgs.slice(-12) : msgs;
  const replies = Array.from(new Set([...followUps, ...quickReplies]));
  return (
    <View style={compact ? undefined : styles.flex}>
      <SupportBanner message={support} />
      <ScrollView ref={scroll} style={compact ? styles.chatCompact : styles.flex} nestedScrollEnabled
        contentContainerStyle={{ gap: spacing.sm, paddingVertical: spacing.sm }}
        onContentSizeChange={() => scroll.current?.scrollToEnd({ animated: true })}>
        {msgs.length === 0 && !history.loading ? (
          compact ? (
            <View style={[styles.bubble, styles.coach]}>
              <MitraTag label="Mitra · AI coach" avatar={false} />
              <Hand size={16}>Namaste! I will draw each step on the board. Stop me anytime and ask why.</Hand>
            </View>
          ) : <AppText variant="small">Ask Mitra anything about your preparation: a concept, a question from your mock, or how to plan your week.</AppText>
        ) : null}
        {shown.map((m) => (
          m.role === 'assistant' && !m.support ? (
            <View key={m.id} style={[styles.bubble, styles.coach]}>
              <MitraTag label="Mitra · AI coach" avatar={false} />
              <AppText variant="small" color={paper.chalkText}>{m.content}</AppText>
            </View>
          ) : (
            <View key={m.id} style={[styles.bubble, m.role === 'user' ? styles.mine : styles.support]}>
              <AppText variant="small" color={colors.text}>{m.content}</AppText>
            </View>
          )
        ))}
        {chat.busy ? <AppText variant="caption">Mitra is thinking…</AppText> : null}
      </ScrollView>
      <AiErrorNotice error={chat.error} onRetry={() => send(last)} />
      <ChipScroller style={{ marginVertical: spacing.xs }}>
        {replies.map((f) => (
          <Chip key={f} label={f} onPress={() => (/hindi/i.test(f) ? send(last || f, { language: 'hi', differently: !!last }) : send(f))} />
        ))}
        {msgs.some((m) => m.role === 'assistant') ? <Chip label="Explain differently" icon="shuffle" onPress={() => send(last || 'Explain that differently', { differently: true })} /> : null}
      </ChipScroller>
      <SwitchRow label="Story mode" value={story} onValueChange={setStory} />
      <View style={styles.composer}>
        <TextInput value={text} onChangeText={setText} placeholder={compact ? 'Ask about this step…' : 'Ask Mitra…'} maxLength={2000} multiline accessibilityLabel="Message"
          placeholderTextColor={colors.textMuted} style={styles.input} />
        <Button title="Send" size="sm" leftIcon="send" disabled={!text.trim() || chat.busy} onPress={() => send(text)} />
      </View>
      <View style={[styles.row, styles.gapSm]}><AllowanceBadge feature="tutor_chat_turns" label="Chat turns" /></View>
      <AiNote style={styles.gapSm}>AI-generated explanations — check with your teacher if unsure. Scores are always calculated by code.</AiNote>
    </View>
  );
}

// ---------- the blackboard ----------
function CheckYourself({ lesson }: { lesson: BlackboardLesson }) {
  const [index, setIndex] = useState(0);
  const [picked, setPicked] = useState<string | null>(null);
  const [res, setRes] = useState<CodeCheck | null>(null);
  const check = useAiAction(aiService.checkLesson);
  useEffect(() => { setIndex(0); setPicked(null); setRes(null); }, [lesson.id]);
  const q = lesson.check[index];
  if (!q) return null;
  const pick = async (key: string) => {
    if (res || check.busy) return;
    setPicked(key);
    const r = await check.run(lesson.id, index, key);
    if (r) setRes(r);
  };
  const another = () => { setIndex((i) => (i + 1) % lesson.check.length); setPicked(null); setRes(null); };
  return (
    <View style={[boardStyles.paperCard, { gap: spacing.sm }]}>
      <View style={styles.rowBetween}>
        <View style={styles.flex}>
          <AppText variant="h3">Check yourself</AppText>
          <AppText variant="caption">Question {index + 1} of {lesson.check.length} · checked instantly by code</AppText>
        </View>
        {lesson.check.length > 1 ? <Button title="Another question" size="sm" variant="outline" onPress={another} /> : null}
      </View>
      <AppText variant="bodyStrong">{q.text}</AppText>
      {q.options.map((o) => {
        let state: OptionState = picked === o.key ? 'selected' : 'idle';
        if (res) state = o.key === res.answer ? (picked === o.key ? 'correct' : 'answer') : picked === o.key ? 'wrong' : 'idle';
        return <OptionRow key={o.key} option={o} state={state} disabled={!!res || check.busy} onPress={() => pick(o.key)} />;
      })}
      {res ? <AppText variant="small" color={res.correct ? colors.success : paper.pen}>{res.correct ? 'Right! ' : `Not quite — it is ${res.answer}. `}{res.explanation}</AppText> : null}
      <AiErrorNotice error={check.error} onRetry={() => picked && check.run(lesson.id, index, picked).then((r) => r && setRes(r))} />
    </View>
  );
}

function Blackboard() {
  const index = useAiQuery(() => aiService.lessons(), 'lessons');
  const [lessonId, setLessonId] = useState<string | null>(null);
  const id = lessonId ?? index.data?.recommended ?? index.data?.items[0]?.id ?? null;
  const lesson = useAiQuery(() => (id ? aiService.lesson(id) : Promise.resolve(null)), `lesson-${id}`);
  const [step, setStep] = useState(0);
  useEffect(() => { setStep(0); }, [id]);

  const L = lesson.data;
  const s = L?.steps[step];
  const total = L?.steps.length ?? 0;
  const why = index.data?.why;
  const context = L && s ? `[Blackboard lesson: ${L.topic}. Step ${step + 1} of ${total}: ${s.title}. ${s.lines.join(' ')}]` : undefined;
  const clueOn = (c: string) => !!s && s.lines.some((l) => l.toLowerCase().includes(c.toLowerCase()));

  return (
    <View style={{ gap: spacing.lg }}>
      {index.loading ? <LoadingSkeleton /> : null}
      <AiErrorNotice error={index.error} onRetry={index.reload} />
      {index.data && index.data.items.length > 1 ? (
        <View style={{ gap: spacing.xs }}>
          <Label>Lessons</Label>
          <ChipScroller>
            {index.data.items.map((it) => (
              <Pill key={it.id} label={`${it.id === index.data!.recommended ? '★ ' : ''}${it.topic}`} selected={it.id === id} onPress={() => setLessonId(it.id)}
                accessibilityLabel={`${it.topic}, ${it.steps} steps${it.id === index.data!.recommended ? ', recommended for you' : ''}`} />
            ))}
          </ChipScroller>
        </View>
      ) : null}

      {L ? (
        <>
          <View style={{ gap: spacing.xs }}>
            <Hand color={colors.secondary} size={16}>the blackboard — {L.subject}</Hand>
            <AppText variant="h1" accessibilityRole="header">{L.topic}</AppText>
            <View style={styles.tutorPill}>
              <View style={styles.dot} />
              <AppText variant="caption" color={paper.chalkText} weight="600">PrepMithra AI tutor · explains, never just answers</AppText>
            </View>
          </View>

          {why && id === index.data?.recommended ? (
            <Sticky title="Why this topic" titleColor={colors.warningText} tilt={-0.8}>
              {`${why.topic} is costing you the most marks (${why.mastery}% mastery). Calculated by code from your answers.`}
            </Sticky>
          ) : null}

          <View style={[boardStyles.paperCard, { gap: spacing.sm }]}>
            <Label>The question · {L.question.style}</Label>
            <AppText variant="body">{L.question.text}</AppText>
            <View style={boardStyles.wrap}>
              {L.question.clues.map((c) => (
                <View key={c} style={[styles.clue, clueOn(c) && styles.clueOn]}><AppText variant="caption" color={colors.text} weight="600">{c}</AppText></View>
              ))}
            </View>
          </View>

          <View style={{ gap: spacing.xs }}>
            <View style={styles.rowBetween}>
              <AppText variant="h3">Lesson outline</AppText>
              <AppText variant="smallStrong">{step + 1} / {total}</AppText>
            </View>
            <ProgressBar value={step + 1} max={total} size="sm" label="Lesson progress" />
            <ChipScroller style={styles.gapSm}>
              {L.steps.map((x, i) => (
                <Pressable key={i} onPress={() => setStep(i)} accessibilityRole="button" accessibilityState={{ selected: i === step }}
                  accessibilityLabel={`Step ${i + 1}: ${x.title}. ${i < step ? 'Done' : i === step ? 'On the board now' : 'Up next'}`}
                  style={[styles.outline, i < step && styles.outlineDone, i === step && styles.outlineNow]}>
                  <View style={[styles.outlineNum, i === step && { backgroundColor: paper.ink }]}>
                    {i < step ? <Ionicons name="checkmark" size={14} color={colors.secondary} /> : <AppText variant="caption" weight="700" color={i === step ? colors.white : colors.text}>{i + 1}</AppText>}
                  </View>
                  <View style={{ maxWidth: 120 }}>
                    <AppText variant="caption" weight="700" color={colors.text} numberOfLines={2}>{x.title}</AppText>
                    <AppText variant="caption">{i < step ? 'Done' : i === step ? 'On the board now' : 'Up next'}</AppText>
                  </View>
                </Pressable>
              ))}
            </ChipScroller>
          </View>

          {s ? (
            <Chalkboard>
              <View style={styles.rowBetween}>
                <MitraTag label="Mitra · AI · writing" />
                <Hand color={paper.chalkMuted} size={15}>Step {step + 1} of {total}</Hand>
              </View>
              <Hand color={paper.marigold} size={26} bold>{s.title}</Hand>
              {s.lines.map((l, i) => <Hand key={i} size={18}>{l}</Hand>)}
              {s.trap ? (
                <>
                  <View style={boardStyles.dashedRule} />
                  <Hand color={paper.marigold} size={16}>Trap: {s.trap}</Hand>
                </>
              ) : null}
              {s.diagram ? (
                <View style={{ alignItems: 'center' }}>
                  <SeatingDiagram seats={s.diagram.seats} placed={s.diagram.placed} arrow={s.diagram.arrow} size={230} center={s.diagram.arrow ? 'count back' : 'centre'} />
                </View>
              ) : null}
              <View style={styles.stepNav}>
                <Button title="Previous" size="sm" variant="outlineLight" leftIcon="arrow-back" disabled={step === 0} onPress={() => setStep((x) => Math.max(0, x - 1))} />
                <View style={styles.dots} importantForAccessibility="no-hide-descendants">
                  {L.steps.map((_, i) => <View key={i} style={[styles.dotSm, i === step && styles.dotOn, i < step && { backgroundColor: paper.marigold }]} />)}
                </View>
                <Button title={step === total - 1 ? 'Done' : 'Next step'} size="sm" variant="accent" rightIcon={step === total - 1 ? 'checkmark' : 'arrow-forward'}
                  disabled={step === total - 1} onPress={() => setStep((x) => Math.min(total - 1, x + 1))} />
              </View>
            </Chalkboard>
          ) : null}

          <CheckYourself lesson={L} />

          <View style={[styles.askCard]}>
            <View style={styles.row}>
              <Mitra size={36} />
              <View style={styles.flex}>
                <AppText variant="h3">Ask Mitra</AppText>
                <AppText variant="caption" color={colors.secondary}>● AI coach · knows this board</AppText>
              </View>
            </View>
            <Chat compact context={context} quickReplies={['Explain facing outside', 'Give me a harder one', 'Explain in Hindi']} />
          </View>
        </>
      ) : lesson.loading && id ? <LoadingSkeleton /> : null}
      <AiErrorNotice error={lesson.error} onRetry={lesson.reload} />
    </View>
  );
}

// ---------- deep dives (unchanged) ----------
const MODES: { value: AiMode; label: string; feature: string }[] = [
  { value: 'smart', label: 'Smart', feature: 'smart_credits' },
  { value: 'master', label: 'Master', feature: 'master_credits' },
  { value: 'ultra', label: 'Ultra', feature: 'ultra_credits' },
];

function DeepDives({ solutionId, initialText }: { solutionId?: string; initialText?: string }) {
  const [text, setText] = useState(initialText ?? '');
  const [mode, setMode] = useState<AiMode>('smart');
  const [dive, setDive] = useState<DeepDive | null>(null);
  const [support, setSupport] = useState<string | null>(null);
  const list = useAiQuery(() => aiService.myDeepDives(), 'dives');
  const run = useAiAction(aiService.deepDive);
  const go = async () => {
    setSupport(null);
    const r = await run.run({ mode, solution_id: solutionId, text: solutionId ? undefined : text.trim() });
    if (!r) return;
    if (isSupportReply(r)) return setSupport(r.support);
    setDive(r);
    list.reload();
  };
  return (
    <View>
      <SupportBanner message={support} />
      <Card>
        {solutionId ? <AppText variant="small">Deep dive on the question you just solved.</AppText> : (
          <Input label="Question or concept" multiline value={text} onChangeText={setText} maxLength={4000} placeholder="Paste a question you got wrong, or name a concept" />
        )}
        <View style={styles.gap}>
          <SegmentedControl value={mode} onChange={setMode} accessibilityLabel="Tutor level" segments={MODES.map((m) => ({ value: m.value, label: m.label }))} />
        </View>
        <View style={[styles.row, styles.gap]}><AllowanceBadge feature={MODES.find((m) => m.value === mode)!.feature} label={`${mode} credits`} /></View>
        <Button title={run.busy ? 'Building your deep dive…' : 'Start deep dive'} loading={run.busy} style={styles.gap} disabled={!solutionId && text.trim().length < 3} onPress={go} />
        <AiErrorNotice error={run.error} onRetry={go} />
      </Card>
      {dive ? (
        <Card style={styles.gap}>
          <ArtifactHeader a={dive} extra={dive.mode ? <Badge label={dive.mode} tone="primary" /> : null} />
          <DeepDiveView p={dive.payload} note={dive.personal_note} />
        </Card>
      ) : null}
      <AppText variant="h3" style={styles.gap}>Your deep dives</AppText>
      <Card style={styles.gapSm}>
        {list.data?.length ? list.data.map((d, i) => (
          <View key={`${d.id}-${i}`}>
            {i > 0 && <Divider />}
            <ListRow icon="school-outline" title={d.title} subtitle={`${d.mode} · ${formatDate(d.saved_at)}`} onPress={() => router.push(`/ai/artifact/${d.id}`)} />
          </View>
        )) : <AppText variant="small">{list.loading ? 'Loading…' : 'Deep dives you make are saved here.'}</AppText>}
      </Card>
    </View>
  );
}

type Tab = 'board' | 'chat' | 'deep';

export default function Tutor() {
  const params = useLocalSearchParams<{ tab?: string; solution?: string; text?: string }>();
  const [tab, setTab] = useState<Tab>(params.tab === 'deep' ? 'deep' : params.tab === 'chat' ? 'chat' : 'board');
  const header = (
    <View style={styles.header}>
      <SegmentedControl value={tab} onChange={setTab} accessibilityLabel="Tutor"
        segments={[{ value: 'board', label: 'Blackboard' }, { value: 'chat', label: 'Ask Mitra' }, { value: 'deep', label: 'Deep dives' }]} />
    </View>
  );
  if (tab === 'chat') return <Screen scroll={false} keyboard header={header}><Chat /></Screen>;
  if (tab === 'deep') return <Screen keyboard header={header}><DeepDives solutionId={params.solution} initialText={params.text} /></Screen>;
  return <Screen keyboard header={header}><Blackboard /></Screen>;
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  gap: { marginTop: spacing.md },
  gapSm: { marginTop: spacing.sm },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, alignItems: 'center' },
  rowBetween: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, flexWrap: 'wrap' },
  header: { paddingHorizontal: spacing.lg, paddingTop: spacing.md },
  chatCompact: { maxHeight: 360 },
  bubble: { maxWidth: '88%', borderRadius: radii.lg, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, gap: 2 },
  mine: { alignSelf: 'flex-end', backgroundColor: colors.card, borderWidth: 1.5, borderColor: paper.ink },
  coach: { alignSelf: 'flex-start', backgroundColor: paper.chalk, borderTopLeftRadius: 4 },
  support: { alignSelf: 'flex-start', backgroundColor: colors.secondarySoft, borderWidth: 2, borderColor: colors.secondary },
  composer: { flexDirection: 'row', alignItems: 'flex-end', gap: spacing.sm },
  input: { flex: 1, minHeight: 44, maxHeight: 120, borderWidth: 1.5, borderColor: paper.ink, borderRadius: radii.md, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, color: colors.text, backgroundColor: colors.card },
  tutorPill: { flexDirection: 'row', alignItems: 'center', gap: 6, alignSelf: 'flex-start', backgroundColor: paper.chalk, borderRadius: radii.full, paddingHorizontal: 12, paddingVertical: 6 },
  dot: { width: 7, height: 7, borderRadius: 4, backgroundColor: paper.marigold },
  clue: { borderWidth: 1, borderColor: colors.border, backgroundColor: colors.background, borderRadius: radii.full, paddingHorizontal: 10, paddingVertical: 5 },
  clueOn: { backgroundColor: paper.stickyYellow, borderColor: paper.ink },
  outline: { flexDirection: 'row', alignItems: 'center', gap: 8, padding: spacing.sm, borderRadius: radii.md, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card },
  outlineDone: { backgroundColor: colors.secondarySoft, borderColor: colors.secondarySoft },
  outlineNow: { backgroundColor: paper.stickyYellow, borderColor: paper.ink, borderWidth: 1.5 },
  outlineNum: { width: 26, height: 26, borderRadius: 13, borderWidth: 1.5, borderColor: paper.ink, alignItems: 'center', justifyContent: 'center' },
  stepNav: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, marginTop: spacing.sm },
  dots: { flexDirection: 'row', gap: 5, flexShrink: 1 },
  dotSm: { width: 7, height: 7, borderRadius: 4, backgroundColor: board.dashed },
  dotOn: { width: 18, backgroundColor: paper.marigold },
  askCard: { backgroundColor: colors.card, borderRadius: radii.lg, borderWidth: 1.5, borderColor: paper.ink, padding: spacing.lg, gap: spacing.xs },
});
