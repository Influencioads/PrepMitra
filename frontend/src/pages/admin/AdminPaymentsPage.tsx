import { useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Download, FileDown, IndianRupee, Percent, ReceiptText, RotateCcw, Undo2 } from 'lucide-react';
import toast from 'react-hot-toast';
import type { AdminOrder, AdminSubscription } from '@prepmitra/shared';
import { DISCLAIMERS, formatDate, formatDateTime, formatINR } from '@prepmitra/shared';
import { Badge, Button, ConfirmationDialog, EmptyState, Notice, PageHeader, SearchInput, Select, StatCard, Tabs } from '@/components/ui';
import { AdminLoadGate, DataTable, FilterBar, IconButton, ResultCount, StatusBadge, type Column } from '@/components/admin/AdminUi';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { buildInvoiceHtml, downloadFile, toCsv, todayStamp } from '@/components/admin/download';
import { GATEWAY_LABELS, ORDER_STATUS, PLAN_LABELS, planLabel, planTone } from '@/components/admin/labels';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { useAdminStore } from '@/store/adminStore';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

type Tab = 'orders' | 'subscriptions' | 'refunds';
const STATUS_FILTER = [{ value: 'all', label: 'All statuses' }, ...Object.entries(ORDER_STATUS).map(([value, m]) => ({ value, label: m.label }))];
const GATEWAY_FILTER = [{ value: 'all', label: 'All gateways' }, ...Object.entries(GATEWAY_LABELS).map(([value, label]) => ({ value, label }))];
const PLAN_FILTER = [{ value: 'all', label: 'All plans' }, ...Object.entries(PLAN_LABELS).filter(([v]) => v !== 'free').map(([value, label]) => ({ value, label }))];
const REFUND_REASONS = ['Duplicate payment', 'Exam paper failed to load — credit not used', 'Charged but credits not added', 'Customer request within policy'].map((r) => ({ value: r, label: r }));
const rupees = (n: number) => `₹${n.toLocaleString('en-IN', { maximumFractionDigits: 2 })}`;

const SUB_STATUS = {
  active: { label: 'Active', tone: 'success' as const },
  cancelled: { label: 'Cancelled', tone: 'warning' as const },
  expired: { label: 'Expired', tone: 'neutral' as const },
};

export function AdminPaymentsPage() {
  useDocumentTitle('Payments');
  const load = useAdminLoad('payments');
  const [params, setParams] = useSearchParams();
  const raw = params.get('tab');
  const tab: Tab = raw === 'subscriptions' || raw === 'refunds' ? raw : 'orders';
  const orders = useAdminStore((s) => s.orders);
  const subscriptions = useAdminStore((s) => s.subscriptions);
  const refunds = orders.filter((o) => o.status === 'refunded');

  const summary = useMemo(() => {
    const paid = orders.filter((o) => o.status === 'paid');
    const gross = paid.reduce((s, o) => s + o.amountInr, 0);
    const gst = paid.reduce((s, o) => s + o.gstInr, 0);
    const settled = orders.filter((o) => o.status !== 'pending');
    return {
      gross,
      gst: Math.round(gst * 100) / 100,
      net: Math.round((gross - gst) * 100) / 100,
      refunded: refunds.reduce((s, o) => s + o.amountInr, 0),
      successRate: Math.round((settled.filter((o) => o.status !== 'failed').length / Math.max(settled.length, 1)) * 1000) / 10,
      paidCount: paid.length,
    };
  }, [orders, refunds]);

  return (
    <div className="space-y-5">
      <PageHeader title="Payments" description="Orders, subscriptions, refunds and GST invoices from Razorpay and Cashfree." />
      <Notice tone="warning" title="Demo data — no real payments">
        {DISCLAIMERS.demoPayment} Refunds here only change demo records; production refunds are issued by the backend through the payment gateway.
      </Notice>
      <AdminLoadGate state={load}>
        <section aria-label="Revenue summary" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Gross revenue" value={formatINR(summary.gross)} icon={<IndianRupee className="h-5 w-5" />} hint={`${summary.paidCount} paid orders, GST inclusive`} />
          <StatCard label="Net of GST" value={rupees(summary.net)} icon={<ReceiptText className="h-5 w-5" />} hint={`GST collected ${rupees(summary.gst)}`} />
          <StatCard label="Refunded" value={formatINR(summary.refunded)} icon={<Undo2 className="h-5 w-5" />} hint={`${refunds.length} refunds`} />
          <StatCard label="Payment success rate" value={`${summary.successRate}%`} icon={<Percent className="h-5 w-5" />} hint="Paid + refunded ÷ settled" />
        </section>
        <Tabs
          ariaLabel="Payments view"
          value={tab}
          onChange={(v) => setParams(v === 'orders' ? {} : { tab: v }, { replace: true })}
          items={[
            { value: 'orders', label: 'Orders', count: orders.length },
            { value: 'subscriptions', label: 'Subscriptions', count: subscriptions.length },
            { value: 'refunds', label: 'Refunds', count: refunds.length },
          ]}
        />
        {tab === 'orders' ? <OrdersTab orders={orders} /> : tab === 'subscriptions' ? <SubscriptionsTab subs={subscriptions} /> : <RefundsTab refunds={refunds} />}
      </AdminLoadGate>
    </div>
  );
}

