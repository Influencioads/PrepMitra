import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import * as Dialog from '@radix-ui/react-dialog';
import {
  Bookmark, Calculator as CalculatorIcon, ChevronLeft, ChevronRight, CircleCheck, CloudOff, CloudUpload, Eraser, Flag, Info, LayoutGrid, Send, X,
} from 'lucide-react';
import type { ClipboardEvent, MouseEvent as ReactMouseEvent } from 'react';
import type { Answer, Attempt, ExamReport, LanguageCode, PaletteStatus } from '@prepmitra/shared';
import {
  addTimeSpent, answeredCount, clearResponse, countPaletteStatuses, getQuestionById, hasTranslation,
  isAnswered, languageName, localizeQuestion, setAnswer, toggleMarkForReview, toggleOption, visitQuestion,
} from '@prepmitra/shared';
import { Avatar, Button, ConfirmationDialog, ErrorState, Logo, Modal } from '@/components/ui';
import { CountdownTimer } from '@/components/exam/CountdownTimer';
import { QuestionCard } from '@/components/exam/QuestionCard';
import { PaletteSwatch, QuestionPalette, legendKey } from '@/components/exam/QuestionPalette';
import { Calculator } from '@/components/exam/Calculator';
import { ReportQuestionModal } from '@/components/exam/ReportQuestionModal';
import { ReportProcessing } from '@/components/exam/ReportProcessing';
import { useOnline } from '@/components/common/OfflineBanner';
import { attemptService, errorMessage, examService } from '@/services';
import { USE_MOCK } from '@/services/mock';
import { track } from '@/lib/analytics';
import { useAuthStore, useExamStore, useNotificationStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { useContentT } from '@/i18n/content';
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
  // Submitted but the report is still being written (real API): the processing screen polls for it.
  if (attempt.status === 'submitted') return <Navigate to={attempt.reportId ? `/exam-result/${attempt.reportId}` : `/exam/${attempt.id}/processing`} replace />;
  return <ExamSession attempt={attempt} />;
}

