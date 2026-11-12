import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { CreditReason, DemoOrder, Exam, InterviewRole, Plan, SubscriptionState } from '@prepmitra/shared';
import { STORAGE_KEYS, createId } from '@prepmitra/shared';
import { demoStorage } from './storage';

export const NEW_USER_SUBSCRIPTION: SubscriptionState = {
  planId: 'free',
  status: 'trial',
  credits: 0,
  autoRenew: false,
  freeMiniMockUsed: false,
  ledger: [],
};

interface SubscriptionStoreState {
  ownerId: string | null;
  sub: SubscriptionState;
  orders: DemoOrder[];
  reset: (ownerId: string, sub: SubscriptionState) => void;
  /** Deducts credits when an attempt starts (credits are not deducted at purchase). */
  consume: (cost: number, reason: CreditReason, label: string, useFreeTrial?: boolean) => boolean;
  refund: (cost: number, label: string) => void;
  applyOrder: (order: DemoOrder, plan: Plan) => void;
  cancelAutoRenew: () => void;
}

const DAY = 86_400_000;

function purchaseSlot(plan: Plan, expiresAt: string | undefined): Partial<SubscriptionState> {
  if (plan.group === 'study') return { planId: plan.id, renewsAt: expiresAt, autoRenew: true };
  if (plan.group === 'combo') return { planId: plan.id, tutorPlanId: undefined, renewsAt: expiresAt, autoRenew: true };
  if (plan.group === 'tutor') return { tutorPlanId: plan.id, autoRenew: true };
  return {};
}

export const useSubscriptionStore = create<SubscriptionStoreState>()(
  persist(
    (set, get) => ({
      ownerId: null,
      sub: NEW_USER_SUBSCRIPTION,
      orders: [],
      reset: (ownerId, sub) => set({ ownerId, sub, orders: [] }),
      consume: (cost, reason, label, useFreeTrial) => {
        const { sub } = get();
        const now = new Date().toISOString();
        if (useFreeTrial && !sub.freeMiniMockUsed) {
          set({
            sub: {
              ...sub,
              freeMiniMockUsed: true,
              ledger: [{ id: createId('cl'), delta: 0, reason: 'free-trial', label: `${label} (free trial)`, at: now }, ...sub.ledger],
            },
          });
          return true;
        }
        if (cost === 0) return true;
        if (sub.credits < cost) return false;
        set({
          sub: {
            ...sub,
            credits: sub.credits - cost,
            ledger: [{ id: createId('cl'), delta: -cost, reason, label, at: now }, ...sub.ledger],
          },
        });
        return true;
      },
      refund: (cost, label) =>
        set((s) => ({
          sub: {
            ...s.sub,
            credits: s.sub.credits + cost,
            ledger: [{ id: createId('cl'), delta: cost, reason: 'refund', label, at: new Date().toISOString() }, ...s.sub.ledger],
          },
        })),
      applyOrder: (order, plan) =>
        set((s) => {
          const now = Date.now();
          const expiresAt = plan.validityDays ? new Date(now + plan.validityDays * DAY).toISOString() : undefined;
          // Study plan / combo takes the plan slot, a tutor pack the tutor slot; add-ons only add credits.
          const slot = purchaseSlot(plan, expiresAt);
          return {
            orders: [order, ...s.orders],
            sub: {
              ...s.sub,
              ...slot,
              status: 'active',
              credits: s.sub.credits + plan.credits,
              ledger: [
                {
                  id: createId('cl'),
                  delta: plan.credits,
                  reason: 'purchase',
                  label: `${plan.name} — ₹${plan.priceInr.toLocaleString('en-IN')} (demo)`,
                  at: new Date(now).toISOString(),
                  expiresAt,
                },
                ...s.sub.ledger,
              ],
            },
          };
        }),
      cancelAutoRenew: () =>
        set((s) => ({ sub: { ...s.sub, autoRenew: false, status: s.sub.status === 'active' ? 'cancelled' : s.sub.status } })),
    }),
    { name: STORAGE_KEYS.subscription, storage: demoStorage },
  ),
);

/** Credits needed to start an exam; the free mini mock costs nothing until the trial is used. */
export function examCreditCost(exam: Exam, sub: SubscriptionState): { cost: number; usesFreeTrial: boolean } {
  if (exam.isFree && !sub.freeMiniMockUsed) return { cost: 0, usesFreeTrial: true };
  return { cost: Math.max(exam.creditCost, 1), usesFreeTrial: false };
}

export const roleCreditCost = (role: InterviewRole) => Math.max(role.creditCost, 1);
