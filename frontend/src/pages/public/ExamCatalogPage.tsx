import { useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { FileQuestion, SlidersHorizontal, X } from 'lucide-react';
import type { Difficulty, ExamCategory, ExamQuery, LanguageCode } from '@prepmitra/shared';
import { EXAM_CATEGORIES, LANGUAGES } from '@prepmitra/shared';
import { Button, ChoiceChip, EmptyState, ErrorState, LoadingSkeleton, Modal, PageHeader, SearchInput, Select } from '@/components/ui';
import { ExamCard } from '@/components/exam/ExamCard';
import { examService } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT, useUiLang } from '@/i18n';
import { catalogMessages, categoryText } from '@/i18n/messages/catalog';
import { commonMessages } from '@/i18n/messages/common';
import { layoutMessages } from '@/i18n/messages/layout';

const SORTS = [
  { value: 'popular', key: 'sortPopular' },
  { value: 'rating', key: 'sortRating' },
  { value: 'duration-asc', key: 'sortShort' },
  { value: 'duration-desc', key: 'sortLong' },
  { value: 'credits-asc', key: 'sortCredits' },
  { value: 'title', key: 'sortTitle' },
] as const;
const DIFFICULTIES = [
  { value: 'all', key: 'allLevels' },
  { value: 'Easy', key: 'diff_Easy' },
  { value: 'Moderate', key: 'diff_Moderate' },
  { value: 'Hard', key: 'diff_Hard' },
] as const;

export function ExamCatalogPage() {
  const t = useT(catalogMessages);
  const tc = useT(commonMessages);
  const tl = useT(layoutMessages);
  const lang = useUiLang();
  useDocumentTitle(t('catalogDocTitle'));
  const sortOptions = SORTS.map((s) => ({ value: s.value, label: t(s.key) }));
  const difficultyOptions = DIFFICULTIES.map((d) => ({ value: d.value, label: t(d.key) }));
  const languageOptions = [
    { value: 'all', label: t('anyLanguage') },
    ...LANGUAGES.filter((l) => l.tier === 1).map((l) => ({ value: l.code, label: lang === 'hi' ? l.nativeName : l.name })),
  ];
  const [params, setParams] = useSearchParams();
  const [search, setSearch] = useState(params.get('q') ?? '');
  const [filtersOpen, setFiltersOpen] = useState(false);
  const debounced = useDebounce(search);

  const query: ExamQuery = {
    search: debounced,
    category: (params.get('category') as ExamCategory | null) ?? 'all',
    difficulty: (params.get('difficulty') as Difficulty | null) ?? 'all',
    language: (params.get('language') as LanguageCode | null) ?? 'all',
    sort: (params.get('sort') as ExamQuery['sort']) ?? 'popular',
  };
  const { data: exams, loading, error, reload } = useAsync(() => examService.list(query), [JSON.stringify(query)]);

  const setParam = (key: string, value: string) => {
    const next = new URLSearchParams(params);
    if (!value || value === 'all' || (key === 'sort' && value === 'popular')) next.delete(key);
    else next.set(key, value);
    setParams(next, { replace: true });
  };

  const activeCount = useMemo(
    () => ['category', 'difficulty', 'language'].filter((k) => params.get(k)).length + (debounced ? 1 : 0),
    [params, debounced],
  );
  const clearAll = () => {
    setSearch('');
    setParams(new URLSearchParams(), { replace: true });
  };

  const filterControls = (
    <>
      <Select label={t('difficulty')} value={query.difficulty} onChange={(e) => setParam('difficulty', e.target.value)} options={difficultyOptions} />
      <Select label={t('language')} value={query.language} onChange={(e) => setParam('language', e.target.value)} options={languageOptions} />
      <Select label={t('sortBy')} value={query.sort} onChange={(e) => setParam('sort', e.target.value)} options={sortOptions} />
    </>
  );

  return (
    <div>
      <PageHeader
        title={t('catalogTitle')}
        description={t('catalogDesc')}
      />

      <div className="space-y-4">
        <div className="flex gap-2">
          <SearchInput value={search} onChange={setSearch} placeholder={t('searchPlaceholder')} className="flex-1" label={t('searchLabel')} />
          <Button variant="outline" className="md:hidden" onClick={() => setFiltersOpen(true)} leftIcon={<SlidersHorizontal className="h-4 w-4" />}>
            {t('filters')}
          </Button>
        </div>

        <div className="-mx-1 flex gap-2 overflow-x-auto px-1 pb-1 scrollbar-thin" role="group" aria-label={t('filterByCategory')}>
          <ChoiceChip selected={query.category === 'all'} onClick={() => setParam('category', 'all')}>{t('allExams')}</ChoiceChip>
          {EXAM_CATEGORIES.map((c) => (
            <ChoiceChip key={c.id} selected={query.category === c.id} onClick={() => setParam('category', c.id)} className="shrink-0">
              {categoryText(t, c.id).label}
            </ChoiceChip>
          ))}
        </div>

        <div className="hidden grid-cols-3 gap-3 md:grid lg:max-w-3xl">{filterControls}</div>

        <div className="flex items-center justify-between text-sm" aria-live="polite">
          <p className="text-muted">{loading ? t('loadingExams') : exams?.length === 1 ? t('examsFoundOne') : t('examsFound', { count: exams?.length ?? 0 })}</p>
          {activeCount > 0 && (
            <button type="button" onClick={clearAll} className="inline-flex items-center gap-1 font-medium text-primary hover:underline">
              <X className="h-4 w-4" aria-hidden /> {t('clearFilters')}
            </button>
          )}
        </div>
      </div>

      <div className="mt-4">
        {loading ? (
          <LoadingSkeleton count={6} />
        ) : error ? (
          <ErrorState title={tc('somethingWrong')} onRetry={reload} description={error} />
        ) : exams && exams.length > 0 ? (
          <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
            {exams.map((e) => <ExamCard key={e.id} exam={e} />)}
          </div>
        ) : (
          <EmptyState
            icon={<FileQuestion className="h-6 w-6" />}
            title={t('noMatchTitle')}
            description={t('noMatchDesc')}
            action={<Button variant="outline" onClick={clearAll}>{t('clearAll')}</Button>}
          />
        )}
      </div>

      <p className="mt-10 text-xs text-muted">{tl('affiliation')}</p>

      <Modal
        open={filtersOpen}
        onOpenChange={setFiltersOpen}
        title={t('filterExams')}
        footer={
          <>
            <Button variant="outline" onClick={clearAll}>{t('reset')}</Button>
            <Button onClick={() => setFiltersOpen(false)}>{t('showResults')}</Button>
          </>
        }
      >
        <div className="space-y-4">{filterControls}</div>
      </Modal>
    </div>
  );
}
