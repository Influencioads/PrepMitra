import { History, LayoutDashboard, Target } from 'lucide-react';
import type { ExamReport } from '@prepmitra/shared';
import { ButtonLink } from '@/components/ui';
import { ShareActions } from '@/components/common/ShareActions';
import { reportService } from '@/services';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { reportMessages } from '@/i18n/messages/report';


export function ReportActions({ report, className, onPrint }: { report: ExamReport; className?: string; onPrint: () => void }) {
  const t = useT(reportMessages);
  const weakExam = report.weaknesses.length > 0 ? report.examId : report.recommendedNextExamId;
  return (
    <div className={cn('flex flex-wrap gap-2', className)} data-print-hide>
      <ShareActions onPrint={onPrint} onDownloadHtml={() => reportService.downloadExamReport(report)} />
      <ButtonLink to={`/exams/${weakExam}`} variant="secondary" leftIcon={<Target className="h-4 w-4" />}>{t('practiceWeak')}</ButtonLink>
      <ButtonLink to="/my-tests" variant="outline" leftIcon={<History className="h-4 w-4" />}>{t('previousAttempts')}</ButtonLink>
      <ButtonLink to="/dashboard" variant="ghost" leftIcon={<LayoutDashboard className="h-4 w-4" />}>{t('dashboard')}</ButtonLink>
    </div>
  );
}
