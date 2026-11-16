import { useState } from 'react';
import { Check, RotateCcw } from 'lucide-react';
import type { TeachConcept, TeachResult } from '@prepmitra/shared';
import { Button, LoadingSkeleton } from '@/components/ui';
import { AiErrorNotice, useAiAction, useAiQuery } from '@/components/ai/AiUi';
import { Chalkboard, CoachBubble, Eyebrow, HandLine, Ring, SeatingDiagram, softCard } from '@/components/ai/Board';
import { aiService } from '@/services/aiService';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

/** "All A are B; some B are C": A sits inside B, C overlaps only the part of B outside A. */
function VennAllSome() {
  return (
    <svg viewBox="0 0 220 150" className="h-auto w-full max-w-[260px]" role="img" aria-label="Venn diagram: A inside B, C overlapping B outside A — case 1, no A is C">
      <g fill="none" stroke="#f5f3ea" strokeWidth={2.2}>
        <circle cx={80} cy={70} r={50} />
        <circle cx={70} cy={72} r={22} />
        <circle cx={140} cy={70} r={28} />
      </g>
      <g fill="#f5f3ea" fontFamily="var(--font-hand)" fontSize={15} textAnchor="middle">
        <text x={70} y={77}>A</text>
        <text x={110} y={28}>B</text>
        <text x={146} y={76}>C</text>
        <text x={80} y={142} fontSize={12} opacity={0.85}>case 1 · no A is C</text>
      </g>
    </svg>
  );
}

function ConceptDiagram({ kind }: { kind: string }) {
  if (kind === 'venn-all-some') return <VennAllSome />;
  if (kind === 'circle-6') return <div className="w-full max-w-[220px]"><SeatingDiagram seats={6} /></div>;
  return null;
}

function ScoreBar({ label, value }: { label: string; value: number | null }) {
  return (
    <div>
      <div className="flex justify-between text-sm font-semibold"><span>{label}</span><span>{value == null ? '–' : `${value}/10`}</span></div>
      <div className="mt-1 h-2 rounded-full bg-surface" aria-hidden>
        {value != null && <div className={cn('h-full rounded-full', value >= 7 ? 'bg-secondary' : value >= 4 ? 'bg-accent' : 'bg-pen')} style={{ width: `${value * 10}%` }} />}
      </div>
    </div>
  );
}

