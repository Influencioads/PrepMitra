import { useRef, useState } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import type { CurrentAffairs, RevisionSubmitResult, RevisionToday, WritingEvaluation, WritingTaskType } from '@prepmitra/shared';
import { AppText, Badge, Button, Card, Input, Screen, SegmentedControl, Select, SwitchRow } from '@/components';
import { AiErrorNotice, AllowanceBadge, useAiAction } from '@/features/ai/AiUi';
import { ArtifactHeader, CheatCardView, CurrentAffairsView, Section, WritingView } from '@/features/ai/AiViews';
import { aiService } from '@/services/aiService';
import { colors, paper, radii, spacing } from '@/theme';

type Tab = 'revision' | 'current' | 'writing';

function Revision() {
  const [session, setSession] = useState<RevisionToday | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [hints, setHints] = useState<Record<string, boolean>>({});
  const [result, setResult] = useState<RevisionSubmitResult | null>(null);
  const started = useRef(Date.now());
  const start = useAiAction(aiService.revisionToday);
  const submit = useAiAction(aiService.submitRevision);
  const begin = async () => {
    setResult(null); setAnswers({}); setHints({});
    const r = await start.run(10);
    if (r) { setSession(r); started.current = Date.now(); }
  };
  const finish = async () => {
    if (!session) return;
    const per = Math.round((Date.now() - started.current) / 1000 / Math.max(1, session.questions.length));
    const r = await submit.run(session.id, session.questions.map((q) => ({ question_id: q.question_id, answer: answers[q.question_id] ?? null, time_spent_sec: per })));
    if (r) setResult(r);
  };
  const byId = new Map(result?.results.map((r) => [r.question_id, r]));
  return (
    <View>
      <Card>
        <AppText variant="bodyStrong">Today’s spaced revision</AppText>
        <AppText variant="small">Questions you got wrong before, due again today, each with an AI hint. Your locked cheat-code cards come along as flashcards.</AppText>
        <Button title={session ? 'New set' : 'Start revision'} style={styles.gap} loading={start.busy} onPress={begin} />
        <AiErrorNotice error={start.error} onRetry={begin} />
      </Card>
      {result ? <Card style={styles.gap}><AppText variant="h3">{result.correct} of {result.total} correct</AppText></Card> : null}
      {session?.questions.map((q, i) => {
        const r = byId.get(q.question_id);
        return (
          <Card key={q.question_id} style={styles.gap}>
            <View style={styles.row}>
              <AppText variant="caption">Q{i + 1} · target {q.target_time_sec}s</AppText>
              {q.topic ? <Badge label={q.topic} /> : null}
              {r ? <Badge label={r.status} tone={r.status === 'correct' ? 'success' : 'error'} /> : null}
            </View>
            <AppText variant="bodyStrong" style={styles.gapSm}>{q.text}</AppText>
            <View style={[styles.gapSm, { gap: spacing.xs }]}>
              {q.options.map((o) => {
                const picked = answers[q.question_id] === o.key;
                const correct = r && String(r.correct_answer) === o.key;
                return (
                  <Pressable key={o.key} disabled={!!result} accessibilityRole="radio" accessibilityState={{ selected: picked }}
                    onPress={() => setAnswers((s) => ({ ...s, [q.question_id]: o.key }))}
                    style={[styles.option, picked && styles.picked, correct && styles.right, picked && r && !correct && styles.wrong]}>
                    <AppText variant="small" color={colors.text}><AppText variant="smallStrong">{o.key}.</AppText> {o.text}</AppText>
                  </Pressable>
                );
              })}
            </View>
            {q.hint && !result ? (hints[q.question_id]
              ? <View style={styles.hint}><AppText variant="small" color={colors.text}>💡 {q.hint}</AppText></View>
              : <Button title="Show hint" size="sm" variant="ghost" leftIcon="bulb-outline" onPress={() => setHints((s) => ({ ...s, [q.question_id]: true }))} />) : null}
            {r?.explanation ? <AppText variant="small" style={styles.gapSm}>{r.explanation}</AppText> : null}
          </Card>
        );
      })}
      {session && !result && session.questions.length > 0 ? <Button title="Check answers" style={styles.gap} loading={submit.busy} onPress={finish} /> : null}
      <AiErrorNotice error={submit.error} onRetry={finish} />
      {session?.flashcards.length ? (
        <Section title="Your flashcards">
          <View style={{ gap: spacing.sm }}>{session.flashcards.map((c) => <CheatCardView key={c.id} p={c.payload} />)}</View>
        </Section>
      ) : null}
    </View>
  );
}

