import { useRef, useState, type ReactNode } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { CircleCheck, FileText, Pencil, Upload, X } from 'lucide-react';
import type { EducationLevel, LanguageCode, ResumeInfo } from '@prepmitra/shared';
import {
  EDUCATION_LEVELS, EXAMS, INDIAN_STATES, INTERVIEW_ROLES, LANGUAGES, RESUME_RULES, STREAMS, educationSchema, languageName, languageSchema,
  personalDetailsSchema, targetsSchema, validateResumeFile, type EducationInput, type LanguageInput, type PersonalDetailsInput,
  type TargetsInput,
} from '@prepmitra/shared';
import { Button, Card, ChoiceChip, Input, LanguageSelector, Logo, Notice, Select, Stepper } from '@/components/ui';
import { errorMessage, profileService } from '@/services';
import { useAuthStore, useProfileStore } from '@/store';
import { track } from '@/lib/analytics';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT, useUiLang, type UiLang } from '@/i18n';
import { educationLabel, onboardingMessages, streamLabel } from '@/i18n/messages/onboarding';

const STEP_KEYS = ['step0', 'step1', 'step2', 'step3', 'step4', 'step5'] as const;

const langLabel = (lang: UiLang, code: LanguageCode) =>
  lang === 'hi' ? LANGUAGES.find((l) => l.code === code)?.nativeName ?? languageName(code) : languageName(code);

interface WizardData {
  personal?: PersonalDetailsInput;
  education?: EducationInput;
  targets?: TargetsInput;
  language?: LanguageInput;
  resume?: ResumeInfo | null;
}

function StepShell({ title, description, children, footer }: { title: string; description: string; children: ReactNode; footer: ReactNode }) {
  return (
    <Card className="p-5 sm:p-8">
      <h1 className="text-xl font-bold sm:text-2xl">{title}</h1>
      <p className="mt-1 text-sm text-muted">{description}</p>
      <div className="mt-6 space-y-4">{children}</div>
      <div className="mt-8 flex flex-col-reverse gap-2 border-t border-line pt-5 sm:flex-row sm:justify-between">{footer}</div>
    </Card>
  );
}

function Nav({ onBack, onSave, submitLabel, loading }: { onBack?: () => void; onSave?: () => void; submitLabel?: string; loading?: boolean }) {
  const t = useT(onboardingMessages);
  return (
    <>
      <div className="flex gap-2">
        {onBack && <Button variant="outline" onClick={onBack} disabled={loading}>{t('back')}</Button>}
        {onSave && <Button variant="ghost" onClick={onSave} disabled={loading}>{t('saveLater')}</Button>}
      </div>
      <Button type="submit" loading={loading}>{submitLabel ?? t('continue')}</Button>
    </>
  );
}

