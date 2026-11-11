import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { SEED_SUBSCRIPTION, formatINR, toPlans } from '@prepmitra/shared';
import { PricingCards } from '@/components/marketing/PricingCards';
import { PricingPage } from '@/pages/public/PricingPage';
import { SubscriptionPage } from '@/pages/dashboard/SubscriptionPage';
import { ExamInstructionsPage } from '@/pages/exam/ExamInstructionsPage';
import { AppTopbar } from '@/layouts/AppLayout';
import { subscriptionService } from '@/services';
import { PaymentError } from '@/services/razorpay';
import { NEW_USER_SUBSCRIPTION, useNotificationStore, useSubscriptionStore } from '@/store';

// GET /v1/plans from the local backend.
const PLANS_RESPONSE = {
  items: [
    { id: 1, code: 'free_trial', name: 'Free trial (30-min mini mock)', price_paise: 0, price_inr: 0, taxable_paise: 0, gst_paise: 0, credits: 1, validity_days: 30, is_recurring: false, purchasable: false },
    { id: 2, code: 'pay_per_exam', name: 'Pay per exam', price_paise: 9900, price_inr: 99, taxable_paise: 8390, gst_paise: 1510, credits: 1, validity_days: 90, is_recurring: false, purchasable: true },
    { id: 5, code: 'credit_pack_10', name: '10-credit pack', price_paise: 39900, price_inr: 399, taxable_paise: 33814, gst_paise: 6086, credits: 10, validity_days: 90, is_recurring: false, purchasable: true },
  ],
};

beforeEach(() => {
  useSubscriptionStore.getState().reset('user-d8', { ...SEED_SUBSCRIPTION, ledger: [...SEED_SUBSCRIPTION.ledger] });
  useNotificationStore.setState({ ownerId: 'user-d8', items: [] });
});
afterEach(() => vi.restoreAllMocks());

describe('Day 8 — pricing from GET /v1/plans', () => {
  it('maps the server plans: price, credits, validity and the GST inside the price', () => {
    const plans = toPlans(PLANS_RESPONSE);
    expect(plans.map((p) => [p.id, p.priceInr, p.credits])).toEqual([['free', 0, 1], ['pay-per-mock', 99, 1], ['monthly', 399, 10]]);
    expect(plans[2]).toMatchObject({ name: '10-Credit Pack', gstInr: 60.86, baseInr: 338.14, purchasable: true, validityDays: 90 });
    expect(plans[0]!.purchasable).toBe(false);
    expect(formatINR(15.1)).toBe('₹15.10');
    expect(formatINR(399)).toBe('₹399');
  });

  it('cards show free mini mock, ₹99, ₹399 for 10 credits and the GST each price includes', () => {
    render(<MemoryRouter><PricingCards plans={toPlans(PLANS_RESPONSE)} /></MemoryRouter>);
    expect(screen.getByText('₹399')).toBeInTheDocument();
    expect(screen.getByText('incl. ₹15.10 GST')).toBeInTheDocument();
    expect(screen.getByText(/incl\. ₹60\.86 GST/)).toBeInTheDocument();
  });

  it('pricing page has the GST note and the FAQ', () => {
    render(<MemoryRouter><PricingPage /></MemoryRouter>);
    expect(screen.getAllByText(/include 18% GST/).length).toBeGreaterThan(0);
    const faq = screen.getByTestId('pricing-faq');
    expect(within(faq).getAllByRole('group')).toHaveLength(7);
    expect(within(faq).getByText('Money was deducted but I got no credits. What now?')).toBeInTheDocument();
  });
});

