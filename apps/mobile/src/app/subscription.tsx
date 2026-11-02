import { useState } from 'react';
import { Alert, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { PlanId } from '@prepmitra/shared';
import { DISCLAIMERS, PLANS, formatDate, formatINR, relativeTime } from '@prepmitra/shared';
import { AppText, Badge, Button, Card, CardHeader, Divider, Notice, Screen, toast } from '@/components';
import { CheckoutSheet } from '@/features/subscription/CheckoutSheet';
import { errorMessage, subscriptionService } from '@/services';
import { useSubscriptionStore } from '@/store';
import { colors, radii, spacing } from '@/theme';

const STATUS_TONE = { active: 'success', trial: 'info', cancelled: 'warning', expired: 'error' } as const;

export default function Subscription() {
  const sub = useSubscriptionStore((s) => s.sub);
  const cancelAutoRenew = useSubscriptionStore((s) => s.cancelAutoRenew);
  const [checkout, setCheckout] = useState<PlanId | null>(null);
  const [cancelling, setCancelling] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const plan = PLANS.find((p) => p.id === sub.planId);
  const ledger = showAll ? sub.ledger : sub.ledger.slice(0, 6);

  const cancel = () =>
    Alert.alert(
      'Cancel auto-renew?',
      `Your ${plan?.name ?? ''} plan stays active until ${sub.renewsAt ? formatDate(sub.renewsAt) : 'the end of the period'}. You won’t be charged again.`,
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

  return (
    <Screen>
      <Card style={styles.current}>
        <View style={styles.currentTop}>
          <View style={styles.flex}>
            <AppText variant="caption">Current plan</AppText>
            <AppText variant="h2">{plan?.name ?? sub.planId}</AppText>
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
          <AppText variant="small">{sub.freeMiniMockUsed ? 'No active subscription. Credits never expire before their validity date.' : 'Your free 30-minute mini mock is available.'}</AppText>
        )}
        <AppText variant="caption">1 credit = 1 full mock exam or 1 mock interview. Credits are used only when you start.</AppText>
        {sub.autoRenew && <Button title="Cancel auto-renew" variant="outline" size="sm" loading={cancelling} onPress={cancel} style={styles.self} />}
      </Card>

      <AppText variant="h3" accessibilityRole="header">Plans</AppText>
      {PLANS.map((p) => {
        const isFree = p.priceInr === 0;
        const current = p.id === sub.planId && p.isRecurring;
        return (
          <Card key={p.id} style={[styles.plan, p.highlighted && styles.planHi]}>
            <View style={styles.planHead}>
              <View style={styles.flex}>
                <View style={styles.planTitle}>
                  <AppText variant="h3">{p.name}</AppText>
                  {p.badge ? <Badge label={p.badge} tone={p.highlighted ? 'primary' : 'secondary'} /> : null}
                  {current ? <Badge label="Current" tone="success" /> : null}
                </View>
                <AppText variant="small">{p.description}</AppText>
              </View>
            </View>
            <View style={styles.price}>
              <AppText variant="h1">{isFree ? 'Free' : formatINR(p.priceInr)}</AppText>
              <AppText variant="small">
                {p.credits} credit{p.credits === 1 ? '' : 's'}{p.validityDays ? ` · ${p.validityDays} days` : ''}{p.isRecurring ? ' · monthly' : ''}
              </AppText>
            </View>
            {p.features.map((f) => (
              <View key={f} style={styles.feature}>
                <Ionicons name="checkmark-circle" size={16} color={colors.success} />
                <AppText variant="small" color={colors.text} style={styles.flex}>{f}</AppText>
              </View>
            ))}
            {isFree ? (
              <Button
                title={sub.freeMiniMockUsed ? 'Free mini mock used' : p.cta}
                variant="outline"
                disabled={sub.freeMiniMockUsed}
                onPress={() => router.push('/exams/general-aptitude/instructions')}
              />
            ) : (
              <Button
                title={current ? 'Add 10 more credits' : p.cta}
                variant={p.highlighted ? 'primary' : 'outline'}
                onPress={() => setCheckout(p.id)}
              />
            )}
          </Card>
        );
      })}
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

      <CheckoutSheet visible={checkout !== null} planId={checkout} onClose={() => setCheckout(null)} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  self: { alignSelf: 'flex-start' },
  current: { gap: spacing.sm },
  currentTop: { flexDirection: 'row', gap: spacing.md, alignItems: 'center' },
  credits: { alignItems: 'center', padding: spacing.md, borderRadius: radii.lg, backgroundColor: colors.primarySoft, minWidth: 84 },
  creditNum: { fontSize: 32, fontWeight: '800', color: colors.primary },
  plan: { gap: spacing.sm },
  planHi: { borderColor: colors.primary, borderWidth: 2 },
  planHead: { flexDirection: 'row' },
  planTitle: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: 6 },
  price: { flexDirection: 'row', alignItems: 'baseline', gap: spacing.sm, flexWrap: 'wrap' },
  feature: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  entry: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, paddingVertical: spacing.sm },
  deltaIcon: { width: 30, height: 30, borderRadius: 15, alignItems: 'center', justifyContent: 'center' },
});
