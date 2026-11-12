import { useState } from 'react';
import { Image, Pressable, StyleSheet, View } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import * as DocumentPicker from 'expo-document-picker';
import { isSupportReply, type AiOption, type DoubtAnswer, type DoubtResult, type DoubtSolution } from '@prepmitra/shared';
import { AppText, Badge, Button, Card, Input, Screen, SegmentedControl, SwitchRow, toast } from '@/components';
import { AiErrorNotice, AllowanceBadge, SupportBanner, useAiAction } from '@/features/ai/AiUi';
import { Bullets, Callout, PracticeQuestions, Section } from '@/features/ai/AiViews';
import { aiService, uriToDataUrl } from '@/services/aiService';
import { errorMessage } from '@/services';
import { colors, radii, spacing } from '@/theme';

const KEYS = ['A', 'B', 'C', 'D'];
const VERIFICATION: Record<DoubtAnswer['verification'], string> = {
  code_checked: 'Checked by calculation', two_models: 'Verified by two AI models', human: 'Checked by our team', unverified: 'Not verified',
};

function SolutionBody({ s }: { s: DoubtSolution }) {
  return (
    <View>
      {s.answer_text ? <AppText variant="bodyStrong" style={styles.gap}>{s.answer_text}</AppText> : null}
      <Section title="Steps"><Bullets items={s.steps} ordered /></Section>
      <View style={[styles.gap, { gap: spacing.sm }]}>
        {s.shortcut ? <Callout tone="success" title="Shortcut">{s.shortcut}</Callout> : null}
        {s.common_trap ? <Callout tone="warning" title="Common trap">{s.common_trap}</Callout> : null}
        {s.memory_hook ? <Callout title="Memory hook">{s.memory_hook}</Callout> : null}
        {s.real_life_example ? <Callout title="Real-life example">{s.real_life_example}</Callout> : null}
      </View>
      {s.practice_question ? <Section title="Try one yourself"><PracticeQuestions questions={[s.practice_question]} /></Section> : null}
    </View>
  );
}

