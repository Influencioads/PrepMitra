import { useEffect, useState } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { DemoOrder, PaymentMethodLabel, Plan, PlanId } from '@prepmitra/shared';
import { DISCLAIMERS, PERIOD_SUFFIX, PLANS, conflictingPlan, demoCheckoutSchema, formatINR, heldPlanIds } from '@prepmitra/shared';
import { AppText, Badge, BottomSheet, Button, Checkbox, Chip, Divider, Notice, toast } from '@/components';
import { errorMessage, gstBreakup, subscriptionService } from '@/services';
import { useNotificationStore, useSubscriptionStore } from '@/store';
import { colors, radii, spacing } from '@/theme';
import type { IoniconName } from '@/utils/icons';

const METHODS: { value: PaymentMethodLabel; label: string; icon: IoniconName }[] = [
  { value: 'upi', label: 'UPI', icon: 'phone-portrait-outline' },
  { value: 'card', label: 'Card', icon: 'card-outline' },
  { value: 'netbanking', label: 'Netbanking', icon: 'business-outline' },
  { value: 'wallet', label: 'Wallet', icon: 'wallet-outline' },
];

/** Quick picks when a student runs out of mocks: mock add-ons and the monthly study plans / combo. */
const quickPicks = (plans: Plan[]) =>
  plans.filter((p) => p.priceInr > 0 && p.credits > 0 && (p.group === 'addon' || p.period === 'monthly'));

export interface CheckoutSheetProps {
  visible: boolean;
  onClose: () => void;
  /** Skip the plan picker and go straight to checkout for this plan. */
  planId?: PlanId | null;
  /** Plans from `GET /v1/plans` (defaults to the bundled catalog). */
  plans?: Plan[];
  /** Shown above the plan picker, e.g. "This mock needs 1 credit and you have 0." */
  reason?: string;
  onSuccess?: (order: DemoOrder, plan: Plan) => void;
}

/**
 * Demo checkout as a bottom sheet: choose a plan → GST breakup → payment
 * method *label* only. No card, UPI or bank fields exist anywhere in the app.
 */
