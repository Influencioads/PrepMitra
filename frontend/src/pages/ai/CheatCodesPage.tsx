import { useEffect, useMemo, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Lock, LockOpen, RotateCcw, Search } from 'lucide-react';
import type { CheatCode, CheatCodeCatalogue, CheatCodeDrillResult } from '@prepmitra/shared';
import { Button, LoadingSkeleton, Mitra } from '@/components/ui';
import { AiErrorNotice, useAiAction, useAiQuery } from '@/components/ai/AiUi';
import { Chalkboard, CoachBubble, Eyebrow, HandLine, softCard } from '@/components/ai/Board';
import { aiService } from '@/services/aiService';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

const SUGGESTIONS = ['1.331', 'unit digit', 'LCM', 'some', 'CI'];

const matches = (c: CheatCode, q: string) => {
  const t = q.trim().toLowerCase();
  if (!t) return true;
  return [c.title, c.topic, c.trick, c.example, ...c.exams].some((x) => x.toLowerCase().includes(t));
};

function YourCode({ c, onPractise }: { c: CheatCode; onPractise: (id: string) => void }) {
  return (
    <button type="button" onClick={() => onPractise(c.id)}
      className={cn('flex items-center gap-3 rounded-xl p-3 text-left transition',
        c.unlocked ? 'border-[1.5px] border-ink bg-card hover:shadow-[3px_3px_0_#1c2321]' : 'border border-dashed border-line-strong bg-surface/70 hover:border-ink')}>
      <span className={cn('flex h-10 w-10 shrink-0 items-center justify-center rounded-full border-[1.5px]', c.unlocked ? 'border-ink bg-marigold' : 'border-subtle bg-card text-muted')}>
        {c.unlocked ? <LockOpen className="h-4 w-4" aria-hidden /> : <Lock className="h-4 w-4" aria-hidden />}
      </span>
      <span className="min-w-0">
        <span className="block text-sm font-semibold leading-snug">{c.title}</span>
        <span className={cn('block text-[11px] leading-snug', c.unlocked ? 'font-semibold text-secondary' : 'text-muted')}>
          {c.unlocked ? `Unlocked · ${c.topic}` : `Locked · drill 2 of ${c.drill_size || 3} to unlock`}
        </span>
      </span>
    </button>
  );
}

function FlipCard({ c, onPractise }: { c: CheatCode; onPractise: (id: string) => void }) {
  const [flipped, setFlipped] = useState(false);
  return (
    <div className="[perspective:1400px]">
      <div className={cn('grid transition-transform duration-500 [transform-style:preserve-3d] motion-reduce:transition-none', flipped && '[transform:rotateY(180deg)]')}>
        {/* front */}
        <article inert={flipped} aria-hidden={flipped} className="flex flex-col rounded-[18px] border-[1.5px] border-ink bg-card p-4 shadow-[4px_5px_0_#1c2321] [backface-visibility:hidden] [grid-area:1/1] sm:p-5">
          <div className="flex items-start justify-between gap-2">
            <Eyebrow tone="primary">{c.topic}</Eyebrow>
            <span className="shrink-0 rounded-full bg-secondary-soft px-2 py-0.5 text-[11px] font-semibold text-secondary">saves ~{c.saves_seconds}s</span>
          </div>
          <h3 className="mt-2 text-lg font-bold leading-snug">{c.title}{c.unlocked && <LockOpen className="ml-1.5 inline h-4 w-4 text-secondary" aria-label="Unlocked" />}</h3>
          <Eyebrow className="mt-3">The trick</Eyebrow>
          <p className="mt-0.5 font-hand text-lg leading-snug">{c.trick}</p>
          <Eyebrow className="mt-3">Worked example</Eyebrow>
          <p className="mt-0.5 rounded-lg bg-paper px-3 py-2 text-sm leading-relaxed">{c.example}</p>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {c.exams.map((e) => <span key={e} className="rounded-full bg-surface px-2 py-0.5 text-[11px] font-semibold">{e}</span>)}
          </div>
          <div className="mt-auto flex flex-wrap gap-2 pt-4">
            <button type="button" onClick={() => setFlipped(true)} className="h-9 rounded-full border-[1.5px] border-ink px-3.5 text-sm font-semibold hover:bg-surface">Flip · the trap</button>
            <Button size="sm" className="h-9 rounded-full" onClick={() => onPractise(c.id)}>Practise this code</Button>
          </div>
        </article>
        {/* back */}
        <article inert={!flipped} aria-hidden={!flipped} className="flex flex-col rounded-[18px] border-[3px] border-pen bg-paper p-4 shadow-[4px_5px_0_#1c2321] [backface-visibility:hidden] [grid-area:1/1] [transform:rotateY(180deg)] sm:p-5">
          <Eyebrow tone="pen">When not to use it</Eyebrow>
          <h3 className="mt-2 font-bold leading-snug">{c.title}</h3>
          <p className="mt-3 font-hand text-lg leading-snug text-pen">{c.trap}</p>
          <svg viewBox="0 0 100 6" className="mt-1 h-2 w-24" aria-hidden><path d="M1 4 Q 30 1 60 3 T 99 3" stroke="#d7263d" strokeWidth={2} fill="none" strokeLinecap="round" /></svg>
          <p className="mt-3 text-xs leading-relaxed text-muted">If the trap applies, solve it the long way. A code that doesn’t fit costs more time than it saves.</p>
          <div className="mt-auto pt-4">
            <button type="button" onClick={() => setFlipped(false)} className="inline-flex h-9 items-center gap-1.5 rounded-full border-[1.5px] border-ink px-3.5 text-sm font-semibold hover:bg-surface">
              <RotateCcw className="h-3.5 w-3.5" aria-hidden /> Flip back
            </button>
          </div>
        </article>
      </div>
    </div>
  );
}

