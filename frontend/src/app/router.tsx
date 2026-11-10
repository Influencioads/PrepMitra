import { lazy, Suspense, type ComponentType, type ReactNode } from 'react';
import { createBrowserRouter, createHashRouter, Navigate } from 'react-router-dom';
import { LoadingSkeleton } from '@/components/ui';
import { PublicLayout } from '@/layouts/PublicLayout';
import { AppLayout } from '@/layouts/AppLayout';
import { AuthLayout } from '@/layouts/AuthLayout';
import { AdaptiveLayout } from '@/layouts/AdaptiveLayout';
import { GuestOnly, RequireAdmin, RequireAuth, RequireReadyProfile } from './guards';
import { RouteError } from '@/pages/RouteError';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { interviewsEnabled } from '@/config/launch';

/** Mock interviews are switched off for the launch (VITE_INTERVIEWS_ENABLED); their pages send people to the exams. */
function InterviewsGate({ children }: { children: ReactNode }) {
  return interviewsEnabled() ? <>{children}</> : <Navigate to="/exams" replace />;
}

const page = (loader: () => Promise<Record<string, ComponentType>>, name: string) =>
  lazy(async () => ({ default: (await loader())[name] as ComponentType }));

const Fallback = () => (
  <div className="container-page py-10">
    <LoadingSkeleton variant="page" />
  </div>
);
const S = ({ children }: { children: ReactNode }) => <Suspense fallback={<Fallback />}>{children}</Suspense>;

// Public
const LandingPage = page(() => import('@/pages/public/LandingPage'), 'LandingPage');
const ExamCatalogPage = page(() => import('@/pages/public/ExamCatalogPage'), 'ExamCatalogPage');
const ExamDetailsPage = page(() => import('@/pages/public/ExamDetailsPage'), 'ExamDetailsPage');
const SharedReportPage = page(() => import('@/pages/public/SharedReportPage'), 'SharedReportPage');
const PricingPage = page(() => import('@/pages/public/PricingPage'), 'PricingPage');
const PrivacyPage = page(() => import('@/pages/legal/PrivacyPage'), 'PrivacyPage');
const TermsPage = page(() => import('@/pages/legal/TermsPage'), 'TermsPage');
const RefundPolicyPage = page(() => import('@/pages/legal/RefundPolicyPage'), 'RefundPolicyPage');
const ContactPage = page(() => import('@/pages/legal/ContactPage'), 'ContactPage');
const UiKitPage = page(() => import('@/pages/dev/UiKitPage'), 'UiKitPage');
const InterviewCatalogPage = page(() => import('@/pages/interview/InterviewCatalogPage'), 'InterviewCatalogPage');
// Auth
const LoginPage = page(() => import('@/pages/auth/LoginPage'), 'LoginPage');
const SignupPage = page(() => import('@/pages/auth/SignupPage'), 'SignupPage');
const VerifyOtpPage = page(() => import('@/pages/auth/VerifyOtpPage'), 'VerifyOtpPage');
const ForgotPasswordPage = page(() => import('@/pages/auth/ForgotPasswordPage'), 'ForgotPasswordPage');
const OnboardingPage = page(() => import('@/pages/auth/OnboardingPage'), 'OnboardingPage');
// User
const DashboardPage = page(() => import('@/pages/dashboard/DashboardPage'), 'DashboardPage');
const MyTestsPage = page(() => import('@/pages/dashboard/MyTestsPage'), 'MyTestsPage');
const ProgressPage = page(() => import('@/pages/dashboard/ProgressPage'), 'ProgressPage');
const SubscriptionPage = page(() => import('@/pages/dashboard/SubscriptionPage'), 'SubscriptionPage');
const NotificationsPage = page(() => import('@/pages/dashboard/NotificationsPage'), 'NotificationsPage');
const ProfilePage = page(() => import('@/pages/dashboard/ProfilePage'), 'ProfilePage');
const SettingsPage = page(() => import('@/pages/dashboard/SettingsPage'), 'SettingsPage');
// Exam
const ExamInstructionsPage = page(() => import('@/pages/exam/ExamInstructionsPage'), 'ExamInstructionsPage');
const ExamSessionPage = page(() => import('@/pages/exam/ExamSessionPage'), 'ExamSessionPage');
const ReportProcessingPage = page(() => import('@/pages/exam/ReportProcessingPage'), 'ReportProcessingPage');
const ExamResultPage = page(() => import('@/pages/exam/ExamResultPage'), 'ExamResultPage');
const ReportPage = page(() => import('@/pages/exam/ReportPage'), 'ReportPage');
// Interview
const MentorDashboardPage = page(() => import('@/pages/mentor/MentorDashboardPage'), 'MentorDashboardPage');
const StudyPlanPage = page(() => import('@/pages/mentor/StudyPlanPage'), 'StudyPlanPage');
const MockAnalysisPage = page(() => import('@/pages/mentor/MockAnalysisPage'), 'MockAnalysisPage');
const MistakeNotebookPage = page(() => import('@/pages/mentor/MistakeNotebookPage'), 'MistakeNotebookPage');
const MentorChatPage = page(() => import('@/pages/mentor/MentorChatPage'), 'MentorChatPage');

