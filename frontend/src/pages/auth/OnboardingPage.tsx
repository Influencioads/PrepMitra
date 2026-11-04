import { useState, type ReactNode } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ArrowLeft, ArrowRight, Award, BookOpenCheck, Briefcase, Check, GraduationCap, Languages, Minus, Plus, School, Target,
} from 'lucide-react';
import type { EducationLevel, ExamCategory, LanguageCode } from '@prepmitra/shared';
import {
  EDUCATION_LEVELS, EXAMS, INDIAN_STATES, INTERVIEW_ROLES, LANGUAGES, STREAMS, educationSchema, languageName, onboardingBasicsSchema,
  onboardingTargetsSchema, type EducationInput, type OnboardingBasicsInput, type OnboardingTargetsInput,
} from '@prepmitra/shared';
import { Button, Checkbox, Input, LanguageSelector, Logo, Select } from '@/components/ui';
import { errorMessage, profileService } from '@/services';
import { useAuthStore, useProfileStore } from '@/store';
import { track } from '@/lib/analytics';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT, useUiLang, type UiLang } from '@/i18n';
import { LanguageSwitcher } from '@/i18n/LanguageSwitcher';
import { catalogMessages } from '@/i18n/messages/catalog';
import { educationLabel, onboardingMessages, streamLabel } from '@/i18n/messages/onboarding';
import { cn } from '@/utils/cn';

/**
 * Onboarding (15-day plan, Day 2): 3 steps.
 *  1. About you — name, date of birth (18+) and preferred language (state and email optional)
 *  2. Education & experience
 *  3. Your targets — at least one exam or role, plus Terms/Privacy consent
 * Exams stay locked until name, language and one target are saved (see isProfileReady).
 * Resume upload lives in Profile and in interview setup, not here.
 */
const STEP_KEYS = ['step0', 'step1', 'step2'] as const;
const DRAFT_VERSION = 2;
const POPULAR_LANGS: LanguageCode[] = ['en', 'hi', 'mr', 'ta', 'te', 'bn'];
const CATEGORY_ORDER: ExamCategory[] = ['government', 'banking', 'railway', 'civil-services', 'higher-education', 'campus-placement'];

const langLabel = (lang: UiLang, code: LanguageCode) =>
  lang === 'hi' ? LANGUAGES.find((l) => l.code === code)?.nativeName ?? languageName(code) : languageName(code);

interface WizardData {
  v: typeof DRAFT_VERSION;
  basics?: OnboardingBasicsInput;
  education?: EducationInput;
  targets?: Omit<OnboardingTargetsInput, 'consent'>;
}

/* ------------------------------------------------------------------ shell */

/** Step buttons: three cards that sit on the edge of the green header. */
function StepPills({ step, onGo }: { step: number; onGo: (i: number) => void }) {
  const t = useT(onboardingMessages);
  return (
    <nav aria-label={t('setupTitle')} className="-mt-9 grid grid-cols-3 gap-2.5 px-4 sm:px-8 lg:-mt-12 lg:gap-4 lg:px-12">
      {STEP_KEYS.map((k, i) => {
        const done = i < step;
        const current = i === step;
        const inner = (
          <>
            <span className={cn('block text-[11px] font-medium lg:text-xs', current ? 'text-white/85' : 'text-muted')}>{t('stepWord')}</span>
            <span className={cn('mt-0.5 flex items-center justify-center gap-1 font-display text-2xl font-bold leading-none', current ? 'text-white' : 'text-secondary-hover')}>
              {done ? <Check className="h-5 w-5 text-secondary" strokeWidth={3} aria-hidden /> : i + 1}
            </span>
            <span className={cn('mt-1 block truncate text-[11px] lg:text-sm', current ? 'text-white' : 'text-muted')}>{t(k)}</span>
          </>
        );
        const cls = cn(
          'block w-full rounded-2xl px-2 py-3 text-center shadow-[0_8px_20px_-12px_rgb(16_36_28/0.45)] transition-colors lg:py-4',
          current ? 'bg-[#f26b1d] ring-4 ring-white' : 'bg-white',
        );
        return done ? (
          <button key={k} type="button" onClick={() => onGo(i)} className={cls}>{inner}</button>
        ) : (
          <div key={k} className={cls} aria-current={current ? 'step' : undefined}>{inner}</div>
        );
      })}
    </nav>
  );
}

