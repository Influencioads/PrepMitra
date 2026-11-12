import { useRef, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Camera, Flag, GraduationCap, RotateCcw, ShieldCheck, Sparkles, ThumbsDown, ThumbsUp, Upload } from 'lucide-react';
import { isSupportReply, type AiOption, type DoubtAnswer, type DoubtResult, type DoubtSolution } from '@prepmitra/shared';
import { Badge, Button, Card, CardBody, Input, PageHeader, Switch, Tabs, Textarea } from '@/components/ui';
import { AiErrorNotice, AllowanceChip, SupportBanner, useAiAction } from '@/components/ai/AiUi';
import { Bullets, Callout, PracticeQuestions, Section } from '@/components/ai/AiViews';
import { aiService, imageFileToDataUrl } from '@/services/aiService';
import { errorMessage } from '@/services';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

type Tab = 'text' | 'photo';
const KEYS = ['A', 'B', 'C', 'D'];

const VERIFICATION: Record<DoubtAnswer['verification'], string> = {
  code_checked: 'Checked by calculation',
  two_models: 'Verified by two AI models',
  human: 'Checked by our team',
  unverified: 'Not verified',
};

function SolutionBody({ s }: { s: DoubtSolution }) {
  return (
    <>
      {s.answer_text && <p className="mt-3 text-base font-medium">{s.answer_text}</p>}
      <Section title="Steps"><Bullets items={s.steps} ordered /></Section>
      <div className="mt-5 grid gap-3 md:grid-cols-2">
        {s.shortcut && <Callout tone="success" title="Shortcut">{s.shortcut}</Callout>}
        {s.common_trap && <Callout tone="warning" title="Common trap">{s.common_trap}</Callout>}
        {s.memory_hook && <Callout title="Memory hook">{s.memory_hook}</Callout>}
        {s.real_life_example && <Callout title="Real-life example">{s.real_life_example}</Callout>}
      </div>
      {s.numeric_check && <p className="mt-3 text-xs text-muted">Check: {s.numeric_check}</p>}
      {s.practice_question && <Section title="Try one yourself"><PracticeQuestions questions={[s.practice_question]} /></Section>}
    </>
  );
}

