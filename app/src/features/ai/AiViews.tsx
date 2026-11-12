import { useState, type ReactNode } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import type {
  AiArtifact, CheatCardPayload, CurrentAffairsPayload, DeckPayload, DeepDivePayload, MistakeSummaryFacts, NotesPayload, PracticeQuestion,
  WritingPayload,
} from '@prepmitra/shared';
import { AppText, Badge, Button, Card } from '@/components';
import { colors, paper, radii, spacing, toneColors } from '@/theme';
import { MermaidView, TableView, VisualView } from './AiUi';

export function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <View style={styles.section}>
      <AppText variant="caption" weight="700" style={styles.sectionTitle}>{title.toUpperCase()}</AppText>
      {children}
    </View>
  );
}

export function Bullets({ items, ordered }: { items?: string[]; ordered?: boolean }) {
  if (!items?.length) return null;
  return (
    <View style={{ gap: 6 }}>
      {items.map((s, i) => (
        <View key={i} style={styles.bullet}>
          <AppText variant="small" color={colors.text} style={styles.bulletMark}>{ordered ? `${i + 1}.` : '•'}</AppText>
          <AppText variant="small" color={colors.text} style={styles.flex}>{s}</AppText>
        </View>
      ))}
    </View>
  );
}

export function Callout({ tone = 'info', title, children }: { tone?: 'info' | 'warning' | 'success'; title: string; children: ReactNode }) {
  const t = toneColors[tone];
  return (
    <View style={[styles.callout, { backgroundColor: t.bg, borderColor: t.border }]}>
      <AppText variant="smallStrong">{title}</AppText>
      <AppText variant="small" color={colors.text}>{children}</AppText>
    </View>
  );
}

export function PracticeQuestions({ questions }: { questions?: PracticeQuestion[] }) {
  const [picked, setPicked] = useState<Record<number, string>>({});
  if (!questions?.length) return null;
  return (
    <View style={{ gap: spacing.md }}>
      {questions.map((q, i) => {
        const p = picked[i];
        return (
          <Card key={i}>
            <AppText variant="bodyStrong">{i + 1}. {q.text}</AppText>
            {q.level ? <Badge label={q.level.replace('_', ' ')} style={styles.gapTop} /> : null}
            <View style={[styles.gapTop, { gap: spacing.xs }]}>
              {q.options.map((o) => {
                const right = !!p && o.key === q.answer;
                const wrong = p === o.key && o.key !== q.answer;
                return (
                  <Pressable key={o.key} disabled={!!p} onPress={() => setPicked((s) => ({ ...s, [i]: o.key }))} accessibilityRole="button"
                    accessibilityLabel={`Option ${o.key}: ${o.text}`}
                    style={[styles.option, right && styles.optRight, wrong && styles.optWrong]}>
                    <AppText variant="smallStrong">{o.key}.</AppText>
                    <AppText variant="small" color={colors.text} style={styles.flex}>{o.text}</AppText>
                    {right && <Ionicons name="checkmark-circle" size={18} color={colors.success} />}
                    {wrong && <Ionicons name="close-circle" size={18} color={colors.error} />}
                  </Pressable>
                );
              })}
            </View>
            {p ? <AppText variant="small" style={styles.gapTop}>Answer {q.answer}. {q.explanation}</AppText> : null}
          </Card>
        );
      })}
    </View>
  );
}

export function ArtifactHeader({ a, extra }: { a: AiArtifact; extra?: ReactNode }) {
  return (
    <View style={{ gap: spacing.xs }}>
      <AppText variant="h2">{a.title}</AppText>
      <View style={styles.row}>
        {a.from_cache ? <Badge label="From the shared library" tone="success" /> : null}
        {a.shared ? <Badge label="Shared" /> : null}
        {extra}
      </View>
    </View>
  );
}

export function DeepDiveView({ p, note }: { p: DeepDivePayload; note?: string }) {
  return (
    <View>
      {note ? <View style={styles.gapTop}><Callout tone="warning" title="About your answer">{note}</Callout></View> : null}
      <Section title="One-page visual"><VisualView visual={p.visual_note} /></Section>
      <Section title="The concept from zero"><Bullets items={p.concept_from_zero} ordered /></Section>
      <View style={[styles.gapTop, { gap: spacing.sm }]}>
        <Callout tone="warning" title="The trap">{p.the_trap}</Callout>
        <Callout title="Why students get it wrong">{p.why_students_get_it_wrong}</Callout>
      </View>
      <Section title="Worked solution"><Bullets items={p.worked_solution} ordered /></Section>
      {p.shortcut ? <View style={styles.gapTop}><Callout tone="success" title="Shortcut">{p.shortcut}</Callout></View> : null}
      <Section title="Never-again checklist"><Bullets items={p.never_again_checklist} /></Section>
      <Section title="Practice (easy → exam hard)"><PracticeQuestions questions={p.practice_questions} /></Section>
    </View>
  );
}