const InterviewSetupPage = page(() => import('@/pages/interview/InterviewSetupPage'), 'InterviewSetupPage');
const InterviewSessionPage = page(() => import('@/pages/interview/InterviewSessionPage'), 'InterviewSessionPage');
const InterviewReportPage = page(() => import('@/pages/interview/InterviewReportPage'), 'InterviewReportPage');
// Admin
const AdminLayout = page(() => import('@/layouts/AdminLayout'), 'AdminLayout');
const AdminDashboardPage = page(() => import('@/pages/admin/AdminDashboardPage'), 'AdminDashboardPage');
const AdminExamsPage = page(() => import('@/pages/admin/AdminExamsPage'), 'AdminExamsPage');
const AdminExamFormPage = page(() => import('@/pages/admin/AdminExamFormPage'), 'AdminExamFormPage');
const AdminQuestionsPage = page(() => import('@/pages/admin/AdminQuestionsPage'), 'AdminQuestionsPage');
const AdminReviewQueuePage = page(() => import('@/pages/admin/AdminReviewQueuePage'), 'AdminReviewQueuePage');
const AdminLessonsPage = page(() => import('@/pages/admin/AdminLessonsPage'), 'AdminLessonsPage');
const AdminLanguagesPage = page(() => import('@/pages/admin/AdminLanguagesPage'), 'AdminLanguagesPage');
const AdminRolesPage = page(() => import('@/pages/admin/AdminRolesPage'), 'AdminRolesPage');
const AdminUsersPage = page(() => import('@/pages/admin/AdminUsersPage'), 'AdminUsersPage');
const AdminPaymentsPage = page(() => import('@/pages/admin/AdminPaymentsPage'), 'AdminPaymentsPage');
const AdminReportsPage = page(() => import('@/pages/admin/AdminReportsPage'), 'AdminReportsPage');
const AdminSettingsPage = page(() => import('@/pages/admin/AdminSettingsPage'), 'AdminSettingsPage');

const auth = (el: ReactNode, opts?: { allowIncompleteOnboarding?: boolean }) => (
  <RequireAuth allowIncompleteOnboarding={opts?.allowIncompleteOnboarding}>
    <S>{el}</S>
  </RequireAuth>
);

