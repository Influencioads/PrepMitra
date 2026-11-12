import { useState, type ReactNode } from 'react';
import toast from 'react-hot-toast';
import { CheckCircle2, Download, Lightbulb, TriangleAlert, XCircle } from 'lucide-react';
import type {
  AiArtifact, CheatCardPayload, CurrentAffairsPayload, DeckPayload, DeepDivePayload, MistakeSummaryFacts, NotesPayload, PracticeQuestion,
  WritingPayload,
} from '@prepmitra/shared';
import { Badge, Button, Card, CardBody } from '@/components/ui';
import { errorMessage } from '@/services';
import { openArtifactPdf } from '@/services/aiService';
import { cn } from '@/utils/cn';
import { AiTable, AiVisualView, MermaidDiagram } from './AiVisual';

export function Section({ title, children, className }: { title: ReactNode; children: ReactNode; className?: string }) {
  return (
    <section className={cn('mt-5', className)}>
      <h3 className="mb-2 text-sm font-semibold uppercase tracking-wide text-muted">{title}</h3>
      {children}
    </section>
  );
}

export function Bullets({ items, ordered }: { items?: string[]; ordered?: boolean }) {
  if (!items?.length) return null;
  const Tag = ordered ? 'ol' : 'ul';
  return <Tag className={cn('space-y-1.5 pl-5 text-sm leading-relaxed', ordered ? 'list-decimal' : 'list-disc')}>{items.map((s, i) => <li key={i}>{s}</li>)}</Tag>;
}

export function Callout({ tone = 'info', title, children }: { tone?: 'info' | 'warning' | 'success'; title: string; children: ReactNode }) {
  const cls = { info: 'border-secondary/25 bg-info-soft', warning: 'border-amber-200 bg-warning-soft', success: 'border-green-200 bg-success-soft' }[tone];
  return (
    <div className={cn('rounded-lg border px-4 py-3 text-sm', cls)}>
      <p className="font-semibold">{title}</p>
      <div className="mt-0.5 leading-relaxed">{children}</div>
    </div>
  );
}

/** Practice questions with tap-to-answer and the explanation revealed after an answer. */
export function PracticeQuestions({ questions }: { questions?: PracticeQuestion[] }) {
  const [picked, setPicked] = useState<Record<number, string>>({});
  if (!questions?.length) return null;
  return (
    <ol className="space-y-4">
      {questions.map((q, i) => {
        const p = picked[i];
        return (
          <li key={i} className="rounded-lg border border-line bg-card p-4">
            <div className="flex items-start justify-between gap-2">
              <p className="text-sm font-medium">{i + 1}. {q.text}</p>
              {q.level && <Badge tone="neutral">{q.level.replace('_', ' ')}</Badge>}
            </div>
            <div className="mt-3 grid gap-2 sm:grid-cols-2">
              {q.options.map((o) => {
                const right = p && o.key === q.answer;
                const wrong = p === o.key && o.key !== q.answer;
                return (
                  <button key={o.key} type="button" disabled={!!p} onClick={() => setPicked((s) => ({ ...s, [i]: o.key }))}
                    className={cn('flex items-center gap-2 rounded-lg border px-3 py-2 text-left text-sm transition-colors', right ? 'border-green-300 bg-success-soft' : wrong ? 'border-red-300 bg-danger-soft' : 'border-line hover:border-primary disabled:hover:border-line')}>
                    <span className="font-semibold">{o.key}.</span><span className="flex-1">{o.text}</span>
                    {right && <CheckCircle2 className="h-4 w-4 text-success" aria-label="Correct" />}
                    {wrong && <XCircle className="h-4 w-4 text-danger" aria-label="Wrong" />}
                  </button>
                );
              })}
            </div>
            {p && <p className="mt-3 text-sm text-muted"><span className="font-semibold text-ink">Answer {q.answer}.</span> {q.explanation}</p>}
          </li>
        );
      })}
    </ol>
  );
}

