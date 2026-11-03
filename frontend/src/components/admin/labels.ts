import type {
  AdminOrderStatus, AdminTeamRole, LessonSource, PaymentGateway, PlanId, PublishStatus, QuestionStatusAdmin, QuestionType,
  ReviewReason, ReviewStatus, Subject,
} from '@prepmitra/shared';
import { ADMIN_MODULES, ADMIN_TEAM_ROLES, LANGUAGES } from '@prepmitra/shared';
import type { BadgeTone, SelectOption } from '@/components/ui';

export const SUBJECT_LABELS: Record<Subject, string> = {
  quant: 'Quantitative aptitude',
  reasoning: 'Reasoning',
  english: 'English',
  'general-awareness': 'General awareness',
  'computer-science': 'Computer science',
  electronics: 'Electronics',
  'general-studies': 'General studies',
  'data-interpretation': 'Data interpretation',
};
export const SUBJECT_OPTIONS: SelectOption[] = Object.entries(SUBJECT_LABELS).map(([value, label]) => ({ value, label }));

export const TYPE_LABELS: Record<QuestionType, string> = { single: 'Single correct', multiple: 'Multiple correct', numeric: 'Numeric' };

export const PUBLISH_STATUS: Record<PublishStatus, { label: string; tone: BadgeTone }> = {
  published: { label: 'Published', tone: 'success' },
  draft: { label: 'Draft', tone: 'neutral' },
  hidden: { label: 'Hidden', tone: 'warning' },
};
export const PUBLISH_OPTIONS: SelectOption[] = (Object.keys(PUBLISH_STATUS) as PublishStatus[]).map((v) => ({ value: v, label: PUBLISH_STATUS[v].label }));

export const QUESTION_STATUS: Record<QuestionStatusAdmin, { label: string; tone: BadgeTone }> = {
  verified: { label: 'Verified', tone: 'success' },
  'pending-review': { label: 'Pending review', tone: 'info' },
  quarantined: { label: 'Quarantined', tone: 'warning' },
  rejected: { label: 'Rejected', tone: 'danger' },
};

export const ORDER_STATUS: Record<AdminOrderStatus, { label: string; tone: BadgeTone }> = {
  paid: { label: 'Paid', tone: 'success' },
  pending: { label: 'Pending', tone: 'info' },
  failed: { label: 'Failed', tone: 'danger' },
  refunded: { label: 'Refunded', tone: 'warning' },
};

export const REVIEW_STATUS: Record<ReviewStatus, { label: string; tone: BadgeTone }> = {
  open: { label: 'Open', tone: 'info' },
  fixed: { label: 'Fix confirmed', tone: 'success' },
  rejected: { label: 'Flag rejected', tone: 'neutral' },
  quarantined: { label: 'Quarantined', tone: 'warning' },
};

export const REASON_LABELS: Record<ReviewReason, string> = {
  'wrong-answer': 'Wrong answer',
  unclear: 'Unclear question',
  translation: 'Translation issue',
  typo: 'Typo',
  'multiple-correct': 'More than one correct',
  outdated: 'Outdated fact',
};

export const LESSON_SOURCE: Record<LessonSource, { label: string; tone: BadgeTone }> = {
  'review-fix': { label: 'Review fix', tone: 'success' },
  'flag-pattern': { label: 'Flag pattern', tone: 'secondary' },
  manual: { label: 'Manual', tone: 'neutral' },
};

export const GATEWAY_LABELS: Record<PaymentGateway, string> = { razorpay: 'Razorpay', cashfree: 'Cashfree' };

export const PLAN_LABELS: Record<PlanId, string> = { free: 'Free', 'pay-per-mock': 'Pay per mock', monthly: 'Monthly', yearly: 'Yearly' };
export const PLAN_TONES: Record<PlanId, BadgeTone> = { free: 'neutral', 'pay-per-mock': 'info', monthly: 'primary', yearly: 'secondary' };

export const TEAM_ROLE_LABELS = Object.fromEntries(ADMIN_TEAM_ROLES.map((r) => [r.id, r.label])) as Record<AdminTeamRole, string>;
export const MODULE_LABELS = Object.fromEntries(ADMIN_MODULES.map((m) => [m.id, m.label])) as Record<string, string>;

export const LANGUAGE_OPTIONS: SelectOption[] = LANGUAGES.map((l) => ({ value: l.code, label: `${l.name} (${l.nativeName})` }));
export const languageLabel = (code: string) => LANGUAGES.find((l) => l.code === code)?.name ?? code;
