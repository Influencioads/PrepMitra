import { useMemo, useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import { DISCLAIMERS } from '@prepmitra/shared';
import { AppText, Chip, EmptyState, ErrorState, InterviewCard, LoadingSkeleton, Notice, Screen } from '@/components';
import { useAsync } from '@/hooks/useAsync';
import { interviewService } from '@/services';
import { useProfileStore } from '@/store';
import { spacing } from '@/theme';

export default function InterviewRoles() {
  const { data, loading, error, reload } = useAsync(() => interviewService.listRoles(), 'roles');
  const targetRoleIds = useProfileStore((s) => s.profile.targetRoleIds);
  const [category, setCategory] = useState('all');
  const categories = useMemo(() => ['all', ...new Set((data ?? []).map((r) => r.category))], [data]);
  const roles = useMemo(
    () =>
      (data ?? [])
        .filter((r) => category === 'all' || r.category === category)
        .sort((a, b) => Number(targetRoleIds.includes(b.id)) - Number(targetRoleIds.includes(a.id)) || b.popularity - a.popularity),
    [data, category, targetRoleIds],
  );

  if (loading) return <Screen><LoadingSkeleton variant="list" rows={4} /></Screen>;
  if (error) return <Screen><ErrorState title="Couldn’t load interview roles" description={error} onRetry={reload} /></Screen>;

  return (
    <Screen>
      <AppText variant="body">Pick a role. You’ll choose level, language and text or voice on the next screen.</AppText>
      <Notice tone="warning" title="Scripted demo">{DISCLAIMERS.demoInterview}</Notice>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chips} accessibilityRole="radiogroup">
        {categories.map((c) => (
          <Chip key={c} role="radio" label={c === 'all' ? 'All roles' : c} selected={category === c} onPress={() => setCategory(c)} />
        ))}
      </ScrollView>
      {roles.length === 0 ? (
        <EmptyState icon="briefcase-outline" title="No roles in this category" actionLabel="Show all roles" onAction={() => setCategory('all')} />
      ) : (
        <View style={styles.list}>
          {roles.map((r) => (
            <InterviewCard key={r.id} role={r} onPress={() => router.push(`/interviews/${r.id}`)} />
          ))}
        </View>
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  chips: { gap: spacing.sm },
  list: { gap: spacing.md },
});
