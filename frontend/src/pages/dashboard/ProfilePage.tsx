import { useRef, useState, type ReactNode } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import toast from 'react-hot-toast';
import { Link, useSearchParams } from 'react-router-dom';
import { CircleCheck, FileText, Upload } from 'lucide-react';
import type { EducationLevel, LanguageCode } from '@prepmitra/shared';
import {
  EDUCATION_LEVELS, EXAMS, INDIAN_STATES, INTERVIEW_ROLES, LANGUAGES, RESUME_RULES, STREAMS, educationSchema, formatDate, getPlan, languageName, planShortName, languageSchema,
  isProfileReady, maskPhone, profilePersonalSchema, targetsSchema, validateResumeFile, type EducationInput, type LanguageInput, type ProfilePersonalInput,
  type TargetsInput,
} from '@prepmitra/shared';
import {
  Avatar, Badge, Button, Card, CardBody, CardHeader, ChoiceChip, ConfirmationDialog, Input, LanguageSelector, Notice, PageHeader, Select,
} from '@/components/ui';
import { errorMessage, profileService } from '@/services';
import { useAuthStore, useProfileStore, useSubscriptionStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT, useUiLang } from '@/i18n';
import { LanguageSwitcher } from '@/i18n/LanguageSwitcher';
import { accountMessages } from '@/i18n/messages/account';
import { catalogMessages, planCopy } from '@/i18n/messages/catalog';
import { interviewsEnabled, isExamOpen } from '@/config/launch';

const SECOND_LANGS = ['en', 'hi', 'mr', 'ta', 'te', 'bn', 'gu', 'kn'] as const;

function Section({ title, description, children, onSubmit, dirty, saving }: { title: string; description?: string; children: ReactNode; onSubmit: () => void; dirty: boolean; saving: boolean }) {
  const t = useT(accountMessages);
  return (
    <Card>
      <form
        noValidate
        onSubmit={(e) => {
          e.preventDefault();
          onSubmit();
        }}
      >
        <CardHeader title={title} description={description} />
        <CardBody className="space-y-4">{children}</CardBody>
        <div className="flex justify-end gap-2 border-t border-line px-5 py-3">
          <Button type="submit" size="sm" disabled={!dirty} loading={saving}>{t('saveChanges')}</Button>
        </div>
      </form>
    </Card>
  );
}

