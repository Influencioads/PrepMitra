import { useState } from 'react';
import { Alert, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { Plan, PlanId } from '@prepmitra/shared';
import {
  DISCLAIMERS, PERIOD_LABEL, PERIOD_SUFFIX, PLANS, conflictingPlan, formatDate, formatINR, groupPlans, heldPlanIds, periodSaving, planShortName,
  relativeTime,
} from '@prepmitra/shared';
import { AppText, Badge, Button, Card, CardHeader, Divider, Notice, ProgressBar, Screen, SegmentedControl, toast } from '@/components';
import { CheckoutSheet } from '@/features/subscription/CheckoutSheet';
import { useAllowances, usePlans } from '@/features/subscription/usePlans';
import { errorMessage, subscriptionService } from '@/services';
import { useSubscriptionStore } from '@/store';
import { colors, radii, spacing } from '@/theme';

const STATUS_TONE = { active: 'success', trial: 'info', cancelled: 'warning', expired: 'error' } as const;

type Period = 'monthly' | 'quarterly' | 'annual';
const PERIOD_ORDER: Period[] = ['monthly', 'quarterly', 'annual'];
const periodsOf = (plans: Plan[]) => PERIOD_ORDER.filter((per) => plans.some((p) => p.period === per));

export default function Subscription() {
  const sub = useSubscriptionStore((s) => s.sub);
  const cancelAutoRenew = useSubscriptionStore((s) => s.cancelAutoRenew);
  const plans = usePlans();
  const { allowances, error: allowancesError } = useAllowances();
  const [checkout, setCheckout] = useState<PlanId | null>(null);
  const [cancelling, setCancelling] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const [studyPeriod, setStudyPeriod] = useState<Period>('monthly');
  const [tutorPeriod, setTutorPeriod] = useState<Period>('monthly');
  const [comboPeriod, setComboPeriod] = useState<Period>('monthly');
  const find = (id?: string) => (id ? plans.find((p) => p.id === id) ?? PLANS.find((p) => p.id === id) : undefined);
  const plan = find(sub.planId);
  const tutorPlan = find(sub.tutorPlanId);
  const held = heldPlanIds(sub);
  const groups = groupPlans(plans);
  const ledger = showAll ? sub.ledger : sub.ledger.slice(0, 6);
  const shownLimits = allowances?.limits.filter((l) => l.limit > 0) ?? [];

  const cancel = () =>
    Alert.alert(
      'Cancel auto-renew?',
      `Your ${plan ? planShortName(plan) : ''} plan stays active until ${sub.renewsAt ? formatDate(sub.renewsAt) : 'the end of the period'}. You won’t be charged again.`,
      [
        { text: 'Keep auto-renew', style: 'cancel' },
        {
          text: 'Cancel auto-renew',
          style: 'destructive',
          onPress: async () => {
            setCancelling(true);
            try {
              await subscriptionService.cancelAutoRenew();
              cancelAutoRenew();
              toast.success('Auto-renew cancelled.');
            } catch (e) {
              toast.error(errorMessage(e));
            } finally {
              setCancelling(false);
            }
          },
        },
      ],
    );

  const card = (p: Plan) => (
    <PlanCard
      key={p.id}
      plan={p}
      plans={plans}
      current={held.includes(p.id)}
      clash={held.includes(p.id) ? undefined : conflictingPlan(p, held, plans)}
      freeMiniMockUsed={sub.freeMiniMockUsed}
      onBuy={() => setCheckout(p.id)}
    />
  );

  const section = (title: string, caption: string, list: Plan[], period: Period, setPeriod: (p: Period) => void, extra?: Plan) => {
    const periods = periodsOf(list);
    const shown = periods.includes(period) ? period : periods[0];
    return (
      <View style={styles.section}>
        <AppText variant="h3" accessibilityRole="header">{title}</AppText>
        <AppText variant="small">{caption}</AppText>
        {periods.length > 1 && (
          <SegmentedControl<Period>
            accessibilityLabel={`${title} billing period`}
            segments={periods.map((v) => ({ value: v, label: PERIOD_LABEL[v] }))}
            value={shown ?? 'monthly'}
            onChange={setPeriod}
          />
        )}
        {extra && card(extra)}
        {list.filter((p) => p.period === shown).map(card)}
      </View>
    );
  };

  return (
    <Screen>
      <Card style={styles.current}>
        <View style={styles.currentTop}>
          <View style={styles.flex}>
            <AppText variant="caption">Current plan</AppText>
            <AppText variant="h2">{plan ? planShortName(plan) : sub.planId}</AppText>
            {plan && plan.group !== 'free' ? <AppText variant="small">{PERIOD_LABEL[plan.period]}</AppText> : null}
            {tutorPlan ? <AppText variant="smallStrong">+ {planShortName(tutorPlan)} ({PERIOD_LABEL[tutorPlan.period].toLowerCase()})</AppText> : null}
            <Badge label={sub.status === 'trial' ? 'Free trial' : sub.status[0]!.toUpperCase() + sub.status.slice(1)} tone={STATUS_TONE[sub.status]} />
          </View>
          <View style={styles.credits} accessible accessibilityLabel={`${sub.credits} credits available`}>
            <AppText style={styles.creditNum}>{sub.credits}</AppText>
            <AppText variant="caption">credits</AppText>
          </View>
        </View>
        {sub.renewsAt ? (
          <AppText variant="small">
            {sub.autoRenew ? `Renews on ${formatDate(sub.renewsAt)}` : `Active until ${formatDate(sub.renewsAt)} · auto-renew off`}
          </AppText>
        ) : (
          <AppText variant="small">{sub.freeMiniMockUsed ? 'No active subscription. Credits never expire before their validity date.' : 'Your free mock is available.'}</AppText>
        )}
        <AppText variant="caption">1 credit = 1 full mock exam or 1 mock interview. Credits are used only when you start.</AppText>
        {sub.autoRenew && <Button title="Cancel auto-renew" variant="outline" size="sm" loading={cancelling} onPress={cancel} style={styles.self} />}
      </Card>

      <Card>
        <CardHeader
          title="AI allowances"
          subtitle={allowances?.resetsAt ? `Monthly allowances reset on ${formatDate(allowances.resetsAt)}` : 'What your plans include this month'}
        />
        {allowances === null ? (
          <AppText variant="small">{allowancesError ? 'Couldn’t load your allowances. Try again later.' : 'Loading…'}</AppText>
        ) : shownLimits.length === 0 ? (
          <AppText variant="small">No AI allowances yet. Pick a plan or an AI Tutor pack below.</AppText>
        ) : (
          shownLimits.map((l) => (
            <View key={l.feature} style={styles.allowance}>
              <View style={styles.row}>
                <AppText variant="small" color={colors.text} style={styles.flex}>{l.label}</AppText>
                <AppText variant="smallStrong">{l.remaining} of {l.limit} left</AppText>
              </View>
              <ProgressBar value={l.used} max={l.limit} size="sm" label={l.label} valueLabel={`${l.used} of ${l.limit} used`} />
            </View>
          ))
        )}
      </Card>

      {section('Study plans', 'One study plan at a time. Save more with quarterly or annual billing.', groups.study, studyPeriod, setStudyPeriod, groups.free)}
      {groups.tutor.length > 0 && section('AI Tutor packs', 'A personal AI tutor that works with any plan, including Free.', groups.tutor, tutorPeriod, setTutorPeriod)}
      {groups.combo.length > 0 && section('Topper Combo', 'Pro and AI Tutor Pro together. Counts as your study plan and your tutor pack.', groups.combo, comboPeriod, setComboPeriod)}

      {groups.addon.length > 0 && (
        <Card>
          <CardHeader title="Add-ons" subtitle="One-time top-ups that work with any plan" />
          {groups.addon.map((p, i) => (
            <View key={p.id}>
              {i > 0 && <Divider />}
              <View style={styles.entry}>
                <View style={styles.flex}>
                  <AppText variant="smallStrong">{p.name}</AppText>
                  <AppText variant="caption">{p.description}</AppText>
                </View>
                <Button title={formatINR(p.priceInr)} size="sm" variant="outline" onPress={() => setCheckout(p.id)} accessibilityLabel={`${p.cta}, ${formatINR(p.priceInr)}`} />
              </View>
            </View>
          ))}
        </Card>
      )}
      <Notice tone="warning" title="Demo checkout">{DISCLAIMERS.demoPayment}</Notice>

      <Card>
        <CardHeader title="Credit history" subtitle="Purchases, usage and refunds" />
        {ledger.length === 0 ? (
          <AppText variant="small">No credit activity yet.</AppText>
        ) : (
          ledger.map((e, i) => (
            <View key={e.id}>
              {i > 0 && <Divider />}
              <View style={styles.entry} accessible accessibilityLabel={`${e.label}, ${e.delta >= 0 ? 'plus' : 'minus'} ${Math.abs(e.delta)} credits, ${relativeTime(e.at)}`}>
                <View style={[styles.deltaIcon, { backgroundColor: e.delta > 0 ? colors.successSoft : e.delta < 0 ? colors.errorSoft : '#F1F5F9' }]}>
                  <Ionicons name={e.delta > 0 ? 'add' : e.delta < 0 ? 'remove' : 'gift-outline'} size={16} color={e.delta > 0 ? colors.success : e.delta < 0 ? colors.error : colors.textSecondary} />
                </View>
                <View style={styles.flex}>
                  <AppText variant="smallStrong">{e.label}</AppText>
                  <AppText variant="caption">
                    {formatDate(e.at)}{e.expiresAt ? ` · expires ${formatDate(e.expiresAt)}` : ''}
                  </AppText>
                </View>
                <AppText variant="bodyStrong" color={e.delta > 0 ? colors.success : e.delta < 0 ? colors.error : colors.textSecondary}>
                  {e.delta > 0 ? `+${e.delta}` : e.delta}
                </AppText>
              </View>
            </View>
          ))
        )}
        {sub.ledger.length > 6 && (
          <Button title={showAll ? 'Show less' : `Show all ${sub.ledger.length}`} variant="ghost" size="sm" onPress={() => setShowAll((s) => !s)} />
        )}
      </Card>

      <CheckoutSheet visible={checkout !== null} planId={checkout} plans={plans} onClose={() => setCheckout(null)} />
    </Screen>
  );
}

function PlanCard({ plan: p, plans, current, clash, freeMiniMockUsed, onBuy }: {
  plan: Plan;
  plans: Plan[];
  current: boolean;
  clash?: Plan;
  freeMiniMockUsed: boolean;
  onBuy: () => void;
}) {
  const isFree = p.priceInr === 0;
  const saving = periodSaving(p, plans);
  return (
    <Card style={[styles.plan, p.highlighted && styles.planHi]}>
      <View style={styles.planTitle}>
        <AppText variant="h3">{planShortName(p)}</AppText>
        {p.badge ? <Badge label={p.badge} tone={p.highlighted ? 'primary' : 'secondary'} /> : null}
        {current ? <Badge label="Current" tone="success" /> : null}
      </View>
      <AppText variant="small">{p.description}</AppText>
      <View style={styles.price}>
        <AppText variant="h1">{isFree ? 'Free' : formatINR(p.priceInr)}</AppText>
        {!isFree && PERIOD_SUFFIX[p.period] ? <AppText variant="small">{PERIOD_SUFFIX[p.period]}</AppText> : null}
        {saving > 0 ? <Badge label={`Save ${saving}%`} tone="success" /> : null}
      </View>
      {p.features.map((f) => (
        <View key={f} style={styles.feature}>
          <Ionicons name="checkmark-circle" size={16} color={colors.success} />
          <AppText variant="small" color={colors.text} style={styles.flex}>{f}</AppText>
        </View>
      ))}
      {isFree ? (
        <Button
          title={freeMiniMockUsed ? 'Free mock used' : p.cta}
          variant="outline"
          disabled={freeMiniMockUsed}
          onPress={() => router.push('/exams/general-aptitude/instructions')}
        />
      ) : current ? (
        <Button title="Current plan" variant="outline" disabled />
      ) : clash ? (
        <>
          <Button title={p.cta} variant="outline" disabled />
          <AppText variant="caption">You already have {planShortName(clash)}. You can switch when it ends.</AppText>
        </>
      ) : (
        <Button title={p.cta} variant={p.highlighted ? 'primary' : 'outline'} onPress={onBuy} />
      )}
    </Card>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  self: { alignSelf: 'flex-start' },
  current: { gap: spacing.sm },
  currentTop: { flexDirection: 'row', gap: spacing.md, alignItems: 'center' },
  credits: { alignItems: 'center', padding: spacing.md, borderRadius: radii.lg, backgroundColor: colors.primarySoft, minWidth: 84 },
  creditNum: { fontSize: 32, fontWeight: '800', color: colors.primary },
  section: { gap: spacing.sm },
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  allowance: { gap: 4, paddingVertical: 4 },
  plan: { gap: spacing.sm },
  planHi: { borderColor: colors.primary, borderWidth: 2 },
  planTitle: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: 6 },
  price: { flexDirection: 'row', alignItems: 'baseline', gap: spacing.sm, flexWrap: 'wrap' },
  feature: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  entry: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, paddingVertical: spacing.sm },
  deltaIcon: { width: 30, height: 30, borderRadius: 15, alignItems: 'center', justifyContent: 'center' },
});
