import { configure, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { AiHubPage } from '@/pages/ai/AiHubPage';
import { DoubtSolverPage } from '@/pages/ai/DoubtSolverPage';
import { TutorPage } from '@/pages/ai/TutorPage';
import { PersonaPage } from '@/pages/ai/PersonaPage';
import { NotesPage } from '@/pages/ai/NotesPage';
import { PracticePage } from '@/pages/ai/PracticePage';
import { CoachPage } from '@/pages/ai/CoachPage';
import { AiErrorNotice } from '@/components/ai/AiUi';

// AI screens render a lot at once; give findBy* more time when the whole suite runs in parallel.
configure({ asyncUtilTimeout: 5000 });

const at = (el: React.ReactNode, path = '/') => render(<MemoryRouter initialEntries={[path]}>{el}</MemoryRouter>);

describe('AI study tools (mock mode)', { timeout: 20_000 }, () => {
  it('hub lists every tool with what is left this month', async () => {
    at(<AiHubPage />);
    for (const t of ['Doubt Solver', 'Ask Mitra (AI tutor)', 'Deep dives', 'Persona & rank', 'Notes & topic decks', 'Revision AI', 'Current affairs', 'Writing evaluator', 'Cheat Code Coach']) {
      expect(screen.getByRole('heading', { name: t })).toBeInTheDocument();
    }
    expect((await screen.findAllByText(/of \d+ left/)).length).toBeGreaterThan(0);
  });

  it('solves a doubt and shows the verified answer, shortcut and trap', async () => {
    const user = userEvent.setup();
    at(<DoubtSolverPage />, '/ai/doubts');
    await user.type(screen.getByLabelText('Question'), 'A price falls by 20%. By what percent must it rise to get back?');
    await user.click(screen.getByRole('button', { name: 'C' }));
    await user.click(screen.getByRole('button', { name: /solve/i }));
    expect(await screen.findByText(/Verified by two AI models/)).toBeInTheDocument();
    expect(screen.getByText('Shortcut')).toBeInTheDocument();
    expect(screen.getByText('About your choice')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /explain again/i }));
    expect(await screen.findByText(/Showing a different explanation/)).toBeInTheDocument();
  });

  it('shows the support message prominently on distress', async () => {
    const user = userEvent.setup();
    at(<DoubtSolverPage />, '/ai/doubts');
    await user.type(screen.getByLabelText('Question'), 'I failed again and I want to die');
    await user.click(screen.getByRole('button', { name: /solve/i }));
    expect(await screen.findByText('You are not alone')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /14416/ })).toHaveAttribute('href', 'tel:14416');
  });

  it('shows the off-topic notice', async () => {
    const user = userEvent.setup();
    at(<DoubtSolverPage />, '/ai/doubts');
    await user.type(screen.getByLabelText('Question'), 'Tell me a joke about my girlfriend please');
    await user.click(screen.getByRole('button', { name: /solve/i }));
    expect(await screen.findByText(/stick to exam prep/i)).toBeInTheDocument();
  });

  it('maps errors: 402 upgrade link, 503 try again', () => {
    const { rerender } = at(<AiErrorNotice error={{ status: 402, code: 'ALLOWANCE_EXHAUSTED', message: 'No ultra credits left.' }} />);
    expect(screen.getByRole('link', { name: /see plans/i })).toHaveAttribute('href', '/subscription');
    rerender(<MemoryRouter><AiErrorNotice error={{ status: 503, code: 'AI_UNAVAILABLE', message: 'Busy' }} onRetry={() => undefined} /></MemoryRouter>);
    expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument();
  });

  it('chats with Ask Mitra and builds a deep dive', async () => {
    const user = userEvent.setup();
    at(<TutorPage />, '/ai/tutor');
    await user.type(screen.getByLabelText('Message'), 'How do I solve time and work?');
    await user.click(screen.getByRole('button', { name: 'Send' }));
    expect(await screen.findByText(/Turn each worker into a rate/)).toBeInTheDocument();
    await user.click(screen.getByRole('tab', { name: 'Deep dives' }));
    await user.type(screen.getByLabelText('Question or concept'), 'successive percentage change');
    await user.click(screen.getByRole('button', { name: /start deep dive/i }));
    expect(await screen.findByText('Never-again checklist')).toBeInTheDocument();
  });

  it('shows the persona and the upgrade prompt when Ultra credits run out', async () => {
    const user = userEvent.setup();
    at(<PersonaPage />, '/ai/persona');
    expect(await screen.findByText('Topic mastery')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /ultra review/i }));
    expect(await screen.findByRole('link', { name: /see plans/i })).toBeInTheDocument();
  });

  it('makes notes with a visual and opens a library deck', async () => {
    const user = userEvent.setup();
    at(<NotesPage />, '/ai/notes');
    await user.type(screen.getByLabelText('Topic'), 'Time and work');
    await user.click(screen.getByRole('button', { name: /make notes/i }));
    expect(await screen.findByText('Formulas')).toBeInTheDocument();
    expect(screen.getAllByLabelText('Diagram').length + screen.getAllByLabelText('Mind map').length).toBeGreaterThan(0);
    await user.click(screen.getByRole('tab', { name: /topic explainer/i }));
    await user.click(await screen.findByRole('button', { name: /Percentages/ }));
    expect(await screen.findByText(/Slide 1 of/)).toBeInTheDocument();
  });

  it('runs revision and the writing evaluator', async () => {
    const user = userEvent.setup();
    const { unmount } = at(<PracticePage />, '/ai/practice');
    await user.click(screen.getByRole('button', { name: 'Start' }));
    expect(await screen.findByText(/Each of the students have/)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Check answers' }));
    expect(await screen.findByText(/of 3 correct/)).toBeInTheDocument();
    unmount();
    at(<PracticePage />, '/ai/practice?tab=writing');
    await user.type(screen.getByLabelText('Question'), 'Write an essay on digital India');
    fireEvent.change(screen.getByLabelText(/Your answer/), { target: { value: Array.from({ length: 40 }, (_, i) => `word${i}`).join(' ') } });
    await user.click(screen.getByRole('button', { name: 'Evaluate' }));
    expect(await screen.findByText('Model answer')).toBeInTheDocument();
  });

  it('walks the cheat code coach through spot, shape, test and lock', async () => {
    const user = userEvent.setup();
    at(<CoachPage />, '/ai/coach');
    await waitFor(() => expect(screen.getByRole('option', { name: 'Percentages' })).toBeInTheDocument());
    await user.selectOptions(screen.getByLabelText('Topic'), 'Percentages');
    await user.click(screen.getByRole('button', { name: /start/i }));
    expect(await screen.findByText(/Spot the pattern/)).toBeInTheDocument();
    await user.type(screen.getByLabelText('Your rule'), 'rise = x ÷ (100 − x) of the new price');
    await user.click(screen.getByRole('button', { name: 'Send' }));
    expect(await screen.findByText(/That is exact/)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /test my rule/i }));
    expect(await screen.findByText(/Works on 80%/)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /lock as a revision card/i }));
    expect(await screen.findByText(/Locked\./)).toBeInTheDocument();
  });
});
