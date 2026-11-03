import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Calculator, CircleCheck, Clock, FileQuestion, Languages, Star, Users, XCircle } from 'lucide-react';
import { EXAM_CATEGORIES, LANGUAGES } from '@prepmitra/shared';
import { Badge, Button, Card, CardBody, CardHeader, ErrorState, IconTile, LoadingSkeleton, Notice } from '@/components/ui';
import { difficultyTone } from '@/components/exam/ExamCard';
import { examService } from '@/services';
import { examCreditCost, useAuthStore, useSubscriptionStore } from '@/store';
import { useAsync } from '@/hooks/useAsync';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT, useUiLang } from '@/i18n';
import { catalogMessages, categoryText, creditsText, difficultyText } from '@/i18n/messages/catalog';
import { layoutMessages } from '@/i18n/messages/layout';

export function ExamDetailsPage() {
  const { id = '' } = useParams();
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.session?.user);
  const sub = useSubscriptionStore((s) => s.sub);
  const { data: exam, loading, error, reload } = useAsync(() => examService.get(id), [id]);
  const [picked, setPicked] = useState<number | null>(null);
  const t = useT(catalogMessages);
  const tl = useT(layoutMessages);
  const lang = useUiLang();
  useDocumentTitle(
    exam ? t('detailsSeoTitle', { exam: exam.shortTitle }) : t('detailsDocTitle'),
    exam ? `${exam.description} ${exam.totalQuestions} questions, ${exam.durationMin} minutes. Practise free with a personal report.` : undefined,
  );

  if (loading) return <LoadingSkeleton variant="page" />;
  if (error || !exam)
    return (
      <ErrorState
        title={t('examNotFound')}
        description={error ?? t('examNotAvailable')}
        onRetry={reload}
      />
    );

  const icon = EXAM_CATEGORIES.find((c) => c.id === exam.category)?.icon ?? 'file';
  const { cost, usesFreeTrial } = examCreditCost(exam, sub);
  const demoQuestions = exam.sections.length * exam.demo.questionsPerSection;
  // The free 30-minute mini mock (plan Day 3): offered on every exam while the trial is unused.
  const miniAvailable = !exam.isFree && !sub.freeMiniMockUsed;
  const start = (mode: 'mini' | 'full') => {
    const dest = `/exams/${exam.id}/instructions${mode === 'mini' ? '?mode=mini' : ''}`;
    if (!user) navigate(`/login?redirect=${encodeURIComponent(dest)}`);
    else navigate(dest);
  };

  return (
    <div>
      <Link to="/exams" className="inline-flex items-center gap-1.5 text-sm font-medium text-muted hover:text-primary">
        <ArrowLeft className="h-4 w-4" aria-hidden /> {t('allExamsBack')}
      </Link>

      <div className="mt-4 grid grid-cols-1 gap-6 lg:grid-cols-[1fr_340px]">
        <div className="space-y-6">
          <Card className="p-6">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
              <IconTile name={icon} className="h-14 w-14" />
              <div className="min-w-0 flex-1">
                <p className="text-sm text-muted">{categoryText(t, exam.category).label} · {exam.conductingBody}</p>
                <h1 className="mt-1 text-2xl font-bold sm:text-3xl">{exam.title}</h1>
                <div className="mt-3 flex flex-wrap gap-2">
                  <Badge tone={difficultyTone[exam.difficulty]}>{difficultyText(t, exam.difficulty)}</Badge>
                  <Badge icon={<Star className="h-3 w-3 fill-current" />}>{t('ratingBadge', { rating: exam.rating.toFixed(1) })}</Badge>
                  <Badge icon={<Users className="h-3 w-3" />}>{t('attemptsBadge', { count: exam.attemptsCount.toLocaleString('en-IN') })}</Badge>
                </div>
              </div>
            </div>
            <p className="mt-5 leading-relaxed text-muted">{exam.description}</p>
            <ul className="mt-5 grid gap-2 sm:grid-cols-3">
              {exam.highlights.map((h) => (
                <li key={h} className="flex items-center gap-2 text-sm"><CircleCheck className="h-4 w-4 shrink-0 text-success" aria-hidden />{h}</li>
              ))}
            </ul>
          </Card>

          <Card>
            <CardHeader title={t('patternTitle')} description={t('patternDesc')} />
            <CardBody>
              <div className="overflow-x-auto">
                <table className="w-full min-w-[520px] text-sm">
                  <thead>
                    <tr className="border-b border-line text-left text-muted">
                      <th scope="col" className="py-2 pr-4 font-medium">{t('colSection')}</th>
                      <th scope="col" className="py-2 pr-4 font-medium">{t('colQuestions')}</th>
                      <th scope="col" className="py-2 pr-4 font-medium">{t('colMarksEach')}</th>
                      <th scope="col" className="py-2 pr-4 font-medium">{t('colNegative')}</th>
                      <th scope="col" className="py-2 font-medium">{t('colTime')}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {exam.sections.map((s) => (
                      <tr key={s.id} className="border-b border-line last:border-0">
                        <th scope="row" className="py-2.5 pr-4 text-left font-medium">{s.name}</th>
                        <td className="py-2.5 pr-4">{s.questionCount}</td>
                        <td className="py-2.5 pr-4">{s.marksPerQuestion}</td>
                        <td className="py-2.5 pr-4">{s.negativeMarks > 0 ? `−${s.negativeMarks}` : t('none')}</td>
                        <td className="py-2.5">{s.durationMin ? t('minShort', { count: s.durationMin }) : t('shared')}</td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot>
                    <tr className="font-semibold">
                      <td className="pt-3">{t('total')}</td>
                      <td className="pt-3">{exam.totalQuestions}</td>
                      <td className="pt-3" colSpan={2}>{t('marksTotal', { count: exam.totalMarks })}</td>
                      <td className="pt-3">{t('minShort', { count: exam.durationMin })}</td>
                    </tr>
                  </tfoot>
                </table>
              </div>
              <p className="mt-4 text-sm text-muted"><b className="text-ink">{t('negativeMarking')}</b> {exam.negativeMarking}</p>
              <p className="mt-1 text-sm text-muted">
                <b className="text-ink">{t('questionTypes')}</b>{' '}
                {exam.questionTypes.map((q) => t(({ single: 'qtSingle', multiple: 'qtMultiple', numeric: 'qtNumeric' } as const)[q])).join(', ')}
              </p>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title={t('sampleTitle')} description={t('sampleDesc')} />
            <CardBody>
              <p className="font-medium">{exam.sampleQuestion.text}</p>
              <div className="mt-4 grid gap-2 sm:grid-cols-2" role="radiogroup" aria-label={t('sampleOptions')}>
                {exam.sampleQuestion.options.map((o, i) => {
                  const isCorrect = i === exam.sampleQuestion.answerIndex;
                  const chosen = picked === i;
                  return (
                    <button
                      key={o}
                      type="button"
                      role="radio"
                      aria-checked={chosen}
                      onClick={() => setPicked(i)}
                      className={cn(
                        'flex items-center gap-3 rounded-lg border px-4 py-3 text-left text-sm transition-colors',
                        picked === null && 'border-line-strong hover:bg-stone-50',
                        picked !== null && isCorrect && 'border-success bg-success-soft',
                        picked !== null && chosen && !isCorrect && 'border-danger bg-danger-soft',
                        picked !== null && !chosen && !isCorrect && 'border-line opacity-70',
                      )}
                    >
                      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-current text-xs font-semibold">{String.fromCharCode(65 + i)}</span>
                      <span className="flex-1">{o}</span>
                      {picked !== null && isCorrect && <CircleCheck className="h-4 w-4 text-success" aria-label={t('correctAnswer')} />}
                      {picked !== null && chosen && !isCorrect && <XCircle className="h-4 w-4 text-danger" aria-label={t('incorrect')} />}
                    </button>
                  );
                })}
              </div>
              {picked !== null && (
                <p className={cn('mt-3 text-sm font-medium', picked === exam.sampleQuestion.answerIndex ? 'text-success' : 'text-danger')} role="status">
                  {picked === exam.sampleQuestion.answerIndex ? t('sampleCorrect') : t('sampleWrong', { letter: String.fromCharCode(65 + exam.sampleQuestion.answerIndex) })}
                </p>
              )}
            </CardBody>
          </Card>
        </div>

        <aside className="space-y-4 lg:sticky lg:top-24 lg:self-start">
          <Card className="p-5">
            <p className="text-sm text-muted">{t('price')}</p>
            <p className="mt-1 text-3xl font-bold">
              {usesFreeTrial ? t('free') : creditsText(t, cost)}
            </p>
            <p className="text-sm text-muted">
              {usesFreeTrial ? t('usesFreeTrial') : t('fullMockOr', { amount: 99 * cost })}
            </p>
            <dl className="mt-5 space-y-2.5 text-sm">
              <div className="flex items-center gap-2.5"><Clock className="h-4 w-4 text-muted" aria-hidden /><dt className="text-muted">{t('duration')}</dt><dd className="ml-auto font-medium">{t('minShort', { count: exam.durationMin })}</dd></div>
              <div className="flex items-center gap-2.5"><FileQuestion className="h-4 w-4 text-muted" aria-hidden /><dt className="text-muted">{t('questions')}</dt><dd className="ml-auto font-medium">{exam.totalQuestions}</dd></div>
              <div className="flex items-center gap-2.5"><Languages className="h-4 w-4 text-muted" aria-hidden /><dt className="text-muted">{t('languages')}</dt><dd className="ml-auto font-medium">{exam.languages.length}</dd></div>
              <div className="flex items-center gap-2.5"><Calculator className="h-4 w-4 text-muted" aria-hidden /><dt className="text-muted">{t('calculator')}</dt><dd className="ml-auto font-medium">{exam.calculatorAllowed ? t('onScreen') : t('notAllowed')}</dd></div>
            </dl>
            {miniAvailable && (
              <Button size="lg" className="mt-5 w-full" onClick={() => start('mini')}>
                {t('startMini')}
              </Button>
            )}
            <Button size="lg" variant={miniAvailable ? 'outline' : 'primary'} className={miniAvailable ? 'mt-2 w-full' : 'mt-5 w-full'} onClick={() => start('full')}>
              {user ? (usesFreeTrial ? t('startFreeMock') : t('startFull', { credits: creditsText(t, cost) })) : t('loginToStart')}
            </Button>
            {miniAvailable && <p className="mt-2 text-center text-xs text-muted">{t('miniNote')}</p>}
            {user && !usesFreeTrial && sub.credits < cost && (
              <p className="mt-2 text-center text-xs text-danger">{t('needCredits', { credits: creditsText(t, cost) })}</p>
            )}
          </Card>
          <Notice tone="info" title={t('demoPaperTitle')}>
            {t('demoPaperBody', { count: demoQuestions, min: exam.demo.durationMin })}
          </Notice>
          <Card className="p-5">
            <p className="text-sm font-semibold">{t('availableIn')}</p>
            <p className="mt-2 text-sm text-muted">{exam.languages.map((c) => { const l = LANGUAGES.find((x) => x.code === c); return l ? (lang === 'hi' ? l.nativeName : l.name) : c; }).join(', ')}</p>
          </Card>
          <p className="text-xs text-muted">{tl('affiliation')}</p>
        </aside>
      </div>
    </div>
  );
}
