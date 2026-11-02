import { useState } from 'react';
import { Alert } from 'react-native';
import type { LanguageCode, UserProfile } from '@prepmitra/shared';
import { toast } from '@/components';
import { WizardContext } from '@/features/onboarding/StepScreen';
import {
  EducationStep, LanguageStep, PersonalStep, ResumeStep, ReviewStep, TargetsStep, type WizardData,
} from '@/features/onboarding/steps';
import { authService, errorMessage, profileService } from '@/services';
import { useAuthStore, useProfileStore } from '@/store';

const STEPS = ['Personal details', 'Education', 'Targets', 'Language', 'Resume', 'Review'];

/**
 * Six-step profile wizard. Every step is validated with the shared zod schemas
 * and the draft is persisted (AsyncStorage) so it survives an app restart.
 */
export default function Onboarding() {
  const user = useAuthStore((s) => s.session?.user);
  const updateUser = useAuthStore((s) => s.updateUser);
  const signOut = useAuthStore((s) => s.signOut);
  const draft = useProfileStore((s) => s.draft);
  const saveDraft = useProfileStore((s) => s.saveDraft);
  const updateProfile = useProfileStore((s) => s.updateProfile);
  const [step, setStep] = useState(draft?.step ?? 0);
  const [data, setData] = useState<WizardData>((draft?.data as WizardData | undefined) ?? {});
  const [finishing, setFinishing] = useState(false);

  const persist = (next: WizardData, nextStep: number) => {
    setData(next);
    setStep(nextStep);
    saveDraft({ step: nextStep, data: next as Record<string, unknown> });
  };
  const back = () => persist(data, Math.max(0, step - 1));
  const saveLater = () => {
    saveDraft({ step, data: data as Record<string, unknown> });
    toast.success('Progress saved on this device. You can finish anytime.');
  };
  const logout = () =>
    Alert.alert('Log out?', 'Your onboarding progress stays saved on this device.', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Log out',
        style: 'destructive',
        onPress: () => {
          saveDraft({ step, data: data as Record<string, unknown> });
          void authService.logout();
          signOut();
        },
      },
    ]);

  const finish = async () => {
    if (!data.personal || !data.education || !data.targets || !data.language) {
      toast.error('Please complete every step before finishing.');
      return;
    }
    setFinishing(true);
    try {
      const profilePatch: Partial<UserProfile> = {
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
      await profileService.updateMe({ profile: profilePatch as UserProfile });
      updateProfile(profilePatch);
      saveDraft(null);
      toast.success('Profile complete — your free mini mock is ready!');
      // Flipping onboardingComplete releases the app route guard and redirects home.
      updateUser({
        name: data.personal.name.trim(),
        dob: data.personal.dob,
        state: data.personal.state,
        email: data.personal.email || user?.email,
        preferredLanguage: data.language.preferredLanguage as LanguageCode,
        onboardingComplete: true,
      });
    } catch (e) {
      toast.error(errorMessage(e));
      setFinishing(false);
    }
  };

  return (
    <WizardContext value={{ steps: STEPS, step, back, saveLater, logout }}>
      {step === 0 && (
        <PersonalStep
          key="s0"
          defaults={data.personal ?? { name: user?.name ?? '', dob: user?.dob ?? '', state: user?.state ?? '', email: user?.email ?? '' }}
          onNext={(v) => persist({ ...data, personal: v }, 1)}
        />
      )}
      {step === 1 && <EducationStep key="s1" defaults={data.education} onNext={(v) => persist({ ...data, education: v }, 2)} />}
      {step === 2 && <TargetsStep key="s2" defaults={data.targets} onNext={(v) => persist({ ...data, targets: v }, 3)} />}
      {step === 3 && <LanguageStep key="s3" defaults={data.language} onNext={(v) => persist({ ...data, language: v }, 4)} />}
      {step === 4 && (
        <ResumeStep
          key="s4"
          value={data.resume ?? null}
          onChange={(r) => persist({ ...data, resume: r }, 4)}
          onNext={() => persist(data, 5)}
        />
      )}
      {step === 5 && <ReviewStep key="s5" data={data} onEdit={(s) => persist(data, s)} onFinish={finish} loading={finishing} />}
    </WizardContext>
  );
}
