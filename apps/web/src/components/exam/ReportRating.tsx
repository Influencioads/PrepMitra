import { useState } from 'react';
import toast from 'react-hot-toast';
import { Star } from 'lucide-react';
import { reportService } from '@/services';
import { useExamStore, useInterviewStore } from '@/store';
import { track } from '@/lib/analytics';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { reportMessages } from '@/i18n/messages/report';


const LABELS = ['rate1', 'rate2', 'rate3', 'rate4', 'rate5'] as const;

/** 1–5 rating shown on every report (MVP success metric: average ≥ 4.0). */
export function ReportRating({ reportId, value, kind = 'exam' }: { reportId: string; value?: number; kind?: 'exam' | 'interview' }) {
  const t = useT(reportMessages);
  const rateExam = useExamStore((s) => s.rateReport);
  const rateInterview = useInterviewStore((s) => s.rateReport);
  const rate = kind === 'interview' ? rateInterview : rateExam;
  const [hover, setHover] = useState(0);
  const shown = hover || value || 0;
  const onRate = async (n: number) => {
    rate(reportId, n);
    track('report_rated', { reportId, kind, rating: n });
    await reportService.rate(reportId, n);
    toast.success(t('thanksRating'));
  };
  return (
    <div>
      <p className="text-sm font-medium">{t('rateQuestion')}</p>
      <div className="mt-2 flex items-center gap-1" role="radiogroup" aria-label={t('rateGroup')} onMouseLeave={() => setHover(0)}>
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            key={n}
            type="button"
            role="radio"
            aria-checked={value === n}
            aria-label={n === 1 ? t('starOne', { label: t(LABELS[0]) }) : t('starMany', { n, label: t(LABELS[n - 1]!) })}
            onMouseEnter={() => setHover(n)}
            onClick={() => void onRate(n)}
            className="rounded p-0.5"
          >
            <Star className={cn('h-7 w-7 transition-colors', n <= shown ? 'fill-warning text-warning' : 'text-line-strong')} />
          </button>
        ))}
        <span className="ml-2 text-xs text-muted">{shown ? t(LABELS[shown - 1]!) : value ? '' : t('tapToRate')}</span>
      </div>
    </div>
  );
}
