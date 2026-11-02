import { createJSONStorage } from 'zustand/middleware';

/** localStorage-backed storage for demo persistence (safe when storage is unavailable). */
export const demoStorage = createJSONStorage(() => {
  try {
    const k = '__pm_probe__';
    localStorage.setItem(k, '1');
    localStorage.removeItem(k);
    return localStorage;
  } catch {
    const mem = new Map<string, string>();
    return {
      getItem: (key: string) => mem.get(key) ?? null,
      setItem: (key: string, value: string) => void mem.set(key, value),
      removeItem: (key: string) => void mem.delete(key),
    };
  }
});
