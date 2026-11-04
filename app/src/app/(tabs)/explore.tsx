import { useEffect, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, TextInput, View } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { Difficulty, ExamCategory, ExamQuery } from '@prepmitra/shared';
import { EXAM_CATEGORIES, INTERVIEW_ROLES } from '@prepmitra/shared';
import {
  AppText, BottomSheet, Button, Card, Chip, EmptyState, ErrorState, ExamCard, IconTile, LoadingSkeleton, Screen, TabHeader,
} from '@/components';
import { useAsync } from '@/hooks/useAsync';
import { examService } from '@/services';
import { useSubscriptionStore } from '@/store';
import { colors, radii, spacing, TOUCH } from '@/theme';
import { CATEGORY_ICONS } from '@/utils/icons';

type Sort = NonNullable<ExamQuery['sort']>;
const SORTS: { value: Sort; label: string }[] = [
  { value: 'popular', label: 'Most popular' },
  { value: 'duration-asc', label: 'Shortest first' },
  { value: 'duration-desc', label: 'Longest first' },
  { value: 'credits-asc', label: 'Fewest credits' },
  { value: 'title', label: 'A–Z' },
];
const DIFFICULTIES: (Difficulty | 'all')[] = ['all', 'Easy', 'Moderate', 'Hard'];
const isCategory = (v: unknown): v is ExamCategory => EXAM_CATEGORIES.some((c) => c.id === v);

export default function Explore() {
  const params = useLocalSearchParams<{ category?: string }>();
  const freeTrialAvailable = useSubscriptionStore((s) => !s.sub.freeMiniMockUsed);
  const [search, setSearch] = useState('');
  const [debounced, setDebounced] = useState('');
  const [category, setCategory] = useState<ExamCategory | 'all'>(isCategory(params.category) ? params.category : 'all');
  const [difficulty, setDifficulty] = useState<Difficulty | 'all'>('all');
  const [sort, setSort] = useState<Sort>('popular');
  const [sheet, setSheet] = useState(false);

  // Deep links such as /explore?category=banking select the category chip.
  useEffect(() => {
    if (isCategory(params.category)) setCategory(params.category);
  }, [params.category]);

  useEffect(() => {
    const t = setTimeout(() => setDebounced(search), 250);
    return () => clearTimeout(t);
  }, [search]);

  const query: ExamQuery = { search: debounced, category, difficulty, sort };
  const { data, loading, error, reload } = useAsync(() => examService.list(query), JSON.stringify(query));
  const filtersActive = difficulty !== 'all' || sort !== 'popular';
  const clearAll = () => {
    setSearch('');
    setCategory('all');
    setDifficulty('all');
    setSort('popular');
  };

  return (
    <Screen
      edges={['top', 'left', 'right']}
      padded={false}
      header={
        <View style={styles.header}>
          <TabHeader title="Explore" subtitle="Mock exams on real patterns, plus mock interviews." />
          <View style={styles.searchRow}>
            <View style={styles.search}>
              <Ionicons name="search" size={18} color={colors.textSecondary} />
              <SearchInput value={search} onChange={setSearch} />
              {search ? (
                <Pressable onPress={() => setSearch('')} accessibilityRole="button" accessibilityLabel="Clear search" hitSlop={10}>
                  <Ionicons name="close-circle" size={18} color={colors.textMuted} />
                </Pressable>
              ) : null}
            </View>
            <Pressable
              onPress={() => setSheet(true)}
              accessibilityRole="button"
              accessibilityLabel={`Filters and sort${filtersActive ? ', active' : ''}`}
              style={[styles.filterBtn, filtersActive && styles.filterActive]}
            >
              <Ionicons name="options-outline" size={20} color={filtersActive ? colors.white : colors.text} />
            </Pressable>
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chips} accessibilityRole="radiogroup">
            <Chip label="All" role="radio" selected={category === 'all'} onPress={() => setCategory('all')} />
            {EXAM_CATEGORIES.map((c) => (
              <Chip key={c.id} role="radio" label={c.label.replace(' Exams', '')} icon={CATEGORY_ICONS[c.id]} selected={category === c.id} onPress={() => setCategory(c.id)} />
            ))}
          </ScrollView>
        </View>
      }
    >
      <View style={styles.body}>
        <Card onPress={() => router.push('/interviews')} accessibilityLabel="Mock interviews. Practise text or voice interviews for 8 roles." style={styles.interviewCard}>
          <IconTile name="mic-outline" tone="secondary" size={44} />
          <View style={styles.flex}>
            <AppText variant="bodyStrong">Mock interviews</AppText>
            <AppText variant="small">{INTERVIEW_ROLES.filter((r) => r.status === 'published').length} roles · text or voice · model answers</AppText>
          </View>
          <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
        </Card>

        {loading && !data ? (
          <LoadingSkeleton variant="list" rows={4} />
        ) : error ? (
          <ErrorState title="Couldn’t load exams" description={error} onRetry={reload} />
        ) : !data || data.length === 0 ? (
          <EmptyState icon="search-outline" title="No exams match" description="Try a different search or clear the filters." actionLabel="Clear filters" onAction={clearAll} />
        ) : (
          <>
            <AppText variant="small" accessibilityLiveRegion="polite">
              {data.length} {data.length === 1 ? 'exam' : 'exams'}
              {loading ? ' · updating…' : ''}
            </AppText>
            {data.map((e) => (
              <ExamCard key={e.id} exam={e} freeTrialAvailable={freeTrialAvailable} onPress={() => router.push(`/exams/${e.id}`)} />
            ))}
          </>
        )}
      </View>

      <BottomSheet
        visible={sheet}
        onClose={() => setSheet(false)}
        title="Filter and sort"
        footer={
          <View style={styles.sheetActions}>
            <Button title="Reset" variant="outline" style={styles.flex} onPress={() => { setDifficulty('all'); setSort('popular'); }} />
            <Button title="Show results" style={styles.flex} onPress={() => setSheet(false)} />
          </View>
        }
      >
        <AppText variant="label">Difficulty</AppText>
        <View style={styles.wrapChips} accessibilityRole="radiogroup">
          {DIFFICULTIES.map((d) => (
            <Chip key={d} role="radio" label={d === 'all' ? 'Any' : d} selected={difficulty === d} onPress={() => setDifficulty(d)} />
          ))}
        </View>
        <AppText variant="label">Sort by</AppText>
        <View style={styles.wrapChips} accessibilityRole="radiogroup">
          {SORTS.map((s) => (
            <Chip key={s.value} role="radio" label={s.label} selected={sort === s.value} onPress={() => setSort(s.value)} />
          ))}
        </View>
      </BottomSheet>
    </Screen>
  );
}


