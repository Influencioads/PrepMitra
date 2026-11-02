import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ArrowLeft, CalendarDays, ChevronDown, CircleAlert, Gauge, MessageSquareText, RotateCcw, ThumbsUp, TriangleAlert } from 'lucide-react';
import type { InterviewScores } from '@prepmitra/shared';
import { formatDate, formatDuration, languageName } from '@prepmitra/shared';
import {
  Badge, ButtonLink, Card, CardBody, CardHeader, DemoBadge, EmptyState, Notice, PageHeader, ProgressBar, ScoreRing, StatCard,
} from '@/components/ui';
import { SkillRadar } from '@/components/charts/Charts';
import { reportService } from '@/services';
import { useInterviewStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { ReportRating } from '@/components/exam/ReportRating';
import { PrintStyles } from '@/components/common/PrintStyles';
import { ShareActions } from '@/components/common/ShareActions';
import { usePrintMode } from '@/lib/share';
import { track } from '@/lib/analytics';
import { useT, useUiLang } from '@/i18n';
import { LEVEL_KEYS, interviewMessages } from '@/i18n/messages/interview';

type IKey = keyof typeof interviewMessages.en;
const SCORE_LABELS = {
  roleKnowledge: 'scoreRoleKnowledge',
  answerStructure: 'scoreAnswerStructure',
  communication: 'scoreCommunication',
  confidence: 'scoreConfidence',
  resumeConsistency: 'scoreResumeConsistency',
} as const satisfies Record<keyof InterviewScores, IKey>;
const RADAR_LABELS = {
  roleKnowledge: 'radarKnowledge', answerStructure: 'radarStructure', communication: 'radarCommunication', confidence: 'radarConfidence', resumeConsistency: 'radarResume',
} as const satisfies Record<keyof InterviewScores, IKey>;
const tone10 = (v: number) => (v >= 7.5 ? 'success' : v >= 5 ? 'warning' : 'danger') as 'success' | 'warning' | 'danger';

export function InterviewReportPage() {
  const { reportId = '' } = useParams();
  const t = useT(interviewMessages);
  const uiLang = useUiLang();
  const report = useInterviewStore((s) => s.reports[reportId]);
  const [open, setOpen] = useState<string | null>(null);
  useDocumentTitle(report ? t('reportDocTitle', { role: report.roleTitle }) : t('reportFallbackTitle'));
  const { printing, print } = usePrintMode();
  useEffect(() => {
    if (report) track('report_viewed', { reportId: report.id, kind: 'interview', roleId: report.roleId });
  }, [report?.id]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!report)
    return (
      <EmptyState
        icon={<CircleAlert className="h-6 w-6" />}
        title={t('reportNotFound')}
        description={t('reportNotFoundDesc')}
        action={<ButtonLink to="/my-tests">{t('viewMyTests')}</ButtonLink>}
      />
    );

  const keys = Object.keys(SCORE_LABELS) as (keyof InterviewScores)[];
  const radar = keys.map((k) => ({ skill: t(SCORE_LABELS[k]), value: report.scores[k] }));
  const radarShort = keys.map((k) => ({ skill: t(RADAR_LABELS[k]), value: report.scores[k] }));

  return (
    <div className="space-y-6">
      <PrintStyles />
      <Link data-print-hide to="/my-tests" className="inline-flex items-center gap-1.5 text-sm font-medium text-muted hover:text-primary">
        <ArrowLeft className="h-4 w-4" aria-hidden /> {t('myTests')}
      </Link>
      <PageHeader
        eyebrow={<DemoBadge>{t('demoEvaluation')}</DemoBadge>}
        title={t('reportTitle', { role: report.roleTitle })}
        description={t('reportSubtitle', { date: formatDate(report.createdAt), mode: report.mode === 'voice' ? t('modeVoiceShort') : t('modeTextShort'), language: languageName(report.language), level: report.level === 'fresher' ? t(LEVEL_KEYS.fresher.title) : t('years', { level: report.level }) })}
        actions={
          <div className="flex flex-wrap gap-2" data-print-hide>
            <ShareActions onPrint={print} onDownloadHtml={() => { reportService.downloadInterviewReport(report); toast.success(t('downloaded')); }} />
            <ButtonLink to={`/interviews/${report.roleId}`} leftIcon={<RotateCcw className="h-4 w-4" />}>{t('practiseAgain')}</ButtonLink>
          </div>
        }
      />
      <Notice tone="warning">{t('demoAi')}{uiLang === 'hi' ? ` ${t('narrativeNote')}` : ''}</Notice>

      <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
        <Card className="flex flex-col items-center p-6 text-center">
          <ScoreRing value={report.overall * 10} label={`${report.overall}`} sublabel={t('outOf10')} size={140} />
          <p className="mt-4 font-semibold">
            {report.overall >= 7.5 ? t('verdictGood') : report.overall >= 5 ? t('verdictOk') : t('verdictLow')}
          </p>
          <p className="mt-1 text-sm text-muted">{t('answersEvaluated', { n: report.questionFeedback.length, time: formatDuration(report.durationSec) })}</p>
        </Card>
        <Card>
          <CardHeader title={t('skillScores')} description={t('skillScoresDesc')} />
          <CardBody className="grid items-center gap-6 md:grid-cols-2">
            <SkillRadar data={radarShort} height={260} />
            <ul className="space-y-4">
              {radar.map((r) => (
                <li key={r.skill}>
                  <div className="mb-1 flex justify-between text-sm"><span className="font-medium">{r.skill}</span><span className="text-muted">{r.value}/10</span></div>
                  <ProgressBar value={r.value} max={10} tone={tone10(r.value)} size="sm" />
                </li>
              ))}
            </ul>
          </CardBody>
        </Card>
      </div>

      {report.voiceMetrics && (
        <div className="grid gap-4 sm:grid-cols-2">
          <StatCard label={t('speakingPace')} value={t('wpm', { n: report.voiceMetrics.wordsPerMinute })} icon={<Gauge className="h-5 w-5" />} hint={t('paceHint')} />
          <StatCard label={t('fillerWords')} value={report.voiceMetrics.fillerWords} icon={<MessageSquareText className="h-5 w-5" />} hint={t('fillerHint')} />
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        <Card>
          <CardHeader title={t('strengths')} />
          <CardBody>
            <ul className="space-y-2.5 text-sm">
              {report.strengths.map((s) => <li key={s} className="flex gap-2"><ThumbsUp className="mt-0.5 h-4 w-4 shrink-0 text-success" aria-hidden />{s}</li>)}
            </ul>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={t('areasToImprove')} />
          <CardBody>
            <ul className="space-y-2.5 text-sm">
              {report.weaknesses.length === 0 && <li className="text-muted">{t('noGaps')}</li>}
              {report.weaknesses.map((s) => <li key={s} className="flex gap-2"><CircleAlert className="mt-0.5 h-4 w-4 shrink-0 text-warning" aria-hidden />{s}</li>)}
            </ul>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={t('redFlags')} />
          <CardBody>
            <ul className="space-y-2.5 text-sm">
              {report.redFlags.length === 0 && <li className="text-muted">{t('noRedFlags')}</li>}
              {report.redFlags.map((s) => <li key={s} className="flex gap-2"><TriangleAlert className="mt-0.5 h-4 w-4 shrink-0 text-danger" aria-hidden />{s}</li>)}
            </ul>
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardHeader title={t('qbqTitle')} description={t('qbqDesc')} />
        <CardBody className="space-y-3">
          {report.questionFeedback.map((f, i) => {
            const isOpen = printing || open === f.questionId;
            return (
              <div key={f.questionId} className="rounded-lg border border-line">
                <button
                  type="button"
                  aria-expanded={isOpen}
                  aria-controls={`fb-${f.questionId}`}
                  onClick={() => setOpen(isOpen ? null : f.questionId)}
                  className="flex w-full items-start gap-3 p-4 text-left hover:bg-stone-50"
                >
                  <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary-soft text-xs font-semibold text-primary">{i + 1}</span>
                  <span className="flex-1 text-sm font-medium">{f.question}</span>
                  <Badge tone={tone10(f.score)}>{f.score}/10</Badge>
                  <ChevronDown className={cn('h-4 w-4 shrink-0 text-muted transition-transform', isOpen && 'rotate-180')} aria-hidden />
                </button>
                {isOpen && (
                  <div id={`fb-${f.questionId}`} className="space-y-3 border-t border-line p-4 text-sm">
                    <div>
                      <p className="font-semibold">{t('yourAnswer')}</p>
                      <p className="mt-1 whitespace-pre-wrap text-muted">{f.answer}</p>
                    </div>
                    <div className="rounded-lg bg-success-soft p-3"><b className="text-green-800">{t('whatWasGood')} </b>{f.good}</div>
                    <div className="rounded-lg bg-warning-soft p-3"><b className="text-amber-800">{t('suggestedImprovement')} </b>{f.missing}</div>
                    <div className="rounded-lg bg-primary-soft p-3"><b className="text-primary-hover">{t('sampleModelAnswer')} </b>{f.modelAnswer}</div>
                  </div>
                )}
              </div>
            );
          })}
          {report.questionFeedback.length === 0 && <p className="text-sm text-muted">{t('noAnswers')}</p>}
        </CardBody>
      </Card>

      <Card>
        <CardHeader title={t('planTitle')} description={t('planDesc')} />
        <CardBody>
          <ol className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {report.plan.map((d) => (
              <li key={d.day} className="rounded-lg border border-line p-4">
                <p className="flex items-center gap-1.5 text-xs font-semibold text-primary"><CalendarDays className="h-3.5 w-3.5" aria-hidden />{t('dayMinutes', { day: d.day, min: d.minutes })}</p>
                <p className="mt-1 font-semibold">{d.title}</p>
                <ul className="mt-2 list-disc space-y-1 pl-4 text-sm text-muted">{d.tasks.map((task) => <li key={task}>{task}</li>)}</ul>
              </li>
            ))}
          </ol>
        </CardBody>
      </Card>

      <Card className="p-5" data-print-hide><ReportRating kind="interview" reportId={report.id} value={report.rating} /></Card>

      <div className="flex flex-col gap-2 sm:flex-row sm:justify-end" data-print-hide>
        <ButtonLink to="/dashboard" variant="outline">{t('backToDashboard')}</ButtonLink>
        <ButtonLink to="/interviews">{t('tryAnotherRole')}</ButtonLink>
      </div>
    </div>
  );
}