export function PdfButton({ id, label = 'PDF' }: { id: string; label?: string }) {
  const [busy, setBusy] = useState(false);
  return (
    <Button size="sm" variant="outline" loading={busy} leftIcon={<Download className="h-4 w-4" />}
      onClick={async () => {
        setBusy(true);
        try { await openArtifactPdf(id); } catch (e) { toast.error(errorMessage(e)); } finally { setBusy(false); }
      }}>
      {label}
    </Button>
  );
}

export function ArtifactHeader({ a, extra }: { a: AiArtifact; extra?: ReactNode }) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-2">
      <div className="min-w-0">
        <h2 className="text-xl font-bold">{a.title}</h2>
        <div className="mt-1 flex flex-wrap gap-1.5">
          {a.from_cache && <Badge tone="success">From the shared library · no AI wait</Badge>}
          {a.shared && <Badge tone="neutral">Shared</Badge>}
          {a.language !== 'en' && <Badge tone="neutral">{a.language.toUpperCase()}</Badge>}
        </div>
      </div>
      <div className="flex gap-2">{extra}<PdfButton id={a.id} /></div>
    </div>
  );
}

export function DeepDiveView({ p, note }: { p: DeepDivePayload; note?: string }) {
  return (
    <div>
      {note && <Callout tone="warning" title="About your answer">{note}</Callout>}
      <Section title="One-page visual"><AiVisualView visual={p.visual_note} />{p.visual_note?.caption && <p className="mt-1 text-xs text-muted">{p.visual_note.caption}</p>}</Section>
      <Section title="The concept from zero"><Bullets items={p.concept_from_zero} ordered /></Section>
      <div className="mt-5 grid gap-3 md:grid-cols-2">
        <Callout tone="warning" title="The trap">{p.the_trap}</Callout>
        <Callout title="Why students get it wrong">{p.why_students_get_it_wrong}</Callout>
      </div>
      <Section title="Worked solution"><Bullets items={p.worked_solution} ordered /></Section>
      {p.shortcut && <div className="mt-4"><Callout tone="success" title="Shortcut">{p.shortcut}</Callout></div>}
      <Section title="Never-again checklist"><Bullets items={p.never_again_checklist} /></Section>
      <Section title="Practice (easy → exam hard)"><PracticeQuestions questions={p.practice_questions} /></Section>
    </div>
  );
}

export function NotesView({ p }: { p: NotesPayload }) {
  return (
    <div>
      {p.summary && <p className="mt-3 text-sm leading-relaxed">{p.summary}</p>}
      {p.sections?.map((s, i) => (
        <Section key={i} title={s.heading}>
          <Bullets items={s.bullets} />
          <AiVisualView visual={s.visual} className="mt-3" />
        </Section>
      ))}
      {p.formulas?.length > 0 && (
        <Section title="Formulas">
          <AiTable rows={[['Formula', '', 'When to use'], ...p.formulas.map((f) => [f.name, f.formula, f.when_to_use])]} />
        </Section>
      )}
      {p.mind_map_mermaid?.trim() && <Section title="Mind map"><MermaidDiagram source={p.mind_map_mermaid} /></Section>}
      {p.one_page_revision?.length > 0 && <Section title="One-page revision"><Bullets items={p.one_page_revision} /></Section>}
    </div>
  );
}