describe('Day 8 — Razorpay checkout states', () => {
  it('a payment Razorpay took but we could not confirm is never offered again: "Check status" instead', async () => {
    const user = userEvent.setup();
    vi.spyOn(subscriptionService, 'createDemoOrder').mockRejectedValue(new PaymentError('VERIFY_FAILED', 'We received your payment but could not confirm it yet.', 'ord-1'));
    const check = vi.spyOn(subscriptionService, 'checkOrder').mockResolvedValue({
      id: 'ord-1', planId: 'pay-per-mock', amountInr: 99, gstInr: 15.1, method: 'upi', status: 'success', createdAt: new Date().toISOString(), invoiceNo: 'PM/2026-27/000007',
    });
    render(<MemoryRouter initialEntries={['/subscription?returnTo=%2Fexams%2Fibps-po%2Finstructions']}><Routes><Route path="/subscription" element={<SubscriptionPage />} /></Routes></MemoryRouter>);
    await user.click(screen.getAllByRole('button', { name: /buy 1 credit/i })[0]!);
    const dialog = await screen.findByRole('dialog');
    await user.click(within(dialog).getByLabelText(/refund and cancellation policy/i));
    await user.click(within(dialog).getByRole('button', { name: /^pay /i }));
    expect(await within(dialog).findByText('Payment received — confirming it')).toBeInTheDocument();
    expect(within(dialog).queryByRole('button', { name: /try again|^pay /i })).toBeNull();
    await user.click(within(dialog).getByRole('button', { name: 'Check status' }));
    expect(check).toHaveBeenCalledWith('ord-1', 'pay-per-mock', 'upi');
    expect(await within(dialog).findByTestId('new-balance')).toBeInTheDocument();
    expect(within(dialog).getByText(/PM\/2026-27\/000007/)).toBeInTheDocument();
    // Came from an exam that needed credits: go straight back to it.
    expect(within(dialog).getByRole('link', { name: 'Continue to your test' })).toHaveAttribute('href', '/exams/ibps-po/instructions');
  });

  it('ignores a returnTo that leaves the site', async () => {
    const user = userEvent.setup();
    render(<MemoryRouter initialEntries={['/subscription?returnTo=%2F%2Fevil.example']}><Routes><Route path="/subscription" element={<SubscriptionPage />} /></Routes></MemoryRouter>);
    await user.click(screen.getAllByRole('button', { name: /buy 1 credit/i })[0]!);
    const dialog = await screen.findByRole('dialog');
    await user.click(within(dialog).getByLabelText(/refund and cancellation policy/i));
    await user.click(within(dialog).getByRole('button', { name: /^pay /i }));
    await within(dialog).findByTestId('new-balance');
    expect(within(dialog).queryByRole('link', { name: 'Continue to your test' })).toBeNull();
    expect(within(dialog).getByRole('link', { name: 'Start practising' })).toHaveAttribute('href', '/exams');
  });
});

describe('Day 8 — credits in the app', () => {
  it('header shows the balance, and "Buy credits" at 0', () => {
    const { rerender } = render(<MemoryRouter><AppTopbar /></MemoryRouter>);
    expect(screen.getByTestId('header-credits')).toHaveAttribute('href', '/subscription');
    expect(screen.getByTestId('header-credits')).toHaveTextContent(`${useSubscriptionStore.getState().sub.credits} credits`);
    useSubscriptionStore.getState().reset('user-d8', { ...NEW_USER_SUBSCRIPTION, credits: 0 });
    rerender(<MemoryRouter><AppTopbar /></MemoryRouter>);
    expect(screen.getByTestId('header-credits')).toHaveTextContent('Buy credits');
  });

  it('a new user with 0 credits who starts a mock is guided to buy credits, and offered the free mini mock', async () => {
    const user = userEvent.setup();
    useSubscriptionStore.getState().reset('user-d8', { ...NEW_USER_SUBSCRIPTION, credits: 0, freeMiniMockUsed: false });
    render(
      <MemoryRouter initialEntries={['/exams/ibps-po/instructions']}>
        <Routes>
          <Route path="/exams/:id/instructions" element={<ExamInstructionsPage />} />
          <Route path="/subscription" element={<p>Pricing page</p>} />
        </Routes>
      </MemoryRouter>,
    );
    await user.click(await screen.findByRole('checkbox'));
    await user.click(screen.getByRole('button', { name: /Start test/ }));
    const dialog = await screen.findByRole('dialog', { name: 'You need more credits' });
    expect(within(dialog).getByRole('link', { name: /Try the free mini mock/ })).toHaveAttribute('href', '/exams/general-aptitude/instructions');
    await user.click(within(dialog).getByRole('button', { name: 'Get credits' }));
    expect(await screen.findByText('Pricing page')).toBeInTheDocument();
  });
});
