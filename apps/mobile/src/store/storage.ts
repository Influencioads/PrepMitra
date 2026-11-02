import AsyncStorage from '@react-native-async-storage/async-storage';
import { createJSONStorage } from 'zustand/middleware';

/**
 * AsyncStorage-backed JSON storage for every persisted demo store.
 * Hydration is asynchronous on native, so the root layout waits for
 * `useStoresHydrated()` before deciding where to route.
 */
export const demoStorage = createJSONStorage(() => AsyncStorage);