function AnswerCard({ r, question }: { r: DoubtAnswer; question: { text: string; options: AiOption[]; chosen?: string | null } }) {
  const [again, setAgain] = useState<DoubtSolution | null>(null);
  const [voted, setVoted] = useState<'up' | 'down' | 'flag' | null>(null);
  const explain = useAiAction(aiService.explainAgain);
  const vote = async (kind: 'up' | 'down' | 'flag') => {
    if (!r.solution_id) return;
    try {
      await aiService.doubtFeedback(r.solution_id, kind === 'flag' ? { report_error: true } : { helpful: kind === 'up' });
      setVoted(kind);
      toast.success(kind === 'flag' ? 'Thanks. Our team will check this answer.' : 'Thanks for the feedback.');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };
  const deepDiveLink = `/ai/tutor?tab=deep${r.solution_id ? `&solution=${r.solution_id}` : `&text=${encodeURIComponent(question.text.slice(0, 1500))}`}`;
  return (
    <Card className="mt-6">
      <CardBody>
        <div className="flex flex-wrap items-center justify-between gap-2">
          <p className="text-2xl font-bold">Answer: <span className="text-primary">{r.answer}</span></p>
          <div className="flex flex-wrap gap-1.5">
            <Badge tone={r.verified ? 'success' : 'warning'} icon={<ShieldCheck className="h-3 w-3" />}>{VERIFICATION[r.verification]}</Badge>
            {(r.source === 'exact' || r.source === 'meaning') && <Badge tone="neutral">Instant from the solution library</Badge>}
            {r.premium_used && <Badge tone="primary">Premium model</Badge>}
          </div>
        </div>
        {r.notice && <div className="mt-3"><Callout tone="warning" title="Please double-check">{r.notice}</Callout></div>}
        {r.personal_note && <div className="mt-3"><Callout tone="warning" title="About your choice">{r.personal_note}</Callout></div>}
        <SolutionBody s={again ?? r.solution} />
        {again && <p className="mt-2 text-xs text-muted">Showing a different explanation.</p>}

        <div className="mt-6 flex flex-wrap items-center gap-2 border-t border-line pt-4">
          {r.solution_id && (
            <Button size="sm" variant="outline" loading={explain.busy} leftIcon={<RotateCcw className="h-4 w-4" />}
              onClick={async () => { const x = await explain.run(r.solution_id!); if (x) setAgain(x.solution); }}>
              Still confused? Explain again
            </Button>
          )}
          <Link to={deepDiveLink} className="inline-flex items-center gap-1.5 rounded-lg border border-line-strong px-3 py-1.5 text-sm font-medium hover:bg-stone-50">
            <GraduationCap className="h-4 w-4" /> Deep dive
          </Link>
          {r.solution_id && (
            <div className="ml-auto flex items-center gap-1">
              <span className="mr-1 text-xs text-muted">Helpful?</span>
              <Button size="icon" variant={voted === 'up' ? 'secondary' : 'ghost'} aria-label="Helpful" disabled={!!voted} onClick={() => vote('up')}><ThumbsUp className="h-4 w-4" /></Button>
              <Button size="icon" variant={voted === 'down' ? 'secondary' : 'ghost'} aria-label="Not helpful" disabled={!!voted} onClick={() => vote('down')}><ThumbsDown className="h-4 w-4" /></Button>
              <Button size="sm" variant="ghost" disabled={voted === 'flag'} leftIcon={<Flag className="h-4 w-4" />} onClick={() => vote('flag')}>Report an error</Button>
            </div>
          )}
        </div>
        <AiErrorNotice error={explain.error} className="mt-3" onRetry={() => explain.run(r.solution_id!).then((x) => x && setAgain(x.solution))} />
      </CardBody>
    </Card>
  );
}

export function DoubtSolverPage() {
  useDocumentTitle('Doubt Solver');
  const [params, setParams] = useSearchParams();
  const tab: Tab = params.get('tab') === 'photo' ? 'photo' : 'text';
  const [text, setText] = useState(params.get('text') ?? '');
  const [options, setOptions] = useState<string[]>(['', '', '', '']);
  const [chosen, setChosen] = useState<string | null>(null);
  const [escalate, setEscalate] = useState(false);
  const [image, setImage] = useState<string | null>(null);
  const [result, setResult] = useState<DoubtResult | null>(null);
  const [asked, setAsked] = useState<{ text: string; options: AiOption[]; chosen?: string | null } | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const solve = useAiAction(aiService.solveDoubt);
  const photo = useAiAction(aiService.photoDoubt);
  const action = tab === 'photo' ? photo : solve;

  const submit = async () => {
    setResult(null);
    if (tab === 'text') {
      const opts = options.map((o, i) => ({ key: KEYS[i]!, text: o.trim() })).filter((o) => o.text);
      const r = await solve.run({ text: text.trim(), options: opts, chosen, escalate });
      if (r) { setResult(r); setAsked({ text: text.trim(), options: opts, chosen }); }
    } else if (image) {
      const r = await photo.run({ image, chosen });
      if (r) { setResult(r); setAsked({ text: r.read_question?.text ?? '', options: r.read_question?.options ?? [], chosen }); }
    }
  };

  const onFile = async (f?: File) => {
    if (!f) return;
    if (!f.type.startsWith('image/')) return toast.error('Choose a photo (JPEG, PNG or WebP).');
    try { setImage(await imageFileToDataUrl(f)); } catch { toast.error('Could not read that photo.'); }
  };

  return (
    <div className="mx-auto max-w-4xl">
      <PageHeader title="Doubt Solver" description="Stuck on a question? Get a verified, step-by-step answer with the shortcut and the trap to avoid."
        actions={<div className="flex flex-wrap gap-2"><AllowanceChip feature="doubts" label="Doubts" /><AllowanceChip feature="photo_doubts" label="Photo" /></div>} />
      {isSupportReply(result) && <SupportBanner message={result.support} className="mb-5" />}
      <Card>
        <Tabs ariaLabel="How to ask" className="px-4" value={tab} onChange={(v) => { setParams(v === 'photo' ? { tab: 'photo' } : {}); setResult(null); }}
          items={[{ value: 'text', label: 'Type the question' }, { value: 'photo', label: 'Photo' }]} />
        <CardBody>
          {tab === 'text' ? (
            <div className="space-y-4">
              <Textarea label="Question" value={text} onChange={(e) => setText(e.target.value)} rows={4} maxLength={4000}
                placeholder="e.g. A price falls by 20%. By what percent must it rise to get back to the original?" />
              <div className="grid gap-3 sm:grid-cols-2">
                {options.map((o, i) => (
                  <Input key={i} label={`Option ${KEYS[i]} (optional)`} value={o} maxLength={500}
                    onChange={(e) => setOptions((s) => s.map((x, j) => (j === i ? e.target.value : x)))} />
                ))}
              </div>
              <Switch checked={escalate} onChange={setEscalate} label="Use the premium model"
                description="For a tricky question. Uses one of your premium doubts (Pro), and falls back to the standard model when none are left." />
            </div>
          ) : (
            <div>
              <input ref={fileRef} type="file" accept="image/*" capture="environment" className="sr-only" onChange={(e) => onFile(e.target.files?.[0])} aria-label="Question photo" />
              {image ? (
                <div className="flex flex-col items-start gap-3 sm:flex-row">
                  <img src={image} alt="Your question" className="max-h-64 rounded-lg border border-line object-contain" />
                  <Button variant="outline" size="sm" onClick={() => fileRef.current?.click()} leftIcon={<Upload className="h-4 w-4" />}>Choose another</Button>
                </div>
              ) : (
                <button type="button" onClick={() => fileRef.current?.click()}
                  className="flex w-full flex-col items-center gap-2 rounded-xl border-2 border-dashed border-line-strong px-6 py-10 text-muted hover:border-primary hover:text-primary">
                  <Camera className="h-8 w-8" aria-hidden />
                  <span className="font-medium">Take or upload a photo of the question</span>
                  <span className="text-xs">One question per photo, with its options if it has them. Photo doubts come with the AI Tutor packs.</span>
                </button>
              )}
            </div>
          )}
          <div className="mt-4">
            <p className="text-sm font-medium">Your answer (optional) <span className="font-normal text-muted">— Mitra explains why it was wrong</span></p>
            <div className="mt-2 flex gap-2">
              {KEYS.map((k) => (
                <button key={k} type="button" aria-pressed={chosen === k} onClick={() => setChosen(chosen === k ? null : k)}
                  className={cn('h-9 w-9 rounded-full border text-sm font-semibold', chosen === k ? 'border-primary bg-primary text-white' : 'border-line-strong hover:border-primary')}>{k}</button>
              ))}
            </div>
          </div>
          <div className="mt-5 flex justify-end">
            <Button onClick={submit} loading={action.busy} disabled={tab === 'text' ? text.trim().length < 8 : !image} leftIcon={<Sparkles className="h-4 w-4" />}>
              {action.busy ? 'Solving and checking…' : 'Solve'}
            </Button>
          </div>
          <AiErrorNotice error={action.error} onRetry={submit} className="mt-4" />
        </CardBody>
      </Card>

      {result && !isSupportReply(result) && asked && (
        <>
          {result.read_question && (
            <Card className="mt-6"><CardBody>
              <p className="text-xs font-semibold uppercase tracking-wide text-muted">Mitra read this question</p>
              <p className="mt-1 text-sm">{result.read_question.text}</p>
              {result.read_question.options.length > 0 && <p className="mt-1 text-sm text-muted">{result.read_question.options.map((o) => `${o.key}. ${o.text}`).join('   ')}</p>}
            </CardBody></Card>
          )}
          <AnswerCard r={result} question={asked} />
        </>
      )}
    </div>
  );
}
