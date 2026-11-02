import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { ContactPage } from '@/pages/legal/ContactPage';
import { contactSchema } from '@/pages/legal/contactSchema';
import { PrivacyPage } from '@/pages/legal/PrivacyPage';

describe('Contact page', () => {
  it('validates required fields', () => {
    expect(contactSchema.safeParse({ name: '', email: 'x', topic: '', message: 'short' }).success).toBe(false);
    expect(contactSchema.safeParse({ name: 'Ravi', email: 'ravi@example.com', phone: '', topic: 'payment', message: 'I was charged twice for order 123.' }).success).toBe(true);
  });

  it('shows errors, then a demo success state after a valid submit', async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><ContactPage /></MemoryRouter>);
    await user.click(screen.getByRole('button', { name: /send message/i }));
    expect(await screen.findByText('Enter your name')).toBeInTheDocument();

    await user.type(screen.getByLabelText(/your name/i), 'Ravi Kumar');
    await user.type(screen.getByLabelText(/^email/i), 'ravi@example.com');
    await user.selectOptions(screen.getByLabelText(/topic/i), 'payment');
    await user.type(screen.getByLabelText(/message/i), 'I was charged twice for order ORD-123, please help.');
    await user.click(screen.getByRole('button', { name: /send message/i }));

    await waitFor(() => expect(screen.getByText('Message recorded')).toBeInTheDocument());
    expect(screen.getByText(/this message is not sent anywhere/i)).toBeInTheDocument();
  });
});

describe('Privacy page', () => {
  it('shows the draft notice and sets meta description', () => {
    render(<MemoryRouter><PrivacyPage /></MemoryRouter>);
    expect(screen.getByText('Draft for review')).toBeInTheDocument();
    expect(screen.getAllByText(/Sharing with recruiters/i).length).toBeGreaterThan(0);
    expect(document.title).toContain('Privacy policy');
    expect(document.head.querySelector('meta[name="description"]')?.getAttribute('content')).toMatch(/DPDP/);
  });
});