export function DeckView({ p, note }: { p: DeckPayload; note?: string }) {
  const [i, setI] = useState(0);
  const slide = p.slides?.[i];
  return (
    <div>
      {note && <div className="mt-3"><Callout title="For you">{note}</Callout></div>}
      {p.why_it_matters && <p className="mt-3 text-sm text-muted">{p.why_it_matters}</p>}
      {slide && (
        <Card className="mt-4">
          <CardBody>
            <p className="text-xs font-semibold text-muted">Slide {i + 1} of {p.slides.length}</p>
            <h3 className="mt-1 text-lg font-bold">{slide.title}</h3>
            <div className="mt-2"><Bullets items={slide.points} /></div>
            <AiVisualView visual={slide.visual} className="mt-3" />
            <div className="mt-4 flex justify-between">
              <Button size="sm" variant="outline" disabled={i === 0} onClick={() => setI(i - 1)}>Previous</Button>
              <Button size="sm" disabled={i >= p.slides.length - 1} onClick={() => setI(i + 1)}>Next</Button>
            </div>
          </CardBody>
        </Card>
      )}
      {p.worked_examples?.length > 0 && (
        <Section title="Worked examples">
          <div className="space-y-3">
            {p.worked_examples.map((w, k) => (
              <div key={k} className="rounded-lg border border-line p-3 text-sm">
                <p className="font-medium">{w.question} <Badge tone="neutral">{w.level}</Badge></p>
                <p className="mt-1 text-success"><Lightbulb className="mr-1 inline h-4 w-4" aria-hidden />{w.fastest_method}</p>
                <Bullets items={w.steps} ordered />
              </div>
            ))}
          </div>
        </Section>
      )}
      {p.traps?.length > 0 && (
        <Section title="Traps"><AiTable rows={[['Wrong', 'Right', 'Why'], ...p.traps.map((t) => [t.wrong, t.right, t.why])]} /></Section>
      )}
      {p.cheat_codes?.length > 0 && (
        <Section title="Cheat codes"><AiTable rows={[['Code', 'Works when', 'Fails when'], ...p.cheat_codes.map((c) => [c.code, c.works_when, c.fails_when])]} /></Section>
      )}
      <Section title="Summary sheet"><Bullets items={p.summary_sheet} /></Section>
      <Section title="Practice"><PracticeQuestions questions={p.practice_questions} /></Section>
    </div>
  );
}

export function CheatCardView({ p, className }: { p: Omit<CheatCardPayload, 'topic_id'>; className?: string }) {
  return (
    <div className={cn('rounded-xl border-2 border-dashed border-primary/40 bg-sticky-yellow p-4 text-sm', className)}>
      <div className="flex items-start justify-between gap-2">
        <p className="font-bold">{p.name}</p>
        {p.pass_rate > 0 && <Badge tone="success">{Math.round(p.pass_rate * 100)}% pass</Badge>}
      </div>
      <p className="mt-1 text-xs text-muted">{p.topic}</p>
      <p className="mt-2 font-medium">{p.rule}</p>
      {p.mnemonic && <p className="mt-1 italic">“{p.mnemonic}”</p>}
      {p.example && <p className="mt-2 text-muted">e.g. {p.example}</p>}
      <div className="mt-2 grid gap-1 text-xs sm:grid-cols-2">
        <p><CheckCircle2 className="mr-1 inline h-3.5 w-3.5 text-success" aria-hidden />{p.works_when}</p>
        <p><TriangleAlert className="mr-1 inline h-3.5 w-3.5 text-warning" aria-hidden />{p.fails_when}</p>
      </div>
    </div>
  );
}

export function MistakeSummaryView({ s }: { s: MistakeSummaryFacts }) {
  const max = Math.max(1, ...s.groups.map((g) => g.count));
  return (
    <div>
      <p className="text-sm leading-relaxed">{s.ai.summary}</p>
      {s.groups.length > 0 && (
        <ul className="mt-4 space-y-2">
          {s.groups.map((g) => (
            <li key={g.type} className="text-sm">
              <div className="flex justify-between"><span className="font-medium capitalize">{g.type.replace('_', ' ')}</span><span>{g.count}</span></div>
              <div className="mt-1 h-2 rounded-full bg-surface"><div className="h-2 rounded-full bg-primary" style={{ width: `${(g.count / max) * 100}%` }} /></div>
              <p className="mt-0.5 text-xs text-muted">{Object.entries(g.topics).map(([t, n]) => `${t} (${n})`).join(' · ')}</p>
            </li>
          ))}
        </ul>
      )}
      {s.ai.patterns.length > 0 && <Section title="Patterns"><Bullets items={s.ai.patterns.map((p) => `${p.type}: ${p.advice}`)} /></Section>}
      {s.ai.this_week.length > 0 && <Section title="This week"><Bullets items={s.ai.this_week} /></Section>}
    </div>
  );
}

