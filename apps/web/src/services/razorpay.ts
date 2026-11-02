import type { DemoOrder, PaymentMethodLabel, PlanId } from '@prepmitra/shared';
import { API_ENDPOINTS } from '@prepmitra/shared';
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
  constructor(code: PaymentErrorCode, message: string) {
    super(message);
    this.code = code;
    this.name = 'PaymentError';
  }
}

interface CreateOrderResponse {
  orderId: string; // Razorpay order id (order_…)
  amountPaise: number;
  currency: 'INR';
  planName: string;
  prefill?: { name?: string; email?: string; contact?: string };
}

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

export async function openRazorpayCheckout(planId: PlanId, method: PaymentMethodLabel): Promise<DemoOrder> {
  if (!env.razorpayKeyId) throw new PaymentError('CHECKOUT_UNAVAILABLE', 'Payments are not configured yet.');
  const order = (await http.post<CreateOrderResponse>(API_ENDPOINTS.orders, { planId })).data;
  await loadCheckout();

  const success = await new Promise<RazorpaySuccess>((resolve, reject) => {
    const rzp = new window.Razorpay!({
      key: env.razorpayKeyId,
      order_id: order.orderId,
      amount: order.amountPaise,
      currency: order.currency,
      name: 'PrepMitra AI',
      description: order.planName,
      prefill: order.prefill,
      config: { display: { preferences: { show_default_blocks: true } } },
      theme: { color: '#C2410C' },
      handler: (resp: RazorpaySuccess) => resolve(resp),
      modal: { ondismiss: () => reject(new PaymentError('PAYMENT_CANCELLED', 'Payment cancelled. No money was deducted.')) },
    });
    rzp.on('payment.failed', (resp) =>
      reject(new PaymentError('PAYMENT_FAILED', resp.error?.description ?? 'Payment failed — no money was deducted. Try again.')),
    );
    rzp.open();
  });

  try {
    return (await http.post<DemoOrder>(API_ENDPOINTS.ordersVerify, { ...success, planId, method })).data;
  } catch {
    throw new PaymentError(
      'VERIFY_FAILED',
      'We received your payment but could not confirm it yet. Credits will appear within a few minutes; contact support if they don’t.',
    );
  }
}
