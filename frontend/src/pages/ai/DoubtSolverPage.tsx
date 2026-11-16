import { useRef, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Camera, Check, Flag, GraduationCap, Plus, RotateCcw, ShieldCheck, Sparkles, ThumbsDown, ThumbsUp, Upload } from 'lucide-react';
import { isSupportReply, relativeTime, type AiOption, type DoubtAnswer, type DoubtResult, type DoubtSolution } from '@prepmitra/shared';
import { Badge, Button, Input, Mitra, Switch, Tabs, Textarea } from '@/components/ui';
import { AiErrorNotice, AllowanceChip, SupportBanner, useAiAction } from '@/components/ai/AiUi';
import { PracticeQuestions } from '@/components/ai/AiViews';
import { AiNote, Chalkboard, Eyebrow, HandLine, softCard } from '@/components/ai/Board';
import { aiService, imageFileToDataUrl } from '@/services/aiService';
import { errorMessage } from '@/services';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

type Tab = 'text' | 'photo';
const KEYS = ['A', 'B', 'C', 'D'];

const VERIFICATION: Record<DoubtAnswer['verification'], string> = {
  code_checked: 'Checked by code',
  two_models: 'Verified by two AI models',
  human: 'Checked by our team',
  unverified: 'Not verified',
};

interface Asked { text: string; options: AiOption[]; chosen?: string | null }
interface DoubtEntry { id: string; at: number; asked: Asked; result: DoubtAnswer }

/** "(c) 40 s" — the answer key in lower case, like a printed paper. */
const optLabel = (o: AiOption) => `(${o.key.toLowerCase()}) ${o.text}`;

function StepHeader({ stage }: { stage: 0 | 1 | 2 }) {
  const steps = ['Ask', 'Mitra solves', 'Understand'];
  return (
    <ol className="flex flex-wrap gap-2" aria-label="Progress">
      {steps.map((s, i) => (
        <li key={s} aria-current={stage === i ? 'step' : undefined}
          className={cn('inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-sm font-semibold',
            stage === i ? 'bg-ink text-white' : 'bg-secondary-soft text-ink')}>
          <span className={cn('flex h-5 w-5 items-center justify-center rounded-full text-[11px]', stage === i ? 'bg-marigold text-ink' : 'border border-secondary text-secondary')}>{i + 1}</span>
          {s}
        </li>
      ))}
    </ol>
  );
}

/** One step: the first sentence is the reasoning; anything after a line break or a colon-led formula is the chalk "working". */
function splitStep(step: string): [string, string | null] {
  const nl = step.split('\n').map((x) => x.trim()).filter(Boolean);
  if (nl.length > 1) return [nl[0]!, nl.slice(1).join(' ')];
  const m = step.match(/^(.*?[.:])\s+([^.]*=[^.]*\.?)$/);
  if (m) return [m[1]!, m[2]!];
  return [step, null];
}

function SolutionBoard({ r, s, asked }: { r: DoubtAnswer; s: DoubtSolution; asked: Asked }) {
  const answerKey = (s.answer ?? r.answer ?? '').trim().toUpperCase();
  const opts = asked.options;
  return (
    <Chalkboard className="p-4 sm:p-6" ariaLabel="Step-by-step solution">
      <span className="flex items-center gap-2"><Mitra size={26} /><Eyebrow tone="chalk">Mitra · AI · step by step</Eyebrow></span>
      {s.answer_text && <p className="mt-3 font-hand text-lg leading-snug text-chalk-text/90">{s.answer_text}</p>}
      <ol className="mt-4 space-y-4">
        {s.steps.map((step, i) => {
          const [say, work] = splitStep(step);
          return (
            <li key={i} className="flex gap-3">
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 border-marigold font-hand text-lg text-marigold">{i + 1}</span>
              <div className="min-w-0 pt-0.5">
                <p className="font-hand text-base leading-snug sm:text-lg">{say}</p>
                {work && <p className={cn('font-hand text-xl font-bold leading-snug sm:text-2xl', i === s.steps.length - 1 ? 'text-marigold' : 'text-chalk-text')}>{work}</p>}
              </div>
            </li>
          );
        })}
      </ol>
      <div className="mt-5 rounded-xl bg-paper p-4 text-ink">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <Eyebrow>Final answer</Eyebrow>
          <span className={cn('inline-flex items-center gap-1 text-xs font-semibold', r.verified ? 'text-secondary' : 'text-warning-ink')}>
            {r.verified ? <Check className="h-3.5 w-3.5" aria-hidden /> : <ShieldCheck className="h-3.5 w-3.5" aria-hidden />}
            {VERIFICATION[r.verification]}{r.verification === 'code_checked' && s.numeric_check ? `: ${s.numeric_check}` : ''}
          </span>
        </div>
        {opts.length > 0 ? (
          <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {opts.map((o) => {
              const right = o.key.toUpperCase() === answerKey;
              return (
                <div key={o.key} className="relative flex min-h-12 items-center justify-center px-2 py-2 text-center text-sm sm:text-base">
                  {right && <span className="absolute -top-3 right-2 rotate-[-6deg] font-hand text-sm text-pen">this one</span>}
                  <span className={cn('relative z-10', right ? 'font-bold' : 'text-muted')}>{optLabel(o)}</span>
                  {right && <span aria-hidden className="absolute inset-0 -rotate-3 rounded-[50%] border-[2.5px] border-pen" />}
                  {right && <span className="sr-only"> (correct answer)</span>}
                </div>
              );
            })}
          </div>
        ) : (
          <p className="mt-2 text-xl font-bold">Answer: <span className="text-primary">{r.answer}</span></p>
        )}
        {r.verification !== 'code_checked' && s.numeric_check && <p className="mt-2 text-xs text-muted">Check: {s.numeric_check}</p>}
      </div>
    </Chalkboard>
  );
}

