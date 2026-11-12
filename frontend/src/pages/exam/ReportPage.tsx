import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useParams, useSearchParams } from 'react-router-dom';
import { ArrowLeft, CircleCheck, CircleMinus, Flag, Lightbulb, Sparkles, TrendingDown, Trophy, TriangleAlert, XCircle } from 'lucide-react';
import type { Answer, Loophole, QuestionOutcome } from '@prepmitra/shared';
import { formatDate, formatDuration, getExamById, getQuestionById, languageName } from '@prepmitra/shared';
import {
  Badge, Button, ButtonLink, Card, CardBody, CardHeader, ChoiceChip, DemoBadge, EmptyState, KeyValue, Notice, PageHeader, Tabs,
} from '@/components/ui';
import { SectionChart, TopicAccuracyChart } from '@/components/charts/Charts';
import { ReportActions } from '@/components/exam/ReportActions';
import { mentorMessages } from '@/i18n/messages/mentor';
import { CheckedSheet } from '@/components/exam/CheckedSheet';
import { SectionTable } from '@/components/exam/SectionTable';
import { ReportRating } from '@/components/exam/ReportRating';
import { TimePerQuestionChart } from '@/components/exam/TimePerQuestionChart';
import { ReportQuestionModal } from '@/components/exam/ReportQuestionModal';
import { PrintStyles } from '@/components/common/PrintStyles';
import { usePrintMode } from '@/lib/share';
import { saveFile } from '@/lib/download';
import { buildReportPdf } from '@/lib/reportPdf';
import { FAST, motion } from '@/components/motion';
import { track } from '@/lib/analytics';
import { describeAnswer, describeCorrect, shortLabel } from '@/features/exam/answers';
import { useAuthStore, useExamStore } from '@/store';
import { attemptService } from '@/services';
import { USE_MOCK } from '@/services/mock';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT, useUiLang } from '@/i18n';
import { useContentT } from '@/i18n/content';
import { reportMessages } from '@/i18n/messages/report';

type Tab = 'overview' | 'analysis' | 'review' | 'plan';
type Filter = 'all' | QuestionOutcome;

const outcomeBadge: Record<QuestionOutcome, { tone: 'success' | 'danger' | 'neutral'; label: 'correct' | 'incorrect' | 'unanswered'; Icon: typeof CircleCheck }> = {
  correct: { tone: 'success', label: 'correct', Icon: CircleCheck },
  incorrect: { tone: 'danger', label: 'incorrect', Icon: XCircle },
  unanswered: { tone: 'neutral', label: 'unanswered', Icon: CircleMinus },
};

