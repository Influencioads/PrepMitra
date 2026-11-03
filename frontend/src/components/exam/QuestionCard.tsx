import type { Answer, Question } from '@prepmitra/shared';
import { numericAnswerSchema } from '@prepmitra/shared';
import { Badge } from '@/components/ui';
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
}

const typeKey = { single: 'typeSingle', multiple: 'typeMultiple', numeric: 'typeNumeric' } as const;

export function QuestionCard({ question, number, total, sectionName, marks, negativeMarks, answer, onToggleOption, onNumericChange, lang }: QuestionCardProps) {
  const t = useT(examMessages);
  const selected = answer?.selectedOptionIds ?? [];
  const multiple = question.type === 'multiple';
  const numeric = answer?.numericValue ?? '';
  const numericInvalid = numeric !== '' && !numericAnswerSchema.safeParse(numeric).success;
  const noNegative = question.type !== 'single' || negativeMarks === 0;

  return (
    <article aria-labelledby="question-heading">
      <div className="flex flex-wrap items-center gap-2 border-b border-line pb-3">
        <h2 id="question-heading" className="text-base font-semibold">
          {t('questionOf', { n: number })} <span className="font-normal text-muted">{t('ofTotal', { total })}</span>
        </h2>
        <Badge tone="primary">{t(typeKey[question.type])}</Badge>
        <span className="text-xs text-muted">{sectionName}</span>
        <span className="ml-auto text-xs text-muted">
          <span className="font-semibold text-success">+{marks}</span>
          {' / '}
          <span className="font-semibold text-danger">{noNegative ? '0' : `−${negativeMarks}`}</span>
        </span>
      </div>

      <p className="mt-4 whitespace-pre-line text-base leading-relaxed text-ink sm:text-lg" lang={lang}>
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
              'mt-1.5 h-12 w-full rounded-lg border bg-card px-4 text-lg font-semibold tabular-nums focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/30',
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
                  isOn ? 'border-primary bg-primary-soft' : 'border-line bg-card hover:border-line-strong hover:bg-stone-50',
                )}
              >
                <span
                  className={cn(
                    'flex h-7 w-7 shrink-0 items-center justify-center border-2 text-xs font-bold',
                    multiple ? 'rounded-md' : 'rounded-full',
                    isOn ? 'border-primary bg-primary text-white' : 'border-line-strong text-muted',
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
    </article>
  );
}