export function OnboardingPage() {
  const t = useT(onboardingMessages);
  useDocumentTitle(t('docTitle'));
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.session?.user);
  const updateUser = useAuthStore((s) => s.updateUser);
  const draft = useProfileStore((s) => s.draft);
  const saveDraft = useProfileStore((s) => s.saveDraft);
  const updateProfile = useProfileStore((s) => s.updateProfile);
  const [step, setStep] = useState(draft?.step ?? 0);
  const [data, setData] = useState<WizardData>((draft?.data as WizardData) ?? {});
  const [finishing, setFinishing] = useState(false);

  const persist = (next: WizardData, nextStep: number) => {
    setData(next);
    setStep(nextStep);
    saveDraft({ step: nextStep, data: next as Record<string, unknown> });
    window.scrollTo({ top: 0 });
  };
  const saveLater = () => {
    saveDraft({ step, data: data as Record<string, unknown> });
    toast.success(t('savedToast'));
  };
  const back = () => persist(data, Math.max(0, step - 1));

  const finish = async () => {
    if (!data.personal || !data.education || !data.targets || !data.language) {
      toast.error(t('incompleteToast'));
      return;
    }
    setFinishing(true);
    try {
      const userPatch = {
        name: data.personal.name,
        dob: data.personal.dob,
        state: data.personal.state,
        email: data.personal.email || user?.email,
        preferredLanguage: data.language.preferredLanguage as LanguageCode,
        onboardingComplete: true,
      };
      const profilePatch = {
        educationLevel: data.education.educationLevel,
        stream: data.education.stream,
        institution: data.education.institution,
        graduationYear: data.education.graduationYear,
        experienceYears: data.education.experienceYears,
        targetExamIds: data.targets.targetExamIds,
        targetRoleIds: data.targets.targetRoleIds,
        secondaryLanguage: (data.language.secondaryLanguage || undefined) as LanguageCode | undefined,
        resume: data.resume ?? undefined,
      };
      await profileService.updateMe({ profile: profilePatch });
      updateProfile(profilePatch);
      updateUser(userPatch);
      track('onboarding_completed', { targets: profilePatch.targetExamIds.length + profilePatch.targetRoleIds.length, language: userPatch.preferredLanguage, resume: !!profilePatch.resume });
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
    <div className="min-h-screen bg-background">
      <header className="border-b border-line bg-card">
        <div className="mx-auto flex h-16 max-w-3xl items-center justify-between px-4">
          <Logo to="/" />
          <span className="text-sm text-muted">{t('takes2')}</span>
        </div>
      </header>
      <main id="main" className="mx-auto max-w-3xl px-4 py-8">
        <Stepper steps={STEP_KEYS.map((k) => t(k))} current={step} className="mb-6" />
        {step === 0 && <PersonalStep defaults={data.personal ?? { name: user?.name ?? '', dob: '', state: '', email: user?.email ?? '' }} onSave={saveLater} onNext={(v) => persist({ ...data, personal: v }, 1)} />}
        {step === 1 && <EducationStep defaults={data.education} onBack={back} onSave={saveLater} onNext={(v) => persist({ ...data, education: v }, 2)} />}
        {step === 2 && <TargetsStep defaults={data.targets} onBack={back} onSave={saveLater} onNext={(v) => persist({ ...data, targets: v }, 3)} />}
        {step === 3 && <LanguageStep defaults={data.language} onBack={back} onSave={saveLater} onNext={(v) => persist({ ...data, language: v }, 4)} />}
        {step === 4 && <ResumeStep value={data.resume ?? null} onBack={back} onNext={(r) => persist({ ...data, resume: r }, 5)} />}
        {step === 5 && <ReviewStep data={data} onEdit={(s) => persist(data, s)} onBack={back} onFinish={finish} loading={finishing} />}
      </main>
    </div>
  );
}

function PersonalStep({ defaults, onNext, onSave }: { defaults: PersonalDetailsInput; onNext: (v: PersonalDetailsInput) => void; onSave: () => void }) {
  const t = useT(onboardingMessages);
  const { register, handleSubmit, formState: { errors } } = useForm<PersonalDetailsInput>({ resolver: zodResolver(personalDetailsSchema), defaultValues: defaults });
  return (
    <form onSubmit={handleSubmit(onNext)} noValidate>
      <StepShell title={t('personalTitle')} description={t('personalDesc')} footer={<Nav onSave={onSave} />}>
        <Input label={t('fullName')} required autoComplete="name" error={errors.name?.message} {...register('name')} />
        <div className="grid gap-4 sm:grid-cols-2">
          <Input label={t('dob')} type="date" required error={errors.dob?.message} max={new Date().toISOString().slice(0, 10)} {...register('dob')} />
          <Select label={t('stateUt')} required placeholder={t('selectState')} options={INDIAN_STATES.map((s) => ({ value: s, label: s }))} error={errors.state?.message} {...register('state')} />
        </div>
        <Input label={t('emailOptional')} type="email" autoComplete="email" error={errors.email?.message} {...register('email')} />
      </StepShell>
    </form>
  );
}

