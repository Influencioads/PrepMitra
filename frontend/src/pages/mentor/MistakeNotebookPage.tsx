import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Bookmark, BookmarkCheck, BookX, Play } from 'lucide-react';
import { Badge, Button, Card, EmptyState, LoadingSkeleton, PageHeader, Select, Tabs } from '@/components/ui';
import { NeedsBackend, PracticeQuiz } from '@/components/mentor/MentorUi';
import { mmss, useMentorT, type MentorKey } from '@/components/mentor/format';
import {
  errorMessage, mentorService, type MistakeType, type NotebookEntry, type NotebookFilter, type NotebookPage, type PracticeSession,
} from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

const FILTERS: NotebookFilter[] = ['due', 'wrong', 'repeated', 'slow', 'corrected', 'bookmarked', 'resolved', 'all'];
const TYPES: MistakeType[] = ['concept', 'calculation', 'misread', 'wrong_formula', 'guessing', 'time_pressure', 'option_confusion'];

const show = (v: unknown, none: string) =>
  v === null || v === undefined || v === '' || (Array.isArray(v) && !v.length) ? none : Array.isArray(v) ? v.join(', ') : String(v);

function EntryCard({ e, onChange }: { e: NotebookEntry; onChange: (e: NotebookEntry) => void }) {
  const t = useMentorT();
  const [open, setOpen] = useState(false);
  const patch = async (body: Parameters<typeof mentorService.updateEntry>[1]) => {
    try {
      onChange(await mentorService.updateEntry(e.id, body));
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };
  const correct = String(e.correct_answer);
  return (
    <Card className="p-4">
      <div className="flex flex-wrap items-center gap-1.5 text-xs">
        {e.topic && <Badge tone="secondary">{e.topic}</Badge>}
        <Badge>{e.difficulty}</Badge>
        {e.reasons.map((r) => <Badge key={r} tone={r === 'wrong' ? 'danger' : 'warning'}>{r}</Badge>)}
        {e.times_wrong > 1 && <Badge tone="danger">{t('wrongTimes', { n: e.times_wrong })}</Badge>}
        {e.status === 'resolved' ? <Badge tone="success">{t('f_resolved')}</Badge> : e.next_review_at && (
          <span className="text-muted">{t('nextReview', { date: new Date(e.next_review_at).toLocaleDateString(undefined, { day: 'numeric', month: 'short' }) })}</span>
        )}
        <button type="button" onClick={() => patch({ bookmarked: !e.bookmarked })} className="ml-auto inline-flex items-center gap-1 rounded-md px-2 py-1 text-muted hover:bg-stone-100"
          aria-pressed={e.bookmarked}>
          {e.bookmarked ? <BookmarkCheck className="h-4 w-4 text-primary" aria-hidden /> : <Bookmark className="h-4 w-4" aria-hidden />}
          {e.bookmarked ? t('bookmarked') : t('bookmark')}
        </button>
      </div>
      <button type="button" className="mt-2 block w-full text-left" onClick={() => setOpen((o) => !o)} aria-expanded={open}>
        <p className={cn('whitespace-pre-line text-ink', !open && 'line-clamp-2')}>{e.text}</p>
      </button>
      {open && (
        <div className="mt-3 space-y-3 text-sm">
          {e.options.length > 0 && (
            <ul className="space-y-1">
              {e.options.map((o) => {
                const isRight = correct.split(',').includes(o.key);
                const isMine = show(e.your_answer, '').split(', ').includes(o.key);
                return (
                  <li key={o.key} className={cn('rounded-md border px-3 py-1.5', isRight ? 'border-green-300 bg-success-soft' : isMine ? 'border-red-200 bg-danger-soft' : 'border-line')}>
                    <b>{o.key}.</b> {o.text}
                  </li>
                );
              })}
            </ul>
          )}
          <p>{t('yourAnswer')}: <b className="text-danger">{show(e.your_answer, t('noAnswer'))}</b> · {t('correctAnswer')}: <b className="text-success">{show(e.correct_answer, '—')}</b> · {mmss(e.last_time_sec)}</p>
          {e.explanation && <div><p className="font-semibold">{t('explanation')}</p><p className="whitespace-pre-line text-muted">{e.explanation}</p></div>}
          {e.shortcut && <div><p className="font-semibold">{t('shortcut')}</p><p className="whitespace-pre-line text-muted">{e.shortcut}</p></div>}
        </div>
      )}
      <div className="mt-3 flex flex-wrap items-center gap-2 text-sm">
        <Select aria-label={t('mistakeType')} className="h-9 w-auto" value={e.mistake_type ?? ''}
          onChange={(ev) => patch(ev.target.value ? { mistake_type: ev.target.value as MistakeType } : { clear_mistake_type: true })}
          options={[{ value: '', label: `${t('mistakeType')}: ${t('untagged')}` }, ...TYPES.map((m) => ({ value: m, label: t(`mt_${m}` as MentorKey) }))]} />
        {e.mistake_type_source === 'auto' && <span className="text-xs text-muted">({t('autoGuess')})</span>}
      </div>
    </Card>
  );
}

export function MistakeNotebookPage() {
  const t = useMentorT();
  useDocumentTitle(t('notebookTitle'));
  const [params, setParams] = useSearchParams();
  const filter = (params.get('filter') as NotebookFilter) || 'due';
  const first = useAsync(() => mentorService.notebook(filter), [filter]);
  const [page, setPage] = useState<NotebookPage>();
  const [quiz, setQuiz] = useState<PracticeSession | null>(null);
  const [busy, setBusy] = useState(false);
  useEffect(() => setPage(first.data), [first.data]);

  const more = async () => {
    if (!page) return;
    const next = await mentorService.notebook(filter, page.items.length);
    setPage({ ...next, items: [...page.items, ...next.items] });
  };
  const start = async () => {
    setBusy(true);
    try {
      setQuiz(await mentorService.startMistakeReview(10));
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };
  const replace = (e: NotebookEntry) => setPage((p) => p && { ...p, items: p.items.map((x) => (x.id === e.id ? e : x)) });

  return (
    <div className="space-y-6">
      <PageHeader title={t('notebookTitle')} description={t('notebookDesc')}
        actions={<Button onClick={start} loading={busy} disabled={!page || page.counts.all - page.counts.resolved === 0} leftIcon={<Play className="h-4 w-4" />}>{t('startRevision')}</Button>} />
      {first.error ? <NeedsBackend error={first.error} /> : (
        <>
          <Tabs ariaLabel={t('notebookTitle')} value={filter} onChange={(f) => setParams({ filter: f })}
            items={FILTERS.map((f) => ({ value: f, label: t(`f_${f}` as MentorKey), count: page?.counts[f] }))} />
          {page && Object.keys(page.by_mistake_type).length > 0 && (
            <div className="flex flex-wrap gap-2 text-xs">
              {Object.entries(page.by_mistake_type).sort((a, b) => b[1] - a[1]).map(([k, n]) => (
                <Badge key={k}>{k === 'untagged' ? t('untagged') : t(`mt_${k}` as MentorKey)}: {n}</Badge>
              ))}
            </div>
          )}
          {first.loading && !page ? <LoadingSkeleton variant="list" /> : !page || page.items.length === 0 ? (
            <EmptyState icon={<BookX className="h-6 w-6" />} title={t('emptyNotebook')} description={t('emptyNotebookDesc')} />
          ) : (
            <div className="space-y-3">
              {page.items.map((e) => <EntryCard key={e.id} e={e} onChange={replace} />)}
              {page.items.length < page.total && <Button variant="outline" onClick={more}>{t('loadMore')}</Button>}
            </div>
          )}
        </>
      )}
      {quiz && <PracticeQuiz session={quiz} onClose={() => { setQuiz(null); first.reload(); }} />}
    </div>
  );
}
