import { StyleSheet, View } from 'react-native';
import { router, type Href } from 'expo-router';
import { formatDate } from '@prepmitra/shared';
import { AppText, Badge, Card, IconTile, Screen, TabHeader } from '@/components';
import { AllowanceBadge, useAllowances } from '@/features/ai/AiUi';
import { colors, spacing } from '@/theme';
import type { IoniconName } from '@/utils/icons';

interface Tool {
  href: Href;
  title: string;
  desc: string;
  icon: IoniconName;
  feature?: string;
  flag?: string;
  plan?: string;
}

const TOOLS: Tool[] = [
  { href: '/ai/doubts', title: 'Doubt Solver', desc: 'Type or photograph a question. Verified steps, shortcut and the trap.', icon: 'help-buoy-outline', feature: 'doubts' },
  { href: '/ai/tutor', title: 'Ask Mitra', desc: 'Your AI tutor who knows your mocks. Story mode too.', icon: 'chatbubbles-outline', feature: 'tutor_chat_turns' },
  { href: { pathname: '/ai/tutor', params: { tab: 'deep' } }, title: 'Deep dives', desc: 'Visual note, concept from zero, the trap and practice.', icon: 'school-outline', feature: 'smart_credits' },
  { href: '/ai/persona', title: 'Persona & rank', desc: 'Topic mastery, error mix, strategy and rank predictor.', icon: 'speedometer-outline', flag: 'rank_predictor', plan: 'Pro' },
  { href: '/ai/notes', title: 'Notes & decks', desc: 'Notes, formula sheets, mind maps and topic decks.', icon: 'document-text-outline', feature: 'personal_notes' },
  { href: '/ai/practice', title: 'Revision AI', desc: 'Today’s spaced quiz from your mistakes, with hints.', icon: 'repeat-outline', flag: 'revision_ai', plan: 'Starter' },
  { href: { pathname: '/ai/practice', params: { tab: 'current' } }, title: 'Current affairs', desc: 'Daily fact-checked digest and GA quiz.', icon: 'newspaper-outline', flag: 'current_affairs', plan: 'Pro' },
  { href: { pathname: '/ai/practice', params: { tab: 'writing' } }, title: 'Writing evaluator', desc: 'Essays and letters scored with a model answer.', icon: 'create-outline', feature: 'descriptive_evals' },
  { href: '/ai/coach', title: 'Cheat Code Coach', desc: 'Discover, test and lock your own shortcuts.', icon: 'flash-outline', feature: 'cheat_code_sessions' },
];

const flagOn = (v: unknown) => v !== undefined && v !== false && v !== 'none';

/** AI study tools hub (tab). Each tool shows what is left on the plan this month. */
export default function AiTools() {
  const allow = useAllowances();
  return (
    <Screen edges={['top', 'left', 'right']}>
      <TabHeader title="AI study tools" subtitle="Everything Mitra can do for you." />
      {allow?.resetsAt ? (
        <AppText variant="caption" style={styles.reset} onPress={() => router.push('/subscription')}>
          Allowances reset on {formatDate(allow.resetsAt)} · <AppText variant="caption" color={colors.primary}>Plans and top-ups</AppText>
        </AppText>
      ) : null}
      <View style={{ gap: spacing.sm }}>
        {TOOLS.map((t) => (
          <Card key={t.title} onPress={() => router.push(t.href)} accessibilityLabel={`${t.title}. ${t.desc}`}>
            <View style={styles.row}>
              <IconTile name={t.icon} tone="primary" />
              <View style={styles.flex}>
                <AppText variant="bodyStrong">{t.title}</AppText>
                <AppText variant="small">{t.desc}</AppText>
                <View style={styles.badge}>
                  {t.feature ? <AllowanceBadge feature={t.feature} /> : null}
                  {t.flag && allow ? (flagOn(allow.flags[t.flag]) ? <Badge label="Included" tone="success" /> : <Badge label={`${t.plan} plan feature`} icon="lock-closed-outline" />) : null}
                </View>
              </View>
            </View>
          </Card>
        ))}
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', gap: spacing.md, alignItems: 'flex-start' },
  flex: { flex: 1, gap: 2 },
  badge: { flexDirection: 'row', marginTop: spacing.xs },
  reset: { marginBottom: spacing.md },
});
