import { Check } from 'lucide-react';
import type { Plan, PlanId } from '@prepmitra/shared';
import { formatINR } from '@prepmitra/shared';
import { getActivePlans } from '@/services/subscriptionService';
import { Button, ButtonLink, Card } from '@/components/ui';
import { cn } from '@/utils/cn';
import { useT, useUiLang } from '@/i18n';
import { catalogMessages, planCopy } from '@/i18n/messages/catalog';
import { Stagger } from '@/components/motion';

const perCredit = (p: Plan) => (p.priceInr > 0 && p.credits > 0 ? Math.round(p.priceInr / p.credits) : 0);

export function PricingCards({
  plans = getActivePlans(), currentPlanId, onSelect, ctaHref,
}: { plans?: Plan[]; currentPlanId?: PlanId; onSelect?: (plan: Plan) => void; ctaHref?: (plan: Plan) => string }) {
  const t = useT(catalogMessages);
  const lang = useUiLang();
  const tx = (s: string) => planCopy(lang, s);
  return (
    <Stagger className={cn('grid gap-5 sm:grid-cols-2', plans.length === 3 ? 'lg:grid-cols-3' : 'xl:grid-cols-4')}>
      {plans.map((p) => {
        const current = currentPlanId === p.id;
        return (
          <Card
            key={p.id}
            className={cn(
              'relative flex flex-col rounded-2xl border-[1.5px] border-ink p-6',
              p.highlighted ? 'border-[2.5px] border-primary bg-primary-soft shadow-[8px_8px_0_var(--color-primary)] xl:-rotate-1' : 'shadow-hard-sm',
            )}
          >
            {p.badge && (
              <span className={cn(
                'absolute -top-4 right-4 rotate-6 rounded-lg border-[2.5px] bg-paper px-2.5 py-1 text-xs font-extrabold uppercase tracking-[0.1em]',
                p.highlighted ? 'border-secondary text-secondary' : 'border-primary text-primary',
              )}>
                {tx(p.badge)}
              </span>
            )}
            <p className={cn('text-[11px] font-bold uppercase tracking-[0.14em]', p.highlighted ? 'text-primary' : 'text-muted')}>{t('admitCard')}</p>
            <h3 className="mt-1 text-xl font-bold">{tx(p.name)}</h3>
            <p className="mt-3">
              <span className="font-display text-4xl font-extrabold tracking-tight">{formatINR(p.priceInr)}</span>
              <span className="text-sm font-semibold text-muted">{p.id === 'monthly' && p.isRecurring ? t('perMonth') : p.id === 'yearly' ? t('perYear') : p.id === 'free' || p.credits > 1 ? '' : t('perCredit')}</span>
            </p>
            <p className="mt-1 h-5 text-xs text-muted">
              {perCredit(p) > 0 && p.credits > 1 ? t('perMock', { amount: formatINR(perCredit(p)) }) : p.id === 'free' ? t('oneTimeTrial') : ''}
              {!!p.gstInr && <span>{perCredit(p) > 0 && p.credits > 1 ? ' · ' : ''}{t('inclGst', { amount: formatINR(p.gstInr) })}</span>}
            </p>
            <p className={cn('mt-4 border-t-2 border-dashed pt-4 text-sm text-muted', p.highlighted ? 'border-[#E7B48F]' : 'border-line-strong')}>{tx(p.description)}</p>
            <ul className="mt-5 space-y-2.5 text-sm">
              {p.features.map((f) => (
                <li key={f} className="flex gap-2"><Check className="mt-0.5 h-4 w-4 shrink-0 text-success" aria-hidden />{tx(f)}</li>
              ))}
            </ul>
            <div className="mt-auto pt-6">
              {current ? (
                <Button variant="outline" className="w-full" disabled>{t('currentPlan')}</Button>
              ) : onSelect ? (
                <Button className={cn('w-full', !p.highlighted && 'border-ink')} variant={p.highlighted ? 'primary' : 'outline'} onClick={() => onSelect(p)} disabled={p.id === 'free'}>
                  {p.id === 'free' ? t('includedNewUsers') : tx(p.cta)}
                </Button>
              ) : (
                <ButtonLink to={ctaHref ? ctaHref(p) : '/signup'} className={cn('w-full', !p.highlighted && 'border-ink')} variant={p.highlighted ? 'primary' : 'outline'}>
                  {tx(p.cta)}
                </ButtonLink>
              )}
            </div>
          </Card>
        );
      })}
    </Stagger>
  );
}
