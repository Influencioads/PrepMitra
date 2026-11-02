import { useMemo } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import {
  formatClock, formatDuration, formatShortDate, getExamById, getRoleById, relativeTime, remainingSeconds,
} from '@prepmitra/shared';
import {
  AppText, Badge, Button, Card, CardHeader, DemoBadge, Divider, EmptyState, ListRow, MitraSays, NotebookBackground, ProgressBar, Screen,
  SectionHeader, ScoreChart, StatCard, TabHeader,
} from '@/components';
import { PrepPath, type PathStep } from '@/features/home/PrepPath';
import { RecommendationList } from '@/features/home/RecommendationList';
import { buildRecommendations } from '@/features/home/recommendations';
import { useNow } from '@/hooks/useNow';
import { useProgress } from '@/hooks/useProgress';
import { selectActiveInterviews, selectInProgress, useAuthStore, useExamStore, useInterviewStore, useProfileStore, useSubscriptionStore } from '@/store';
import { accuracyTone, colors, paper, radii, spacing } from '@/theme';
import type { IoniconName } from '@/utils/icons';

const greeting = () => {
  const h = new Date().getHours();
  return h < 12 ? 'Good morning' : h < 17 ? 'Good afternoon' : 'Good evening';
};

export default function Home() {
  const user = useAuthStore((s) => s.session?.user);
  const profile = useProfileStore((s) => s.profile);
  const sub = useSubscriptionStore((s) => s.sub);
  const attempts = useExamStore((s) => s.attempts);
  const sessions = useInterviewStore((s) => s.sessions);
  const p = useProgress();
  const now = useNow(30_000);

  const inProgress = selectInProgress(attempts)[0];
  const activeInterview = selectActiveInterviews(sessions)[0];
  const recommendations = useMemo(() => buildRecommendations(p, sub, profile), [p, sub, profile]);
  const firstName = user?.name.split(' ')[0] ?? 'there';
  const hasHistory = p.history.length > 0;
  const trend = p.trend.slice(-8);

  // Prep path: the latest report's improvement plan, or a single "free mini mock" step for new users.
  const latest = p.history[0] ? p.reports.find((r) => r.id === p.history[0]!.reportId) : undefined;
  const weakest = latest?.weaknesses[0];
  const coachLine = latest
    ? weakest
      ? `${weakest.topic} cost you marks in ${latest.examTitle}. Let’s fix that today — one short session.`
      : `Strong work in ${latest.examTitle}. Keep the streak going with today’s step.`
    : 'Start with the free 30-minute mini mock. I’ll show you exactly where your marks leak.';
  const steps: PathStep[] = latest && latest.improvementPlan.length > 0
    ? latest.improvementPlan.slice(0, 6).map((d, i, arr) => ({
        key: `d${d.day}`,
        label: i === 0 ? `Today · Day ${d.day}` : `Day ${d.day}`,
        title: d.title,
        meta: `${d.minutes} min`,
        state: i === 0 ? 'today' : i === arr.length - 1 ? 'goal' : 'locked',
      }))
    : [
        { key: 'free', label: 'Today', title: 'Free 30-min mini mock', meta: 'General aptitude · free', state: 'today' },
        { key: 'report', label: 'Next', title: 'Your report in under a minute', state: 'locked' },
        { key: 'plan', label: 'Then', title: 'A 7-day plan from your mistakes', state: 'goal' },
      ];
  const startStep = () => router.push(latest ? `/reports/${latest.id}` : '/exams/general-aptitude');

  const quick: { icon: IoniconName; title: string; sub: string; href: string }[] = [
    { icon: 'bulb-outline', title: '30-min aptitude', sub: sub.freeMiniMockUsed ? '1 credit' : 'Free trial', href: '/exams/general-aptitude' },
    { icon: 'cash-outline', title: 'Banking mocks', sub: 'IBPS · SBI', href: '/explore?category=banking' },
    { icon: 'chatbubbles-outline', title: 'Mock interview', sub: 'Text or voice', href: '/interviews' },
    { icon: 'trending-up-outline', title: 'Progress', sub: 'Trends & mastery', href: '/progress' },
  ];

  return (
    <Screen edges={['top', 'left', 'right']}>
      <TabHeader
        eyebrow={<DemoBadge />}
        title={`${greeting()}, ${firstName}`}
        subtitle={hasHistory ? 'Small, regular practice wins.' : 'Start with your free mini mock to unlock insights.'}
      />

      <MitraSays>{coachLine}</MitraSays>

      <View style={styles.pathCard} accessibilityLabel="Your prep path">
        <NotebookBackground margin={26} spacing={32} lines={24} />
        <View style={styles.pathHead}>
          <AppText variant="h3">Your prep path</AppText>
          <View style={styles.streak} accessibilityLabel={`${p.streakDays} day streak`}>
            <Ionicons name="flame" size={14} color={colors.warning} />
            <AppText variant="smallStrong" color={colors.white}>{p.streakDays}</AppText>
          </View>
        </View>
        <PrepPath steps={steps} onStart={startStep} />
      </View>

      {inProgress && (
        <Card tone="primary" style={styles.banner}>
          <View style={styles.bannerText}>
            <AppText variant="bodyStrong" color={colors.primary}>You have an unfinished mock</AppText>
            <AppText variant="small">
              {getExamById(inProgress.examId)?.shortTitle} · started {relativeTime(inProgress.startedAt, now)} ·{' '}
              {remainingSeconds(inProgress, now) > 0 ? `${formatClock(remainingSeconds(inProgress, now))} left` : 'time is up — submit now'}
            </AppText>
          </View>
          <Button title="Resume exam" rightIcon="arrow-forward" onPress={() => router.push(`/exam/${inProgress.id}`)} />
        </Card>
      )}
      {activeInterview && (
        <Card tone="primary" style={styles.banner}>
          <View style={styles.bannerText}>
            <AppText variant="bodyStrong" color={colors.primary}>Interview in progress</AppText>
            <AppText variant="small">{getRoleById(activeInterview.config.roleId)?.shortTitle} · {activeInterview.config.mode === 'voice' ? 'Voice' : 'Text'} · started {relativeTime(activeInterview.startedAt, now)}</AppText>
          </View>
          <Button title="Continue interview" variant="soft" rightIcon="arrow-forward" onPress={() => router.push(`/interview/session/${activeInterview.id}`)} />
        </Card>
      )}

      <View style={styles.grid}>
        <StatCard label="Mock tests taken" value={p.history.length} icon="clipboard-outline" hint={hasHistory ? `Last: ${formatShortDate(p.history[0]!.submittedAt)}` : 'No attempts yet'} />
        <StatCard label="Average score" value={`${p.avg}%`} icon="locate-outline" tone="success" trend={hasHistory ? p.delta : undefined} hint={hasHistory ? 'vs previous mock' : 'Take a mock to see this'} />
      </View>
      <View style={styles.grid}>
        <StatCard label="Practice streak" value={`${p.streakDays} ${p.streakDays === 1 ? 'day' : 'days'}`} icon="flame-outline" tone="warning" hint={`${p.totalMinutes} min this week`} />
        <StatCard
          label="Credits"
          value={sub.credits}
          icon="wallet-outline"
          tone="secondary"
          hint={sub.freeMiniMockUsed ? 'Tap to manage' : 'Free mini mock available'}
          onPress={() => router.push('/subscription')}
        />
      </View>

      <View style={styles.quickGrid} accessibilityLabel="Quick practice">
        {quick.map((q) => (
          <Pressable
            key={q.title}
            onPress={() => router.push(q.href)}
            accessibilityRole="button"
            accessibilityLabel={`${q.title}, ${q.sub}`}
            style={({ pressed }) => [styles.quick, pressed && styles.pressed]}
          >
            <View style={styles.quickIcon}>
              <Ionicons name={q.icon} size={20} color={colors.secondary} />
            </View>
            <AppText variant="smallStrong" numberOfLines={1}>{q.title}</AppText>
            <AppText variant="caption" numberOfLines={1}>{q.sub}</AppText>
          </Pressable>
        ))}
      </View>

      <Card>
        <CardHeader
          title="Score trend"
          subtitle="Score and accuracy across your recent mocks"
          action={hasHistory ? <Button title="Details" variant="ghost" size="sm" onPress={() => router.push('/progress')} /> : undefined}
        />
        {trend.length > 0 ? (
          <ScoreChart data={trend} />
        ) : (
          <EmptyState compact icon="trending-up-outline" title="No scores yet" description="Your score trend appears after your first mock." />
        )}
      </Card>

      <SectionHeader title="Recommended for you" subtitle="Personalised next steps" />
      <RecommendationList items={recommendations} />

      <Card>
        <CardHeader title="Topic-wise accuracy" subtitle="Across all your attempts" />
        {p.topics.length > 0 ? (
          <View style={styles.bars}>
            {p.topics.slice(0, 6).map((t) => (
              <ProgressBar key={t.topic} label={t.topic} value={t.mastery} showValue tone={accuracyTone(t.mastery)} size="sm" />
            ))}
          </View>
        ) : (
          <EmptyState compact icon="podium-outline" title="No topic data yet" description="Topic accuracy builds up as you practise." />
        )}
      </Card>

      <Card>
        <CardHeader title="Strengths and weaknesses" />
        <AppText variant="smallStrong" color={colors.success} style={styles.swTitle}>Strengths</AppText>
        <View style={styles.bars}>
          {p.strong.slice(0, 3).map((t) => (
            <ProgressBar key={t.topic} label={t.topic} value={t.mastery} showValue tone="success" size="sm" />
          ))}
          {p.strong.length === 0 && <AppText variant="small">Topics with 75%+ mastery appear here.</AppText>}
        </View>
        <AppText variant="smallStrong" color={colors.error} style={styles.swTitle}>Needs work</AppText>
        <View style={styles.bars}>
          {p.weak.slice(0, 3).map((t) => (
            <ProgressBar key={t.topic} label={t.topic} value={t.mastery} showValue tone={accuracyTone(t.mastery)} size="sm" />
          ))}
          {p.weak.length === 0 && <AppText variant="small">Topics below 60% appear here.</AppText>}
        </View>
      </Card>

      <SectionHeader title="Recent attempts" actionLabel={hasHistory ? 'View all' : undefined} onAction={() => router.push('/reports')} />
      {hasHistory ? (
        <Card style={styles.list}>
          {p.history.slice(0, 5).map((h, i) => (
            <View key={h.reportId}>
              {i > 0 && <Divider />}
              <ListRow
                title={h.examTitle}
                subtitle={`${formatShortDate(h.submittedAt)} · ${h.score}/${h.maxScore} · ${formatDuration(h.timeTakenSec)}`}
                right={<Badge label={`${h.accuracy}%`} tone={accuracyTone(h.accuracy)} />}
                onPress={() => router.push(`/reports/${h.reportId}`)}
                accessibilityHint="Opens the performance report"
              />
            </View>
          ))}
        </Card>
      ) : (
        <Card>
          <EmptyState
            compact
            icon="clipboard-outline"
            title="No attempts yet"
            description="Your attempts and reports will be listed here."
            actionLabel="Take the free mini mock"
            onAction={() => router.push('/exams/general-aptitude')}
          />
        </Card>
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  banner: { gap: spacing.md },
  pathCard: { overflow: 'hidden', borderRadius: radii.xl, borderWidth: 1.5, borderColor: paper.ink, backgroundColor: paper.paper, padding: spacing.lg, paddingLeft: spacing.lg + 6, gap: spacing.md },
  pathHead: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  streak: { flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: paper.ink, borderRadius: 999, paddingHorizontal: 10, paddingVertical: 4 },
  bannerText: { gap: 2 },
  grid: { flexDirection: 'row', gap: spacing.md },
  quickGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md },
  quick: {
    flexGrow: 1,
    flexBasis: '45%',
    minHeight: 92,
    padding: spacing.md,
    gap: 4,
    borderRadius: radii.lg,
    backgroundColor: colors.card,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: colors.border,
  },
  pressed: { opacity: 0.8 },
  quickIcon: { width: 36, height: 36, borderRadius: radii.md, backgroundColor: colors.secondarySoft, alignItems: 'center', justifyContent: 'center', marginBottom: 4 },
  bars: { gap: spacing.md },
  swTitle: { marginTop: spacing.sm, marginBottom: spacing.sm },
  list: { paddingVertical: 4 },
});
