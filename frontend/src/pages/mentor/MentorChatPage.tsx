import { useEffect, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { Send } from 'lucide-react';
import { Button, Card, LoadingSkeleton, Mitra, PageHeader } from '@/components/ui';
import { NeedsBackend } from '@/components/mentor/MentorUi';
import { useMentorT, type MentorKey } from '@/components/mentor/format';
import { errorMessage, mentorService, type ChatMessage } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

const STARTERS: MentorKey[] = ['q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9'];

export function MentorChatPage() {
  const t = useMentorT();
  useDocumentTitle(t('chatTitle'));
  const history = useAsync(() => mentorService.chatHistory(), []);
  const [msgs, setMsgs] = useState<ChatMessage[]>([]);
  const [text, setText] = useState('');
  const [busy, setBusy] = useState(false);
  const end = useRef<HTMLDivElement>(null);
  useEffect(() => { if (history.data) setMsgs(history.data.items); }, [history.data]);
  useEffect(() => { end.current?.scrollIntoView({ block: 'end' }); }, [msgs.length, busy]);

  const ask = async (q: string) => {
    const message = q.trim();
    if (!message || busy) return;
    setText('');
    setMsgs((m) => [...m, { id: -Date.now(), role: 'student', content: message, follow_ups: [], created_at: new Date().toISOString() }]);
    setBusy(true);
    try {
      const reply = await mentorService.chat(message);
      setMsgs((m) => [...m, reply]);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };
  const last = [...msgs].reverse().find((m) => m.role === 'mentor');
  const suggestions = last?.follow_ups.length ? last.follow_ups : STARTERS.map((k) => t(k));

  return (
    <div className="flex h-[calc(100dvh-10rem)] min-h-[480px] flex-col">
      <PageHeader title={t('chatTitle')} description={t('chatDesc')} className="mb-4" />
      {history.error ? <NeedsBackend error={history.error} /> : (
        <Card className="flex min-h-0 flex-1 flex-col">
          <div className="min-h-0 flex-1 space-y-3 overflow-y-auto p-4" aria-live="polite">
            {history.loading && !history.data ? <LoadingSkeleton variant="list" /> : msgs.length === 0 && (
              <div className="flex items-center gap-3 text-muted"><Mitra size={40} /><p>{t('chatEmpty')}</p></div>
            )}
            {msgs.map((m) => (
              <div key={m.id} className={cn('flex gap-2', m.role === 'student' ? 'justify-end' : 'justify-start')}>
                {m.role === 'mentor' && <Mitra size={32} className="mt-1 shrink-0" />}
                <div className={cn('max-w-[85%] rounded-2xl px-4 py-2.5 text-sm sm:max-w-[70%]', m.role === 'student' ? 'rounded-br-sm bg-primary text-white' : 'rounded-bl-sm border border-line bg-card text-ink')}>
                  <p className="whitespace-pre-line">{m.content}</p>
                  {m.role === 'mentor' && m.source && <p className="mt-1 text-[11px] text-muted">{m.source === 'ai' ? t('sourceAi') : t('sourceCode')}</p>}
                </div>
              </div>
            ))}
            {busy && <div className="flex gap-2"><Mitra size={32} /><span className="animate-pulse rounded-2xl border border-line px-4 py-2.5 text-sm text-muted">…</span></div>}
            <div ref={end} />
          </div>
          <div className="border-t border-line p-3">
            <div className="mb-2 flex gap-2 overflow-x-auto pb-1">
              {suggestions.map((s) => (
                <button key={s} type="button" onClick={() => ask(s)} disabled={busy}
                  className="shrink-0 rounded-full border border-line-strong px-3 py-1 text-xs hover:bg-stone-50 disabled:opacity-50">{s}</button>
              ))}
            </div>
            <form className="flex gap-2" onSubmit={(e) => { e.preventDefault(); void ask(text); }}>
              <input value={text} onChange={(e) => setText(e.target.value)} maxLength={1000} placeholder={t('chatPlaceholder')} aria-label={t('chatPlaceholder')}
                className="h-10 min-w-0 flex-1 rounded-lg border border-line-strong px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
              <Button type="submit" loading={busy} disabled={!text.trim()} leftIcon={<Send className="h-4 w-4" />}>{t('send')}</Button>
            </form>
          </div>
        </Card>
      )}
    </div>
  );
}
