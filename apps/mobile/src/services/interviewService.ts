import type { InterviewConfig, InterviewReport, InterviewRole, InterviewSession } from '@prepmitra/shared';
import {
  API_ENDPOINTS, INTERVIEW_ROLES, buildInterviewReport, createId, endInterview, getRoleById, startInterview, submitAnswer,
} from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';

/**
 * Scripted interview service. Production uses a WebSocket (`/v1/interviews/{id}/stream`)
 * with an LLM interviewer plus speech-to-text / text-to-speech providers.
 */
export const interviewService = {
  /** GET /v1/interview-roles */
  async listRoles(): Promise<InterviewRole[]> {
    if (!USE_MOCK) return (await http.get<InterviewRole[]>(API_ENDPOINTS.interviewRoles)).data;
    await delay(300);
    return INTERVIEW_ROLES.filter((r) => r.status === 'published');
  },

  async getRole(id: string): Promise<InterviewRole> {
    if (!USE_MOCK) return (await http.get<InterviewRole>(`${API_ENDPOINTS.interviewRoles}/${id}`)).data;
    await delay(250);
    const role = getRoleById(id);
    if (!role || role.status !== 'published') throw mockError(404, 'ROLE_NOT_FOUND', 'This interview role is not available.');
    return role;
  },

  getRoleSync: (id: string) => getRoleById(id),

  /** POST /v1/interviews */
  async start(config: InterviewConfig): Promise<InterviewSession> {
    if (!USE_MOCK) return (await http.post<InterviewSession>(API_ENDPOINTS.interviews, config)).data;
    await delay(900);
    return startInterview(config, { id: createId('int') });
  },

  /** Mock of a streamed interviewer reply (~1–2 s "thinking" delay). */
  async answer(session: InterviewSession, text: string, durationSec?: number): Promise<InterviewSession> {
    await delay(1100 + Math.min(text.length, 400) * 2);
    return submitAnswer(session, text, { durationSec });
  },

  /** POST /v1/interviews/{id}/end then GET /v1/interviews/{id}/report */
  async end(session: InterviewSession): Promise<{ session: InterviewSession; report: InterviewReport }> {
    if (!USE_MOCK) {
      await http.post(API_ENDPOINTS.interviewEnd(session.id));
      const report = (await http.get<InterviewReport>(API_ENDPOINTS.interviewReport(session.id))).data;
      return { session: { ...session, status: 'completed', reportId: report.id }, report };
    }
    await delay(1400);
    const ended = endInterview(session);
    const role = getRoleById(session.config.roleId);
    if (!role) throw mockError(404, 'ROLE_NOT_FOUND', 'This interview role is no longer available.');
    const report = buildInterviewReport(ended, role, { id: createId('irep') });
    return { session: { ...ended, reportId: report.id }, report };
  },
};