function EducationStep({ defaults, onNext, onBack, onSave }: { defaults?: EducationInput; onNext: (v: EducationInput) => void; onBack: () => void; onSave: () => void }) {
  const t = useT(onboardingMessages);
  const lang = useUiLang();
  const { register, handleSubmit, formState: { errors } } = useForm<EducationInput>({
    resolver: zodResolver(educationSchema),
    defaultValues: defaults ?? { educationLevel: undefined as unknown as EducationLevel, stream: '', institution: '', experienceYears: 0 },
  });
  return (
    <form onSubmit={handleSubmit(onNext)} noValidate>
      <StepShell title={t('eduTitle')} description={t('eduDesc')} footer={<Nav onBack={onBack} onSave={onSave} />}>
        <div className="grid gap-4 sm:grid-cols-2">
          <Select label={t('highestEdu')} required placeholder={t('select')} options={EDUCATION_LEVELS.map((e) => ({ value: e.value, label: educationLabel(lang, e.value, e.label) }))} error={errors.educationLevel?.message} {...register('educationLevel')} />
          <Select label={t('stream')} required placeholder={t('selectStream')} options={STREAMS.map((s) => ({ value: s, label: streamLabel(lang, s) }))} error={errors.stream?.message} {...register('stream')} />
        </div>
        <Input label={t('institution')} error={errors.institution?.message} {...register('institution')} />
        <div className="grid gap-4 sm:grid-cols-2">
          <Input
            label={t('yearPassing')}
            type="number"
            inputMode="numeric"
            error={errors.graduationYear?.message}
            {...register('graduationYear', { setValueAs: (v) => (v === '' || v === null ? undefined : Number(v)) })}
          />
          <Input label={t('workExp')} type="number" inputMode="numeric" min={0} max={40} required error={errors.experienceYears?.message} {...register('experienceYears', { valueAsNumber: true })} />
        </div>
      </StepShell>
    </form>
  );
}

function TargetsStep({ defaults, onNext, onBack, onSave }: { defaults?: TargetsInput; onNext: (v: TargetsInput) => void; onBack: () => void; onSave: () => void }) {
  const t = useT(onboardingMessages);
  const { handleSubmit, watch, setValue, formState: { errors } } = useForm<TargetsInput>({
    resolver: zodResolver(targetsSchema),
    defaultValues: defaults ?? { targetExamIds: [], targetRoleIds: [] },
  });
  const exams = watch('targetExamIds');
  const roles = watch('targetRoleIds');
  const toggle = (key: 'targetExamIds' | 'targetRoleIds', id: string) => {
    const current = key === 'targetExamIds' ? exams : roles;
    setValue(key, current.includes(id) ? current.filter((x) => x !== id) : [...current, id], { shouldValidate: true });
  };
  return (
    <form onSubmit={handleSubmit(onNext)} noValidate>
      <StepShell title={t('targetsTitle')} description={t('targetsDesc')} footer={<Nav onBack={onBack} onSave={onSave} />}>
        <fieldset>
          <legend className="text-sm font-medium">{t('targetExams')} <span className="text-muted">{t('selected', { count: exams.length })}</span></legend>
          <div className="mt-3 flex flex-wrap gap-2">
            {EXAMS.map((e) => (
              <ChoiceChip key={e.id} selected={exams.includes(e.id)} onClick={() => toggle('targetExamIds', e.id)}>
                {exams.includes(e.id) && <CircleCheck className="h-4 w-4" aria-hidden />}
                {e.shortTitle}
              </ChoiceChip>
            ))}
          </div>
        </fieldset>
        <fieldset className="pt-2">
          <legend className="text-sm font-medium">{t('targetRoles')} <span className="text-muted">{t('selected', { count: roles.length })}</span></legend>
          <div className="mt-3 flex flex-wrap gap-2">
            {INTERVIEW_ROLES.map((r) => (
              <ChoiceChip key={r.id} selected={roles.includes(r.id)} onClick={() => toggle('targetRoleIds', r.id)}>
                {roles.includes(r.id) && <CircleCheck className="h-4 w-4" aria-hidden />}
                {r.shortTitle}
              </ChoiceChip>
            ))}
          </div>
        </fieldset>
        {errors.targetExamIds && <p role="alert" className="text-sm font-medium text-danger">{errors.targetExamIds.message}</p>}
      </StepShell>
    </form>
  );
}