export function ProfilePage() {
  const t = useT(accountMessages);
  const tcat = useT(catalogMessages);
  const uiLang = useUiLang();
  useDocumentTitle(t('profileTitle'));
  const user = useAuthStore((s) => s.session?.user);
  const updateUser = useAuthStore((s) => s.updateUser);
  const profile = useProfileStore((s) => s.profile);
  const updateProfile = useProfileStore((s) => s.updateProfile);
  const planId = useSubscriptionStore((s) => s.sub.planId);
  const currentPlan = getPlan(planId);
  const planName = currentPlan ? planShortName(currentPlan) : 'Free';
  const [saving, setSaving] = useState<string | null>(null);
  const [params] = useSearchParams();
  const ready = isProfileReady(user, profile);

  const save = async (key: string, apply: () => void, payload: Parameters<typeof profileService.updateMe>[0]) => {
    setSaving(key);
    try {
      await profileService.updateMe(payload);
      apply();
      toast.success(t('profileUpdated'));
      return true;
    } catch (e) {
      toast.error(errorMessage(e));
      return false;
    } finally {
      setSaving(null);
    }
  };

  const personal = useForm<ProfilePersonalInput>({
    resolver: zodResolver(profilePersonalSchema),
    defaultValues: { name: user?.name ?? '', dob: user?.dob ?? '', state: user?.state ?? '', email: user?.email ?? '' },
  });
  const education = useForm<EducationInput>({
    resolver: zodResolver(educationSchema),
    defaultValues: {
      educationLevel: profile.educationLevel ?? (undefined as unknown as EducationLevel),
      stream: profile.stream ?? '',
      institution: profile.institution ?? '',
      graduationYear: profile.graduationYear,
      experienceYears: profile.experienceYears ?? 0,
    },
  });
  const targets = useForm<TargetsInput>({
    resolver: zodResolver(targetsSchema),
    defaultValues: { targetExamIds: profile.targetExamIds, targetRoleIds: profile.targetRoleIds },
  });
  const language = useForm<LanguageInput>({
    resolver: zodResolver(languageSchema),
    defaultValues: { preferredLanguage: user?.preferredLanguage ?? 'en', secondaryLanguage: profile.secondaryLanguage ?? '' },
  });

  if (!user) return null;
  const examIds = targets.watch('targetExamIds');
  const roleIds = targets.watch('targetRoleIds');
  const toggle = (key: 'targetExamIds' | 'targetRoleIds', id: string) => {
    const cur = targets.getValues(key);
    targets.setValue(key, cur.includes(id) ? cur.filter((x) => x !== id) : [...cur, id], { shouldDirty: true, shouldValidate: true });
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <PageHeader title={t('profileTitle')} description={t('profileDesc')} />
      {params.get('complete') === '1' && !ready && <Notice tone="warning" title={t('completeTitle')}>{t('completeBody')}</Notice>}
      {params.get('complete') === '1' && ready && params.get('redirect')?.startsWith('/') && (
        <Notice tone="success" title={t('readyTitle')}>
          <Link to={params.get('redirect')!} className="font-semibold text-primary underline">{t('readyContinue')}</Link>
        </Notice>
      )}

      <Card className="flex flex-col items-start gap-4 p-5 sm:flex-row sm:items-center">
        <Avatar name={user.name} size="lg" />
        <div className="min-w-0 flex-1">
          <p className="text-xl font-bold">{user.name}</p>
          <p className="text-sm text-muted">{maskPhone(user.phone)}{user.email ? ` · ${user.email}` : ''}</p>
          <div className="mt-2 flex flex-wrap gap-1.5">
            <Badge tone="primary">{planCopy(uiLang, planName)}</Badge>
            <Badge>{languageName(user.preferredLanguage)}</Badge>
            <Badge>{t('memberSince', { date: formatDate(user.createdAt) })}</Badge>
          </div>
        </div>
      </Card>

      <Section
        title={t('personalInfo')}
        dirty={personal.formState.isDirty}
        saving={saving === 'personal'}
        onSubmit={personal.handleSubmit(async (v) => {
          const patch = { name: v.name, dob: v.dob, state: v.state || undefined, email: v.email || undefined };
          if (await save('personal', () => updateUser(patch), { user: { ...user, ...patch } })) personal.reset(v);
        })}
      >
        <div className="grid gap-4 sm:grid-cols-2">
          <Input label={t('fullName')} required error={personal.formState.errors.name?.message} {...personal.register('name')} />
          <Input label={t('email')} type="email" error={personal.formState.errors.email?.message} {...personal.register('email')} />
          <Input label={t('dob')} type="date" required max={new Date().toISOString().slice(0, 10)} error={personal.formState.errors.dob?.message} {...personal.register('dob')} />
          <Select label={t('stateUt')} placeholder={t('selectState')} options={INDIAN_STATES.map((s) => ({ value: s, label: s }))} error={personal.formState.errors.state?.message} {...personal.register('state')} />
        </div>
        <Input label={t('mobile')} value={`+91 ${user.phone}`} disabled hint={t('mobileHint')} readOnly />
      </Section>

      <Section
        title={t('education')}
        dirty={education.formState.isDirty}
        saving={saving === 'education'}
        onSubmit={education.handleSubmit(async (v) => {
          if (await save('education', () => updateProfile(v), { profile: { ...profile, ...v } })) education.reset(v);
        })}
      >
        <div className="grid gap-4 sm:grid-cols-2">
          <Select label={t('highestEdu')} required placeholder={t('select')} options={EDUCATION_LEVELS.map((e) => ({ value: e.value, label: t(`edu_${e.value}`) }))} error={education.formState.errors.educationLevel?.message} {...education.register('educationLevel')} />
          <Select label={t('stream')} required placeholder={t('selectStream')} options={STREAMS.map((s) => ({ value: s, label: s }))} error={education.formState.errors.stream?.message} {...education.register('stream')} />
          <Input label={t('institution')} error={education.formState.errors.institution?.message} {...education.register('institution')} />
          <Input label={t('workExp')} type="number" min={0} max={40} required error={education.formState.errors.experienceYears?.message} {...education.register('experienceYears', { valueAsNumber: true })} />
        </div>
      </Section>

      <Section
        title={t('targetsTitle')}
        description={t('targetsDesc')}
        dirty={targets.formState.isDirty}
        saving={saving === 'targets'}
        onSubmit={targets.handleSubmit(async (v) => {
          if (await save('targets', () => updateProfile(v), { profile: { ...profile, ...v } })) targets.reset(v);
        })}
      >
        <fieldset>
          <legend className="text-sm font-medium">{t('targetExams')}</legend>
          <div className="mt-2 flex flex-wrap gap-2">
            {EXAMS.map((e) => (
              <ChoiceChip key={e.id} selected={examIds.includes(e.id)} onClick={() => toggle('targetExamIds', e.id)}>
                {examIds.includes(e.id) && <CircleCheck className="h-4 w-4" aria-hidden />}{e.shortTitle}
                {!isExamOpen(e) && <span className="rounded-full bg-line px-1.5 text-[10px] font-bold uppercase tracking-wide text-muted">{tcat('soon')}</span>}
              </ChoiceChip>
            ))}
          </div>
        </fieldset>
        {interviewsEnabled() && <fieldset>
          <legend className="text-sm font-medium">{t('targetRoles')}</legend>
          <div className="mt-2 flex flex-wrap gap-2">
            {INTERVIEW_ROLES.map((r) => (
              <ChoiceChip key={r.id} selected={roleIds.includes(r.id)} onClick={() => toggle('targetRoleIds', r.id)}>
                {roleIds.includes(r.id) && <CircleCheck className="h-4 w-4" aria-hidden />}{r.shortTitle}
              </ChoiceChip>
            ))}
          </div>
        </fieldset>}
        {targets.formState.errors.targetExamIds && <p role="alert" className="text-sm font-medium text-danger">{targets.formState.errors.targetExamIds.message}</p>}
      </Section>

      <Section
        title={t('langPrefs')}
        dirty={language.formState.isDirty}
        saving={saving === 'language'}
        onSubmit={language.handleSubmit(async (v) => {
          const pref = v.preferredLanguage as LanguageCode;
          const sec = (v.secondaryLanguage || undefined) as LanguageCode | undefined;
          if (await save('language', () => { updateUser({ preferredLanguage: pref }); updateProfile({ secondaryLanguage: sec }); }, { user: { ...user, preferredLanguage: pref } })) language.reset(v);
        })}
      >
        <div className="flex flex-col gap-3 rounded-lg border border-line bg-background p-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="min-w-0">
            <p className="text-sm font-medium">{t('websiteLanguage')}</p>
            <p className="text-xs text-muted">{t('websiteLanguageHint')}</p>
          </div>
          <LanguageSwitcher size="md" className="self-start sm:self-auto" />
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <LanguageSelector label={t('preferredLang')} value={language.watch('preferredLanguage')} onChange={(c) => language.setValue('preferredLanguage', c, { shouldDirty: true })} error={language.formState.errors.preferredLanguage?.message} />
          <Select
            label={t('secondLang')}
            placeholder={t('none')}
            value={language.watch('secondaryLanguage') ?? ''}
            onChange={(e) => language.setValue('secondaryLanguage', e.target.value, { shouldDirty: true })}
            options={SECOND_LANGS.map((code) => {
              const l = LANGUAGES.find((x) => x.code === code);
              return { value: code, label: l ? (uiLang === 'hi' ? l.nativeName : l.name) : code };
            })}
          />
        </div>
      </Section>

      <ResumeCard />
    </div>
  );
}

