import type { AppNotification } from '@prepmitra/shared';
import { API_ENDPOINTS } from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay } from './mock';

export const notificationService = {
  async list(): Promise<AppNotification[] | null> {
    if (!USE_MOCK) return (await http.get<AppNotification[]>(API_ENDPOINTS.notifications)).data;
    await delay(300);
    return null; // mock: the store already holds the seeded list
  },
  async markRead(ids: string[]): Promise<void> {
    if (!USE_MOCK) {
      await http.post(`${API_ENDPOINTS.notifications}/read`, { ids });
      return;
    }
    await delay(150);
  },
};