function downloadInvoice(o: AdminOrder) {
  downloadFile(`invoice-${o.invoiceNo.replace(/\//g, '-')}.html`, buildInvoiceHtml(o), 'text/html');
  toast.success(`Invoice ${o.invoiceNo} downloaded`);
}

function exportOrders(rows: AdminOrder[], name: string) {
  const csv = toCsv(
    ['Order ID', 'Invoice', 'User ID', 'User', 'Plan', 'Amount (INR)', 'GST (INR)', 'Taxable (INR)', 'Gateway', 'Method', 'Status', 'Created', 'Refunded', 'Refund reason'],
    rows.map((o) => [
      o.id, o.invoiceNo, o.userId, o.userName, planLabel(o.planId), o.amountInr, o.gstInr, Math.round((o.amountInr - o.gstInr) * 100) / 100,
      GATEWAY_LABELS[o.gateway], o.method, o.status, o.createdAt, o.refundedAt ?? '', o.refundReason ?? '',
    ]),
  );
  downloadFile(`prepmitra-${name}-${todayStamp()}.csv`, csv, 'text/csv');
  toast.success(`Exported ${rows.length} rows to CSV`);
}

function orderColumns(onRefund?: (o: AdminOrder) => void): Column<AdminOrder>[] {
  return [
    {
      key: 'id',
      header: 'Order',
      cell: (o) => (
        <div>
          <p className="font-mono text-xs font-semibold">{o.id}</p>
          <p className="text-xs text-muted">{o.invoiceNo}</p>
        </div>
      ),
    },
    { key: 'user', header: 'User', cell: (o) => <div><p className="whitespace-nowrap font-medium">{o.userName}</p><p className="text-xs text-muted">{o.userId}</p></div> },
    { key: 'plan', header: 'Plan', cell: (o) => <Badge tone={planTone(o.planId)}>{planLabel(o.planId)}</Badge> },
    { key: 'amount', header: 'Amount', className: 'text-right', cell: (o) => <span className="font-semibold tabular-nums">{formatINR(o.amountInr)}</span> },
    { key: 'gst', header: 'GST', className: 'text-right', cell: (o) => <span className="tabular-nums text-muted">{rupees(o.gstInr)}</span> },
    { key: 'gateway', header: 'Gateway', cell: (o) => <span className="whitespace-nowrap">{GATEWAY_LABELS[o.gateway]} <span className="text-xs uppercase text-muted">· {o.method}</span></span> },
    { key: 'status', header: 'Status', cell: (o) => <StatusBadge map={ORDER_STATUS} value={o.status} /> },
    { key: 'date', header: 'Date', cell: (o) => <span className="whitespace-nowrap text-muted">{formatDate(o.createdAt)}</span> },
    {
      key: 'actions',
      header: 'Actions',
      srHeader: true,
      className: 'text-right',
      cell: (o) => (
        <div className="flex justify-end gap-0.5">
          <IconButton label={`Download GST invoice ${o.invoiceNo}`} onClick={() => downloadInvoice(o)} disabled={o.status === 'failed' || o.status === 'pending'}>
            <FileDown className="h-4 w-4" />
          </IconButton>
          {onRefund && (
            <IconButton label={`Refund order ${o.id}`} tone="danger" onClick={() => onRefund(o)} disabled={o.status !== 'paid'}>
              <RotateCcw className="h-4 w-4" />
            </IconButton>
          )}
        </div>
      ),
    },
  ];
}