export function NotesView({ p }: { p: NotesPayload }) {
  return (
    <View>
      {p.summary ? <AppText variant="body" style={styles.gapTop}>{p.summary}</AppText> : null}
      {p.sections?.map((s, i) => (
        <Section key={i} title={s.heading}><Bullets items={s.bullets} /><VisualView visual={s.visual} /></Section>
      ))}
      {p.formulas?.length ? (
        <Section title="Formulas"><TableView rows={[['Formula', '', 'When to use'], ...p.formulas.map((f) => [f.name, f.formula, f.when_to_use])]} /></Section>
      ) : null}
      {p.mind_map_mermaid?.trim() ? <Section title="Mind map"><MermaidView source={p.mind_map_mermaid} /></Section> : null}
      <Section title="One-page revision"><Bullets items={p.one_page_revision} /></Section>
    </View>
  );
}

export function DeckView({ p, note }: { p: DeckPayload; note?: string }) {
  const [i, setI] = useState(0);
  const slide = p.slides?.[i];
  return (
    <View>
      {note ? <View style={styles.gapTop}><Callout title="For you">{note}</Callout></View> : null}
      {p.why_it_matters ? <AppText variant="small" style={styles.gapTop}>{p.why_it_matters}</AppText> : null}
      {slide ? (
        <Card style={styles.gapTop}>
          <AppText variant="caption">Slide {i + 1} of {p.slides.length}</AppText>
          <AppText variant="h3">{slide.title}</AppText>
          <View style={styles.gapTop}><Bullets items={slide.points} /></View>
          <VisualView visual={slide.visual} />
          <View style={[styles.row, styles.gapTop, { justifyContent: 'space-between' }]}>
            <Button title="Previous" size="sm" variant="outline" disabled={i === 0} onPress={() => setI(i - 1)} />
            <Button title="Next" size="sm" disabled={i >= p.slides.length - 1} onPress={() => setI(i + 1)} />
          </View>
        </Card>
      ) : null}
      {p.worked_examples?.length ? (
        <Section title="Worked examples">
          {p.worked_examples.map((w, k) => (
            <View key={k} style={styles.box}>
              <AppText variant="smallStrong">{w.question}</AppText>
              <AppText variant="small" color={colors.success}>{w.fastest_method}</AppText>
              <Bullets items={w.steps} ordered />
            </View>
          ))}
        </Section>
      ) : null}
      {p.traps?.length ? <Section title="Traps"><TableView rows={[['Wrong', 'Right', 'Why'], ...p.traps.map((t) => [t.wrong, t.right, t.why])]} /></Section> : null}
      {p.cheat_codes?.length ? (
        <Section title="Cheat codes"><TableView rows={[['Code', 'Works when', 'Fails when'], ...p.cheat_codes.map((c) => [c.code, c.works_when, c.fails_when])]} /></Section>
      ) : null}
      <Section title="Summary sheet"><Bullets items={p.summary_sheet} /></Section>
      <Section title="Practice"><PracticeQuestions questions={p.practice_questions} /></Section>
    </View>
  );
}

export function CheatCardView({ p }: { p: Omit<CheatCardPayload, 'topic_id'> }) {
  return (
    <View style={styles.cheat}>
      <View style={[styles.row, { justifyContent: 'space-between' }]}>
        <AppText variant="bodyStrong" style={styles.flex}>{p.name}</AppText>
        {p.pass_rate > 0 ? <Badge label={`${Math.round(p.pass_rate * 100)}% pass`} tone="success" /> : null}
      </View>
      <AppText variant="caption">{p.topic}</AppText>
      <AppText variant="smallStrong" style={styles.gapTop}>{p.rule}</AppText>
      {p.mnemonic ? <AppText variant="small" style={{ fontStyle: 'italic' }}>“{p.mnemonic}”</AppText> : null}
      {p.example ? <AppText variant="small">e.g. {p.example}</AppText> : null}
      <AppText variant="caption" style={styles.gapTop}>✓ {p.works_when}</AppText>
      <AppText variant="caption">⚠ {p.fails_when}</AppText>
    </View>
  );
}

export function MistakeSummaryView({ s }: { s: MistakeSummaryFacts }) {
  const max = Math.max(1, ...s.groups.map((g) => g.count));
  return (
    <View>
      <AppText variant="body">{s.ai.summary}</AppText>
      {s.groups.map((g) => (
        <View key={g.type} style={styles.gapTop}>
          <View style={[styles.row, { justifyContent: 'space-between' }]}>
            <AppText variant="smallStrong">{g.type.replace('_', ' ')}</AppText>
            <AppText variant="small">{g.count}</AppText>
          </View>
          <View style={styles.barTrack}><View style={[styles.bar, { width: `${(g.count / max) * 100}%` }]} /></View>
          <AppText variant="caption">{Object.entries(g.topics).map(([t, n]) => `${t} (${n})`).join(' · ')}</AppText>
        </View>
      ))}
      {s.ai.patterns.length ? <Section title="Patterns"><Bullets items={s.ai.patterns.map((p) => `${p.type}: ${p.advice}`)} /></Section> : null}
      {s.ai.this_week.length ? <Section title="This week"><Bullets items={s.ai.this_week} /></Section> : null}
    </View>
  );
}

