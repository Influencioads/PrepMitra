import { z } from 'zod';
import { RESUME_RULES } from '../constants';

export const phoneSchema = z
  .string()
  .trim()
  .regex(/^[6-9]\d{9}$/, 'Enter a valid 10-digit Indian mobile number');

export const otpSchema = z.object({
  otp: z.string().trim().regex(/^\d{6}$/, 'Enter the 6-digit code'),
});

export const loginSchema = z.object({
  phone: phoneSchema,
});

export const signupSchema = z.object({
  name: z.string().trim().min(2, 'Enter your full name').max(60, 'Name is too long'),
  phone: phoneSchema,
  email: z.union([z.literal(''), z.email('Enter a valid email address')]).optional(),
  ageConfirmed: z.boolean().refine((v) => v, 'You must be 18 or older to use PrepMitra AI'),
  consent: z.boolean().refine((v) => v, 'Please accept the terms and privacy policy'),
});

const isAdult = (dob: string) => {
  const d = new Date(dob);
  if (Number.isNaN(d.getTime())) return false;
  const now = new Date();
  let age = now.getFullYear() - d.getFullYear();
  const m = now.getMonth() - d.getMonth();
  if (m < 0 || (m === 0 && now.getDate() < d.getDate())) age -= 1;
  return age >= 18 && age <= 80;
};

export const personalDetailsSchema = z.object({
  name: z.string().trim().min(2, 'Enter your full name').max(60),
  dob: z.string().min(1, 'Select your date of birth').refine(isAdult, 'You must be between 18 and 80 years old'),
  state: z.string().min(1, 'Select your state'),
  email: z.union([z.literal(''), z.email('Enter a valid email address')]).optional(),
});

export const educationSchema = z.object({
  educationLevel: z.enum(['12th', 'graduate', 'postgraduate'], { message: 'Select your highest education' }),
  stream: z.string().min(1, 'Select your stream'),
  institution: z.string().trim().max(100).optional(),
  graduationYear: z
    .number({ message: 'Enter a valid year' })
    .int()
    .min(1980, 'Enter a year after 1980')
    .max(2032, 'Enter a year before 2032')
    .optional(),
  experienceYears: z.number({ message: 'Enter years of experience' }).min(0).max(40),
});

export const targetsSchema = z
  .object({
    targetExamIds: z.array(z.string()),
    targetRoleIds: z.array(z.string()),
  })
  .refine((v) => v.targetExamIds.length + v.targetRoleIds.length > 0, {
    message: 'Pick at least one target exam or job role',
    path: ['targetExamIds'],
  });

export const languageSchema = z.object({
  preferredLanguage: z.string().min(2, 'Choose a preferred language'),
  secondaryLanguage: z.string().optional(),
});

/** Edit-profile personal details: name and date of birth (18+, checked again by the backend) are required. */
export const profilePersonalSchema = z.object({
  name: z.string().trim().min(2, 'Enter your full name').max(60),
  dob: z.string().min(1, 'Select your date of birth').refine(isAdult, 'You must be between 18 and 80 years old'),
  state: z.string().optional(),
  email: z.union([z.literal(''), z.email('Enter a valid email address')]).optional(),
});

/**
 * Onboarding step 1 (15-day plan, Day 2): name + language, plus date of birth because the backend
 * only lets 18+ users start an exam (GET /v1/me `missing_fields`). State and email are optional.
 */
export const onboardingBasicsSchema = z.object({
  name: z.string().trim().min(2, 'Enter your full name').max(60),
  dob: z.string().min(1, 'Select your date of birth').refine(isAdult, 'You must be between 18 and 80 years old'),
  preferredLanguage: z.string().min(2, 'Choose a preferred language'),
  secondaryLanguage: z.string().optional(),
  state: z.string().optional(),
  email: z.union([z.literal(''), z.email('Enter a valid email address')]).optional(),
});

/** Onboarding step 3: targets plus the Terms/Privacy consent, which is required. */
export const onboardingTargetsSchema = z
  .object({
    targetExamIds: z.array(z.string()),
    targetRoleIds: z.array(z.string()),
    consent: z.boolean().refine((v) => v, 'Please agree to the Terms of Use and Privacy Policy to continue'),
  })
  .refine((v) => v.targetExamIds.length + v.targetRoleIds.length > 0, {
    message: 'Pick at least one target exam or job role',
    path: ['targetExamIds'],
  });

