import { useEffect, useRef, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { ArrowRight, BookOpenText, Check, Send, Shuffle } from 'lucide-react';
import { formatDate, isSupportReply, type AiMode, type BlackboardLesson, type CodeCheck, type DeepDive, type TutorChatMessage } from '@prepmitra/shared';
import { Badge, Button, Card, CardBody, CardHeader, EmptyState, LoadingSkeleton, Mitra, Tabs, Textarea } from '@/components/ui';
import { AiErrorNotice, AllowanceChip, SupportBanner, useAiAction, useAiQuery } from '@/components/ai/AiUi';
import { ArtifactHeader, DeepDiveView } from '@/components/ai/AiViews';
import { AiNote, Chalkboard, Eyebrow, HandLine, SeatingDiagram, softCard } from '@/components/ai/Board';
import { aiService } from '@/services/aiService';
import { useCurrentUser } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

type Tab = 'board' | 'deep';

interface Msg { id: string | number; role: 'user' | 'assistant'; content: string; support?: boolean }

const DEFAULT_CHIPS = ['Why does this step work?', 'Give me a harder one', 'Explain in Hindi'];

// ---------- Ask Mitra (tutor chat) ----------
function AskMitra({ topic, step }: { topic?: string; step?: string }) {
  const user = useCurrentUser();
  const history = useAiQuery(() => aiService.tutorHistory(), 'tutor-history');
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [text, setText] = useState('');
  const [story, setStory] = useState(false);
  const [followUps, setFollowUps] = useState<string[]>([]);
  const [support, setSupport] = useState<string | null>(null);
  const [lastMsg, setLastMsg] = useState('');
  const box = useRef<HTMLDivElement>(null);
  const chat = useAiAction(aiService.tutorChat);

  useEffect(() => {
    const items: TutorChatMessage[] = history.data ?? [];
    if (!items.length) return;
    setMsgs(items.slice(-20).map((m) => ({ id: m.id, role: m.role, content: m.content })));
    setSessionId(items[items.length - 1]!.session_id);
  }, [history.data]);
  useEffect(() => { const el = box.current; if (el) el.scrollTop = el.scrollHeight; }, [msgs.length, chat.busy]);

  const send = async (message: string, explainDifferently = false) => {
    const m = message.trim();
    if (!m || chat.busy) return;
    setText('');
    setLastMsg(m);
    if (!explainDifferently) setMsgs((s) => [...s, { id: `u${Date.now()}`, role: 'user', content: m }]);
    const r = await chat.run({
      message: m, session_id: sessionId, style: story ? 'story' : 'normal', explain_differently: explainDifferently,
      language: /\bhindi\b/i.test(m) ? 'hi' : undefined,
    });
    if (!r) return;
    setSessionId(r.session_id);
    setFollowUps(r.follow_ups);
    if (r.support) setSupport(r.support);
    setMsgs((s) => [...s, { id: `a${Date.now()}`, role: 'assistant', content: r.reply, support: !!r.support }]);
  };

  const first = user?.name?.split(' ')[0];
  const greeting = topic
    ? `Namaste${first ? ` ${first}` : ''}! Today we crack ${topic.toLowerCase()}. I will draw each step on the board. Stop me anytime and ask why.`
    : `Namaste${first ? ` ${first}` : ''}! Ask me anything: a concept, a question from your mock, or how to plan the week.`;
  const chips = followUps.length ? followUps : DEFAULT_CHIPS;

  return (
    <aside className={cn(softCard, 'flex min-h-[460px] flex-col border-[1.5px] border-ink shadow-[4px_5px_0_#1c2321] lg:sticky lg:top-20 lg:max-h-[calc(100dvh-7rem)]')} aria-label="Ask Mitra">
      <div className="flex items-center gap-3 border-b border-line p-4">
        <Mitra size={36} />
        <div>
          <h2 className="font-bold">Ask Mitra</h2>
          <p className="flex items-center gap-1.5 text-xs text-secondary"><span className="h-1.5 w-1.5 rounded-full bg-success" aria-hidden />AI coach{step ? ' · knows this board' : ''}</p>
        </div>
      </div>
      <SupportBanner message={support} className="m-3" />
      <div ref={box} className="min-h-0 flex-1 space-y-3 overflow-y-auto p-3 scrollbar-thin" aria-live="polite">
        <ChatBubble role="assistant" content={greeting} />
        {history.loading && !msgs.length && <LoadingSkeleton variant="list" count={2} />}
        {msgs.map((m) => <ChatBubble key={m.id} role={m.role} content={m.content} support={m.support} />)}
        {chat.busy && <p className="px-1 font-hand text-muted">Mitra is writing…</p>}
      </div>
      <div className="border-t border-line p-3">
        <AiErrorNotice error={chat.error} onRetry={() => send(lastMsg)} className="mb-3" />
        <div className="mb-3 flex flex-col items-start gap-2">
          {chips.map((f) => (
            <button key={f} type="button" onClick={() => send(f)} disabled={chat.busy}
              className="rounded-full border-[1.5px] border-primary px-3 py-1 text-left text-xs font-semibold text-primary hover:bg-primary-soft disabled:opacity-50">{f}</button>
          ))}
          {msgs.some((m) => m.role === 'assistant') && (
            <button type="button" onClick={() => send(lastMsg || 'Explain that differently', true)} disabled={chat.busy}
              className="inline-flex items-center gap-1 rounded-full border border-line-strong px-3 py-1 text-xs font-semibold hover:border-primary hover:text-primary">
              <Shuffle className="h-3 w-3" aria-hidden /> Explain differently
            </button>
          )}
        </div>
        <form className="flex items-end gap-2" onSubmit={(e) => { e.preventDefault(); void send(text); }}>
          <textarea value={text} onChange={(e) => setText(e.target.value)} maxLength={2000} rows={1} aria-label="Message"
            onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); void send(text); } }}
            placeholder={step ? 'Ask about this step…' : 'Ask Mitra…'} className="min-h-10 min-w-0 flex-1 resize-none rounded-lg border-[1.5px] border-ink bg-card px-3 py-2 text-sm focus:border-primary focus:outline-none" />
          <Button type="submit" size="icon" aria-label="Send" disabled={!text.trim() || chat.busy}><Send className="h-4 w-4" /></Button>
        </form>
        <label className="mt-2 flex items-center gap-1.5 text-xs text-muted">
          <input type="checkbox" checked={story} onChange={(e) => setStory(e.target.checked)} /> Story mode
        </label>
        <p className="mt-2 text-[11px] leading-snug text-muted">AI-generated explanations — check with your teacher if unsure. Scores are always calculated by code.</p>
      </div>
    </aside>
  );
}

