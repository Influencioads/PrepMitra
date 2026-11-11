import type { DemoOrder, PaymentMethodLabel, PlanId } from '@prepmitra/shared';
import { API_ENDPOINTS, planCodeFromId } from '@prepmitra/shared';
import type { Json } from '@prepmitra/shared';
import { env } from '@/utils/env';
import { http } from './http';

/**
 * Razorpay Checkout adapter (15-day plan, Day 8). Used only when the real API is on.
 * Flow: POST /v1/orders → open Razorpay Checkout (UPI, cards, net banking) →
 * POST /v1/orders/verify (server checks the signature and adds credits).
 * Card/UPI details are entered inside Razorpay's own window; this app never sees them.
 * Credits are also added idempotently by the server-side webhook.
 */
export type PaymentErrorCode = 'PAYMENT_CANCELLED' | 'PAYMENT_FAILED' | 'CHECKOUT_UNAVAILABLE' | 'VERIFY_FAILED';

export class PaymentError extends Error {
  readonly code: PaymentErrorCode;
  readonly status = 402;
  /** Our order id, so a payment that could not be confirmed can be checked again (never paid twice). */
  readonly orderId?: string;
  constructor(code: PaymentErrorCode, message: string, orderId?: string) {
    super(message);
    this.code = code;
    this.orderId = orderId;
    this.name = 'PaymentError';
  }
}

/** Backend order (GET/POST /v1/orders…) → the receipt shape the checkout screens use. */
export const toOrder = (o: Json, planId: PlanId, method: PaymentMethodLabel): DemoOrder => ({
  id: o.id,
  planId,
  amountInr: o.amount_paise / 100,
  gstInr: (o.gst_amount_paise ?? 0) / 100,
  method,
  status: o.status === 'paid' ? 'success' : o.status === 'refunded' ? 'refunded' : o.status === 'failed' ? 'failed' : 'pending',
  createdAt: o.paid_at ?? o.created_at,
  invoiceNo: o.invoice_no ?? undefined,
  creditsAfter: typeof o.credits?.total === 'number' ? o.credits.total : undefined,
});

interface RazorpaySuccess {
  razorpay_payment_id: string;
  razorpay_order_id: string;
  razorpay_signature: string;
}

interface RazorpayInstance {
  open: () => void;
  on: (event: 'payment.failed', cb: (resp: { error?: { description?: string } }) => void) => void;
}

declare global {
  interface Window {
    Razorpay?: new (options: Record<string, unknown>) => RazorpayInstance;
  }
}

const CHECKOUT_SRC = 'https://checkout.razorpay.com/v1/checkout.js';
let scriptPromise: Promise<void> | null = null;

function loadCheckout(): Promise<void> {
  if (window.Razorpay) return Promise.resolve();
  scriptPromise ??= new Promise<void>((resolve, reject) => {
    const el = document.createElement('script');
    el.src = CHECKOUT_SRC;
    el.async = true;
    el.onload = () => resolve();
    el.onerror = () => {
      scriptPromise = null;
      reject(new PaymentError('CHECKOUT_UNAVAILABLE', 'Could not load the payment window. Check your connection and try again.'));
    };
    document.head.appendChild(el);
  });
  return scriptPromise;
}

export async function openRazorpayCheckout(planId: PlanId, method: PaymentMethodLabel, opts: { simulateFailure?: boolean } = {}): Promise<DemoOrder> {
  const order = await checkout(planId, method, opts);
  // Show the new balance from the server before the success screen.
  await import('@/store/sync').then((m) => m.syncCredits()).catch(() => undefined);
  return order;
}

/** GET /v1/orders/{id} — used to re-check a payment that could not be confirmed straight away. */
export async function fetchOrder(orderId: string, planId: PlanId, method: PaymentMethodLabel): Promise<DemoOrder> {
  const order = toOrder((await http.get(`/v1/orders/${orderId}`)).data, planId, method);
  if (order.status === 'success') await import('@/store/sync').then((m) => m.syncCredits()).catch(() => undefined);
  return order;
}

async function checkout(planId: PlanId, method: PaymentMethodLabel, opts: { simulateFailure?: boolean }): Promise<DemoOrder> {
  const order = (await http.post(API_ENDPOINTS.orders, { plan_code: planCodeFromId(planId), platform: 'web' })).data;
  if (order.mock) {
    // Backend without Razorpay keys (development): its mock gateway settles the order and adds the credits.
    // "Make this payment fail" (development only) leaves the order unpaid, like a declined payment.
    if (opts.simulateFailure) throw new PaymentError('PAYMENT_FAILED', 'Payment failed — no money was deducted. Try again.', order.order_id);
    return toOrder((await http.post(`/v1/orders/${order.order_id}/mock-pay`)).data, planId, method);
  }
  const key = order.key_id || env.razorpayKeyId;
  if (!key) throw new PaymentError('CHECKOUT_UNAVAILABLE', 'Payments are not configured yet.');
  await loadCheckout();

  const success = await new Promise<RazorpaySuccess>((resolve, reject) => {
    const rzp = new window.Razorpay!({
      key,
      order_id: order.gateway_order_id,
      amount: order.amount_paise,
      currency: order.currency,
      name: 'PrepMitra AI',
      description: order.plan?.name,
      // Opens Razorpay on the method the student picked (they can still switch inside Razorpay).
      prefill: { ...order.checkout_options?.prefill, method: method === 'card' ? 'card' : method },
      notes: order.checkout_options?.notes,
      config: { display: { preferences: { show_default_blocks: true } } },
      theme: { color: '#C2410C' },
      handler: (resp: RazorpaySuccess) => resolve(resp),
      modal: { ondismiss: () => reject(new PaymentError('PAYMENT_CANCELLED', 'Payment cancelled. No money was deducted.', order.order_id)) },
    });
    rzp.on('payment.failed', (resp) =>
      reject(new PaymentError('PAYMENT_FAILED', resp.error?.description ?? 'Payment failed — no money was deducted. Try again.', order.order_id)),
    );
    rzp.open();
  });

  try {
    return toOrder((await http.post(API_ENDPOINTS.ordersVerify, success)).data, planId, method);
  } catch {
    throw new PaymentError(
      'VERIFY_FAILED',
      'We received your payment but could not confirm it yet. Credits will appear within a few minutes; contact support if they don’t.',
      order.order_id,
    );
  }
}
