import type { InterviewConfig, InterviewReport, InterviewRole, InterviewSession } from '@prepmitra/shared';
import {
  API_ENDPOINTS, INTERVIEW_ROLES, buildInterviewReport, createId, endInterview, getRoleById, startInterview, submitAnswer,
} from '@prepmitra/shared';
import { http } from './http';
import { USE_MOCK, delay, mockError } from './mock';

let roleSource: () => InterviewRole[] = () => INTERVIEW_ROLES;
export const setRoleSource = (fn: () => InterviewRole[]) => {
  roleSource = fn;
};

/**
 * Scripted interview service. Production uses a WebSocket (`/v1/interviews/{id}/stream`)
 * with an LLM interviewer plus speech-to-text / text-to-speech providers.
 */
export const interviewService = {
  /** GET /v1/interview-roles */
  async listRoles(): Promise<InterviewRole[]> {
    if (!USE_MOCK) return (await http.get<InterviewRole[]>(API_ENDPOINTS.interviewRoles)).data;
    await delay(300);
    return roleSource().filter((r) => r.status === 'published');
  },

  async getRole(id: string): Promise<InterviewRole> {
    if (!USE_MOCK) {
      const role = (await http.get<InterviewRole[]>(API_ENDPOINTS.interviewRoles)).data.find((r) => r.id === id);
      if (!role) throw mockError(404, 'ROLE_NOT_FOUND', 'This interview role is not available.');
      return role;
    }
    await delay(250);
    const role = roleSource().find((r) => r.id === id) ?? getRoleById(id);
    if (!role) throw mockError(404, 'ROLE_NOT_FOUND', 'This interview role is not available.');
    return role;
  },

  getRoleSync: (id: string) => roleSource().find((r) => r.id === id) ?? getRoleById(id),

  /** POST /v1/interviews — role, level, language, mode, resume reference and job description. */
  async start(config: InterviewConfig): Promise<InterviewSession> {
    if (!USE_MOCK) return (await http.post<InterviewSession>(API_ENDPOINTS.interviews, config)).data;
    await delay(900);
    return startInterview(config, { id: createId('int') });
  },

  /** GET /v1/interviews/{id} — transcript, so a dropped interview can resume once within 10 minutes. */
  async getSession(id: string): Promise<InterviewSession | null> {
    if (USE_MOCK) return null;
    return (await http.get<InterviewSession>(API_ENDPOINTS.interview(id))).data;
  },

  /** POST /v1/interviews/{id}/answer — saves the answer and returns the session with the next question. */
  async answer(session: InterviewSession, text: string, durationSec?: number): Promise<InterviewSession> {
    if (!USE_MOCK) return (await http.post<InterviewSession>(API_ENDPOINTS.interviewAnswer(session.id), { text, durationSec })).data;
    await delay(1100 + Math.min(text.length, 400) * 2);
    return submitAnswer(session, text, { durationSec });
  },

  /** POST /v1/interviews/{id}/end then GET /v1/interviews/{id}/report */
  async end(session: InterviewSession): Promise<{ session: InterviewSession; report: InterviewReport }> {
    if (!USE_MOCK) {
      await http.post(API_ENDPOINTS.interviewEnd(session.id));
      // The report is written in a background job; poll until it is ready (≤ 60 s target).
      let report: InterviewReport | null = null;
      for (let i = 0; i < 40 && !report; i++) {
        const res = (await http.get<{ status: 'processing' } | { status: 'ready'; report: InterviewReport }>(API_ENDPOINTS.interviewReport(session.id))).data;
        if (res.status === 'ready') report = res.report;
        else await new Promise((r) => setTimeout(r, 3000));
      }
      if (!report) throw mockError(504, 'REPORT_TIMEOUT', 'Your interview report is taking longer than usual. We will email you when it is ready.');
      return { session: { ...session, status: 'completed', reportId: report.id }, report };
    }
    await delay(1400);
    const ended = endInterview(session);
    const role = roleSource().find((r) => r.id === session.config.roleId) ?? getRoleById(session.config.roleId)!;
    const report = buildInterviewReport(ended, role, { id: createId('irep') });
    return { session: { ...ended, reportId: report.id }, report };
  },
};
