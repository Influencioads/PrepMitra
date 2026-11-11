import { Link } from 'react-router-dom';
import { Check, ChevronDown, Minus } from 'lucide-react';
import { PRICES_INCLUDE_GST } from '@prepmitra/shared';
import { Card, Notice, PageHeader } from '@/components/ui';
import { usePlans } from '@/hooks/usePlans';
import { USE_MOCK } from '@/services/mock';
import { interviewsEnabled } from '@/config/launch';
import { PricingCards } from '@/components/marketing/PricingCards';
import { useAuthStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT, useUiLang } from '@/i18n';
import { catalogMessages, planCopy } from '@/i18n/messages/catalog';

type CatalogKey = keyof typeof catalogMessages.en;

export function PricingPage() {
  const t = useT(catalogMessages);
  const lang = useUiLang();
  useDocumentTitle(t('pricingDocTitle'));
  const user = useAuthStore((s) => s.session?.user);
  // GET /v1/plans: the server decides prices, credits, validity and GST.
  const { plans: PLANS } = usePlans();
  const validity = PLANS.find((p) => p.id !== 'free' && p.validityDays)?.validityDays ?? 90;

  const rows: { feature: CatalogKey; values: (boolean | string)[] }[] = [
    { feature: 'cmpCredits', values: PLANS.map((p) => (p.id === 'free' ? t('oneMiniMock') : String(p.credits))) },
    { feature: 'cmpValidity', values: PLANS.map((p) => (p.validityDays ? t('days', { count: p.validityDays }) : t('oneTime'))) },
    { feature: 'cmpReport', values: PLANS.map(() => true) },
    { feature: 'cmpInterviews', values: PLANS.map((p) => p.id !== 'free') },
    { feature: 'cmpAnalytics', values: PLANS.map((p) => p.credits >= 10) },
    { feature: 'cmpAutoRenew', values: PLANS.map((p) => p.isRecurring) },
    { feature: 'cmpPriority', values: PLANS.map((p) => p.id === 'yearly') },
  ];
  // Hide rows no plan offers (e.g. auto-renew in the launch packs) and interviews while they are switched off.
  const comparison = rows.filter((r) => r.values.some((v) => v !== false) && (r.feature !== 'cmpInterviews' || interviewsEnabled()));
  const faqs = ([1, 2, 3, 4, 5, 6, 7] as const).map((n) => ({
    q: t(`faq${n}q` as CatalogKey),
    a: t(`faq${n}a` as CatalogKey, { days: validity }),
  }));

  return (
    <div className="container-page py-12 lg:py-16">
      <PageHeader title={t('pricingTitle')} description={t('pricingDesc')} />
      <PricingCards plans={PLANS} ctaHref={(p) => (user ? (p.id === 'free' ? '/exams/general-aptitude' : `/subscription?plan=${p.id}`) : p.id === 'free' ? '/signup' : `/signup?plan=${p.id}`)} />

      <h2 className="mt-16 text-2xl font-bold">{t('comparePlans')}</h2>
      <Card className="mt-5 overflow-x-auto">
        <table className="w-full min-w-[640px] text-sm">
          <thead>
            <tr className="border-b border-line text-left">
              <th scope="col" className="px-5 py-3 font-medium text-muted">{t('feature')}</th>
              {PLANS.map((p) => <th scope="col" key={p.id} className="px-5 py-3 font-semibold">{planCopy(lang, p.name)}</th>)}
            </tr>
          </thead>
          <tbody>
            {comparison.map((row) => (
              <tr key={row.feature} className="border-b border-line last:border-0">
                <th scope="row" className="px-5 py-3 text-left font-medium">{t(row.feature)}</th>
                {row.values.map((v, i) => (
                  <td key={i} className="px-5 py-3">
                    {typeof v === 'string' ? v : v ? <Check className="h-4 w-4 text-success" aria-label={t('included')} /> : <Minus className="h-4 w-4 text-subtle" aria-label={t('notIncluded')} />}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      <div id="refunds" className="mt-12 grid scroll-mt-24 gap-5 md:grid-cols-2">
        <Card className="p-6">
          <h2 className="text-lg font-semibold">{t('refundsTitle')}</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-muted">
            <li>{t('refund1')}</li>
            <li>{t('refund2')}</li>
            {PLANS.some((p) => p.isRecurring) && <li>{t('refund3')}</li>}
            {PLANS.some((p) => p.isRecurring) && <li>{t('refund4')}</li>}
          </ul>
          <Link to="/refund-policy" className="mt-4 inline-block text-sm font-semibold text-primary hover:underline">{t('readRefundPolicy')} →</Link>
        </Card>
        <Card className="p-6">
          <h2 className="text-lg font-semibold">{t('taxesTitle')}</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-muted">
            <li>{PRICES_INCLUDE_GST ? t('gstInclude') : t('gstExclude')}</li>
            <li>{USE_MOCK ? t('tax2') : t('taxRazorpay')}</li>
            {USE_MOCK && <li>{t('tax3')}</li>}
          </ul>
        </Card>
      </div>
      <section aria-labelledby="faq-h" className="mt-12">
        <h2 id="faq-h" className="text-2xl font-bold">{t('faqTitle')}</h2>
        <div className="mt-5 divide-y divide-line rounded-2xl border border-line bg-card" data-testid="pricing-faq">
          {faqs.map((f, i) => (
            <details key={f.q} className="group px-5 py-4" open={i === 0}>
              <summary className="flex cursor-pointer list-none items-center justify-between gap-4 font-medium [&::-webkit-details-marker]:hidden">
                {f.q}
                <ChevronDown className="h-4 w-4 shrink-0 text-muted transition-transform group-open:rotate-180" aria-hidden />
              </summary>
              <p className="mt-2 text-sm leading-relaxed text-muted">{f.a}</p>
            </details>
          ))}
        </div>
      </section>
      {USE_MOCK && <Notice tone="warning" className="mt-8" title={t('prototype')}>{t('demoPayment')}</Notice>}
    </div>
  );
}
