import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach } from 'vitest';
import { useI18nStore } from '@/i18n';
import { PublicLayout } from '@/layouts/PublicLayout';
import { LandingPage } from '@/pages/public/LandingPage';

function renderLanding() {
  return render(
    <MemoryRouter initialEntries={['/']}>
      <Routes>
        <Route element={<PublicLayout />}>
          <Route index element={<LandingPage />} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

afterEach(() => useI18nStore.getState().setLang('en'));

describe('Website UI language (English / Hindi)', () => {
  it('renders the landing page in Hindi and switches back to English from the header', async () => {
    useI18nStore.getState().setLang('hi');
    const user = userEvent.setup();
    renderLanding();

    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('असली परीक्षा हो।');
    expect(heading).toHaveTextContent('नौकरी पाएँ।');
    expect(screen.getAllByRole('link', { name: /पहला गोला भरें/ }).length).toBeGreaterThan(0);
    // Brand name stays unchanged in Hindi.
    expect(screen.getAllByText(/PrepMitra AI/).length).toBeGreaterThan(0);

    const englishButtons = screen.getAllByRole('button', { name: 'English' });
    expect(englishButtons[0]).toHaveAttribute('aria-pressed', 'false');
    await user.click(englishButtons[0]!);

    expect(useI18nStore.getState().lang).toBe('en');
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('the real exam.');
    expect(screen.getAllByRole('link', { name: /Fill your first bubble/ }).length).toBeGreaterThan(0);
    expect(screen.getByRole('heading', { level: 1 })).not.toHaveTextContent('असली परीक्षा');
    expect(screen.getAllByRole('button', { name: 'हिन्दी' })[0]).toHaveAttribute('aria-pressed', 'false');
  });

  it('defaults to English', () => {
    renderLanding();
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Get Hired.');
  });
});