export function CheckoutSheet({ visible, onClose, planId, plans = PLANS, reason, onSuccess }: CheckoutSheetProps) {
  const sub = useSubscriptionStore((s) => s.sub);
  const held = heldPlanIds(sub);
  const applyOrder = useSubscriptionStore((s) => s.applyOrder);
  const pushNotification = useNotificationStore((s) => s.push);
  const [selected, setSelected] = useState<PlanId | null>(planId ?? null);
  const [stage, setStage] = useState<'choose' | 'pay'>(planId ? 'pay' : 'choose');
  const [method, setMethod] = useState<PaymentMethodLabel>('upi');
  const [accept, setAccept] = useState(false);
  const [acceptError, setAcceptError] = useState<string | null>(null);
  const [paying, setPaying] = useState(false);

  useEffect(() => {
    if (visible) {
      setSelected(planId ?? null);
      setStage(planId ? 'pay' : 'choose');
      setAccept(false);
      setAcceptError(null);
      setPaying(false);
    }
  }, [visible, planId]);

  const plan = plans.find((p) => p.id === selected) ?? PLANS.find((p) => p.id === selected);
  const picks = quickPicks(plans).filter((p) => !conflictingPlan(p, held, plans));
  const breakup = plan ? gstBreakup(plan.priceInr) : null;

  const pay = async () => {
    if (!plan) return;
    const parsed = demoCheckoutSchema.safeParse({ planId: plan.id, method, acceptTerms: accept });
    if (!parsed.success) {
      setAcceptError(parsed.error.issues[0]?.message ?? 'Please accept the policy');
      return;
    }
    setPaying(true);
    try {
      const order = await subscriptionService.createDemoOrder(plan.id, method, held);
      applyOrder(order, plan);
      pushNotification({
        type: 'payment',
        title: `Payment receipt — ${formatINR(order.amountInr)} (demo)`,
        body: `${plan.name} activated${plan.credits ? ` with ${plan.credits} credit${plan.credits === 1 ? '' : 's'}` : ''}.${order.status === 'success' ? '' : ' Your payment is being confirmed.'}`,
        link: '/subscription',
      });
      toast.success(plan.credits ? `${plan.credits} credit${plan.credits === 1 ? '' : 's'} added.` : `${plan.name} activated.`);
      onSuccess?.(order, plan);
      onClose();
    } catch (e) {
      toast.error(errorMessage(e));
      setPaying(false);
    }
  };

  return (
    <BottomSheet
      visible={visible}
      onClose={onClose}
      dismissable={!paying}
      title={stage === 'choose' ? 'Get more credits' : 'Demo checkout'}
      subtitle={stage === 'choose' ? reason : plan?.name}
      footer={
        stage === 'choose' ? (
          <Button title="Continue" disabled={!plan} onPress={() => setStage('pay')} fullWidth />
        ) : (
          <View style={styles.footerRow}>
            {!planId && <Button title="Back" variant="outline" onPress={() => setStage('choose')} disabled={paying} />}
            <Button title={plan ? `Pay ${formatINR(breakup!.total)} (demo)` : 'Pay'} onPress={pay} loading={paying} style={styles.flex} leftIcon="lock-closed-outline" />
          </View>
        )
      }
    >
      {stage === 'choose' ? (
        <>
          {picks.map((p) => {
            const active = p.id === selected;
            return (
              <Pressable
                key={p.id}
                onPress={() => setSelected(p.id)}
                accessibilityRole="radio"
                accessibilityState={{ checked: active }}
                accessibilityLabel={`${p.name}, ${formatINR(p.priceInr)}, ${p.credits} credits`}
                style={[styles.plan, active && styles.planActive]}
              >
                <Ionicons name={active ? 'radio-button-on' : 'radio-button-off'} size={22} color={active ? colors.primary : colors.borderStrong} />
                <View style={styles.flex}>
                  <View style={styles.planTitle}>
                    <AppText variant="bodyStrong">{p.name}</AppText>
                    {p.badge ? <Badge label={p.badge} tone="secondary" /> : null}
                  </View>
                  <AppText variant="small">{p.credits} credit{p.credits === 1 ? '' : 's'}{p.isRecurring ? ` ${PERIOD_SUFFIX[p.period]} · auto-renews` : p.validityDays ? ` · valid ${p.validityDays} days` : ''}</AppText>
                </View>
                <AppText variant="h3">{formatINR(p.priceInr)}</AppText>
              </Pressable>
            );
          })}
          <AppText variant="caption">Credits are used only when you start a mock or interview.</AppText>
        </>
      ) : plan && breakup ? (
        <>
          <View style={styles.summary}>
            <SummaryRow label={plan.credits ? `${plan.name} (${plan.credits} credit${plan.credits === 1 ? '' : 's'})` : plan.name} value={formatINR(breakup.base)} />
            <SummaryRow label="GST (18%)" value={formatINR(breakup.gst)} />
            <Divider />
            <SummaryRow label="Total" value={formatINR(breakup.total)} strong />
            <AppText variant="caption">Prices include GST. A tax invoice is issued after payment.</AppText>
          </View>
          <AppText variant="label">Payment method</AppText>
          <View style={styles.methods} accessibilityRole="radiogroup">
            {METHODS.map((m) => (
              <Chip key={m.value} role="radio" label={m.label} icon={m.icon} selected={method === m.value} onPress={() => setMethod(m.value)} />
            ))}
          </View>
          <AppText variant="caption">You’ll only choose a method label here. In production you’d complete payment on the gateway’s secure page.</AppText>
          <Checkbox
            label="I accept the refund and cancellation policy"
            checked={accept}
            onChange={(v) => {
              setAccept(v);
              setAcceptError(null);
            }}
            error={acceptError ?? undefined}
          />
          <Notice tone="warning" title="Demo payment">{DISCLAIMERS.demoPayment}</Notice>
        </>
      ) : null}
    </BottomSheet>
  );
}

function SummaryRow({ label, value, strong }: { label: string; value: string; strong?: boolean }) {
  return (
    <View style={styles.row}>
      <AppText variant={strong ? 'bodyStrong' : 'small'} color={strong ? colors.text : colors.textSecondary} style={styles.flex}>{label}</AppText>
      <AppText variant={strong ? 'h3' : 'smallStrong'}>{value}</AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  footerRow: { flexDirection: 'row', gap: spacing.sm },
  plan: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    padding: spacing.md,
    borderRadius: radii.lg,
    borderWidth: 1.5,
    borderColor: colors.border,
    minHeight: 64,
  },
  planActive: { borderColor: colors.primary, backgroundColor: colors.primarySoft },
  planTitle: { flexDirection: 'row', alignItems: 'center', gap: 6, flexWrap: 'wrap' },
  summary: { gap: spacing.sm, padding: spacing.md, borderRadius: radii.md, backgroundColor: colors.background },
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  methods: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
});
