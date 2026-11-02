import { Share } from 'react-native';
import type { ExamReport, InterviewReport } from '@prepmitra/shared';
import { API_ENDPOINTS } from '@prepmitra/shared';
import { examReportText, interviewReportText } from '@/utils/reportText';
import { http } from './http';
import { USE_MOCK, delay } from './mock';

export const reportService = {
  /** GET /v1/attempts/{id}/report */
  async getExamReport(attemptId: string): Promise<ExamReport> {
    return (await http.get<ExamReport>(API_ENDPOINTS.attemptReport(attemptId))).data;
  },

  /** POST /v1/reports/{id}/rating */
  async rate(reportId: string, rating: number): Promise<void> {
    if (!USE_MOCK) {
      await http.post(API_ENDPOINTS.reportRating(reportId), { rating });
      return;
    }
    await delay(300);
  },

  /** Production shares a server-generated PDF link. The prototype shares a text summary. */
  async shareExamReport(r: ExamReport): Promise<boolean> {
    const res = await Share.share({ title: `${r.examTitle} — report`, message: examReportText(r) });
    return res.action === Share.sharedAction;
  },

  async shareInterviewReport(r: InterviewReport): Promise<boolean> {
    const res = await Share.share({ title: `${r.roleTitle} — interview report`, message: interviewReportText(r) });
    return res.action === Share.sharedAction;
  },
};
