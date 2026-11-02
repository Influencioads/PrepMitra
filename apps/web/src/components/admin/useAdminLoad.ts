import { useCallback, useEffect, useState } from 'react';
import type { AdminModule } from '@prepmitra/shared';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';

/** Modules already fetched this session; revisiting a page then renders instantly. */
const loaded = new Set<AdminModule>();
/** In-flight loads, shared so StrictMode's double effect run does not fire two requests. */
const inFlight = new Map<AdminModule, Promise<void>>();

/** Test helper: forget which modules were loaded. */
export const resetAdminLoadCache = () => {
  loaded.clear();
  inFlight.clear();
};

function loadOnce(module: AdminModule): Promise<void> {
  let p = inFlight.get(module);
  if (!p) {
    p = adminService
      .load(module)
      .then(() => {
        loaded.add(module);
      })
      .finally(() => inFlight.delete(module));
    inFlight.set(module, p);
  }
  return p;
}

export interface AdminLoadState {
  loading: boolean;
  error: string | null;
  reload: () => void;
}

/** Loads an admin module once per session through the service (simulated latency in mock mode). */
export function useAdminLoad(module: AdminModule): AdminLoadState {
  const [loading, setLoading] = useState(!loaded.has(module));
  const [error, setError] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    if (loaded.has(module) && tick === 0) {
      setLoading(false);
      return;
    }
    let alive = true;
    setLoading(true);
    setError(null);
    loadOnce(module)
      .catch((e) => alive && setError(errorMessage(e)))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [module, tick]);

  const reload = useCallback(() => setTick((t) => t + 1), []);
  return { loading, error, reload };
}
