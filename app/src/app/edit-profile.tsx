import { useState } from 'react';
import { Alert, StyleSheet, View } from 'react-native';
import { router, usePreventRemove } from 'expo-router';
import { Controller, useForm } from 'react-hook-form';
import type { EducationLevel, LanguageCode, ResumeInfo } from '@prepmitra/shared';
import {
  EDUCATION_LEVELS, EXAMS, INDIAN_STATES, INTERVIEW_ROLES, STREAMS, languageName, profileSchema, targetsSchema,
} from '@prepmitra/shared';
import {
  AppText, Button, Card, CardHeader, Chip, IconTile, Input, LanguageSelector, Screen, Select, toast,
} from '@/components';
import { DateField } from '@/features/onboarding/DateField';
import { useResumePicker } from '@/hooks/useResumePicker';
import { errorMessage, profileService } from '@/services';
import { useAuthStore, useProfileStore } from '@/store';
import { colors, spacing } from '@/theme';

interface FormValues {
  name: string;
  email: string;
  dob: string;
  state: string;
  preferredLanguage: LanguageCode;
  secondaryLanguage: string;
  educationLevel: EducationLevel | '';
  stream: string;
  institution: string;
  graduationYear: string;
  experienceYears: string;
  targetExamIds: string[];
  targetRoleIds: string[];
}

const SECOND_LANGS: LanguageCode[] = ['en', 'hi', 'mr', 'ta', 'te', 'bn', 'gu', 'kn'];

