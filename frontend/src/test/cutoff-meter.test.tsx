import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CutoffMeter } from '@/components/marketing/CutoffMeter';

describe('CutoffMeter (home page)', () => {
  it('flips between the before and after scores', async () => {
    const user = userEvent.setup();
    render(<CutoffMeter />);
    const before = screen.getByRole('button', { name: 'After mock 1' });
    const after = screen.getByRole('button', { name: 'After the 7-day plan' });

    await user.click(before);
    expect(before).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByText('2.5 short')).toBeInTheDocument();
    expect(screen.getByText('−4')).toBeInTheDocument();

    await user.click(after);
    expect(after).toHaveAttribute('aria-pressed', 'true');
    expect(await screen.findByText('Cleared by 4.75')).toBeInTheDocument();
    expect(screen.getAllByText(/· plugged/).length).toBe(3);
    expect(screen.getByText(/Sample numbers/)).toBeInTheDocument();
  });
});
