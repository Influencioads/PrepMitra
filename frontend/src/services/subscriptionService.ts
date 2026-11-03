import type { CreditLedgerEntry, DemoOrder, PaymentMethodLabel, Plan, PlanId } from '@prepmitra/shared';
import { API_ENDPOINTS, GST_RATE, PRICES_INCLUDE_GST, createId, getPlanSet, toCredits, toPlans } from '@prepmitra/shared';
import type { Json } from '@prepmitra/shared';
import { env } from '@/utils/env';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';
import { openRazorpayCheckout } from './razorpay';

/** Plans shown in the app: VITE_PRICING_SET=launch switches to the 15-day MVP packs. */
export const getActivePlans = (): Plan[] => getPlanSet(env.pricingSet);

export interface CreditsResponse {
  credits: number;
  nextExpiry?: string;
  ledger: CreditLedgerEntry[];
}

export const gstBreakup = (price: number) => {
  const gst = PRICES_INCLUDE_GST ? Math.round((price - price / (1 + GST_RATE)) * 100) / 100 : Math.round(price * GST_RATE * 100) / 100;
  const total = PRICES_INCLUDE_GST ? price : price + gst;
  return { base: Math.round((total - gst) * 100) / 100, gst, total };
};

/**
 * Demo checkout. No payment gateway is called and no card/UPI/bank details are
 * collected. Production creates a Razorpay/Cashfree order on the backend and
 * credits are added only after a signature-verified webhook.
 */
export const subscriptionService = {
  /** GET /v1/plans */
  async getPlans(): Promise<Plan[]> {
    if (!USE_MOCK) return toPlans((await http.get(API_ENDPOINTS.plans)).data);
    await delay(250);
    return getActivePlans();
  },

  /** GET /v1/me/credits */
  async getCredits(): Promise<CreditsResponse | null> {
    if (USE_MOCK) return null;
    return toCredits((await http.get(API_ENDPOINTS.credits)).data);
  },

  /**
   * Real mode: Razorpay Checkout (POST /v1/orders → Checkout → POST /v1/orders/verify).
   * Demo mode: simulated; `simulateFailure` exercises the failure/retry screen.
   */
  async createDemoOrder(planId: PlanId, method: PaymentMethodLabel, opts: { simulateFailure?: boolean } = {}): Promise<DemoOrder> {
    const plan = getActivePlans().find((p) => p.id === planId) ?? getPlanSet('full').find((p) => p.id === planId)!;
    if (!USE_MOCK) return openRazorpayCheckout(planId, method);
    await delay(1500);
    if (opts.simulateFailure) throw mockError(402, 'PAYMENT_FAILED', 'Payment failed — no money was deducted. Try again.');
    const { gst, total } = gstBreakup(plan.priceInr);
    return { id: createId('ord'), planId, amountInr: total, gstInr: gst, method, status: 'success', createdAt: new Date().toISOString() };
  },

  async cancelAutoRenew(): Promise<void> {
    if (!USE_MOCK) {
      const subs: Json[] = (await http.get(API_ENDPOINTS.progress)).data.subscriptions ?? [];
      for (const sub of subs.filter((x) => x.status === 'active')) await http.post(`/v1/subscriptions/${sub.id}/cancel`);
      return;
    }
    await delay(500);
  },
};