function ChatBubble({ role, content, support }: { role: 'user' | 'assistant'; content: string; support?: boolean }) {
  if (role === 'user') {
    return <div className="flex justify-end"><p className="max-w-[85%] whitespace-pre-line rounded-2xl rounded-br-sm border-[1.5px] border-ink bg-card px-3.5 py-2 text-sm">{content}</p></div>;
  }
  return (
    <div className={cn('max-w-[92%] rounded-2xl rounded-tl-sm px-3.5 py-2.5', support ? 'border-2 border-secondary bg-secondary-soft text-ink' : 'bg-chalkboard text-chalk-text shadow-[0_3px_0_var(--color-wood)]')}>
      <Eyebrow tone={support ? 'green' : 'chalk'}>Mitra · AI coach</Eyebrow>
      <p className="mt-0.5 whitespace-pre-line font-hand text-[15px] leading-snug">{content}</p>
    </div>
  );
}

// ---------- the blackboard ----------
function CheckYourself({ lesson }: { lesson: BlackboardLesson }) {
  const [i, setI] = useState(0);
  const [picked, setPicked] = useState<string | null>(null);
  const [res, setRes] = useState<CodeCheck | null>(null);
  const check = useAiAction(aiService.checkLesson);
  const q = lesson.check[i];
  useEffect(() => { setI(0); setPicked(null); setRes(null); }, [lesson.id]);
  if (!q) return null;
  const pick = async (key: string) => {
    if (res || check.busy) return;
    setPicked(key);
    const r = await check.run(lesson.id, i, key);
    if (r) setRes(r);
  };
  const next = () => { setI((x) => (x + 1) % lesson.check.length); setPicked(null); setRes(null); };
  return (
    <section className={cn(softCard, 'p-4 sm:p-5')} aria-labelledby="check-yourself">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 id="check-yourself" className="font-bold">Check yourself <span className="ml-1 text-xs font-normal text-muted">Question {i + 1} of {lesson.check.length} · checked instantly by code</span></h2>
        {lesson.check.length > 1 && <Button size="sm" variant="outline" onClick={next}>Another question</Button>}
      </div>
      <p className="mt-3 font-semibold">{q.text}</p>
      <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
        {q.options.map((o) => {
          const isAns = res && res.answer === o.key;
          const wrong = res && picked === o.key && !res.correct;
          return (
            <button key={o.key} type="button" onClick={() => pick(o.key)} disabled={!!res || check.busy} aria-pressed={picked === o.key}
              className={cn('flex items-center gap-2 rounded-xl border-[1.5px] px-3 py-2.5 text-left text-sm font-medium transition',
                isAns ? 'border-success bg-success-soft' : wrong ? 'border-pen bg-danger-soft' : picked === o.key ? 'border-primary' : 'border-line-strong hover:border-ink')}>
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-ink text-xs">{o.key}</span>
              <span className="min-w-0">{o.text}</span>
            </button>
          );
        })}
      </div>
      <AiErrorNotice error={check.error} className="mt-3" />
      {res && (
        <p className={cn('mt-3 font-hand text-lg', res.correct ? 'text-secondary' : 'text-pen')}>
          {res.correct ? '✓ Right. ' : `✗ Not quite — it is ${res.answer}. `}{res.explanation}
        </p>
      )}
    </section>
  );
}

