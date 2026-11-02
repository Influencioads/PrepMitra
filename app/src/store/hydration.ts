import { useEffect, useState } from 'react';
import { useAuthStore } from './authStore';
import { useExamStore } from './examStore';
import { useInterviewStore } from './interviewStore';
import { useNotificationStore } from './notificationStore';
import { useProfileStore } from './profileStore';
import { useSubscriptionStore } from './subscriptionStore';

const PERSISTED = [useAuthStore, useProfileStore, useExamStore, useInterviewStore, useSubscriptionStore, useNotificationStore];

const allHydrated = () => PERSISTED.every((s) => s.persist.hasHydrated());

/** True once every AsyncStorage-backed store has finished rehydrating. */
export function useStoresHydrated(): boolean {
  const [hydrated, setHydrated] = useState(allHydrated);
  useEffect(() => {
    if (hydrated) return;
    const update = () => {
      if (allHydrated()) setHydrated(true);
    };
    const unsubs = PERSISTED.map((s) => s.persist.onFinishHydration(update));
    update();
    return () => unsubs.forEach((u) => u());
  }, [hydrated]);
  return hydrated;
}