export function WritingView({ p }: { p: WritingPayload }) {
  const e = p.evaluation;
  return (
    <View>
      <AppText variant="display" color={colors.primary}>{p.total_score}<AppText variant="h3" color={colors.textSecondary}>/{p.out_of}</AppText></AppText>
      <AppText variant="small">{p.word_count} words{p.word_limit ? ` · limit ${p.word_limit}` : ''}{p.over_limit ? ' · over the limit (−10)' : ''}</AppText>
      <AppText variant="body" style={styles.gapTop}>{e.overall_feedback}</AppText>
      <Section title="Scores"><TableView rows={[['Criterion', 'Score', 'Comment'], ...e.scores.map((s) => [s.criterion, `${s.score}/10`, s.comment])]} /></Section>
      {e.corrections.length ? <Section title="Corrections"><TableView rows={[['You wrote', 'Better', 'Why'], ...e.corrections.map((c) => [c.original, c.corrected, c.why])]} /></Section> : null}
      <Section title="Strengths"><Bullets items={e.strengths} /></Section>
      <Section title="Improve"><Bullets items={e.improvements} /></Section>
      <Section title="Model answer"><View style={styles.paper}><AppText variant="small" color={colors.text}>{e.model_answer}</AppText></View></Section>
      {p.topper_rewrite ? (
        <Section title="Topper rewrite">
          <View style={[styles.paper, { backgroundColor: paper.stickyGreen }]}><AppText variant="small" color={colors.text}>{p.topper_rewrite.topper_version}</AppText></View>
          <Bullets items={p.topper_rewrite.what_changed} />
        </Section>
      ) : null}
    </View>
  );
}

export function CurrentAffairsView({ p }: { p: CurrentAffairsPayload }) {
  return (
    <View>
      {p.items.map((it, i) => (
        <Card key={i} style={styles.gapTop}>
          <Badge label={it.category} tone="secondary" />
          <AppText variant="bodyStrong" style={styles.gapTop}>{it.headline}</AppText>
          <AppText variant="small" color={colors.text}>{it.summary}</AppText>
          <AppText variant="small" style={styles.gapTop}>Exam angle: {it.exam_angle}</AppText>
        </Card>
      ))}
      <Section title={`Quiz (${p.quiz.length} fact-checked)`}><PracticeQuestions questions={p.quiz} /></Section>
    </View>
  );
}

export function ArtifactBody({ a }: { a: AiArtifact & { personal_note?: string } }) {
  if (a.kind.startsWith('deep_dive')) return <DeepDiveView p={a.payload as DeepDivePayload} note={a.personal_note} />;
  if (a.kind === 'notes' || a.kind === 'master_notes') return <NotesView p={a.payload as NotesPayload} />;
  if (a.kind.startsWith('topic_deck')) return <DeckView p={a.payload as DeckPayload} note={a.personal_note} />;
  if (a.kind === 'cheat_card') return <CheatCardView p={a.payload as CheatCardPayload} />;
  if (a.kind === 'writing_eval') return <WritingView p={a.payload as WritingPayload} />;
  if (a.kind === 'current_affairs') return <CurrentAffairsView p={a.payload as CurrentAffairsPayload} />;
  if (a.kind === 'mistake_summary') return <MistakeSummaryView s={a.payload as MistakeSummaryFacts} />;
  return <AppText variant="caption">{JSON.stringify(a.payload, null, 2)}</AppText>;
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  row: { flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', gap: spacing.xs },
  gapTop: { marginTop: spacing.sm },
  section: { marginTop: spacing.lg, gap: spacing.xs },
  sectionTitle: { letterSpacing: 0.6 },
  bullet: { flexDirection: 'row', gap: 6 },
  bulletMark: { minWidth: 16 },
  callout: { borderWidth: 1, borderRadius: radii.md, padding: spacing.md, gap: 2 },
  option: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, borderWidth: 1, borderColor: colors.border, borderRadius: radii.md, padding: spacing.sm, minHeight: 44 },
  optRight: { borderColor: '#86EFAC', backgroundColor: colors.successSoft },
  optWrong: { borderColor: '#FCA5A5', backgroundColor: colors.errorSoft },
  box: { borderWidth: 1, borderColor: colors.border, borderRadius: radii.md, padding: spacing.sm, gap: 4, marginTop: spacing.xs },
  cheat: { borderWidth: 2, borderStyle: 'dashed', borderColor: '#F6C9A6', backgroundColor: paper.stickyYellow, borderRadius: radii.lg, padding: spacing.md, gap: 2 },
  barTrack: { height: 8, borderRadius: 4, backgroundColor: colors.background, marginVertical: 4 },
  bar: { height: 8, borderRadius: 4, backgroundColor: colors.primary },
  paper: { backgroundColor: paper.paper, borderRadius: radii.md, padding: spacing.md },
});
