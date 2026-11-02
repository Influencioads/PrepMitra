import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  Bookmark, Calculator as CalculatorIcon, ChevronLeft, ChevronRight, CircleCheck, CloudOff, CloudUpload, Eraser, Flag, Info, LayoutGrid, Send,
} from 'lucide-react';
import type { ClipboardEvent, MouseEvent as ReactMouseEvent } from 'react';
import type { Attempt, ExamReport, LanguageCode, PaletteStatus } from '@prepmitra/shared';
import {
  addTimeSpent, answeredCount, clearResponse, countPaletteStatuses, getQuestionById, hasTranslation,
  isAnswered, languageName, localizeQuestion, setAnswer, toggleMarkForReview, toggleOption, visitQuestion,
} from '@prepmitra/shared';
import { Button, ConfirmationDialog, ErrorState, Logo, Modal } from '@/components/ui';
import { CountdownTimer } from '@/components/exam/CountdownTimer';
import { QuestionCard } from '@/components/exam/QuestionCard';
import { PaletteSwatch, QuestionPalette, legendKey } from '@/components/exam/QuestionPalette';
import { Calculator } from '@/components/exam/Calculator';
import { ReportQuestionModal } from '@/components/exam/ReportQuestionModal';
import { ReportProcessing } from '@/components/exam/ReportProcessing';
import { useOnline } from '@/components/common/OfflineBanner';
import { attemptService, errorMessage, examService, reportService } from '@/services';
import { USE_MOCK } from '@/services/mock';
import { track } from '@/lib/analytics';
import { useExamStore, useNotificationStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { examMessages } from '@/i18n/messages/exam';

const STATUS_ORDER: PaletteStatus[] = ['answered', 'answered-marked', 'marked', 'not-answered', 'not-visited'];

export function ExamSessionPage() {
  const { attemptId = '' } = useParams();
  const t = useT(examMessages);
  const attempt = useExamStore((s) => s.attempts[attemptId]);
  const exam = attempt ? examService.getSync(attempt.examId) : undefined;
  useDocumentTitle(exam ? t('examInProgressTitle', { exam: exam.shortTitle }) : t('examFallbackTitle'));

  if (!attempt || !exam)
    return (
      <div className="flex min-h-screen items-center justify-center bg-background p-4">
        <div className="w-full max-w-md">
          <ErrorState title={t('attemptNotFound')} description={t('attemptNotFoundDesc')} />
          <p className="mt-4 text-center text-sm">
            <Link to="/my-tests" className="font-semibold text-primary hover:underline">{t('goToMyTests')}</Link>
          </p>
        </div>
      </div>
    );
  if (attempt.status === 'submitted') return <Navigate to={attempt.reportId ? `/exam-result/${attempt.reportId}` : '/my-tests'} replace />;
  return <ExamSession attempt={attempt} />;
}

function ExamSession({ attempt }: { attempt: Attempt }) {
  const navigate = useNavigate();
  const t = useT(examMessages);
  const exam = examService.getSync(attempt.examId)!;
  const updateAttempt = useExamStore((s) => s.updateAttempt);
  const completeAttempt = useExamStore((s) => s.completeAttempt);
  const pushNotification = useNotificationStore((s) => s.push);

  const [viewLang, setViewLang] = useState<LanguageCode>(attempt.language);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [calcOpen, setCalcOpen] = useState(false);
  const [reportOpen, setReportOpen] = useState(false);
  const [infoOpen, setInfoOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [saveState, setSaveState] = useState<'saved' | 'saving' | 'error'>('saved');
  const [processing, setProcessing] = useState<{ done: boolean } | null>(null);
  const submittingRef = useRef(false);
  const dirtyRef = useRef(false);
  const savingRef = useRef(false);
  const online = useOnline();

  const id = attempt.id;
  const index = attempt.currentIndex;
  const item = attempt.paper[index]!;
  const total = attempt.paper.length;
  const ids = useMemo(() => attempt.paper.map((p) => p.questionId), [attempt.paper]);
  const baseQuestion = getQuestionById(item.questionId)!;
  const translated = hasTranslation(baseQuestion, viewLang);
  const question = localizeQuestion(baseQuestion, viewLang);
  const state = attempt.states[item.questionId];
  const section = exam.sections.find((s) => s.id === item.sectionId);
  const counts = countPaletteStatuses(ids, attempt.states);
  const answered = answeredCount(ids, attempt.states);

  const update = useCallback((fn: (a: Attempt) => Attempt) => updateAttempt(id, fn), [id, updateAttempt]);
  const goTo = useCallback(
    (i: number) => {
      update((a) => visitQuestion(a, Math.max(0, Math.min(a.paper.length - 1, i))));
      setPaletteOpen(false);
    },
    [update],
  );

  // Mark the current question as visited (covers restore after refresh).
  useEffect(() => {
    if (!state?.visited) update((a) => visitQuestion(a, a.currentIndex));
  }, [state?.visited, update]);

  // Time spent on the current question.
  useEffect(() => {
    const t = window.setInterval(() => {
      if (document.visibilityState === 'visible') update((a) => addTimeSpent(a, a.paper[a.currentIndex]!.questionId, 1));
    }, 1000);
    return () => window.clearInterval(t);
  }, [update]);

  // Autosave (plan Day 5): on every change (debounced) and every 10 s, plus a flush when the
  // network returns. The store has already persisted answers to this device.
  const flushSave = useCallback(async () => {
    if (savingRef.current || !dirtyRef.current) return;
    const latest = useExamStore.getState().attempts[id];
    if (!latest || latest.status !== 'in-progress') return;
    savingRef.current = true;
    dirtyRef.current = false;
    setSaveState('saving');
    try {
      await attemptService.saveAnswers(latest);
      setSaveState('saved');
    } catch {
      dirtyRef.current = true;
      setSaveState('error');
    } finally {
      savingRef.current = false;
    }
  }, [id]);

  const statesKey = JSON.stringify(attempt.states, (k, v) => (k === 'timeSpentSec' ? undefined : v));
  const firstRender = useRef(true);
  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
    dirtyRef.current = true;
    setSaveState('saving');
    const t = window.setTimeout(() => void flushSave(), 700);
    return () => window.clearTimeout(t);
  }, [statesKey, flushSave]);

  useEffect(() => {
    const t = window.setInterval(() => {
      dirtyRef.current = true; // also syncs time spent per question
      void flushSave();
    }, 10_000);
    const onOnline = () => {
      dirtyRef.current = true;
      void flushSave();
    };
    window.addEventListener('online', onOnline);
    return () => {
      window.clearInterval(t);
      window.removeEventListener('online', onOnline);
    };
  }, [flushSave]);

  // Tab-switch logging (counted, not punished).
  useEffect(() => {
    const onVis = () => {
      if (document.visibilityState === 'hidden' && !submittingRef.current) {
        update((a) => ({ ...a, tabSwitches: a.tabSwitches + 1 }));
        void attemptService.logEvent(id, { type: 'tab_switch', at: new Date().toISOString() });
        toast(t('tabSwitchToast'), { icon: '⚠️', id: 'tab-switch' });
      }
    };
    document.addEventListener('visibilitychange', onVis);
    return () => document.removeEventListener('visibilitychange', onVis);
  }, [update, id, t]);

  // Light anti-cheat (plan Day 5): no copying, pasting or right-click on the question.
  const blockCopy = (e: ClipboardEvent | ReactMouseEvent) => {
    const tag = (e.target as HTMLElement).tagName;
    if (e.type === 'paste' && (tag === 'INPUT' || tag === 'TEXTAREA')) return; // allow pasting a numeric answer
    e.preventDefault();
    if (e.type === 'copy' || e.type === 'cut') {
      update((a) => ({ ...a, copyAttempts: (a.copyAttempts ?? 0) + 1 }));
      void attemptService.logEvent(id, { type: 'copy_attempt', at: new Date().toISOString() });
      toast(t('copyBlockedToast'), { id: 'copy-blocked' });
    }
  };

  // Warn before leaving mid-exam.
  useEffect(() => {
    const onUnload = (e: BeforeUnloadEvent) => {
      if (submittingRef.current) return;
      e.preventDefault();
    };
    window.addEventListener('beforeunload', onUnload);
    return () => window.removeEventListener('beforeunload', onUnload);
  }, []);

  const submit = useCallback(
    async (auto: boolean) => {
      if (submittingRef.current) return;
      submittingRef.current = true;
      setSubmitting(true);
      const latest = useExamStore.getState().attempts[id];
      if (!latest) return;
      const final: Attempt = { ...latest, submittedAt: new Date().toISOString(), autoSubmitted: auto || undefined };
      const started = Date.now();
      try {
        const immediate = await attemptService.submit(exam, final);
        setConfirmOpen(false);
        setProcessing({ done: false });
        track('exam_submitted', { examId: exam.id, auto, mini: !!final.isMini, answered: answeredCount(final.paper.map((p) => p.questionId), final.states) });
        // Real API: the report is written in a background job — poll every 3 s until ready.
        const report: ExamReport = immediate ?? (await reportService.pollExamReport(final.id, { intervalMs: 3000 }));
        const minMs = USE_MOCK && import.meta.env.MODE !== 'test' ? 2500 : 0;
        const wait = minMs - (Date.now() - started);
        if (wait > 0) await new Promise((r) => setTimeout(r, wait));
        setProcessing({ done: true });
        completeAttempt(final, report);
        pushNotification({
          type: 'result',
          title: t('reportReadyTitle', { exam: exam.shortTitle }),
          body: t('reportReadyBody', { score: report.result.score, max: report.result.maxScore, accuracy: report.result.accuracy }),
          link: `/reports/${report.id}`,
        });
        if (auto) toast(t('autoSubmitted'), { icon: '⏰' });
        else toast.success(t('submitted'));
        navigate(`/exam-result/${report.id}`, { replace: true });
      } catch (e) {
        submittingRef.current = false;
        setSubmitting(false);
        setProcessing(null);
        toast.error(t('submitFailed', { error: errorMessage(e) }));
      }
    },
    [completeAttempt, exam, id, navigate, pushNotification, t],
  );

  const onToggleOption = (optionId: string) =>
    update((a) => setAnswer(a, item.questionId, toggleOption(a.states[item.questionId]?.answer, optionId, baseQuestion.type === 'multiple')));
  const onNumeric = (v: string) => update((a) => setAnswer(a, item.questionId, v === '' ? undefined : { numericValue: v }));
  const onClear = () => update((a) => clearResponse(a, item.questionId));
  const onSaveNext = () => (index < total - 1 ? goTo(index + 1) : setConfirmOpen(true));
  const onMarkNext = () => {
    update((a) => (a.states[item.questionId]?.marked ? a : toggleMarkForReview(a, item.questionId)));
    if (index < total - 1) goTo(index + 1);
    else toast(t('lastQuestionMarked'), { id: 'last-q' });
  };
  const onUnmark = () => update((a) => toggleMarkForReview(a, item.questionId));

  // Keyboard shortcuts (outside text fields): ← / → to move between questions.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement)?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || e.metaKey || e.ctrlKey || e.altKey) return;
      if (document.querySelector('[role="dialog"]')) return;
      if (e.key === 'ArrowRight' && index < total - 1) goTo(index + 1);
      if (e.key === 'ArrowLeft' && index > 0) goTo(index - 1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [goTo, index, total]);

  const marked = !!state?.marked;
  const hasAnswer = isAnswered(state?.answer);
  const palette = <QuestionPalette paper={attempt.paper} states={attempt.states} sections={exam.sections} currentIndex={index} onSelect={goTo} />;

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="sticky top-0 z-20 border-b border-line bg-card">
        <div className="flex h-14 items-center gap-3 px-3 sm:px-5">
          <div className="hidden sm:block"><Logo to="/dashboard" className="pointer-events-none" /></div>
          <div className="min-w-0 flex-1 sm:border-l sm:border-line sm:pl-4">
            <h1 className="truncate text-sm font-semibold sm:text-base">{exam.title}</h1>
            <p className="flex items-center gap-1 text-xs text-muted" aria-live="polite">
              {!online || saveState === 'error' ? (
                <><CloudOff className="h-3 w-3 text-warning-ink" aria-hidden /> {t('offlineSaved')}</>
              ) : saveState === 'saving' ? (
                <><CloudUpload className="h-3 w-3" aria-hidden /> {t('saving')}</>
              ) : (
                <><CircleCheck className="h-3 w-3 text-success" aria-hidden /> {t('saved')}</>
              )}
            </p>
          </div>
          <div className="flex items-center gap-1.5">
            <CountdownTimer endsAt={attempt.endsAt} onExpire={() => void submit(true)} paused={submitting} />
            <button type="button" onClick={() => setInfoOpen(true)} className="rounded-md p-1.5 text-muted hover:bg-stone-100" aria-label={t('aboutDemoTimer')}>
              <Info className="h-4 w-4" />
            </button>
          </div>
          <Button className="hidden sm:inline-flex" variant="success" onClick={() => setConfirmOpen(true)} leftIcon={<Send className="h-4 w-4" />} disabled={submitting}>
            {t('submitTest')}
          </Button>
        </div>
        <nav aria-label={t('sections')} className="flex items-center gap-1 overflow-x-auto border-t border-line px-3 py-1.5 scrollbar-thin sm:px-5">
          {exam.sections.map((s) => {
            const first = attempt.paper.findIndex((p) => p.sectionId === s.id);
            if (first < 0) return null;
            const secIds = attempt.paper.filter((p) => p.sectionId === s.id).map((p) => p.questionId);
            const active = s.id === item.sectionId;
            return (
              <button
                key={s.id}
                type="button"
                onClick={() => goTo(first)}
                aria-current={active ? 'true' : undefined}
                className={cn('shrink-0 rounded-md px-3 py-1.5 text-xs font-medium transition-colors sm:text-sm', active ? 'bg-primary text-white' : 'text-ink/80 hover:bg-stone-100')}
              >
                {s.name} <span className={cn('ml-1 text-xs', active ? 'text-white/80' : 'text-muted')}>{answeredCount(secIds, attempt.states)}/{secIds.length}</span>
              </button>
            );
          })}
        </nav>
      </header>

      <div className="mx-auto grid w-full max-w-7xl flex-1 grid-cols-1 gap-5 p-3 pb-28 sm:p-5 sm:pb-28 lg:grid-cols-[1fr_320px] lg:pb-5">
        <main id="main" className="min-w-0">
          <div className="rounded-[var(--radius-card)] border border-line bg-card p-4 shadow-card sm:p-6">
            <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
              {attempt.language !== 'en' ? (
                <div className="inline-flex rounded-lg border border-line p-0.5" role="group" aria-label={t('questionLanguage')}>
                  {[attempt.language, 'en' as LanguageCode].map((l) => (
                    <button
                      key={l}
                      type="button"
                      aria-pressed={viewLang === l}
                      onClick={() => setViewLang(l)}
                      className={cn('rounded-md px-3 py-1 text-xs font-medium', viewLang === l ? 'bg-primary text-white' : 'text-muted hover:text-ink')}
                    >
                      {languageName(l)}
                    </button>
                  ))}
                </div>
              ) : (
                <span className="text-xs text-muted">{t('languageEnglish')}</span>
              )}
              <div className="flex gap-1">
                {exam.calculatorAllowed && (
                  <Button variant="ghost" size="sm" onClick={() => setCalcOpen(true)} leftIcon={<CalculatorIcon className="h-4 w-4" />}>{t('calculator')}</Button>
                )}
                <Button variant="ghost" size="sm" onClick={() => setReportOpen(true)} leftIcon={<Flag className="h-4 w-4" />}>{t('report')}</Button>
              </div>
            </div>
            {!translated && viewLang !== 'en' && (
              <p className="mb-3 rounded-md bg-warning-soft px-3 py-2 text-xs text-warning-ink">
                {t('noTranslation', { language: languageName(viewLang) })}
              </p>
            )}
            <div
              className="select-none [&_input]:select-text"
              onCopy={blockCopy}
              onCut={blockCopy}
              onPaste={blockCopy}
              onContextMenu={blockCopy}
              data-testid="question-area"
            >
            <QuestionCard
              question={question}
              number={index + 1}
              total={total}
              sectionName={section?.name ?? ''}
              marks={item.marks}
              negativeMarks={item.negativeMarks}
              answer={state?.answer}
              onToggleOption={onToggleOption}
              onNumericChange={onNumeric}
              lang={translated ? viewLang : 'en'}
            />
            </div>
            {marked && (
              <p className="mt-4 inline-flex items-center gap-1.5 rounded-md bg-secondary-soft px-2.5 py-1 text-xs font-medium text-secondary">
                <Bookmark className="h-3.5 w-3.5" aria-hidden /> {t('markedForReview')}{hasAnswer ? t('willBeEvaluated') : ''}
              </p>
            )}
          </div>

          {/* Desktop action bar */}
          <div className="mt-4 hidden flex-wrap items-center gap-2 lg:flex">
            <Button variant="outline" onClick={() => goTo(index - 1)} disabled={index === 0} leftIcon={<ChevronLeft className="h-4 w-4" />}>{t('previous')}</Button>
            {marked ? (
              <Button variant="outline" onClick={onUnmark} leftIcon={<Bookmark className="h-4 w-4" />}>{t('unmarkReview')}</Button>
            ) : (
              <Button variant="secondary" onClick={onMarkNext} leftIcon={<Bookmark className="h-4 w-4" />}>{t('markReviewNext')}</Button>
            )}
            <Button variant="ghost" onClick={onClear} disabled={!hasAnswer} leftIcon={<Eraser className="h-4 w-4" />}>{t('clearResponse')}</Button>
            <Button className="ml-auto" onClick={onSaveNext} rightIcon={<ChevronRight className="h-4 w-4" />}>
              {index < total - 1 ? t('saveNext') : t('saveReview')}
            </Button>
          </div>
        </main>

        <aside className="hidden lg:block" aria-label={t('questionPaletteRegion')}>
          <div className="sticky top-32 rounded-[var(--radius-card)] border border-line bg-card p-4 shadow-card">
            <div className="mb-4 flex items-center justify-between text-sm">
              <span className="font-semibold">{t('questions')}</span>
              <span className="text-muted">{t('answeredOfTotal', { answered, total })}</span>
            </div>
            <div className="max-h-[calc(100vh-18rem)] overflow-y-auto pr-1 scrollbar-thin">{palette}</div>
            <Button variant="success" className="mt-4 w-full" onClick={() => setConfirmOpen(true)} disabled={submitting} leftIcon={<Send className="h-4 w-4" />}>
              {t('submitTest')}
            </Button>
          </div>
        </aside>
      </div>

      {/* Mobile / tablet sticky bar */}
      <div className="fixed inset-x-0 bottom-0 z-20 border-t border-line bg-card p-2 shadow-[0_-4px_12px_rgba(15,23,42,0.06)] lg:hidden">
        <div className="mx-auto flex max-w-3xl items-center gap-2">
          <Button variant="outline" size="lg" className="px-3" onClick={() => goTo(index - 1)} disabled={index === 0} aria-label={t('previousQuestion')}>
            <ChevronLeft className="h-5 w-5" />
          </Button>
          <Button variant="outline" size="lg" className="px-3" onClick={() => setPaletteOpen(true)} aria-label={t('openPalette', { answered, total })}>
            <LayoutGrid className="h-5 w-5" /> <span className="text-sm">{answered}/{total}</span>
          </Button>
          <Button variant={marked ? 'outline' : 'secondary'} size="lg" className="px-3" onClick={marked ? onUnmark : onMarkNext} aria-label={marked ? t('unmarkReview') : t('markReviewNextAria')}>
            <Bookmark className={cn('h-5 w-5', marked && 'fill-current')} />
          </Button>
          <Button variant="ghost" size="lg" className="px-3" onClick={onClear} disabled={!hasAnswer} aria-label={t('clearResponse')}>
            <Eraser className="h-5 w-5" />
          </Button>
          <Button size="lg" className="flex-1 px-3" onClick={onSaveNext}>
            {index < total - 1 ? t('saveNext') : t('review')}
          </Button>
        </div>
      </div>

      <Modal
        open={paletteOpen}
        onOpenChange={setPaletteOpen}
        title={t('questionsCount', { total })}
        description={t('answeredUnanswered', { answered, unanswered: total - answered })}
        footer={
          <Button variant="success" className="w-full" onClick={() => { setPaletteOpen(false); setConfirmOpen(true); }} leftIcon={<Send className="h-4 w-4" />}>
            {t('submitTest')}
          </Button>
        }
      >
        {palette}
      </Modal>

      <ConfirmationDialog
        open={confirmOpen}
        onOpenChange={setConfirmOpen}
        title={t('submitConfirmTitle')}
        description={t('submitConfirmDesc')}
        confirmLabel={t('submitTest')}
        cancelLabel={t('keepWorking')}
        variant="success"
        loading={submitting}
        onConfirm={() => submit(false)}
      >
        <ul className="space-y-2 text-sm">
          {STATUS_ORDER.map((s) => (
            <li key={s} className="flex items-center gap-3">
              <PaletteSwatch status={s} className="h-6 w-6">{counts[s]}</PaletteSwatch>
              <span className="flex-1">{t(legendKey[s])}</span>
              <span className="font-semibold">{counts[s]}</span>
            </li>
          ))}
        </ul>
        {total - answered > 0 && <p className="mt-3 text-xs text-warning-ink">{t('stillUnanswered', { n: total - answered })}</p>}
      </ConfirmationDialog>

      <Modal open={infoOpen} onOpenChange={setInfoOpen} title={t('aboutTimerTitle')} size="sm">
        <p className="text-sm text-muted">{t('demoTimerBody')}</p>
        <p className="mt-3 text-sm text-muted">{t('tabSwitchesSoFar')} <b className="text-ink">{attempt.tabSwitches}</b></p>
        <p className="mt-1 text-sm text-muted">{t('copyAttemptsBlocked')} <b className="text-ink">{attempt.copyAttempts ?? 0}</b></p>
      </Modal>
      {exam.calculatorAllowed && <Calculator open={calcOpen} onOpenChange={setCalcOpen} />}
      {processing && <ReportProcessing examTitle={exam.title} done={processing.done} />}
      <ReportQuestionModal open={reportOpen} onOpenChange={setReportOpen} questionId={item.questionId} questionNumber={index + 1} />
    </div>
  );
}
