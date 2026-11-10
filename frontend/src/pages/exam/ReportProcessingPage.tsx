import { useCallback, useEffect, useRef, useState } from 'react';
import { Navigate, useNavigate, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Clock, RotateCw, TriangleAlert } from 'lucide-react';
import type { ExamReport } from '@prepmitra/shared';
import { liveCatalog } from '@prepmitra/shared';
import { Button, ButtonLink } from '@/components/ui';
import { ReportProcessing } from '@/components/exam/ReportProcessing';
import { ReportPollError, errorMessage, reportService } from '@/services';
import { useExamStore, useNotificationStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT } from '@/i18n';
import { examMessages } from '@/i18n/messages/exam';

type Phase = { kind: 'polling'; online: boolean } | { kind: 'done' } | { kind: 'failed'; message: string; reportId?: string; creditRestored?: boolean } | { kind: 'slow' };

/**
 * /exam/:attemptId/processing — after submit the server writes the report in a background job.
 * This screen checks GET /v1/attempts/{id}/report every 3 s and opens the result as soon as it is
 * ready. It survives a page refresh (the attempt id is in the URL) and a dropped network.
 */
export function ReportProcessingPage() {
  const { attemptId = '' } = useParams();
  const t = useT(examMessages);
  const navigate = useNavigate();
  const attempt = useExamStore((s) => s.attempts[attemptId]);
  const pushNotification = useNotificationStore((s) => s.push);
  const [phase, setPhase] = useState<Phase>({ kind: 'polling', online: true });
  const [run, setRun] = useState(0);
  const ctrl = useRef<AbortController | null>(null);
  const examTitle = (attempt && liveCatalog.exam(attempt.examId)?.title) || '';
  useDocumentTitle(t('preparingReport'));

  const finish = useCallback(
    (report: ExamReport) => {
      const store = useExamStore.getState();
      const local = store.attempts[attemptId];
      if (local) store.completeAttempt({ ...local, submittedAt: local.submittedAt ?? new Date().toISOString() }, report);
      else useExamStore.setState((s) => ({ reports: { ...s.reports, [report.id]: report } }));
      pushNotification({
        type: 'result',
        title: t('reportReadyTitle', { exam: report.examTitle }),
        body: t('reportReadyBody', { score: report.result.score, max: report.result.maxScore, accuracy: report.result.accuracy }),
        link: `/reports/${report.id}`,
      });
      navigate(`/exam-result/${report.id}`, { replace: true });
    },
    [attemptId, navigate, pushNotification, t],
  );

  useEffect(() => {
    const c = new AbortController();
    ctrl.current = c;
    setPhase({ kind: 'polling', online: true });
    reportService
      .pollExamReport(attemptId, {
        intervalMs: 3000,
        signal: c.signal,
        onNetwork: (online) => !c.signal.aborted && setPhase((p) => (p.kind === 'polling' && p.online !== online ? { kind: 'polling', online } : p)),
      })
      .then((report) => {
        if (c.signal.aborted) return;
        setPhase({ kind: 'done' });
        finish(report);
      })
      .catch((e) => {
        if (c.signal.aborted) return;
        if (e instanceof ReportPollError && e.kind === 'timeout') return setPhase({ kind: 'slow' });
        if (e instanceof ReportPollError && e.kind === 'failed') {
          return setPhase({ kind: 'failed', message: e.message, reportId: e.reportId, creditRestored: e.creditRestored });
        }
        setPhase({ kind: 'failed', message: errorMessage(e) });
      });
    return () => c.abort();
  }, [attemptId, finish, run]);

  // Already has a report on this device (e.g. back button): go straight to it.
  if (attempt?.reportId) return <Navigate to={`/exam-result/${attempt.reportId}`} replace />;

  const retry = async () => {
    if (phase.kind === 'failed' && phase.reportId) {
      try {
        await reportService.retryReport(phase.reportId);
      } catch (e) {
        toast.error(errorMessage(e));
        return;
      }
    }
    setRun((n) => n + 1);
  };

  if (phase.kind === 'polling' || phase.kind === 'done') {
    return <ReportProcessing examTitle={examTitle} done={phase.kind === 'done'} note={phase.kind === 'polling' && !phase.online ? t('reconnecting') : undefined} />;
  }

  const failed = phase.kind === 'failed';
  return (
    <main className="flex min-h-screen items-center justify-center bg-background p-4">
      <div className="w-full max-w-md rounded-2xl border border-line bg-card p-6 text-center shadow-overlay sm:p-8" role="alert">
        <span className={failed ? 'mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-danger-soft text-danger' : 'mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-warning-soft text-warning-ink'}>
          {failed ? <TriangleAlert className="h-6 w-6" aria-hidden /> : <Clock className="h-6 w-6" aria-hidden />}
        </span>
        {examTitle && <p className="mt-4 text-sm font-medium text-muted">{examTitle}</p>}
        <h1 className="mt-1 text-xl font-bold">{failed ? t('reportFailedTitle') : t('reportSlowTitle')}</h1>
        <p className="mt-2 text-sm text-muted">{failed ? phase.message : t('reportSlowBody')}</p>
        {failed && phase.creditRestored && <p className="mt-2 text-sm font-medium text-success">{t('reportFailedCredit')}</p>}
        <div className="mt-6 flex flex-col gap-2 sm:flex-row sm:justify-center">
          <Button onClick={retry} leftIcon={<RotateCw className="h-4 w-4" />}>{failed ? t('tryAgain') : t('checkAgain')}</Button>
          <ButtonLink to="/my-tests" variant="outline">{t('goToMyTests')}</ButtonLink>
        </div>
      </div>
    </main>
  );
}
