import { useId, useState, type ReactNode } from 'react';
import { Check, Sparkles } from 'lucide-react';
import { AnimatePresence } from 'framer-motion';
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
  /** Home page: one plan group at a time, picked from a switch above the cards. */
  tabbed?: boolean;
}

type GroupKey = 'study' | 'tutor' | 'combo' | 'addon';

/**
 * Pricing blueprint: Study plans (monthly / quarterly / yearly), AI Tutor packs, Topper Combo and Add-ons.
 * Each subscription group has its own billing-period switch.
 */
export function PricingCards({ plans = getActivePlans(), currentPlanId, heldPlanIds = [], onSelect, ctaHref, inView, tabbed }: PricingCardsProps) {
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
  const [tab, setTab] = useState<GroupKey>('study');
  const tabsId = useId();
  const sections: Record<GroupKey, ReactNode> = {
    study: <PlanSection title={t('studyPlansTitle')} description={t('studyPlansDesc')} plans={groups.study} lead={groups.free} card={card} cols="sm:grid-cols-2 xl:grid-cols-3" hideTitle={tabbed} />,
    tutor: groups.tutor.length > 0 && <PlanSection title={t('tutorPacksTitle')} description={t('tutorPacksDesc')} plans={groups.tutor} card={card} cols="sm:grid-cols-2" narrow={tabbed} hideTitle={tabbed} />,
    combo: groups.combo.length > 0 && <PlanSection title={t('comboTitle')} description={t('comboDesc')} plans={groups.combo} card={card} cols="sm:grid-cols-2 xl:grid-cols-3" narrow={tabbed} hideTitle={tabbed} />,
    addon: groups.addon.length > 0 && (
      <section aria-labelledby="addons-h">
        <h3 id="addons-h" className={cn('text-xl font-bold', tabbed && 'sr-only')}>{t('addonsTitle')}</h3>
        {!tabbed && <p className="mt-1 text-sm text-muted">{t('addonsDesc')}</p>}
        <div className={cn('grid gap-4 sm:grid-cols-2 xl:grid-cols-3', !tabbed && 'mt-6')}>
          {groups.addon.map((p) => <AddonCard key={p.id} plan={p} onSelect={onSelect} ctaHref={ctaHref} />)}
        </div>
      </section>
    ),
  };
  const rise = inView ? { initial: { opacity: 0, y: 24 }, whileInView: { opacity: 1, y: 0 }, viewport: { once: true, amount: 0.1 }, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] as const } } : {};

  if (tabbed) {
    const tabs: { key: GroupKey; label: string; show: boolean }[] = [
      { key: 'study', label: t('studyPlansTitle'), show: true },
      { key: 'tutor', label: t('tutorPacksTitle'), show: groups.tutor.length > 0 },
      { key: 'combo', label: t('comboTitle'), show: groups.combo.length > 0 },
      { key: 'addon', label: t('addonsTitle'), show: groups.addon.length > 0 },
    ];
    const shown = tabs.filter((x) => x.show);
    return (
      <motion.div {...rise}>
        <div className="-mx-4 overflow-x-auto px-4 pb-2 [scrollbar-width:none] sm:mx-0 sm:px-0">
          <div role="tablist" aria-label={t('planGroups')} className="mx-auto flex w-max gap-1 rounded-2xl border-[1.5px] border-ink bg-card p-1.5 shadow-hard-sm">
            {shown.map((x) => {
              const on = tab === x.key;
              return (
                <button key={x.key} type="button" role="tab" aria-selected={on} aria-controls={`${tabsId}-panel`} onClick={() => setTab(x.key)}
                  className={cn('relative whitespace-nowrap rounded-xl px-4 py-2 text-sm font-bold transition-colors sm:px-5', on ? 'text-white' : 'text-muted hover:text-ink')}>
                  {on && <motion.span layoutId={`${tabsId}-pill`} className="absolute inset-0 rounded-xl bg-ink" transition={{ type: 'spring', stiffness: 420, damping: 34 }} aria-hidden />}
                  <span className="relative">{x.label}</span>
                </button>
              );
            })}
          </div>
        </div>
        <div id={`${tabsId}-panel`} role="tabpanel" className="mt-5">
          <AnimatePresence mode="wait" initial={false}>
            <motion.div key={tab} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.22 }}>
              {sections[tab]}
            </motion.div>
          </AnimatePresence>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div className="space-y-12" {...rise}>
      {sections.study}
      {sections.tutor}
      {sections.combo}
      {sections.addon}
    </motion.div>
  );
}

