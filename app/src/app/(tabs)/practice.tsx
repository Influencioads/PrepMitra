import { useMemo } from 'react';
import { StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import { INTERVIEW_ROLES, formatClock, getExamById, getRoleById, interviewProgress, relativeTime, remainingSeconds } from '@prepmitra/shared';
import {
  AppText, Badge, Button, Card, Divider, ExamCard, IconTile, InterviewCard, ListRow, Screen, SectionHeader, TabHeader,
} from '@/components';
import { RecommendationList } from '@/features/home/RecommendationList';
import { buildRecommendations, recommendedExams } from '@/features/home/recommendations';
import { useNow } from '@/hooks/useNow';
import { useProgress } from '@/hooks/useProgress';
import { selectActiveInterviews, selectInProgress, useExamStore, useInterviewStore, useProfileStore, useSubscriptionStore } from '@/store';
import { colors, spacing } from '@/theme';

/** Quick-start hub: free mini mock, unfinished work, interviews and recommendations. */
export default function Practice() {
  const sub = useSubscriptionStore((s) => s.sub);
  const profile = useProfileStore((s) => s.profile);
  const attempts = useExamStore((s) => s.attempts);
  const sessions = useInterviewStore((s) => s.sessions);
  const p = useProgress();
  const now = useNow(15_000);
  const inProgress = selectInProgress(attempts);
  const activeInterviews = selectActiveInterviews(sessions);
  const recs = useMemo(() => buildRecommendations(p, sub, profile), [p, sub, profile]);
  const exams = useMemo(() => recommendedExams(profile, 3), [profile]);
  const roles = useMemo(() => {
    const targets = profile.targetRoleIds.map((id) => getRoleById(id)).filter((r): r is NonNullable<typeof r> => !!r && r.status === 'published');
    const rest = INTERVIEW_ROLES.filter((r) => r.status === 'published' && !targets.includes(r)).sort((a, b) => b.popularity - a.popularity);
    return [...targets, ...rest].slice(0, 2);
  }, [profile.targetRoleIds]);
  const mini = getExamById('general-aptitude');

  return (
    <Screen edges={['top', 'left', 'right']}>
      <TabHeader title="Practice" subtitle="Pick up where you left off or start something new." />

      <Card tone="primary" style={styles.hero}>
        <View style={styles.heroTop}>
          <IconTile name="flash" tone="primary" size={44} />
          <View style={styles.flex}>
            <AppText variant="h3">{sub.freeMiniMockUsed ? '30-minute aptitude mock' : 'Free mini mock'}</AppText>
            <AppText variant="small">
              {mini?.sections.length ?? 3} sections · {mini?.demo.durationMin ?? 30} min · full report with a 7-day plan
            </AppText>
          </View>
        </View>
        <View style={styles.badges}>
          <Badge label={sub.freeMiniMockUsed ? '1 credit' : 'Free trial'} tone={sub.freeMiniMockUsed ? 'primary' : 'success'} icon="wallet-outline" />
          <Badge label={`${sub.credits} credits left`} icon="layers-outline" />
        </View>
        <Button
          title={sub.freeMiniMockUsed ? 'Start aptitude mock' : 'Start free mini mock'}
          leftIcon="play"
          onPress={() => router.push('/exams/general-aptitude/instructions')}
        />
      </Card>

      {(inProgress.length > 0 || activeInterviews.length > 0) && (
        <>
          <SectionHeader title="Continue" />
          <Card style={styles.list}>
            {inProgress.map((a, i) => {
              const left = remainingSeconds(a, now);
              return (
                <View key={a.id}>
                  {i > 0 && <Divider />}
                  <ListRow
                    icon="document-text-outline"
                    title={getExamById(a.examId)?.shortTitle ?? 'Mock exam'}
                    subtitle={`Started ${relativeTime(a.startedAt, now)} · ${left > 0 ? `${formatClock(left)} left` : 'time is up — submit now'}`}
                    onPress={() => router.push(`/exam/${a.id}`)}
                    accessibilityHint="Resumes the exam with the remaining time"
                  />
                </View>
              );
            })}
            {activeInterviews.map((s, i) => {
              const prog = interviewProgress(s);
              return (
                <View key={s.id}>
                  {(i > 0 || inProgress.length > 0) && <Divider />}
                  <ListRow
                    icon={s.config.mode === 'voice' ? 'mic-outline' : 'chatbubbles-outline'}
                    iconTone="secondary"
                    title={`${getRoleById(s.config.roleId)?.shortTitle ?? 'Interview'} interview`}
                    subtitle={`Question ${prog.asked} of ${prog.total} · started ${relativeTime(s.startedAt, now)}`}
                    onPress={() => router.push(`/interview/session/${s.id}`)}
                  />
                </View>
              );
            })}
          </Card>
        </>
      )}

      <SectionHeader title="Mock interviews" actionLabel="All roles" onAction={() => router.push('/interviews')} />
      {roles.map((r) => (
        <InterviewCard key={r.id} role={r} compact onPress={() => router.push(`/interviews/${r.id}`)} />
      ))}

      <SectionHeader title="Recommended next steps" />
      <RecommendationList items={recs} />

      <SectionHeader title="Exams for your targets" actionLabel="Explore all" onAction={() => router.push('/explore')} />
      {exams.map((e) => (
        <ExamCard key={e.id} exam={e} freeTrialAvailable={!sub.freeMiniMockUsed} onPress={() => router.push(`/exams/${e.id}`)} />
      ))}

      <Card style={styles.credits} onPress={() => router.push('/subscription')} accessibilityLabel={`${sub.credits} credits. Manage credits and plans.`}>
        <IconTile name="wallet-outline" tone="secondary" />
        <View style={styles.flex}>
          <AppText variant="bodyStrong">{sub.credits} credits available</AppText>
          <AppText variant="small">1 credit = 1 full mock or 1 interview. Buy more or change plan.</AppText>
        </View>
        <AppText variant="smallStrong" color={colors.primary}>Manage</AppText>
      </Card>
    </Screen>
  );
}

const styles = StyleSheet.create({
  hero: { gap: spacing.md },
  heroTop: { flexDirection: 'row', gap: spacing.md, alignItems: 'center' },
  badges: { flexDirection: 'row', gap: 6, flexWrap: 'wrap' },
  flex: { flex: 1 },
  list: { paddingVertical: 4 },
  credits: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
});
