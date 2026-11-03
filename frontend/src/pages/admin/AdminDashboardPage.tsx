import { useMemo } from 'react';
import { Link } from 'react-router-dom';
import { Activity, ClipboardCheck, Flag, IndianRupee, Star, UserCheck, Users } from 'lucide-react';
import { PLATFORM_ANALYTICS, QUALITY_METRICS, formatINR, languageName, relativeTime } from '@prepmitra/shared';
import { Badge, ButtonLink, Card, CardBody, CardHeader, DemoBadge, EmptyState, PageHeader, StatCard } from '@/components/ui';
import { AdminLoadGate, TargetCard } from '@/components/admin/AdminUi';
import { BarListChart, ColumnChart, TrendChart } from '@/components/admin/AdminCharts';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { MODULE_LABELS } from '@/components/admin/labels';
import { selectOpenReviewCount, useAdminStore } from '@/store/adminStore';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/** Last `n` calendar months as { key: 'YYYY-M', label: 'Oct' }. */
function lastMonths(n: number) {
  const d = new Date();
  return Array.from({ length: n }, (_, i) => {
    const m = new Date(d.getFullYear(), d.getMonth() - (n - 1 - i), 1);
    return { key: `${m.getFullYear()}-${m.getMonth()}`, label: MONTHS[m.getMonth()]! };
  });
}
const monthKey = (iso: string) => {
  const d = new Date(iso);
  return `${d.getFullYear()}-${d.getMonth()}`;
};

