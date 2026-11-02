import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Building2, CircleCheck, CircleX, Coins, CreditCard, Download, Landmark, Receipt, RotateCcw, Smartphone, Wallet } from 'lucide-react';
import type { DemoOrder, PaymentMethodLabel, Plan } from '@prepmitra/shared';
import {
  GST_RATE, PRICES_INCLUDE_GST, demoCheckoutSchema, formatDate, formatDateTime, formatINR, getPlanSet, type DemoCheckoutInput,
} from '@prepmitra/shared';
import {
  Badge, Button, ButtonLink, Card, CardBody, CardHeader, Checkbox, ConfirmationDialog, DemoBadge, EmptyState, KeyValue, Modal, Notice, PageHeader,
  StatCard,
} from '@/components/ui';
import { PricingCards } from '@/components/marketing/PricingCards';
import { RadioCards } from '@/components/interview/RadioCards';
import { errorMessage, getActivePlans, gstBreakup, subscriptionService } from '@/services';
import { USE_MOCK } from '@/services/mock';
import { track } from '@/lib/analytics';
import { useAuthStore, useNotificationStore, useSubscriptionStore } from '@/store';
import { downloadBlob, escapeHtml } from '@/features/account/download';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT, useUiLang } from '@/i18n';
import { accountMessages } from '@/i18n/messages/account';
import { commonMessages } from '@/i18n/messages/common';
import { planCopy } from '@/i18n/messages/catalog';

/** Receipt HTML stays English (a downloaded document); on-screen labels use METHOD_KEY. */
const METHOD_LABEL: Record<PaymentMethodLabel, string> = { upi: 'UPI', card: 'Credit / debit card', netbanking: 'Net banking', wallet: 'Wallet' };
const METHOD_KEY = { upi: 'methodUpi', card: 'methodCardLong', netbanking: 'methodNetbanking', wallet: 'methodWallet' } as const satisfies Record<PaymentMethodLabel, keyof typeof accountMessages.en>;
const STATUS_KEY = { active: 'statusActive', trial: 'statusTrial', cancelled: 'statusCancelled', expired: 'statusExpired' } as const;
const STATUS_TONE = { active: 'success', trial: 'info', cancelled: 'warning', expired: 'danger' } as const;
const PLANS = getActivePlans();
/** Looks a plan up in the active set first, then the full set (older orders may use another set). */
const getPlan = (id: string): Plan | undefined => PLANS.find((p) => p.id === id) ?? getPlanSet('full').find((p) => p.id === id);

