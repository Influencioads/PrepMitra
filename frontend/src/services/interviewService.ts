import type { InterviewConfig, InterviewReport, InterviewRole, InterviewSession } from '@prepmitra/shared';
import {
  API_ENDPOINTS, INTERVIEW_ROLES, buildInterviewReport, createId, endInterview, getRoleById, liveCatalog, startInterview, submitAnswer,
  toInterviewReport, toInterviewSession,
} from '@prepmitra/shared';
import { fetchRoles, roleUuid } from './backend';
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
    if (!USE_MOCK) return fetchRoles();
    await delay(300);
    return roleSource().filter((r) => r.status === 'published');
  },

  async getRole(id: string): Promise<InterviewRole> {
    if (!USE_MOCK) {
      const role = (await fetchRoles()).find((r) => r.id === id);
      if (!role) throw mockError(404, 'ROLE_NOT_FOUND', 'This interview role is not available.');
      return role;
    }
    await delay(250);
    const role = roleSource().find((r) => r.id === id) ?? getRoleById(id);
    if (!role) throw mockError(404, 'ROLE_NOT_FOUND', 'This interview role is not available.');
    return role;
  },

  getRoleSync: (id: string) => (USE_MOCK ? undefined : liveCatalog.role(id)) ?? roleSource().find((r) => r.id === id) ?? getRoleById(id),

  /** POST /v1/interviews — role, level, language, mode, resume reference and job description. */
  async start(config: InterviewConfig): Promise<InterviewSession> {
    if (!USE_MOCK) {
      const { data } = await http.post(API_ENDPOINTS.interviews, {
        role_id: await roleUuid(config.roleId),
        level: config.level,
        language: config.language,
        mode: config.mode,
        job_description: config.jobDescription,
        use_profile_resume: !!config.resumeFileName,
      });
      void import('@/store/sync').then((m) => m.syncCredits()).catch(() => undefined);
      return { ...toInterviewSession(data), config };
    }
    await delay(900);
    return startInterview(config, { id: createId('int') });
  },

  /** GET /v1/interviews/{id} — transcript, so a dropped interview can resume once within 10 minutes. */
  async getSession(id: string): Promise<InterviewSession | null> {
    if (USE_MOCK) return null;
    return toInterviewSession((await http.get(API_ENDPOINTS.interview(id))).data);
  },

  /** POST /v1/interviews/{id}/answer — saves the answer and returns the session with the next question. */
  async answer(session: InterviewSession, text: string, durationSec?: number): Promise<InterviewSession> {
    if (!USE_MOCK) {
      await http.post(API_ENDPOINTS.interviewAnswer(session.id), { text, duration_sec: durationSec });
      // The answer call returns only the next turn; reload the session so the transcript matches the server.
      const next = toInterviewSession((await http.get(API_ENDPOINTS.interview(session.id))).data);
      return { ...next, config: session.config };
    }
    await delay(1100 + Math.min(text.length, 400) * 2);
    return submitAnswer(session, text, { durationSec });
  },

  /** POST /v1/interviews/{id}/end then GET /v1/interviews/{id}/report */
  async end(session: InterviewSession): Promise<{ session: InterviewSession; report: InterviewReport }> {
    if (!USE_MOCK) {
      // Ending twice is harmless: a finished interview already has its report job.
      await http.post(API_ENDPOINTS.interviewEnd(session.id)).catch((e) => {
        if (e?.status !== 409) throw e;
      });
      const ended = { ...toInterviewSession((await http.get(API_ENDPOINTS.interview(session.id))).data), config: session.config };
      // The report is written in a background job; poll until it is ready (≤ 60 s target).
      let report: InterviewReport | null = null;
      for (let i = 0; i < 40 && !report; i++) {
        const { data } = await http.get(API_ENDPOINTS.interviewReport(session.id));
        if (data.status === 'ready') report = toInterviewReport(data, ended);
        else if (data.status === 'failed') throw mockError(500, 'REPORT_FAILED', data.error || 'The interview report could not be generated. Your credit has been restored.');
        else await new Promise((r) => setTimeout(r, 3000));
      }
      if (!report) throw mockError(504, 'REPORT_TIMEOUT', 'Your interview report is taking longer than usual. We will email you when it is ready.');
      return { session: { ...ended, status: 'completed', reportId: report.id }, report };
    }
    await delay(1400);
    const ended = endInterview(session);
    const role = roleSource().find((r) => r.id === session.config.roleId) ?? getRoleById(session.config.roleId)!;
    const report = buildInterviewReport(ended, role, { id: createId('irep') });
    return { session: { ...ended, reportId: report.id }, report };
  },
};
