import { useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { CheckCircle2, Lock, Send, Wand2, XCircle } from 'lucide-react';
import { examSlugFromId, getExamById, type CheatCard, type CoachSession, type CoachTestResult } from '@prepmitra/shared';
import { Badge, Button, Card, CardBody, CardHeader, LoadingSkeleton, PageHeader, Select, Stepper, Switch, Tabs, Textarea } from '@/components/ui';
import { AiErrorNotice, AllowanceChip, SupportBanner, useAiAction, useAiQuery } from '@/components/ai/AiUi';
import { CheatCardView } from '@/components/ai/AiViews';
import { aiService } from '@/services/aiService';
import { useProfileStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

type Tab = 'coach' | 'cards' | 'library';
const STEPS = ['Spot', 'Shape', 'Test', 'Lock'];

function CoachFlow({ onLocked }: { onLocked: (c: CheatCard) => void }) {
  const targets = useProfileStore((s) => s.profile.targetExamIds);
  const exams = useMemo(() => targets.map((id) => getExamById(id)).filter((e): e is NonNullable<typeof e> => !!e), [targets]);
  const [examId, setExamId] = useState(exams[0]?.id ?? 'ssc-cgl');
  const topics = useAiQuery(() => aiService.coachTopics(examSlugFromId(examId)), examId);
  const [topicId, setTopicId] = useState<number | null>(null);
  const [session, setSession] = useState<CoachSession | null>(null);
  const [thread, setThread] = useState<{ who: 'coach' | 'me'; text: string }[]>([]);
  const [msg, setMsg] = useState('');
  const [step, setStep] = useState(0);
  const [rule, setRule] = useState('');
  const [test, setTest] = useState<CoachTestResult | null>(null);
  const [share, setShare] = useState(false);
  const [support, setSupport] = useState<string | null>(null);
  const [card, setCard] = useState<CheatCard | null>(null);
  const start = useAiAction(aiService.coachStart);
  const reply = useAiAction(aiService.coachReply);
  const runTest = useAiAction(aiService.coachTest);
  const lock = useAiAction(aiService.coachLock);

  const begin = async () => {
    if (topicId == null) return;
    const s = await start.run(topicId);
    if (!s) return;
    setSession(s); setThread([{ who: 'coach', text: s.coach }]); setStep(1); setTest(null); setCard(null); setRule('');
  };
  const send = async () => {
    if (!session || !msg.trim()) return;
    const m = msg.trim();
    setMsg('');
    setThread((t) => [...t, { who: 'me', text: m }]);
    const r = await reply.run(session.session_id, m);
    if (!r) return;
    if (r.support) setSupport(r.support);
    setThread((t) => [...t, { who: 'coach', text: r.coach }]);
    if (r.rule_draft) setRule(r.rule_draft);
    if (r.step === 'test') setStep(2);
  };
  const doTest = async () => {
    if (!session) return;
    const r = await runTest.run(session.session_id, rule);
    if (!r) return;
    setTest(r);
    setStep(r.step === 'lock' ? 3 : 1);
  };
  const doLock = async () => {
    if (!session) return;
    const c = await lock.run(session.session_id, share);
    if (c) { setCard(c); onLocked(c); setStep(4); }
  };

  if (!session) {
    return (
      <Card><CardBody className="space-y-4">
        <p className="text-sm text-muted">Mitra shows you three solved questions of one type. You find the pattern, write the rule in your own words, test it on five real questions, and lock it as a revision card. Rules you discover yourself stick.</p>
        <div className="grid gap-3 sm:grid-cols-2">
          <Select label="Exam" value={examId} onChange={(e) => { setExamId(e.target.value); setTopicId(null); }}
            options={(exams.length ? exams : [getExamById('ssc-cgl')!].filter(Boolean)).map((e) => ({ value: e.id, label: e.shortTitle }))} />
          {topics.loading ? <LoadingSkeleton variant="list" count={1} /> : (
            <Select label="Topic" value={topicId != null ? String(topicId) : ''} placeholder="Choose a topic" onChange={(e) => setTopicId(Number(e.target.value))}
              options={(topics.data ?? []).map((t) => ({ value: String(t.id), label: t.name }))} />
          )}
        </div>
        <AiErrorNotice error={topics.error} onRetry={topics.reload} />
        <div className="flex flex-wrap items-center justify-between gap-2">
          <AllowanceChip feature="cheat_code_sessions" label="Sessions" />
          <Button onClick={begin} loading={start.busy} disabled={topicId == null} leftIcon={<Wand2 className="h-4 w-4" />}>Start (uses 1 session)</Button>
        </div>
        <AiErrorNotice error={start.error} onRetry={begin} />
      </CardBody></Card>
    );
  }

  return (
    <div className="space-y-5">
      <Stepper steps={STEPS} current={Math.min(step, 3)} />
      <SupportBanner message={support} />
      <Card>
        <CardHeader title={`Spot the pattern: ${session.topic}`} />
        <CardBody className="grid gap-3 md:grid-cols-3">
          {session.solved_questions.map((q, i) => (
            <div key={q.question_id} className="rounded-lg border border-line bg-paper p-3 text-sm">
              <p className="font-medium">{i + 1}. {q.text}</p>
              {q.options.length > 0 && <p className="mt-1 text-xs text-muted">{q.options.map((o) => `${o.key}. ${o.text}`).join('  ')}</p>}
              <p className="mt-2"><span className="font-semibold">Answer {String(q.answer)}.</span> {q.explanation}</p>
            </div>
          ))}
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Shape your rule" description="Say the pattern in your own words. Mitra asks until it is exact." />
        <CardBody>
          <div className="space-y-2">
            {thread.map((m, i) => (
              <p key={i} className={m.who === 'coach' ? 'rounded-lg bg-secondary-soft px-3 py-2 text-sm' : 'ml-auto max-w-[80%] rounded-lg bg-primary-soft px-3 py-2 text-sm'}>{m.text}</p>
            ))}
          </div>
          {step === 1 && (
            <form className="mt-3 flex gap-2" onSubmit={(e) => { e.preventDefault(); void send(); }}>
              <input value={msg} onChange={(e) => setMsg(e.target.value)} maxLength={1500} aria-label="Your rule" placeholder="My rule is…"
                className="flex-1 rounded-lg border border-line-strong bg-card px-3 py-2 text-sm focus:border-primary focus:outline-none" />
              <Button type="submit" size="icon" aria-label="Send" loading={reply.busy} disabled={!msg.trim()}><Send className="h-4 w-4" /></Button>
            </form>
          )}
          <AiErrorNotice error={reply.error} onRetry={send} className="mt-3" />
        </CardBody>
      </Card>

      {step >= 1 && step < 4 && (
        <Card>
          <CardHeader title="Test it" description="Your rule runs on five new questions from the bank." />
          <CardBody>
            <Textarea label="Rule" rows={2} maxLength={1000} value={rule} onChange={(e) => setRule(e.target.value)} />
            <div className="mt-3 flex justify-end"><Button onClick={doTest} loading={runTest.busy} disabled={rule.trim().length < 10}>Test my rule</Button></div>
            <AiErrorNotice error={runTest.error} onRetry={doTest} className="mt-3" />
            {test && (
              <div className="mt-4">
                <p className="font-semibold">Works on {Math.round(test.pass_rate * 100)}% of the questions where it applies</p>
                <ul className="mt-2 space-y-2">
                  {test.results.map((r, i) => (
                    <li key={i} className="flex gap-2 rounded-lg border border-line p-3 text-sm">
                      {r.works ? <CheckCircle2 className="h-4 w-4 shrink-0 text-success" aria-label="Works" /> : <XCircle className="h-4 w-4 shrink-0 text-danger" aria-label="Breaks" />}
                      <div><p className="font-medium">{r.question.text}</p><p className="text-muted">{r.applies ? r.working : 'Rule does not apply here.'}</p></div>
                    </li>
                  ))}
                </ul>
                <p className="mt-3 text-sm">{test.advice}</p>
                {test.step === 'shape' && <p className="mt-2 text-sm text-warning-ink">Not reliable yet: sharpen the rule with Mitra above and test again.</p>}
              </div>
            )}
          </CardBody>
        </Card>
      )}

      {step === 3 && (
        <Card><CardBody>
          <Switch checked={share} onChange={setShare} label="Share with other students" description="If it passes 80% or more, your card can join the shared shortcut library." />
          <div className="flex justify-end"><Button onClick={doLock} loading={lock.busy} leftIcon={<Lock className="h-4 w-4" />}>Lock as a revision card</Button></div>
          <AiErrorNotice error={lock.error} onRetry={doLock} className="mt-3" />
        </CardBody></Card>
      )}
      {card && (
        <Card><CardBody>
          <p className="mb-3 font-semibold text-success">Locked. It will come back in Revision AI.</p>
          <CheatCardView p={card.payload} />
          <Button className="mt-4" variant="outline" onClick={() => { setSession(null); setStep(0); }}>Start another</Button>
        </CardBody></Card>
      )}
    </div>
  );
}

function CardsPanel({ version }: { version: number }) {
  const cards = useAiQuery(() => aiService.coachCards(), `cards-${version}`);
  if (cards.loading) return <LoadingSkeleton variant="cards" />;
  if (cards.error) return <AiErrorNotice error={cards.error} onRetry={cards.reload} />;
  if (!cards.data?.length) return <p className="text-sm text-muted">No cards yet. Finish a coach session to lock your first rule.</p>;
  return <div className="grid gap-4 md:grid-cols-2">{cards.data.map((c) => <CheatCardView key={c.id} p={c.payload} />)}</div>;
}

function LibraryPanel() {
  const [topic, setTopic] = useState('');
  const list = useAiQuery(() => aiService.shortcuts(topic), `sc-${topic}`);
  return (
    <div>
      <input value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="Filter by topic" aria-label="Filter shortcuts"
        className="mb-4 w-full max-w-sm rounded-lg border border-line-strong bg-card px-3 py-2 text-sm focus:border-primary focus:outline-none" />
      {list.loading ? <LoadingSkeleton variant="cards" /> : list.error ? <AiErrorNotice error={list.error} onRetry={list.reload} /> : (
        <div className="grid gap-4 md:grid-cols-2">{(list.data ?? []).map((s) => <CheatCardView key={s.id} p={s.payload} />)}</div>
      )}
    </div>
  );
}

export function CoachPage() {
  useDocumentTitle('Cheat Code Coach');
  const [params, setParams] = useSearchParams();
  const t = params.get('tab');
  const tab: Tab = t === 'cards' || t === 'library' ? t : 'coach';
  const [version, setVersion] = useState(0);
  return (
    <div className="mx-auto max-w-5xl">
      <PageHeader title="Cheat Code Coach" description="Spot, shape, test and lock your own exam shortcuts." actions={<Badge tone="primary" icon={<Wand2 className="h-3 w-3" />}>Spot · Shape · Test · Lock</Badge>} />
      <Tabs ariaLabel="Coach" className="mb-5" value={tab} onChange={(v) => setParams(v === 'coach' ? {} : { tab: v })}
        items={[{ value: 'coach', label: 'Coach' }, { value: 'cards', label: 'My cards' }, { value: 'library', label: 'Shortcut library' }]} />
      {tab === 'coach' ? <CoachFlow onLocked={() => setVersion((v) => v + 1)} /> : tab === 'cards' ? <CardsPanel version={version} /> : <LibraryPanel />}
    </div>
  );
}