function LanguageStep({ defaults, onNext, onBack, onSave }: { defaults?: LanguageInput; onNext: (v: LanguageInput) => void; onBack: () => void; onSave: () => void }) {
  const t = useT(onboardingMessages);
  const lang = useUiLang();
  const { handleSubmit, watch, setValue, formState: { errors } } = useForm<LanguageInput>({
    resolver: zodResolver(languageSchema),
    defaultValues: defaults ?? { preferredLanguage: 'en', secondaryLanguage: '' },
  });
  return (
    <form onSubmit={handleSubmit(onNext)} noValidate>
      <StepShell title={t('langTitle')} description={t('langDesc')} footer={<Nav onBack={onBack} onSave={onSave} />}>
        <LanguageSelector label={t('preferredLang')} value={watch('preferredLanguage')} onChange={(v) => setValue('preferredLanguage', v, { shouldValidate: true })} error={errors.preferredLanguage?.message} />
        <Select
          label={t('secondLang')}
          value={watch('secondaryLanguage') ?? ''}
          onChange={(e) => setValue('secondaryLanguage', e.target.value)}
          placeholder={t('none')}
          options={(['en', 'hi', 'mr', 'ta', 'te', 'bn'] as LanguageCode[]).map((code) => ({ value: code, label: langLabel(lang, code) }))}
        />
        <Notice tone="info">{t('voiceNote')}</Notice>
      </StepShell>
    </form>
  );
}

function ResumeStep({ value, onNext, onBack }: { value: ResumeInfo | null; onNext: (r: ResumeInfo | null) => void; onBack: () => void }) {
  const t = useT(onboardingMessages);
  const [resume, setResume] = useState<ResumeInfo | null>(value);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handle = async (file?: File) => {
    if (!file) return;
    setError(null);
    const check = validateResumeFile(file);
    if (!check.ok) {
      setError(check.error);
      return;
    }
    setUploading(true);
    try {
      setResume(await profileService.uploadResume(file));
      toast.success(t('resumeAttached'));
    } catch (e) {
      setError(errorMessage(e));
    } finally {
      setUploading(false);
    }
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onNext(resume);
      }}
    >
      <StepShell
        title={t('resumeTitle')}
        description={t('resumeDesc')}
        footer={<Nav onBack={onBack} submitLabel={resume ? t('continue') : t('skipForNow')} loading={uploading} />}
      >
        {resume ? (
          <div className="flex items-center gap-3 rounded-lg border border-line bg-background p-4">
            <FileText className="h-8 w-8 text-primary" aria-hidden />
            <div className="min-w-0 flex-1">
              <p className="truncate font-medium">{resume.fileName}</p>
              <p className="text-xs text-muted">{t('ready', { size: resume.sizeKb })}</p>
            </div>
            <Button variant="ghost" size="sm" onClick={() => setResume(null)} leftIcon={<X className="h-4 w-4" />}>{t('remove')}</Button>
          </div>
        ) : (
          <div
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              void handle(e.dataTransfer.files[0]);
            }}
            className={`flex flex-col items-center rounded-xl border-2 border-dashed px-6 py-10 text-center transition-colors ${dragOver ? 'border-primary bg-primary-soft' : 'border-line-strong bg-card'}`}
          >
            <Upload className="h-8 w-8 text-primary" aria-hidden />
            <p className="mt-3 font-medium">{t('dragDrop')}</p>
            <p className="mt-1 text-sm text-muted">{t('fileRules', { mb: RESUME_RULES.maxSizeMb })}</p>
            <Button variant="outline" className="mt-4" onClick={() => inputRef.current?.click()} loading={uploading}>{t('chooseFile')}</Button>
            <input
              ref={inputRef}
              type="file"
              accept={RESUME_RULES.acceptedExtensions.join(',')}
              className="sr-only"
              aria-label={t('uploadResume')}
              onChange={(e) => {
                void handle(e.target.files?.[0]);
                e.target.value = '';
              }}
            />
          </div>
        )}
        {error && <p role="alert" className="text-sm font-medium text-danger">{error}</p>}
        <p className="text-xs text-muted">{t('resumePrototype')}</p>
      </StepShell>
    </form>
  );
}