function Blackboard() {
  const index = useAiQuery(() => aiService.lessons(), 'lessons');
  const [lessonId, setLessonId] = useState<string | null>(null);
  const id = lessonId ?? index.data?.recommended ?? index.data?.items[0]?.id ?? null;
  const lesson = useAiQuery(() => (id ? aiService.lesson(id) : Promise.resolve(null)), `lesson-${id ?? ''}`);
  const [step, setStep] = useState(0);
  useEffect(() => { setStep(0); }, [id]);
  const l = lesson.data;
  const s = l?.steps[step];

  if (index.loading || (lesson.loading && !l)) return <LoadingSkeleton variant="page" />;
  if (index.error) return <AiErrorNotice error={index.error} onRetry={index.reload} />;
  if (lesson.error) return <AiErrorNotice error={lesson.error} onRetry={lesson.reload} />;
  if (!l || !s) return <EmptyState icon={<BookOpenText className="h-6 w-6" />} title="No lessons yet" description="Blackboard lessons appear here once they are ready." />;

  const why = index.data?.why;
  const items = index.data?.items ?? [];
  const lineText = l.steps[step]!.lines.join(' ').toLowerCase();

  return (
    <div>
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0">
          <HandLine>the blackboard — {l.subject}{why && l.id === index.data?.recommended ? ' · picked for you' : ''}</HandLine>
          <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">{l.topic}</h1>
        </div>
        <p className="inline-flex w-fit items-center gap-2 rounded-full bg-chalkboard px-3.5 py-1.5 text-xs font-semibold text-chalk-text shadow-[0_3px_0_var(--color-wood)]">
          <span className="h-2 w-2 rounded-full bg-marigold" aria-hidden /> PrepMithra AI tutor · explains, never just answers
        </p>
      </div>

      <div className="grid gap-5 lg:grid-cols-[210px_minmax(0,1fr)_300px]">
        {/* outline */}
        <div className="space-y-5">
          <nav className={cn(softCard, 'p-4')} aria-label="Lesson outline">
            <div className="flex items-center justify-between">
              <h2 className="font-bold">Lesson outline</h2>
              <span className="text-xs font-semibold text-muted">{step + 1} / {l.steps.length}</span>
            </div>
            <div className="mt-2 h-1.5 rounded-full bg-surface" aria-hidden><div className="h-full rounded-full bg-secondary" style={{ width: `${((step + 1) / l.steps.length) * 100}%` }} /></div>
            <ol className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-1">
              {l.steps.map((x, i) => {
                const done = i < step;
                const cur = i === step;
                return (
                  <li key={x.title}>
                    <button type="button" onClick={() => setStep(i)} aria-current={cur ? 'step' : undefined}
                      className={cn('flex w-full items-center gap-2.5 rounded-xl px-2.5 py-2 text-left transition',
                        cur ? 'border-[1.5px] border-ink bg-sticky-yellow' : done ? 'bg-secondary-soft' : 'hover:bg-surface')}>
                      <span className={cn('flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-xs font-bold',
                        done ? 'bg-secondary text-white' : cur ? 'bg-ink text-white' : 'border-[1.5px] border-ink')}>
                        {done ? <Check className="h-3.5 w-3.5" aria-hidden /> : i + 1}
                      </span>
                      <span className="min-w-0">
                        <span className="block text-sm font-semibold leading-tight">{x.title}</span>
                        <span className="block text-[11px] text-muted">{done ? 'Done' : cur ? 'On the board now' : 'Up next'}</span>
                      </span>
                    </button>
                  </li>
                );
              })}
            </ol>
            {items.length > 1 && (
              <label className="mt-4 block text-xs font-semibold text-muted">
                Another lesson
                <select value={l.id} onChange={(e) => setLessonId(e.target.value)} className="mt-1 w-full rounded-lg border border-line-strong bg-card px-2 py-1.5 text-sm text-ink">
                  {items.map((x) => <option key={x.id} value={x.id}>{x.topic}</option>)}
                </select>
              </label>
            )}
          </nav>
          {why && (
            <div className="-rotate-1 bg-sticky-yellow p-4 shadow-sticky">
              <Eyebrow tone="primary">Why this topic</Eyebrow>
              <p className="mt-1 text-sm leading-snug">{why.topic} costs you marks right now ({why.mastery}% mastery). Calculated by code from your answers.</p>
            </div>
          )}
        </div>

        {/* board */}
        <div className="min-w-0 space-y-5">
          <section className="rounded-[16px] border-[1.5px] border-ink bg-card p-4" aria-label="The question">
            <Eyebrow>The question · {l.question.style}</Eyebrow>
            <p className="mt-1.5 text-sm sm:text-base">{l.question.text}</p>
            <div className="mt-3 flex flex-wrap gap-2">
              {l.question.clues.map((c) => {
                const on = lineText.includes(c.toLowerCase());
                return <span key={c} className={cn('rounded-full px-3 py-1 text-xs font-semibold sm:text-sm', on ? 'border-[1.5px] border-ink bg-marigold' : 'bg-surface')}>{c}</span>;
              })}
            </div>
          </section>

          <Chalkboard className="p-4 sm:p-6" ariaLabel={`Step ${step + 1} of ${l.steps.length}: ${s.title}`}>
            <div className="flex items-center justify-between gap-2">
              <span className="flex items-center gap-2"><Mitra size={26} /><Eyebrow tone="chalk">Mitra · AI · writing</Eyebrow></span>
              <span className="font-hand text-lg text-chalk-text/85">Step {step + 1} of {l.steps.length}</span>
            </div>
            <div className="mt-4 grid items-center gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,240px)]">
              <div className="min-w-0" aria-live="polite">
                <h2 className="font-hand text-2xl font-bold !text-marigold sm:text-3xl">{s.title}</h2>
                {s.lines.map((line) => <p key={line} className="mt-2 font-hand text-lg leading-snug sm:text-xl">{line}</p>)}
                {s.trap && <p className="mt-4 border-t border-dashed border-white/30 pt-3 font-hand text-base text-marigold sm:text-lg">Trap: {s.trap}</p>}
              </div>
              {s.diagram && s.diagram.seats > 0 && (
                <div className="mx-auto w-full max-w-[260px]">
                  <SeatingDiagram seats={s.diagram.seats} placed={s.diagram.placed} arrow={s.diagram.arrow} centre={s.diagram.arrow ? 'count back' : 'facing centre'} />
                </div>
              )}
            </div>
            <div className="mt-5 flex items-center justify-between gap-3">
              <button type="button" onClick={() => setStep((x) => Math.max(0, x - 1))} disabled={step === 0}
                className="h-10 rounded-lg border-[1.5px] border-chalk-text/70 px-4 text-sm font-semibold hover:bg-white/10 disabled:opacity-40">← Previous</button>
              <span className="hidden items-center gap-1.5 sm:flex" aria-hidden>
                {l.steps.map((_, i) => <span key={i} className={cn('h-1.5 rounded-full', i === step ? 'w-5 bg-marigold' : i < step ? 'w-1.5 bg-marigold' : 'w-1.5 bg-white/35')} />)}
              </span>
              <button type="button" onClick={() => setStep((x) => Math.min(l.steps.length - 1, x + 1))} disabled={step === l.steps.length - 1}
                className="inline-flex h-10 items-center gap-1.5 rounded-lg bg-marigold px-4 text-sm font-bold text-ink shadow-[0_3px_0_#c2410c] hover:brightness-105 disabled:opacity-40">
                Next step <ArrowRight className="h-4 w-4" aria-hidden />
              </button>
            </div>
          </Chalkboard>

          <CheckYourself lesson={l} />
        </div>

        <AskMitra topic={l.topic} step={s.title} />
      </div>
    </div>
  );
}

