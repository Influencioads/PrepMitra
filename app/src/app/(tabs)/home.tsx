import { useMemo } from 'react';
import { Pressable, ScrollView, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import {
  formatClock, formatDuration, formatShortDate, getExamById, getRoleById, relativeTime, remainingSeconds, formatMarks,
} from '@prepmitra/shared';
import {
  AppText, Badge, Button, Card, Divider, EmptyState, ListRow, MitraSays, NotebookBackground, Screen, SectionHeader, ScoreChart,
} from '@/components';
import { AppTopBar } from '@/components/AppTopBar';
import { PrepPath, type PathStep } from '@/features/home/PrepPath';
import { buildRecommendations, recommendationHref } from '@/features/home/recommendations';
import { useNow } from '@/hooks/useNow';
import { useProgress } from '@/hooks/useProgress';
import { selectActiveInterviews, selectInProgress, useAuthStore, useExamStore, useInterviewStore, useProfileStore, useSubscriptionStore } from '@/store';
import { accuracyTone, colors, paper, radii, spacing, toneColors, type Tone } from '@/theme';
import type { IoniconName } from '@/utils/icons';

const greeting = () => {
  const h = new Date().getHours();
  return h < 12 ? 'Good morning' : h < 17 ? 'Good afternoon' : 'Good evening';
};

/** Steps of the prep path shown on Home; the full plan lives in the report. */
const HOME_PATH_STEPS = 3;

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
  const plan = latest?.improvementPlan ?? [];
  const steps: PathStep[] = plan.length > 0
    ? plan.slice(0, HOME_PATH_STEPS).map((d, i, arr) => ({
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

  const quick: { icon: IoniconName; label: string; tone: Tone; href: string }[] = [
    { icon: 'flash', label: sub.freeMiniMockUsed ? 'Aptitude' : 'Free mock', tone: 'primary', href: '/exams/general-aptitude' },
    { icon: 'cash', label: 'Banking', tone: 'secondary', href: '/explore?category=banking' },
    { icon: 'chatbubbles', label: 'Interview', tone: 'info', href: '/interviews' },
    { icon: 'sparkles', label: 'AI tutor', tone: 'warning', href: '/ai' },
  ];

  const stats = [
    { label: 'Mocks', value: String(p.history.length) },
    { label: 'Avg score', value: `${p.avg}%`, delta: hasHistory ? p.delta : undefined },
    { label: 'Streak', value: `${p.streakDays}d` },
  ];

  return (
    <Screen edges={['top', 'left', 'right']}>
      <AppTopBar name={user?.name ?? 'there'} greeting={greeting()} credits={sub.credits} />

      {/* Continue where you left off — the most important thing on screen when it exists. */}
      {inProgress && (
        <Pressable
          onPress={() => router.push(`/exam/${inProgress.id}`)}
          accessibilityRole="button"
          accessibilityLabel="Resume your unfinished mock"
          style={({ pressed }) => [styles.resume, pressed && styles.pressed]}
        >
          <View style={styles.resumeIcon}><Ionicons name="play" size={18} color={colors.white} /></View>
          <View style={styles.flex}>
            <AppText variant="bodyStrong" color={colors.white}>Resume {getExamById(inProgress.examId)?.shortTitle}</AppText>
            <AppText variant="caption" color="rgba(255,255,255,0.85)">
              Started {relativeTime(inProgress.startedAt, now)} ·{' '}
              {remainingSeconds(inProgress, now) > 0 ? `${formatClock(remainingSeconds(inProgress, now))} left` : 'time is up — submit now'}
            </AppText>
          </View>
          <Ionicons name="chevron-forward" size={20} color={colors.white} />
        </Pressable>
      )}
      {activeInterview && (
        <Card tone="primary" onPress={() => router.push(`/interview/session/${activeInterview.id}`)} style={styles.inlineRow} accessibilityLabel="Continue your interview">
          <Ionicons name="chatbubbles" size={20} color={colors.primary} />
          <View style={styles.flex}>
            <AppText variant="bodyStrong" color={colors.primary}>Interview in progress</AppText>
            <AppText variant="caption">{getRoleById(activeInterview.config.roleId)?.shortTitle} · {activeInterview.config.mode === 'voice' ? 'Voice' : 'Text'}</AppText>
          </View>
          <Ionicons name="chevron-forward" size={18} color={colors.primary} />
        </Card>
      )}

      {/* Stat strip */}
      <View style={styles.statStrip} accessibilityRole="summary">
        {stats.map((s, i) => (
          <View key={s.label} style={[styles.stat, i > 0 && styles.statDivider]} accessibilityLabel={`${s.label}: ${s.value}`}>
            <View style={styles.statValueRow}>
              <AppText variant="h2">{s.value}</AppText>
              {s.delta !== undefined && s.delta !== 0 && (
                <Ionicons name={s.delta > 0 ? 'arrow-up' : 'arrow-down'} size={13} color={s.delta > 0 ? colors.success : colors.error} />
              )}
            </View>
            <AppText variant="caption">{s.label}</AppText>
          </View>
        ))}
      </View>

      {/* Quick actions */}
      <View style={styles.quickRow} accessibilityLabel="Quick actions">
        {quick.map((q) => (
          <Pressable
            key={q.label}
            onPress={() => router.push(q.href)}
            accessibilityRole="button"
            accessibilityLabel={q.label}
            style={({ pressed }) => [styles.quick, pressed && styles.pressed]}
          >
            <View style={[styles.quickIcon, { backgroundColor: toneColors[q.tone].bg }]}>
              <Ionicons name={q.icon} size={24} color={toneColors[q.tone].fg} />
            </View>
            <AppText variant="caption" weight="600" color={colors.text} numberOfLines={1}>{q.label}</AppText>
          </Pressable>
        ))}
      </View>

      <MitraSays>{coachLine}</MitraSays>

      {/* Today's step on the prep path */}
      <View style={styles.pathCard} accessibilityLabel="Your prep path">
        <NotebookBackground margin={26} spacing={32} lines={12} />
        <View style={styles.pathHead}>
          <AppText variant="h3">Your prep path</AppText>
          <View style={styles.streak} accessibilityLabel={`${p.streakDays} day streak`}>
            <Ionicons name="flame" size={14} color={colors.warning} />
            <AppText variant="smallStrong" color={colors.white}>{p.streakDays}</AppText>
          </View>
        </View>
        <PrepPath steps={steps} onStart={startStep} />
        {latest && plan.length > HOME_PATH_STEPS && (
          <Pressable onPress={startStep} accessibilityRole="button" style={styles.pathMore}>
            <AppText variant="smallStrong" color={colors.primary}>See all {plan.length} days</AppText>
            <Ionicons name="chevron-forward" size={14} color={colors.primary} />
          </Pressable>
        )}
      </View>

      {/* Recommendations as a swipeable carousel */}
      {recommendations.length > 0 && (
        <View style={styles.section}>
          <SectionHeader title="For you" />
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            snapToInterval={CARD_W + spacing.md}
            decelerationRate="fast"
            contentContainerStyle={styles.carousel}
            style={styles.bleed}
          >
            {recommendations.map((r) => {
              const tone: Tone = r.roleId ? 'secondary' : 'primary';
              return (
                <Pressable
                  key={r.id}
                  onPress={() => router.push(recommendationHref(r))}
                  accessibilityRole="button"
                  accessibilityLabel={`${r.title}. ${r.reason}`}
                  style={({ pressed }) => [styles.recCard, pressed && styles.pressed]}
                >
                  <View style={[styles.recIcon, { backgroundColor: toneColors[tone].bg }]}>
                    <Ionicons name={r.roleId ? 'chatbubbles-outline' : 'locate-outline'} size={20} color={toneColors[tone].fg} />
                  </View>
                  <AppText variant="bodyStrong" numberOfLines={2}>{r.title}</AppText>
                  <AppText variant="caption" numberOfLines={3} style={styles.flex}>{r.reason}</AppText>
                  <View style={styles.recFoot}>
                    <Badge label={`${r.minutes} min`} icon="time-outline" />
                    <View style={styles.recGo}><Ionicons name="arrow-forward" size={16} color={colors.white} /></View>
                  </View>
                </Pressable>
              );
            })}
          </ScrollView>
        </View>
      )}

      <View style={styles.section}>
        <SectionHeader title="Score trend" actionLabel={hasHistory ? 'Details' : undefined} onAction={() => router.push('/progress')} />
        <Card>
          {trend.length > 0 ? (
            <ScoreChart data={trend} />
          ) : (
            <EmptyState compact icon="trending-up-outline" title="No scores yet" description="Your score trend appears after your first mock." />
          )}
        </Card>
      </View>

      {p.weak.length > 0 && (
        <View style={styles.section}>
          <SectionHeader title="Focus topics" actionLabel="Progress" onAction={() => router.push('/progress')} />
          <View style={styles.chips}>
            {p.weak.slice(0, 6).map((t) => {
              const tone = toneColors[accuracyTone(t.mastery)];
              return (
                <View key={t.topic} style={[styles.chip, { backgroundColor: tone.bg, borderColor: tone.border }]}>
                  <AppText variant="smallStrong" color={tone.fg}>{t.topic}</AppText>
                  <AppText variant="caption" color={tone.fg}>{t.mastery}%</AppText>
                </View>
              );
            })}
          </View>
        </View>
      )}

      <View style={styles.section}>
        <SectionHeader title="Recent attempts" actionLabel={hasHistory ? 'See all' : undefined} onAction={() => router.push('/reports')} />
        {hasHistory ? (
          <Card style={styles.list}>
            {p.history.slice(0, 3).map((h, i) => (
              <View key={h.reportId}>
                {i > 0 && <Divider />}
                <ListRow
                  title={h.examTitle}
                  subtitle={`${formatShortDate(h.submittedAt)} · ${formatMarks(h.score)}/${formatMarks(h.maxScore)} · ${formatDuration(h.timeTakenSec)}`}
                  right={<Badge label={`${h.accuracy}%`} tone={accuracyTone(h.accuracy)} />}
                  onPress={() => router.push(`/reports/${h.reportId}`)}
                  accessibilityHint="Opens the performance report"
                />
              </View>
            ))}
          </Card>
        ) : (
          <Card>
            <EmptyState compact icon="clipboard-outline" title="No attempts yet" description="Your attempts and reports will be listed here." />
            <Button title="Take the free mini mock" onPress={() => router.push('/exams/general-aptitude')} />
          </Card>
        )}
      </View>
    </Screen>
  );
}

const CARD_W = 220;

const styles = StyleSheet.create({
  flex: { flex: 1 },
  pressed: { opacity: 0.8, transform: [{ scale: 0.98 }] },
  section: { gap: spacing.sm },
  resume: {
    flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.md,
    borderRadius: radii.xl, backgroundColor: colors.primary,
  },
  resumeIcon: { width: 40, height: 40, borderRadius: 20, backgroundColor: 'rgba(255,255,255,0.22)', alignItems: 'center', justifyContent: 'center' },
  inlineRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.md },
  statStrip: {
    flexDirection: 'row', backgroundColor: colors.card, borderRadius: radii.xl, paddingVertical: spacing.md,
    borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border,
  },
  stat: { flex: 1, alignItems: 'center', gap: 2 },
  statDivider: { borderLeftWidth: StyleSheet.hairlineWidth, borderLeftColor: colors.border },
  statValueRow: { flexDirection: 'row', alignItems: 'center', gap: 2 },
  quickRow: { flexDirection: 'row', justifyContent: 'space-between' },
  quick: { alignItems: 'center', gap: 6, width: 76 },
  quickIcon: { width: 58, height: 58, borderRadius: 20, alignItems: 'center', justifyContent: 'center' },
  pathCard: { overflow: 'hidden', borderRadius: radii.xl, borderWidth: 1.5, borderColor: paper.ink, backgroundColor: paper.paper, padding: spacing.lg, paddingLeft: spacing.lg + 6, gap: spacing.md },
  pathHead: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  pathMore: { flexDirection: 'row', alignItems: 'center', gap: 2, alignSelf: 'flex-end' },
  streak: { flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: paper.ink, borderRadius: 999, paddingHorizontal: 10, paddingVertical: 4 },
  bleed: { marginHorizontal: -spacing.lg },
  carousel: { paddingHorizontal: spacing.lg, gap: spacing.md },
  recCard: {
    width: CARD_W, minHeight: 190, padding: spacing.md, gap: spacing.sm, borderRadius: radii.xl,
    backgroundColor: colors.card, borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border,
  },
  recIcon: { width: 40, height: 40, borderRadius: 14, alignItems: 'center', justifyContent: 'center' },
  recFoot: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  recGo: { width: 30, height: 30, borderRadius: 15, backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center' },
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  chip: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 12, paddingVertical: 8, borderRadius: radii.full, borderWidth: 1 },
  list: { paddingVertical: 4 },
});
