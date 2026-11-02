import { useMemo } from 'react';
import { Download } from 'lucide-react';
import toast from 'react-hot-toast';
import { PLATFORM_ANALYTICS, QUALITY_METRICS, categoryLabel } from '@prepmitra/shared';
import { Button, Card, CardBody, CardHeader, DemoBadge, PageHeader } from '@/components/ui';
import { AdminLoadGate, DataTable, TargetCard } from '@/components/admin/AdminUi';
import { BarListChart, ColumnChart, TrendChart } from '@/components/admin/AdminCharts';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { downloadFile, toCsv, todayStamp } from '@/components/admin/download';
import { useAdminStore } from '@/store/adminStore';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

const pct = (v: number) => `${v.toFixed(1)}%`;

export function AdminReportsPage() {
  useDocumentTitle('Reports');
  const load = useAdminLoad('reports');
  const users = useAdminStore((s) => s.users);
  const a = PLATFORM_ANALYTICS;
  const q = QUALITY_METRICS;

  // Sample-based figures from the users in the admin store.
  const sample = useMemo(() => {
    const withAttempt = users.filter((u) => u.attempts.length >= 1).length;
    const withSecond = users.filter((u) => u.attempts.length >= 2).length;
    const paid = users.filter((u) => u.planId !== 'free').length;
    return {
      secondAttempt: withAttempt ? (withSecond / withAttempt) * 100 : 0,
      conversion: users.length ? (paid / users.length) * 100 : 0,
      users: users.length,
    };
  }, [users]);

  const byCategory = a.attemptsByCategory.map((c) => ({ label: categoryLabel(c.category).replace(' Exams', ''), value: c.attempts }));
  const totalRatings = q.ratingDistribution.reduce((s, r) => s + r.count, 0);

  const exportCsv = () => {
    const rows: unknown[][] = [
      ['Summary', 'Second-attempt rate (%)', a.secondAttemptRate, `target ${a.secondAttemptTarget}`],
      ['Summary', 'Free→paid conversion (%)', a.conversionRate, `target ${a.conversionTarget}`],
      ['Summary', 'Average report rating', q.avgReportRating, ''],
      ['Summary', 'Question flag rate (%)', q.flagRate, ''],
      ['Summary', 'AI cost per attempt (INR)', q.aiCostPerAttemptInr, `cap ${q.aiCostCapInr}`],
      ['Summary', 'Report generation time (s)', q.reportGenSec, `target ${q.reportGenTargetSec}`],
      ...a.attemptsByCategory.map((c) => ['Attempts by category', categoryLabel(c.category), c.attempts, '']),
      ...a.attemptsByExam.map((e) => ['Daily attempts by exam', e.label, e.attempts, '']),
      ...a.interviewsByRole.map((r) => ['Interview sessions by role', r.label, r.sessions, '']),
      ...q.ratingDistribution.map((r) => ['Report rating distribution', `${r.stars} stars`, r.count, '']),
      ...a.retentionTrend.map((p) => ['Second-attempt rate by month (%)', p.label, p.value, '']),
      ...a.conversionTrend.map((p) => ['Conversion by month (%)', p.label, p.value, '']),
    ];
    downloadFile(`prepmitra-platform-report-${todayStamp()}.csv`, toCsv(['Section', 'Metric', 'Value', 'Note'], rows), 'text/csv');
    toast.success('Platform report exported to CSV');
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Reports"
        description="Platform analytics against MVP success targets."
        eyebrow={<DemoBadge>Demo analytics</DemoBadge>}
        actions={<Button leftIcon={<Download className="h-4 w-4" />} onClick={exportCsv}>Export CSV</Button>}
      />
      <AdminLoadGate state={load} variant="page">
        <section aria-label="Success targets" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <TargetCard label="Users taking a 2nd attempt" value={a.secondAttemptRate} target={a.secondAttemptTarget} max={60} format={pct} hint="30-day window" />
          <TargetCard label="Free → paid conversion" value={a.conversionRate} target={a.conversionTarget} max={10} format={pct} hint="within 14 days" />
          <TargetCard label="Avg report rating" value={q.avgReportRating} target={4.2} max={5} format={(v) => v.toFixed(1)} hint={`${totalRatings.toLocaleString('en-IN')} ratings`} />
          <TargetCard label="Question flag rate" value={q.flagRate} target={2} higherIsBetter={false} max={4} format={pct} />
        </section>
        <p className="text-xs text-muted">
          Demo sample check: of the {sample.users} users in this console, {pct(sample.secondAttempt)} of those with an attempt took a second one and {pct(sample.conversion)} are on a paid plan.
        </p>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Second-attempt rate" description="Monthly, against the 35% target" />
            <CardBody>
              <TrendChart data={a.retentionTrend} name="2nd attempt" format={(v) => `${v.toFixed(0)}%`} target={{ value: a.secondAttemptTarget, label: '35% target' }} ariaLabel="Monthly second-attempt rate against the 35 percent target" />
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Free → paid conversion" description="Monthly, against the 5% target" />
            <CardBody>
              <TrendChart data={a.conversionTrend} name="Conversion" format={(v) => `${v.toFixed(1)}%`} target={{ value: a.conversionTarget, label: '5% target' }} ariaLabel="Monthly free to paid conversion against the 5 percent target" />
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Attempts by category" description="All-time exam attempts" />
            <CardBody>
              <BarListChart data={byCategory} name="Attempts" format={(v) => v.toLocaleString('en-IN')} ariaLabel="All-time attempts per exam category" />
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Report rating distribution" description="Learner ratings of exam and interview reports" />
            <CardBody>
              <ColumnChart data={q.ratingDistribution.map((r) => ({ label: `${r.stars}★`, value: r.count })).reverse()} name="Ratings" ariaLabel="Number of reports rated 1 to 5 stars" />
            </CardBody>
          </Card>
          <Card className="lg:col-span-2">
            <CardHeader title="Interview sessions by role" description="Last 30 days" />
            <CardBody>
              <BarListChart data={a.interviewsByRole.map((r) => ({ label: r.label, value: r.sessions }))} name="Sessions" format={(v) => v.toLocaleString('en-IN')} ariaLabel="Interview sessions per role in the last 30 days" />
            </CardBody>
          </Card>
        </div>

        <section aria-labelledby="table-view" className="space-y-3">
          <h2 id="table-view" className="text-lg font-semibold">Attempts by category — table</h2>
          <DataTable
            caption="Attempts by category"
            minWidth={420}
            rows={a.attemptsByCategory}
            rowKey={(c) => c.category}
            columns={[
              { key: 'cat', header: 'Category', cell: (c) => categoryLabel(c.category) },
              { key: 'n', header: 'Attempts', className: 'text-right', cell: (c) => <span className="tabular-nums">{c.attempts.toLocaleString('en-IN')}</span> },
              {
                key: 'share',
                header: 'Share',
                className: 'text-right',
                cell: (c) => <span className="tabular-nums text-muted">{pct((c.attempts / a.attemptsByCategory.reduce((s, x) => s + x.attempts, 0)) * 100)}</span>,
              },
            ]}
          />
        </section>
      </AdminLoadGate>
    </div>
  );
}
