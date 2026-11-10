import { Link, useParams } from 'react-router-dom';
import { ArrowRight, CircleCheck, Lightbulb, ShieldCheck, Sparkles, TrendingDown, Trophy, TriangleAlert } from 'lucide-react';
import { formatDate } from '@prepmitra/shared';
import { Badge, ButtonLink, Card, CardBody, CardHeader, EmptyState, LoadingSkeleton } from '@/components/ui';
import { reportService } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT } from '@/i18n';
import { useContentT } from '@/i18n/content';
import { reportMessages } from '@/i18n/messages/report';

/**
 * /shared/reports/:token — the public page behind "Copy share link". Anyone with the link can open it
 * without logging in; the server sends only the score and the written feedback (no name, phone or questions).
 */
export function SharedReportPage() {
  const { token = '' } = useParams();
  const t = useT(reportMessages);
  const ct = useContentT();
  const { data, loading, error } = useAsync(() => reportService.getSharedReport(token), [token]);
  useDocumentTitle(data ? `${data.title} — ${t('sharedEyebrow')}` : t('sharedDocTitle'));

  if (loading) return <div className="mx-auto max-w-3xl py-10"><LoadingSkeleton variant="page" /></div>;
  if (error || !data)
    return (
      <EmptyState
        className="py-16"
        title={t('sharedNotFound')}
        description={t('sharedNotFoundDesc')}
        action={<ButtonLink to="/exams">{t('sharedCta')}</ButtonLink>}
      />
    );

  const sc = data.score;
  return (
    <div className="mx-auto max-w-3xl space-y-6 py-8">
      <div>
        <Badge tone="primary">{t('sharedEyebrow')}</Badge>
        <h1 className="mt-3 text-3xl font-bold tracking-tight">{ct(data.title)}</h1>
        <p className="mt-1 text-sm text-muted">{formatDate(data.createdAt)}</p>
      </div>

      {sc && (
        <Card className="grid grid-cols-2 gap-4 p-5 sm:grid-cols-4" data-testid="shared-score">
          <div><p className="text-xs text-muted">{t('sharedScore')}</p><p className="text-2xl font-bold">{sc.score}<span className="text-base font-medium text-muted">/{sc.maxScore}</span></p></div>
          <div><p className="text-xs text-muted">{t('accuracy')}</p><p className="text-2xl font-bold">{sc.accuracy}%</p></div>
          <div><p className="text-xs text-muted">{t('correctIncorrectSkipped')}</p><p className="text-lg font-semibold">{sc.correct} / {sc.incorrect} / {sc.unanswered}</p></div>
          <div><p className="text-xs text-muted">{t('lostNegative')}</p><p className="text-lg font-semibold text-danger">{sc.negativeMarksLost > 0 ? `−${sc.negativeMarksLost}` : '0'}</p></div>
        </Card>
      )}

      {(data.summary || data.encouragement) && (
        <Card className="flex gap-3 p-5">
          <Sparkles className="mt-0.5 h-5 w-5 shrink-0 text-[#f26b1d]" aria-hidden />
          <div className="space-y-1 text-sm">
            {data.summary && <p className="font-medium">{data.summary}</p>}
            {data.encouragement && <p className="text-secondary">{data.encouragement}</p>}
          </div>
        </Card>
      )}

      <div className="grid gap-6 sm:grid-cols-2">
        <Card>
          <CardHeader title={<span className="flex items-center gap-2 text-success"><Trophy className="h-5 w-5" aria-hidden />{t('strengths')}</span>} />
          <CardBody>
            {data.strengths.length ? (
              <ul className="space-y-2 text-sm">{data.strengths.map((s) => <li key={s} className="flex gap-2"><CircleCheck className="mt-0.5 h-4 w-4 shrink-0 text-success" aria-hidden />{ct(s)}</li>)}</ul>
            ) : <p className="text-sm text-muted">—</p>}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={<span className="flex items-center gap-2 text-danger"><TrendingDown className="h-5 w-5" aria-hidden />{t('weaknesses')}</span>} />
          <CardBody>
            {data.weaknesses.length ? (
              <ul className="space-y-2 text-sm">{data.weaknesses.map((w) => <li key={w.topic}><b>{ct(w.topic)}</b>{w.detail ? ` — ${w.detail}` : ''}</li>)}</ul>
            ) : <p className="text-sm text-muted">{t('noWeakness')}</p>}
          </CardBody>
        </Card>
      </div>

      {data.loopholes.length > 0 && (
        <Card>
          <CardHeader title={<span className="flex items-center gap-2 text-warning-ink"><TriangleAlert className="h-5 w-5" aria-hidden />{t('loopholes')}</span>} />
          <CardBody><ul className="space-y-2 text-sm">{data.loopholes.map((l, i) => <li key={i}>{l.detail || l.title}</li>)}</ul></CardBody>
        </Card>
      )}

      {data.plan.length > 0 && (
        <Card>
          <CardHeader title={<span className="flex items-center gap-2 text-primary"><Lightbulb className="h-5 w-5" aria-hidden />{t('sharedPlan')}</span>} />
          <CardBody>
            <ol className="grid gap-3 sm:grid-cols-2">
              {data.plan.map((d) => (
                <li key={d.day} className="rounded-lg border border-line p-3 text-sm">
                  <p className="font-semibold">{t('day', { n: d.day })} · {ct(d.title)}</p>
                  <p className="mt-1 text-muted">{d.tasks.join(' · ')}</p>
                </li>
              ))}
            </ol>
          </CardBody>
        </Card>
      )}

      <p className="flex items-start gap-2 text-xs text-muted"><ShieldCheck className="mt-0.5 h-4 w-4 shrink-0" aria-hidden />{t('sharedPrivacy')}</p>
      <Link to="/exams" className="inline-flex items-center gap-1.5 text-sm font-semibold text-primary hover:underline">
        {t('sharedCta')} <ArrowRight className="h-4 w-4" aria-hidden />
      </Link>
    </div>
  );
}
