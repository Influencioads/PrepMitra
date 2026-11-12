import { beforeEach, describe, expect, it } from 'vitest';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { SEED_SUBSCRIPTION } from '@prepmitra/shared';
import { SubscriptionPage } from '@/pages/dashboard/SubscriptionPage';
import { useNotificationStore, useSubscriptionStore } from '@/store';
import { clearTrackedEvents, getTrackedEvents } from '@/lib/analytics';

describe('SubscriptionPage checkout (demo payments)', () => {
  beforeEach(() => {
    useSubscriptionStore.getState().reset('user-test', { ...SEED_SUBSCRIPTION, ledger: [...SEED_SUBSCRIPTION.ledger] });
    useNotificationStore.setState({ ownerId: 'user-test', items: [] });
    clearTrackedEvents();
  });

  it('shows a failure with retry, then succeeds and updates the balance', async () => {
    const user = userEvent.setup();
    const before = useSubscriptionStore.getState().sub.credits;
    render(
      <MemoryRouter>
        <SubscriptionPage />
      </MemoryRouter>,
    );

    await user.click(screen.getAllByRole('button', { name: /buy 1 mock/i })[0]!);
    const dialog = await screen.findByRole('dialog');
    await user.click(within(dialog).getByLabelText(/refund and cancellation policy/i));
    await user.click(within(dialog).getByLabelText(/simulate a failed payment/i));
    await user.click(within(dialog).getByRole('button', { name: /^pay /i }));

    const alert = await within(dialog).findByRole('alert');
    expect(alert).toHaveTextContent(/payment failed — no money was deducted/i);
    expect(useSubscriptionStore.getState().sub.credits).toBe(before);
    expect(useSubscriptionStore.getState().orders).toHaveLength(0);

    await user.click(within(dialog).getByRole('button', { name: /try again/i }));

    const balance = await within(dialog).findByTestId('new-balance');
    expect(balance).toHaveTextContent(`New balance: ${before + 1} credits`);
    expect(balance).toHaveTextContent(`(was ${before})`);
    expect(useSubscriptionStore.getState().sub.credits).toBe(before + 1);
    expect(useSubscriptionStore.getState().orders).toHaveLength(1);
    expect(getTrackedEvents().map((e) => e.event)).toEqual(['purchase_started', 'purchase_failed', 'purchase_started', 'purchase_completed']);
  });
});