function SearchInput({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return (
    <TextInput
      value={value}
      onChangeText={onChange}
      placeholder="Search SSC, IBPS, CAT, GATE…"
      placeholderTextColor={colors.textMuted}
      accessibilityLabel="Search exams"
      returnKeyType="search"
      autoCorrect={false}
      style={styles.searchInput}
    />
  );
}

const styles = StyleSheet.create({
  header: { paddingHorizontal: spacing.lg, paddingTop: spacing.lg, gap: spacing.md, paddingBottom: spacing.sm },
  searchRow: { flexDirection: 'row', gap: spacing.sm },
  search: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    minHeight: TOUCH + 4,
    paddingHorizontal: spacing.md,
    backgroundColor: colors.card,
    borderRadius: radii.md,
    borderWidth: 1,
    borderColor: colors.border,
  },
  searchInput: { flex: 1, fontSize: 16, color: colors.text, paddingVertical: 10 },
  filterBtn: {
    width: TOUCH + 4,
    height: TOUCH + 4,
    borderRadius: radii.md,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
  },
  filterActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  chips: { gap: spacing.sm, paddingRight: spacing.lg },
  body: { padding: spacing.lg, paddingTop: spacing.sm, gap: spacing.md, paddingBottom: spacing['2xl'] },
  interviewCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  flex: { flex: 1 },
  wrapChips: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  sheetActions: { flexDirection: 'row', gap: spacing.sm },
});
