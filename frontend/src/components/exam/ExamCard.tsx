import { ArrowRight, Clock, FileQuestion, Languages } from 'lucide-react';
import { Link } from 'react-router-dom';
import type { Exam } from '@prepmitra/shared';
import { EXAM_CATEGORIES } from '@prepmitra/shared';
import { AppIcon, type BadgeTone } from '@/components/ui';
import { useT } from '@/i18n';
import { useContentT } from '@/i18n/content';
import { catalogMessages, categoryText, creditsText, difficultyText } from '@/i18n/messages/catalog';
import { cn } from '@/utils/cn';
import { CATEGORY_TONE } from './categoryTone';
import { isExamOpen } from '@/config/launch';

export const difficultyTone: Record<Exam['difficulty'], BadgeTone> = { Easy: 'success', Moderate: 'warning', Hard: 'danger' };
const DIFF_PILL: Record<Exam['difficulty'], string> = {
  Easy: 'bg-success-soft text-success',
  Moderate: 'bg-warning-soft text-warning-ink',
  Hard: 'bg-danger-soft text-danger',
};

/** Catalog card: the whole card links to the exam's details. */
export function ExamCard({ exam }: { exam: Exam }) {
  const icon = EXAM_CATEGORIES.find((c) => c.id === exam.category)?.icon ?? 'file';
  const t = useT(catalogMessages);
  const ct = useContentT();
  const title = ct(exam.title);
  const open = isExamOpen(exam);
  return (
    <Link
      to={`/exams/${exam.id}`}
      aria-label={t('viewDetailsFor', { title })}
      className={cn(
        'group flex h-full flex-col rounded-[22px] border border-line p-5 transition duration-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-secondary',
        open ? 'bg-card hover:-translate-y-0.5 hover:border-secondary/40 hover:shadow-[0_18px_40px_-24px_rgb(23_74_56/0.45)]' : 'bg-surface/60 hover:border-line-strong',
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <span className={cn('flex h-11 w-11 items-center justify-center rounded-2xl', open ? CATEGORY_TONE[exam.category] : 'bg-line text-muted')}>
          <AppIcon name={icon} className="h-5 w-5" />
        </span>
        {open ? (
          <span className={cn('rounded-full px-2.5 py-1 text-xs font-medium', DIFF_PILL[exam.difficulty])}>{difficultyText(t, exam.difficulty)}</span>
        ) : (
          <span className="rounded-full bg-ink/80 px-2.5 py-1 text-xs font-semibold text-white">{t('comingSoon')}</span>
        )}
      </div>
      <p className="mt-4 text-xs font-medium text-muted">{categoryText(t, exam.category).label}</p>
      <h3 className={cn('mt-1 text-lg font-semibold leading-snug', open ? 'text-ink' : 'text-muted')}>{title}</h3>
      <ul className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-sm text-muted">
        <li className="flex items-center gap-1.5"><Clock className="h-4 w-4 text-subtle" aria-hidden />{t('minShort', { count: exam.durationMin })}</li>
        <li className="flex items-center gap-1.5"><FileQuestion className="h-4 w-4 text-subtle" aria-hidden />{t('qsShort', { count: exam.totalQuestions })}</li>
        <li className="flex items-center gap-1.5"><Languages className="h-4 w-4 text-subtle" aria-hidden />{exam.languages.length === 1 ? t('english') : t('langsShort', { count: exam.languages.length })}</li>
      </ul>
      <div className="min-h-5 flex-1" aria-hidden />
      <div className="flex items-center justify-between gap-3 border-t border-dashed border-line-strong pt-4">
        {open ? (
          <p className="text-sm">
            <span className="font-semibold text-ink">{exam.isFree ? t('free') : creditsText(t, exam.creditCost)}</span>
            <span className="text-muted"> · {exam.isFree ? t('firstAttempt') : `₹${Math.max(1, exam.creditCost) * 99}`}</span>
          </p>
        ) : (
          <p className="text-sm font-medium text-muted">{t('comingSoon')}</p>
        )}
        <span className="inline-flex items-center gap-1.5 text-sm font-semibold text-secondary">
          <span className="hidden sm:inline">{t('viewDetails')}</span>
          <span className={cn('flex h-8 w-8 items-center justify-center rounded-full transition-colors', open ? 'bg-secondary-soft text-secondary group-hover:bg-secondary group-hover:text-white' : 'bg-line text-muted')}>
            <ArrowRight className="h-4 w-4" aria-hidden />
          </span>
        </span>
      </div>
    </Link>
  );
}
