import { useState, type ComponentProps } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import { Stack, router, useLocalSearchParams } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { ExperienceLevel, InterviewMode, LanguageCode, ResumeInfo } from '@prepmitra/shared';
import { DISCLAIMERS, EXPERIENCE_LEVELS, LANGUAGES, RESUME_RULES, interviewSetupSchema, pluralize } from '@prepmitra/shared';
import {
  AppText, Badge, Button, Card, CardHeader, ErrorState, IconTile, Input, LanguageSelector, LoadingSkeleton, Notice, Screen, toast,
} from '@/components';
import { CheckoutSheet } from '@/features/subscription/CheckoutSheet';
import { useAsync } from '@/hooks/useAsync';
import { useResumePicker } from '@/hooks/useResumePicker';
import { errorMessage, interviewService } from '@/services';
import { roleCreditCost, useAuthStore, useInterviewStore, useProfileStore, useSubscriptionStore } from '@/store';
import { colors, radii, spacing } from '@/theme';
import { ICONS } from '@/utils/icons';

const JD_MAX = 4000;
const voiceOk = (code: LanguageCode) => !!LANGUAGES.find((l) => l.code === code)?.voiceSupported;

export default function InterviewSetup() {
  const { roleId = '' } = useLocalSearchParams<{ roleId: string }>();
  const { data: role, loading, error, reload } = useAsync(() => interviewService.getRole(roleId), roleId);
  const user = useAuthStore((s) => s.session?.user);
  const profileResume = useProfileStore((s) => s.profile.resume);
  const sub = useSubscriptionStore((s) => s.sub);
  const consume = useSubscriptionStore((s) => s.consume);
  const saveSession = useInterviewStore((s) => s.saveSession);
  const [level, setLevel] = useState<ExperienceLevel | null>(null);
  const [language, setLanguage] = useState<LanguageCode | null>(null);
  const [mode, setMode] = useState<InterviewMode>('text');
  const [jd, setJd] = useState('');
  const [jdError, setJdError] = useState<string | null>(null);
  const [resume, setResume] = useState<ResumeInfo | null>(profileResume ?? null);
  const [starting, setStarting] = useState(false);
  const [buyOpen, setBuyOpen] = useState(false);
  const picker = useResumePicker((r) => {
    setResume(r);
    toast.success('Resume attached for this interview');
  });

  if (loading) return <Screen><LoadingSkeleton /></Screen>;
  if (error || !role) return <Screen><ErrorState title="Interview role not found" description={error ?? 'This role is not available.'} onRetry={reload} /></Screen>;

  const cost = roleCreditCost(role);
  const lvl = level ?? role.levels[0] ?? 'fresher';
  const preferred = user?.preferredLanguage ?? 'en';
  const allowed = role.languages.filter((c) => mode === 'text' || voiceOk(c));
  const lang: LanguageCode = language && allowed.includes(language) ? language : allowed.includes(preferred) ? preferred : 'en';

  const chooseMode = (m: InterviewMode) => {
    setMode(m);
    if (m === 'voice' && language && !voiceOk(language)) {
      setLanguage('en');
      toast.info('Voice mode is not yet available in that language — switched to English.');
    }
  };

  const start = async () => {
    const parsed = interviewSetupSchema.safeParse({ roleId: role.id, level: lvl, language: lang, mode, jobDescription: jd.trim() || undefined });
    if (!parsed.success) {
      setJdError(parsed.error.issues[0]?.message ?? 'Check your settings');
      return;
    }
    if (sub.credits < cost) {
      setBuyOpen(true);
      return;
    }
    setStarting(true);
    try {
      const session = await interviewService.start({
        roleId: role.id,
        level: lvl,
        language: lang,
        mode,
        resumeFileName: resume?.fileName,
        jobDescription: jd.trim() || undefined,
      });
      if (!consume(cost, 'interview', `${role.shortTitle} mock interview`)) {
        setStarting(false);
        setBuyOpen(true);
        return;
      }
      saveSession(session);
      toast.success(`${pluralize(cost, 'credit')} used. Good luck!`);
      router.replace(`/interview/session/${session.id}`);
    } catch (e) {
      toast.error(errorMessage(e));
      setStarting(false);
    }
  };

  return (
    <Screen
      keyboard
      footer={
        <View style={styles.footer}>
          <View style={styles.flex}>
            <AppText variant="bodyStrong">{pluralize(cost, 'credit')}</AppText>
            <AppText variant="caption">You have {pluralize(sub.credits, 'credit')}</AppText>
          </View>
          <Button title={sub.credits >= cost ? 'Start interview' : 'Get credits'} leftIcon={sub.credits >= cost ? (mode === 'voice' ? 'mic' : 'chatbubbles') : 'wallet-outline'} loading={starting} onPress={start} />
        </View>
      }
    >
      <Stack.Screen options={{ title: role.shortTitle }} />
      <View style={styles.head}>
        <IconTile name={ICONS[role.icon]} tone="secondary" size={52} />
        <View style={styles.flex}>
          <AppText variant="caption">{role.category}</AppText>
          <AppText variant="h2" accessibilityRole="header">{role.title}</AppText>
        </View>
      </View>
      <View style={styles.badges}>
        <Badge label={`${role.durationMin} min`} icon="time-outline" />
        <Badge label={`${role.questionCount}+ questions`} />
        <Badge label={pluralize(cost, 'credit')} tone="primary" />
      </View>
      <AppText variant="body" color={colors.textSecondary}>{role.description}</AppText>
      <Card>
        <CardHeader title="What we evaluate" />
        {role.evaluates.map((e) => (
          <View key={e} style={styles.bullet}>
            <Ionicons name="checkmark-circle" size={16} color={colors.success} />
            <AppText variant="small" color={colors.text}>{e}</AppText>
          </View>
        ))}
      </Card>

      <Card style={styles.gap}>
        <CardHeader title="Configure your interview" subtitle="These settings shape the questions and the feedback." />
        <AppText variant="label">Experience level</AppText>
        <View style={styles.options} accessibilityRole="radiogroup">
          {EXPERIENCE_LEVELS.filter((l) => role.levels.includes(l.value)).map((l) => (
            <OptionCard key={l.value} title={l.label} selected={lvl === l.value} onPress={() => setLevel(l.value)} />
          ))}
        </View>
        <AppText variant="label">Interview mode</AppText>
        <View style={styles.options} accessibilityRole="radiogroup">
          <OptionCard title="Text" description="Type your answers in a chat" icon="chatbubbles-outline" selected={mode === 'text'} onPress={() => chooseMode('text')} />
          <OptionCard
            title="Voice"
            description={role.voiceAvailable ? 'Simulated speaking practice' : 'Not available for this role'}
            icon="mic-outline"
            selected={mode === 'voice'}
            disabled={!role.voiceAvailable}
            onPress={() => chooseMode('voice')}
          />
        </View>
        <LanguageSelector label="Interview language" value={lang} onChange={setLanguage} allowed={allowed} hint={mode === 'voice' ? 'Voice mode supports 12 Tier-1 languages.' : undefined} />
      </Card>

      <Card style={styles.gap}>
        <CardHeader title="Resume (optional)" subtitle="Makes resume questions specific to your experience." />
        {resume ? (
          <View style={styles.file}>
            <IconTile name="document-text" size={40} />
            <View style={styles.flex}>
              <AppText variant="smallStrong" numberOfLines={1}>{resume.fileName}</AppText>
              <AppText variant="caption">{resume.sizeKb} KB{resume === profileResume ? ' · from your profile' : ''}</AppText>
            </View>
            <Button title="Remove" variant="ghost" size="sm" onPress={() => setResume(null)} accessibilityLabel={`Remove ${resume.fileName}`} />
          </View>
        ) : (
          <Button title="Attach resume" variant="outline" leftIcon="attach" loading={picker.uploading} onPress={() => void picker.pick()} />
        )}
        <AppText variant="caption">PDF or DOCX, up to {RESUME_RULES.maxSizeMb} MB.</AppText>
        {picker.error ? <AppText variant="small" color={colors.error} accessibilityRole="alert">{picker.error}</AppText> : null}
      </Card>

      <Input
        label="Job description (optional)"
        multiline
        value={jd}
        onChangeText={(t) => {
          setJd(t);
          setJdError(null);
        }}
        maxLength={JD_MAX}
        showCount
        placeholder="Paste the job description to tailor the questions"
        error={jdError ?? undefined}
      />
      <Notice tone="warning" title="Scripted demo">{DISCLAIMERS.demoInterview}</Notice>

      <CheckoutSheet visible={buyOpen} onClose={() => setBuyOpen(false)} reason={`This interview needs ${pluralize(cost, 'credit')} and you have ${sub.credits}.`} />
    </Screen>
  );
}