function PlanSection({ title, description, plans, lead, card, cols, hideTitle, narrow }: {
  title: string; description: string; plans: Plan[]; lead?: Plan; card: (p: Plan) => ReactNode; cols: string; hideTitle?: boolean; narrow?: boolean;
}) {
  const t = useT(catalogMessages);
  const periods = PERIODS.filter((per) => plans.some((p) => p.period === per));
  const [period, setPeriod] = useState<Period>('monthly');
  const shown = periods.includes(period) ? period : periods[0];
  const headingId = `plans-${title.replace(/\W+/g, '-').toLowerCase()}`;
  const pillId = useId();
  return (
    <section aria-labelledby={headingId}>
      <div className={cn('flex flex-wrap items-end gap-3', hideTitle ? 'flex-col items-center text-center' : 'justify-between')}>
        <div>
          <h3 id={headingId} className={cn('text-xl font-bold', hideTitle && 'sr-only')}>{title}</h3>
          {!hideTitle && <p className="mt-1 text-sm text-muted">{description}</p>}
        </div>
        {periods.length > 1 && (
          <div role="group" aria-label={t('billingPeriod', { group: title })} className="inline-flex rounded-full border-[1.5px] border-ink bg-paper p-1">
            {periods.map((per) => (
              <button
                key={per}
                type="button"
                aria-pressed={shown === per}
                onClick={() => setPeriod(per)}
                className={cn('relative rounded-full px-4 py-1.5 text-sm font-semibold transition-colors', shown === per ? 'text-white' : 'text-muted hover:text-ink')}
              >
                {shown === per && <motion.span layoutId={pillId} className="absolute inset-0 rounded-full bg-primary" transition={{ type: 'spring', stiffness: 420, damping: 34 }} aria-hidden />}
                <span className="relative">{t(PERIOD_KEY[per])}</span>
              </button>
            ))}
          </div>
        )}
      </div>
      <div className={cn('grid items-stretch gap-6', cols, narrow && 'mx-auto max-w-4xl', (!hideTitle || periods.length > 1) && 'mt-8')}>
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
  const hi = !!p.highlighted;
  return (
    <Card
      className={cn(
        'relative flex flex-col rounded-3xl border-[1.5px] border-ink bg-card p-0 transition-[transform,box-shadow] duration-200 hover:-translate-y-1',
        hi ? 'border-[2.5px] border-primary shadow-[8px_8px_0_var(--color-primary)]' : 'shadow-hard-sm hover:shadow-hard',
      )}
      data-testid={`plan-${p.id}`}
    >
      {p.badge && (
        <span className={cn(
          'absolute -top-3.5 right-5 z-10 rotate-3 rounded-lg border-[2.5px] bg-paper px-2.5 py-1 text-[11px] font-extrabold uppercase tracking-[0.1em]',
          hi ? 'border-secondary text-secondary' : 'border-primary text-primary',
        )}>
          {tx(p.badge)}
        </span>
      )}

      {/* ticket head */}
      <div className={cn('rounded-t-[22px] px-6 pb-6 pt-6', hi ? 'bg-primary-soft' : isFree ? 'bg-secondary-soft/60' : '')}>
        <p className={cn('flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-[0.16em]', hi ? 'text-primary' : 'text-muted')}>
          {hi && <Sparkles className="h-3.5 w-3.5" aria-hidden />}{t('admitCard')}
        </p>
        <h4 className="mt-1.5 text-xl font-bold">{tx(planShortName(p))}</h4>
        <p className="mt-4 flex items-baseline gap-1">
          <span className="font-display text-5xl font-extrabold tracking-tight">{formatINR(p.priceInr)}</span>
          {!isFree && suffix && <span className="text-sm font-semibold text-muted">{t(suffix)}</span>}
        </p>
        <p className="mt-2 min-h-6 text-xs">
          {saving > 0 ? <span className="rounded-full bg-success-soft px-2 py-0.5 font-bold text-success">{t('savePct', { pct: saving })}</span>
            : perMock(p) > 0 ? <span className="text-muted">{t('perMock', { amount: formatINR(perMock(p)) })}</span>
              : isFree ? <span className="font-semibold text-secondary">{t('freeForever')}</span> : ''}
        </p>
      </div>

      {/* perforation */}
      <div className="relative" aria-hidden>
        <span className={cn('absolute -left-2.5 top-1/2 h-5 w-5 -translate-y-1/2 rounded-full border-[1.5px] bg-paper', hi ? 'border-primary' : 'border-ink')} />
        <span className={cn('absolute -right-2.5 top-1/2 h-5 w-5 -translate-y-1/2 rounded-full border-[1.5px] bg-paper', hi ? 'border-primary' : 'border-ink')} />
        <div className={cn('mx-6 border-t-2 border-dashed', hi ? 'border-primary/40' : 'border-line-strong')} />
      </div>

      {/* ticket body */}
      <div className="flex flex-1 flex-col px-6 pb-6 pt-5">
        <p className="text-sm leading-relaxed text-muted">{tx(p.description)}</p>
        <ul className="mt-5 space-y-3 text-sm">
          {p.features.map((f) => (
            <li key={f} className="flex gap-2.5">
              <span className={cn('mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded-full', hi ? 'bg-primary text-white' : 'bg-success-soft text-success')}>
                <Check className="h-2.5 w-2.5" strokeWidth={3.5} aria-hidden />
              </span>
              {tx(f)}
            </li>
          ))}
        </ul>
        <div className="mt-auto pt-7">
          {current ? (
            <Button variant="outline" className="w-full" disabled>{t('currentPlan')}</Button>
          ) : onSelect ? (
            <>
              <Button
                className={cn('w-full', !hi && 'border-ink')}
                variant={hi ? 'primary' : 'outline'}
                onClick={() => onSelect(p)}
                disabled={isFree || !!clash}
              >
                {isFree ? t('includedNewUsers') : tx(p.cta)}
              </Button>
              {clash && <p className="mt-2 text-xs text-muted">{t('alreadyHave', { plan: tx(planShortName(clash)) })}</p>}
            </>
          ) : (
            <ButtonLink to={ctaHref ? ctaHref(p) : '/signup'} className={cn('w-full', !hi && 'border-ink')} variant={hi ? 'primary' : 'outline'}>
              {tx(p.cta)}
            </ButtonLink>
          )}
        </div>
      </div>
    </Card>
  );
}

function AddonCard({ plan: p, onSelect, ctaHref }: { plan: Plan; onSelect?: (plan: Plan) => void; ctaHref?: (plan: Plan) => string }) {
  const lang = useUiLang();
  const tx = (s: string) => planCopy(lang, s);
  return (
    <Card className="flex flex-col rounded-2xl border-[1.5px] border-ink bg-card p-5 shadow-hard-sm transition-[transform,box-shadow] duration-200 hover:-translate-y-1 hover:shadow-hard" data-testid={`plan-${p.id}`}>
      <div className="flex items-start justify-between gap-3">
        <h4 className="font-semibold">{tx(p.name)}</h4>
        <span className="shrink-0 rounded-full bg-accent-soft px-3 py-1 font-display text-lg font-extrabold text-primary">{formatINR(p.priceInr)}</span>
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
