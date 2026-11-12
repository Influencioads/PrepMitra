import { useState, type ReactNode } from 'react';
import { Check } from 'lucide-react';
import type { Plan, PlanId, PlanPeriod } from '@prepmitra/shared';
import { conflictingPlan, formatINR, groupPlans, periodSaving, planShortName } from '@prepmitra/shared';
import { getActivePlans } from '@/services/subscriptionService';
import { Button, ButtonLink, Card } from '@/components/ui';
import { cn } from '@/utils/cn';
import { useT, useUiLang } from '@/i18n';
import { catalogMessages, planCopy } from '@/i18n/messages/catalog';
import { motion } from '@/components/motion';

type Period = 'monthly' | 'quarterly' | 'annual';
const PERIODS: Period[] = ['monthly', 'quarterly', 'annual'];
const PERIOD_KEY = { monthly: 'periodMonthly', quarterly: 'periodQuarterly', annual: 'periodAnnual' } as const;
const SUFFIX_KEY: Partial<Record<PlanPeriod, 'perMonth' | 'perQuarter' | 'perYear'>> = { monthly: 'perMonth', quarterly: 'perQuarter', annual: 'perYear' };
const perMock = (p: Plan) => (p.priceInr > 0 && p.credits > 1 ? Math.round(p.priceInr / p.credits) : 0);

interface PricingCardsProps {
  plans?: Plan[];
  /** The student's study plan (or combo); kept for older callers, merged into `heldPlanIds`. */
  currentPlanId?: PlanId;
  /** Plans the student holds now (study plan / combo and tutor pack). */
  heldPlanIds?: PlanId[];
  onSelect?: (plan: Plan) => void;
  ctaHref?: (plan: Plan) => string;
  /** Home page: the plan sections rise in when scrolled into view. */
  inView?: boolean;
}

/**
 * Pricing blueprint: Study plans (monthly / quarterly / yearly), AI Tutor packs, Topper Combo and Add-ons.
 * Each subscription group has its own billing-period switch.
 */
export function PricingCards({ plans = getActivePlans(), currentPlanId, heldPlanIds = [], onSelect, ctaHref, inView }: PricingCardsProps) {
  const t = useT(catalogMessages);
  const held = [...new Set([...heldPlanIds, ...(currentPlanId && currentPlanId !== 'free' ? [currentPlanId] : [])])];
  const groups = groupPlans(plans);
  const card = (p: Plan) => (
    <PlanCard
      key={p.id}
      plan={p}
      plans={plans}
      current={held.includes(p.id) || (p.group === 'free' && currentPlanId === 'free')}
      clash={held.includes(p.id) ? undefined : conflictingPlan(p, held, plans)}
      onSelect={onSelect}
      ctaHref={ctaHref}
    />
  );
  return (
    <motion.div
      className="space-y-12"
      {...(inView ? { initial: { opacity: 0, y: 24 }, whileInView: { opacity: 1, y: 0 }, viewport: { once: true, amount: 0.1 }, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] } } : {})}
    >
      <PlanSection title={t('studyPlansTitle')} description={t('studyPlansDesc')} plans={groups.study} lead={groups.free} card={card} cols="sm:grid-cols-2 xl:grid-cols-3" />
      {groups.tutor.length > 0 && <PlanSection title={t('tutorPacksTitle')} description={t('tutorPacksDesc')} plans={groups.tutor} card={card} cols="sm:grid-cols-2" />}
      {groups.combo.length > 0 && <PlanSection title={t('comboTitle')} description={t('comboDesc')} plans={groups.combo} card={card} cols="sm:grid-cols-2 xl:grid-cols-3" />}
      {groups.addon.length > 0 && (
        <section aria-labelledby="addons-h">
          <h3 id="addons-h" className="text-xl font-bold">{t('addonsTitle')}</h3>
          <p className="mt-1 text-sm text-muted">{t('addonsDesc')}</p>
          <div className="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {groups.addon.map((p) => <AddonCard key={p.id} plan={p} onSelect={onSelect} ctaHref={ctaHref} />)}
          </div>
        </section>
      )}
    </motion.div>
  );
}