/**
 * A user can start an exam only when their profile has a name, an 18+ date of birth, a preferred language and at
 * least one target exam or role (15-day plan, Day 2). UI check only; the backend enforces it too.
 */
export function isProfileReady(
  user: { name?: string; dob?: string; preferredLanguage?: string; onboardingComplete?: boolean } | null | undefined,
  profile: { targetExamIds?: string[]; targetRoleIds?: string[] } | null | undefined,
): boolean {
  if (!user?.onboardingComplete) return false;
  const hasName = (user.name ?? '').trim().length >= 2;
  const hasLanguage = (user.preferredLanguage ?? '').length >= 2;
  const hasDob = !!user.dob;
  const targets = (profile?.targetExamIds?.length ?? 0) + (profile?.targetRoleIds?.length ?? 0);
  return hasName && hasDob && hasLanguage && targets > 0;
}

export const profileSchema = personalDetailsSchema.extend({
  preferredLanguage: z.string().min(2),
  educationLevel: z.enum(['12th', 'graduate', 'postgraduate']),
  stream: z.string().min(1, 'Select your stream'),
  institution: z.string().trim().max(100).optional(),
  experienceYears: z.number().min(0).max(40),
});

export interface FileLike {
  name: string;
  size: number;
  type?: string;
}

/** Validates resume uploads: PDF or DOCX, max 5 MB (MVP doc §5.1). */
export function validateResumeFile(file: FileLike): { ok: true } | { ok: false; error: string } {
  const lower = file.name.toLowerCase();
  const extOk = RESUME_RULES.acceptedExtensions.some((ext) => lower.endsWith(ext));
  const mimeOk = !file.type || (RESUME_RULES.acceptedMimeTypes as readonly string[]).includes(file.type);
  if (!extOk || !mimeOk) return { ok: false, error: 'Upload a PDF or DOCX file' };
  if (file.size <= 0) return { ok: false, error: 'This file is empty' };
  if (file.size > RESUME_RULES.maxSizeMb * 1024 * 1024)
    return { ok: false, error: `File must be ${RESUME_RULES.maxSizeMb} MB or smaller` };
  return { ok: true };
}

export const interviewSetupSchema = z.object({
  roleId: z.string().min(1, 'Choose a role'),
  level: z.enum(['fresher', '1-3', '3-5']),
  language: z.string().min(2),
  mode: z.enum(['text', 'voice']),
  jobDescription: z.string().max(4000, 'Keep the job description under 4,000 characters').optional(),
});

export const numericAnswerSchema = z
  .string()
  .trim()
  .regex(/^-?\d{0,7}(\.\d{0,4})?$/, 'Enter a number (up to 4 decimals)');

export const demoCheckoutSchema = z.object({
  planId: z.enum(['pay-per-mock', 'monthly', 'yearly']),
  method: z.enum(['upi', 'card', 'netbanking', 'wallet']),
  acceptTerms: z.boolean().refine((v) => v, 'Please accept the refund and cancellation policy'),
});

// ---------- Admin ----------
export const adminExamSchema = z.object({
  title: z.string().trim().min(3, 'Title is required'),
  shortTitle: z.string().trim().min(2, 'Short title is required').max(20),
  category: z.enum(['government', 'banking', 'railway', 'civil-services', 'higher-education', 'campus-placement']),
  conductingBody: z.string().trim().min(2, 'Enter the pattern source (e.g. SSC)'),
  description: z.string().trim().min(20, 'Write at least 20 characters'),
  durationMin: z.number({ message: 'Enter duration' }).int().min(10, 'Min 10 minutes').max(300, 'Max 300 minutes'),
  totalQuestions: z.number({ message: 'Enter question count' }).int().min(5).max(300),
  totalMarks: z.number({ message: 'Enter total marks' }).min(5).max(1000),
  difficulty: z.enum(['Easy', 'Moderate', 'Hard']),
  creditCost: z.number().int().min(0).max(5),
  negativeMarking: z.string().trim().min(1, 'Describe negative marking (or "None")'),
  languages: z.array(z.string()).min(1, 'Pick at least one language'),
  status: z.enum(['published', 'draft', 'hidden']),
  calculatorAllowed: z.boolean(),
});

