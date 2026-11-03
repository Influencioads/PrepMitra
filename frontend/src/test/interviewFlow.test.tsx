import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes, useParams } from 'react-router-dom';
import { startInterview } from '@prepmitra/shared';
import { InterviewSessionPage } from '@/pages/interview/InterviewSessionPage';
import { useInterviewStore, useNotificationStore } from '@/store';

function ReportMarker() {
  const { reportId } = useParams();
  return <p>Report page {reportId}</p>;
}

describe('text interview flow', () => {
  beforeEach(() => {
    const session = startInterview({ roleId: 'hr-executive', level: 'fresher', language: 'en', mode: 'text' }, { id: 'int-test', now: Date.now() });
    useInterviewStore.setState({ ownerId: 'u', sessions: { [session.id]: session }, reports: {} });
    useNotificationStore.setState({ ownerId: 'u', items: [] });
  });

  it('answers a question, gets the next one, ends and saves a report', async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/interview/session/int-test']}>
        <Routes>
          <Route path="/interview/session/:sessionId" element={<InterviewSessionPage />} />
          <Route path="/interview/report/:reportId" element={<ReportMarker />} />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText(/Question 1 of/)).toBeInTheDocument();
    await user.type(
      screen.getByLabelText('Your answer'),
      'I am a commerce graduate with an internship in recruitment where I screened candidates and coordinated interviews because I enjoy working with people.',
    );
    await user.click(screen.getByRole('button', { name: /send answer/i }));

    // "internship" triggers a scripted follow-up on the same question.
    await waitFor(() => expect(useInterviewStore.getState().sessions['int-test']!.turns.length).toBe(3));
    expect(screen.getByText('Follow-up')).toBeInTheDocument();
    expect(screen.getByText(/Question 1 of/)).toBeInTheDocument();
    expect(screen.getByLabelText('Your answer')).toHaveValue('');

    await user.type(screen.getByLabelText('Your answer'), 'Scheduling twenty interviews in two days, so I built a shared calendar.');
    await user.click(screen.getByRole('button', { name: /send answer/i }));
    await waitFor(() => expect(screen.getByText(/Question 2 of/)).toBeInTheDocument());

    await user.click(screen.getByRole('button', { name: /end interview/i }));
    expect(await screen.findByText(/You have answered only 2 questions/)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /end and see report/i }));

    expect(await screen.findByText(/Report page/)).toBeInTheDocument();
    const state = useInterviewStore.getState();
    const session = state.sessions['int-test']!;
    expect(session.status).toBe('completed');
    expect(session.reportId).toBeTruthy();
    expect(state.reports[session.reportId!]!.questionFeedback.length).toBe(1);
    expect(useNotificationStore.getState().items[0]?.type).toBe('interview');
  });

  it('shows an error state for an unknown session', () => {
    render(
      <MemoryRouter initialEntries={['/interview/session/missing']}>
        <Routes>
          <Route path="/interview/session/:sessionId" element={<InterviewSessionPage />} />
        </Routes>
      </MemoryRouter>,
    );
    expect(screen.getByText(/Interview session not found/)).toBeInTheDocument();
  });
});