function DrillPanel({ codeId, onUnlocked, onClose }: { codeId: string | null; onUnlocked: () => void; onClose: () => void }) {
  const drill = useAiQuery(() => (codeId ? aiService.cheatCodeDrill(codeId) : Promise.resolve(null)), `drill-${codeId ?? ''}`);
  const [answers, setAnswers] = useState<(string | null)[]>([]);
  const [result, setResult] = useState<CheatCodeDrillResult | null>(null);
  const check = useAiAction(aiService.checkCheatCodeDrill);
  useEffect(() => { setAnswers([]); setResult(null); check.setError(null); }, [codeId]); // eslint-disable-line react-hooks/exhaustive-deps
  const d = drill.data;

  const submit = async () => {
    if (!d || !codeId) return;
    const r = await check.run(codeId, d.questions.map((_, i) => answers[i] ?? null));
    if (r) { setResult(r); if (r.unlocked) onUnlocked(); }
  };

  return (
    <Chalkboard as="div" className="p-4 sm:p-5" ariaLabel="Practise a code">
      <span className="flex items-center gap-2"><Mitra size={24} /><Eyebrow tone="chalk">Mitra · AI drill</Eyebrow></span>
      {!codeId ? (
        <>
          <h2 className="mt-3 text-xl font-bold !text-chalk-text">Practise a code</h2>
          <p className="mt-2 font-hand text-lg leading-snug text-chalk-text/90">Pick any card and hit “Practise”. Three questions, one code, instant feedback. Get 2 right and it’s yours.</p>
        </>
      ) : drill.loading ? (
        <div className="mt-4 space-y-2" aria-busy><div className="h-4 w-2/3 rounded bg-white/15" /><div className="h-24 rounded bg-white/10" /></div>
      ) : drill.error ? (
        <div className="mt-3 rounded-lg bg-paper p-2 text-ink"><AiErrorNotice error={drill.error} onRetry={drill.reload} /></div>
      ) : d && (
        <>
          <h2 className="mt-3 text-lg font-bold leading-snug !text-chalk-text">{d.title}</h2>
          <ol className="mt-3 space-y-4">
            {d.questions.map((q, i) => {
              const res = result?.results[i];
              return (
                <li key={i} className="rounded-xl bg-white/[0.06] p-3">
                  <p className="text-sm font-semibold"><span className="font-hand text-marigold">Q{i + 1}.</span> {q.text}</p>
                  <div className="mt-2 grid gap-1.5" role="radiogroup" aria-label={`Question ${i + 1}`}>
                    {q.options.map((o) => {
                      const sel = answers[i] === o.key;
                      const right = res && res.answer === o.key;
                      return (
                        <button key={o.key} type="button" role="radio" aria-checked={sel} disabled={!!result}
                          onClick={() => setAnswers((a) => { const n = [...a]; n[i] = o.key; return n; })}
                          className={cn('flex items-center gap-2 rounded-lg border px-2.5 py-1.5 text-left text-sm',
                            right ? 'border-[#9be3b8] bg-[#9be3b8]/15' : res && sel ? 'border-[#ff9aa8] bg-[#ff9aa8]/15' : sel ? 'border-marigold bg-marigold/15' : 'border-white/25 enabled:hover:border-white/60')}>
                          <span className={cn('flex h-5 w-5 shrink-0 items-center justify-center rounded-full border text-[10px] font-bold', sel ? 'border-marigold bg-marigold text-ink' : 'border-white/50')}>{o.key}</span>
                          {o.text}
                        </button>
                      );
                    })}
                  </div>
                  {res && <p className={cn('mt-2 font-hand text-base leading-snug', res.correct ? 'text-[#9be3b8]' : 'text-[#ffb3bd]')}>{res.correct ? '✓ ' : `✗ Answer ${res.answer}. `}{res.explanation}</p>}
                </li>
              );
            })}
          </ol>
          <div className="mt-3 rounded-lg bg-paper p-0 text-ink empty:hidden"><AiErrorNotice error={check.error} onRetry={submit} /></div>
          {result ? (
            <div className="mt-4" aria-live="polite">
              <p className="font-hand text-2xl text-marigold">{result.right} of {result.of} right</p>
              <p className="mt-1 text-sm">{result.newly_unlocked ? 'Unlocked! This code is now yours.' : result.unlocked ? 'Already unlocked — nice revision.' : `Get 2 of ${result.of} to unlock. Try the drill again.`}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                <button type="button" onClick={() => { setResult(null); setAnswers([]); }} className="h-9 rounded-full border-[1.5px] border-chalk-text/70 px-3.5 text-sm font-semibold hover:bg-white/10">Try again</button>
                <button type="button" onClick={onClose} className="h-9 rounded-full px-3.5 text-sm font-semibold text-chalk-text/80 hover:bg-white/10">Close drill</button>
              </div>
            </div>
          ) : (
            <Button className="mt-4 w-full rounded-full" loading={check.busy} disabled={answers.filter(Boolean).length < d.questions.length} onClick={submit}>
              Check my answers
            </Button>
          )}
        </>
      )}
      <p className="mt-4 text-[11px] leading-snug text-chalk-text/70">Drill answers are checked by code. Mitra’s explanations are AI-generated — check with your teacher if unsure.</p>
    </Chalkboard>
  );
}