function StepShell({ step, title, description, children, footer }: { step: number; title: string; description: string; children: ReactNode; footer: ReactNode }) {
  const t = useT(onboardingMessages);
  return (
    <div className="flex min-h-full flex-col">
      <div className="mx-auto w-full max-w-[640px] flex-1 px-5 pb-8 pt-6 sm:px-8 lg:pt-10">
        <div className="text-center">
          <p className="sr-only">{t('stepOf', { n: step + 1 })}</p>
          <h1 className="font-display text-[28px] font-bold leading-tight tracking-tight text-secondary-hover sm:text-[40px]">{title}</h1>
          <p className="mx-auto mt-2 max-w-md text-[15px] text-muted">{description}</p>
        </div>
        <div className="mt-9 space-y-6">{children}</div>
      </div>
      <div className="sticky bottom-0 z-10 border-t border-line bg-paper lg:rounded-b-[32px]">
        <div className="mx-auto flex w-full max-w-[640px] items-center gap-2 px-5 py-4 sm:px-8">{footer}</div>
      </div>
    </div>
  );
}

function Nav({ onBack, onSave, submitLabel, loading }: { onBack?: () => void; onSave?: () => void; submitLabel?: string; loading?: boolean }) {
  const t = useT(onboardingMessages);
  return (
    <>
      {onBack && (
        <Button variant="ghost" onClick={onBack} disabled={loading} leftIcon={<ArrowLeft className="h-4 w-4" aria-hidden />} className="px-3">
          {t('back')}
        </Button>
      )}
      {onSave && (
        <Button variant="link" onClick={onSave} disabled={loading} className="hidden text-muted hover:text-primary sm:inline-flex">
          {t('saveLater')}
        </Button>
      )}
      <Button
        type="submit"
        size="lg"
        loading={loading}
        className="group ml-auto rounded-xl bg-[#f26b1d] px-6 hover:bg-[#e05e12] shadow-[0_12px_26px_-12px_rgb(242_107_29/0.9)]"
        rightIcon={<ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" aria-hidden />}
      >
        {submitLabel ?? t('continue')}
      </Button>
    </>
  );
}

/** Small uppercase divider label inside a step. */
function GroupLabel({ children, right }: { children: ReactNode; right?: ReactNode }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs font-bold uppercase tracking-[0.12em] text-subtle">{children}</span>
      <span className="h-px flex-1 bg-line" />
      {right}
    </div>
  );
}

/* ------------------------------------------------------------------- page */

