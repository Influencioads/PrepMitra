import type { User } from '@prepmitra/shared';
import { DEMO_ADMIN, DEMO_USER } from '@prepmitra/shared';

/**
 * Demo mode only: accounts created on this device, keyed by phone, so a number that finished
 * onboarding is a returning user next time (like the backend). Not used with the real API.
 */
const KEY = 'pm.demoAccounts';

export function readDemoAccount(phone: string): User | undefined {
  try {
    return (JSON.parse(localStorage.getItem(KEY) ?? '{}') as Record<string, User>)[phone];
  } catch {
    return undefined;
  }
}

export function rememberDemoAccount(user: User): void {
  if (user.role !== 'user' || user.phone === DEMO_USER.phone || user.phone === DEMO_ADMIN.phone) return;
  try {
    const all = JSON.parse(localStorage.getItem(KEY) ?? '{}') as Record<string, User>;
    all[user.phone] = user;
    localStorage.setItem(KEY, JSON.stringify(all));
  } catch {
    // storage unavailable: the account is simply new again next time
  }
}