/** Edit personal info, education, targets, languages and resume. */
export default function EditProfile() {
  const user = useAuthStore((s) => s.session?.user);
  const updateUser = useAuthStore((s) => s.updateUser);
  const profile = useProfileStore((s) => s.profile);
  const updateProfile = useProfileStore((s) => s.updateProfile);
  const [resume, setResume] = useState<ResumeInfo | undefined>(profile.resume);
  const [saving, setSaving] = useState(false);
  const picker = useResumePicker((r) => {
    setResume(r);
    toast.success('Resume attached. Save to keep it.');
  });

  const { control, handleSubmit, setError, watch, setValue, formState: { errors, isDirty } } = useForm<FormValues>({
    defaultValues: {
      name: user?.name ?? '',
      email: user?.email ?? '',
      dob: user?.dob ?? '',
      state: user?.state ?? '',
      preferredLanguage: user?.preferredLanguage ?? 'en',
      secondaryLanguage: profile.secondaryLanguage ?? '',
      educationLevel: profile.educationLevel ?? '',
      stream: profile.stream ?? '',
      institution: profile.institution ?? '',
      graduationYear: profile.graduationYear ? String(profile.graduationYear) : '',
      experienceYears: String(profile.experienceYears ?? 0),
      targetExamIds: profile.targetExamIds,
      targetRoleIds: profile.targetRoleIds,
    },
  });
  const resumeChanged = resume !== profile.resume;
  const dirty = (isDirty || resumeChanged) && !saving;

  const discard = usePreventRemove(dirty, ({ repeat }) => {
    Alert.alert('Discard changes?', 'You have unsaved changes to your profile.', [
      { text: 'Keep editing', style: 'cancel' },
      { text: 'Discard', style: 'destructive', onPress: repeat },
    ]);
  });

  const onSave = handleSubmit(async (v) => {
    const parsed = profileSchema.safeParse({
      name: v.name,
      email: v.email,
      dob: v.dob,
      state: v.state,
      preferredLanguage: v.preferredLanguage,
      educationLevel: v.educationLevel || undefined,
      stream: v.stream,
      institution: v.institution.trim() || undefined,
      experienceYears: v.experienceYears.trim() === '' ? Number.NaN : Number(v.experienceYears),
    });
    const targets = targetsSchema.safeParse({ targetExamIds: v.targetExamIds, targetRoleIds: v.targetRoleIds });
    const year = v.graduationYear.trim() ? Number(v.graduationYear) : undefined;
    let ok = true;
    if (!parsed.success) {
      ok = false;
      for (const issue of parsed.error.issues) setError(issue.path[0] as keyof FormValues, { message: issue.message });
    }
    if (!targets.success) {
      ok = false;
      setError('targetExamIds', { message: targets.error.issues[0]?.message });
    }
    if (year !== undefined && (Number.isNaN(year) || year < 1980 || year > 2032)) {
      ok = false;
      setError('graduationYear', { message: 'Enter a year between 1980 and 2032' });
    }
    if (!ok || !parsed.success) {
      toast.error('Please fix the highlighted fields.');
      return;
    }
    setSaving(true);
    try {
      const profilePatch = {
        educationLevel: parsed.data.educationLevel,
        stream: parsed.data.stream,
        institution: parsed.data.institution,
        graduationYear: year,
        experienceYears: parsed.data.experienceYears,
        targetExamIds: v.targetExamIds,
        targetRoleIds: v.targetRoleIds,
        secondaryLanguage: (v.secondaryLanguage || undefined) as LanguageCode | undefined,
        resume,
      };
      const userPatch = {
        name: parsed.data.name.trim(),
        email: parsed.data.email || undefined,
        dob: parsed.data.dob,
        state: parsed.data.state,
        preferredLanguage: v.preferredLanguage,
      };
      await profileService.updateMe({ profile: { ...profile, ...profilePatch }, user: user ? { ...user, ...userPatch } : undefined });
      updateProfile(profilePatch);
      updateUser(userPatch);
      discard();
      toast.success('Profile saved.');
      router.back();
    } catch (e) {
      toast.error(errorMessage(e));
      setSaving(false);
    }
  });

  const exams = watch('targetExamIds');
  const roles = watch('targetRoleIds');
  const toggle = (key: 'targetExamIds' | 'targetRoleIds', id: string) => {
    const current = key === 'targetExamIds' ? exams : roles;
    setValue(key, current.includes(id) ? current.filter((x) => x !== id) : [...current, id], { shouldDirty: true });
  };

  return (
    <Screen keyboard footer={<Button title="Save changes" loading={saving} onPress={() => void onSave()} fullWidth disabled={!dirty && !saving} />}>
      <Card style={styles.card}>
        <CardHeader title="Personal details" />
        <Controller control={control} name="name" render={({ field }) => (
          <Input label="Full name" required value={field.value} onChangeText={field.onChange} onBlur={field.onBlur} autoCapitalize="words" error={errors.name?.message} />
        )} />
        <Controller control={control} name="email" render={({ field }) => (
          <Input label="Email (optional)" value={field.value} onChangeText={field.onChange} onBlur={field.onBlur} keyboardType="email-address" autoCapitalize="none" error={errors.email?.message} />
        )} />
        <Controller control={control} name="dob" render={({ field }) => (
          <DateField label="Date of birth" value={field.value} onChange={(d) => field.onChange(d)} error={errors.dob?.message} />
        )} />
        <Controller control={control} name="state" render={({ field }) => (
          <Select label="State / UT" required value={field.value} options={INDIAN_STATES.map((s) => ({ value: s, label: s }))} onChange={field.onChange} error={errors.state?.message} />
        )} />
        <AppText variant="caption">Mobile number: +91 {user?.phone}. Contact support to change it.</AppText>
      </Card>

      <Card style={styles.card}>
        <CardHeader title="Languages" />
        <Controller control={control} name="preferredLanguage" render={({ field }) => (
          <LanguageSelector label="Preferred language" value={field.value} onChange={field.onChange} error={errors.preferredLanguage?.message} />
        )} />
        <Controller control={control} name="secondaryLanguage" render={({ field }) => (
          <Select
            label="Second language (optional)"
            value={field.value}
            placeholder="None"
            options={SECOND_LANGS.map((c) => ({ value: c, label: languageName(c) }))}
            onChange={field.onChange}
            allowClear
            onClear={() => field.onChange('')}
          />
        )} />
      </Card>

      <Card style={styles.card}>
        <CardHeader title="Education" />
        <Controller control={control} name="educationLevel" render={({ field }) => (
          <Select label="Highest education" required value={field.value} options={EDUCATION_LEVELS.map((e) => ({ value: e.value, label: e.label }))} onChange={field.onChange} error={errors.educationLevel?.message} />
        )} />
        <Controller control={control} name="stream" render={({ field }) => (
          <Select label="Stream" required value={field.value} options={STREAMS.map((s) => ({ value: s, label: s }))} onChange={field.onChange} error={errors.stream?.message} />
        )} />
        <Controller control={control} name="institution" render={({ field }) => (
          <Input label="College / institution (optional)" value={field.value} onChangeText={field.onChange} onBlur={field.onBlur} error={errors.institution?.message} />
        )} />
        <View style={styles.row}>
          <View style={styles.flex}>
            <Controller control={control} name="graduationYear" render={({ field }) => (
              <Input label="Year of passing" value={field.value} onChangeText={(t) => field.onChange(t.replace(/\D/g, '').slice(0, 4))} keyboardType="number-pad" maxLength={4} error={errors.graduationYear?.message} />
            )} />
          </View>
          <View style={styles.flex}>
            <Controller control={control} name="experienceYears" render={({ field }) => (
              <Input label="Experience (years)" required value={field.value} onChangeText={(t) => field.onChange(t.replace(/\D/g, '').slice(0, 2))} keyboardType="number-pad" maxLength={2} error={errors.experienceYears?.message} />
            )} />
          </View>
        </View>
      </Card>

      <Card style={styles.card}>
        <CardHeader title="Targets" subtitle="Pick at least one exam or job role" />
        <AppText variant="label">Exams</AppText>
        <View style={styles.chips}>
          {EXAMS.filter((e) => e.status === 'published').map((e) => (
            <Chip key={e.id} role="checkbox" label={e.shortTitle} selected={exams.includes(e.id)} onPress={() => toggle('targetExamIds', e.id)} />
          ))}
        </View>
        <AppText variant="label">Job roles</AppText>
        <View style={styles.chips}>
          {INTERVIEW_ROLES.filter((r) => r.status === 'published').map((r) => (
            <Chip key={r.id} role="checkbox" label={r.shortTitle} selected={roles.includes(r.id)} onPress={() => toggle('targetRoleIds', r.id)} />
          ))}
        </View>
        {errors.targetExamIds?.message ? <AppText variant="small" color={colors.error} accessibilityRole="alert">{errors.targetExamIds.message}</AppText> : null}
      </Card>

      <Card style={styles.card}>
        <CardHeader title="Resume" />
        {resume ? (
          <View style={styles.file}>
            <IconTile name="document-text" size={40} />
            <View style={styles.flex}>
              <AppText variant="smallStrong" numberOfLines={1}>{resume.fileName}</AppText>
              <AppText variant="caption">{resume.sizeKb} KB</AppText>
            </View>
            <Button title="Remove" variant="ghost" size="sm" onPress={() => setResume(undefined)} accessibilityLabel={`Remove ${resume.fileName}`} />
          </View>
        ) : (
          <AppText variant="small">No resume attached.</AppText>
        )}
        <Button title={resume ? 'Replace resume' : 'Upload resume'} variant="outline" leftIcon="cloud-upload-outline" loading={picker.uploading} onPress={() => void picker.pick()} />
        {picker.error ? <AppText variant="small" color={colors.error} accessibilityRole="alert">{picker.error}</AppText> : null}
        <AppText variant="caption">PDF or DOCX, up to 5 MB. Prototype: stays on this device.</AppText>
      </Card>
    </Screen>
  );
}

const styles = StyleSheet.create({
  card: { gap: spacing.md },
  row: { flexDirection: 'row', gap: spacing.md },
  flex: { flex: 1 },
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  file: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
});