export function OnboardingPage() {
  const t = useT(onboardingMessages);
  useDocumentTitle(t('docTitle'));
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.session?.user);
  const updateUser = useAuthStore((s) => s.updateUser);
  const draft = useProfileStore((s) => s.draft);
  const saveDraft = useProfileStore((s) => s.saveDraft);
  const updateProfile = useProfileStore((s) => s.updateProfile);
  // Drafts saved by the older 6-step wizard are ignored.
  const saved = (draft?.data as Partial<WizardData> | undefined)?.v === DRAFT_VERSION ? draft : null;
  const [step, setStep] = useState(Math.min(saved?.step ?? 0, 2));
  const [data, setData] = useState<WizardData>((saved?.data as unknown as WizardData) ?? { v: DRAFT_VERSION });
  const [finishing, setFinishing] = useState(false);

  const persist = (next: WizardData, nextStep: number) => {
    setData(next);
    setStep(nextStep);
    saveDraft({ step: nextStep, data: next as unknown as Record<string, unknown> });
    window.scrollTo({ top: 0 });
    document.getElementById('main')?.scrollTo?.({ top: 0 });
  };
  const saveLater = () => {
    saveDraft({ step, data: data as unknown as Record<string, unknown> });
    toast.success(t('savedToast'));
  };
  const back = () => persist(data, Math.max(0, step - 1));

  const finish = async (targets: OnboardingTargetsInput) => {
    if (!data.basics || !data.education) {
      toast.error(t('incompleteToast'));
      return;
    }
    setFinishing(true);
    try {
      const userPatch = {
        name: data.basics.name,
        dob: data.basics.dob,
        state: data.basics.state || undefined,
        email: data.basics.email || user?.email,
        preferredLanguage: data.basics.preferredLanguage as LanguageCode,
        onboardingComplete: true,
      };
      const profilePatch = {
        educationLevel: data.education.educationLevel,
        stream: data.education.stream,
        institution: data.education.institution,
        graduationYear: data.education.graduationYear,
        experienceYears: data.education.experienceYears,
        targetExamIds: targets.targetExamIds,
        targetRoleIds: targets.targetRoleIds,
        secondaryLanguage: (data.basics.secondaryLanguage || undefined) as LanguageCode | undefined,
      };
      // POST /v1/me/consents first: the profile is only saved once consent is on record.
      await profileService.recordConsent('terms-and-privacy', true);
      await profileService.updateMe({ user: userPatch, profile: profilePatch });
      updateProfile(profilePatch);
      updateUser(userPatch);
      track('onboarding_completed', { targets: targets.targetExamIds.length + targets.targetRoleIds.length, language: userPatch.preferredLanguage, resume: false });
      saveDraft(null);
      toast.success(t('completeToast'));
      navigate('/dashboard', { replace: true });
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setFinishing(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-ink">
      {/* Solid green header: brand, title */}
      <header className="bg-secondary px-5 pb-[5.5rem] pt-5 text-white sm:px-8 lg:pb-36 lg:pt-7">
        <div className="mx-auto max-w-[820px]">
          <div className="flex items-center justify-between gap-3">
            <Logo light />
            <LanguageSwitcher />
          </div>
          <div className="mt-6 lg:mt-12 lg:text-center">
            <h2 className="font-display text-[34px] font-bold leading-[1.1] text-white lg:text-5xl">{t('setupTitle')}</h2>
            <p className="mt-2 text-sm text-white/75 lg:text-base">{t('setupSub')}</p>
          </div>
        </div>
      </header>

      {/* Cream card: step buttons on the header edge, then this step's questions */}
      <main
        id="main"
        className="relative z-10 mx-auto -mt-10 flex w-full max-w-[820px] flex-col rounded-t-[28px] bg-paper lg:-mt-16 lg:mb-10 lg:rounded-[32px] lg:shadow-[0_30px_60px_-30px_rgb(16_36_28/0.35)]"
      >
        <StepPills step={step} onGo={(i) => persist(data, i)} />
            {step === 0 && (
              <BasicsStep
                defaults={data.basics ?? { name: user?.name ?? '', dob: user?.dob ?? '', preferredLanguage: user?.preferredLanguage ?? 'en', secondaryLanguage: '', state: user?.state ?? '', email: user?.email ?? '' }}
                onSave={saveLater}
                onNext={(v) => persist({ ...data, basics: v }, 1)}
              />
            )}
            {step === 1 && <EducationStep defaults={data.education} onBack={back} onSave={saveLater} onNext={(v) => persist({ ...data, education: v }, 2)} />}
            {step === 2 && (
              <TargetsStep
                defaults={data.targets}
                onBack={back}
                onSave={(v) => {
                  saveDraft({ step: 2, data: { ...data, targets: v } as unknown as Record<string, unknown> });
                  toast.success(t('savedToast'));
                }}
                onFinish={finish}
                loading={finishing}
              />
            )}
      </main>
    </div>
  );
}

/* ----------------------------------------------------------------- step 1 */

function BasicsStep({ defaults, onNext, onSave }: { defaults: OnboardingBasicsInput; onNext: (v: OnboardingBasicsInput) => void; onSave: () => void }) {
  const t = useT(onboardingMessages);
  const lang = useUiLang();
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<OnboardingBasicsInput>({
    resolver: zodResolver(onboardingBasicsSchema),
    defaultValues: defaults,
  });
  const preferred = watch('preferredLanguage');
  const pick = (code: LanguageCode) => setValue('preferredLanguage', code, { shouldValidate: true });
  return (
    <form onSubmit={handleSubmit(onNext)} noValidate className="flex flex-1 flex-col">
      <StepShell step={0} title={t('basicsTitle')} description={t('basicsDesc')} footer={<Nav onSave={onSave} />}>
        <div className="grid gap-4 sm:grid-cols-2">
          <Input label={t('fullName')} required autoComplete="name" className="h-12 rounded-xl" error={errors.name?.message} {...register('name')} />
          <Input
            label={t('dob')}
            type="date"
            required
            className="h-12 rounded-xl"
            hint={t('dobHint')}
            error={errors.dob?.message}
            max={new Date().toISOString().slice(0, 10)}
            {...register('dob')}
          />
        </div>

        <fieldset className="space-y-3">
          <legend className="mb-3 flex items-center gap-2 text-sm font-medium text-ink">
            <Languages className="h-4 w-4 text-secondary" aria-hidden /> {t('preferredLang')}
            <span className="text-danger" aria-hidden>*</span>
          </legend>
          <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3" role="radiogroup" aria-label={t('preferredLang')}>
            {POPULAR_LANGS.map((code) => {
              const l = LANGUAGES.find((x) => x.code === code)!;
              const on = preferred === code;
              return (
                <button
                  key={code}
                  type="button"
                  role="radio"
                  aria-checked={on}
                  onClick={() => pick(code)}
                  className={cn(
                    'relative flex flex-col items-start rounded-2xl border-2 px-4 py-3 text-left transition-all',
                    on ? 'border-primary bg-primary-soft shadow-[0_8px_18px_-12px_rgb(194_65_12/0.7)]' : 'border-line bg-card hover:border-line-strong',
                  )}
                >
                  <span lang={code} className={cn('font-display text-lg font-bold leading-tight', on ? 'text-primary' : 'text-ink')}>{l.nativeName}</span>
                  <span className="text-xs text-muted">{l.name}</span>
                  {on && (
                    <span className="absolute right-2.5 top-2.5 flex h-5 w-5 items-center justify-center rounded-full bg-primary text-white">
                      <Check className="h-3 w-3" strokeWidth={3} aria-hidden />
                    </span>
                  )}
                </button>
              );
            })}
          </div>
          <LanguageSelector
            label={t('otherLang')}
            placeholder={t('otherLangPick')}
            allowed={LANGUAGES.map((l) => l.code).filter((c) => !POPULAR_LANGS.includes(c))}
            value={POPULAR_LANGS.includes(preferred as LanguageCode) ? '' : preferred}
            onChange={pick}
            error={errors.preferredLanguage?.message}
          />
          <p className="text-xs text-muted lg:hidden">{t('langDesc')}</p>
        </fieldset>

        <div className="space-y-4">
          <GroupLabel>{t('optionalDetails')}</GroupLabel>
          <div className="grid gap-4 sm:grid-cols-2">
            <Select
              label={t('secondLang')}
              value={watch('secondaryLanguage') ?? ''}
              onChange={(e) => setValue('secondaryLanguage', e.target.value)}
              placeholder={t('none')}
              options={(['en', 'hi', 'mr', 'ta', 'te', 'bn'] as LanguageCode[]).map((code) => ({ value: code, label: langLabel(lang, code) }))}
            />
            <Select label={t('stateOptional')} placeholder={t('selectState')} options={INDIAN_STATES.map((s) => ({ value: s, label: s }))} {...register('state')} />
            <Input label={t('emailOptional')} type="email" autoComplete="email" containerClassName="sm:col-span-2" error={errors.email?.message} {...register('email')} />
          </div>
        </div>
      </StepShell>
    </form>
  );
}

/* ----------------------------------------------------------------- step 2 */

const EDU_ICONS: Record<string, typeof School> = { '12th': School, graduate: GraduationCap, postgraduate: Award };
const EDU_HINTS = { '12th': 'eduHint12th', graduate: 'eduHintGrad', postgraduate: 'eduHintPg' } as const;
const EXP_QUICK = [0, 1, 2, 3, 5];

function EducationStep({ defaults, onNext, onBack, onSave }: { defaults?: EducationInput; onNext: (v: EducationInput) => void; onBack: () => void; onSave: () => void }) {
  const t = useT(onboardingMessages);
  const lang = useUiLang();
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<EducationInput>({
    resolver: zodResolver(educationSchema),
    defaultValues: defaults ?? { educationLevel: undefined as unknown as EducationLevel, stream: '', institution: '', experienceYears: 0 },
  });
  const level = watch('educationLevel');
  const exp = Number(watch('experienceYears')) || 0;
  const setExp = (n: number) => setValue('experienceYears', Math.max(0, Math.min(40, n)), { shouldValidate: true });

  return (
    <form onSubmit={handleSubmit(onNext)} noValidate className="flex flex-1 flex-col">
      <StepShell step={1} title={t('eduTitle')} description={t('eduDesc')} footer={<Nav onBack={onBack} onSave={onSave} />}>
        <fieldset>
          <legend className="mb-3 text-sm font-medium text-ink">
            {t('eduLevelLabel')} <span className="text-danger" aria-hidden>*</span>
          </legend>
          <div className="grid gap-2.5 sm:grid-cols-3">
            {EDUCATION_LEVELS.map((e) => {
              const Icon = EDU_ICONS[e.value];
              const on = level === e.value;
              return (
                <label
                  key={e.value}
                  className={cn(
                    'relative flex cursor-pointer items-center gap-3 rounded-2xl border-2 p-4 transition-all sm:flex-col sm:items-start sm:gap-3',
                    on ? 'border-primary bg-primary-soft shadow-[0_8px_18px_-12px_rgb(194_65_12/0.7)]' : 'border-line bg-card hover:border-line-strong',
                    'has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-2 has-[:focus-visible]:outline-primary',
                  )}
                >
                  <input type="radio" value={e.value} className="sr-only" {...register('educationLevel')} />
                  <span className={cn('flex h-11 w-11 items-center justify-center rounded-xl', on ? 'bg-primary text-white' : 'bg-secondary-soft text-secondary')}>
                    <Icon className="h-5 w-5" aria-hidden />
                  </span>
                  <span>
                    <span className={cn('block font-semibold', on ? 'text-primary' : 'text-ink')}>{educationLabel(lang, e.value, e.label)}</span>
                    <span className="block text-xs text-muted">{t(EDU_HINTS[e.value])}</span>
                  </span>
                  {on && (
                    <span className="absolute right-3 top-3 flex h-5 w-5 items-center justify-center rounded-full bg-primary text-white">
                      <Check className="h-3 w-3" strokeWidth={3} aria-hidden />
                    </span>
                  )}
                </label>
              );
            })}
          </div>
          {errors.educationLevel && <p role="alert" className="mt-2 text-xs font-medium text-danger">{errors.educationLevel.message}</p>}
        </fieldset>

        <div className="grid gap-4 sm:grid-cols-2">
          <Select label={t('stream')} required placeholder={t('selectStream')} options={STREAMS.map((s) => ({ value: s, label: streamLabel(lang, s) }))} error={errors.stream?.message} {...register('stream')} />
          <Input label={t('institution')} error={errors.institution?.message} {...register('institution')} />
        </div>

        <div className="grid gap-4 sm:grid-cols-[1fr_1.4fr]">
          <Input
            label={t('yearPassing')}
            type="number"
            inputMode="numeric"
            error={errors.graduationYear?.message}
            {...register('graduationYear', { setValueAs: (v) => (v === '' || v === null ? undefined : Number(v)) })}
          />
          <div className="space-y-1.5">
            <label htmlFor="exp-years" className="flex items-center gap-1.5 text-sm font-medium text-ink">
              <Briefcase className="h-4 w-4 text-secondary" aria-hidden /> {t('workExp')} <span className="text-danger" aria-hidden>*</span>
            </label>
            <div className="flex items-center gap-2">
              <button type="button" onClick={() => setExp(exp - 1)} aria-label={t('expLess')} className="flex h-12 w-12 items-center justify-center rounded-xl border border-line-strong bg-card text-ink hover:bg-stone-50 disabled:opacity-40" disabled={exp <= 0}>
                <Minus className="h-4 w-4" />
              </button>
              <input
                id="exp-years"
                type="number"
                inputMode="numeric"
                min={0}
                max={40}
                className="h-12 w-20 rounded-xl border border-line-strong bg-card text-center text-lg font-bold text-ink focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/30"
                {...register('experienceYears', { valueAsNumber: true })}
              />
              <button type="button" onClick={() => setExp(exp + 1)} aria-label={t('expMore')} className="flex h-12 w-12 items-center justify-center rounded-xl border border-line-strong bg-card text-ink hover:bg-stone-50">
                <Plus className="h-4 w-4" />
              </button>
            </div>
            <div className="flex flex-wrap gap-1.5 pt-1">
              {EXP_QUICK.map((n) => (
                <button
                  key={n}
                  type="button"
                  onClick={() => setExp(n)}
                  aria-pressed={exp === n}
                  className={cn('rounded-full border px-3 py-1 text-xs font-semibold transition-colors', exp === n ? 'border-secondary bg-secondary text-white' : 'border-line-strong bg-card text-muted hover:text-ink')}
                >
                  {n === 0 ? t('expFresher') : n === 1 ? t('expYear') : t('expYears', { n: n === 5 ? '5+' : n })}
                </button>
              ))}
            </div>
            {errors.experienceYears && <p role="alert" className="text-xs font-medium text-danger">{errors.experienceYears.message}</p>}
          </div>
        </div>
      </StepShell>
    </form>
  );
}

/* ----------------------------------------------------------------- step 3 */

function TargetChip({ selected, onClick, children }: { selected: boolean; onClick: () => void; children: ReactNode }) {
  return (
    <button
      type="button"
      aria-pressed={selected}
      onClick={onClick}
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full border-2 px-4 py-2 text-sm font-semibold transition-all',
        selected ? 'border-[#f26b1d] bg-[#f26b1d] text-white shadow-[0_8px_18px_-10px_rgb(242_107_29/0.9)]' : 'border-line bg-card text-ink hover:border-line-strong',
      )}
    >
      {selected ? <Check className="h-4 w-4" strokeWidth={3} aria-hidden /> : <Plus className="h-4 w-4 text-subtle" aria-hidden />}
      {children}
    </button>
  );
}

