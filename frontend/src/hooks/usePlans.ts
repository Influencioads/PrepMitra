import { useEffect, useState } from 'react';
import type { Plan } from '@prepmitra/shared';
import { getActivePlans, subscriptionService } from '@/services/subscriptionService';
import { USE_MOCK } from '@/services/mock';

let cache: Plan[] | null = null;

/**
 * Plans from GET /v1/plans (prices, credits, validity and GST come from the server).
 * Shows the built-in plans until the server answers, and keeps them if it cannot be reached.
 */
export function usePlans(): { plans: Plan[]; fromServer: boolean } {
  const [plans, setPlans] = useState<Plan[]>(() => cache ?? getActivePlans());
  const [fromServer, setFromServer] = useState(!!cache);
  useEffect(() => {
    if (USE_MOCK || cache) return;
    let alive = true;
    subscriptionService.getPlans().then(
      (p) => {
        if (!p.length) return;
        cache = p;
        if (alive) {
          setPlans(p);
          setFromServer(true);
        }
      },
      () => undefined,
    );
    return () => {
      alive = false;
    };
  }, []);
  return { plans, fromServer };
}

/** Tests: forget the cached plans. */
export const resetPlansCache = () => {
  cache = null;
};
