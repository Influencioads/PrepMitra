import { Link } from 'react-router-dom';
import { Check, Minus } from 'lucide-react';
import type { Plan } from '@prepmitra/shared';
import { PRICES_INCLUDE_GST, planShortName } from '@prepmitra/shared';
import { Card, Notice, PageHeader } from '@/components/ui';
import { PricingCards } from '@/components/marketing/PricingCards';
import { useAuthStore } from '@/store';
import { usePlans } from '@/hooks/usePlans';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT, useUiLang } from '@/i18n';
import { catalogMessages, planCopy } from '@/i18n/messages/catalog';

type CatalogKey = keyof typeof catalogMessages.en;

/** Comparison columns: Free and the monthly Starter, Pro and Topper Combo. */
const COMPARE = ['free', 'starter_monthly', 'pro_monthly', 'combo_monthly'];
const limit = (p: Plan, ...keys: string[]) => keys.reduce((n, k) => n + (p.entitlements.limits[k] ?? 0), 0);

export function PricingPage() {
  const t = useT(catalogMessages);
  const lang = useUiLang();
  useDocumentTitle(t('pricingDocTitle'));
  const user = useAuthStore((s) => s.session?.user);
  const plans = usePlans();
  const PLANS = COMPARE.map((id) => plans.find((p) => p.id === id)).filter((p): p is Plan => !!p);
  const num = (n: number) => (n > 0 ? String(n) : false);

  const comparison: { feature: CatalogKey; values: (boolean | string)[] }[] = [
    { feature: 'cmpFullMocks', values: PLANS.map((p) => (p.group === 'free' ? t('freeMockPerCategory') : num(p.entitlements.fullMocksPerMonth ?? p.credits))) },
    { feature: 'cmpReport', values: PLANS.map(() => true) },
    { feature: 'cmpSectional', values: PLANS.map((p) => num(limit(p, 'sectional_tests'))) },
    { feature: 'cmpDoubts', values: PLANS.map((p) => num(limit(p, 'doubts'))) },
    { feature: 'cmpNotes', values: PLANS.map((p) => num(limit(p, 'personal_notes'))) },
    { feature: 'cmpDecks', values: PLANS.map((p) => num(limit(p, 'topic_decks'))) },
    { feature: 'cmpTutorCredits', values: PLANS.map((p) => num(limit(p, 'smart_credits', 'master_credits'))) },
    { feature: 'cmpTextInterviews', values: PLANS.map((p) => num(limit(p, 'text_interviews'))) },
    { feature: 'cmpPlanner', values: PLANS.map((p) => !!p.entitlements.flags.study_planner) },
    { feature: 'cmpRankPredictor', values: PLANS.map((p) => !!p.entitlements.flags.rank_predictor) },
    { feature: 'cmpAutoRenew', values: PLANS.map((p) => p.isRecurring) },
  ];

  return (
    <div className="container-page py-12 lg:py-16">
      <PageHeader title={t('pricingTitle')} description={t('pricingDesc')} />
      <PricingCards plans={plans} ctaHref={(p) => (user ? '/subscription' : p.id === 'free' ? '/signup' : `/signup?plan=${p.id}`)} />

      <h2 className="mt-16 text-2xl font-bold">{t('comparePlans')}</h2>
      <Card className="mt-5 overflow-x-auto">
        <table className="w-full min-w-[640px] text-sm">
          <thead>
            <tr className="border-b border-line text-left">
              <th scope="col" className="px-5 py-3 font-medium text-muted">{t('feature')}</th>
              {PLANS.map((p) => <th scope="col" key={p.id} className="px-5 py-3 font-semibold">{planCopy(lang, planShortName(p))}</th>)}
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
            <li>{t('refund3')}</li>
            <li>{t('refund4')}</li>
          </ul>
          <Link to="/refund-policy" className="mt-4 inline-block text-sm font-semibold text-primary hover:underline">{t('readRefundPolicy')} →</Link>
        </Card>
        <Card className="p-6">
          <h2 className="text-lg font-semibold">{t('taxesTitle')}</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-muted">
            <li>{PRICES_INCLUDE_GST ? t('gstInclude') : t('gstExclude')}</li>
            <li>{t('tax2')}</li>
            <li>{t('tax3')}</li>
          </ul>
        </Card>
      </div>
      <Notice tone="warning" className="mt-8" title={t('prototype')}>{t('demoPayment')}</Notice>
    </div>
  );
}
