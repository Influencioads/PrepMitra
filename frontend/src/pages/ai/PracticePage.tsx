import { useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { CheckCircle2, Lightbulb, XCircle } from 'lucide-react';
import type { CurrentAffairs, RevisionSubmitResult, RevisionToday, WritingEvaluation, WritingTaskType } from '@prepmitra/shared';
import { Badge, Button, Card, CardBody, CardHeader, Input, LoadingSkeleton, PageHeader, Select, Switch, Tabs, Textarea } from '@/components/ui';
import { AiErrorNotice, AllowanceChip, useAiAction } from '@/components/ai/AiUi';
import { ArtifactHeader, CheatCardView, CurrentAffairsView, WritingView } from '@/components/ai/AiViews';
import { aiService } from '@/services/aiService';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

type Tab = 'revision' | 'current' | 'writing';

function RevisionPanel() {
  const [count, setCount] = useState(10);
  const [session, setSession] = useState<RevisionToday | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [hints, setHints] = useState<Record<string, boolean>>({});
  const [result, setResult] = useState<RevisionSubmitResult | null>(null);
  const started = useRef(Date.now());
  const start = useAiAction(aiService.revisionToday);
  const submit = useAiAction(aiService.submitRevision);

  const begin = async () => {
    setResult(null); setAnswers({}); setHints({});
    const r = await start.run(count);
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
    <div className="space-y-6">
      <Card><CardBody className="flex flex-wrap items-end gap-3">
        <div className="flex-1">
          <p className="font-semibold">Today’s spaced revision</p>
          <p className="text-sm text-muted">Questions you got wrong before, due again today, with an AI hint for each. Your locked cheat-code cards come along as flashcards.</p>
        </div>
        <Select label="Questions" value={String(count)} onChange={(e) => setCount(Number(e.target.value))} options={[5, 10, 15, 20].map((n) => ({ value: String(n), label: String(n) }))} />
        <Button onClick={begin} loading={start.busy}>{session ? 'New set' : 'Start'}</Button>
      </CardBody></Card>
      <AiErrorNotice error={start.error} onRetry={begin} />
      {session && (
        <>
          {result && <Card><CardBody><p className="text-lg font-bold">{result.correct} of {result.total} correct{result.accuracy != null ? ` · ${result.accuracy}%` : ''}</p></CardBody></Card>}
          <ol className="space-y-4">
            {session.questions.map((q, i) => {
              const r = byId.get(q.question_id);
              return (
                <li key={q.question_id}><Card><CardBody>
                  <div className="flex flex-wrap items-center gap-2 text-xs text-muted">
                    <span>Q{i + 1}</span>{q.topic && <Badge tone="neutral">{q.topic}</Badge>}<span>Target {q.target_time_sec}s</span>
                    {r && (r.status === 'correct' ? <Badge tone="success" icon={<CheckCircle2 className="h-3 w-3" />}>Correct</Badge> : <Badge tone="danger" icon={<XCircle className="h-3 w-3" />}>{r.status}</Badge>)}
                  </div>
                  <p className="mt-2 text-sm font-medium whitespace-pre-line">{q.text}</p>
                  <div className="mt-3 grid gap-2 sm:grid-cols-2">
                    {q.options.map((o) => {
                      const picked = answers[q.question_id] === o.key;
                      const correct = r && String(r.correct_answer) === o.key;
                      return (
                        <button key={o.key} type="button" disabled={!!result} onClick={() => setAnswers((s) => ({ ...s, [q.question_id]: o.key }))}
                          className={cn('rounded-lg border px-3 py-2 text-left text-sm', correct ? 'border-green-300 bg-success-soft' : picked ? (r ? 'border-red-300 bg-danger-soft' : 'border-primary bg-primary-soft') : 'border-line hover:border-primary')}>
                          <span className="font-semibold">{o.key}.</span> {o.text}
                        </button>
                      );
                    })}
                  </div>
                  {q.hint && !result && (hints[q.question_id]
                    ? <p className="mt-3 rounded-lg bg-sticky-yellow px-3 py-2 text-sm"><Lightbulb className="mr-1 inline h-4 w-4" aria-hidden />{q.hint}</p>
                    : <Button size="sm" variant="ghost" className="mt-2" onClick={() => setHints((s) => ({ ...s, [q.question_id]: true }))} leftIcon={<Lightbulb className="h-4 w-4" />}>Show hint</Button>)}
                  {r?.explanation && <p className="mt-3 text-sm text-muted">{r.explanation}</p>}
                </CardBody></Card></li>
              );
            })}
          </ol>
          {!result && session.questions.length > 0 && <div className="flex justify-end"><Button onClick={finish} loading={submit.busy}>Check answers</Button></div>}
          <AiErrorNotice error={submit.error} onRetry={finish} />
          {session.flashcards.length > 0 && (
            <Card><CardHeader title="Your flashcards" /><CardBody className="grid gap-3 md:grid-cols-2">
              {session.flashcards.map((c) => <CheatCardView key={c.id} p={c.payload} />)}
            </CardBody></Card>
          )}
        </>
      )}
    </div>
  );
}

function CurrentAffairsPanel() {
  const [date, setDate] = useState('');
  const [ca, setCa] = useState<CurrentAffairs | null>(null);
  const run = useAiAction(aiService.currentAffairs);
  const load = async () => { const r = await run.run(date || undefined); if (r) setCa(r); };
  return (
    <div className="space-y-6">
      <Card><CardBody className="flex flex-wrap items-end gap-3">
        <div className="flex-1">
          <p className="font-semibold">Daily current affairs</p>
          <p className="text-sm text-muted">The day’s exam-relevant news, every quiz question fact-checked by a second model.</p>
        </div>
        <Input label="Date (optional)" type="date" value={date} max={new Date().toISOString().slice(0, 10)} onChange={(e) => setDate(e.target.value)} />
        <Button onClick={load} loading={run.busy}>{ca ? 'Load' : 'Show digest'}</Button>
      </CardBody></Card>
      <AiErrorNotice error={run.error} onRetry={load} />
      {run.busy && !ca && <LoadingSkeleton variant="list" />}
      {ca && <Card><CardBody><ArtifactHeader a={ca} /><div className="mt-4"><CurrentAffairsView p={ca.payload} /></div></CardBody></Card>}
    </div>
  );
}

const TASKS: { value: WritingTaskType; label: string }[] = [
  { value: 'essay', label: 'Essay' }, { value: 'formal_letter', label: 'Formal letter' }, { value: 'informal_letter', label: 'Informal letter' },
  { value: 'precis', label: 'Précis' }, { value: 'report', label: 'Report' }, { value: 'paragraph', label: 'Paragraph' },
];

function WritingPanel() {
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
    <div className="space-y-6">
      <Card><CardBody className="space-y-4">
        <div className="grid gap-3 sm:grid-cols-2">
          <Select label="Task" value={task} onChange={(e) => setTask(e.target.value as WritingTaskType)} options={TASKS} />
          <Input label="Word limit" type="number" min={50} max={2000} value={limit} onChange={(e) => setLimit(e.target.value)} />
        </div>
        <Textarea label="Question" rows={2} maxLength={3000} value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Paste the essay or letter question" />
        <Textarea label={`Your answer (${words} words)`} rows={10} maxLength={16000} value={answer} onChange={(e) => setAnswer(e.target.value)} />
        <Switch checked={rewrite} onChange={setRewrite} label="Also show a topper rewrite" description="Uses 1 Master credit (AI Tutor Pro or the Topper Combo)." />
        <div className="flex flex-wrap items-center justify-between gap-2">
          <AllowanceChip feature="descriptive_evals" label="Evaluations" />
          <Button onClick={go} loading={run.busy} disabled={question.trim().length < 5 || words < 30}>{run.busy ? 'Evaluating…' : 'Evaluate'}</Button>
        </div>
        {words > 0 && words < 30 && <p className="text-xs text-muted">Write at least 30 words.</p>}
        <AiErrorNotice error={run.error} onRetry={go} />
      </CardBody></Card>
      {ev && <Card><CardBody><ArtifactHeader a={ev} /><div className="mt-4"><WritingView p={ev.payload} /></div></CardBody></Card>}
    </div>
  );
}

export function PracticePage() {
  useDocumentTitle('Revision & practice');
  const [params, setParams] = useSearchParams();
  const t = params.get('tab');
  const tab: Tab = t === 'current' || t === 'writing' ? t : 'revision';
  return (
    <div className="mx-auto max-w-5xl">
      <PageHeader title="Revision & practice" description="Spaced revision from your mistakes, daily current affairs and descriptive writing practice." />
      <Tabs ariaLabel="Practice" className="mb-5" value={tab} onChange={(v) => setParams({ tab: v })}
        items={[{ value: 'revision', label: 'Revision AI' }, { value: 'current', label: 'Current affairs' }, { value: 'writing', label: 'Writing evaluator' }]} />
      {tab === 'revision' ? <RevisionPanel /> : tab === 'current' ? <CurrentAffairsPanel /> : <WritingPanel />}
    </div>
  );
}
