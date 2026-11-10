import { useMemo, useState } from 'react';
import { Link, Navigate, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { isExamOpen } from '@/config/launch';
import toast from 'react-hot-toast';
import { ArrowLeft, Calculator, CircleAlert, Clock, Coins, FileQuestion, Languages, Play, RotateCcw } from 'lucide-react';
import type { LanguageCode } from '@prepmitra/shared';
import { MINI_MOCK, formatClock, relativeTime, remainingSeconds } from '@prepmitra/shared';
import {
  Badge, Button, ButtonLink, Card, CardBody, CardHeader, Checkbox, ErrorState, LanguageSelector, LoadingSkeleton, Modal, Notice, PageHeader,
} from '@/components/ui';
import { PaletteLegend } from '@/components/exam/QuestionPalette';
import { attemptService, errorMessage, examService } from '@/services';
import { examCreditCost, useAuthStore, useExamStore, useSubscriptionStore } from '@/store';
import { useAsync } from '@/hooks/useAsync';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { track } from '@/lib/analytics';
import { useT } from '@/i18n';
import { examMessages } from '@/i18n/messages/exam';
import { USE_MOCK } from '@/services/mock';
import { commonMessages } from '@/i18n/messages/common';


const RULES = ['rule1', 'rule2', 'rule3', 'rule4', 'rule5', 'rule6'] as const;

export function ExamInstructionsPage() {
  const { id = '' } = useParams();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const t = useT(examMessages);
  const tc = useT(commonMessages);
  const creditsText = (n: number) => (n === 1 ? tc('credit') : tc('credits', { count: n }));
  const user = useAuthStore((s) => s.session?.user);
  const sub = useSubscriptionStore((s) => s.sub);
  const consume = useSubscriptionStore((s) => s.consume);
  const refund = useSubscriptionStore((s) => s.refund);
  const attempts = useExamStore((s) => s.attempts);
  const saveAttempt = useExamStore((s) => s.saveAttempt);
  const { data: exam, loading, error, reload } = useAsync(() => examService.get(id), [id]);
  useDocumentTitle(exam ? t('instructionsDocTitle', { exam: exam.shortTitle }) : t('instructionsTitleFallback'));

  const [language, setLanguage] = useState<LanguageCode | null>(null);
  const [agreed, setAgreed] = useState(false);
  const [agreeError, setAgreeError] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);
  const [noCredits, setNoCredits] = useState(false);

  const resumable = useMemo(
    () => Object.values(attempts).find((a) => a.examId === id && a.status === 'in-progress' && remainingSeconds(a) > 0),
    [attempts, id],
  );

  if (loading) return <LoadingSkeleton variant="page" />;
  if (error || !exam) return <ErrorState title={t('examNotAvailable')} description={error ?? t('examNotLoaded')} onRetry={reload} />;
  // Exams that are not open yet ("Coming soon") cannot be started, even from a direct link.
  if (!isExamOpen(exam)) return <Navigate to={`/exams/${exam.id}`} replace />;

  const lang: LanguageCode = language ?? (user && exam.languages.includes(user.preferredLanguage) ? user.preferredLanguage : 'en');
  // ?mode=mini starts the free 30-minute mini mock (only while the free trial is unused).
  // Real API: the free trial is the dedicated mini-mock exam (exam.isFree), so other exams always run in full.
  const mini = USE_MOCK && params.get('mode') === 'mini' && !sub.freeMiniMockUsed && !exam.isFree;
  const { cost, usesFreeTrial } = examCreditCost(exam, sub, mini ? 'mini' : 'full');
  const enough = usesFreeTrial || sub.credits >= cost;
  const fullQs = exam.sections.length * exam.demo.questionsPerSection;
  const demoQs = mini ? Math.min(MINI_MOCK.maxQuestions, fullQs) : fullQs;
  const durationMin = mini ? MINI_MOCK.durationMin : exam.demo.durationMin;

  const start = async () => {
    if (!agreed) {
      setAgreeError(t('agreeError'));
      return;
    }
    if (!enough) {
      setNoCredits(true);
      return;
    }
    setStarting(true);
    const label = t(mini ? 'labelMiniMock' : 'labelMock', { exam: exam.shortTitle });
    const ok = consume(cost, 'exam-attempt', label, usesFreeTrial);
    if (!ok) {
      setStarting(false);
      setNoCredits(true);
      return;
    }
    try {
      const attempt = await attemptService.start(exam, lang, { mini });
      saveAttempt(attempt);
      track('exam_started', { examId: exam.id, mode: mini ? 'mini' : 'full', language: lang, freeTrial: usesFreeTrial });
      toast.success(usesFreeTrial ? t('miniStarted') : t('creditsUsedStarted', { credits: creditsText(cost) }));
      navigate(`/exam/${attempt.id}`, { replace: true });
    } catch (e) {
      if (!usesFreeTrial) refund(cost, t('couldNotStart', { label }));
      setStarting(false);
      // The server requires a complete profile (name, date of birth, a target, consent) before any exam.
      if ((e as { code?: string })?.code === 'profile_incomplete') {
        toast.error(t('profileIncompleteStart'));
        navigate('/profile', { replace: false });
        return;
      }
      const err = e as { status?: number; code?: string };
      // 402: the server's credit balance is lower than this device thought — refresh it and offer plans.
      if (err?.status === 402 || err?.code === 'insufficient_credits') {
        void import('@/store/sync').then((m) => m.syncCredits()).catch(() => undefined);
        toast.error(t('noCreditsStart'), { id: 'no-credits' });
        setNoCredits(true);
        return;
      }
      // No network: the request never reached the server, so nothing was charged.
      if (err?.status === 0) {
        toast.error(t('offlineStart'), { id: 'offline-start' });
        return;
      }
      toast.error(t('creditRestored', { error: errorMessage(e) }));
    }
  };

  return (
    <div className="mx-auto max-w-4xl">
      <Link to={`/exams/${exam.id}`} className="inline-flex items-center gap-1.5 text-sm font-medium text-muted hover:text-primary">
        <ArrowLeft className="h-4 w-4" aria-hidden /> {t('examDetails')}
      </Link>
      <PageHeader
        className="mt-3"
        title={t('instructionsTitle', { exam: exam.title })}
        description={mini ? t('miniDescription') : t('readCarefully')}
        eyebrow={mini ? <Badge tone="success">{t('freeMiniMock')}</Badge> : undefined}
      />
      {USE_MOCK && params.get('mode') === 'mini' && !mini && !exam.isFree && (
        <Notice tone="info" className="mb-6">{t('miniUsedNotice')}</Notice>
      )}

      {resumable && (
        <Notice
          tone="info"
          className="mb-6"
          title={t('unfinishedTitle')}
          action={<ButtonLink to={`/exam/${resumable.id}`} size="sm" leftIcon={<RotateCcw className="h-4 w-4" />}>{t('resume')}</ButtonLink>}
        >
          {t('unfinishedBody', { when: relativeTime(resumable.startedAt), left: formatClock(remainingSeconds(resumable)) })}
        </Notice>
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_300px]">
        <div className="space-y-6">
          <Card>
            <CardHeader title={USE_MOCK ? t('atAGlance') : t('paperAtAGlance')} description={USE_MOCK ? t('atAGlanceDesc', { exam: exam.shortTitle }) : t('paperAtAGlanceDesc', { exam: exam.shortTitle })} />
            <CardBody>
              <dl className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                {[
                  { icon: FileQuestion, k: t('statQuestions'), v: demoQs },
                  { icon: Clock, k: t('statDuration'), v: t('minValue', { n: durationMin }) },
                  { icon: Languages, k: t('statLanguages'), v: exam.languages.length },
                  { icon: Calculator, k: t('statCalculator'), v: exam.calculatorAllowed ? t('allowed') : t('no') },
                ].map(({ icon: Icon, k, v }) => (
                  <div key={k} className="rounded-lg bg-background p-3">
                    <dt className="flex items-center gap-1.5 text-xs text-muted"><Icon className="h-3.5 w-3.5" aria-hidden />{k}</dt>
                    <dd className="mt-1 text-lg font-semibold">{v}</dd>
                  </div>
                ))}
              </dl>
              <div className="mt-5 overflow-x-auto">
                <table className="w-full min-w-[460px] text-sm">
                  <thead>
                    <tr className="border-b border-line text-left text-muted">
                      <th scope="col" className="py-2 pr-3 font-medium">{t('colSection')}</th>
                      <th scope="col" className="py-2 pr-3 font-medium">{t('colQuestions')}</th>
                      <th scope="col" className="py-2 pr-3 font-medium">{t('colCorrect')}</th>
                      <th scope="col" className="py-2 font-medium">{t('colWrong')}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {exam.sections.map((s) => (
                      <tr key={s.id} className="border-b border-line last:border-0">
                        <th scope="row" className="py-2 pr-3 text-left font-medium">{s.name}</th>
                        <td className="py-2 pr-3">{exam.demo.questionsPerSection}</td>
                        <td className="py-2 pr-3 text-success">+{s.marksPerQuestion}</td>
                        <td className="py-2 text-danger">{s.negativeMarks > 0 ? `−${s.negativeMarks}` : '0'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="mt-3 text-xs text-muted">{t('noNegativeNote', { rule: exam.negativeMarking })}</p>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title={t('generalInstructions')} />
            <CardBody>
              <ol className="list-decimal space-y-2.5 pl-5 text-sm leading-relaxed">
                {RULES.map((r) => <li key={r}>{t(r)}</li>)}
              </ol>
              <h3 className="mt-6 text-sm font-semibold">{t('questionPalette')}</h3>
              <div className="mt-3 max-w-md"><PaletteLegend /></div>
              <Notice tone="info" className="mt-6" title={t('fairPlayTitle')}>
                {t('fairPlayBody')}
              </Notice>
            </CardBody>
          </Card>
        </div>

        <aside className="space-y-4 lg:sticky lg:top-24 lg:self-start">
          <Card className="p-5">
            <LanguageSelector label={t('examLanguage')} value={lang} onChange={setLanguage} allowed={exam.languages} hint={t('examLanguageHint')} />
            <div className="mt-5 flex items-center justify-between rounded-lg bg-background px-3 py-2.5 text-sm">
              <span className="flex items-center gap-1.5 text-muted"><Coins className="h-4 w-4 text-warning" aria-hidden />{t('cost')}</span>
              <span className="font-semibold">{usesFreeTrial ? t('freeTrial') : creditsText(cost)}</span>
            </div>
            <p className="mt-2 text-xs text-muted">{t('youHaveCredits', { credits: creditsText(sub.credits) })}</p>
            {!enough && (
              <p className="mt-2 flex items-start gap-1.5 text-xs font-medium text-danger"><CircleAlert className="mt-0.5 h-3.5 w-3.5 shrink-0" />{t('notEnoughCredits')}</p>
            )}
            <Checkbox
              className="mt-5"
              label={t('agreeLabel')}
              checked={agreed}
              onChange={(e) => {
                setAgreed(e.target.checked);
                setAgreeError(null);
              }}
              error={agreeError ?? undefined}
            />
            <Button size="lg" className="mt-5 w-full" onClick={start} loading={starting} leftIcon={<Play className="h-4 w-4" />}>
              {resumable ? t('startNewAttempt') : t('startTest')}
            </Button>
          </Card>
          {USE_MOCK ? (
            <Notice tone="warning" title={<span className="flex items-center gap-2">{t('demoTimerTitle')} <Badge tone="warning">{t('prototype')}</Badge></span>}>
              {t('demoTimerBody')}
            </Notice>
          ) : (
            <Notice tone="info" title={t('serverTimerTitle')}>{t('serverTimerBody')}</Notice>
          )}
        </aside>
      </div>

      <Modal
        open={noCredits}
        onOpenChange={setNoCredits}
        title={t('needCreditsTitle')}
        description={t('needCreditsDesc', { needed: creditsText(cost), have: sub.credits })}
        size="sm"
        footer={
          <>
            <Button variant="outline" onClick={() => setNoCredits(false)}>{t('notNow')}</Button>
            <Button onClick={() => navigate(`/subscription?returnTo=${encodeURIComponent(`/exams/${exam.id}/instructions`)}`)}>{t('getCredits')}</Button>
          </>
        }
      >
        <p className="text-sm text-muted">{t('needCreditsBody')}</p>
      </Modal>
    </div>
  );
}