function PlanSection({ title, description, plans, lead, card, cols }: {
  title: string; description: string; plans: Plan[]; lead?: Plan; card: (p: Plan) => ReactNode; cols: string;
}) {
  const t = useT(catalogMessages);
  const periods = PERIODS.filter((per) => plans.some((p) => p.period === per));
  const [period, setPeriod] = useState<Period>('monthly');
  const shown = periods.includes(period) ? period : periods[0];
  const headingId = `plans-${title.replace(/\W+/g, '-').toLowerCase()}`;
  return (
    <section aria-labelledby={headingId}>
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h3 id={headingId} className="text-xl font-bold">{title}</h3>
          <p className="mt-1 text-sm text-muted">{description}</p>
        </div>
        {periods.length > 1 && (
          <div role="group" aria-label={t('billingPeriod', { group: title })} className="inline-flex rounded-xl border-[1.5px] border-ink bg-paper p-1">
            {periods.map((per) => (
              <button
                key={per}
                type="button"
                aria-pressed={shown === per}
                onClick={() => setPeriod(per)}
                className={cn('rounded-lg px-3 py-1.5 text-sm font-semibold transition-colors', shown === per ? 'bg-primary text-white' : 'text-muted hover:text-ink')}
              >
                {t(PERIOD_KEY[per])}
              </button>
            ))}
          </div>
        )}
      </div>
      <div className={cn('mt-6 grid gap-5', cols)}>
        {lead && card(lead)}
        {plans.filter((p) => p.period === shown).map(card)}
      </div>
    </section>
  );
}

function PlanCard({ plan: p, plans, current, clash, onSelect, ctaHref }: {
  plan: Plan; plans: Plan[]; current: boolean; clash?: Plan; onSelect?: (plan: Plan) => void; ctaHref?: (plan: Plan) => string;
}) {
  const t = useT(catalogMessages);
  const lang = useUiLang();
  const tx = (s: string) => planCopy(lang, s);
  const isFree = p.group === 'free' || p.priceInr === 0;
  const saving = periodSaving(p, plans);
  const suffix = SUFFIX_KEY[p.period];
  return (
    <Card
      className={cn(
        'relative flex flex-col rounded-2xl border-[1.5px] border-ink p-6',
        p.highlighted ? 'border-[2.5px] border-primary bg-primary-soft shadow-[8px_8px_0_var(--color-primary)]' : 'shadow-hard-sm',
      )}
      data-testid={`plan-${p.id}`}
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
      <h4 className="mt-1 text-xl font-bold">{tx(planShortName(p))}</h4>
      <p className="mt-3">
        <span className="font-display text-4xl font-extrabold tracking-tight">{formatINR(p.priceInr)}</span>
        {!isFree && suffix && <span className="text-sm font-semibold text-muted">{t(suffix)}</span>}
      </p>
      <p className="mt-1 h-5 text-xs text-muted">
        {saving > 0 ? <span className="font-semibold text-success">{t('savePct', { pct: saving })}</span>
          : perMock(p) > 0 ? t('perMock', { amount: formatINR(perMock(p)) })
            : isFree ? t('freeForever') : ''}
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
          <>
            <Button
              className={cn('w-full', !p.highlighted && 'border-ink')}
              variant={p.highlighted ? 'primary' : 'outline'}
              onClick={() => onSelect(p)}
              disabled={isFree || !!clash}
            >
              {isFree ? t('includedNewUsers') : tx(p.cta)}
            </Button>
            {clash && <p className="mt-2 text-xs text-muted">{t('alreadyHave', { plan: tx(planShortName(clash)) })}</p>}
          </>
        ) : (
          <ButtonLink to={ctaHref ? ctaHref(p) : '/signup'} className={cn('w-full', !p.highlighted && 'border-ink')} variant={p.highlighted ? 'primary' : 'outline'}>
            {tx(p.cta)}
          </ButtonLink>
        )}
      </div>
    </Card>
  );
}

function AddonCard({ plan: p, onSelect, ctaHref }: { plan: Plan; onSelect?: (plan: Plan) => void; ctaHref?: (plan: Plan) => string }) {
  const lang = useUiLang();
  const tx = (s: string) => planCopy(lang, s);
  return (
    <Card className="flex flex-col rounded-2xl border-[1.5px] border-ink p-5 shadow-hard-sm" data-testid={`plan-${p.id}`}>
      <div className="flex items-start justify-between gap-3">
        <h4 className="font-semibold">{tx(p.name)}</h4>
        <span className="font-display text-xl font-extrabold">{formatINR(p.priceInr)}</span>
      </div>
      <p className="mt-2 flex-1 text-sm text-muted">{tx(p.description)}</p>
      <div className="mt-4">
        {onSelect ? (
          <Button variant="outline" size="sm" className="w-full border-ink" onClick={() => onSelect(p)}>{tx(p.cta)}</Button>
        ) : (
          <ButtonLink to={ctaHref ? ctaHref(p) : '/signup'} variant="outline" size="sm" className="w-full border-ink">{tx(p.cta)}</ButtonLink>
        )}
      </div>
    </Card>
  );
}
