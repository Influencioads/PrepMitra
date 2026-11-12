import { useEffect, useMemo, useState } from 'react';
import type { Allowances, Plan } from '@prepmitra/shared';
import { PLANS, activePurchaseIds } from '@prepmitra/shared';
import { subscriptionService } from '@/services';
import { useSubscriptionStore } from '@/store';

let cached: Plan[] | null = null;

/** Plans from `GET /v1/plans` (the bundled catalog until they load, or if the request fails). */
export function usePlans(): Plan[] {
  const [plans, setPlans] = useState<Plan[]>(cached ?? PLANS);
  useEffect(() => {
    let alive = true;
    subscriptionService.getPlans().then(
      (p) => {
        if (!p.length) return;
        cached = p;
        if (alive) setPlans(p);
      },
      () => undefined,
    );
    return () => {
      alive = false;
    };
  }, []);
  return plans;
}

/** `GET /v1/me/allowances`, refetched whenever the student's plans or orders change. */
export function useAllowances(): { allowances: Allowances | null; error: boolean } {
  const sub = useSubscriptionStore((s) => s.sub);
  const orders = useSubscriptionStore((s) => s.orders);
  const held = useMemo(() => activePurchaseIds(sub, orders), [sub, orders]);
  const key = held.join(',');
  const [state, setState] = useState<{ allowances: Allowances | null; error: boolean }>({ allowances: null, error: false });
  useEffect(() => {
    let alive = true;
    subscriptionService.getAllowances(key ? key.split(',') : []).then(
      (a) => alive && setState({ allowances: a, error: false }),
      () => alive && setState((s) => ({ ...s, error: true })),
    );
    return () => {
      alive = false;
    };
  }, [key, orders.length]);
  return state;
}
