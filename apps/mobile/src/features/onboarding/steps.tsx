import { StyleSheet, View } from 'react-native';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import type { EducationLevel, LanguageCode, ResumeInfo } from '@prepmitra/shared';
import {
  EDUCATION_LEVELS, EXAMS, INDIAN_STATES, INTERVIEW_ROLES, RESUME_RULES, STREAMS, educationSchema, languageName, languageSchema,
  personalDetailsSchema, targetsSchema, type EducationInput, type LanguageInput, type PersonalDetailsInput, type TargetsInput,
} from '@prepmitra/shared';
import { AppText, Button, Card, Chip, IconTile, Input, LanguageSelector, Notice, Select } from '@/components';
import { useResumePicker } from '@/hooks/useResumePicker';
import { colors, radii, spacing } from '@/theme';
import { DateField } from './DateField';
import { StepScreen } from './StepScreen';

export interface StepProps<T> {
  defaults?: T;
  onNext: (v: T) => void;
}

export function PersonalStep({ defaults, onNext }: StepProps<PersonalDetailsInput>) {
  const { control, handleSubmit, formState: { errors } } = useForm<PersonalDetailsInput>({
    resolver: zodResolver(personalDetailsSchema),
    defaultValues: defaults ?? { name: '', dob: '', state: '', email: '' },
  });
  return (
    <StepScreen title="Tell us about yourself" description="We use this to personalise your practice and reports." onContinue={handleSubmit(onNext)}>
      <Controller control={control} name="name" render={({ field }) => (
        <Input label="Full name" required value={field.value} onChangeText={field.onChange} onBlur={field.onBlur} autoCapitalize="words" autoComplete="name" error={errors.name?.message} />
      )} />
      <Controller control={control} name="dob" render={({ field }) => (
        <DateField label="Date of birth" value={field.value} onChange={field.onChange} error={errors.dob?.message} />
      )} />
      <Controller control={control} name="state" render={({ field }) => (
        <Select label="State / UT" required placeholder="Select state" value={field.value} options={INDIAN_STATES.map((s) => ({ value: s, label: s }))} onChange={field.onChange} error={errors.state?.message} />
      )} />
      <Controller control={control} name="email" render={({ field }) => (
        <Input label="Email (optional)" value={field.value ?? ''} onChangeText={field.onChange} onBlur={field.onBlur} keyboardType="email-address" autoCapitalize="none" autoComplete="email" error={errors.email?.message} />
      )} />
    </StepScreen>
  );
}

interface EducationForm {
  educationLevel: EducationLevel | '';
  stream: string;
  institution: string;
  graduationYear: string;
  experienceYears: string;
}

export function EducationStep({ defaults, onNext }: StepProps<EducationInput>) {
  const { control, handleSubmit, setError, formState: { errors } } = useForm<EducationForm>({
    defaultValues: {
      educationLevel: defaults?.educationLevel ?? '',
      stream: defaults?.stream ?? '',
      institution: defaults?.institution ?? '',
      graduationYear: defaults?.graduationYear ? String(defaults.graduationYear) : '',
      experienceYears: String(defaults?.experienceYears ?? 0),
    },
  });
  // Text fields hold strings; convert and validate with the shared zod schema.
  const submit = handleSubmit((v) => {
      const parsed = educationSchema.safeParse({
        educationLevel: v.educationLevel || undefined,
        stream: v.stream,
        institution: v.institution.trim() || undefined,
        graduationYear: v.graduationYear.trim() ? Number(v.graduationYear) : undefined,
        experienceYears: v.experienceYears.trim() === '' ? Number.NaN : Number(v.experienceYears),
      });
      if (!parsed.success) {
        for (const issue of parsed.error.issues) {
          const key = issue.path[0] as keyof EducationForm;
          setError(key, { message: issue.message });
        }
        return;
      }
      onNext(parsed.data);
  });
  return (
    <StepScreen title="Your education" description="Helps us recommend the right exams and difficulty." onContinue={submit}>
      <Controller control={control} name="educationLevel" render={({ field }) => (
        <Select label="Highest education" required value={field.value} options={EDUCATION_LEVELS.map((e) => ({ value: e.value, label: e.label }))} onChange={field.onChange} error={errors.educationLevel?.message} />
      )} />
      <Controller control={control} name="stream" render={({ field }) => (
        <Select label="Stream" required placeholder="Select stream" value={field.value} options={STREAMS.map((s) => ({ value: s, label: s }))} onChange={field.onChange} error={errors.stream?.message} />
      )} />
      <Controller control={control} name="institution" render={({ field }) => (
        <Input label="College / institution (optional)" value={field.value} onChangeText={field.onChange} onBlur={field.onBlur} error={errors.institution?.message} />
      )} />
      <View style={styles.row}>
        <View style={styles.flex}>
          <Controller control={control} name="graduationYear" render={({ field }) => (
            <Input label="Year of passing" value={field.value} onChangeText={(t) => field.onChange(t.replace(/\D/g, '').slice(0, 4))} keyboardType="number-pad" maxLength={4} hint="Optional" error={errors.graduationYear?.message} />
          )} />
        </View>
        <View style={styles.flex}>
          <Controller control={control} name="experienceYears" render={({ field }) => (
            <Input label="Experience (years)" required value={field.value} onChangeText={(t) => field.onChange(t.replace(/\D/g, '').slice(0, 2))} keyboardType="number-pad" maxLength={2} error={errors.experienceYears?.message} />
          )} />
        </View>
      </View>
    </StepScreen>
  );
}

