import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { AppNotification } from '@prepmitra/shared';
import { STORAGE_KEYS, createId } from '@prepmitra/shared';
import { demoStorage } from './storage';

interface NotificationState {
  ownerId: string | null;
  items: AppNotification[];
  reset: (ownerId: string, items: AppNotification[]) => void;
  markRead: (id: string) => void;
  markUnread: (id: string) => void;
  markAllRead: () => void;
  remove: (id: string) => void;
  clearAll: () => void;
  push: (n: Omit<AppNotification, 'id' | 'createdAt' | 'read'>) => void;
}

export const useNotificationStore = create<NotificationState>()(
  persist(
    (set) => ({
      ownerId: null,
      items: [],
      reset: (ownerId, items) => set({ ownerId, items }),
      markRead: (id) => set((s) => ({ items: s.items.map((n) => (n.id === id ? { ...n, read: true } : n)) })),
      markUnread: (id) => set((s) => ({ items: s.items.map((n) => (n.id === id ? { ...n, read: false } : n)) })),
      markAllRead: () => set((s) => ({ items: s.items.map((n) => ({ ...n, read: true })) })),
      remove: (id) => set((s) => ({ items: s.items.filter((n) => n.id !== id) })),
      clearAll: () => set({ items: [] }),
      push: (n) => set((s) => ({ items: [{ ...n, id: createId('n'), createdAt: new Date().toISOString(), read: false }, ...s.items] })),
    }),
    { name: STORAGE_KEYS.notifications, storage: demoStorage },
  ),
);

export const useUnreadCount = () => useNotificationStore((s) => s.items.filter((n) => !n.read).length);