function Lesson({ concept }: { concept: TeachConcept }) {
  const [round, setRound] = useState(0);
  const [results, setResults] = useState<TeachResult[]>([]);
  const [text, setText] = useState('');
  const answer = useAiAction(aiService.teachAnswer);
  const total = concept.rounds.length;
  const cur = concept.rounds[round];
  const answered = results[round];
  const latest = results[results.length - 1];
  const done = !!latest?.done || results.length >= total;

  const teach = async (body: { choice?: string; text?: string }) => {
    if (answer.busy || answered) return;
    const r = await answer.run(concept.id, { round, ...body });
    if (r) { setResults((x) => { const n = [...x]; n[round] = r; return n; }); setText(''); }
  };
  const restart = () => { setRound(0); setResults([]); setText(''); answer.setError(null); };

  return (
    <>
      <div className="mb-5 flex flex-wrap gap-2" role="list" aria-label="Rounds">
        {concept.rounds.map((_, i) => {
          const r = results[i];
          const on = i === round;
          return (
            <span key={i} role="listitem" aria-current={on ? 'step' : undefined}
              className={cn('inline-flex items-center gap-2 rounded-full border-[1.5px] px-3.5 py-1.5 text-sm font-semibold',
                on ? 'border-ink bg-primary-soft' : r ? 'border-secondary bg-secondary-soft text-secondary' : 'border-line-strong bg-card text-muted')}>
              {r ? <Check className="h-3.5 w-3.5" aria-hidden /> : <span className={cn('h-2 w-2 rounded-full', on ? 'bg-accent' : 'bg-line-strong')} aria-hidden />}
              Round {i + 1}{r ? ` · ${r.total}/${r.max_total}` : ''}
            </span>
          );
        })}
      </div>

      <div className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_240px]">
        <div className="min-w-0 space-y-5">
          <Chalkboard className="p-4 sm:p-6" ariaLabel="Today's concept">
            <div className="grid gap-6 md:grid-cols-2">
              <div className="min-w-0">
                <Eyebrow tone="chalk">Today’s concept · {concept.topic}</Eyebrow>
                <div className="mt-2 space-y-0.5 font-hand text-xl leading-snug sm:text-2xl">{concept.board.map((b) => <p key={b}>{b}</p>)}</div>
                <p className="mt-3 border-t border-dashed border-white/30 pt-3 font-hand text-lg sm:text-xl">{concept.ask}</p>
                <div className="mt-4 flex justify-center md:justify-start"><ConceptDiagram kind={concept.diagram} /></div>
              </div>
              <div className="min-w-0 md:border-l md:border-white/15 md:pl-6">
                <Eyebrow tone="chalk">Your lesson so far · written by you</Eyebrow>
                {results.length === 0 ? (
                  <p className="mt-2 font-hand text-lg text-chalk-text/70">(empty board — pick an explanation below and it gets written here)</p>
                ) : (
                  <ol className="mt-2 space-y-3">
                    {results.map((r, i) => r && (
                      <li key={i} className="font-hand text-base leading-snug sm:text-lg">
                        <span className="text-marigold">{i + 1}.</span> {r.written}
                        <span className={cn('ml-2 text-sm', r.good ? 'text-[#9be3b8]' : 'text-[#ff9aa8]')}>{r.good ? '✓' : '✗'}</span>
                      </li>
                    ))}
                  </ol>
                )}
              </div>
            </div>
          </Chalkboard>

          {cur && (
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start">
              <div className="flex shrink-0 flex-row items-center gap-3 sm:w-28 sm:flex-col sm:gap-1">
                <span className="flex h-16 w-16 items-center justify-center rounded-full border-[1.5px] border-ink bg-secondary-soft font-display text-xl font-bold text-secondary sm:h-20 sm:w-20" aria-hidden>CH</span>
                <div className="sm:text-center">
                  <p className="font-semibold">Chotu</p>
                  <span className="rounded bg-secondary-soft px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-secondary">AI student</span>
                </div>
              </div>
              <div className="min-w-0 flex-1 rounded-[4px_16px_16px_16px] border-[1.5px] border-ink bg-ruled p-4 shadow-[3px_4px_0_#1c2321]" aria-live="polite">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <Eyebrow>Chotu asks · {cur.kind}</Eyebrow>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-secondary">{answered ? (answered.good ? 'happy' : 'confused') : cur.mood}</span>
                </div>
                <p className="mt-1.5 font-semibold leading-snug">{answered ? answered.chotu_reply : cur.chotu}</p>
              </div>
            </div>
          )}

          <section className="rounded-[18px] border-[1.5px] border-ink bg-card p-4 shadow-[4px_5px_0_#1c2321] sm:p-5" aria-labelledby="explain">
            {done ? (
              <div className="flex flex-col items-start gap-3">
                <h2 id="explain" className="text-lg font-bold">Lesson taught — {results.reduce((s, r) => s + (r?.total ?? 0), 0)} of {results.reduce((s, r) => s + (r?.max_total ?? 0), 0)} across {results.length} rounds</h2>
                <p className="text-sm text-muted">Read Mitra’s margin notes, then teach it again to beat your score.</p>
                <Button variant="outline" leftIcon={<RotateCcw className="h-4 w-4" />} onClick={restart}>Teach it again</Button>
              </div>
            ) : cur && (
              <>
                <div className="flex flex-wrap items-baseline justify-between gap-2">
                  <h2 id="explain" className="text-lg font-bold">Your explanation · round {round + 1} of {total}</h2>
                  <span className="text-xs font-semibold text-muted">Pick one, or write your own</span>
                </div>
                <div className="mt-3 space-y-2.5">
                  {cur.options.map((o) => {
                    const picked = answered?.written === o.text;
                    return (
                      <button key={o.key} type="button" onClick={() => teach({ choice: o.key })} disabled={!!answered || answer.busy}
                        className={cn('flex w-full items-start gap-3 rounded-xl border px-3 py-3 text-left text-sm transition disabled:cursor-default',
                          picked ? (answered.good ? 'border-secondary bg-secondary-soft' : 'border-pen bg-danger-soft') : 'border-line-strong bg-paper enabled:hover:border-ink')}>
                        <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full border-[1.5px] border-ink text-xs font-bold">{o.key}</span>
                        <span className="pt-0.5">{o.text}</span>
                      </button>
                    );
                  })}
                </div>
                <form className="mt-4" onSubmit={(e) => { e.preventDefault(); if (text.trim().length >= 3) void teach({ text: text.trim() }); }}>
                  <label htmlFor="teach-own" className="text-sm font-semibold">Or explain in your own words</label>
                  <div className="mt-1.5 flex flex-col gap-2 sm:flex-row">
                    <input id="teach-own" value={text} onChange={(e) => setText(e.target.value)} disabled={!!answered} maxLength={600}
                      placeholder="e.g. Draw B big, A inside it, C on the other side…" className="h-11 min-w-0 flex-1 rounded-lg border border-line-strong bg-paper px-3 text-sm focus:border-primary focus:outline-none" />
                    <Button type="submit" loading={answer.busy} disabled={!!answered || text.trim().length < 3} className="h-11 bg-secondary hover:bg-secondary-hover border-[1.5px] border-ink shadow-[3px_3px_0_#1c2321]">Teach this</Button>
                  </div>
                </form>
                <AiErrorNotice error={answer.error} className="mt-3" />
                {answered && round < total - 1 && (
                  <div className="mt-4 flex justify-end"><Button onClick={() => setRound((r) => r + 1)}>Next round →</Button></div>
                )}
              </>
            )}
          </section>
        </div>

        <div className="space-y-4">
          <section className={cn(softCard, 'p-4')} aria-label="Teaching score">
            <div className="flex items-center gap-3">
              <Ring value={latest ? latest.total : null} max={latest?.max_total ?? 30} size={84} />
              <div>
                <h2 className="font-bold">Teaching score</h2>
                <p className="text-xs text-muted">{latest ? `Round ${latest.round + 1} of ${total}` : 'Updates after each answer'}</p>
              </div>
            </div>
            <div className="mt-4 space-y-3">
              <ScoreBar label="Clarity" value={latest?.scores.clarity ?? null} />
              <ScoreBar label="Correctness" value={latest?.scores.correctness ?? null} />
              <ScoreBar label="Examples" value={latest?.scores.examples ?? null} />
            </div>
            <p className="mt-3 text-[11px] leading-snug text-muted">Scores come from a fixed rubric calculated by code. Mitra only writes the notes.</p>
          </section>
          <section className="rounded-[14px] border border-line bg-notebook p-4 pl-10 [--margin-x:22px]" aria-label="Mitra's margin notes">
            <Eyebrow>Mitra’s margin notes · AI</Eyebrow>
            <p className="mt-0.5 text-[11px] text-muted">AI-generated — check with your teacher if unsure.</p>
            {results.length === 0 ? (
              <p className="mt-2 font-hand text-lg leading-snug text-muted">Red pen is ready. Teach your first answer.</p>
            ) : (
              <ul className="mt-2 space-y-2">
                {results.map((r, i) => r && <li key={i} className="font-hand text-base leading-snug text-pen sm:text-lg"><b>R{i + 1}:</b> {r.note}</li>)}
              </ul>
            )}
          </section>
          {cur && !done && <CoachBubble>{cur.coach_hint}</CoachBubble>}
        </div>
      </div>
    </>
  );
}

