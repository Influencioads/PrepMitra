import { useEffect, useRef, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { BookOpenText, Send, Shuffle } from 'lucide-react';
import { formatDate, isSupportReply, type AiMode, type DeepDive, type TutorChatMessage } from '@prepmitra/shared';
import { Badge, Button, Card, CardBody, CardHeader, EmptyState, LoadingSkeleton, Mitra, PageHeader, Tabs, Textarea } from '@/components/ui';
import { AiErrorNotice, AllowanceChip, SupportBanner, useAiAction, useAiQuery } from '@/components/ai/AiUi';
import { ArtifactHeader, DeepDiveView } from '@/components/ai/AiViews';
import { aiService } from '@/services/aiService';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

type Tab = 'chat' | 'deep';

interface Msg { id: string | number; role: 'user' | 'assistant'; content: string; support?: boolean }

function ChatPanel() {
  const history = useAiQuery(() => aiService.tutorHistory(), 'tutor-history');
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [text, setText] = useState('');
  const [story, setStory] = useState(false);
  const [followUps, setFollowUps] = useState<string[]>([]);
  const [support, setSupport] = useState<string | null>(null);
  const [lastMsg, setLastMsg] = useState('');
  const end = useRef<HTMLDivElement>(null);
  const chat = useAiAction(aiService.tutorChat);

  useEffect(() => {
    const items: TutorChatMessage[] = history.data ?? [];
    if (!items.length) return;
    setMsgs(items.map((m) => ({ id: m.id, role: m.role, content: m.content })));
    setSessionId(items[items.length - 1]!.session_id);
  }, [history.data]);
  useEffect(() => { end.current?.scrollIntoView?.({ block: 'end' }); }, [msgs.length, chat.busy]);

  const send = async (message: string, explainDifferently = false) => {
    const m = message.trim();
    if (!m || chat.busy) return;
    setText('');
    setLastMsg(m);
    if (!explainDifferently) setMsgs((s) => [...s, { id: `u${Date.now()}`, role: 'user', content: m }]);
    const r = await chat.run({ message: m, session_id: sessionId, style: story ? 'story' : 'normal', explain_differently: explainDifferently });
    if (!r) return;
    setSessionId(r.session_id);
    setFollowUps(r.follow_ups);
    if (r.support) setSupport(r.support);
    setMsgs((s) => [...s, { id: `a${Date.now()}`, role: 'assistant', content: r.reply, support: !!r.support }]);
  };

  return (
    <div className="flex h-[calc(100dvh-16rem)] min-h-[460px] flex-col">
      <SupportBanner message={support} className="mb-3" />
      <Card className="flex min-h-0 flex-1 flex-col">
        <div className="min-h-0 flex-1 space-y-3 overflow-y-auto p-4" aria-live="polite">
          {history.loading && !msgs.length ? <LoadingSkeleton variant="list" /> : msgs.length === 0 && (
            <div className="flex items-center gap-3 text-muted"><Mitra size={40} /><p>Ask Mitra anything about your preparation: a concept, a question from your mock, or how to plan the week.</p></div>
          )}
          {msgs.map((m) => (
            <div key={m.id} className={cn('flex gap-2', m.role === 'user' ? 'justify-end' : 'justify-start')}>
              {m.role === 'assistant' && <Mitra size={32} className="mt-1 shrink-0" />}
              <div className={cn('max-w-[85%] whitespace-pre-line rounded-2xl px-4 py-2.5 text-sm sm:max-w-[70%]',
                m.role === 'user' ? 'rounded-br-sm bg-primary text-white' : m.support ? 'rounded-bl-sm border-2 border-secondary bg-secondary-soft' : 'rounded-bl-sm border border-line bg-card')}>
                {m.content}
              </div>
            </div>
          ))}
          {chat.busy && <p className="text-sm text-muted">Mitra is thinking…</p>}
          <div ref={end} />
        </div>
        <div className="border-t border-line p-3">
          <AiErrorNotice error={chat.error} onRetry={() => send(lastMsg)} className="mb-3" />
          <div className="mb-2 flex flex-wrap gap-2">
            {followUps.map((f) => (
              <button key={f} type="button" onClick={() => send(f)} className="rounded-full border border-line-strong px-3 py-1 text-xs hover:border-primary hover:text-primary">{f}</button>
            ))}
            {msgs.some((m) => m.role === 'assistant') && (
              <button type="button" onClick={() => send(lastMsg || 'Explain that differently', true)} className="inline-flex items-center gap-1 rounded-full border border-line-strong px-3 py-1 text-xs hover:border-primary hover:text-primary">
                <Shuffle className="h-3 w-3" /> Explain differently
              </button>
            )}
          </div>
          <form className="flex items-end gap-2" onSubmit={(e) => { e.preventDefault(); void send(text); }}>
            <label className="flex shrink-0 items-center gap-1.5 self-center text-xs text-muted">
              <input type="checkbox" checked={story} onChange={(e) => setStory(e.target.checked)} /> Story mode
            </label>
            <textarea value={text} onChange={(e) => setText(e.target.value)} maxLength={2000} rows={1} aria-label="Message"
              onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); void send(text); } }}
              placeholder="Ask Mitra…" className="min-h-10 flex-1 resize-none rounded-lg border border-line-strong bg-card px-3 py-2 text-sm focus:border-primary focus:outline-none" />
            <Button type="submit" size="icon" aria-label="Send" disabled={!text.trim() || chat.busy}><Send className="h-4 w-4" /></Button>
          </form>
        </div>
      </Card>
    </div>
  );
}

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
  const tab: Tab = params.get('tab') === 'deep' ? 'deep' : 'chat';
  return (
    <div>
      <PageHeader title="AI Tutor" description="Ask Mitra, your tutor who knows your mocks, or go deep on one question."
        actions={<div className="flex flex-wrap gap-2"><AllowanceChip feature="tutor_chat_turns" label="Chat" /><AllowanceChip feature="smart_credits" label="Smart" /></div>} />
      <Tabs ariaLabel="Tutor" className="mb-5" value={tab} onChange={(v) => setParams(v === 'deep' ? { tab: 'deep' } : {})}
        items={[{ value: 'chat', label: 'Ask Mitra' }, { value: 'deep', label: 'Deep dives' }]} />
      {tab === 'chat' ? <ChatPanel /> : <DeepDivePanel />}
    </div>
  );
}