function AnswerCard({ r, text }: { r: DoubtAnswer; text: string }) {
  const [again, setAgain] = useState<DoubtSolution | null>(null);
  const [voted, setVoted] = useState(false);
  const explain = useAiAction(aiService.explainAgain);
  const vote = async (body: { helpful?: boolean; report_error?: boolean }) => {
    if (!r.solution_id) return;
    try {
      await aiService.doubtFeedback(r.solution_id, body);
      setVoted(true);
      toast.success(body.report_error ? 'Thanks. Our team will check this answer.' : 'Thanks for the feedback.');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };
  return (
    <Card style={styles.gap}>
      <AppText variant="h2">Answer: <AppText variant="h2" color={colors.primary}>{r.answer}</AppText></AppText>
      <View style={styles.row}>
        <Badge label={VERIFICATION[r.verification]} tone={r.verified ? 'success' : 'warning'} icon="shield-checkmark-outline" />
        {r.source === 'exact' || r.source === 'meaning' ? <Badge label="Instant from library" /> : null}
        {r.premium_used ? <Badge label="Premium model" tone="primary" /> : null}
      </View>
      {r.notice ? <View style={styles.gap}><Callout tone="warning" title="Please double-check">{r.notice}</Callout></View> : null}
      {r.personal_note ? <View style={styles.gap}><Callout tone="warning" title="About your choice">{r.personal_note}</Callout></View> : null}
      <SolutionBody s={again ?? r.solution} />
      <View style={[styles.gap, { gap: spacing.sm }]}>
        {r.solution_id ? (
          <Button title="Still confused? Explain again" variant="outline" leftIcon="refresh" loading={explain.busy}
            onPress={async () => { const x = await explain.run(r.solution_id!); if (x) setAgain(x.solution); }} />
        ) : null}
        <Button title="Deep dive on this" variant="soft" leftIcon="school-outline"
          onPress={() => router.push({ pathname: '/ai/tutor', params: r.solution_id ? { tab: 'deep', solution: r.solution_id } : { tab: 'deep', text: text.slice(0, 1500) } })} />
        <AiErrorNotice error={explain.error} />
        {r.solution_id && !voted ? (
          <View style={styles.row}>
            <Button title="Helpful" size="sm" variant="ghost" leftIcon="thumbs-up-outline" onPress={() => vote({ helpful: true })} />
            <Button title="Not helpful" size="sm" variant="ghost" leftIcon="thumbs-down-outline" onPress={() => vote({ helpful: false })} />
            <Button title="Report an error" size="sm" variant="ghost" leftIcon="flag-outline" onPress={() => vote({ report_error: true })} />
          </View>
        ) : null}
      </View>
    </Card>
  );
}

export default function DoubtSolver() {
  const params = useLocalSearchParams<{ tab?: string }>();
  const [tab, setTab] = useState<'text' | 'photo'>(params.tab === 'photo' ? 'photo' : 'text');
  const [text, setText] = useState('');
  const [options, setOptions] = useState(['', '', '', '']);
  const [chosen, setChosen] = useState<string | null>(null);
  const [escalate, setEscalate] = useState(false);
  const [image, setImage] = useState<string | null>(null);
  const [result, setResult] = useState<DoubtResult | null>(null);
  const [asked, setAsked] = useState('');
  const solve = useAiAction(aiService.solveDoubt);
  const photo = useAiAction(aiService.photoDoubt);
  const action = tab === 'photo' ? photo : solve;

  const pick = async () => {
    try {
      const r = await DocumentPicker.getDocumentAsync({ type: ['image/*'], copyToCacheDirectory: true, multiple: false });
      if (r.canceled || !r.assets[0]) return;
      const dataUrl = await uriToDataUrl(r.assets[0].uri);
      if (dataUrl.length > 6_000_000) return toast.error('That photo is too large. Crop it to just the question.');
      setImage(dataUrl);
    } catch (e) {
      toast.error(errorMessage(e, 'Could not open the photo.'));
    }
  };

  const submit = async () => {
    setResult(null);
    if (tab === 'text') {
      const opts: AiOption[] = options.map((o, i) => ({ key: KEYS[i]!, text: o.trim() })).filter((o) => o.text);
      const r = await solve.run({ text: text.trim(), options: opts, chosen, escalate });
      if (r) { setResult(r); setAsked(text.trim()); }
    } else if (image) {
      const r = await photo.run({ image, chosen });
      if (r) { setResult(r); setAsked(r.read_question?.text ?? ''); }
    }
  };

  return (
    <Screen keyboard>
      <View style={styles.row}><AllowanceBadge feature="doubts" label="Doubts" /><AllowanceBadge feature="photo_doubts" label="Photo" /></View>
      {isSupportReply(result) ? <View style={styles.gap}><SupportBanner message={result.support} /></View> : null}
      <View style={styles.gap}>
        <SegmentedControl value={tab} onChange={(v) => { setTab(v); setResult(null); }} accessibilityLabel="How to ask"
          segments={[{ value: 'text', label: 'Type it' }, { value: 'photo', label: 'Photo' }]} />
      </View>
      <Card style={styles.gap}>
        {tab === 'text' ? (
          <View style={{ gap: spacing.sm }}>
            <Input label="Question" multiline value={text} onChangeText={setText} maxLength={4000}
              placeholder="e.g. A price falls by 20%. By what percent must it rise to get back?" />
            {options.map((o, i) => (
              <Input key={i} label={`Option ${KEYS[i]} (optional)`} value={o} maxLength={500} onChangeText={(v) => setOptions((s) => s.map((x, j) => (j === i ? v : x)))} />
            ))}
            <SwitchRow label="Use the premium model" description="For a tricky question. Uses a premium doubt (Pro) when you have one." value={escalate} onValueChange={setEscalate} />
          </View>
        ) : (
          <View style={{ gap: spacing.sm }}>
            {image ? <Image source={{ uri: image }} style={styles.photo} resizeMode="contain" accessibilityLabel="Your question photo" /> : null}
            <Button title={image ? 'Choose another photo' : 'Choose a photo of the question'} variant={image ? 'outline' : 'soft'} leftIcon="camera-outline" onPress={pick} />
            <AppText variant="caption">One question per photo, with its options. Photo doubts come with the AI Tutor packs.</AppText>
          </View>
        )}
        <AppText variant="label" style={styles.gap}>Your answer (optional)</AppText>
        <View style={styles.row}>
          {KEYS.map((k) => (
            <Pressable key={k} accessibilityRole="radio" accessibilityState={{ selected: chosen === k }} accessibilityLabel={`I chose ${k}`}
              onPress={() => setChosen(chosen === k ? null : k)} style={[styles.key, chosen === k && styles.keyOn]}>
              <AppText variant="bodyStrong" color={chosen === k ? colors.white : colors.text}>{k}</AppText>
            </Pressable>
          ))}
        </View>
        <Button title={action.busy ? 'Solving and checking…' : 'Solve'} leftIcon="sparkles" loading={action.busy} style={styles.gap}
          disabled={tab === 'text' ? text.trim().length < 8 : !image} onPress={submit} />
        <AiErrorNotice error={action.error} onRetry={submit} />
      </Card>
      {result && !isSupportReply(result) ? (
        <>
          {result.read_question ? (
            <Card style={styles.gap}>
              <AppText variant="caption">MITRA READ THIS QUESTION</AppText>
              <AppText variant="small" color={colors.text}>{result.read_question.text}</AppText>
            </Card>
          ) : null}
          <AnswerCard r={result} text={asked} />
        </>
      ) : null}
    </Screen>
  );
}

const styles = StyleSheet.create({
  gap: { marginTop: spacing.md },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.xs, alignItems: 'center' },
  photo: { width: '100%', height: 220, borderRadius: radii.md, backgroundColor: colors.background },
  key: { width: 44, height: 44, borderRadius: 22, borderWidth: 1, borderColor: colors.borderStrong, alignItems: 'center', justifyContent: 'center' },
  keyOn: { backgroundColor: colors.primary, borderColor: colors.primary },
});