export const routes = [
  {
    errorElement: <RouteError />,
    children: [
      {
        element: <PublicLayout />,
        children: [
          { path: '/', element: <S><LandingPage /></S> },
          { path: '/pricing', element: <S><PricingPage /></S> },
          { path: '/ui-kit', element: <S><UiKitPage /></S> },
          { path: '/privacy', element: <S><PrivacyPage /></S> },
          { path: '/terms', element: <S><TermsPage /></S> },
          { path: '/refund-policy', element: <S><RefundPolicyPage /></S> },
          { path: '/contact', element: <S><ContactPage /></S> },
        ],
      },
      {
        // Catalog pages use the app shell when signed in, the marketing shell otherwise.
        element: <AdaptiveLayout />,
        children: [
          { path: '/exams', element: <S><ExamCatalogPage /></S> },
          { path: '/exams/:id', element: <S><ExamDetailsPage /></S> },
          { path: '/shared/reports/:token', element: <S><SharedReportPage /></S> },
          { path: '/interviews', element: <InterviewsGate><S><InterviewCatalogPage /></S></InterviewsGate> },
          { path: '/interviews/:roleId', element: <InterviewsGate>{auth(<RequireReadyProfile><InterviewSetupPage /></RequireReadyProfile>)}</InterviewsGate> },
        ],
      },
      {
        element: <AuthLayout />,
        children: [
          { path: '/login', element: <GuestOnly><S><LoginPage /></S></GuestOnly> },
          { path: '/signup', element: <GuestOnly><S><SignupPage /></S></GuestOnly> },
          { path: '/verify-otp', element: <S><VerifyOtpPage /></S> },
          { path: '/forgot-password', element: <GuestOnly><S><ForgotPasswordPage /></S></GuestOnly> },
        ],
      },
      { path: '/onboarding', element: auth(<OnboardingPage />, { allowIncompleteOnboarding: true }) },
      {
        element: <RequireAuth><AppLayout /></RequireAuth>,
        children: [
          { path: '/dashboard', element: <S><DashboardPage /></S> },
          { path: '/my-tests', element: <S><MyTestsPage /></S> },
          { path: '/exams/:id/instructions', element: <S><RequireReadyProfile><ExamInstructionsPage /></RequireReadyProfile></S> },
          { path: '/exam-result/:reportId', element: <S><ExamResultPage /></S> },
          { path: '/reports/:reportId', element: <S><ReportPage /></S> },
          { path: '/progress', element: <S><ProgressPage /></S> },
          { path: '/mentor', element: <S><MentorDashboardPage /></S> },
          { path: '/mentor/plan', element: <S><StudyPlanPage /></S> },
          { path: '/mentor/analysis/:attemptId', element: <S><MockAnalysisPage /></S> },
          { path: '/mentor/notebook', element: <S><MistakeNotebookPage /></S> },
          { path: '/mentor/chat', element: <S><MentorChatPage /></S> },
          { path: '/subscription', element: <S><SubscriptionPage /></S> },
          { path: '/notifications', element: <S><NotificationsPage /></S> },
          { path: '/profile', element: <S><ProfilePage /></S> },
          { path: '/settings', element: <S><SettingsPage /></S> },
          { path: '/interview/report/:reportId', element: <S><InterviewReportPage /></S> },
        ],
      },
      // Focused, full-screen experiences
      { path: '/exam/:attemptId', element: auth(<RequireReadyProfile><ExamSessionPage /></RequireReadyProfile>) },
      { path: '/exam/:attemptId/processing', element: auth(<S><ReportProcessingPage /></S>) },
      { path: '/interview/session/:sessionId', element: <InterviewsGate>{auth(<InterviewSessionPage />)}</InterviewsGate> },
      {
        path: '/admin',
        element: <RequireAdmin><S><AdminLayout /></S></RequireAdmin>,
        children: [
          { index: true, element: <Navigate to="/admin/dashboard" replace /> },
          { path: 'dashboard', element: <S><AdminDashboardPage /></S> },
          { path: 'exams', element: <S><AdminExamsPage /></S> },
          { path: 'exams/new', element: <S><AdminExamFormPage /></S> },
          { path: 'exams/:examId/edit', element: <S><AdminExamFormPage /></S> },
          { path: 'questions', element: <S><AdminQuestionsPage /></S> },
          { path: 'review-queue', element: <S><AdminReviewQueuePage /></S> },
          { path: 'ai-lessons', element: <S><AdminLessonsPage /></S> },
          { path: 'languages', element: <S><AdminLanguagesPage /></S> },
          { path: 'interview-roles', element: <S><AdminRolesPage /></S> },
          { path: 'users', element: <S><AdminUsersPage /></S> },
          { path: 'payments', element: <S><AdminPaymentsPage /></S> },
          { path: 'reports', element: <S><AdminReportsPage /></S> },
          { path: 'settings', element: <S><AdminSettingsPage /></S> },
        ],
      },
      { path: '*', element: <PublicLayout />, children: [{ path: '*', element: <NotFoundPage /> }] },
    ],
  },
];

/** Hash routing is used for static hosts without SPA rewrites (VITE_ROUTER_MODE=hash). */
export const router = (import.meta.env.VITE_ROUTER_MODE === 'hash' ? createHashRouter : createBrowserRouter)(routes);