export function TargetsStep({ defaults, onNext }: StepProps<TargetsInput>) {
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
    <StepScreen title="What are you preparing for?" description="Pick at least one exam or job role. You can change this later." onContinue={handleSubmit(onNext)}>
      <AppText variant="label">Target exams <AppText variant="small">({exams.length} selected)</AppText></AppText>
      <View style={styles.chips}>
        {EXAMS.filter((e) => e.status === 'published').map((e) => (
          <Chip key={e.id} role="checkbox" label={e.shortTitle} selected={exams.includes(e.id)} onPress={() => toggle('targetExamIds', e.id)} />
        ))}
      </View>
      <AppText variant="label">Target job roles <AppText variant="small">({roles.length} selected)</AppText></AppText>
      <View style={styles.chips}>
        {INTERVIEW_ROLES.filter((r) => r.status === 'published').map((r) => (
          <Chip key={r.id} role="checkbox" label={r.shortTitle} selected={roles.includes(r.id)} onPress={() => toggle('targetRoleIds', r.id)} />
        ))}
      </View>
      {errors.targetExamIds?.message ? (
        <AppText variant="small" color={colors.error} accessibilityRole="alert">{errors.targetExamIds.message}</AppText>
      ) : null}
    </StepScreen>
  );
}

const SECOND_LANGS: LanguageCode[] = ['en', 'hi', 'mr', 'ta', 'te', 'bn', 'gu', 'kn'];

export function LanguageStep({ defaults, onNext }: StepProps<LanguageInput>) {
  const { handleSubmit, watch, setValue, formState: { errors } } = useForm<LanguageInput>({
    resolver: zodResolver(languageSchema),
    defaultValues: defaults ?? { preferredLanguage: 'en', secondaryLanguage: '' },
  });
  return (
    <StepScreen
      title="Choose your language"
      description="Exams, interviews and reports will use this language. You can switch to English during any exam."
      onContinue={handleSubmit(onNext)}
    >
      <LanguageSelector
        label="Preferred language"
        value={watch('preferredLanguage') as LanguageCode}
        onChange={(v) => setValue('preferredLanguage', v, { shouldValidate: true })}
        error={errors.preferredLanguage?.message}
      />
      <Select
        label="Second language (optional)"
        value={watch('secondaryLanguage') ?? ''}
        placeholder="None"
        options={SECOND_LANGS.map((c) => ({ value: c, label: languageName(c) }))}
        onChange={(v) => setValue('secondaryLanguage', v)}
        allowClear
        onClear={() => setValue('secondaryLanguage', '')}
      />
      <Notice tone="info">Voice interviews are available in 12 Tier-1 languages. Other languages support exams and text interviews.</Notice>
    </StepScreen>
  );
}

export function ResumeStep({ value, onChange, onNext }: { value: ResumeInfo | null; onChange: (r: ResumeInfo | null) => void; onNext: () => void }) {
  const { pick, uploading, error } = useResumePicker(onChange);
  return (
    <StepScreen
      title="Add your resume (optional)"
      description="Interview questions and feedback become specific to your projects and experience."
      onContinue={onNext}
      continueLabel={value ? 'Continue' : 'Skip for now'}
      loading={uploading}
    >
      {value ? (
        <Card style={styles.file}>
          <IconTile name="document-text" tone="primary" size={44} />
          <View style={styles.flex}>
            <AppText variant="bodyStrong" numberOfLines={1}>{value.fileName}</AppText>
            <AppText variant="caption">{value.sizeKb} KB · ready</AppText>
          </View>
          <Button title="Remove" variant="ghost" size="sm" leftIcon="close" onPress={() => onChange(null)} accessibilityLabel={`Remove ${value.fileName}`} />
        </Card>
      ) : (
        <View style={styles.drop}>
          <IconTile name="cloud-upload-outline" tone="primary" size={52} />
          <AppText variant="bodyStrong" align="center">Upload your resume</AppText>
          <AppText variant="small" align="center">PDF or DOCX, up to {RESUME_RULES.maxSizeMb} MB</AppText>
          <Button title="Choose file" variant="outline" leftIcon="folder-open-outline" loading={uploading} onPress={() => void pick()} />
        </View>
      )}
      {error ? <AppText variant="small" color={colors.error} accessibilityRole="alert">{error}</AppText> : null}
      <AppText variant="caption">Prototype: the file stays on your device and is not uploaded to any server.</AppText>
    </StepScreen>
  );
}

