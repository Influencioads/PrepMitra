import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Check, CircleCheck, XCircle } from 'lucide-react';
import { EXAM_CATEGORIES, LANGUAGES } from '@prepmitra/shared';
import { AppIcon, Button, ButtonLink, ErrorState, LoadingSkeleton, Notice } from '@/components/ui';
import { examService } from '@/services';
import { USE_MOCK } from '@/services/mock';
import { isExamOpen, openExamCategories } from '@/config/launch';
import { examCreditCost, useAuthStore, useSubscriptionStore } from '@/store';
import { useAsync } from '@/hooks/useAsync';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT, useUiLang } from '@/i18n';
import { useContentT } from '@/i18n/content';
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
  const ct = useContentT();
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
  const langNames = exam.languages.map((c) => { const l = LANGUAGES.find((x) => x.code === c); return l ? (lang === 'hi' ? l.nativeName : l.name) : c; });
  // Facts from the exam itself (no marketing claims that the data can't back up).
  const highlights = [
    t('hlPattern', { sections: exam.sections.length, questions: exam.totalQuestions }),
    t('hlReport'),
    t('hlLangs', { langs: langNames.join(', ') }),
  ];
  // Backend sample questions carry their topic as a "[Topic] …" prefix.
  const topicMatch = /^\[([^\]]+)\]\s*/.exec(exam.sampleQuestion.text);
  const sample = { topic: topicMatch?.[1], text: topicMatch ? exam.sampleQuestion.text.slice(topicMatch[0].length) : exam.sampleQuestion.text };
  const negMax = Math.max(0, ...exam.sections.map((s) => s.negativeMarks));
  const open = isExamOpen(exam);
  const openCats = openExamCategories();
  const openList = openCats !== 'all' && openCats.length === 1 ? `/exams?category=${openCats[0]}` : '/exams';
  const facts = [
    { label: t('duration'), value: t('minShort', { count: exam.durationMin }) },
    { label: t('questions'), value: String(exam.totalQuestions) },
    { label: t('totalMarks'), value: String(exam.totalMarks) },
    { label: t('colNegative'), value: negMax > 0 ? `−${negMax}` : t('none') },
  ];
  const start = (mode: 'mini' | 'full') => {
    const dest = `/exams/${exam.id}/instructions${mode === 'mini' ? '?mode=mini' : ''}`;
    if (!user) navigate(`/login?redirect=${encodeURIComponent(dest)}`);
    else navigate(dest);
  };

  return (
    <div>
      <Link to="/exams" className="inline-flex items-center gap-1.5 text-sm font-medium text-muted hover:text-ink">
        <ArrowLeft className="h-4 w-4" aria-hidden /> {t('allExamsBack')}
      </Link>

      {/* ---------- Header ---------- */}
      <header className="mt-6 max-w-3xl">
        <p className="flex items-center gap-2 text-sm font-medium text-secondary">
          <AppIcon name={icon} className="h-4 w-4" />
          {categoryText(t, exam.category).label}
          <span className="text-subtle">·</span>
          <span className="text-muted">{difficultyText(t, exam.difficulty)}</span>
        </p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">{ct(exam.title)}</h1>
        <p className="mt-3 leading-relaxed text-muted">{ct(exam.description)}</p>
        <ul className="mt-4 flex flex-wrap gap-x-5 gap-y-1.5 text-sm text-muted">
          {highlights.map((h) => (
            <li key={h} className="flex items-center gap-1.5"><Check className="h-4 w-4 text-secondary" aria-hidden />{h}</li>
          ))}
        </ul>
      </header>

      {/* ---------- Key facts ---------- */}
      <dl className="mt-8 grid grid-cols-2 overflow-hidden rounded-2xl border border-line bg-card sm:grid-cols-4">
        {facts.map((f, i) => (
          <div key={f.label} className={cn('px-5 py-4', i % 2 === 1 && 'border-l border-line', i >= 2 && 'border-t border-line sm:border-t-0', i === 2 && 'sm:border-l')}>
            <dt className="text-xs text-muted">{f.label}</dt>
            <dd className="mt-1 text-xl font-semibold tabular-nums text-ink">{f.value}</dd>
          </div>
        ))}
      </dl>

      <div className="mt-10 grid grid-cols-1 gap-10 lg:grid-cols-[1fr_320px]">
        <div className="min-w-0 space-y-12">
          {/* ---------- Pattern ---------- */}
          <section aria-labelledby="pattern-heading">
            <h2 id="pattern-heading" className="text-xl font-semibold">{t('patternTitle')}</h2>
            <p className="mt-1 text-sm text-muted">{t('patternDesc')}</p>

            {/* Phone: one row per section */}
            <ul className="mt-4 divide-y divide-line rounded-2xl border border-line bg-card sm:hidden">
              {exam.sections.map((s) => (
                <li key={s.id} className="px-4 py-3.5">
                  <p className="text-sm font-medium">{ct(s.name)}</p>
                  <p className="mt-1 text-xs text-muted">
                    {t('qsShort', { count: s.questionCount })} · {t('colMarksEach')} {s.marksPerQuestion} · {t('colNegative')} {s.negativeMarks > 0 ? `−${s.negativeMarks}` : t('none')} · {s.durationMin ? t('minShort', { count: s.durationMin }) : t('shared')}
                  </p>
                </li>
              ))}
              <li className="flex justify-between px-4 py-3.5 text-sm font-semibold">
                <span>{t('total')}</span>
                <span className="tabular-nums">{exam.totalQuestions} · {t('marksTotal', { count: exam.totalMarks })} · {t('minShort', { count: exam.durationMin })}</span>
              </li>
            </ul>

            <div className="mt-4 hidden overflow-hidden rounded-2xl border border-line bg-card sm:block">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-line text-left text-xs text-muted">
                    <th scope="col" className="px-5 py-3 font-medium">{t('colSection')}</th>
                    <th scope="col" className="px-3 py-3 text-right font-medium">{t('colQuestions')}</th>
                    <th scope="col" className="px-3 py-3 text-right font-medium">{t('colMarksEach')}</th>
                    <th scope="col" className="px-3 py-3 text-right font-medium">{t('colNegative')}</th>
                    <th scope="col" className="px-5 py-3 text-right font-medium">{t('colTime')}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-line">
                  {exam.sections.map((s) => (
                    <tr key={s.id}>
                      <th scope="row" className="px-5 py-3.5 text-left font-medium">{ct(s.name)}</th>
                      <td className="px-3 py-3.5 text-right tabular-nums">{s.questionCount}</td>
                      <td className="px-3 py-3.5 text-right tabular-nums">{s.marksPerQuestion}</td>
                      <td className="px-3 py-3.5 text-right tabular-nums">{s.negativeMarks > 0 ? `−${s.negativeMarks}` : t('none')}</td>
                      <td className="px-5 py-3.5 text-right text-muted">{s.durationMin ? t('minShort', { count: s.durationMin }) : t('shared')}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr className="border-t border-line bg-background/60 font-semibold">
                    <td className="px-5 py-3.5">{t('total')}</td>
                    <td className="px-3 py-3.5 text-right tabular-nums">{exam.totalQuestions}</td>
                    <td className="px-3 py-3.5 text-right" colSpan={2}>{t('marksTotal', { count: exam.totalMarks })}</td>
                    <td className="px-5 py-3.5 text-right">{t('minShort', { count: exam.durationMin })}</td>
                  </tr>
                </tfoot>
              </table>
            </div>
            <p className="mt-4 text-sm text-muted"><span className="font-medium text-ink">{t('negativeMarking')}</span> {ct(exam.negativeMarking)}</p>
            <p className="mt-1 text-sm text-muted">
              <span className="font-medium text-ink">{t('questionTypes')}</span>{' '}
              {exam.questionTypes.map((q) => t(({ single: 'qtSingle', multiple: 'qtMultiple', numeric: 'qtNumeric' } as const)[q])).join(', ')}
            </p>
          </section>

          {/* ---------- Sample question ---------- */}
          <section aria-labelledby="sample-heading">
            <h2 id="sample-heading" className="text-xl font-semibold">{t('sampleTitle')}</h2>
            <p className="mt-1 text-sm text-muted">{t('sampleDesc')}</p>
            <div className="mt-4 rounded-2xl border border-line bg-card p-5 sm:p-6">
              {sample.topic && <p className="text-xs font-medium uppercase tracking-wide text-secondary">{t('sampleTopic', { topic: ct(sample.topic) })}</p>}
              <p className={cn('font-medium leading-relaxed', sample.topic && 'mt-2')}>{sample.text}</p>
              {lang === 'hi' && <p className="mt-1 text-xs text-muted">{t('sampleInEnglish')}</p>}
              <div className="mt-5 grid gap-2 sm:grid-cols-2" role="radiogroup" aria-label={t('sampleOptions')}>
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
                        'flex items-center gap-3 rounded-xl border px-4 py-3 text-left text-sm transition-colors',
                        picked === null && 'border-line hover:border-secondary/50 hover:bg-background',
                        picked !== null && isCorrect && 'border-success bg-success-soft',
                        picked !== null && chosen && !isCorrect && 'border-danger bg-danger-soft',
                        picked !== null && !chosen && !isCorrect && 'border-line opacity-60',
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
            </div>
          </section>
        </div>

        {/* ---------- Price + start ---------- */}
        <aside className="space-y-4 lg:sticky lg:top-24 lg:self-start">
          {!open && (
            <div className="rounded-2xl border border-line bg-card p-6">
              <span className="inline-flex rounded-full bg-ink/80 px-2.5 py-1 text-xs font-semibold text-white">{t('comingSoon')}</span>
              <p className="mt-3 text-lg font-semibold">{t('comingSoonTitle')}</p>
              <p className="mt-1 text-sm text-muted">{t('comingSoonBody')}</p>
              <ButtonLink to={openList} className="mt-5 w-full">{t('seeOpenExams')}</ButtonLink>
            </div>
          )}
          {open && (
          <div className="rounded-2xl border border-line bg-card p-6">
            <p className="text-sm text-muted">{t('price')}</p>
            <p className="mt-1 text-3xl font-bold tracking-tight">{usesFreeTrial ? t('free') : creditsText(t, cost)}</p>
            <p className="mt-0.5 text-sm text-muted">{usesFreeTrial ? t('usesFreeTrial') : t('fullMockOr', { amount: 99 * cost })}</p>
            {!exam.isFree && (
              <p className="mt-4 flex items-center justify-between border-t border-line pt-4 text-sm">
                <span className="text-muted">{t('miniPrice')}</span>
                <span className="font-medium text-primary">{sub.freeMiniMockUsed ? '—' : t('oncePerUser')}</span>
              </p>
            )}
            {exam.isFree ? (
              <Button size="lg" className="mt-5 w-full" onClick={() => start('full')}>
                {usesFreeTrial || !user ? t('startFreeMock') : t('startFull', { credits: creditsText(t, cost) })}
              </Button>
            ) : (
              <>
                {miniAvailable && (
                  <Button size="lg" className="mt-5 w-full" onClick={() => start('mini')}>
                    {t('startMini')}
                  </Button>
                )}
                <Button
                  size="lg"
                  variant={miniAvailable ? 'outline' : 'primary'}
                  className={cn('w-full', miniAvailable ? 'mt-2' : 'mt-5')}
                  onClick={() => start('full')}
                >
                  {user ? t('startFull', { credits: creditsText(t, cost) }) : t('startFullMock')}
                </Button>
                <p className="mt-3 text-center text-xs text-muted">{miniAvailable ? t('miniNote') : t('miniUsedNote')}</p>
              </>
            )}
            {!user && <p className="mt-1 text-center text-xs text-muted">{t('loginFirstNote')}</p>}
            {user && !usesFreeTrial && sub.credits < cost && (
              <p className="mt-2 text-center text-xs text-danger">{t('needCredits', { credits: creditsText(t, cost) })}</p>
            )}
            <dl className="mt-5 space-y-2 border-t border-line pt-4 text-sm">
              <div className="flex justify-between gap-3"><dt className="text-muted">{t('languages')}</dt><dd className="text-right font-medium">{langNames.join(', ')}</dd></div>
              <div className="flex justify-between gap-3"><dt className="text-muted">{t('calculator')}</dt><dd className="font-medium">{exam.calculatorAllowed ? t('onScreen') : t('notAllowed')}</dd></div>
            </dl>
          </div>
          )}
          {USE_MOCK && open && (
            <Notice tone="info" title={t('demoPaperTitle')}>
              {t('demoPaperBody', { count: demoQuestions, min: exam.demo.durationMin })}
            </Notice>
          )}
          <p className="text-xs text-subtle">{tl('affiliation')}</p>
        </aside>
      </div>
    </div>
  );
}
