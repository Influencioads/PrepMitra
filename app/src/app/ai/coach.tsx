import { useMemo, useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { examSlugFromId, getExamById, type CheatCard, type CoachSession, type CoachTestResult } from '@prepmitra/shared';
import { AppText, Button, Card, CardHeader, Input, Screen, SegmentedControl, Select, SwitchRow } from '@/components';
import { AiErrorNotice, AllowanceBadge, SupportBanner, useAiAction, useAiQuery } from '@/features/ai/AiUi';
import { CheatCardView } from '@/features/ai/AiViews';
import { aiService } from '@/services/aiService';
import { useProfileStore } from '@/store';
import { colors, radii, spacing } from '@/theme';

const STEPS = ['Spot', 'Shape', 'Test', 'Lock'];

function Flow({ onLocked }: { onLocked: () => void }) {
  const targets = useProfileStore((s) => s.profile.targetExamIds);
  const exams = useMemo(() => {
    const list = targets.map((id) => getExamById(id)).filter((e): e is NonNullable<typeof e> => !!e);
    const fallback = getExamById('ssc-cgl');
    return list.length ? list : fallback ? [fallback] : [];
  }, [targets]);
  const [examId, setExamId] = useState(exams[0]?.id ?? 'ssc-cgl');
  const topics = useAiQuery(() => aiService.coachTopics(examSlugFromId(examId)), examId);
  const [topicId, setTopicId] = useState('');
  const [session, setSession] = useState<CoachSession | null>(null);
  const [thread, setThread] = useState<{ who: 'coach' | 'me'; text: string }[]>([]);
  const [msg, setMsg] = useState('');
  const [step, setStep] = useState(0);
  const [rule, setRule] = useState('');
  const [test, setTest] = useState<CoachTestResult | null>(null);
  const [share, setShare] = useState(false);
  const [support, setSupport] = useState<string | null>(null);
  const [card, setCard] = useState<CheatCard | null>(null);
  const start = useAiAction(aiService.coachStart);
  const reply = useAiAction(aiService.coachReply);
  const runTest = useAiAction(aiService.coachTest);
  const lock = useAiAction(aiService.coachLock);

  const begin = async () => {
    const s = await start.run(Number(topicId));
    if (!s) return;
    setSession(s); setThread([{ who: 'coach', text: s.coach }]); setStep(1); setTest(null); setCard(null); setRule('');
  };
  const send = async () => {
    if (!session || !msg.trim()) return;
    const m = msg.trim();
    setMsg('');
    setThread((t) => [...t, { who: 'me', text: m }]);
    const r = await reply.run(session.session_id, m);
    if (!r) return;
    if (r.support) setSupport(r.support);
    setThread((t) => [...t, { who: 'coach', text: r.coach }]);
    if (r.rule_draft) setRule(r.rule_draft);
    if (r.step === 'test') setStep(2);
  };
  const doTest = async () => {
    if (!session) return;
    const r = await runTest.run(session.session_id, rule);
    if (!r) return;
    setTest(r);
    setStep(r.step === 'lock' ? 3 : 1);
  };
  const doLock = async () => {
    if (!session) return;
    const c = await lock.run(session.session_id, share);
    if (c) { setCard(c); setStep(4); onLocked(); }
  };

  if (!session) {
    return (
      <Card>
        <AppText variant="small">Mitra shows three solved questions of one type. You find the pattern, write the rule, test it on five real questions and lock it as a revision card.</AppText>
        <View style={[styles.gap, { gap: spacing.sm }]}>
          <Select label="Exam" value={examId} onChange={(v) => { setExamId(v); setTopicId(''); }} options={exams.map((e) => ({ value: e.id, label: e.shortTitle }))} />
          <Select label="Topic" value={topicId} placeholder={topics.loading ? 'Loading topics…' : 'Choose a topic'} onChange={setTopicId}
            options={(topics.data ?? []).map((t) => ({ value: String(t.id), label: t.name }))} />
          <AiErrorNotice error={topics.error} onRetry={topics.reload} />
          <AllowanceBadge feature="cheat_code_sessions" label="Sessions" />
          <Button title="Start (uses 1 session)" leftIcon="flash" loading={start.busy} disabled={!topicId} onPress={begin} />
          <AiErrorNotice error={start.error} onRetry={begin} />
        </View>
      </Card>
    );
  }

  return (
    <View>
      <View style={styles.steps}>
        {STEPS.map((s, i) => (
          <View key={s} style={[styles.step, i <= Math.min(step, 3) && styles.stepOn]}>
            <AppText variant="caption" weight="700" color={i <= Math.min(step, 3) ? colors.white : colors.textSecondary}>{s}</AppText>
          </View>
        ))}
      </View>
      <SupportBanner message={support} />
      <Card style={styles.gap}>
        <CardHeader title={`Spot the pattern: ${session.topic}`} />
        {session.solved_questions.map((q, i) => (
          <View key={q.question_id} style={styles.solved}>
            <AppText variant="smallStrong">{i + 1}. {q.text}</AppText>
            <AppText variant="small" color={colors.text}>Answer {String(q.answer)}. {q.explanation}</AppText>
          </View>
        ))}
      </Card>
      <Card style={styles.gap}>
        <CardHeader title="Shape your rule" subtitle="Mitra asks until it is exact." />
        {thread.map((m, i) => (
          <View key={i} style={[styles.bubble, m.who === 'coach' ? styles.coach : styles.me]}>
            <AppText variant="small" color={colors.text}>{m.text}</AppText>
          </View>
        ))}
        {step === 1 ? (
          <View style={styles.gapSm}>
            <Input label="Your rule" value={msg} onChangeText={setMsg} maxLength={1500} multiline placeholder="My rule is…" />
            <Button title="Send" size="sm" leftIcon="send" loading={reply.busy} disabled={!msg.trim()} onPress={send} style={styles.gapSm} />
          </View>
        ) : null}
        <AiErrorNotice error={reply.error} onRetry={send} />
      </Card>
      {step >= 1 && step < 4 ? (
        <Card style={styles.gap}>
          <CardHeader title="Test it" subtitle="Your rule runs on five new questions." />
          <Input label="Rule" value={rule} onChangeText={setRule} multiline maxLength={1000} />
          <Button title="Test my rule" style={styles.gapSm} loading={runTest.busy} disabled={rule.trim().length < 10} onPress={doTest} />
          <AiErrorNotice error={runTest.error} onRetry={doTest} />
          {test ? (
            <View style={styles.gapSm}>
              <AppText variant="bodyStrong">Works on {Math.round(test.pass_rate * 100)}% where it applies</AppText>
              {test.results.map((r, i) => (
                <View key={i} style={styles.solved}>
                  <AppText variant="smallStrong">{r.works ? '✓' : '✗'} {r.question.text}</AppText>
                  <AppText variant="small">{r.applies ? r.working : 'Rule does not apply here.'}</AppText>
                </View>
              ))}
              <AppText variant="small" color={colors.text} style={styles.gapSm}>{test.advice}</AppText>
            </View>
          ) : null}
        </Card>
      ) : null}
      {step === 3 ? (
        <Card style={styles.gap}>
          <SwitchRow label="Share with other students" description="Cards that pass 80% can join the shortcut library." value={share} onValueChange={setShare} />
          <Button title="Lock as a revision card" leftIcon="lock-closed" loading={lock.busy} onPress={doLock} />
          <AiErrorNotice error={lock.error} onRetry={doLock} />
        </Card>
      ) : null}
      {card ? (
        <Card style={styles.gap}>
          <AppText variant="bodyStrong" color={colors.success}>Locked. It will come back in Revision AI.</AppText>
          <View style={styles.gapSm}><CheatCardView p={card.payload} /></View>
          <Button title="Start another" variant="outline" style={styles.gap} onPress={() => { setSession(null); setStep(0); }} />
        </Card>
      ) : null}
    </View>
  );
}

function Cards({ version }: { version: number }) {
  const cards = useAiQuery(() => aiService.coachCards(), `cards-${version}`);
  if (cards.error) return <AiErrorNotice error={cards.error} onRetry={cards.reload} />;
  if (!cards.data?.length) return <AppText variant="small">{cards.loading ? 'Loading…' : 'No cards yet. Finish a coach session to lock your first rule.'}</AppText>;
  return <View style={{ gap: spacing.sm }}>{cards.data.map((c) => <CheatCardView key={c.id} p={c.payload} />)}</View>;
}

function Library() {
  const list = useAiQuery(() => aiService.shortcuts(), 'shortcuts');
  if (list.error) return <AiErrorNotice error={list.error} onRetry={list.reload} />;
  return <View style={{ gap: spacing.sm }}>{(list.data ?? []).map((s) => <CheatCardView key={s.id} p={s.payload} />)}</View>;
}

export default function Coach() {
  const [tab, setTab] = useState<'coach' | 'cards' | 'library'>('coach');
  const [version, setVersion] = useState(0);
  return (
    <Screen keyboard>
      <SegmentedControl value={tab} onChange={setTab} accessibilityLabel="Coach"
        segments={[{ value: 'coach', label: 'Coach' }, { value: 'cards', label: 'My cards' }, { value: 'library', label: 'Library' }]} />
      <View style={styles.gap}>
        {tab === 'coach' ? <Flow onLocked={() => setVersion((v) => v + 1)} /> : tab === 'cards' ? <Cards version={version} /> : <Library />}
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  gap: { marginTop: spacing.md },
  gapSm: { marginTop: spacing.sm },
  steps: { flexDirection: 'row', gap: spacing.xs, marginBottom: spacing.sm },
  step: { flex: 1, alignItems: 'center', paddingVertical: 6, borderRadius: radii.sm, backgroundColor: colors.background },
  stepOn: { backgroundColor: colors.primary },
  solved: { borderWidth: 1, borderColor: colors.border, borderRadius: radii.md, padding: spacing.sm, marginTop: spacing.xs, gap: 2 },
  bubble: { borderRadius: radii.md, padding: spacing.sm, marginTop: spacing.xs, maxWidth: '90%' },
  coach: { alignSelf: 'flex-start', backgroundColor: colors.secondarySoft },
  me: { alignSelf: 'flex-end', backgroundColor: colors.primarySoft },
});
