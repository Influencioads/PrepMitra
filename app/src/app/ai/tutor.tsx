import { useEffect, useRef, useState } from 'react';
import { ScrollView, StyleSheet, TextInput, View, type ScrollViewInstance } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { formatDate, isSupportReply, type AiMode, type DeepDive } from '@prepmitra/shared';
import { AppText, Badge, Button, Card, Chip, Divider, Input, ListRow, Screen, SegmentedControl, SwitchRow } from '@/components';
import { AiErrorNotice, AllowanceBadge, SupportBanner, useAiAction, useAiQuery } from '@/features/ai/AiUi';
import { ArtifactHeader, DeepDiveView } from '@/features/ai/AiViews';
import { aiService } from '@/services/aiService';
import { colors, radii, spacing } from '@/theme';

interface Msg { id: string; role: 'user' | 'assistant'; content: string; support?: boolean }

function Chat() {
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

  const send = async (message: string, differently = false) => {
    const m = message.trim();
    if (!m || chat.busy) return;
    setText('');
    setLast(m);
    if (!differently) setMsgs((s) => [...s, { id: `u${Date.now()}`, role: 'user', content: m }]);
    const r = await chat.run({ message: m, session_id: sessionId, style: story ? 'story' : 'normal', explain_differently: differently });
    if (!r) return;
    setSessionId(r.session_id);
    setFollowUps(r.follow_ups);
    if (r.support) setSupport(r.support);
    setMsgs((s) => [...s, { id: `a${Date.now()}`, role: 'assistant', content: r.reply, support: !!r.support }]);
  };

  return (
    <View style={styles.flex}>
      <SupportBanner message={support} />
      <ScrollView ref={scroll} style={styles.flex} contentContainerStyle={{ gap: spacing.sm, paddingVertical: spacing.sm }}
        onContentSizeChange={() => scroll.current?.scrollToEnd({ animated: true })}>
        {msgs.length === 0 && !history.loading ? (
          <AppText variant="small">Ask Mitra anything about your preparation: a concept, a question from your mock, or how to plan your week.</AppText>
        ) : null}
        {msgs.map((m) => (
          <View key={m.id} style={[styles.bubble, m.role === 'user' ? styles.mine : m.support ? styles.support : styles.theirs]}>
            <AppText variant="small" color={m.role === 'user' ? colors.white : colors.text}>{m.content}</AppText>
          </View>
        ))}
        {chat.busy ? <AppText variant="caption">Mitra is thinking…</AppText> : null}
      </ScrollView>
      <AiErrorNotice error={chat.error} onRetry={() => send(last)} />
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: spacing.xs, paddingVertical: spacing.xs }}>
        {followUps.map((f) => <Chip key={f} label={f} onPress={() => send(f)} />)}
        {msgs.some((m) => m.role === 'assistant') ? <Chip label="Explain differently" icon="shuffle" onPress={() => send(last || 'Explain that differently', true)} /> : null}
      </ScrollView>
      <SwitchRow label="Story mode" value={story} onValueChange={setStory} />
      <View style={styles.composer}>
        <TextInput value={text} onChangeText={setText} placeholder="Ask Mitra…" maxLength={2000} multiline accessibilityLabel="Message"
          placeholderTextColor={colors.textMuted} style={styles.input} />
        <Button title="Send" size="sm" leftIcon="send" disabled={!text.trim() || chat.busy} onPress={() => send(text)} />
      </View>
    </View>
  );
}

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

export default function Tutor() {
  const params = useLocalSearchParams<{ tab?: string; solution?: string; text?: string }>();
  const [tab, setTab] = useState<'chat' | 'deep'>(params.tab === 'deep' ? 'deep' : 'chat');
  const header = (
    <View style={styles.header}>
      <SegmentedControl value={tab} onChange={setTab} accessibilityLabel="Tutor" segments={[{ value: 'chat', label: 'Ask Mitra' }, { value: 'deep', label: 'Deep dives' }]} />
      {tab === 'chat' ? <View style={[styles.row, styles.gapSm]}><AllowanceBadge feature="tutor_chat_turns" label="Chat turns" /></View> : null}
    </View>
  );
  if (tab === 'chat') {
    return <Screen scroll={false} keyboard header={header}><Chat /></Screen>;
  }
  return <Screen keyboard header={header}><DeepDives solutionId={params.solution} initialText={params.text} /></Screen>;
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  gap: { marginTop: spacing.md },
  gapSm: { marginTop: spacing.sm },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.xs },
  header: { paddingHorizontal: spacing.lg, paddingTop: spacing.md },
  bubble: { maxWidth: '85%', borderRadius: radii.lg, paddingHorizontal: spacing.md, paddingVertical: spacing.sm },
  mine: { alignSelf: 'flex-end', backgroundColor: colors.primary },
  theirs: { alignSelf: 'flex-start', backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  support: { alignSelf: 'flex-start', backgroundColor: colors.secondarySoft, borderWidth: 2, borderColor: colors.secondary },
  composer: { flexDirection: 'row', alignItems: 'flex-end', gap: spacing.sm },
  input: { flex: 1, minHeight: 44, maxHeight: 120, borderWidth: 1, borderColor: colors.borderStrong, borderRadius: radii.md, paddingHorizontal: spacing.md, paddingVertical: spacing.sm, color: colors.text, backgroundColor: colors.card },
});

