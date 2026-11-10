import type { Answer, Question } from '@prepmitra/shared';
import { numericAnswerSchema } from '@prepmitra/shared';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { examMessages } from '@/i18n/messages/exam';


export interface QuestionCardProps {
  question: Question;
  number: number;
  total: number;
  sectionName: string;
  marks: number;
  negativeMarks: number;
  answer?: Answer;
  onToggleOption: (optionId: string) => void;
  onNumericChange: (value: string) => void;
  lang?: string;
  /** The shown answer differs from the saved one (real CBT: saved only on Save & Next). */
  unsaved?: boolean;
}

const typeKey = { single: 'typeSingle', multiple: 'typeMultiple', numeric: 'typeNumeric' } as const;

export function QuestionCard({ question, number, total, sectionName, marks, negativeMarks, answer, onToggleOption, onNumericChange, lang, unsaved }: QuestionCardProps) {
  const t = useT(examMessages);
  const selected = answer?.selectedOptionIds ?? [];
  const multiple = question.type === 'multiple';
  const numeric = answer?.numericValue ?? '';
  const numericInvalid = numeric !== '' && !numericAnswerSchema.safeParse(numeric).success;
  const noNegative = question.type !== 'single' || negativeMarks === 0;

  return (
    <article aria-labelledby="question-heading">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-2 border-b border-line pb-4">
        <h2 id="question-heading" className="text-lg font-semibold">
          {t('questionOf', { n: number })} <span className="text-sm font-normal text-muted">{t('ofTotal', { total })}</span>
        </h2>
        <span className="rounded-full bg-secondary-soft px-2.5 py-0.5 text-xs font-medium text-secondary">{t(typeKey[question.type])}</span>
        <span className="hidden text-xs text-muted sm:inline">{sectionName}</span>
        <span className="ml-auto flex items-center gap-1.5 text-xs font-semibold tabular-nums">
          <span className="rounded-md bg-success-soft px-2 py-0.5 text-success">+{marks}</span>
          <span className="rounded-md bg-danger-soft px-2 py-0.5 text-danger">{noNegative ? '0' : `−${negativeMarks}`}</span>
        </span>
      </div>

      <p className="mt-5 whitespace-pre-line text-base leading-relaxed text-ink sm:text-lg" lang={lang}>
        {question.text}
      </p>
      {multiple && <p className="mt-2 text-sm text-muted">{t('multipleHint')}</p>}

      {question.type === 'numeric' ? (
        <div className="mt-6 max-w-xs">
          <label htmlFor="numeric-answer" className="block text-sm font-medium">{t('yourAnswer')}</label>
          <input
            id="numeric-answer"
            inputMode="decimal"
            autoComplete="off"
            value={numeric}
            onChange={(e) => onNumericChange(e.target.value.replace(/[^\d.-]/g, ''))}
            aria-invalid={numericInvalid || undefined}
            aria-describedby="numeric-help"
            placeholder={t('typeNumber')}
            className={cn(
              'mt-1.5 h-12 w-full rounded-xl border bg-card px-4 text-lg font-semibold tabular-nums focus:border-secondary focus:outline-none focus:ring-2 focus:ring-secondary/25',
              numericInvalid ? 'border-danger' : 'border-line-strong',
            )}
          />
          <p id="numeric-help" className={cn('mt-1.5 text-xs', numericInvalid ? 'text-danger' : 'text-muted')}>
            {numericInvalid ? t('numericInvalid') : t('numericHelp')}
          </p>
        </div>
      ) : (
        <div className="mt-6 space-y-3" role={multiple ? 'group' : 'radiogroup'} aria-labelledby="question-heading">
          {question.options?.map((o, i) => {
            const isOn = selected.includes(o.id);
            return (
              <button
                key={o.id}
                type="button"
                role={multiple ? 'checkbox' : 'radio'}
                aria-checked={isOn}
                onClick={() => onToggleOption(o.id)}
                className={cn(
                  'flex w-full items-start gap-3 rounded-xl border-2 px-4 py-3.5 text-left text-sm transition-colors sm:text-base',
                  isOn ? 'border-secondary bg-secondary-soft' : 'border-line bg-card hover:border-secondary/30 hover:bg-background',
                )}
              >
                <span
                  className={cn(
                    'flex h-7 w-7 shrink-0 items-center justify-center border-2 text-xs font-bold',
                    multiple ? 'rounded-md' : 'rounded-full',
                    isOn ? 'border-secondary bg-secondary text-white' : 'border-line-strong text-muted',
                  )}
                  aria-hidden
                >
                  {String.fromCharCode(65 + i)}
                </span>
                <span className="pt-0.5" lang={lang}>{o.text}</span>
              </button>
            );
          })}
        </div>
      )}
      {unsaved && (
        <p className="mt-4 rounded-lg bg-warning-soft px-3 py-2 text-xs font-medium text-warning-ink" role="status">{t('unsavedHint')}</p>
      )}
    </article>
  );
}