export function WritingView({ p }: { p: WritingPayload }) {
  const e = p.evaluation;
  return (
    <div>
      <div className="flex flex-wrap items-end gap-4">
        <p className="text-4xl font-bold text-primary">{p.total_score}<span className="text-lg text-muted">/{p.out_of}</span></p>
        <p className="text-sm text-muted">{p.word_count} words{p.word_limit ? ` · limit ${p.word_limit}` : ''}{p.over_limit && <span className="ml-1 font-semibold text-danger">· over the limit (−10)</span>}</p>
      </div>
      <p className="mt-3 text-sm leading-relaxed">{e.overall_feedback}</p>
      <Section title="Scores">
        <AiTable rows={[['Criterion', 'Score', 'Comment'], ...e.scores.map((s) => [s.criterion, `${s.score}/10`, s.comment])]} />
      </Section>
      {e.corrections.length > 0 && (
        <Section title="Corrections"><AiTable rows={[['You wrote', 'Better', 'Why'], ...e.corrections.map((c) => [c.original, c.corrected, c.why])]} /></Section>
      )}
      <div className="mt-5 grid gap-4 md:grid-cols-2">
        <div><h3 className="mb-2 text-sm font-semibold">Strengths</h3><Bullets items={e.strengths} /></div>
        <div><h3 className="mb-2 text-sm font-semibold">Improve</h3><Bullets items={e.improvements} /></div>
      </div>
      <Section title="Model answer"><p className="whitespace-pre-line rounded-lg bg-paper p-4 text-sm leading-relaxed">{e.model_answer}</p></Section>
      {p.topper_rewrite && (
        <Section title="Topper rewrite">
          <p className="whitespace-pre-line rounded-lg bg-sticky-green p-4 text-sm leading-relaxed">{p.topper_rewrite.topper_version}</p>
          <div className="mt-2"><Bullets items={p.topper_rewrite.what_changed} /></div>
        </Section>
      )}
    </div>
  );
}

export function CurrentAffairsView({ p }: { p: CurrentAffairsPayload }) {
  return (
    <div>
      <ul className="space-y-3">
        {p.items.map((it, i) => (
          <li key={i} className="rounded-lg border border-line bg-card p-4 text-sm">
            <div className="flex flex-wrap items-center gap-2"><Badge tone="secondary">{it.category}</Badge><p className="font-semibold">{it.headline}</p></div>
            <p className="mt-1.5 leading-relaxed">{it.summary}</p>
            <p className="mt-1.5 text-muted"><span className="font-semibold text-ink">Exam angle:</span> {it.exam_angle}</p>
          </li>
        ))}
      </ul>
      <Section title={`Quiz (${p.quiz.length} fact-checked questions)`}><PracticeQuestions questions={p.quiz} /></Section>
      {p.dropped_after_fact_check > 0 && <p className="mt-2 text-xs text-muted">{p.dropped_after_fact_check} question(s) dropped after fact-checking.</p>}
    </div>
  );
}

/** Any stored artifact by kind (GET /ai/artifacts/{id}). */
export function ArtifactBody({ a }: { a: AiArtifact & { personal_note?: string } }) {
  if (a.kind.startsWith('deep_dive')) return <DeepDiveView p={a.payload as DeepDivePayload} note={a.personal_note} />;
  if (a.kind === 'notes' || a.kind === 'master_notes') return <NotesView p={a.payload as NotesPayload} />;
  if (a.kind.startsWith('topic_deck')) return <DeckView p={a.payload as DeckPayload} note={a.personal_note} />;
  if (a.kind === 'cheat_card') return <CheatCardView p={a.payload as CheatCardPayload} className="mt-4" />;
  if (a.kind === 'writing_eval') return <WritingView p={a.payload as WritingPayload} />;
  if (a.kind === 'current_affairs') return <CurrentAffairsView p={a.payload as CurrentAffairsPayload} />;
  if (a.kind === 'mistake_summary') return <MistakeSummaryView s={a.payload as MistakeSummaryFacts} />;
  return <pre className="mt-4 overflow-x-auto rounded-lg bg-surface p-3 text-xs">{JSON.stringify(a.payload, null, 2)}</pre>;
}
