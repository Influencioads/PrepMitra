import { configure, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { AiHubPage } from '@/pages/ai/AiHubPage';
import { DoubtSolverPage } from '@/pages/ai/DoubtSolverPage';
import { TutorPage } from '@/pages/ai/TutorPage';
import { PersonaPage } from '@/pages/ai/PersonaPage';
import { NotesPage } from '@/pages/ai/NotesPage';
import { PracticePage } from '@/pages/ai/PracticePage';
import { CoachPage } from '@/pages/ai/CoachPage';
import { TeachBackPage } from '@/pages/ai/TeachBackPage';
import { CheatCodesPage } from '@/pages/ai/CheatCodesPage';
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
    expect((await screen.findAllByText(/Verified by two AI models/)).length).toBeGreaterThan(0);
    expect(screen.getByText('Shortcut')).toBeInTheDocument();
    expect(screen.getByText('The trap')).toBeInTheDocument();
    // The solved doubt is kept in the session's recent list.
    expect(screen.getByRole('navigation', { name: 'Recent doubts' })).toHaveTextContent(/A price falls by 20%/);
    expect(screen.getByText('About your choice')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /explain differently/i }));
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
    await user.type(await screen.findByLabelText('Message'), 'How do I solve time and work?');
    await user.click(screen.getByRole('button', { name: 'Send' }));
    expect(await screen.findByText(/Turn each worker into a rate/)).toBeInTheDocument();
    await user.click(screen.getByRole('tab', { name: 'Deep dives' }));
    await user.type(screen.getByLabelText('Question or concept'), 'successive percentage change');
    await user.click(screen.getByRole('button', { name: /start deep dive/i }));
    expect(await screen.findByText('Never-again checklist')).toBeInTheDocument();
  });

  it('teaches the blackboard lesson step by step and marks the check question by code', async () => {
    const user = userEvent.setup();
    at(<TutorPage />, '/ai/tutor');
    expect(await screen.findByRole('heading', { name: 'Circular seating arrangement' })).toBeInTheDocument();
    expect(screen.getByText('Step 1 of 6')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /next step/i }));
    await user.click(screen.getByRole('button', { name: /next step/i }));
    expect(screen.getByText('Step 3 of 6')).toBeInTheDocument();
    expect(screen.getByRole('img', { name: /D in seat 1, A in seat 5/ })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /^As*C$/ }));
    expect(await screen.findByText(/Right\.|Not quite/)).toBeInTheDocument();
  });

  it('shows the exam persona with the radar, evidence and game plan', async () => {
    const user = userEvent.setup();
    at(<PersonaPage />, '/ai/persona');
    expect(await screen.findByRole('heading', { name: 'The Fast Guesser', level: 2 })).toBeInTheDocument();
    expect(screen.getByText(/after 380 answers/)).toBeInTheDocument();
    expect(screen.getByText(/96% trait match/)).toBeInTheDocument();
    await user.click(screen.getByRole('tab', { name: /The Perfectionist/ }));
    expect(screen.getByRole('img', { name: /Trait shape: You .*The Perfectionist/ })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Stamina' }));
    expect(screen.getByText(/held at 70% accuracy/)).toBeInTheDocument();
    expect(screen.queryByText(/11 questions in under 15 seconds/)).not.toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'How to beat The Fast Guesser' })).toBeInTheDocument();
    expect(screen.getAllByRole('link', { name: /Start 3-Q drill/ })[0]).toHaveAttribute('href', '/ai/cheat-codes?drill=stem-first-scan');
    expect(screen.getByText(/73 right · 20 wrong → 73 − 5 = 68 marks/)).toBeInTheDocument();
  });

  it('teaches Chotu three rounds and shows the rubric score', async () => {
    const user = userEvent.setup();
    at(<TeachBackPage />, '/ai/teach-back');
    expect(await screen.findByText(/Bhaiya, A sits inside B/)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /Draw it\. Put A fully inside B/ }));
    expect(await screen.findByText(/Spot on/)).toBeInTheDocument();
    expect(screen.getByRole('img', { name: '28 of 30' })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /next round/i }));
    expect(screen.getByRole('heading', { name: /round 2 of 3/i })).toBeInTheDocument();
    await user.type(screen.getByLabelText(/own words/i), 'It is possible but not always: draw C overlapping A, for example.');
    await user.click(screen.getByRole('button', { name: 'Teach this' }));
    expect(await screen.findByText(/R2:/)).toBeInTheDocument();
  });

  it('flips a cheat code and unlocks it with a 3-question drill', async () => {
    const user = userEvent.setup();
    at(<CheatCodesPage />, '/ai/cheat-codes');
    expect(await screen.findByRole('heading', { name: 'Cheat codes', level: 1 })).toBeInTheDocument();
    await user.type(screen.getByLabelText('Search cheat codes'), 'LCM');
    expect(screen.getByRole('heading', { name: '1 code' })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Flip · the trap' }));
    expect(screen.getByText(/take units from the ratio/)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /Flip back/ }));
    await user.click(screen.getByRole('button', { name: 'Practise this code' }));
    const groups = await screen.findAllByRole('radiogroup');
    for (const g of groups) await user.click(within(g).getAllByRole('radio')[0]!);
    await user.click(screen.getByRole('button', { name: /check my answers/i }));
    expect(await screen.findByText(/of 3 right/)).toBeInTheDocument();
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