export const adminQuestionSchema = z
  .object({
    subject: z.string().min(1, 'Select a subject'),
    topic: z.string().trim().min(2, 'Enter a topic'),
    type: z.enum(['single', 'multiple', 'numeric']),
    difficulty: z.enum(['Easy', 'Moderate', 'Hard']),
    text: z.string().trim().min(10, 'Question text is too short'),
    options: z.array(z.string()),
    correct: z.array(z.number()),
    correctNumeric: z.string().optional(),
    explanation: z.string().trim().min(10, 'Add an explanation'),
    shortcut: z.string().optional(),
  })
  .superRefine((v, ctx) => {
    if (v.type === 'numeric') {
      if (!v.correctNumeric || Number.isNaN(Number(v.correctNumeric)))
        ctx.addIssue({ code: 'custom', message: 'Enter the numeric answer', path: ['correctNumeric'] });
      return;
    }
    const filled = v.options.filter((o) => o.trim().length > 0);
    if (filled.length < 2) ctx.addIssue({ code: 'custom', message: 'Add at least two options', path: ['options'] });
    if (v.correct.length === 0) ctx.addIssue({ code: 'custom', message: 'Mark the correct option', path: ['correct'] });
    if (v.type === 'single' && v.correct.length > 1)
      ctx.addIssue({ code: 'custom', message: 'Single-correct questions have exactly one answer', path: ['correct'] });
  });

export const adminRoleSchema = z.object({
  title: z.string().trim().min(3, 'Title is required'),
  shortTitle: z.string().trim().min(2).max(24),
  category: z.string().trim().min(2),
  description: z.string().trim().min(20, 'Write at least 20 characters'),
  levels: z.array(z.enum(['fresher', '1-3', '3-5'])).min(1, 'Pick at least one level'),
  durationMin: z.number().int().min(10).max(60),
  questionCount: z.number().int().min(5).max(15),
  themes: z.string().trim().min(3, 'Enter comma-separated themes'),
  voiceAvailable: z.boolean(),
  status: z.enum(['published', 'draft', 'hidden']),
});

export const adminLessonSchema = z.object({
  topic: z.string().trim().min(2, 'Topic is required'),
  language: z.string().min(2),
  lessonText: z.string().trim().min(15, 'Lesson must be at least 15 characters').max(400),
  active: z.boolean(),
});

export const adminGlossarySchema = z.object({
  term: z.string().trim().min(2, 'Term is required'),
  language: z.string().min(2),
  approvedTranslation: z.string().trim().min(1, 'Translation is required'),
});

export const adminCreditAdjustSchema = z.object({
  delta: z.number({ message: 'Enter a number' }).int().min(-50).max(50).refine((v) => v !== 0, 'Cannot be zero'),
  reason: z.string().trim().min(5, 'Give a reason for the audit log'),
});

export type LoginInput = z.infer<typeof loginSchema>;
export type SignupInput = z.infer<typeof signupSchema>;
export type OtpInput = z.infer<typeof otpSchema>;
export type PersonalDetailsInput = z.infer<typeof personalDetailsSchema>;
export type EducationInput = z.infer<typeof educationSchema>;
export type TargetsInput = z.infer<typeof targetsSchema>;
export type LanguageInput = z.infer<typeof languageSchema>;
export type ProfilePersonalInput = z.infer<typeof profilePersonalSchema>;
export type OnboardingBasicsInput = z.infer<typeof onboardingBasicsSchema>;
export type OnboardingTargetsInput = z.infer<typeof onboardingTargetsSchema>;
export type ProfileInput = z.infer<typeof profileSchema>;
export type InterviewSetupInput = z.infer<typeof interviewSetupSchema>;
export type DemoCheckoutInput = z.infer<typeof demoCheckoutSchema>;
export type AdminExamInput = z.infer<typeof adminExamSchema>;
export type AdminQuestionInput = z.infer<typeof adminQuestionSchema>;
export type AdminRoleInput = z.infer<typeof adminRoleSchema>;
export type AdminLessonInput = z.infer<typeof adminLessonSchema>;
export type AdminGlossaryInput = z.infer<typeof adminGlossarySchema>;
export type AdminCreditAdjustInput = z.infer<typeof adminCreditAdjustSchema>;
