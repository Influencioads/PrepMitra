import type { ExamCategory } from '@prepmitra/shared';

/** Soft tint + ink per exam category (warm and green family only). */
export const CATEGORY_TONE: Record<ExamCategory, string> = {
  government: 'bg-primary-soft text-primary',
  banking: 'bg-secondary-soft text-secondary',
  railway: 'bg-sticky-yellow text-[#92400E]',
  'civil-services': 'bg-sticky-purple text-[#7E22CE]',
  'higher-education': 'bg-[#FCE7EC] text-[#9F1239]',
  'campus-placement': 'bg-sticky-green text-[#3F6212]',
};