export function TeachBackPage() {
  useDocumentTitle('AI student');
  const list = useAiQuery(() => aiService.teachConcepts(), 'teach-concepts');
  const [id, setId] = useState<string | null>(null);
  const conceptId = id ?? list.data?.[0]?.id ?? null;
  const concept = useAiQuery(() => (conceptId ? aiService.teachConcept(conceptId) : Promise.resolve(null)), `teach-${conceptId ?? ''}`);

  return (
    <div className="min-w-0">
      <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
        <div className="min-w-0">
          <HandLine tone="pen">teach-back — new</HandLine>
          <h1 className="max-w-2xl text-2xl font-bold leading-tight tracking-tight sm:text-4xl">Teaching is the fastest way to learn — explain it to Chotu</h1>
          <p className="mt-2 max-w-2xl text-sm text-muted sm:text-base">Chotu is an AI junior aspirant. He asks the questions an examiner would. Answer three of them, and Mitra marks how well you taught.</p>
        </div>
        <div className="max-w-xs shrink-0 rotate-[-1.5deg] bg-sticky-yellow p-4 shadow-sticky md:w-56">
          <p className="font-hand text-lg">why teach-back?</p>
          <p className="mt-1 text-sm leading-snug">If you can explain it simply, you can solve it under pressure. Chotu finds the gaps before the exam does.</p>
        </div>
      </div>

      {(list.data?.length ?? 0) > 1 && (
        <div className="mt-5 flex flex-wrap gap-2" role="group" aria-label="Pick a concept">
          {list.data!.map((c) => (
            <button key={c.id} type="button" aria-pressed={c.id === conceptId} onClick={() => setId(c.id)}
              className={cn('rounded-full border px-3.5 py-1.5 text-sm font-semibold', c.id === conceptId ? 'border-ink bg-ink text-white' : 'border-line-strong bg-card hover:border-ink')}>
              {c.topic}
            </button>
          ))}
        </div>
      )}

      <div className="mt-5">
        {list.loading || concept.loading ? <LoadingSkeleton variant="page" /> : list.error ? <AiErrorNotice error={list.error} onRetry={list.reload} />
          : concept.error ? <AiErrorNotice error={concept.error} onRetry={concept.reload} />
            : concept.data ? <Lesson key={concept.data.id} concept={concept.data} />
              : <p className="text-sm text-muted">No concepts to teach yet.</p>}
      </div>
    </div>
  );
}
