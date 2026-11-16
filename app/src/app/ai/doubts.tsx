import { useState } from 'react';
import { Image, Pressable, StyleSheet, View } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import * as DocumentPicker from 'expo-document-picker';
import Ionicons from '@expo/vector-icons/Ionicons';
import { isSupportReply, type AiOption, type DoubtAnswer, type DoubtResult, type DoubtSolution } from '@prepmitra/shared';
import { AppText, Button, Input, Screen, SegmentedControl, SwitchRow, toast } from '@/components';
import { AiErrorNotice, AllowanceBadge, SupportBanner, useAiAction } from '@/features/ai/AiUi';
import { Callout, PracticeQuestions } from '@/features/ai/AiViews';
import { AiNote, Chalkboard, Hand, Label, MitraTag, SectionHead, Sticky, board, boardStyles } from '@/features/ai/Board';
import { aiService, uriToDataUrl } from '@/services/aiService';
import { errorMessage } from '@/services';
import { colors, paper, radii, spacing } from '@/theme';

const KEYS = ['A', 'B', 'C', 'D'];
const VERIFICATION: Record<DoubtAnswer['verification'], string> = {
  code_checked: 'Checked by code', two_models: 'Verified by two AI models', human: 'Checked by our team', unverified: 'Not verified',
};

/** Which option is the answer: by key ("C", "(c)", "c) 40 s") or by matching text. */
function answerKey(answer: string, options: AiOption[]): string | null {
  const a = answer.trim();
  const m = /^\(?([a-e])\)?(?:[\s.):]|$)/i.exec(a);
  if (m && options.some((o) => o.key.toUpperCase() === m[1]!.toUpperCase())) return m[1]!.toUpperCase();
  const t = a.toLowerCase();
  const hit = options.find((o) => o.text.trim().toLowerCase() === t || (t.length > 1 && o.text.toLowerCase().includes(t)));
  return hit ? hit.key.toUpperCase() : null;
}

function Progress({ stage }: { stage: 0 | 1 | 2 }) {
  const items = ['Ask', 'Mitra solves', 'Understand'];
  return (
    <View style={styles.progress} accessibilityLabel={`Step ${stage + 1} of 3: ${items[stage]}`}>
      {items.map((l, i) => (
        <View key={l} style={[styles.stage, i === stage && styles.stageOn, i < stage && styles.stageDone]}>
          <View style={[styles.stageNum, i === stage && { backgroundColor: paper.marigold, borderColor: paper.marigold }]}>
            <AppText variant="caption" weight="700" color={paper.ink}>{i + 1}</AppText>
          </View>
          <AppText variant="caption" weight="700" color={i === stage ? colors.white : colors.text} numberOfLines={1}>{l}</AppText>
        </View>
      ))}
    </View>
  );
}

function Steps({ s }: { s: DoubtSolution }) {
  return (
    <View style={{ gap: spacing.md }}>
      {s.steps.map((step, i) => {
        const [first, ...rest] = step.split('\n').map((x) => x.trim()).filter(Boolean);
        return (
          <View key={i} style={styles.step}>
            <View style={styles.stepNum}><Hand color={paper.marigold} size={16} bold>{i + 1}</Hand></View>
            <View style={styles.flex}>
              <Hand size={17}>{first}</Hand>
              {rest.map((r, j) => <Hand key={j} size={20} bold color={i === s.steps.length - 1 ? paper.marigold : paper.chalkText}>{r}</Hand>)}
            </View>
          </View>
        );
      })}
    </View>
  );
}

