import { Clock, FileQuestion, Languages, Star } from 'lucide-react';
import type { Exam } from '@prepmitra/shared';
import { EXAM_CATEGORIES } from '@prepmitra/shared';
import { Badge, ButtonLink, Card, IconTile, type BadgeTone } from '@/components/ui';
import { useT } from '@/i18n';
import { catalogMessages, categoryText, creditsText, difficultyText } from '@/i18n/messages/catalog';

export const difficultyTone: Record<Exam['difficulty'], BadgeTone> = { Easy: 'success', Moderate: 'warning', Hard: 'danger' };

export function ExamCard({ exam }: { exam: Exam }) {
  const icon = EXAM_CATEGORIES.find((c) => c.id === exam.category)?.icon ?? 'file';
  const t = useT(catalogMessages);
  return (
    <Card className="flex h-full flex-col p-5 transition-shadow hover:shadow-raised">
      <div className="flex items-start gap-3">
        <IconTile name={icon} />
        <div className="min-w-0 flex-1">
          <p className="text-xs font-medium text-muted">{categoryText(t, exam.category).label}</p>
          <h3 className="mt-0.5 text-base font-semibold leading-snug">{exam.title}</h3>
        </div>
      </div>
      <div className="mt-3 flex flex-wrap gap-1.5">
        <Badge tone={difficultyTone[exam.difficulty]}>{difficultyText(t, exam.difficulty)}</Badge>
        {exam.isFree ? <Badge tone="success">{t('freeTrial')}</Badge> : <Badge tone="primary">{creditsText(t, exam.creditCost)}</Badge>}
        <Badge icon={<Star className="h-3 w-3 fill-current" aria-hidden />}>{exam.rating.toFixed(1)}</Badge>
      </div>
      <dl className="mt-4 grid grid-cols-3 gap-2 text-xs text-muted">
        <div className="flex items-center gap-1.5"><Clock className="h-3.5 w-3.5" aria-hidden /><dt className="sr-only">{t('duration')}</dt><dd>{t('minShort', { count: exam.durationMin })}</dd></div>
        <div className="flex items-center gap-1.5"><FileQuestion className="h-3.5 w-3.5" aria-hidden /><dt className="sr-only">{t('questions')}</dt><dd>{t('qsShort', { count: exam.totalQuestions })}</dd></div>
        <div className="flex items-center gap-1.5"><Languages className="h-3.5 w-3.5" aria-hidden /><dt className="sr-only">{t('languages')}</dt><dd>{exam.languages.length === 1 ? t('english') : t('langsShort', { count: exam.languages.length })}</dd></div>
      </dl>
      <div className="mt-auto flex items-center justify-between gap-3 pt-5">
        <p className="text-sm">
          <span className="font-semibold text-ink">{exam.isFree ? '₹0' : exam.creditCost > 1 ? `₹${exam.creditCost * 99}` : '₹99'}</span>
          <span className="text-muted"> {exam.isFree ? t('firstAttempt') : t('orPlanCredits')}</span>
        </p>
        <ButtonLink to={`/exams/${exam.id}`} size="sm" variant="outline" aria-label={t('viewDetailsFor', { title: exam.title })}>
          {t('viewDetails')}
        </ButtonLink>
      </div>
    </Card>
  );
}