function OptionCard({
  title, description, icon, selected, onPress, disabled,
}: { title: string; description?: string; icon?: ComponentProps<typeof Ionicons>['name']; selected: boolean; onPress: () => void; disabled?: boolean }) {
  return (
    <Pressable
      onPress={disabled ? undefined : onPress}
      accessibilityRole="radio"
      accessibilityState={{ checked: selected, disabled: !!disabled }}
      accessibilityLabel={description ? `${title}. ${description}` : title}
      style={[styles.option, selected && styles.optionOn, disabled && styles.optionOff]}
    >
      {icon && <Ionicons name={icon} size={20} color={selected ? colors.primary : colors.textSecondary} />}
      <View style={styles.flex}>
        <AppText variant="bodyStrong" color={selected ? colors.primary : colors.text}>{title}</AppText>
        {description ? <AppText variant="caption">{description}</AppText> : null}
      </View>
      <Ionicons name={selected ? 'radio-button-on' : 'radio-button-off'} size={20} color={selected ? colors.primary : colors.borderStrong} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  head: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  badges: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  bullet: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, paddingVertical: 3 },
  gap: { gap: spacing.md },
  options: { gap: spacing.sm },
  option: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    minHeight: 56,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: radii.md,
    borderWidth: 1.5,
    borderColor: colors.border,
    backgroundColor: colors.white,
  },
  optionOn: { borderColor: colors.primary, backgroundColor: colors.primarySoft },
  optionOff: { opacity: 0.5 },
  file: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  footer: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
});