function AnswerView({ entry, onNew }: { entry: DoubtEntry; onNew: () => void }) {
  const { result: r, asked } = entry;
  const [again, setAgain] = useState<DoubtSolution | null>(null);
  const [voted, setVoted] = useState<'up' | 'down' | 'flag' | null>(null);
  const [similar, setSimilar] = useState(false);
  const explain = useAiAction(aiService.explainAgain);
  const s = again ?? r.solution;
  const chosenOpt = asked.chosen ? asked.options.find((o) => o.key === asked.chosen) : undefined;
  const wrongChoice = asked.chosen && asked.chosen.toUpperCase() !== (s.answer ?? r.answer).toUpperCase();

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
  const explainAgain = async () => { const x = await explain.run(r.solution_id!); if (x) setAgain(x.solution); };
  const deepDiveLink = `/ai/tutor?tab=deep${r.solution_id ? `&solution=${r.solution_id}` : `&text=${encodeURIComponent(asked.text.slice(0, 1500))}`}`;

  return (
    <div className="space-y-5">
      <section className="rounded-[16px] border border-line bg-card p-4 sm:p-5" aria-label="Your question">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <Eyebrow tone="green">Question recognised{r.read_question ? ' · read from your photo' : ''}</Eyebrow>
          <div className="flex flex-wrap gap-1.5">
            <Badge tone={r.verified ? 'success' : 'warning'} icon={<ShieldCheck className="h-3 w-3" />}>{VERIFICATION[r.verification]}</Badge>
            {(r.source === 'exact' || r.source === 'meaning') && <Badge tone="neutral">Instant from the solution library</Badge>}
            {r.premium_used && <Badge tone="primary">Premium model</Badge>}
          </div>
        </div>
        <p className="mt-2 text-sm leading-relaxed sm:text-base">{asked.text}</p>
        {asked.options.length > 0 && <p className="mt-1 text-sm text-muted">{asked.options.map(optLabel).join('   ')}</p>}
      </section>

      {r.notice && <AiNote tone="paper" className="rounded-xl !text-warning-ink">Please double-check: {r.notice}</AiNote>}

      <div className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_260px]">
        <div className="min-w-0 space-y-4">
          <SolutionBoard r={r} s={s} asked={asked} />
          {again && <p className="text-xs text-muted">Showing a different explanation.</p>}
          {(s.memory_hook || s.real_life_example) && (
            <div className="grid gap-3 sm:grid-cols-2">
              {s.memory_hook && <div className="bg-sticky-green p-4 shadow-sticky"><Eyebrow tone="green">Memory hook</Eyebrow><p className="mt-1 font-hand text-lg leading-snug">{s.memory_hook}</p></div>}
              {s.real_life_example && <div className="bg-sticky-purple p-4 shadow-sticky"><Eyebrow>Real-life example</Eyebrow><p className="mt-1 text-sm">{s.real_life_example}</p></div>}
            </div>
          )}
          {similar && s.practice_question && (
            <section className={cn(softCard, 'p-4')} aria-label="Similar question">
              <h2 className="font-bold">Similar question</h2>
              <PracticeQuestions questions={[s.practice_question]} />
            </section>
          )}
        </div>

        <div className="space-y-4">
          {(s.common_trap || r.personal_note) && (
            <section className="rounded-[16px] border-[1.5px] border-ink bg-danger-soft p-4">
              <h2 className="font-hand text-2xl font-bold !text-pen">The trap</h2>
              {r.personal_note && (
                <div className="mt-2">
                  <Eyebrow tone="pen">About your choice</Eyebrow>
                  {wrongChoice && chosenOpt && <p className="mt-0.5 font-bold">Option {optLabel(chosenOpt)}</p>}
                  <p className="mt-1 text-sm leading-relaxed">{r.personal_note}</p>
                </div>
              )}
              {s.common_trap && <p className="mt-2 text-sm leading-relaxed">{s.common_trap}</p>}
            </section>
          )}
          {s.shortcut && (
            <section className="rounded-[16px] border-[1.5px] border-ink bg-primary-soft p-4">
              <Eyebrow tone="primary">Faster method · cheat code</Eyebrow>
              <h2 className="sr-only">Shortcut</h2>
              <p className="mt-2 font-hand text-lg leading-snug text-pen">{s.shortcut}</p>
              <Link to="/ai/cheat-codes" className="mt-3 inline-block text-sm font-semibold text-primary hover:underline">Open in Cheat codes →</Link>
            </section>
          )}
          <section className={cn(softCard, 'space-y-3 p-4')}>
            {r.solution_id && (
              <div className="flex items-center justify-between gap-2">
                <h2 className="font-bold">Was this clear?</h2>
                <div className="flex gap-1.5">
                  <Button size="icon" variant={voted === 'up' ? 'secondary' : 'outline'} aria-label="Helpful" disabled={!!voted} onClick={() => vote('up')}><ThumbsUp className="h-4 w-4" /></Button>
                  <Button size="icon" variant={voted === 'down' ? 'secondary' : 'outline'} aria-label="Not helpful" disabled={!!voted} onClick={() => vote('down')}><ThumbsDown className="h-4 w-4" /></Button>
                </div>
              </div>
            )}
            {r.solution_id && (
              <Button variant="outline" className="w-full border-[1.5px] border-ink" loading={explain.busy} leftIcon={<RotateCcw className="h-4 w-4" />} onClick={explainAgain}>
                Explain differently
              </Button>
            )}
            {s.practice_question && (
              <Button variant="outline" className="w-full border-[1.5px] border-ink" aria-pressed={similar} onClick={() => setSimilar((v) => !v)}>Similar question</Button>
            )}
            <Link to={deepDiveLink} className="flex h-10 w-full items-center justify-center gap-1.5 rounded-lg border border-line-strong text-sm font-medium hover:bg-stone-50">
              <GraduationCap className="h-4 w-4" aria-hidden /> Deep dive
            </Link>
            <AiErrorNotice error={explain.error} onRetry={explainAgain} />
            {r.solution_id && (
              <button type="button" disabled={voted === 'flag'} onClick={() => vote('flag')} className="inline-flex items-center gap-1 text-xs text-muted hover:text-pen disabled:opacity-50">
                <Flag className="h-3.5 w-3.5" aria-hidden /> Report an error
              </button>
            )}
            <p className="text-[11px] leading-snug text-muted">AI-generated explanation. The final answer is re-checked by code; ask your teacher if a step still feels off.</p>
          </section>
          <Button className="w-full lg:hidden" variant="secondary" leftIcon={<Plus className="h-4 w-4" />} onClick={onNew}>Ask another doubt</Button>
        </div>
      </div>
    </div>
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
  const [support, setSupport] = useState<string | null>(null);
  const [history, setHistory] = useState<DoubtEntry[]>([]);
  const [openId, setOpenId] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const solve = useAiAction(aiService.solveDoubt);
  const photo = useAiAction(aiService.photoDoubt);
  const action = tab === 'photo' ? photo : solve;
  const open = history.find((h) => h.id === openId) ?? null;

  const keep = (r: DoubtResult, asked: Asked) => {
    if (isSupportReply(r)) { setSupport(r.support); return; }
    const entry: DoubtEntry = { id: r.solution_id ?? `d${Date.now()}`, at: Date.now(), asked, result: r };
    setHistory((h) => [entry, ...h.filter((x) => x.id !== entry.id)].slice(0, 12));
    setOpenId(entry.id);
  };

  const submit = async () => {
    setSupport(null);
    if (tab === 'text') {
      const opts = options.map((o, i) => ({ key: KEYS[i]!, text: o.trim() })).filter((o) => o.text);
      const r = await solve.run({ text: text.trim(), options: opts, chosen, escalate });
      if (r) keep(r, { text: text.trim(), options: opts, chosen });
    } else if (image) {
      const r = await photo.run({ image, chosen });
      if (r) keep(r, { text: r.read_question?.text ?? '', options: r.read_question?.options ?? [], chosen });
    }
  };

  const newDoubt = () => {
    setOpenId(null); setSupport(null); setText(''); setOptions(['', '', '', '']); setChosen(null); setImage(null);
  };

  const onFile = async (f?: File) => {
    if (!f) return;
    if (!f.type.startsWith('image/')) return toast.error('Choose a photo (JPEG, PNG or WebP).');
    try { setImage(await imageFileToDataUrl(f)); } catch { toast.error('Could not read that photo.'); }
  };

  const stage: 0 | 1 | 2 = action.busy ? 1 : open ? 2 : 0;

  return (
    <div className="grid min-w-0 gap-6 lg:grid-cols-[220px_minmax(0,1fr)]">
      {/* left rail */}
      <aside className="order-2 space-y-4 lg:order-1">
        <Button onClick={newDoubt} className="h-12 w-full rounded-xl border-[1.5px] border-ink shadow-[3px_4px_0_#1c2321]" leftIcon={<Plus className="h-4 w-4" />}>New doubt</Button>
        <nav className={cn(softCard, 'p-3')} aria-label="Recent doubts">
          <h2 className="px-1 font-bold">Recent doubts</h2>
          {history.length === 0 ? (
            <p className="mt-2 px-1 text-xs text-muted">Doubts you solve in this session show up here.</p>
          ) : (
            <ul className="mt-2 space-y-1.5">
              {history.map((h) => (
                <li key={h.id}>
                  <button type="button" onClick={() => setOpenId(h.id)} aria-current={h.id === openId ? 'true' : undefined}
                    className={cn('flex w-full gap-2 rounded-lg px-2.5 py-2 text-left', h.id === openId ? 'border-[1.5px] border-ink bg-sticky-yellow' : 'bg-surface/60 hover:bg-surface')}>
                    <span className={cn('mt-1.5 h-2 w-2 shrink-0 rounded-full', h.id === openId ? 'bg-primary' : 'bg-line-strong')} aria-hidden />
                    <span className="min-w-0">
                      <span className="line-clamp-2 block text-sm font-semibold leading-snug">{h.asked.text || 'Photo question'}</span>
                      <span className="block text-[11px] text-muted">{relativeTime(new Date(h.at).toISOString())}</span>
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </nav>
        <div className="hidden rotate-[-1deg] bg-sticky-yellow p-4 shadow-sticky sm:block">
          <Eyebrow tone="primary">Photo tip</Eyebrow>
          <p className="mt-1 text-sm leading-snug">Crop to one question, options included. Mitra reads printed and neat handwritten text.</p>
        </div>
      </aside>

      <div className="order-1 min-w-0 lg:order-2">
        <div className="mb-5 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <HandLine>stuck on one question? —</HandLine>
            <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">Doubt solver</h1>
          </div>
          <StepHeader stage={stage} />
        </div>
        <SupportBanner message={support} className="mb-5" />

        {open ? <AnswerView key={open.id} entry={open} onNew={newDoubt} /> : (
          <section className="rounded-[18px] border-[1.5px] border-ink bg-card shadow-[4px_5px_0_#1c2321]" aria-label="Ask a doubt">
            <div className="flex flex-wrap items-center justify-between gap-2 px-4 pt-3">
              <Tabs ariaLabel="How to ask" value={tab} onChange={(v) => setParams(v === 'photo' ? { tab: 'photo' } : {})}
                items={[{ value: 'text', label: 'Type the question' }, { value: 'photo', label: 'Photo' }]} />
              <div className="flex flex-wrap gap-2"><AllowanceChip feature="doubts" label="Doubts" /><AllowanceChip feature="photo_doubts" label="Photo" /></div>
            </div>
            <div className="p-4 sm:p-5">
              {tab === 'text' ? (
                <div className="space-y-4">
                  <Textarea label="Question" value={text} onChange={(e) => setText(e.target.value)} rows={4} maxLength={4000}
                    placeholder="e.g. A train 240 m long passes a pole in 16 seconds. How long will it take to cross a platform 360 m long?" />
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
                      <img src={image} alt="Your question" className="max-h-64 max-w-full rounded-lg border border-line object-contain" />
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
                      className={cn('h-9 w-9 rounded-full border-[1.5px] text-sm font-semibold', chosen === k ? 'border-primary bg-primary text-white' : 'border-ink hover:border-primary')}>{k}</button>
                  ))}
                </div>
              </div>
              <div className="mt-5 flex justify-end">
                <Button onClick={submit} loading={action.busy} disabled={tab === 'text' ? text.trim().length < 8 : !image} leftIcon={<Sparkles className="h-4 w-4" />}
                  className="rounded-full border-[1.5px] border-ink shadow-[3px_3px_0_#1c2321]">
                  {action.busy ? 'Solving and checking…' : 'Solve'}
                </Button>
              </div>
              <AiErrorNotice error={action.error} onRetry={submit} className="mt-4" />
              <p className="mt-4 text-[11px] text-muted">AI-generated explanation. The final answer is re-checked by code; ask your teacher if a step still feels off.</p>
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