function ExamSession({ attempt }: { attempt: Attempt }) {
  const navigate = useNavigate();
  const t = useT(examMessages);
  const exam = examService.getSync(attempt.examId)!;
  const updateAttempt = useExamStore((s) => s.updateAttempt);
  const completeAttempt = useExamStore((s) => s.completeAttempt);
  const pushNotification = useNotificationStore((s) => s.push);
  const userName = useAuthStore((s) => s.session?.user.name) ?? '';
  const ct = useContentT();

  const [viewLang, setViewLang] = useState<LanguageCode>(attempt.language);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [calcOpen, setCalcOpen] = useState(false);
  const [reportOpen, setReportOpen] = useState(false);
  const [infoOpen, setInfoOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [saveState, setSaveState] = useState<'saved' | 'saving' | 'error'>('saved');
  const [lastSavedAt, setLastSavedAt] = useState<Date | null>(null);
  const [processing, setProcessing] = useState<{ done: boolean } | null>(null);
  const submittingRef = useRef(false);
  /** A submit that failed because the device was offline (true = it was the time-up auto-submit). */
  const pendingSubmitRef = useRef<boolean | null>(null);
  const submitRef = useRef<(auto: boolean) => Promise<void>>(async () => undefined);
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
  // Real CBT: a choice only counts after "Save & Next" / "Mark for Review & Next". Until then it
  // is a draft; moving away (Previous, palette, section tab) discards it.
  const [draft, setDraft] = useState<{ index: number; answer: Answer | undefined } | null>(null);
  const pending = draft && draft.index === index ? draft : null;
  const shownAnswer = pending ? pending.answer : state?.answer;
  const unsaved = !!pending && JSON.stringify(pending.answer ?? null) !== JSON.stringify(state?.answer ?? null);
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
  /** The server has closed this attempt (already submitted, or its time ran out): stop and wait for the report. */
  const closeFromServer = useCallback(
    (code: 'deadline_passed' | 'attempt_closed') => {
      submittingRef.current = true;
      const latest = useExamStore.getState().attempts[id];
      if (latest && latest.status === 'in-progress') {
        useExamStore.getState().saveAttempt({ ...latest, status: 'submitted', submittedAt: new Date().toISOString(), autoSubmitted: code === 'deadline_passed' || undefined });
      }
      toast(t(code === 'deadline_passed' ? 'serverClosedDeadline' : 'serverClosedSubmitted'), { icon: '⏰', id: 'server-closed' });
      navigate(`/exam/${id}/processing`, { replace: true });
    },
    [id, navigate, t],
  );

  const flushSave = useCallback(async () => {
    if (savingRef.current || !dirtyRef.current || submittingRef.current) return;
    const latest = useExamStore.getState().attempts[id];
    if (!latest || latest.status !== 'in-progress') return;
    savingRef.current = true;
    dirtyRef.current = false;
    setSaveState('saving');
    let succeeded = false;
    try {
      const { remainingSec } = await attemptService.saveAnswers(latest);
      succeeded = true;
      setSaveState('saved');
      setLastSavedAt(new Date());
      // The server owns the clock: follow its remaining time if this device has drifted (> 2 s).
      if (remainingSec !== undefined) {
        const serverEnds = Date.now() + remainingSec * 1000;
        const current = useExamStore.getState().attempts[id];
        if (current && Math.abs(serverEnds - new Date(current.endsAt).getTime()) > 2000) {
          updateAttempt(id, (a) => ({ ...a, endsAt: new Date(serverEnds).toISOString() }));
        }
      }
    } catch (e) {
      const code = (e as { code?: string })?.code;
      if (code === 'deadline_passed' || code === 'attempt_closed') return closeFromServer(code);
      dirtyRef.current = true;
      setSaveState('error');
    } finally {
      savingRef.current = false;
      // A change arrived while this save was in flight: save it right away rather than at the next 10 s tick.
      if (succeeded && dirtyRef.current) window.setTimeout(() => void flushSaveRef.current(), 300);
    }
  }, [closeFromServer, id, updateAttempt]);
  const flushSaveRef = useRef(flushSave);
  flushSaveRef.current = flushSave;

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
    const tick = window.setInterval(() => {
      dirtyRef.current = true; // also syncs time spent per question
      void flushSave();
    }, 10_000);
    const onOnline = () => {
      void attemptService.logEvent(id, { type: 'network_online', at: new Date().toISOString() });
      // A submit that failed offline goes through as soon as the network is back.
      if (pendingSubmitRef.current !== null) {
        toast(t('submitRetrying'), { id: 'submit-offline' });
        void submitRef.current(pendingSubmitRef.current);
        return;
      }
      dirtyRef.current = true;
      void flushSave();
    };
    const onOffline = () => void attemptService.logEvent(id, { type: 'network_offline', at: new Date().toISOString() });
    window.addEventListener('online', onOnline);
    window.addEventListener('offline', onOffline);
    // After a refresh: send anything saved only on this device and re-sync the timer with the server.
    dirtyRef.current = true;
    void flushSave();
    void attemptService.flushEvents(id);
    return () => {
      window.clearInterval(tick);
      window.removeEventListener('online', onOnline);
      window.removeEventListener('offline', onOffline);
    };
  }, [flushSave, id]); // eslint-disable-line react-hooks/exhaustive-deps

  // Tab-switch logging (counted, not punished). Refreshing or leaving the page also hides it, so
  // `pagehide` (which fires first) marks those as not-a-tab-switch.
  useEffect(() => {
    let leaving = false;
    const onPageHide = () => {
      leaving = true;
    };
    window.addEventListener('pagehide', onPageHide);
    const onVis = () => {
      if (document.visibilityState === 'hidden' && !submittingRef.current && !leaving) {
        update((a) => ({ ...a, tabSwitches: a.tabSwitches + 1 }));
        void attemptService.logEvent(id, { type: 'tab_switch', at: new Date().toISOString() });
        toast(t('tabSwitchToast'), { icon: '⚠️', id: 'tab-switch' });
      }
    };
    document.addEventListener('visibilitychange', onVis);
    return () => {
      document.removeEventListener('visibilitychange', onVis);
      window.removeEventListener('pagehide', onPageHide);
    };
  }, [update, id, t]);

  // Light anti-cheat (plan Day 5): no copying, pasting or right-click on the question.
  const lastRightClick = useRef(0);
  const blockCopy = (e: ClipboardEvent | ReactMouseEvent) => {
    const tag = (e.target as HTMLElement).tagName;
    if (e.type === 'paste' && (tag === 'INPUT' || tag === 'TEXTAREA')) return; // allow pasting a numeric answer
    e.preventDefault();
    const at = new Date().toISOString();
    if (e.type === 'copy' || e.type === 'cut') {
      update((a) => ({ ...a, copyAttempts: (a.copyAttempts ?? 0) + 1 }));
      void attemptService.logEvent(id, { type: 'copy_attempt', at });
      toast(t('copyBlockedToast'), { id: 'copy-blocked' });
    } else if (e.type === 'paste') {
      void attemptService.logEvent(id, { type: 'paste_attempt', at });
    } else if (e.type === 'contextmenu' && Date.now() - lastRightClick.current > 3000) {
      lastRightClick.current = Date.now(); // one event per burst of right-clicks
      void attemptService.logEvent(id, { type: 'right_click', at });
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
        pendingSubmitRef.current = null;
        setConfirmOpen(false);
        track('exam_submitted', { examId: exam.id, auto, mini: !!final.isMini, answered: answeredCount(final.paper.map((p) => p.questionId), final.states) });
        if (!immediate) {
          // Real API: scoring is done; the report is written in a background job. The processing
          // screen checks every 3 s and opens it when ready (and survives a refresh).
          useExamStore.getState().saveAttempt({ ...final, status: 'submitted' });
          if (auto) toast(t('autoSubmitted'), { icon: '⏰' });
          navigate(`/exam/${id}/processing`, { replace: true });
          return;
        }
        setProcessing({ done: false });
        const report: ExamReport = immediate;
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
        const err = e as { status?: number; code?: string };
        if (err?.code === 'deadline_passed' || err?.code === 'attempt_closed') return closeFromServer(err.code);
        if (err?.status === 0 || (typeof navigator !== 'undefined' && navigator.onLine === false)) {
          // No network: answers are already on this device; submit again when the network returns.
          pendingSubmitRef.current = auto;
          setConfirmOpen(false);
          toast(t('submitOffline'), { icon: '📶', id: 'submit-offline', duration: 8000 });
          return;
        }
        toast.error(t('submitFailed', { error: errorMessage(e) }));
      }
    },
    [closeFromServer, completeAttempt, exam, id, navigate, pushNotification, t],
  );
  submitRef.current = submit;

  const onToggleOption = (optionId: string) =>
    setDraft({ index, answer: toggleOption(shownAnswer, optionId, baseQuestion.type === 'multiple') });
  const onNumeric = (v: string) => setDraft({ index, answer: v === '' ? undefined : { numericValue: v } });
  /** Writes the draft (if any) into the attempt — the palette updates in the same render. */
  const commit = (mark: boolean) => {
    const answer = pending ? pending.answer : state?.answer;
    update((a) => {
      let next = pending ? setAnswer(a, item.questionId, isAnswered(answer) ? answer : undefined) : a;
      // Save & Next removes a review mark; Mark for Review & Next sets it (real CBT behaviour).
      if (mark !== !!next.states[item.questionId]?.marked) next = toggleMarkForReview(next, item.questionId);
      return next;
    });
    setDraft(null);
  };
  const onClear = () => {
    setDraft(null);
    update((a) => clearResponse(a, item.questionId));
  };
  const onSaveNext = () => {
    commit(false);
    if (index < total - 1) goTo(index + 1);
    else setConfirmOpen(true);
  };
  const onMarkNext = () => {
    commit(true);
    if (index < total - 1) goTo(index + 1);
    else toast(t('lastQuestionMarked'), { id: 'last-q' });
  };

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

  const sectionSummary = exam.sections
    .map((sec) => {
      const secIds = attempt.paper.filter((p) => p.sectionId === sec.id).map((p) => p.questionId);
      return { id: sec.id, name: sec.name, total: secIds.length, counts: countPaletteStatuses(secIds, attempt.states) };
    })
    .filter((r) => r.total > 0);
  const onFiveMin = () => {
    if (useExamStore.getState().attempts[id]?.fiveMinWarned) return;
    update((a) => ({ ...a, fiveMinWarned: true }));
    toast(t('fiveMinToast'), { icon: '⏳', id: 'five-min', duration: 8000 });
  };
  const marked = !!state?.marked;
  const hasAnswer = isAnswered(shownAnswer);
  const palette = <QuestionPalette paper={attempt.paper} states={attempt.states} sections={exam.sections} currentIndex={index} onSelect={goTo} />;
  const candidate = (
    <div className="flex items-center gap-3 rounded-xl bg-secondary-soft px-3 py-2.5">
      <Avatar name={userName || t('candidate')} size="sm" />
      <div className="min-w-0">
        <p className="truncate text-sm font-semibold">{userName || t('candidate')}</p>
        <p className="text-xs text-muted">{t('candidate')}</p>
      </div>
      <span className="ml-auto text-xs font-medium text-secondary">{t('answeredOfTotal', { answered, total })}</span>
    </div>
  );

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="sticky top-0 z-20">
        <div className="flex h-14 items-center gap-3 bg-secondary-hover px-3 text-white sm:h-16 sm:px-5">
          <div className="hidden sm:block"><Logo to="/dashboard" light className="pointer-events-none" /></div>
          <div className="min-w-0 flex-1 sm:border-l sm:border-white/15 sm:pl-4">
            <h1 className="truncate text-sm font-semibold text-white sm:text-base">{ct(exam.title)}</h1>
            <p className="flex items-center gap-1 text-xs text-white/70" aria-live="polite">
              {!online || saveState === 'error' ? (
                <><CloudOff className="h-3 w-3 text-marigold" aria-hidden /> {t('offlineSaved')}</>
              ) : saveState === 'saving' ? (
                <><CloudUpload className="h-3 w-3" aria-hidden /> {t('saving')}</>
              ) : (
                <><CircleCheck className="h-3 w-3 text-[#86efac]" aria-hidden /> {lastSavedAt ? t('savedAt', { time: lastSavedAt.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' }) }) : t('saved')}</>
              )}
            </p>
          </div>
          <div className="flex items-center gap-1">
            <CountdownTimer endsAt={attempt.endsAt} onExpire={() => void submit(true)} onWarning={onFiveMin} paused={submitting} variant="dark" />
            <button type="button" onClick={() => setInfoOpen(true)} className="rounded-md p-1.5 text-white/70 hover:bg-white/10 hover:text-white" aria-label={t('aboutDemoTimer')}>
              <Info className="h-4 w-4" />
            </button>
          </div>
          <Button className="hidden bg-[#f26b1d] hover:bg-[#e05e12] sm:inline-flex" onClick={() => setConfirmOpen(true)} leftIcon={<Send className="h-4 w-4" />} disabled={submitting}>
            {t('submitTest')}
          </Button>
        </div>
        <div className="flex items-center gap-2 border-b border-line bg-card px-3 py-2 sm:px-5">
          <nav aria-label={t('sections')} className="flex flex-1 items-center gap-1.5 overflow-x-auto scrollbar-thin">
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
                  className={cn(
                    'shrink-0 rounded-full border px-3.5 py-1.5 text-xs font-medium transition-colors sm:text-sm',
                    active ? 'border-secondary bg-secondary text-white' : 'border-line text-ink/80 hover:border-secondary/40',
                  )}
                >
                  {ct(s.name)} <span className={cn('ml-1 text-xs tabular-nums', active ? 'text-white/75' : 'text-muted')}>{answeredCount(secIds, attempt.states)}/{secIds.length}</span>
                </button>
              );
            })}
          </nav>
          <button
            type="button"
            onClick={() => setPaletteOpen(true)}
            className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-line px-3 py-1.5 text-xs font-semibold text-secondary lg:hidden"
            aria-label={t('openPalette', { answered, total })}
          >
            <LayoutGrid className="h-4 w-4" aria-hidden /> {answered}/{total}
          </button>
        </div>
      </header>

      <div className="mx-auto grid w-full max-w-7xl flex-1 grid-cols-1 gap-5 p-3 pb-24 sm:p-5 sm:pb-24 lg:grid-cols-[1fr_330px] lg:pb-5">
        <main id="main" className="flex min-w-0 flex-col">
          <div className="rounded-2xl border border-line bg-card p-4 sm:p-6">
            <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
              {attempt.language !== 'en' ? (
                <div className="inline-flex rounded-full border border-line p-0.5" role="group" aria-label={t('questionLanguage')}>
                  {[attempt.language, 'en' as LanguageCode].map((l) => (
                    <button
                      key={l}
                      type="button"
                      aria-pressed={viewLang === l}
                      onClick={() => setViewLang(l)}
                      className={cn('rounded-full px-3 py-1 text-xs font-medium', viewLang === l ? 'bg-secondary text-white' : 'text-muted hover:text-ink')}
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
                sectionName={ct(section?.name ?? '')}
                marks={item.marks}
                negativeMarks={item.negativeMarks}
                answer={shownAnswer}
                onToggleOption={onToggleOption}
                onNumericChange={onNumeric}
                lang={translated ? viewLang : 'en'}
                unsaved={unsaved}
              />
            </div>
            {marked && (
              <p className="mt-4 inline-flex items-center gap-1.5 rounded-full bg-[#F3E8FA] px-3 py-1 text-xs font-medium text-[#6B21A8]">
                <Bookmark className="h-3.5 w-3.5 fill-current" aria-hidden /> {t('markedForReview')}{isAnswered(state?.answer) ? t('willBeEvaluated') : ''}
              </p>
            )}
          </div>

          {/* Desktop action bar — same order as the real CBT */}
          <div className="mt-4 hidden items-center gap-2 rounded-2xl border border-line bg-card p-3 lg:flex">
            <Button variant="outline" onClick={onMarkNext} className="border-[#7E22CE]/40 text-[#6B21A8] hover:bg-[#F3E8FA]" leftIcon={<Bookmark className="h-4 w-4" />}>
              {t('markReviewNext')}
            </Button>
            <Button variant="ghost" onClick={onClear} disabled={!hasAnswer} leftIcon={<Eraser className="h-4 w-4" />}>{t('clearResponse')}</Button>
            <div className="ml-auto flex gap-2">
              <Button variant="outline" onClick={() => goTo(index - 1)} disabled={index === 0} leftIcon={<ChevronLeft className="h-4 w-4" />}>{t('previous')}</Button>
              <Button onClick={onSaveNext} className="bg-secondary px-6 hover:bg-secondary-hover" rightIcon={<ChevronRight className="h-4 w-4" />}>
                {index < total - 1 ? t('saveNext') : t('saveReview')}
              </Button>
            </div>
          </div>
        </main>

        <aside className="hidden lg:block" aria-label={t('questionPaletteRegion')}>
          <div className="sticky top-36 space-y-4 rounded-2xl border border-line bg-card p-4">
            {candidate}
            <div className="max-h-[calc(100vh-22rem)] overflow-y-auto pr-1 scrollbar-thin">{palette}</div>
            <Button className="w-full bg-[#f26b1d] hover:bg-[#e05e12]" onClick={() => setConfirmOpen(true)} disabled={submitting} leftIcon={<Send className="h-4 w-4" />}>
              {t('submitTest')}
            </Button>
          </div>
        </aside>
      </div>

      {/* Phone / tablet action bar */}
      <div className="fixed inset-x-0 bottom-0 z-20 border-t border-line bg-card px-2 pb-[max(0.5rem,env(safe-area-inset-bottom))] pt-2 shadow-[0_-6px_16px_rgba(23,74,56,0.08)] lg:hidden">
        <div className="mx-auto flex max-w-3xl items-center gap-1.5">
          <Button variant="outline" size="lg" className="px-3" onClick={() => goTo(index - 1)} disabled={index === 0} aria-label={t('previousQuestion')}>
            <ChevronLeft className="h-5 w-5" />
          </Button>
          <Button variant="outline" size="lg" className="border-[#7E22CE]/40 px-3 text-[#6B21A8]" onClick={onMarkNext} aria-label={t('markReviewNextAria')}>
            <Bookmark className="h-5 w-5" /> <span className="hidden text-sm min-[360px]:inline">{t('markNextShort')}</span>
          </Button>
          <Button variant="ghost" size="lg" className="px-2.5" onClick={onClear} disabled={!hasAnswer} aria-label={t('clearResponse')}>
            <Eraser className="h-5 w-5" />
          </Button>
          <Button size="lg" className="flex-1 bg-secondary px-3 hover:bg-secondary-hover" onClick={onSaveNext}>
            {index < total - 1 ? t('saveNext') : t('review')}
          </Button>
        </div>
      </div>

      {/* Palette drawer (phone / tablet) */}
      <Dialog.Root open={paletteOpen} onOpenChange={setPaletteOpen}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 z-50 bg-stone-900/50 animate-fade-in lg:hidden" />
          <Dialog.Content className="fixed inset-y-0 right-0 z-50 flex w-[88vw] max-w-sm flex-col bg-card shadow-overlay animate-drawer-in focus:outline-none lg:hidden">
            <div className="flex items-start justify-between gap-3 bg-secondary-hover px-5 py-4 text-white">
              <div>
                <Dialog.Title className="text-base font-semibold">{t('questionsCount', { total })}</Dialog.Title>
                <Dialog.Description className="mt-0.5 text-xs text-white/70">{t('answeredUnanswered', { answered, unanswered: total - answered })}</Dialog.Description>
              </div>
              <Dialog.Close className="rounded-md p-1 text-white/80 hover:bg-white/10 hover:text-white" aria-label={t('closePalette')}>
                <X className="h-5 w-5" />
              </Dialog.Close>
            </div>
            <div className="flex-1 space-y-4 overflow-y-auto px-5 py-4 scrollbar-thin">
              {candidate}
              {palette}
            </div>
            <div className="border-t border-line p-4">
              <Button className="w-full bg-[#f26b1d] hover:bg-[#e05e12]" onClick={() => { setPaletteOpen(false); setConfirmOpen(true); }} leftIcon={<Send className="h-4 w-4" />}>
                {t('submitTest')}
              </Button>
            </div>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      <ConfirmationDialog
        open={confirmOpen}
        onOpenChange={setConfirmOpen}
        title={t('submitConfirmTitle')}
        description={t('submitConfirmDesc')}
        confirmLabel={t('submitTest')}
        cancelLabel={t('keepWorking')}
        variant="success"
        size="md"
        loading={submitting}
        onConfirm={() => submit(false)}
      >
        {/* Exam summary like the real CBT: totals, then section by section */}
        <ul className="grid grid-cols-2 gap-2 text-sm sm:grid-cols-3">
          {STATUS_ORDER.map((s) => (
            <li key={s} className="flex items-center gap-2.5 rounded-xl border border-line px-3 py-2">
              <PaletteSwatch status={s} className="h-7 w-7 shrink-0">{counts[s]}</PaletteSwatch>
              <span className="text-xs leading-tight text-muted">{t(legendKey[s])}</span>
            </li>
          ))}
        </ul>
        <div className="mt-4 overflow-x-auto rounded-xl border border-line">
          <table className="w-full text-xs">
            <caption className="sr-only">{t('summaryBySection')}</caption>
            <thead>
              <tr className="border-b border-line bg-background text-muted">
                <th scope="col" className="px-3 py-2 text-left font-medium">{t('colSection')}</th>
                <th scope="col" className="px-2 py-2 text-right font-medium">{t('colQuestions')}</th>
                {STATUS_ORDER.map((st) => (
                  <th key={st} scope="col" className="px-2 py-2 text-right font-medium">
                    <span className="inline-flex justify-end" title={t(legendKey[st])}>
                      <PaletteSwatch status={st} className="h-4 w-4" />
                      <span className="sr-only">{t(legendKey[st])}</span>
                    </span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {sectionSummary.map((row) => (
                <tr key={row.id}>
                  <th scope="row" className="px-3 py-2 text-left font-medium">{ct(row.name)}</th>
                  <td className="px-2 py-2 text-right tabular-nums">{row.total}</td>
                  {STATUS_ORDER.map((st) => <td key={st} className="px-2 py-2 text-right tabular-nums">{row.counts[st]}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {unsaved && <p className="mt-3 text-xs font-medium text-warning-ink">{t('unsavedOnSubmit', { n: index + 1 })}</p>}
        {total - answered > 0 && <p className="mt-2 text-xs text-warning-ink">{t('stillUnanswered', { n: total - answered })}</p>}
      </ConfirmationDialog>

      <Modal open={infoOpen} onOpenChange={setInfoOpen} title={t('aboutTimerTitle')} size="sm">
        <p className="text-sm text-muted">{USE_MOCK ? t('demoTimerBody') : t('serverTimerBody')}</p>
        <p className="mt-3 text-sm text-muted">{t('tabSwitchesSoFar')} <b className="text-ink">{attempt.tabSwitches}</b></p>
        <p className="mt-1 text-sm text-muted">{t('copyAttemptsBlocked')} <b className="text-ink">{attempt.copyAttempts ?? 0}</b></p>
      </Modal>
      {exam.calculatorAllowed && <Calculator open={calcOpen} onOpenChange={setCalcOpen} />}
      {processing && <ReportProcessing examTitle={exam.title} done={processing.done} />}
      <ReportQuestionModal open={reportOpen} onOpenChange={setReportOpen} questionId={item.questionId} questionNumber={index + 1} />
    </div>
  );
}
