import { useMemo, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { ArrowRight, FileQuestion, Search, SlidersHorizontal, Sparkles, X } from 'lucide-react';
import type { Difficulty, ExamCategory, ExamQuery, LanguageCode } from '@prepmitra/shared';
import { EXAM_CATEGORIES, LANGUAGES } from '@prepmitra/shared';
import { Button, EmptyState, ErrorState, LoadingSkeleton, Modal, Select } from '@/components/ui';
import { ExamCard } from '@/components/exam/ExamCard';
import { InterviewCard } from '@/components/interview/InterviewCard';
import { examService, interviewService } from '@/services';
import { filterExams } from '@/services/examService';
import { useAsync } from '@/hooks/useAsync';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT, useUiLang } from '@/i18n';
import { useContentT } from '@/i18n/content';
import { catalogMessages, categoryText } from '@/i18n/messages/catalog';
import { commonMessages } from '@/i18n/messages/common';
import { layoutMessages } from '@/i18n/messages/layout';

const SORTS = [
  { value: 'popular', key: 'sortPopular' },
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

/** `all`, one exam category, or the interview roles. */
type Tab = ExamCategory | 'all' | 'interviews';

/** One filter pill: label and a muted count. The selected pill is solid green. */
function Pill({ selected, onClick, label, count }: { selected: boolean; onClick: () => void; label: string; count?: number }) {
  return (
    <button
      type="button"
      aria-pressed={selected}
      onClick={onClick}
      className={cn(
        'inline-flex h-9 shrink-0 items-center gap-2 rounded-full px-4 text-sm font-medium transition-colors',
        selected ? 'bg-secondary text-white' : 'text-muted hover:bg-surface hover:text-ink',
      )}
    >
      {label}
      {count !== undefined && <span className={cn('text-xs tabular-nums', selected ? 'text-white/75' : 'text-subtle')}>{count}</span>}
    </button>
  );
}

/** Compact select for the inline filter row (label is for screen readers). */
function MiniSelect({ label, value, onChange, options }: { label: string; value: string; onChange: (v: string) => void; options: { value: string; label: string }[] }) {
  return (
    <label className="relative">
      <span className="sr-only">{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="h-9 cursor-pointer appearance-none rounded-lg border border-line bg-card pl-3 pr-8 text-sm text-ink hover:border-line-strong focus:border-secondary focus:outline-none focus:ring-2 focus:ring-secondary/20"
      >
        {options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
      <svg viewBox="0 0 20 20" className="pointer-events-none absolute right-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" aria-hidden><path d="M6 8l4 4 4-4" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" /></svg>
    </label>
  );
}

/**
 * Catalog home: search across exams and interview roles, category tiles (only categories that
 * have content), exam cards and interview cards. Data comes from GET /v1/exams and
 * GET /v1/interview-roles (or the demo catalog in mock mode). The free mini mock is promoted
 * in its own strip rather than listed as a regular exam.
 */
export function ExamCatalogPage() {
  const t = useT(catalogMessages);
  const tc = useT(commonMessages);
  const tl = useT(layoutMessages);
  const ct = useContentT();
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
  const term = debounced.trim().toLowerCase();

  const exams = useAsync(() => examService.list({}), []);
  const roles = useAsync(() => interviewService.listRoles(), []);

  const tab = (params.get('category') as Tab | null) ?? 'all';
  const query: ExamQuery = {
    search: debounced,
    category: tab === 'interviews' ? 'all' : tab,
    difficulty: (params.get('difficulty') as Difficulty | null) ?? 'all',
    language: (params.get('language') as LanguageCode | null) ?? 'all',
    sort: (params.get('sort') as ExamQuery['sort']) ?? 'popular',
  };

  const all = exams.data ?? [];
  const paid = all.filter((e) => !e.isFree);
  const freeExam = all.find((e) => e.isFree);
  const shownExams = useMemo(() => filterExams(paid, query), [exams.data, JSON.stringify(query)]); // eslint-disable-line react-hooks/exhaustive-deps
  const freeMatches = freeExam ? filterExams([freeExam], query).length > 0 : false;
  const shownRoles = useMemo(
    () =>
      (roles.data ?? [])
        .filter((r) => !term || `${r.title} ${r.category} ${r.description} ${ct(r.title)} ${ct(r.category)} ${ct(r.description)}`.toLowerCase().includes(term))
        .sort((a, b) => b.popularity - a.popularity),
    [roles.data, term, ct],
  );
  // Only categories that actually have exams get a tile.
  const categories = EXAM_CATEGORIES.map((c) => ({ ...c, count: paid.filter((e) => e.category === c.id).length })).filter((c) => c.count > 0);
  const roleCount = roles.data?.length ?? 0;

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

  const showExams = tab !== 'interviews';
  const showRoles = tab === 'all' || tab === 'interviews';
  const filterControls = (
    <>
      <Select label={t('difficulty')} value={query.difficulty} onChange={(e) => setParam('difficulty', e.target.value)} options={difficultyOptions} />
      <Select label={t('language')} value={query.language} onChange={(e) => setParam('language', e.target.value)} options={languageOptions} />
      <Select label={t('sortBy')} value={query.sort} onChange={(e) => setParam('sort', e.target.value)} options={sortOptions} />
    </>
  );
  const nothing = !exams.loading && !roles.loading && (!showExams || shownExams.length === 0) && (!showRoles || shownRoles.length === 0) && !(showExams && freeMatches);

  const count = (n: number, one: string, many: string) => (n === 1 ? one : many);
  const emptyNote = (text: string) => <p className="rounded-2xl border border-dashed border-line-strong px-4 py-8 text-center text-sm text-muted">{text}</p>;

  return (
    <div>
      {/* ---------- Header with search ---------- */}
      <header className="mx-auto max-w-2xl pb-8 pt-4 text-center sm:pb-10 sm:pt-10">
        <p className="text-sm font-medium text-secondary">{t('homeEyebrow')}</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight sm:text-[2.75rem] sm:leading-tight">{t('homeTitle')}</h1>
        <p className="mx-auto mt-3 max-w-xl text-muted">{t('homeDesc')}</p>
        <div className="mt-7 flex items-center gap-2 rounded-2xl border border-line-strong bg-card px-4 shadow-[0_1px_2px_rgb(28_35_33/0.04)] transition focus-within:border-secondary focus-within:ring-4 focus-within:ring-secondary/10">
          <Search className="h-5 w-5 shrink-0 text-subtle" aria-hidden />
          <input
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t('homeSearchPlaceholder')}
            aria-label={t('homeSearchLabel')}
            className="h-14 min-w-0 flex-1 bg-transparent text-base text-ink placeholder:text-subtle focus:outline-none [&::-webkit-search-cancel-button]:hidden"
          />
          {search && (
            <button type="button" onClick={() => setSearch('')} aria-label={t('clearFilters')} className="flex h-8 w-8 items-center justify-center rounded-full text-muted hover:bg-surface">
              <X className="h-4 w-4" aria-hidden />
            </button>
          )}
        </div>
        <p className="mt-4 text-sm text-muted">
          {[
            count(paid.length, t('statExamOne'), t('statExams', { count: paid.length })),
            count(roleCount, t('statRoleOne'), t('statRoles', { count: roleCount })),
            freeExam ? t('statFree') : null,
          ].filter(Boolean).join(' · ')}
        </p>
      </header>

      {/* ---------- Category pills ---------- */}
      <div className="flex items-center gap-3 border-b border-line pb-3">
        <div className="-mx-4 flex flex-1 gap-1 overflow-x-auto px-4 scrollbar-thin sm:mx-0 sm:px-0" role="group" aria-label={t('filterByCategory')}>
          <Pill selected={tab === 'all'} onClick={() => setParam('category', 'all')} label={t('catAll')} />
          {categories.map((c) => (
            <Pill key={c.id} selected={tab === c.id} onClick={() => setParam('category', c.id)} label={categoryText(t, c.id).label} count={c.count} />
          ))}
          {roleCount > 0 && <Pill selected={tab === 'interviews'} onClick={() => setParam('category', 'interviews')} label={t('catInterviews')} count={roleCount} />}
        </div>
        {activeCount > 0 && (
          <button type="button" onClick={clearAll} className="hidden shrink-0 items-center gap-1 text-sm font-medium text-muted hover:text-ink sm:inline-flex">
            <X className="h-4 w-4" aria-hidden /> {t('clearFilters')}
          </button>
        )}
      </div>

      {/* ---------- Free mini mock ---------- */}
      {showExams && freeExam && freeMatches && (
        <Link
          to={`/exams/${freeExam.id}`}
          className="group mt-6 flex items-center gap-4 rounded-2xl border border-line bg-card px-5 py-4 transition-colors hover:border-primary/40"
        >
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-accent-soft text-primary"><Sparkles className="h-5 w-5" aria-hidden /></span>
          <span className="min-w-0 flex-1">
            <span className="block font-semibold text-ink">{t('miniStripTitle')}</span>
            <span className="block text-sm text-muted">{t('miniStripBody')}</span>
          </span>
          <span className="hidden shrink-0 items-center gap-1 text-sm font-semibold text-primary sm:inline-flex">
            {t('miniStripCta')} <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" aria-hidden />
          </span>
          <ArrowRight className="h-5 w-5 shrink-0 text-primary sm:hidden" aria-hidden />
        </Link>
      )}

      {/* ---------- Exams ---------- */}
      {showExams && (
        <section aria-labelledby="exams-heading" className="mt-10">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h2 id="exams-heading" className="text-xl font-semibold">
              {t('examsHeading')}
              <span className="ml-2 text-sm font-normal text-muted" aria-live="polite">
                {exams.loading ? t('loadingExams') : count(shownExams.length, t('examsFoundOne'), t('examsFound', { count: shownExams.length }))}
              </span>
            </h2>
            <div className="hidden items-center gap-2 md:flex">
              <MiniSelect label={t('difficulty')} value={query.difficulty ?? 'all'} onChange={(v) => setParam('difficulty', v)} options={difficultyOptions} />
              <MiniSelect label={t('language')} value={query.language ?? 'all'} onChange={(v) => setParam('language', v)} options={languageOptions} />
              <MiniSelect label={t('sortBy')} value={query.sort ?? 'popular'} onChange={(v) => setParam('sort', v)} options={sortOptions} />
            </div>
            <Button variant="outline" size="sm" className="md:hidden" onClick={() => setFiltersOpen(true)} leftIcon={<SlidersHorizontal className="h-4 w-4" />}>
              {t('filters')}
            </Button>
          </div>
          <div className="mt-4">
            {exams.loading ? (
              <LoadingSkeleton count={3} />
            ) : exams.error ? (
              <ErrorState title={tc('somethingWrong')} onRetry={exams.reload} description={exams.error} />
            ) : shownExams.length > 0 ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {shownExams.map((e) => <ExamCard key={e.id} exam={e} />)}
              </div>
            ) : (
              !nothing && emptyNote(t('noMatchDesc'))
            )}
          </div>
        </section>
      )}

      {/* ---------- Interviews ---------- */}
      {showRoles && (
        <section aria-labelledby="roles-heading" className="mt-12">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h2 id="roles-heading" className="text-xl font-semibold">
              {t('interviewsHeading')}
              <span className="ml-2 text-sm font-normal text-muted" aria-live="polite">
                {roles.loading ? t('loadingRoles') : count(shownRoles.length, t('rolesFoundOne'), t('rolesFound', { count: shownRoles.length }))}
              </span>
            </h2>
            <Link to="/interviews" className="inline-flex items-center gap-1 text-sm font-medium text-secondary hover:underline">
              {t('howInterviews')} <ArrowRight className="h-4 w-4" aria-hidden />
            </Link>
          </div>
          <p className="mt-1 text-sm text-muted">{t('interviewsSub')}</p>
          <div className="mt-4">
            {roles.loading ? (
              <LoadingSkeleton count={2} />
            ) : roles.error ? (
              <ErrorState title={tc('somethingWrong')} onRetry={roles.reload} description={roles.error} />
            ) : shownRoles.length > 0 ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {shownRoles.map((r) => <InterviewCard key={r.id} role={r} />)}
              </div>
            ) : (
              !nothing && emptyNote(t('noRolesMatch'))
            )}
          </div>
        </section>
      )}

      {nothing && (
        <div className="mt-8">
          <EmptyState
            icon={<FileQuestion className="h-6 w-6" />}
            title={t('noMatchTitle')}
            description={t('noMatchDesc')}
            action={<Button variant="outline" onClick={clearAll}>{t('clearAll')}</Button>}
          />
        </div>
      )}

      <p className="mt-12 text-xs text-subtle">{tl('affiliation')}</p>

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