export function AdminDashboardPage() {
  useDocumentTitle('Admin dashboard');
  const load = useAdminLoad('dashboard');
  const users = useAdminStore((s) => s.users);
  const orders = useAdminStore((s) => s.orders);
  const auditLog = useAdminStore((s) => s.auditLog);
  const openReviews = useAdminStore(selectOpenReviewCount);
  const q = QUALITY_METRICS;

  const stats = useMemo(() => {
    const thisMonth = monthKey(new Date().toISOString());
    const paidOrders = orders.filter((o) => o.status === 'paid');
    const months = lastMonths(6);
    return {
      paidUsers: users.filter((u) => u.planId !== 'free').length,
      blocked: users.filter((u) => u.status === 'blocked').length,
      revenueMonth: paidOrders.filter((o) => monthKey(o.createdAt) === thisMonth).reduce((s, o) => s + o.amountInr, 0),
      revenueTrend: months.map((m) => ({
        label: m.label,
        value: paidOrders.filter((o) => monthKey(o.createdAt) === m.key).reduce((s, o) => s + o.amountInr, 0),
      })),
      signups: months.map((m) => ({ label: m.label, value: users.filter((u) => monthKey(u.joinedAt) === m.key).length })),
    };
  }, [users, orders]);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard"
        description="Platform health, revenue and AI quality at a glance."
        eyebrow={<DemoBadge>Demo data</DemoBadge>}
        actions={
          <ButtonLink to="/admin/review-queue" variant="outline" leftIcon={<ClipboardCheck className="h-4 w-4" />}>
            Review queue{openReviews > 0 ? ` (${openReviews})` : ''}
          </ButtonLink>
        }
      />

      <AdminLoadGate state={load} variant="page">
        <section aria-label="Key metrics" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          <StatCard label="Users" value={users.length.toLocaleString('en-IN')} icon={<Users className="h-5 w-5" />} hint={`${stats.blocked} blocked · demo sample`} />
          <StatCard label="Paid users" value={stats.paidUsers} icon={<UserCheck className="h-5 w-5" />} hint={`${Math.round((stats.paidUsers / Math.max(users.length, 1)) * 100)}% of users`} />
          <StatCard label="Attempts today" value={PLATFORM_ANALYTICS.attemptsToday.toLocaleString('en-IN')} icon={<Activity className="h-5 w-5" />} trend={{ value: 8, label: '%' }} hint=" vs yesterday" />
          <StatCard label="Revenue this month" value={formatINR(stats.revenueMonth)} icon={<IndianRupee className="h-5 w-5" />} hint="Paid orders, GST inclusive" />
          <StatCard label="Avg report rating" value={`${q.avgReportRating.toFixed(1)} / 5`} icon={<Star className="h-5 w-5" />} hint={`${q.ratingDistribution.reduce((s, r) => s + r.count, 0).toLocaleString('en-IN')} ratings`} />
          <StatCard label="Question flag rate" value={`${q.flagRate}%`} icon={<Flag className="h-5 w-5" />} hint="Of served questions, last 7 days" />
        </section>

        <section aria-label="Growth charts" className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Revenue trend" description="Paid orders per month (₹, GST inclusive)" />
            <CardBody>
              <TrendChart data={stats.revenueTrend} name="Revenue" format={(v) => formatINR(Math.round(v))} ariaLabel="Monthly revenue for the last six months" />
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="New signups" description="Users joined per month" />
            <CardBody>
              <ColumnChart data={stats.signups} name="Signups" ariaLabel="New signups per month for the last six months" />
            </CardBody>
          </Card>
          <Card className="lg:col-span-2">
            <CardHeader title="Attempts by exam" description="Average daily attempts, last 30 days" />
            <CardBody>
              <BarListChart
                data={PLATFORM_ANALYTICS.attemptsByExam.map((a) => ({ label: a.label, value: a.attempts }))}
                name="Attempts / day"
                ariaLabel="Average daily attempts for the eight most attempted exams"
              />
            </CardBody>
          </Card>
        </section>

        <section aria-labelledby="ai-quality" className="space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <h2 id="ai-quality" className="text-lg font-semibold">AI quality</h2>
            <Badge tone="warning">Simulated metrics</Badge>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <TargetCard label="AI cost per attempt" value={q.aiCostPerAttemptInr} target={q.aiCostCapInr} higherIsBetter={false} format={(v) => `₹${v.toFixed(1)}`} hint="hard cap" />
            <TargetCard label="Report generation time" value={q.reportGenSec} target={q.reportGenTargetSec} higherIsBetter={false} format={(v) => `${Math.round(v)} s`} hint="p50" />
            <TargetCard label="Answer-verification failures" value={q.verificationFailureRate} target={5} higherIsBetter={false} format={(v) => `${v.toFixed(1)}%`} hint="2nd-model check" />
            <TargetCard label="Avg report rating" value={q.avgReportRating} target={4.2} max={5} format={(v) => v.toFixed(1)} />
          </div>
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader title="Flag rate by exam" description="% of served questions reported by learners" />
              <CardBody>
                <BarListChart
                  data={[...q.flagRateByExam].sort((a, b) => b.rate - a.rate).map((f) => ({ label: f.label, value: f.rate }))}
                  name="Flag rate"
                  format={(v) => `${v}%`}
                  target={{ value: 2, label: '2% limit' }}
                  ariaLabel="Question flag rate per exam"
                />
              </CardBody>
            </Card>
            <div className="grid gap-6">
              <Card>
                <CardHeader title="Flag rate by language" description="Tier 1 languages" />
                <CardBody>
                  <ColumnChart
                    data={q.flagRateByLanguage.map((f) => ({ label: f.language.toUpperCase(), value: f.rate }))}
                    name="Flag rate"
                    format={(v) => `${v}%`}
                    height={200}
                    ariaLabel={`Flag rate per language: ${q.flagRateByLanguage.map((f) => `${languageName(f.language)} ${f.rate}%`).join(', ')}`}
                  />
                </CardBody>
              </Card>
              <Card>
                <CardHeader title="Report ratings" description="Learner ratings of AI reports" />
                <CardBody>
                  <BarListChart
                    data={q.ratingDistribution.map((r) => ({ label: `${r.stars} star${r.stars > 1 ? 's' : ''}`, value: r.count }))}
                    name="Ratings"
                    height={190}
                    ariaLabel="Distribution of report ratings from 5 stars to 1 star"
                  />
                </CardBody>
              </Card>
            </div>
            <Card className="lg:col-span-2">
              <CardHeader title="AI cost per attempt" description="Weekly average (₹) against the ₹20 cap" />
              <CardBody>
                <TrendChart data={q.aiCostTrend} name="Cost / attempt" format={(v) => `₹${v.toFixed(1)}`} target={{ value: q.aiCostCapInr, label: '₹20 cap' }} height={220} ariaLabel="Weekly AI cost per attempt" />
              </CardBody>
            </Card>
          </div>
        </section>

        <Card>
          <CardHeader
            title="Recent activity"
            description="Audit log of admin changes"
            action={<Link to="/admin/settings?tab=audit" className="text-sm font-medium text-primary hover:underline">View full audit log</Link>}
          />
          <CardBody>
            {auditLog.length === 0 ? (
              <EmptyState title="No admin activity yet" description="Changes made in the console will appear here." />
            ) : (
              <ol className="divide-y divide-line">
                {auditLog.slice(0, 8).map((a) => (
                  <li key={a.id} className="flex flex-col gap-1 py-3 sm:flex-row sm:items-center sm:gap-4">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm">
                        <span className="font-semibold">{a.actor}</span> <span className="text-muted">{a.action.toLowerCase()}</span>{' '}
                        <span className="font-medium">{a.target}</span>
                      </p>
                      {a.details && <p className="truncate text-xs text-muted">{a.details}</p>}
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge>{MODULE_LABELS[a.module] ?? a.module}</Badge>
                      <time className="whitespace-nowrap text-xs text-muted" dateTime={a.at}>{relativeTime(a.at)}</time>
                    </div>
                  </li>
                ))}
              </ol>
            )}
          </CardBody>
        </Card>
      </AdminLoadGate>
    </div>
  );
}
