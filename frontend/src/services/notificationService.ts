import type { AppNotification } from '@prepmitra/shared';
import { API_ENDPOINTS, toNotification } from '@prepmitra/shared';
import type { Json } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay } from './mock';

export const notificationService = {
  async list(): Promise<AppNotification[] | null> {
    if (!USE_MOCK) return ((await http.get(API_ENDPOINTS.notifications)).data.items as Json[]).map(toNotification);
    await delay(300);
    return null; // mock: the store already holds the seeded list
  },
  async markRead(ids: string[]): Promise<void> {
    if (!USE_MOCK) {
      // Only server notifications have numeric ids; ones created on this device are local.
      await Promise.all(ids.filter((id) => /^\d+$/.test(id)).map((id) => http.post(`${API_ENDPOINTS.notifications}/${id}/read`).catch(() => undefined)));
      return;
    }
    await delay(150);
  },
};