function ReviewStep({ data, onEdit, onBack, onFinish, loading }: { data: WizardData; onEdit: (step: number) => void; onBack: () => void; onFinish: () => void; loading: boolean }) {
  const t = useT(onboardingMessages);
  const lang = useUiLang();
  const Row = ({ label, value }: { label: string; value: ReactNode }) => (
    <div className="grid grid-cols-[140px_1fr] gap-2 py-1.5 text-sm">
      <dt className="text-muted">{label}</dt>
      <dd className="font-medium">{value || '—'}</dd>
    </div>
  );
  const Section = ({ title, step, children }: { title: string; step: number; children: ReactNode }) => (
    <section className="rounded-lg border border-line p-4">
      <div className="flex items-center justify-between">
        <h2 className="font-semibold">{title}</h2>
        <Button variant="ghost" size="sm" onClick={() => onEdit(step)} leftIcon={<Pencil className="h-3.5 w-3.5" />}>{t('edit')}</Button>
      </div>
      <dl className="mt-2">{children}</dl>
    </section>
  );
  const complete = !!(data.personal && data.education && data.targets && data.language);
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onFinish();
      }}
    >
      <StepShell title={t('reviewTitle')} description={t('reviewDesc')} footer={<Nav onBack={onBack} submitLabel={t('completeProfile')} loading={loading} />}>
        {!complete && <Notice tone="warning">{t('incompleteNotice')}</Notice>}
        <Section title={t('step0')} step={0}>
          <Row label={t('name')} value={data.personal?.name} />
          <Row label={t('dob')} value={data.personal?.dob} />
          <Row label={t('state')} value={data.personal?.state} />
          <Row label={t('email')} value={data.personal?.email} />
        </Section>
        <Section title={t('step1')} step={1}>
          <Row label={t('highest')} value={(() => { const e = EDUCATION_LEVELS.find((x) => x.value === data.education?.educationLevel); return e ? educationLabel(lang, e.value, e.label) : ''; })()} />
          <Row label={t('stream')} value={data.education ? streamLabel(lang, data.education.stream) : ''} />
          <Row label={t('experience')} value={data.education ? t('years', { count: data.education.experienceYears }) : ''} />
        </Section>
        <Section title={t('step2')} step={2}>
          <Row label={t('exams')} value={data.targets?.targetExamIds.map((id) => EXAMS.find((e) => e.id === id)?.shortTitle).join(', ')} />
          <Row label={t('roles')} value={data.targets?.targetRoleIds.map((id) => INTERVIEW_ROLES.find((r) => r.id === id)?.shortTitle).join(', ')} />
        </Section>
        <Section title={t('step3')} step={3}>
          <Row label={t('preferred')} value={data.language ? langLabel(lang, data.language.preferredLanguage as LanguageCode) : ''} />
          <Row label={t('second')} value={data.language?.secondaryLanguage ? langLabel(lang, data.language.secondaryLanguage as LanguageCode) : ''} />
        </Section>
        <Section title={t('step4')} step={4}>
          <Row label={t('file')} value={data.resume?.fileName ?? t('notAdded')} />
        </Section>
      </StepShell>
    </form>
  );
}