// ---------- deep dives (kept from the previous tutor screen) ----------
const MODES: { value: AiMode; label: string; desc: string; feature: string }[] = [
  { value: 'smart', label: 'Smart', desc: '1 Smart credit', feature: 'smart_credits' },
  { value: 'master', label: 'Master', desc: '1 Master credit · deeper, stronger model', feature: 'master_credits' },
  { value: 'ultra', label: 'Ultra', desc: '1 Ultra credit · our strongest model', feature: 'ultra_credits' },
];

function DeepDivePanel() {
  const [params] = useSearchParams();
  const solutionId = params.get('solution') ?? undefined;
  const [text, setText] = useState(params.get('text') ?? '');
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
    <div className="grid gap-6 lg:grid-cols-[1fr_280px]">
      <div className="min-w-0">
        <SupportBanner message={support} className="mb-4" />
        <Card>
          <CardBody className="space-y-4">
            {solutionId ? (
              <p className="rounded-lg bg-surface px-3 py-2 text-sm">Deep dive on the question you just solved.</p>
            ) : (
              <Textarea label="Question or concept" rows={4} maxLength={4000} value={text} onChange={(e) => setText(e.target.value)}
                placeholder="Paste a question you got wrong, or name a concept (e.g. 'successive percentage change')." />
            )}
            <div>
              <p className="mb-2 text-sm font-medium">Tutor level</p>
              <div className="grid gap-2 sm:grid-cols-3">
                {MODES.map((m) => (
                  <button key={m.value} type="button" aria-pressed={mode === m.value} onClick={() => setMode(m.value)}
                    className={cn('rounded-lg border p-3 text-left', mode === m.value ? 'border-primary bg-primary-soft' : 'border-line hover:border-primary')}>
                    <p className="font-semibold">{m.label}</p>
                    <p className="text-xs text-muted">{m.desc}</p>
                    <div className="mt-2"><AllowanceChip feature={m.feature} /></div>
                  </button>
                ))}
              </div>
            </div>
            <div className="flex justify-end">
              <Button onClick={go} loading={run.busy} disabled={!solutionId && text.trim().length < 3}>{run.busy ? 'Building your deep dive…' : 'Start deep dive'}</Button>
            </div>
            <AiErrorNotice error={run.error} onRetry={go} />
          </CardBody>
        </Card>
        {dive && (
          <Card className="mt-6"><CardBody>
            <ArtifactHeader a={dive} extra={dive.mode && <Badge tone="primary">{dive.mode}</Badge>} />
            <DeepDiveView p={dive.payload} note={dive.personal_note} />
          </CardBody></Card>
        )}
      </div>
      <Card className="h-fit">
        <CardHeader title="Your deep dives" />
        <CardBody>
          {list.loading ? <LoadingSkeleton variant="list" count={2} /> : !list.data?.length ? (
            <EmptyState icon={<BookOpenText className="h-6 w-6" />} title="None yet" description="Deep dives you make are saved here." className="py-6" />
          ) : (
            <ul className="space-y-2">
              {list.data.map((d, i) => (
                <li key={`${d.id}-${i}`}>
                  <Link to={`/ai/artifacts/${d.id}`} className="block rounded-lg border border-line px-3 py-2 text-sm hover:border-primary">
                    <p className="font-medium">{d.title}</p>
                    <p className="text-xs text-muted">{d.mode} · {formatDate(d.saved_at)}</p>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </CardBody>
      </Card>
    </div>
  );
}

export function TutorPage() {
  useDocumentTitle('AI Tutor');
  const [params, setParams] = useSearchParams();
  const tab: Tab = params.get('tab') === 'deep' ? 'deep' : 'board';
  return (
    <div className="min-w-0">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <Tabs ariaLabel="Tutor" value={tab} onChange={(v) => setParams(v === 'deep' ? { tab: 'deep' } : {})}
          items={[{ value: 'board', label: 'Blackboard' }, { value: 'deep', label: 'Deep dives' }]} />
        <div className="flex flex-wrap gap-2"><AllowanceChip feature="tutor_chat_turns" label="Chat" /><AllowanceChip feature="smart_credits" label="Smart" /></div>
      </div>
      {tab === 'board' ? <Blackboard /> : (
        <>
          <HandLine>go deep on one question —</HandLine>
          <h1 className="mb-5 text-2xl font-bold tracking-tight sm:text-3xl">Deep dives</h1>
          <DeepDivePanel />
          <AiNote className="mt-6 inline-block">AI-generated explanations — check with your teacher if unsure.</AiNote>
        </>
      )}
    </div>
  );
}
