import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { SEED_NOTIFICATIONS } from '@prepmitra/shared';
import { NotificationsPage } from '@/pages/dashboard/NotificationsPage';
import { useNotificationStore, useUnreadCount } from '@/store';

const renderPage = () =>
  render(
    <MemoryRouter>
      <NotificationsPage />
    </MemoryRouter>,
  );

describe('NotificationsPage', () => {
  beforeEach(() => useNotificationStore.setState({ ownerId: 'u', items: SEED_NOTIFICATIONS.map((n) => ({ ...n })) }));

  it('marks a single notification as read', async () => {
    const user = userEvent.setup();
    renderPage();
    const unread = SEED_NOTIFICATIONS.filter((n) => !n.read);
    await user.click(screen.getByRole('button', { name: `Mark “${unread[0]!.title}” as read` }));
    expect(useNotificationStore.getState().items.filter((n) => !n.read)).toHaveLength(unread.length - 1);
  });

  it('marks all as read and shows the empty unread state', async () => {
    const user = userEvent.setup();
    renderPage();
    await user.click(screen.getByRole('button', { name: /mark all as read/i }));
    expect(useNotificationStore.getState().items.every((n) => n.read)).toBe(true);
    await user.click(screen.getByRole('tab', { name: /unread/i }));
    expect(screen.getByText(/You’re all caught up/)).toBeInTheDocument();
  });

  it('shows the empty state after clearing all', async () => {
    const user = userEvent.setup();
    renderPage();
    await user.click(screen.getByRole('button', { name: /clear all/i }));
    const dialog = await screen.findByRole('dialog');
    await user.click(within(dialog).getByRole('button', { name: /clear all/i }));
    expect(screen.getByText('No notifications')).toBeInTheDocument();
    expect(useNotificationStore.getState().items).toHaveLength(0);
  });

  it('unread counter hook reflects store', () => {
    function Count() {
      return <span>{useUnreadCount()}</span>;
    }
    render(<Count />);
    expect(screen.getByText(String(SEED_NOTIFICATIONS.filter((n) => !n.read).length))).toBeInTheDocument();
  });
});