function coachLine(cat: CheatCodeCatalogue) {
  const next = cat.yours.find((c) => !c.unlocked) ?? cat.yours[0] ?? cat.items[0];
  if (!next) return null;
  return `Start with “${next.title}” — it alone saves about ${next.saves_seconds} seconds a question. Drill it once and it is yours.`;
}

export function CheatCodesPage() {
  useDocumentTitle('Cheat codes');
  const [params, setParams] = useSearchParams();
  const cat = useAiQuery(() => aiService.cheatCodes(), 'cheat-codes');
  const [q, setQ] = useState('');
  const [topic, setTopic] = useState<string | null>(null);
  const drillId = params.get('drill');
  const panel = useRef<HTMLDivElement>(null);
  const data = cat.data;

  const practise = (id: string) => {
    setParams((p) => { const n = new URLSearchParams(p); n.set('drill', id); return n; }, { replace: true });
    requestAnimationFrame(() => panel.current?.scrollIntoView?.({ behavior: 'smooth', block: 'start' }));
  };
  const closeDrill = () => setParams((p) => { const n = new URLSearchParams(p); n.delete('drill'); return n; }, { replace: true });

  const items = useMemo(() => (data?.items ?? []).filter((c) => (!topic || c.topic === topic) && matches(c, q)), [data, topic, q]);
  const suggestions = useMemo(() => SUGGESTIONS.filter((s) => data?.items.some((c) => matches(c, s))).slice(0, 3), [data]);

  if (cat.loading && !data) return <LoadingSkeleton variant="page" />;
  if (cat.error && !data) return <AiErrorNotice error={cat.error} onRetry={cat.reload} />;
  if (!data) return null;
  const coach = coachLine(data);

  return (
    <div className="min-w-0">
      <Chalkboard className="p-5 sm:p-7" ariaLabel="Cheat codes">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div className="min-w-0">
            <HandLine tone="chalk">exam-safe shortcuts —</HandLine>
            <h1 className="text-3xl font-extrabold !text-chalk-text sm:text-5xl">Cheat codes</h1>
            <p className="mt-2 max-w-xl text-sm text-chalk-text/85 sm:text-base">Elimination, approximation and unit-digit checks for every slow or wrong answer. Legal in every exam hall — no guessing, just less writing.</p>
          </div>
          {coach && <CoachBubble className="max-w-sm">{coach}</CoachBubble>}
        </div>
        <div className="mt-5 flex flex-col gap-3 md:flex-row md:items-center">
          <label className="relative min-w-0 flex-1">
            <span className="sr-only">Search cheat codes</span>
            <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" aria-hidden />
            <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search: 1.331, unit digit, LCM, 'some'…"
              className="h-12 w-full rounded-full border-[1.5px] border-ink bg-card pl-11 pr-4 text-sm text-ink placeholder:text-subtle focus:outline-none focus:ring-2 focus:ring-marigold" />
          </label>
          {suggestions.length > 0 && (
            <div className="flex flex-wrap items-center gap-2 text-sm">
              <span className="text-chalk-text/75">Try</span>
              {suggestions.map((s) => (
                <button key={s} type="button" onClick={() => setQ(s)} className="rounded-full border border-dashed border-marigold/70 px-3 py-1 font-hand text-marigold hover:bg-white/10">{s}</button>
              ))}
            </div>
          )}
        </div>
        <div className="mt-4 flex flex-wrap gap-2" role="group" aria-label="Topics">
          {[{ name: null as string | null, count: data.total }, ...data.topics.map((t) => ({ name: t.name as string | null, count: t.count }))].map((t) => (
            <button key={t.name ?? 'all'} type="button" aria-pressed={topic === t.name} onClick={() => setTopic(t.name)}
              className={cn('rounded-full border px-3.5 py-1.5 text-sm font-semibold transition', topic === t.name ? 'border-marigold bg-marigold text-ink' : 'border-white/35 text-chalk-text hover:bg-white/10')}>
              {t.name ?? 'All'} <span className="opacity-75">{t.count}</span>
            </button>
          ))}
        </div>
      </Chalkboard>

      <div className="mt-6 grid gap-6 lg:grid-cols-[minmax(0,1fr)_300px]">
        <div className="min-w-0 space-y-6">
          {data.yours.length > 0 && (
            <section className={cn(softCard, 'p-4 sm:p-5')} aria-labelledby="your-codes">
              <HandLine tone="pen">picked from your mock reports —</HandLine>
              <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
                <h2 id="your-codes" className="text-xl font-bold">Your codes</h2>
                <p className="text-xs text-muted">Locked codes unlock when you score 2 of 3 in their drill.</p>
              </div>
              <div className="mt-4 grid gap-2.5 sm:grid-cols-2 xl:grid-cols-3">
                {data.yours.map((c) => <YourCode key={c.id} c={c} onPractise={practise} />)}
              </div>
            </section>
          )}

          <section aria-labelledby="all-codes">
            <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
              <h2 id="all-codes" className="text-xl font-bold">{items.length} code{items.length === 1 ? '' : 's'}</h2>
              <p className="text-xs text-muted">Every example is worked out — check it yourself.</p>
            </div>
            {items.length === 0 ? (
              <p className="mt-4 rounded-xl border border-dashed border-line-strong p-6 text-center text-sm text-muted">No code matches “{q}”. Try another word.</p>
            ) : (
              <div className="mt-4 grid gap-5 sm:grid-cols-2">
                {items.map((c) => <FlipCard key={c.id} c={c} onPractise={practise} />)}
              </div>
            )}
          </section>
        </div>

        <div ref={panel} className="scroll-mt-20 space-y-4 lg:sticky lg:top-20 lg:self-start">
          <div className="rounded-[16px] bg-chalk-deep p-4 text-chalk-text">
            <Eyebrow tone="chalk">Codes unlocked</Eyebrow>
            <p className="mt-1 font-display text-3xl font-extrabold">{data.unlocked_count} <span className="text-base font-semibold text-chalk-text/80">of {data.total}</span></p>
            <div className="mt-2 h-2 rounded-full bg-white/15" aria-hidden><div className="h-full rounded-full bg-marigold" style={{ width: `${data.total ? (data.unlocked_count / data.total) * 100 : 0}%` }} /></div>
          </div>
          <DrillPanel codeId={drillId} onUnlocked={cat.reload} onClose={closeDrill} />
        </div>
      </div>
    </div>
  );
}