function FinalAnswer({ r, options, s }: { r: DoubtAnswer; options: AiOption[]; s: DoubtSolution }) {
  const key = answerKey(s.answer ?? r.answer, options) ?? answerKey(r.answer, options);
  const checked = r.verification === 'code_checked';
  return (
    <View style={styles.final}>
      <View style={styles.rowBetween}>
        <Label>Final answer</Label>
        {r.verified ? (
          <View style={styles.row}>
            <Ionicons name="checkmark" size={14} color={colors.secondary} />
            <AppText variant="caption" color={colors.secondary} weight="700">
              {VERIFICATION[r.verification]}{checked && s.numeric_check ? `: ${s.numeric_check}` : ''}
            </AppText>
          </View>
        ) : <AppText variant="caption" color={colors.warningText} weight="700">{VERIFICATION[r.verification]}</AppText>}
      </View>
      {options.length && key ? (
        <View style={styles.finalOpts}>
          {options.map((o) => {
            const on = o.key.toUpperCase() === key;
            return (
              <View key={o.key} style={[styles.finalOpt, on && styles.finalOptOn]} accessibilityLabel={`${on ? 'Answer: ' : ''}option ${o.key}, ${o.text}`}>
                {on ? <Hand color={paper.pen} size={13} style={styles.thisOne}>this one</Hand> : null}
                <AppText variant={on ? 'bodyStrong' : 'small'} color={on ? colors.text : colors.textSecondary}>({o.key.toLowerCase()}) {o.text}</AppText>
              </View>
            );
          })}
        </View>
      ) : (
        <AppText variant="h2" color={colors.primary}>{s.answer_text || r.answer}</AppText>
      )}
      {options.length && key && s.answer_text ? <AppText variant="small" color={colors.text}>{s.answer_text}</AppText> : null}
    </View>
  );
}

