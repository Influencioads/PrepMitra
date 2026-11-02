import { useState } from 'react';
import { Check } from 'lucide-react';
import type { LanguageCode, Question } from '@prepmitra/shared';
import { LANGUAGES } from '@prepmitra/shared';
import { Badge, Tabs } from '@/components/ui';
import { cn } from '@/utils/cn';
import { TYPE_LABELS, languageLabel } from './labels';

/** Read-only question view with every available translation. */
export function QuestionPreview({ question, compact }: { question: Question; compact?: boolean }) {
  const langs = ['en', ...Object.keys(question.translations ?? {})] as (LanguageCode | 'en')[];
  const [lang, setLang] = useState<string>('en');
  const tr = lang === 'en' ? undefined : question.translations?.[lang as LanguageCode];
  const text = tr?.text ?? question.text;
  const rtl = LANGUAGES.find((l) => l.code === lang)?.rtl;

  return (
    <div className="space-y-3">
      {langs.length > 1 && (
        <Tabs
          ariaLabel="Question language"
          value={lang}
          onChange={setLang}
          items={langs.map((l) => ({ value: l, label: languageLabel(l) }))}
        />
      )}
      {!compact && (
        <div className="flex flex-wrap gap-1.5">
          <Badge tone="primary">{TYPE_LABELS[question.type]}</Badge>
          <Badge>{question.difficulty}</Badge>
          <Badge>{question.topic}</Badge>
          <Badge tone={langs.length > 1 ? 'info' : 'neutral'}>{langs.length} language{langs.length > 1 ? 's' : ''}</Badge>
        </div>
      )}
      <p className="whitespace-pre-line text-sm leading-relaxed text-ink" dir={rtl ? 'rtl' : undefined}>{text}</p>
      {question.type === 'numeric' ? (
        <p className="rounded-lg bg-success-soft px-3 py-2 text-sm text-green-800">
          Answer: <strong>{question.correctNumeric}</strong>
          {question.tolerance ? ` (± ${question.tolerance})` : ''}
        </p>
      ) : (
        <ol className="space-y-1.5" aria-label="Options">
          {question.options?.map((o, i) => {
            const correct = question.correctOptionIds?.includes(o.id);
            return (
              <li
                key={o.id}
                className={cn('flex items-start gap-2 rounded-lg border px-3 py-2 text-sm', correct ? 'border-green-300 bg-success-soft' : 'border-line')}
              >
                <span className="font-semibold text-muted">{String.fromCharCode(65 + i)}.</span>
                <span className="flex-1" dir={rtl ? 'rtl' : undefined}>{tr?.options?.[i] ?? o.text}</span>
                {correct && (
                  <span className="inline-flex items-center gap-1 text-xs font-semibold text-green-700">
                    <Check className="h-3.5 w-3.5" aria-hidden /> Correct
                  </span>
                )}
              </li>
            );
          })}
        </ol>
      )}
      <div className="rounded-lg bg-stone-50 px-3 py-2 text-sm">
        <p className="font-medium text-ink">Explanation</p>
        <p className="mt-0.5 text-muted">{question.explanation}</p>
        {question.shortcut && !compact && (
          <p className="mt-2 text-muted">
            <span className="font-medium text-ink">Shortcut: </span>
            {question.shortcut}
          </p>
        )}
      </div>
    </div>
  );
}
