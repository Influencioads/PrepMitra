import { useEffect, useState, type ReactNode } from 'react';
import type { ExamSection, PaletteStatus, PaperQuestion, QuestionState } from '@prepmitra/shared';
import { answeredCount, countPaletteStatuses, getPaletteStatus, paletteColors } from '@prepmitra/shared';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { useContentT } from '@/i18n/content';
import { examMessages } from '@/i18n/messages/exam';

/** Legend order used by real CBT screens. */
const ORDER: PaletteStatus[] = ['answered', 'not-answered', 'not-visited', 'marked', 'answered-marked'];

const statusKey = {
  'not-visited': 'statusNotVisited',
  'not-answered': 'statusNotAnswered',
  answered: 'statusAnswered',
  marked: 'statusMarked',
  'answered-marked': 'statusAnsweredMarked',
} as const satisfies Record<PaletteStatus, keyof typeof examMessages.en>;

export const legendKey = {
  'not-visited': 'legendNotVisited',
  'not-answered': 'legendNotAnswered',
  answered: 'legendAnswered',
  marked: 'legendMarked',
  'answered-marked': 'legendAnsweredMarked',
} as const satisfies Record<PaletteStatus, keyof typeof examMessages.en>;

/** One palette tile: squares for answered / not answered / not visited, circles for marked. */
export function PaletteSwatch({ status, children, className }: { status: PaletteStatus; children?: ReactNode; className?: string }) {
  const c = paletteColors[status];
  return (
    <span
      className={cn('relative inline-flex items-center justify-center border text-xs font-semibold', status === 'marked' || status === 'answered-marked' ? 'rounded-full' : 'rounded-lg', className)}
      style={{ background: c.bg, color: c.fg, borderColor: c.border }}
    >
      {children}
      {status === 'answered-marked' && <span className="absolute -bottom-0.5 -right-0.5 h-3 w-3 rounded-full border-2 border-white bg-[#15803D]" aria-hidden />}
    </span>
  );
}

export function PaletteLegend({ counts }: { counts?: Record<PaletteStatus, number> }) {
  const t = useT(examMessages);
  return (
    <ul className="grid grid-cols-2 gap-x-3 gap-y-2.5 text-xs">
      {ORDER.map((s) => (
        <li key={s} className={cn('flex items-center gap-2', s === 'answered-marked' && 'col-span-2')}>
          <PaletteSwatch status={s} className="h-7 w-7 shrink-0">{counts ? counts[s] : ''}</PaletteSwatch>
          <span className="leading-tight text-muted">{t(legendKey[s])}</span>
        </li>
      ))}
    </ul>
  );
}

export interface QuestionPaletteProps {
  paper: PaperQuestion[];
  states: Record<string, QuestionState>;
  sections: ExamSection[];
  currentIndex: number;
  onSelect: (index: number) => void;
}

/**
 * CBT question palette: legend with counts, a section switcher, and the numbered tiles of one
 * section (the section of the current question unless the candidate picks another to look at).
 */
export function QuestionPalette({ paper, states, sections, currentIndex, onSelect }: QuestionPaletteProps) {
  const t = useT(examMessages);
  const ct = useContentT();
  const currentSection = paper[currentIndex]?.sectionId;
  const [viewId, setViewId] = useState(currentSection);
  useEffect(() => setViewId(currentSection), [currentSection]);

  const present = sections.filter((s) => paper.some((p) => p.sectionId === s.id));
  const view = present.find((s) => s.id === viewId) ?? present[0];
  const items = paper.map((p, i) => ({ p, i })).filter(({ p }) => p.sectionId === view?.id);
  const counts = countPaletteStatuses(paper.map((p) => p.questionId), states);

  return (
    <div className="space-y-5">
      <PaletteLegend counts={counts} />

      {present.length > 1 && (
        <div role="group" aria-label={t('paletteSections')} className="flex flex-wrap gap-1.5 border-t border-line pt-4">
          {present.map((s) => {
            const ids = paper.filter((p) => p.sectionId === s.id).map((p) => p.questionId);
            const selected = s.id === view?.id;
            return (
              <button
                key={s.id}
                type="button"
                aria-pressed={selected}
                onClick={() => setViewId(s.id)}
                className={cn(
                  'rounded-full border px-3 py-1 text-xs font-medium transition-colors',
                  selected ? 'border-secondary bg-secondary text-white' : 'border-line text-muted hover:border-secondary/40 hover:text-ink',
                )}
              >
                {ct(s.name)} <span className={selected ? 'text-white/75' : 'text-subtle'}>{answeredCount(ids, states)}/{ids.length}</span>
              </button>
            );
          })}
        </div>
      )}

      {view && (
        <section aria-label={t('paletteSectionLabel', { section: ct(view.name) })}>
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted">{t('sectionPalette', { section: ct(view.name) })}</h3>
          <div className="grid grid-cols-5 gap-2.5">
            {items.map(({ p, i }) => {
              const status = getPaletteStatus(states[p.questionId]);
              const current = i === currentIndex;
              return (
                <button
                  key={p.questionId}
                  type="button"
                  onClick={() => onSelect(i)}
                  aria-label={t('paletteQuestionLabel', { n: i + 1, status: t(statusKey[status]) })}
                  aria-current={current ? 'step' : undefined}
                  data-status={status}
                  className={cn('rounded-lg transition-transform hover:scale-105 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-secondary', current && 'ring-2 ring-[#f26b1d] ring-offset-2')}
                >
                  <PaletteSwatch status={status} className="h-10 w-full min-w-10 text-sm">{i + 1}</PaletteSwatch>
                </button>
              );
            })}
          </div>
        </section>
      )}
    </div>
  );
}