const styles = StyleSheet.create({
  review: { gap: 6 },
  reviewHead: { flexDirection: 'row', alignItems: 'center' },
  reviewRow: { flexDirection: 'row', gap: spacing.md },
  reviewKey: { width: 100 },
  row: { flexDirection: 'row', gap: spacing.md },
  flex: { flex: 1 },
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  file: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  drop: {
    alignItems: 'center',
    gap: spacing.sm,
    padding: spacing.xl,
    borderRadius: radii.lg,
    borderWidth: 2,
    borderStyle: 'dashed',
    borderColor: colors.borderStrong,
    backgroundColor: colors.white,
  },
});

export interface WizardData {
  personal?: PersonalDetailsInput;
  education?: EducationInput;
  targets?: TargetsInput;
  language?: LanguageInput;
  resume?: ResumeInfo | null;
}

function ReviewSection({ title, onEdit, rows }: { title: string; onEdit: () => void; rows: [string, string | undefined][] }) {
  return (
    <Card style={styles.review}>
      <View style={styles.reviewHead}>
        <AppText variant="bodyStrong" style={styles.flex}>{title}</AppText>
        <Button title="Edit" variant="ghost" size="sm" leftIcon="create-outline" onPress={onEdit} accessibilityLabel={`Edit ${title}`} />
      </View>
      {rows.map(([k, v]) => (
        <View key={k} style={styles.reviewRow}>
          <AppText variant="small" style={styles.reviewKey}>{k}</AppText>
          <AppText variant="smallStrong" style={styles.flex}>{v || '—'}</AppText>
        </View>
      ))}
    </Card>
  );
}

export function ReviewStep({ data, onEdit, onFinish, loading }: { data: WizardData; onEdit: (step: number) => void; onFinish: () => void; loading: boolean }) {
  const complete = !!(data.personal && data.education && data.targets && data.language);
  return (
    <StepScreen title="Review your profile" description="Check everything looks right, then complete your profile." onContinue={onFinish} continueLabel="Complete profile" loading={loading} hideSave>
      {!complete && <Notice tone="warning">Some steps are incomplete. Use Edit to fill them in.</Notice>}
      <ReviewSection
        title="Personal details"
        onEdit={() => onEdit(0)}
        rows={[['Name', data.personal?.name], ['Date of birth', data.personal?.dob], ['State', data.personal?.state], ['Email', data.personal?.email]]}
      />
      <ReviewSection
        title="Education"
        onEdit={() => onEdit(1)}
        rows={[
          ['Highest', EDUCATION_LEVELS.find((e) => e.value === data.education?.educationLevel)?.label],
          ['Stream', data.education?.stream],
          ['Institution', data.education?.institution],
          ['Experience', data.education ? `${data.education.experienceYears} years` : undefined],
        ]}
      />
      <ReviewSection
        title="Targets"
        onEdit={() => onEdit(2)}
        rows={[
          ['Exams', data.targets?.targetExamIds.map((id) => EXAMS.find((e) => e.id === id)?.shortTitle).join(', ')],
          ['Roles', data.targets?.targetRoleIds.map((id) => INTERVIEW_ROLES.find((r) => r.id === id)?.shortTitle).join(', ')],
        ]}
      />
      <ReviewSection
        title="Language"
        onEdit={() => onEdit(3)}
        rows={[
          ['Preferred', data.language ? languageName(data.language.preferredLanguage as LanguageCode) : undefined],
          ['Second', data.language?.secondaryLanguage ? languageName(data.language.secondaryLanguage as LanguageCode) : undefined],
        ]}
      />
      <ReviewSection title="Resume" onEdit={() => onEdit(4)} rows={[['File', data.resume?.fileName ?? 'Not added']]} />
    </StepScreen>
  );
}

