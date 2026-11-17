import { describe, expect, it } from 'vitest';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { AiToolsShowcase } from '@/components/marketing/AiToolsShowcase';

describe('AiToolsShowcase (home page)', () => {
  it('shows the six main AI tools and switches the sample demo', async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><AiToolsShowcase /></MemoryRouter>);
    const tabs = screen.getAllByRole('tab');
    expect(tabs).toHaveLength(6);
    const panel = screen.getByRole('tabpanel');
    expect(within(panel).getByText('Sample')).toBeInTheDocument();
    expect(within(panel).getByText(/A 120 m train passes a pole/)).toBeInTheDocument();

    await user.click(tabs[3]);
    expect(tabs[3]).toHaveAttribute('aria-selected', 'true');
    expect(await within(panel).findByText('Percent ↔ fraction')).toBeInTheDocument();

    await user.click(tabs[5]);
    expect(await within(panel).findByText('Your score')).toBeInTheDocument();
    for (const l of screen.getAllByRole('link', { name: /See all AI tools/ })) expect(l).toHaveAttribute('href', '/ai');
  });
});