function Current() {
  const [ca, setCa] = useState<CurrentAffairs | null>(null);
  const run = useAiAction(aiService.currentAffairs);
  const load = async () => { const r = await run.run(); if (r) setCa(r); };
  return (
    <View>
      {!ca ? (
        <Card>
          <AppText variant="bodyStrong">Daily current affairs</AppText>
          <AppText variant="small">Today’s exam-relevant news, with a GA quiz fact-checked by a second model.</AppText>
          <Button title="Show today’s digest" style={styles.gap} loading={run.busy} onPress={load} />
        </Card>
      ) : <Card><ArtifactHeader a={ca} /><CurrentAffairsView p={ca.payload} /></Card>}
      <AiErrorNotice error={run.error} onRetry={load} />
    </View>
  );
}

const TASKS: { value: WritingTaskType; label: string }[] = [
  { value: 'essay', label: 'Essay' }, { value: 'formal_letter', label: 'Formal letter' }, { value: 'informal_letter', label: 'Informal letter' },
  { value: 'precis', label: 'Précis' }, { value: 'report', label: 'Report' }, { value: 'paragraph', label: 'Paragraph' },
];

function Writing() {
  const [task, setTask] = useState<WritingTaskType>('essay');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [limit, setLimit] = useState('250');
  const [rewrite, setRewrite] = useState(false);
  const [ev, setEv] = useState<WritingEvaluation | null>(null);
  const run = useAiAction(aiService.evaluateWriting);
  const words = answer.trim() ? answer.trim().split(/\s+/).length : 0;
  const go = async () => {
    const r = await run.run({ task_type: task, question: question.trim(), answer, word_limit: Number(limit) || null, topper_rewrite: rewrite });
    if (r) setEv(r);
  };
  return (
    <View>
      <Card>
        <View style={{ gap: spacing.sm }}>
          <Select label="Task" value={task} onChange={setTask} options={TASKS} />
          <Input label="Word limit" value={limit} onChangeText={setLimit} keyboardType="number-pad" />
          <Input label="Question" multiline value={question} onChangeText={setQuestion} maxLength={3000} />
          <Input label={`Your answer (${words} words)`} multiline value={answer} onChangeText={setAnswer} maxLength={16000} hint="At least 30 words." />
          <SwitchRow label="Also show a topper rewrite" description="Uses 1 Master credit." value={rewrite} onValueChange={setRewrite} />
          <AllowanceBadge feature="descriptive_evals" label="Evaluations" />
          <Button title={run.busy ? 'Evaluating…' : 'Evaluate'} loading={run.busy} disabled={question.trim().length < 5 || words < 30} onPress={go} />
          <AiErrorNotice error={run.error} onRetry={go} />
        </View>
      </Card>
      {ev ? <Card style={styles.gap}><ArtifactHeader a={ev} /><WritingView p={ev.payload} /></Card> : null}
    </View>
  );
}

export default function Practice() {
  const params = useLocalSearchParams<{ tab?: string }>();
  const [tab, setTab] = useState<Tab>(params.tab === 'current' || params.tab === 'writing' ? params.tab : 'revision');
  return (
    <Screen keyboard>
      <SegmentedControl value={tab} onChange={setTab} accessibilityLabel="Practice"
        segments={[{ value: 'revision', label: 'Revision' }, { value: 'current', label: 'Current affairs' }, { value: 'writing', label: 'Writing' }]} />
      <View style={styles.gap}>{tab === 'revision' ? <Revision /> : tab === 'current' ? <Current /> : <Writing />}</View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  gap: { marginTop: spacing.md },
  gapSm: { marginTop: spacing.sm },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.xs, alignItems: 'center' },
  option: { borderWidth: 1, borderColor: colors.border, borderRadius: radii.md, padding: spacing.sm, minHeight: 44, justifyContent: 'center' },
  picked: { borderColor: colors.primary, backgroundColor: colors.primarySoft },
  right: { borderColor: '#86EFAC', backgroundColor: colors.successSoft },
  wrong: { borderColor: '#FCA5A5', backgroundColor: colors.errorSoft },
  hint: { marginTop: spacing.sm, backgroundColor: paper.stickyYellow, borderRadius: radii.md, padding: spacing.sm },
});