function TargetsStep({
  defaults, onFinish, onBack, onSave, loading,
}: {
  defaults?: Omit<OnboardingTargetsInput, 'consent'>;
  onFinish: (v: OnboardingTargetsInput) => void;
  onBack: () => void;
  onSave: (v: Omit<OnboardingTargetsInput, 'consent'>) => void;
  loading: boolean;
}) {
  const t = useT(onboardingMessages);
  const tc = useT(catalogMessages);
  const { register, handleSubmit, watch, setValue, getValues, formState: { errors } } = useForm<OnboardingTargetsInput>({
    resolver: zodResolver(onboardingTargetsSchema),
    defaultValues: { targetExamIds: defaults?.targetExamIds ?? [], targetRoleIds: defaults?.targetRoleIds ?? [], consent: false },
  });
  const exams = watch('targetExamIds');
  const roles = watch('targetRoleIds');
  const consent = watch('consent');
  const total = exams.length + roles.length;
  const toggle = (key: 'targetExamIds' | 'targetRoleIds', id: string) => {
    const current = key === 'targetExamIds' ? exams : roles;
    setValue(key, current.includes(id) ? current.filter((x) => x !== id) : [...current, id], { shouldValidate: true });
  };
  const groups = CATEGORY_ORDER.map((c) => ({ c, items: EXAMS.filter((e) => e.category === c) })).filter((g) => g.items.length);

  return (
    <form onSubmit={handleSubmit(onFinish)} noValidate className="flex flex-1 flex-col">
      <StepShell
        step={2}
        title={t('targetsTitle')}
        description={t('targetsDesc')}
        footer={<Nav onBack={onBack} onSave={() => onSave({ targetExamIds: getValues('targetExamIds'), targetRoleIds: getValues('targetRoleIds') })} submitLabel={t('startPractising')} loading={loading} />}
      >
        <div
          className={cn(
            'flex items-center gap-3 rounded-2xl border px-4 py-3 text-sm transition-colors',
            total ? 'border-secondary/30 bg-secondary-soft text-secondary-hover' : 'border-dashed border-line-strong bg-card text-muted',
          )}
          aria-live="polite"
        >
          <Target className="h-4 w-4 shrink-0" aria-hidden />
          <span className="font-semibold">{total ? t('nSelected', { count: total }) : t('pickAtLeastOne')}</span>
        </div>

        <fieldset className="space-y-4">
          <legend className="mb-1 flex items-center gap-2 text-sm font-semibold text-ink">
            <BookOpenCheck className="h-4 w-4 text-secondary" aria-hidden /> {t('targetExams')}
          </legend>
          {groups.map(({ c, items }) => (
            <div key={c}>
              <p className="mb-2 text-xs font-bold uppercase tracking-[0.1em] text-subtle">{tc(`cat_${c}_label`)}</p>
              <div className="flex flex-wrap gap-2">
                {items.map((e) => (
                  <TargetChip key={e.id} selected={exams.includes(e.id)} onClick={() => toggle('targetExamIds', e.id)}>{e.shortTitle}</TargetChip>
                ))}
              </div>
            </div>
          ))}
        </fieldset>

        <fieldset>
          <legend className="mb-1 flex items-center gap-2 text-sm font-semibold text-ink">
            <Briefcase className="h-4 w-4 text-secondary" aria-hidden /> {t('targetRoles')}
          </legend>
          <p className="mb-2 text-xs text-muted">{t('rolesHint')}</p>
          <div className="flex flex-wrap gap-2">
            {INTERVIEW_ROLES.map((r) => (
              <TargetChip key={r.id} selected={roles.includes(r.id)} onClick={() => toggle('targetRoleIds', r.id)}>{r.shortTitle}</TargetChip>
            ))}
          </div>
        </fieldset>
        {errors.targetExamIds && <p role="alert" className="text-sm font-medium text-danger">{errors.targetExamIds.message}</p>}

        <div className={cn('rounded-2xl border-2 p-4 transition-colors sm:p-5', consent ? 'border-secondary/40 bg-secondary-soft' : errors.consent ? 'border-danger/50 bg-danger-soft' : 'border-line bg-card')}>
          <Checkbox
            label={
              <span className="font-medium">
                {t('consentLead')}{' '}
                <Link to="/terms" target="_blank" rel="noopener" className="font-semibold text-primary underline">{t('consentTerms')}</Link>{' '}
                {t('consentAnd')}{' '}
                <Link to="/privacy" target="_blank" rel="noopener" className="font-semibold text-primary underline">{t('consentPrivacy')}</Link>
              </span>
            }
            description={t('consentHelp')}
            error={errors.consent?.message}
            {...register('consent')}
          />
        </div>
      </StepShell>
    </form>
  );
}