function OrdersTab({ orders }: { orders: AdminOrder[] }) {
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('all');
  const [gateway, setGateway] = useState('all');
  const [plan, setPlan] = useState('all');
  const [refunding, setRefunding] = useState<AdminOrder | null>(null);
  const [reason, setReason] = useState(REFUND_REASONS[0]!.value);
  const [busy, setBusy] = useState(false);
  const term = useDebounce(search).trim().toLowerCase();
  const columns = orderColumns((o) => {
    setReason(REFUND_REASONS[0]!.value);
    setRefunding(o);
  });

  const rows = useMemo(
    () =>
      orders.filter(
        (o) =>
          (status === 'all' || o.status === status) &&
          (gateway === 'all' || o.gateway === gateway) &&
          (plan === 'all' || o.planId === plan) &&
          (!term || `${o.id} ${o.invoiceNo} ${o.userName} ${o.userId}`.toLowerCase().includes(term)),
      ),
    [orders, status, gateway, plan, term],
  );
  const filtered = status !== 'all' || gateway !== 'all' || plan !== 'all' || !!term;

  const refund = async () => {
    if (!refunding) return;
    setBusy(true);
    try {
      await adminService.refundOrder(refunding.id, reason);
      toast.success(`Refund of ${formatINR(refunding.amountInr)} issued for ${refunding.id} (demo)`);
      setRefunding(null);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <FilterBar>
        <SearchInput value={search} onChange={setSearch} placeholder="Order id, invoice or user" label="Search orders" />
        <Select aria-label="Status" value={status} onChange={(e) => setStatus(e.target.value)} options={STATUS_FILTER} />
        <Select aria-label="Gateway" value={gateway} onChange={(e) => setGateway(e.target.value)} options={GATEWAY_FILTER} />
        <Select aria-label="Plan" value={plan} onChange={(e) => setPlan(e.target.value)} options={PLAN_FILTER} />
      </FilterBar>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <ResultCount count={rows.length} noun="order" onClear={filtered ? () => { setSearch(''); setStatus('all'); setGateway('all'); setPlan('all'); } : undefined} />
        <Button size="sm" variant="outline" leftIcon={<Download className="h-4 w-4" />} onClick={() => exportOrders(rows, 'orders')} disabled={rows.length === 0}>
          Export CSV
        </Button>
      </div>
      <DataTable
        caption="Orders"
        columns={columns}
        rows={rows}
        rowKey={(o) => o.id}
        minWidth={1040}
        empty={<EmptyState icon={<ReceiptText className="h-6 w-6" />} title="No orders match" description="Try a different search or clear the filters." />}
      />
      <ConfirmationDialog
        open={!!refunding}
        onOpenChange={(o) => !o && setRefunding(null)}
        title="Issue refund?"
        description={refunding ? `${formatINR(refunding.amountInr)} to ${refunding.userName} via ${GATEWAY_LABELS[refunding.gateway]} for order ${refunding.id}. ${planLabel(refunding.planId)} credits will be revoked.` : undefined}
        confirmLabel="Issue refund"
        variant="danger"
        loading={busy}
        onConfirm={refund}
      >
        <Select label="Refund reason" value={reason} onChange={(e) => setReason(e.target.value)} options={REFUND_REASONS} />
      </ConfirmationDialog>
    </>
  );
}

function RefundsTab({ refunds }: { refunds: AdminOrder[] }) {
  const base = orderColumns();
  const columns: Column<AdminOrder>[] = [
    ...base.slice(0, 4),
    { key: 'refunded', header: 'Refunded on', cell: (o) => <span className="whitespace-nowrap text-muted">{o.refundedAt ? formatDateTime(o.refundedAt) : '—'}</span> },
    { key: 'reason', header: 'Reason', cell: (o) => <span className="text-muted">{o.refundReason ?? '—'}</span> },
    base[base.length - 1]!,
  ];
  return (
    <>
      <div className="flex justify-end">
        <Button size="sm" variant="outline" leftIcon={<Download className="h-4 w-4" />} onClick={() => exportOrders(refunds, 'refunds')} disabled={refunds.length === 0}>
          Export CSV
        </Button>
      </div>
      <DataTable
        caption="Refunds"
        columns={columns}
        rows={refunds}
        rowKey={(o) => o.id}
        minWidth={900}
        empty={<EmptyState icon={<Undo2 className="h-6 w-6" />} title="No refunds yet" description="Refunds issued from the Orders tab appear here." />}
      />
    </>
  );
}

function SubscriptionsTab({ subs }: { subs: AdminSubscription[] }) {
  const [status, setStatus] = useState('all');
  const rows = subs.filter((s) => status === 'all' || s.status === status);
  const columns: Column<AdminSubscription>[] = [
    { key: 'id', header: 'Subscription', cell: (s) => <span className="font-mono text-xs font-semibold">{s.id}</span> },
    { key: 'user', header: 'User', cell: (s) => <span className="whitespace-nowrap font-medium">{s.userName}</span> },
    { key: 'plan', header: 'Plan', cell: (s) => <Badge tone={planTone(s.planId)}>{planLabel(s.planId)}</Badge> },
    { key: 'amount', header: 'Amount', className: 'text-right', cell: (s) => <span className="tabular-nums">{formatINR(s.amountInr)}</span> },
    { key: 'status', header: 'Status', cell: (s) => <StatusBadge map={SUB_STATUS} value={s.status} /> },
    { key: 'auto', header: 'Auto-renew', cell: (s) => (s.autoRenew ? 'On' : 'Off') },
    { key: 'start', header: 'Started', cell: (s) => <span className="whitespace-nowrap text-muted">{formatDate(s.startedAt)}</span> },
    { key: 'renew', header: 'Renews / ends', cell: (s) => <span className="whitespace-nowrap text-muted">{formatDate(s.renewsAt)}</span> },
  ];
  return (
    <>
      <FilterBar>
        <Select aria-label="Subscription status" value={status} onChange={(e) => setStatus(e.target.value)} options={[{ value: 'all', label: 'All statuses' }, { value: 'active', label: 'Active' }, { value: 'cancelled', label: 'Cancelled' }, { value: 'expired', label: 'Expired' }]} />
      </FilterBar>
      <DataTable
        caption="Subscriptions"
        columns={columns}
        rows={rows}
        rowKey={(s) => s.id}
        minWidth={820}
        empty={<EmptyState title="No subscriptions" description="Monthly and yearly plans appear here." />}
      />
    </>
  );
}
