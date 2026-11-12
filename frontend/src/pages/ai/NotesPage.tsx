import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Layers, Search } from 'lucide-react';
import type { DeckRequest, Notes, NotesKind, NotesLevel, TopicDeck } from '@prepmitra/shared';
import { Badge, Button, Card, CardBody, CardHeader, EmptyState, Input, LoadingSkeleton, PageHeader, Select, Switch, Tabs } from '@/components/ui';
import { AiErrorNotice, AllowanceChip, useAiAction, useAiQuery } from '@/components/ai/AiUi';
import { ArtifactHeader, DeckView, NotesView } from '@/components/ai/AiViews';
import { aiService } from '@/services/aiService';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

type Tab = 'notes' | 'decks';
const KINDS: { value: NotesKind; label: string }[] = [
  { value: 'notes', label: 'Notes' }, { value: 'formula_sheet', label: 'Formula sheet' }, { value: 'mind_map', label: 'Mind map' }, { value: 'revision_sheet', label: 'Revision sheet' },
];
const LEVELS: { value: NotesLevel; label: string }[] = [{ value: 'basic', label: 'Basic' }, { value: 'exam', label: 'Exam level' }, { value: 'advanced', label: 'Advanced' }];

function NotesPanel() {
  const [topic, setTopic] = useState('');
  const [kind, setKind] = useState<NotesKind>('notes');
  const [level, setLevel] = useState<NotesLevel>('exam');
  const [personal, setPersonal] = useState(false);
  const [notes, setNotes] = useState<Notes | null>(null);
  const run = useAiAction(aiService.notes);
  const go = async () => { const r = await run.run({ topic: topic.trim(), kind, level, personal }); if (r) setNotes(r); };
  return (
    <>
      <Card><CardBody className="space-y-4">
        <Input label="Topic" value={topic} maxLength={120} onChange={(e) => setTopic(e.target.value)} placeholder="e.g. Time and work, Indian Constitution: Fundamental Rights" />
        <div className="grid gap-3 sm:grid-cols-2">
          <Select label="Format" value={kind} onChange={(e) => setKind(e.target.value as NotesKind)} options={KINDS} />
          <Select label="Level" value={level} onChange={(e) => setLevel(e.target.value as NotesLevel)} options={LEVELS} />
        </div>
        <Switch checked={personal} onChange={setPersonal} label="Make them personal"
          description="Built from your own mistakes on this topic. Uses one personal note (Starter 5, Pro 20 a month). Shared notes are free." />
        <div className="flex justify-end"><Button onClick={go} loading={run.busy} disabled={topic.trim().length < 3}>{run.busy ? 'Writing your notes…' : 'Make notes'}</Button></div>
        <AiErrorNotice error={run.error} onRetry={go} />
      </CardBody></Card>
      {notes && <Card className="mt-6"><CardBody><ArtifactHeader a={notes} /><NotesView p={notes.payload} /></CardBody></Card>}
    </>
  );
}

function DecksPanel() {
  const [q, setQ] = useState('');
  const query = useDebounce(q, 300);
  const lib = useAiQuery(() => aiService.deckLibrary(query), `lib-${query}`);
  const [deck, setDeck] = useState<TopicDeck | null>(null);
  const [topic, setTopic] = useState('');
  const [level, setLevel] = useState<NotesLevel>('exam');
  const [mode, setMode] = useState<NonNullable<DeckRequest['mode']>>('smart');
  const open = useAiAction(aiService.libraryDeck);
  const make = useAiAction(aiService.topicDeck);
  const go = async () => { const r = await make.run({ topic: topic.trim(), level, mode }); if (r) setDeck(r); };

  return (
    <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
      <div className="space-y-6">
        <Card>
          <CardHeader title="Free library" description="Ready-made decks, free on every plan." />
          <CardBody>
            <div className="relative">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" aria-hidden />
              <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search topics" aria-label="Search decks"
                className="w-full rounded-lg border border-line-strong bg-card py-2 pl-9 pr-3 text-sm focus:border-primary focus:outline-none" />
            </div>
            <div className="mt-3">
              {lib.loading ? <LoadingSkeleton variant="list" count={3} /> : lib.error ? <AiErrorNotice error={lib.error} onRetry={lib.reload} /> : !lib.data?.length ? (
                <p className="text-sm text-muted">No library deck matches. Make a custom one.</p>
              ) : (
                <ul className="space-y-1.5">
                  {lib.data.map((d) => (
                    <li key={d.id}>
                      <button type="button" onClick={async () => { const r = await open.run(d.id); if (r) setDeck(r); }}
                        className="flex w-full items-center justify-between rounded-lg border border-line px-3 py-2 text-left text-sm hover:border-primary">
                        <span className="font-medium">{d.title}</span><Badge tone="neutral">{d.level}</Badge>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Custom deck" description="10–15 slides with a visual on each, traps, cheat codes and practice." />
          <CardBody className="space-y-3">
            <Input label="Topic" value={topic} maxLength={120} onChange={(e) => setTopic(e.target.value)} />
            <Select label="Level" value={level} onChange={(e) => setLevel(e.target.value as NotesLevel)} options={LEVELS} />
            <Select label="Made with" value={mode} onChange={(e) => setMode(e.target.value as typeof mode)} options={[
              { value: 'library', label: 'Library only (free)' },
              { value: 'smart', label: 'Smart (1 Pro deck, or 3 Smart credits)' },
              { value: 'master', label: 'Master (3 Master credits)' },
              { value: 'ultra', label: 'Ultra (4 Ultra credits)' },
            ]} />
            <div className="flex flex-wrap gap-1.5"><AllowanceChip feature="topic_decks" label="Decks" /><AllowanceChip feature="smart_credits" label="Smart" /></div>
            <Button className="w-full" onClick={go} loading={make.busy} disabled={topic.trim().length < 3}>{make.busy ? 'Building slides…' : 'Make deck'}</Button>
            <AiErrorNotice error={make.error} onRetry={go} />
          </CardBody>
        </Card>
      </div>
      <div className="min-w-0">
        <AiErrorNotice error={open.error} className="mb-4" />
        {open.busy ? <LoadingSkeleton variant="page" /> : deck ? (
          <Card><CardBody><ArtifactHeader a={deck} extra={deck.paid_with && <Badge tone="neutral">{deck.paid_with.replace('_', ' ')}</Badge>} /><DeckView key={deck.id} p={deck.payload} note={deck.personal_note} /></CardBody></Card>
        ) : (
          <EmptyState icon={<Layers className="h-6 w-6" />} title="Pick a deck" description="Open a free library deck or make a custom one for any topic." />
        )}
      </div>
    </div>
  );
}

export function NotesPage() {
  useDocumentTitle('Notes & topic decks');
  const [params, setParams] = useSearchParams();
  const tab: Tab = params.get('tab') === 'decks' ? 'decks' : 'notes';
  return (
    <div>
      <PageHeader title="Notes & topic decks" description="Exam-ready notes, formula sheets and mind maps, or a full Topic Explainer deck."
        actions={<AllowanceChip feature="personal_notes" label="Personal notes" />} />
      <Tabs ariaLabel="Notes or decks" className="mb-5" value={tab} onChange={(v) => setParams(v === 'decks' ? { tab: 'decks' } : {})}
        items={[{ value: 'notes', label: 'Notes Maker' }, { value: 'decks', label: 'Topic Explainer decks' }]} />
      {tab === 'notes' ? <NotesPanel /> : <DecksPanel />}
    </div>
  );
}
