import type { ReactNode } from 'react';
import type { ExamSection, PaletteStatus, PaperQuestion, QuestionState } from '@prepmitra/shared';
import { countPaletteStatuses, getPaletteStatus, paletteColors } from '@prepmitra/shared';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { examMessages } from '@/i18n/messages/exam';


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

export function PaletteSwatch({ status, children, className }: { status: PaletteStatus; children?: ReactNode; className?: string }) {
  const c = paletteColors[status];
  return (
    <span
      className={cn('relative inline-flex items-center justify-center border text-xs font-semibold', status === 'marked' || status === 'answered-marked' ? 'rounded-full' : 'rounded-md', className)}
      style={{ background: c.bg, color: c.fg, borderColor: c.border }}
    >
      {children}
      {status === 'answered-marked' && <span className="absolute -bottom-0.5 -right-0.5 h-2.5 w-2.5 rounded-full border-2 border-white bg-success" aria-hidden />}
    </span>
  );
}

export function PaletteLegend({ counts }: { counts?: Record<PaletteStatus, number> }) {
  const t = useT(examMessages);
  return (
    <ul className="grid grid-cols-2 gap-x-3 gap-y-2 text-xs">
      {ORDER.map((s) => (
        <li key={s} className={cn('flex items-center gap-2', s === 'answered-marked' && 'col-span-2')}>
          <PaletteSwatch status={s} className="h-6 w-6">{counts ? counts[s] : ''}</PaletteSwatch>
          <span className="text-muted">{t(legendKey[s])}</span>
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

/** CBT question palette grouped by section, with the five standard statuses. */
export function QuestionPalette({ paper, states, sections, currentIndex, onSelect }: QuestionPaletteProps) {
  const t = useT(examMessages);
  const counts = countPaletteStatuses(paper.map((p) => p.questionId), states);
  return (
    <div className="space-y-5">
      <PaletteLegend counts={counts} />
      {sections.map((sec) => {
        const items = paper.map((p, i) => ({ p, i })).filter(({ p }) => p.sectionId === sec.id);
        if (!items.length) return null;
        return (
          <section key={sec.id} aria-label={t('paletteSectionLabel', { section: sec.name })}>
            <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted">{sec.name}</h3>
            <div className="grid grid-cols-5 gap-2">
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
                    className={cn('rounded-md transition-transform hover:scale-105', current && 'ring-2 ring-ink ring-offset-2')}
                  >
                    <PaletteSwatch status={status} className="h-10 w-full min-w-10 text-sm">{i + 1}</PaletteSwatch>
                  </button>
                );
              })}
            </div>
          </section>
        );
      })}
    </div>
  );
}
