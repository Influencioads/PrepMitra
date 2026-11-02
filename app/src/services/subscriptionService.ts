import type { DemoOrder, PaymentMethodLabel, Plan, PlanId } from '@prepmitra/shared';
import { API_ENDPOINTS, GST_RATE, PLANS, PRICES_INCLUDE_GST, createId } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';

export const gstBreakup = (price: number) => {
  const gst = PRICES_INCLUDE_GST
    ? Math.round((price - price / (1 + GST_RATE)) * 100) / 100
    : Math.round(price * GST_RATE * 100) / 100;
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
    if (!USE_MOCK) return (await http.get<Plan[]>(API_ENDPOINTS.plans)).data;
    await delay(250);
    return PLANS;
  },

  /** POST /v1/orders (simulated success) */
  async createDemoOrder(planId: PlanId, method: PaymentMethodLabel): Promise<DemoOrder> {
    if (!USE_MOCK) return (await http.post<DemoOrder>(API_ENDPOINTS.orders, { planId, method })).data;
    const plan = PLANS.find((p) => p.id === planId);
    if (!plan) throw mockError(404, 'PLAN_NOT_FOUND', 'This plan is no longer available.');
    await delay(1500);
    const { gst, total } = gstBreakup(plan.priceInr);
    return { id: createId('ord'), planId, amountInr: total, gstInr: gst, method, status: 'success', createdAt: new Date().toISOString() };
  },

  async cancelAutoRenew(): Promise<void> {
    if (!USE_MOCK) {
      await http.post('/v1/me/subscription/cancel');
      return;
    }
    await delay(500);
  },
};