function AnswerView({ r, text, options }: { r: DoubtAnswer; text: string; options: AiOption[] }) {
  const [again, setAgain] = useState<DoubtSolution | null>(null);
  const [voted, setVoted] = useState<null | 'up' | 'down' | 'report'>(null);
  const [similar, setSimilar] = useState(false);
  const explain = useAiAction(aiService.explainAgain);
  const s = again ?? r.solution;
  const vote = async (body: { helpful?: boolean; report_error?: boolean }, v: 'up' | 'down' | 'report') => {
    if (!r.solution_id) return;
    try {
      await aiService.doubtFeedback(r.solution_id, body);
      setVoted(v);
      toast.success(body.report_error ? 'Thanks. Our team will check this answer.' : 'Thanks for the feedback.');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };
  return (
    <View style={{ gap: spacing.lg }}>
      <View style={[boardStyles.paperCard, { gap: spacing.xs }]}>
        <Label color={colors.secondary}>Question recognised</Label>
        <AppText variant="body">{text}</AppText>
        {r.source === 'exact' || r.source === 'meaning' ? <AppText variant="caption">Instant from the question library</AppText> : null}
        {r.premium_used ? <AppText variant="caption" color={colors.primary}>Solved with the premium model</AppText> : null}
      </View>
      {r.notice ? <Callout tone="warning" title="Please double-check">{r.notice}</Callout> : null}
      {r.personal_note ? <Callout tone="warning" title="About your choice">{r.personal_note}</Callout> : null}

      <Chalkboard>
        <MitraTag label={again ? 'Mitra · AI · explained differently' : 'Mitra · AI · step by step'} />
        <Steps s={s} />
        <FinalAnswer r={r} options={options} s={s} />
      </Chalkboard>

      {s.common_trap ? (
        <View style={[styles.side, { backgroundColor: board.stickyPink, borderColor: paper.pen }]}>
          <Hand bold color={paper.pen} size={22}>The trap</Hand>
          <AppText variant="small" color={colors.text}>{s.common_trap}</AppText>
        </View>
      ) : null}
      {s.shortcut ? (
        <View style={[styles.side, { backgroundColor: board.saffronSoft, borderColor: colors.primary }]}>
          <Label color={colors.primary}>Faster method · cheat code</Label>
          {s.method ? <AppText variant="bodyStrong">{s.method}</AppText> : null}
          <Hand color={paper.pen} size={17}>{s.shortcut}</Hand>
          <AppText variant="smallStrong" color={colors.primary} accessibilityRole="link" onPress={() => router.push('/ai/cheat-codes')}>Open in Cheat codes →</AppText>
        </View>
      ) : null}
      {s.memory_hook ? <Sticky title="Memory hook" tone="yellow" tilt={-0.6}>{s.memory_hook}</Sticky> : null}
      {s.real_life_example ? <Sticky title="Real-life example" tone="green" titleColor={colors.secondary} tilt={0.6}>{s.real_life_example}</Sticky> : null}

      <View style={[boardStyles.paperCard, { gap: spacing.sm }]}>
        <View style={styles.rowBetween}>
          <AppText variant="h3">Was this clear?</AppText>
          {r.solution_id ? (
            <View style={styles.row}>
              <Pressable onPress={() => vote({ helpful: true }, 'up')} disabled={!!voted} accessibilityRole="button" accessibilityLabel="Yes, clear" accessibilityState={{ selected: voted === 'up' }}
                style={[styles.thumb, voted === 'up' && styles.thumbOn]}><Ionicons name={voted === 'up' ? 'thumbs-up' : 'thumbs-up-outline'} size={20} color={colors.text} /></Pressable>
              <Pressable onPress={() => vote({ helpful: false }, 'down')} disabled={!!voted} accessibilityRole="button" accessibilityLabel="Not clear" accessibilityState={{ selected: voted === 'down' }}
                style={[styles.thumb, voted === 'down' && styles.thumbOn]}><Ionicons name={voted === 'down' ? 'thumbs-down' : 'thumbs-down-outline'} size={20} color={colors.text} /></Pressable>
            </View>
          ) : null}
        </View>
        {r.solution_id ? (
          <Button title="Explain differently" variant="outline" leftIcon="refresh" loading={explain.busy}
            onPress={async () => { const x = await explain.run(r.solution_id!); if (x) setAgain(x.solution); }} />
        ) : null}
        {s.practice_question ? <Button title={similar ? 'Hide similar question' : 'Similar question'} variant="outline" leftIcon="copy-outline" onPress={() => setSimilar((v) => !v)} /> : null}
        {similar && s.practice_question ? <PracticeQuestions questions={[s.practice_question]} /> : null}
        <Button title="Deep dive on this" variant="soft" leftIcon="school-outline"
          onPress={() => router.push({ pathname: '/ai/tutor', params: r.solution_id ? { tab: 'deep', solution: r.solution_id } : { tab: 'deep', text: text.slice(0, 1500) } })} />
        <AiErrorNotice error={explain.error} />
        {r.solution_id && voted !== 'report' ? (
          <Button title="Report an error" size="sm" variant="ghost" leftIcon="flag-outline" onPress={() => vote({ report_error: true }, 'report')} />
        ) : null}
        <AppText variant="caption">AI-generated explanation. The final answer is re-checked by code; ask your teacher if a step still feels off.</AppText>
      </View>
    </View>
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
  const [askedOptions, setAskedOptions] = useState<AiOption[]>([]);
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
      if (r) { setResult(r); setAsked(text.trim()); setAskedOptions(opts); }
    } else if (image) {
      const r = await photo.run({ image, chosen });
      if (r) { setResult(r); setAsked(r.read_question?.text ?? ''); setAskedOptions(r.read_question?.options ?? []); }
    }
  };

  const answered = result && !isSupportReply(result) ? result : null;
  const stage: 0 | 1 | 2 = answered ? 2 : action.busy ? 1 : 0;

  return (
    <Screen keyboard>
      <View style={{ gap: spacing.lg }}>
        <View style={{ gap: spacing.sm }}>
          <SectionHead kicker="stuck on one question? —" title="Doubt solver" />
          <Progress stage={stage} />
          <View style={boardStyles.wrap}><AllowanceBadge feature="doubts" label="Doubts" /><AllowanceBadge feature="photo_doubts" label="Photo" /></View>
        </View>
        {isSupportReply(result) ? <SupportBanner message={result.support} /> : null}

        <View style={[boardStyles.paperCard, { gap: spacing.sm }]}>
          <View style={styles.rowBetween}>
            <AppText variant="h3">{answered ? 'New doubt' : 'Ask Mitra'}</AppText>
            {answered ? <Button title="Clear" size="sm" variant="ghost" leftIcon="add" onPress={() => { setResult(null); setText(''); setOptions(['', '', '', '']); setImage(null); setChosen(null); }} /> : null}
          </View>
          <SegmentedControl value={tab} onChange={(v) => { setTab(v); setResult(null); }} accessibilityLabel="How to ask"
            segments={[{ value: 'text', label: 'Type it' }, { value: 'photo', label: 'Photo' }]} />
          {tab === 'text' ? (
            <View style={{ gap: spacing.sm }}>
              <Input label="Question" multiline value={text} onChangeText={setText} maxLength={4000}
                placeholder="e.g. A train 240 m long passes a pole in 16 seconds…" />
              {options.map((o, i) => (
                <Input key={i} label={`Option ${KEYS[i]} (optional)`} value={o} maxLength={500} onChangeText={(v) => setOptions((s) => s.map((x, j) => (j === i ? v : x)))} />
              ))}
              <SwitchRow label="Use the premium model" description="For a tricky question. Uses a premium doubt (Pro) when you have one." value={escalate} onValueChange={setEscalate} />
            </View>
          ) : (
            <View style={{ gap: spacing.sm }}>
              {image ? <Image source={{ uri: image }} style={styles.photo} resizeMode="contain" accessibilityLabel="Your question photo" /> : null}
              <Button title={image ? 'Choose another photo' : 'Choose a photo of the question'} variant={image ? 'outline' : 'soft'} leftIcon="camera-outline" onPress={pick} />
              <Sticky title="Photo tip" titleColor={colors.warningText} tilt={-0.8}>
                Crop to one question, options included. Mitra reads printed and neat handwritten text. Photo doubts come with the AI Tutor packs.
              </Sticky>
            </View>
          )}
          <AppText variant="label" style={styles.gap}>Your answer (optional)</AppText>
          <View style={boardStyles.wrap}>
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
        </View>

        {answered ? <AnswerView r={answered} text={asked} options={askedOptions} /> : (
          <AiNote>AI-generated explanation. The final answer is re-checked by code; ask your teacher if a step still feels off.</AiNote>
        )}
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  gap: { marginTop: spacing.sm },
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs },
  rowBetween: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, flexWrap: 'wrap' },
  progress: { flexDirection: 'row', gap: spacing.xs },
  stage: { flex: 1, flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 8, paddingVertical: 6, borderRadius: radii.full, backgroundColor: colors.secondarySoft },
  stageOn: { backgroundColor: paper.ink },
  stageDone: { backgroundColor: colors.secondarySoft },
  stageNum: { width: 22, height: 22, borderRadius: 11, borderWidth: 1.5, borderColor: colors.secondary, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center' },
  step: { flexDirection: 'row', gap: spacing.sm, alignItems: 'flex-start' },
  stepNum: { width: 30, height: 30, borderRadius: 15, borderWidth: 1.5, borderColor: paper.marigold, alignItems: 'center', justifyContent: 'center' },
  final: { backgroundColor: colors.card, borderRadius: radii.md, padding: spacing.md, gap: spacing.sm, marginTop: spacing.sm },
  finalOpts: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  finalOpt: { flexBasis: '46%', flexGrow: 1, alignItems: 'center', paddingVertical: 10, paddingHorizontal: 8, borderRadius: radii.full },
  finalOptOn: { borderWidth: 2.5, borderColor: paper.pen, transform: [{ rotate: '-2deg' }] },
  thisOne: { position: 'absolute', top: -14, left: 14 },
  side: { borderWidth: 2, borderRadius: radii.lg, padding: spacing.lg, gap: spacing.xs },
  thumb: { width: 44, height: 44, borderRadius: radii.md, borderWidth: 1.5, borderColor: paper.ink, alignItems: 'center', justifyContent: 'center' },
  thumbOn: { backgroundColor: paper.stickyYellow },
  photo: { width: '100%', height: 220, borderRadius: radii.md, backgroundColor: colors.background },
  key: { width: 44, height: 44, borderRadius: 22, borderWidth: 1, borderColor: colors.borderStrong, alignItems: 'center', justifyContent: 'center' },
  keyOn: { backgroundColor: colors.primary, borderColor: colors.primary },
});