function ResumeCard() {
  const t = useT(accountMessages);
  const resume = useProfileStore((s) => s.profile.resume);
  const updateProfile = useProfileStore((s) => s.updateProfile);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [confirmRemove, setConfirmRemove] = useState(false);
  const ref = useRef<HTMLInputElement>(null);

  const upload = async (file?: File) => {
    if (!file) return;
    setError(null);
    const check = validateResumeFile(file);
    if (!check.ok) {
      setError(check.error);
      return;
    }
    setUploading(true);
    try {
      const info = await profileService.uploadResume(file);
      updateProfile({ resume: info });
      toast.success(t('resumeUpdated'));
    } catch (e) {
      setError(errorMessage(e));
    } finally {
      setUploading(false);
    }
  };

  return (
    <Card>
      <CardHeader title={t('resumeCv')} description={t('resumeDesc')} />
      <CardBody>
        {resume ? (
          <div className="flex flex-wrap items-center gap-3 rounded-lg border border-line bg-background p-4">
            <FileText className="h-8 w-8 text-primary" aria-hidden />
            <div className="min-w-0 flex-1">
              <p className="truncate font-medium">{resume.fileName}</p>
              <p className="text-xs text-muted">{t('uploadedOn', { size: resume.sizeKb, date: formatDate(resume.uploadedAt) })}</p>
            </div>
            <Badge tone="success">{t('active')}</Badge>
            <Button variant="outline" size="sm" onClick={() => ref.current?.click()} loading={uploading}>{t('replace')}</Button>
            <Button variant="ghost" size="sm" className="text-danger" onClick={() => setConfirmRemove(true)}>{t('remove')}</Button>
          </div>
        ) : (
          <div className="flex flex-col items-center rounded-xl border-2 border-dashed border-line-strong px-6 py-8 text-center">
            <Upload className="h-7 w-7 text-primary" aria-hidden />
            <p className="mt-2 font-medium">{t('noResume')}</p>
            <p className="text-sm text-muted">{t('resumeRules', { mb: RESUME_RULES.maxSizeMb })}</p>
            <Button className="mt-4" variant="outline" onClick={() => ref.current?.click()} loading={uploading}>{t('uploadResume')}</Button>
          </div>
        )}
        <input ref={ref} type="file" className="sr-only" aria-label={t('uploadResume')} accept={RESUME_RULES.acceptedExtensions.join(',')} onChange={(e) => { void upload(e.target.files?.[0]); e.target.value = ''; }} />
        {error && <p role="alert" className="mt-2 text-sm font-medium text-danger">{error}</p>}
      </CardBody>
      <ConfirmationDialog
        open={confirmRemove}
        onOpenChange={setConfirmRemove}
        title={t('removeResumeTitle')}
        description={t('removeResumeDesc')}
        confirmLabel={t('removeResume')}
        variant="danger"
        onConfirm={() => {
          updateProfile({ resume: undefined });
          setConfirmRemove(false);
          toast.success(t('resumeRemoved'));
        }}
      />
    </Card>
  );
}