export function SubscriptionPage() {
  const t = useT(accountMessages);
  const lang = useUiLang();
  useDocumentTitle(t('subDocTitle'));
  const [params, setParams] = useSearchParams();
  const sub = useSubscriptionStore((s) => s.sub);
  const orders = useSubscriptionStore((s) => s.orders);
  const cancelAutoRenew = useSubscriptionStore((s) => s.cancelAutoRenew);
  const user = useAuthStore((s) => s.session?.user);
  const [checkoutPlan, setCheckoutPlan] = useState<Plan | null>(null);
  const [confirmCancel, setConfirmCancel] = useState(false);
  const [cancelling, setCancelling] = useState(false);
  const plan = getPlan(sub.planId) ?? PLANS[0]!;

  useEffect(() => {
    const p = params.get('plan');
    const found = p ? PLANS.find((x) => x.id === p && x.id !== 'free') : undefined;
    if (found) {
      setCheckoutPlan(found);
      const next = new URLSearchParams(params);
      next.delete('plan');
      setParams(next, { replace: true });
    }
  }, [params, setParams]);

  const doCancel = async () => {
    setCancelling(true);
    try {
      await subscriptionService.cancelAutoRenew();
      cancelAutoRenew();
      toast.success(t('autoRenewCancelled'));
      setConfirmCancel(false);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setCancelling(false);
    }
  };

  const downloadReceipt = (o: DemoOrder) => {
    const p = getPlan(o.planId);
    const html = `<!doctype html><html><head><meta charset="utf-8"><title>Receipt ${escapeHtml(o.id)}</title>
<style>body{font-family:"DM Sans",system-ui,sans-serif;max-width:560px;margin:32px auto;color:#1C2321}h1{color:#C2410C}td{padding:6px 0}td:last-child{text-align:right}.n{background:#FFFBEB;border:1px solid #FDE68A;padding:8px;border-radius:8px;font-size:13px}</style></head><body>
<h1>PrepMitra AI — Payment receipt</h1><p class="n">DEMO RECEIPT — no real payment was processed. Not a tax invoice.</p>
<table style="width:100%"><tr><td>Receipt no.</td><td>${escapeHtml(o.id)}</td></tr><tr><td>Date</td><td>${formatDateTime(o.createdAt)}</td></tr>
<tr><td>Billed to</td><td>${escapeHtml(user?.name ?? '')}</td></tr><tr><td>Plan</td><td>${escapeHtml(p?.name ?? o.planId)} (${p?.credits ?? 0} credits)</td></tr>
<tr><td>Method</td><td>${METHOD_LABEL[o.method]}</td></tr><tr><td>Amount (excl. GST)</td><td>${formatINR(Math.round((o.amountInr - o.gstInr) * 100) / 100)}</td></tr>
<tr><td>GST @ ${GST_RATE * 100}%</td><td>${formatINR(o.gstInr)}</td></tr><tr><td><b>Total</b></td><td><b>${formatINR(o.amountInr)}</b></td></tr></table></body></html>`;
    downloadBlob(`PrepMitra-receipt-${o.id}.html`, html, 'text/html');
    toast.success(t('receiptDownloaded'));
  };

  return (
    <div className="space-y-6">
      <PageHeader eyebrow={<DemoBadge>{t('demoBilling')}</DemoBadge>} title={t('subTitle')} description={t('subDesc')} />

      <div className="grid gap-4 lg:grid-cols-[1.4fr_1fr_1fr]">
        <Card className="p-5">
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-sm text-muted">{t('currentPlan')}</p>
              <p className="mt-1 text-2xl font-bold">{planCopy(lang, plan.name)}</p>
            </div>
            <Badge tone={STATUS_TONE[sub.status]}>{t(STATUS_KEY[sub.status])}</Badge>
          </div>
          <dl className="mt-3 divide-y divide-line">
            {sub.renewsAt && <KeyValue label={sub.autoRenew ? t('renewsOn') : t('activeUntil')} value={formatDate(sub.renewsAt)} />}
            <KeyValue label={t('autoRenew')} value={sub.autoRenew ? t('on') : t('off')} />
            <KeyValue label={t('freeMini')} value={sub.freeMiniMockUsed ? t('used') : t('available')} />
          </dl>
          <div className="mt-4 flex flex-wrap gap-2">
            {sub.autoRenew && <Button variant="outline" size="sm" onClick={() => setConfirmCancel(true)}>{t('cancelAutoRenew')}</Button>}
            <Button size="sm" onClick={() => setCheckoutPlan(PLANS.find((p) => p.id === 'monthly')!)}>{t('upgradePlan')}</Button>
          </div>
        </Card>
        <StatCard label={t('availableCredits')} value={sub.credits} icon={<Coins className="h-5 w-5" />} hint={sub.planId === 'monthly' ? t('monthlyExpireHint') : t('oldestFirstHint')} />
        <Card className="flex flex-col justify-between p-5">
          <div>
            <p className="text-sm text-muted">{t('topUpQ')}</p>
            <p className="mt-1 text-lg font-semibold">{t('topUpPrice')}</p>
            <p className="text-xs text-muted">{t('topUpValid')}</p>
          </div>
          <Button variant="secondary" className="mt-4" onClick={() => setCheckoutPlan(PLANS.find((p) => p.id === 'pay-per-mock')!)}>{t('buyOne')}</Button>
        </Card>
      </div>

      <section aria-labelledby="plans-h">
        <h2 id="plans-h" className="mb-4 text-lg font-semibold">{t('comparePlans')}</h2>
        <PricingCards plans={PLANS} currentPlanId={sub.planId} onSelect={setCheckoutPlan} />
      </section>

      <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
        <Card className="min-w-0">
          <CardHeader title={t('usageHistory')} description={t('usageHistoryDesc')} />
          <CardBody className="p-0">
            {sub.ledger.length === 0 ? (
              <div className="p-5"><EmptyState title={t('noActivity')} description={t('noActivityDesc')} className="border-0" /></div>
            ) : (
              <div className="max-h-[420px] overflow-auto scrollbar-thin">
                <table className="w-full min-w-[480px] text-sm">
                  <thead className="sticky top-0 bg-card">
                    <tr className="border-b border-line text-left text-muted">
                      <th scope="col" className="px-5 py-2.5 font-medium">{t('colDate')}</th>
                      <th scope="col" className="px-5 py-2.5 font-medium">{t('colActivity')}</th>
                      <th scope="col" className="px-5 py-2.5 text-right font-medium">{t('colCredits')}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sub.ledger.map((l) => (
                      <tr key={l.id} className="border-b border-line last:border-0">
                        <td className="whitespace-nowrap px-5 py-2.5 text-muted">{formatDate(l.at)}</td>
                        <td className="px-5 py-2.5">
                          {l.label}
                          {l.expiresAt && <span className="block text-xs text-muted">{t('expires', { date: formatDate(l.expiresAt) })}</span>}
                        </td>
                        <td className={cn('px-5 py-2.5 text-right font-semibold', l.delta > 0 ? 'text-success' : l.delta < 0 ? 'text-danger' : 'text-muted')}>
                          {l.delta > 0 ? `+${l.delta}` : l.delta === 0 ? t('free') : l.delta}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardBody>
        </Card>
        <Card className="min-w-0">
          <CardHeader title={t('receipts')} description={t('receiptsDesc')} />
          <CardBody>
            {orders.length === 0 ? (
              <EmptyState icon={<Receipt className="h-6 w-6" />} title={t('noReceipts')} description={t('noReceiptsDesc')} className="border-0 py-6" />
            ) : (
              <ul className="space-y-3">
                {orders.map((o) => (
                  <li key={o.id} className="flex items-center gap-3 rounded-lg border border-line p-3">
                    <Receipt className="h-5 w-5 shrink-0 text-muted" aria-hidden />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium">{planCopy(lang, getPlan(o.planId)?.name ?? o.planId)} · {formatINR(o.amountInr)}</p>
                      <p className="truncate text-xs text-muted">{formatDateTime(o.createdAt)} · {t(METHOD_KEY[o.method])}</p>
                    </div>
                    <Button variant="ghost" size="sm" onClick={() => downloadReceipt(o)} leftIcon={<Download className="h-4 w-4" />} aria-label={t('downloadReceiptAria', { id: o.id })}>{t('receipt')}</Button>
                  </li>
                ))}
              </ul>
            )}
          </CardBody>
        </Card>
      </div>

      <Notice tone="warning" title={t('prototype')}>{t('demoPaymentNotice')}</Notice>

      <CheckoutModal plan={checkoutPlan} onClose={() => setCheckoutPlan(null)} onReceipt={downloadReceipt} />

      <ConfirmationDialog
        open={confirmCancel}
        onOpenChange={setConfirmCancel}
        title={t('cancelTitle')}
        description={t('cancelDesc', { plan: planCopy(lang, plan.name), date: sub.renewsAt ? formatDate(sub.renewsAt) : t('itExpires') })}
        confirmLabel={t('cancelAutoRenew')}
        cancelLabel={t('keepAutoRenew')}
        variant="danger"
        loading={cancelling}
        onConfirm={doCancel}
      />
    </div>
  );
}

function CheckoutModal({ plan, onClose, onReceipt }: { plan: Plan | null; onClose: () => void; onReceipt: (o: DemoOrder) => void }) {
  const t = useT(accountMessages);
  const tc = useT(commonMessages);
  const lang = useUiLang();
  const creditsText = (n: number) => (n === 1 ? tc('credit') : tc('credits', { count: n }));
  const applyOrder = useSubscriptionStore((s) => s.applyOrder);
  const push = useNotificationStore((s) => s.push);
  const sub = useSubscriptionStore((s) => s.sub);
  const [order, setOrder] = useState<DemoOrder | null>(null);
  const [failure, setFailure] = useState<string | null>(null);
  const [simulateFailure, setSimulateFailure] = useState(false);
  const [creditsBefore, setCreditsBefore] = useState(0);
  const { handleSubmit, register, watch, setValue, reset, formState: { errors, isSubmitting } } = useForm<DemoCheckoutInput>({
    resolver: zodResolver(demoCheckoutSchema),
    defaultValues: { planId: 'monthly', method: 'upi', acceptTerms: false },
  });

  useEffect(() => {
    if (plan && plan.id !== 'free') {
      reset({ planId: plan.id, method: 'upi', acceptTerms: false });
      setOrder(null);
      setFailure(null);
      setSimulateFailure(false);
    }
  }, [plan, reset]);

  if (!plan) return null;
  const { base, gst, total } = gstBreakup(plan.priceInr);
  const planName = planCopy(lang, plan.name);

  // `simulate` is passed in (not read from state) so Retry never reuses a stale failure flag.
  const runPay = (simulate: boolean) => handleSubmit(async (v) => {
    setFailure(null);
    track('purchase_started', { planId: v.planId, method: v.method, amount: total });
    try {
      const o = await subscriptionService.createDemoOrder(v.planId, v.method, { simulateFailure: simulate });
      setCreditsBefore(useSubscriptionStore.getState().sub.credits);
      applyOrder(o, plan);
      track('purchase_completed', { planId: v.planId, method: v.method, amount: o.amountInr, credits: plan.credits });
      push({ type: 'payment', title: t('receiptNotifTitle', { amount: formatINR(o.amountInr) }), body: t('receiptNotifBody', { plan: planName, credits: creditsText(plan.credits) }), link: '/subscription' });
      setOrder(o);
      toast.success(t('creditsAddedToast', { credits: creditsText(plan.credits) }));
    } catch (e) {
      track('purchase_failed', { planId: v.planId, method: v.method });
      setFailure(errorMessage(e, t('failedFallback')));
    }
  })();
  const pay = () => runPay(simulateFailure);
  const retry = () => {
    setSimulateFailure(false);
    setFailure(null);
    void runPay(false);
  };

  return (
    <Modal
      open={!!plan}
      onOpenChange={(o) => !o && onClose()}
      title={order ? (USE_MOCK ? t('paymentSuccessDemo') : t('paymentSuccess')) : failure ? t('paymentFailed') : t('checkoutTitle', { plan: planName })}
      description={order || failure ? undefined : USE_MOCK ? t('reviewDemo') : t('reviewLive')}
      footer={
        failure ? (
          <>
            <Button variant="outline" onClick={onClose}>{t('close')}</Button>
            <Button onClick={retry} loading={isSubmitting} leftIcon={<RotateCcw className="h-4 w-4" />}>{t('tryAgain')}</Button>
          </>
        ) : order ? (
          <>
            <Button variant="outline" onClick={() => onReceipt(order)} leftIcon={<Download className="h-4 w-4" />}>{t('downloadReceipt')}</Button>
            <ButtonLink to="/exams" onClick={onClose}>{t('startPractising')}</ButtonLink>
          </>
        ) : (
          <>
            <Button variant="outline" onClick={onClose} disabled={isSubmitting}>{t('cancel')}</Button>
            <Button onClick={() => void pay()} loading={isSubmitting}>{t(USE_MOCK ? 'payDemo' : 'pay', { amount: formatINR(total) })}</Button>
          </>
        )
      }
    >
      {failure ? (
        <div className="flex flex-col items-center py-4 text-center" role="alert">
          <CircleX className="h-12 w-12 text-danger" aria-hidden />
          <p className="mt-3 text-lg font-semibold">{t('failedHeading')}</p>
          {!/^payment failed — no money was deducted/i.test(failure) && failure !== t('failedFallback') && <p className="mt-1 max-w-sm text-sm text-muted">{failure}</p>}
          <p className="mt-3 text-xs text-muted">{t('failedHelp')}</p>
        </div>
      ) : order ? (
        <div className="flex flex-col items-center py-4 text-center">
          <CircleCheck className="h-12 w-12 text-success" aria-hidden />
          <p className="mt-3 text-lg font-semibold">{t('creditsAdded', { credits: creditsText(plan.credits) })}</p>
          <p className="mt-1 text-sm text-muted">{t('orderLine', { id: order.id, amount: formatINR(order.amountInr), method: t(METHOD_KEY[order.method]) })}</p>
          <p className="mt-4 rounded-full bg-success-soft px-4 py-1.5 text-sm font-semibold text-success" data-testid="new-balance">
            {t('newBalance', { n: sub.credits })} <span className="font-normal text-muted">{t('wasBalance', { n: creditsBefore })}</span>
          </p>
        </div>
      ) : (
        <form onSubmit={(e) => { e.preventDefault(); void pay(); }} className="space-y-5">
          <div className="rounded-lg bg-background p-4">
            <p className="font-semibold">{planName}</p>
            <p className="text-sm text-muted">{creditsText(plan.credits)}{plan.validityDays ? t('validDays', { n: plan.validityDays }) : ''}{plan.isRecurring ? t('autoRenewsMonthly') : ''}</p>
            <dl className="mt-3 divide-y divide-line">
              <KeyValue label={t('priceExcl')} value={formatINR(base)} />
              <KeyValue label={t('gstAt', { rate: GST_RATE * 100 })} value={formatINR(gst)} />
              <KeyValue label={<b className="text-ink">{t('totalPayable')}</b>} value={formatINR(total)} />
            </dl>
            <p className="mt-1 text-xs text-muted">{PRICES_INCLUDE_GST ? t('pricesInclude') : t('pricesExclude')}</p>
          </div>
          <RadioCards<PaymentMethodLabel>
            label={t('paymentMethod')}
            columns={2}
            value={watch('method')}
            onChange={(v) => setValue('method', v, { shouldValidate: true })}
            options={[
              { value: 'upi', title: t('methodUpi'), description: t('methodUpiDesc'), icon: <Smartphone className="h-5 w-5" /> },
              { value: 'card', title: t('methodCard'), description: t('methodCardDesc'), icon: <CreditCard className="h-5 w-5" /> },
              { value: 'netbanking', title: t('methodNetbanking'), description: t('methodNetbankingDesc'), icon: <Landmark className="h-5 w-5" /> },
              { value: 'wallet', title: t('methodWallet'), description: t('methodWalletDesc'), icon: <Wallet className="h-5 w-5" /> },
            ]}
            error={errors.method?.message}
          />
          <Notice tone="info" title={t('noDetailsTitle')}>
            <span className="inline-flex items-center gap-1"><Building2 className="h-3.5 w-3.5" aria-hidden />{t('noDetailsBody')}</span>
          </Notice>
          {USE_MOCK && (
            <Checkbox
              label={t('simulateFail')}
              description={t('simulateFailDesc')}
              checked={simulateFailure}
              onChange={(e) => setSimulateFailure(e.target.checked)}
            />
          )}
          <Checkbox label={t('agreeRefund')} description={t('agreeRefundDesc')} error={errors.acceptTerms?.message} {...register('acceptTerms')} />
          <p className="text-xs text-muted">{t('demoPaymentNotice')}</p>
        </form>
      )}
    </Modal>
  );
}
