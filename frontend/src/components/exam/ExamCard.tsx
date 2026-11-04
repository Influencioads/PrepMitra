import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import type { Exam } from '@prepmitra/shared';
import { EXAM_CATEGORIES } from '@prepmitra/shared';
import { AppIcon, type BadgeTone } from '@/components/ui';
import { useT } from '@/i18n';
import { useContentT } from '@/i18n/content';
import { catalogMessages, categoryText, creditsText, difficultyText } from '@/i18n/messages/catalog';
import { cn } from '@/utils/cn';

export const difficultyTone: Record<Exam['difficulty'], BadgeTone> = { Easy: 'success', Moderate: 'warning', Hard: 'danger' };
const DIFF_DOT: Record<Exam['difficulty'], string> = { Easy: 'bg-success', Moderate: 'bg-warning', Hard: 'bg-danger' };

/** Minimal catalog card: the whole card is one link to the exam's details. */
export function ExamCard({ exam }: { exam: Exam }) {
  const icon = EXAM_CATEGORIES.find((c) => c.id === exam.category)?.icon ?? 'file';
  const t = useT(catalogMessages);
  const ct = useContentT();
  const title = ct(exam.title);
  const facts = [
    t('minShort', { count: exam.durationMin }),
    t('qsShort', { count: exam.totalQuestions }),
    exam.languages.length === 1 ? t('english') : t('langsShort', { count: exam.languages.length }),
  ];
  return (
    <Link
      to={`/exams/${exam.id}`}
      aria-label={t('viewDetailsFor', { title })}
      className="group flex h-full flex-col rounded-2xl border border-line bg-card p-5 transition-colors hover:border-secondary/50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-secondary"
    >
      <div className="flex items-center gap-2 text-xs font-medium text-muted">
        <AppIcon name={icon} className="h-4 w-4 text-secondary" />
        {categoryText(t, exam.category).label}
      </div>
      <h3 className="mt-3 text-lg font-semibold leading-snug text-ink">{title}</h3>
      <p className="mt-2 text-sm text-muted">{facts.join(' · ')}</p>
      <p className="mt-1 flex items-center gap-1.5 text-sm text-muted">
        <span className={cn('h-1.5 w-1.5 rounded-full', DIFF_DOT[exam.difficulty])} aria-hidden />
        {difficultyText(t, exam.difficulty)}
      </p>
      <div className="min-h-5 flex-1" aria-hidden />
      <div className="flex items-end justify-between gap-3 border-t border-line pt-4">
        <p className="text-sm">
          <span className="font-semibold text-ink">{exam.isFree ? t('free') : creditsText(t, exam.creditCost)}</span>
          <span className="text-muted"> · {exam.isFree ? t('firstAttempt') : `₹${Math.max(1, exam.creditCost) * 99}`}</span>
        </p>
        <span className="inline-flex items-center gap-1 text-sm font-semibold text-secondary">
          {t('viewDetails')}
          <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" aria-hidden />
        </span>
      </div>
    </Link>
  );
}
