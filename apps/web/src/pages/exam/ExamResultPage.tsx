import { Link, useNavigate, useParams } from 'react-router-dom';
import { ArrowRight, FileText, Timer, TrendingDown, Trophy } from 'lucide-react';
import { formatDuration, getExamById } from '@prepmitra/shared';
import { Badge, ButtonLink, Card, CardBody, CardHeader, DemoBadge, EmptyState, Notice } from '@/components/ui';
import { CheckedSheet } from '@/components/exam/CheckedSheet';
import { SectionChart } from '@/components/charts/Charts';
import { ExamCard } from '@/components/exam/ExamCard';
import { ReportActions } from '@/components/exam/ReportActions';
import { ReportRating } from '@/components/exam/ReportRating';
import { useAuthStore, useExamStore } from '@/store';
import { shortLabel } from '@/features/exam/answers';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { PrintStyles } from '@/components/common/PrintStyles';
import { usePrintMode } from '@/lib/share';
import { useT, useUiLang } from '@/i18n';
import { reportMessages } from '@/i18n/messages/report';


export function ExamResultPage() {
  const { reportId = '' } = useParams();
  const t = useT(reportMessages);
  const lang = useUiLang();
  const report = useExamStore((s) => s.reports[reportId]);
  const firstName = useAuthStore((s) => s.session?.user.name?.split(' ')[0]);
  const navigate = useNavigate();
  useDocumentTitle(report ? t('resultDocTitle', { exam: report.examTitle }) : t('resultFallbackTitle'));
  const { print } = usePrintMode();

  if (!report)
    return (
      <EmptyState
        title={t('resultNotFound')}
        description={t('resultNotFoundDesc')}
        action={<ButtonLink to="/my-tests">{t('viewMyTests')}</ButtonLink>}
      />
    );

  const r = report.result;
  const next = getExamById(report.recommendedNextExamId);

  return (
    <div className="space-y-6">
      <PrintStyles />
      <div>
        <div className="flex flex-wrap gap-2">
          <DemoBadge>{t('demoAnalysis')}</DemoBadge>
          {report.isMini && <Badge tone="success">{t('freeMiniMock')}</Badge>}
          {report.autoSubmitted && <Badge tone="warning" icon={<Timer className="h-3 w-3" />}>{t('autoSubmittedBadge')}</Badge>}
        </div>
        <h1 className="sr-only">{report.examTitle}</h1>
        <p className="mt-2 text-muted">{t('resultIntro')}</p>
      </div>
      <CheckedSheet report={report} studentName={firstName} onOpenPlan={() => navigate(`/reports/${report.id}?tab=plan`)} />

      <ReportActions report={report} onPrint={print} />
      <div data-print-hide>
        <ButtonLink to={`/reports/${report.id}`} size="lg" leftIcon={<FileText className="h-4 w-4" />} rightIcon={<ArrowRight className="h-4 w-4" />}>
          {t('viewDetailedReport')}
        </ButtonLink>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1.4fr_1fr]">
        <Card>
          <CardHeader title={t('sectionWise')} />
          <CardBody>
            <SectionChart data={r.sections.map((s) => ({ name: shortLabel(s.name), correct: s.correct, incorrect: s.incorrect, unanswered: s.unanswered }))} />
            <div className="mt-4 overflow-x-auto">
              <table className="w-full min-w-[480px] text-sm">
                <thead>
                  <tr className="border-b border-line text-left text-muted">
                    <th scope="col" className="py-2 pr-3 font-medium">{t('colSection')}</th>
                    <th scope="col" className="py-2 pr-3 font-medium">{t('colScore')}</th>
                    <th scope="col" className="py-2 pr-3 font-medium">{t('colAccuracy')}</th>
                    <th scope="col" className="py-2 font-medium">{t('colTime')}</th>
                  </tr>
                </thead>
                <tbody>
                  {r.sections.map((s) => (
                    <tr key={s.sectionId} className="border-b border-line last:border-0">
                      <th scope="row" className="py-2 pr-3 text-left font-medium">{s.name}</th>
                      <td className="py-2 pr-3">{s.score}/{s.maxScore}</td>
                      <td className="py-2 pr-3"><Badge tone={s.accuracy >= 75 ? 'success' : s.accuracy >= 50 ? 'warning' : 'danger'}>{s.accuracy}%</Badge></td>
                      <td className="py-2 text-muted">{formatDuration(s.timeSpentSec)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardBody>
        </Card>
        <div className="space-y-6">
          <Card>
            <CardHeader title={t('quickInsights')} />
            <CardBody className="space-y-4">
              <div>
                <p className="flex items-center gap-1.5 text-sm font-semibold text-success"><Trophy className="h-4 w-4" aria-hidden />{t('strengths')}</p>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">
                  {report.strengths.slice(0, 2).map((s) => <li key={s}>{s}</li>)}
                </ul>
              </div>
              <div>
                <p className="flex items-center gap-1.5 text-sm font-semibold text-danger"><TrendingDown className="h-4 w-4" aria-hidden />{t('weaknesses')}</p>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">
                  {report.weaknesses.slice(0, 3).map((w) => <li key={w.topic}><b className="text-ink">{w.topic}</b> — {t('accuracySuffix', { n: w.accuracy })}</li>)}
                  {report.weaknesses.length === 0 && <li>{t('noWeakTopics')}</li>}
                </ul>
              </div>
              <Link to={`/reports/${report.id}`} className="inline-flex items-center gap-1 text-sm font-semibold text-primary hover:underline">
                {t('seeLoopholes')} <ArrowRight className="h-4 w-4" aria-hidden />
              </Link>
            </CardBody>
          </Card>
          <Card className="p-5">
            <ReportRating reportId={report.id} value={report.rating} />
          </Card>
        </div>
      </div>

      {next && (
        <section aria-labelledby="next-mock">
          <h2 id="next-mock" className="mb-3 text-lg font-semibold">{t('recommendedNext')}</h2>
          <div className="max-w-md"><ExamCard exam={next} /></div>
        </section>
      )}
      <Notice tone="warning">{t('demoAiNotice')} {t('percentileNote')}{lang === 'hi' ? ` ${t('narrativeNote')}` : ''}</Notice>
    </div>
  );
}