export function ReportPage() {
  const { reportId = '' } = useParams();
  const t = useT(reportMessages);
  const tm = useT(mentorMessages);
  const uiLang = useUiLang();
  const report = useExamStore((s) => s.reports[reportId]);
  const attempt = useExamStore((s) => (report ? s.attempts[report.attemptId] : undefined));
  const [params] = useSearchParams();
  const initialTab = (['overview', 'analysis', 'review', 'plan'] as Tab[]).find((x) => x === params.get('tab')) ?? 'overview';
  const [tab, setTab] = useState<Tab>(initialTab);
  const firstName = useAuthStore((s) => s.session?.user.name?.split(' ')[0]);
  const [filter, setFilter] = useState<Filter>('all');
  const [timeSection, setTimeSection] = useState<string>('all');
  useDocumentTitle(report ? t('reportDocTitle', { exam: report.examTitle }) : t('reportFallbackTitle'));

  const numbered = useMemo(() => report?.result.questions.map((q, i) => ({ ...q, n: i + 1 })) ?? [], [report]);
  const { printing, print, withExpanded } = usePrintMode();
  const pageRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (report) track('report_viewed', { reportId: report.id, examId: report.examId, kind: 'exam' });
  }, [report?.id]); // eslint-disable-line react-hooks/exhaustive-deps

  // Real API: question text, answer key and explanations come from GET /v1/attempts/{id}/review.
  // Also gives the student's own answers, so the review works on a device that did not take the test.
  const [reviewAnswers, setReviewAnswers] = useState<Record<string, Answer | undefined> | null>(null);
  useEffect(() => {
    if (USE_MOCK || !report) return;
    attemptService.fetchReviewItems(report.attemptId).then(
      (items) => setReviewAnswers(Object.fromEntries(items.map((i) => [i.questionId, i.answer]))),
      () => undefined,
    );
  }, [report?.id]); // eslint-disable-line react-hooks/exhaustive-deps

  const ct = useContentT();
  const [flash, setFlash] = useState<string | null>(null);
  const [flagQ, setFlagQ] = useState<{ id: string; n: number } | null>(null);
  const [flagged, setFlagged] = useState<Set<string>>(() => new Set());

  if (!report)
    return (
      <EmptyState
        title={t('reportNotFound')}
        description={t('reportNotFoundDesc')}
        action={<ButtonLink to="/my-tests">{t('viewMyTests')}</ButtonLink>}
      />
    );

  const r = report.result;
  const exam = getExamById(report.examId);
  const next = getExamById(report.recommendedNextExamId);
  const qNumber = (qid: string) => numbered.find((q) => q.questionId === qid)?.n ?? 0;
  /** Tap a question number anywhere in the report: open it in the review and highlight it. */
  const jumpTo = (qid: string) => {
    setFilter('all');
    setTab('review');
    setFlash(qid);
    setTimeout(() => {
      const el = document.getElementById(`q-${qid}`);
      el?.scrollIntoView?.({ behavior: 'smooth', block: 'start' });
      el?.querySelector<HTMLElement>('[data-q-focus]')?.focus({ preventScroll: true });
    }, 50);
    setTimeout(() => setFlash((f) => (f === qid ? null : f)), 2000);
  };
  const QChips = ({ ids, max = 10 }: { ids: string[]; max?: number }) => (
    <span className="inline-flex flex-wrap items-center gap-1.5">
      {ids.slice(0, max).map((qid) => (
        <button key={qid} type="button" onClick={() => jumpTo(qid)} aria-label={t('openQuestion', { n: qNumber(qid) })} className="rounded bg-card px-2 py-0.5 text-xs font-semibold text-primary hover:underline">
          Q{qNumber(qid)}
        </button>
      ))}
      {ids.length > max && <span className="text-xs text-muted">+{ids.length - max}</span>}
    </span>
  );
  const loopTitle = (l: Loophole) =>
    l.pattern === 'careless_easy' ? t('loopCarelessEasy')
    : l.pattern === 'negative_guess' ? t('loopNegativeGuess')
    : l.pattern === 'time_sink' ? t('loopTimeSink')
    : l.pattern === 'skipped_section' && l.section ? t('loopSkippedSection', { section: ct(l.section) })
    : l.title;
  // The AI may give the same method for several questions: show it once with all its question numbers.
  const shortcutGroups = Object.values(
    (report.shortcuts ?? []).reduce<Record<string, { technique: string; detail: string; ids: string[] }>>((acc, sc) => {
      const key = `${sc.technique}|${sc.detail}`;
      (acc[key] ??= { technique: sc.technique, detail: sc.detail, ids: [] }).ids.push(sc.questionId);
      return acc;
    }, {}),
  );
  const shown = numbered.filter((q) => printing || filter === 'all' || q.outcome === filter);
  const show = (which: Tab) => printing || tab === which;
  const attemptRate = r.questions.length ? Math.round((r.attempted / r.questions.length) * 100) : 0;
  const timeData = numbered.map((q) => ({
    q: `Q${q.n}`,
    spent: q.timeSpentSec,
    expected: q.expectedTimeSec ?? getQuestionById(q.questionId)?.expectedTimeSec ?? 0,
    outcome: q.outcome,
    sectionId: q.sectionId,
  }));
  const marksLostWrong = r.questions.filter((q) => q.outcome === 'incorrect').reduce((s, q) => s + q.maxMarks, 0);
  const marksLostSkipped = r.questions.filter((q) => q.outcome === 'unanswered').reduce((s, q) => s + q.maxMarks, 0);

  // Demo reports have no server PDF: build one from the expanded page in the browser.
  const downloadPdf = report.isDemo
    ? async () => {
        const blob = await withExpanded(() => buildReportPdf(pageRef.current!));
        await saveFile(`PrepMitra-${report.examId}-report.pdf`, blob);
      }
    : undefined;

  return (
    <div ref={pageRef}>
      <PrintStyles />
      <Link data-print-hide to={`/exam-result/${report.id}`} className="inline-flex items-center gap-1.5 text-sm font-medium text-muted hover:text-primary">
        <ArrowLeft className="h-4 w-4" aria-hidden /> {t('resultSummary')}
      </Link>
      <PageHeader
        className="mt-3"
        eyebrow={report.isDemo ? <DemoBadge>{t('demoAnalysis')}</DemoBadge> : undefined}
        title={t('reportTitle', { exam: report.examTitle })}
        description={t('reportSubtitle', { date: formatDate(report.createdAt), language: languageName(report.language), taken: formatDuration(report.timeTakenSec), duration: formatDuration(report.durationSec) })}
        actions={USE_MOCK ? undefined : (
          <ButtonLink data-print-hide to={`/mentor/analysis/${report.attemptId}`} variant="outline">{tm('viewAnalysis')}</ButtonLink>
        )}
      />
      <CheckedSheet
        report={report}
        studentName={firstName}
        className="mb-8"
        onOpenPlan={() => { setTab('plan'); setTimeout(() => document.getElementById('report-tabs')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 30); }}
      />
      <ReportActions report={report} className="mb-6" onDownloadPdf={downloadPdf} onPrint={() => { track('report_viewed', { reportId: report.id, kind: 'exam', action: 'pdf' }); print(); }} />

      <div id="report-tabs" className="scroll-mt-24" />
      <div data-print-hide>
      <Tabs<Tab>
        ariaLabel={t('tabsLabel')}
        value={tab}
        onChange={setTab}
        items={[
          { value: 'overview', label: t('tabOverview') },
          { value: 'analysis', label: t('tabAnalysis') },
          { value: 'review', label: t('tabReview'), count: r.questions.length },
          { value: 'plan', label: t('tabPlan') },
        ]}
      />
      </div>

      <motion.div key={printing ? 'all' : tab} className="mt-6" role="tabpanel" aria-label={tab} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={FAST}>
        {show('overview') && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-[320px_1fr]">
              <Card className="p-6">
                <h3 className="text-lg font-bold">{t('atAGlance')}</h3>
                <dl className="mt-3 w-full divide-y divide-line text-left">
                  <KeyValue label={t('accuracy')} value={`${r.accuracy}%`} />
                  <KeyValue label={t('attemptRate')} value={`${attemptRate}% (${r.attempted}/${r.questions.length})`} />
                  <KeyValue label={t('lostNegative')} value={<span className={r.negativeMarksLost > 0 ? 'text-danger' : undefined}>{r.negativeMarksLost > 0 ? `−${r.negativeMarksLost}` : '0'}</span>} />
                  <KeyValue label={t('percentileEst')} value={report.percentile} />
                  <KeyValue label={t('correctIncorrectSkipped')} value={`${r.correct} / ${r.incorrect} / ${r.unanswered}`} />
                  <KeyValue label={t('timeTaken')} value={formatDuration(report.timeTakenSec)} />
                  {attempt && <KeyValue label={t('tabSwitchesCopy')} value={`${attempt.tabSwitches} / ${attempt.copyAttempts ?? 0}`} />}
                </dl>
              </Card>
              <Card>
                <CardHeader title={t('sectionWise')} />
                <CardBody>
                  <SectionChart data={r.sections.map((s) => ({ name: shortLabel(s.name), correct: s.correct, incorrect: s.incorrect, unanswered: s.unanswered }))} />
                  <SectionTable sections={r.sections} className="mt-4" />
                </CardBody>
              </Card>
            </div>
            <Card data-print-section>
              <CardHeader title={t('timePerQuestion')} description={t('timePerQuestionDesc')} />
              <CardBody>
                {r.sections.length > 1 && (
                  <div className="mb-4 flex flex-wrap gap-2" role="group" aria-label={t('timePerQuestion')} data-print-hide>
                    <ChoiceChip selected={timeSection === 'all'} onClick={() => setTimeSection('all')}>{t('allSections')}</ChoiceChip>
                    {r.sections.map((s) => (
                      <ChoiceChip key={s.sectionId} selected={timeSection === s.sectionId} onClick={() => setTimeSection(s.sectionId)}>{s.name}</ChoiceChip>
                    ))}
                  </div>
                )}
                <TimePerQuestionChart data={printing ? timeData : timeData.filter((d) => timeSection === 'all' || d.sectionId === timeSection)} />
              </CardBody>
            </Card>
            <Card data-print-section>
              <CardHeader title={t('topicWise')} description={t('topicWiseDesc')} />
              <CardBody><TopicAccuracyChart data={r.topics.map((t) => ({ topic: t.topic, accuracy: t.accuracy }))} /></CardBody>
            </Card>
          </div>
        )}

        {show('analysis') && (
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2" data-print-break>
            {(report.summary || report.encouragement) && (
              <Card className="flex gap-3 p-5 lg:col-span-2">
                <Sparkles className="mt-0.5 h-5 w-5 shrink-0 text-[#f26b1d]" aria-hidden />
                <div className="space-y-1 text-sm">
                  {report.summary && <p className="font-medium text-ink">{report.summary}</p>}
                  {report.encouragement && <p className="text-secondary">{report.encouragement}</p>}
                </div>
              </Card>
            )}
            <Card>
              <CardHeader title={<span className="flex items-center gap-2 text-success"><Trophy className="h-5 w-5" aria-hidden />{t('strengths')}</span>} />
              <CardBody>
                <ul className="space-y-3 text-sm">
                  {report.strengths.map((s) => <li key={s} className="rounded-lg bg-success-soft p-3 text-green-900">{s}</li>)}
                  {report.strengths.length === 0 && <li className="text-muted">{t('noStrengths')}</li>}
                </ul>
              </CardBody>
            </Card>
            <Card>
              <CardHeader title={<span className="flex items-center gap-2 text-danger"><TrendingDown className="h-5 w-5" aria-hidden />{t('weaknesses')}</span>} description={t('weaknessesDesc')} />
              <CardBody>
                {report.weaknesses.length === 0 ? (
                  <p className="text-sm text-muted">{t('noWeakness')}</p>
                ) : (
                  <ul className="space-y-3">
                    {report.weaknesses.map((w) => (
                      <li key={w.topic} className="rounded-lg border border-red-100 bg-danger-soft/60 p-3">
                        <div className="flex items-center justify-between gap-2">
                          <p className="font-semibold">{ct(w.topic)}</p>
                          <Badge tone="danger">{w.accuracy}%</Badge>
                        </div>
                        <p className="mt-1 text-sm text-muted">{w.note}</p>
                        {w.evidenceQuestionIds.length > 0 && (
                          <p className="mt-2 flex flex-wrap items-center gap-1.5 text-xs">
                            <span className="text-muted">{t('evidence')}</span>
                            <QChips ids={w.evidenceQuestionIds} />
                          </p>
                        )}
                      </li>
                    ))}
                  </ul>
                )}
              </CardBody>
            </Card>
            <Card>
              <CardHeader title={<span className="flex items-center gap-2 text-warning-ink"><TriangleAlert className="h-5 w-5" aria-hidden />{t('loopholes')}</span>} description={t('loopholesDesc')} />
              <CardBody>
                {report.loopholes.length === 0 ? (
                  <p className="text-sm text-muted">{t('noLoopholes')}</p>
                ) : (
                  <ul className="space-y-3">
                    {report.loopholes.map((l) => (
                      <li key={l.title} className="rounded-lg bg-warning-soft p-3">
                        <div className="flex items-start justify-between gap-2">
                          <p className="font-semibold text-amber-900">{loopTitle(l)}</p>
                          {l.marksImpact > 0 && <Badge tone="warning">{t('minusMarks', { n: Math.round(l.marksImpact * 100) / 100 })}</Badge>}
                        </div>
                        {l.detail && <p className="mt-1 text-sm text-amber-900/80">{l.detail}</p>}
                        {!!l.evidenceQuestionIds?.length && (
                          <p className="mt-2 flex flex-wrap items-center gap-1.5 text-xs">
                            <span className="text-amber-900/70">{t('questionsLabel')}</span>
                            <QChips ids={l.evidenceQuestionIds} max={8} />
                          </p>
                        )}
                      </li>
                    ))}
                  </ul>
                )}
              </CardBody>
            </Card>
            <Card>
              <CardHeader title={<span className="flex items-center gap-2 text-primary"><Lightbulb className="h-5 w-5" aria-hidden />{t('shortcutsTitle')}</span>} description={t('shortcutsDesc')} />
              <CardBody>
                {shortcutGroups.length === 0 ? (
                  <p className="text-sm text-muted">{t('noShortcuts')}</p>
                ) : (
                  <ul className="space-y-3" data-testid="shortcuts">
                    {shortcutGroups.map((g) => (
                      <li key={`${g.technique}|${g.detail}`} className="rounded-lg border border-primary/20 bg-primary-soft p-3">
                        {g.technique && <p className="font-semibold text-primary">{ct(g.technique)}</p>}
                        <p className="mt-1 text-sm text-primary-hover/80">{g.detail}</p>
                        <p className="mt-2 flex flex-wrap items-center gap-1.5 text-xs">
                          <span className="text-muted">{t('questionsLabel')}</span>
                          <QChips ids={g.ids} max={8} />
                        </p>
                      </li>
                    ))}
                  </ul>
                )}
              </CardBody>
            </Card>
            <Card>
              <CardHeader title={t('whereLost')} />
              <CardBody>
                <dl className="divide-y divide-line">
                  <KeyValue label={t('maxPossible')} value={r.maxScore} />
                  <KeyValue label={t('yourScore')} value={r.score} />
                  <KeyValue label={t('lostIncorrect')} value={marksLostWrong} />
                  <KeyValue label={t('lostNegative')} value={r.negativeMarksLost} />
                  <KeyValue label={t('leftOnTable')} value={marksLostSkipped} />
                  <KeyValue label={t('totalLost')} value={<span className="text-danger">{r.marksLostTotal}</span>} />
                </dl>
              </CardBody>
            </Card>
          </div>
        )}

        {show('review') && (
          <div data-print-break>
            <div className="mb-4 flex flex-wrap gap-2" role="group" aria-label={t('filterQuestions')} data-print-hide>
              {(['all', 'incorrect', 'unanswered', 'correct'] as Filter[]).map((f) => (
                <ChoiceChip key={f} selected={filter === f} onClick={() => setFilter(f)}>
                  {f === 'all' ? t('filterAll') : t(outcomeBadge[f].label)} ({f === 'all' ? r.questions.length : r.questions.filter((q) => q.outcome === f).length})
                </ChoiceChip>
              ))}
            </div>
            {shown.length === 0 && <EmptyState title={t('noQuestionsFilter')} className="py-8" />}
            <ol className="space-y-4">
              {shown.map((qr) => {
                const q = getQuestionById(qr.questionId);
                if (!q) return null;
                const answer = attempt?.states[qr.questionId]?.answer ?? reviewAnswers?.[qr.questionId];
                const haveAnswers = !!attempt || !!reviewAnswers;
                const ob = outcomeBadge[qr.outcome];
                const slow = qr.timeSpentSec > q.expectedTimeSec * 1.5;
                const sectionName = exam?.sections.find((s) => s.id === qr.sectionId)?.name;
                return (
                  <li key={qr.questionId} id={`q-${qr.questionId}`} className="scroll-mt-24">
                    <Card className={cn('p-5 transition-shadow', flash === qr.questionId && 'ring-2 ring-[#f26b1d] ring-offset-2')}>
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-sm font-semibold outline-none" tabIndex={-1} data-q-focus>Q{qr.n}</span>
                        <Badge tone={ob.tone} icon={<ob.Icon className="h-3 w-3" />}>{t(ob.label)}</Badge>
                        <Badge>{q.topic}</Badge>
                        {sectionName && <span className="text-xs text-muted">{sectionName}</span>}
                        <span className="ml-auto text-xs text-muted">
                          {t('marksTime', { marks: `${qr.marksAwarded > 0 ? '+' : ''}${qr.marksAwarded}` })} · <span className={cn(slow && 'font-semibold text-warning-ink')}>{formatDuration(qr.timeSpentSec)}</span> / {t('expectedLabel', { time: formatDuration(q.expectedTimeSec) })}
                        </span>
                      </div>
                      <p className="mt-3 font-medium leading-relaxed">{q.text}</p>
                      {q.options && (
                        <ul className="mt-3 grid gap-2 sm:grid-cols-2">
                          {q.options.map((o, i) => {
                            const correct = q.correctOptionIds?.includes(o.id);
                            const picked = answer?.selectedOptionIds?.includes(o.id);
                            return (
                              <li
                                key={o.id}
                                className={cn(
                                  'flex items-start gap-2 rounded-lg border px-3 py-2 text-sm',
                                  correct ? 'border-green-300 bg-success-soft' : picked ? 'border-red-300 bg-danger-soft' : 'border-line',
                                )}
                              >
                                <span className="font-semibold">{String.fromCharCode(65 + i)}.</span>
                                <span className="flex-1">{o.text}</span>
                                {correct && <CircleCheck className="h-4 w-4 shrink-0 text-success" aria-label={t('correctOption')} />}
                                {picked && !correct && <XCircle className="h-4 w-4 shrink-0 text-danger" aria-label={t('yourChoice')} />}
                              </li>
                            );
                          })}
                        </ul>
                      )}
                      <dl className="mt-3 flex flex-wrap gap-x-6 gap-y-1 text-sm">
                        <div><dt className="inline text-muted">{t('yourAnswer')} </dt><dd className="inline font-semibold">{haveAnswers ? describeAnswer(q, answer) : t('notAvailable')}</dd></div>
                        <div><dt className="inline text-muted">{t('correctAnswer')} </dt><dd className="inline font-semibold text-success">{describeCorrect(q)}</dd></div>
                      </dl>
                      <div className="mt-4 rounded-lg bg-background p-3 text-sm">
                        <p className="font-semibold">{t('explanation')}</p>
                        <p className="mt-1 text-muted">{q.explanation}</p>
                      </div>
                      {q.shortcut && (
                        <div className="mt-3 rounded-lg border border-primary/20 bg-primary-soft p-3 text-sm">
                          <p className="flex items-center gap-1.5 font-semibold text-primary"><Lightbulb className="h-4 w-4" aria-hidden />{t('shortcut')}</p>
                          <p className="mt-1 text-primary-hover/80">{q.shortcut}</p>
                        </div>
                      )}
                      <div className="mt-3 flex justify-end" data-print-hide>
                        <Button
                          variant="ghost"
                          size="sm"
                          leftIcon={<Flag className="h-4 w-4" />}
                          disabled={flagged.has(qr.questionId)}
                          onClick={() => setFlagQ({ id: qr.questionId, n: qr.n })}
                        >
                          {flagged.has(qr.questionId) ? t('reportedQuestion') : t('reportThisQuestion')}
                        </Button>
                      </div>
                    </Card>
                  </li>
                );
              })}
            </ol>
          </div>
        )}

        {show('plan') && (
          <div className="space-y-6" data-print-break>
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {report.improvementPlan.map((d) => (
                <Card key={d.day} className="flex flex-col p-5">
                  <div className="flex items-center justify-between">
                    <Badge tone="primary">{t('day', { n: d.day })}</Badge>
                    <span className="text-xs text-muted">{t('minutes', { n: d.minutes })}</span>
                  </div>
                  <h3 className="mt-3 font-semibold">{ct(d.title)}</h3>
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">
                    {d.tasks.map((task) => <li key={task}>{task}</li>)}
                  </ul>
                </Card>
              ))}
            </div>
            {next && (
              <Card className="flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm text-muted">{t('recommendedNext')}</p>
                  <p className="font-semibold">{ct(next.title)}</p>
                  {report.nextTestReason && <p className="mt-1 text-sm text-muted">{t('whyThisTest')} {report.nextTestReason}</p>}
                </div>
                <ButtonLink to={`/exams/${next.id}`}>{t('viewExam')}</ButtonLink>
              </Card>
            )}
          </div>
        )}
      </motion.div>

      <Card className="mt-8 p-5" data-print-hide><ReportRating reportId={report.id} value={report.rating} /></Card>
      {flagQ && (
        <ReportQuestionModal
          open
          onOpenChange={(o) => !o && setFlagQ(null)}
          questionId={flagQ.id}
          questionNumber={flagQ.n}
          onSent={() => setFlagged((s) => new Set(s).add(flagQ.id))}
        />
      )}
      <Notice tone={report.isDemo ? 'warning' : 'info'} className="mt-6">{report.isDemo ? t('demoAiNotice') : t('serverScoredNotice')}{uiLang === 'hi' && (report.isDemo ? ` ${t('narrativeNote')}` : report.language !== 'hi' ? ` ${t('narrativeApiNote')}` : '')}</Notice>
    </div>
  );
}
