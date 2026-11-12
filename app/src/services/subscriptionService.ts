import { Platform } from 'react-native';
import type { Allowances, DemoOrder, Json, PaymentMethodLabel, Plan, PlanId } from '@prepmitra/shared';
import {
  API_ENDPOINTS, GST_RATE, PLANS, PRICES_INCLUDE_GST, conflictingPlan, createId, mockAllowances, planCodeFromId, planIdFromCode,
  toAllowances, toPlans,
} from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';

export const gstBreakup = (price: number) => {
  const gst = PRICES_INCLUDE_GST
    ? Math.round((price - price / (1 + GST_RATE)) * 100) / 100
    : Math.round(price * GST_RATE * 100) / 100;
  const total = PRICES_INCLUDE_GST ? price : price + gst;
  return { base: Math.round((total - gst) * 100) / 100, gst, total };
};

const toOrder = (o: Json, planId: PlanId, method: PaymentMethodLabel): DemoOrder => ({
  id: o.id ?? o.order_id,
  planId: o.plan_code ? planIdFromCode(o.plan_code) : planId,
  amountInr: o.amount_paise / 100,
  gstInr: (o.gst_amount_paise ?? 0) / 100,
  method,
  status: o.status === 'paid' ? 'success' : o.status === 'refunded' ? 'refunded' : o.status === 'failed' ? 'failed' : 'pending',
  createdAt: o.paid_at ?? o.created_at ?? new Date().toISOString(),
});

/**
 * Demo checkout. No payment gateway is called and no card/UPI/bank details are
 * collected. Production creates a Razorpay/Cashfree order on the backend and
 * credits are added only after a signature-verified webhook.
 */
export const subscriptionService = {
  /** GET /v1/plans (study plans, AI Tutor packs, Topper Combo, add-ons). */
  async getPlans(): Promise<Plan[]> {
    if (!USE_MOCK) return toPlans((await http.get(API_ENDPOINTS.plans)).data);
    await delay(250);
    return PLANS;
  },

  /** GET /v1/me/allowances. Mock mode computes them from the plans held (`held`), with nothing used yet. */
  async getAllowances(held: PlanId[]): Promise<Allowances> {
    if (!USE_MOCK) return toAllowances((await http.get(API_ENDPOINTS.allowances)).data);
    await delay(200);
    return mockAllowances(held);
  },

  /**
   * POST /v1/orders { plan_code }. `held` is the student's current plans: a second study plan or tutor pack is
   * refused (the server answers 409 `already_subscribed`; mock mode does the same).
   */
  async createDemoOrder(planId: PlanId, method: PaymentMethodLabel, held: PlanId[] = []): Promise<DemoOrder> {
    if (!USE_MOCK) {
      const order = (await http.post(API_ENDPOINTS.orders, { plan_code: planCodeFromId(planId), platform: Platform.OS === 'ios' ? 'ios' : 'android' })).data;
      // Backend without Razorpay keys (development): its mock gateway settles the order and adds the credits.
      if (order.mock) return toOrder((await http.post(`/v1/orders/${order.order_id}/mock-pay`)).data, planId, method);
      throw mockError(501, 'CHECKOUT_UNAVAILABLE', 'In-app payments are coming soon. Please buy this plan on the PrepMitra website.');
    }
    const plan = PLANS.find((p) => p.id === planId);
    if (!plan) throw mockError(404, 'PLAN_NOT_FOUND', 'This plan is no longer available.');
    const clash = conflictingPlan(plan, held, PLANS);
    if (clash) throw mockError(409, 'already_subscribed', `You already have ${clash.name}. Cancel it or wait for it to end before switching.`);
    await delay(1500);
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
