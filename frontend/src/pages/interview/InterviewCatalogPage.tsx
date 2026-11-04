import { useMemo, useState } from 'react';
import { FileText, Info, MessageSquare, Mic, Search, UserSearch, X } from 'lucide-react';
import { Button, EmptyState, ErrorState, LoadingSkeleton } from '@/components/ui';
import { cn } from '@/utils/cn';
import { InterviewCard } from '@/components/interview/InterviewCard';
import { interviewService } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT } from '@/i18n';
import { interviewMessages } from '@/i18n/messages/interview';
import { useContentT } from '@/i18n/content';

const HOW = [
  { icon: UserSearch, title: 'how1Title', body: 'how1Body' },
  { icon: MessageSquare, title: 'how2Title', body: 'how2Body' },
  { icon: Mic, title: 'how3Title', body: 'how3Body' },
  { icon: FileText, title: 'how4Title', body: 'how4Body' },
] as const;

export function InterviewCatalogPage() {
  const t = useT(interviewMessages);
  const ct = useContentT();
  useDocumentTitle(t('catalogDocTitle'));
  const { data: roles, loading, error, reload } = useAsync(() => interviewService.listRoles(), []);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('all');
  const term = useDebounce(search).trim().toLowerCase();

  const categories = useMemo(() => [...new Set((roles ?? []).map((r) => r.category))], [roles]);
  const filtered = useMemo(
    () =>
      (roles ?? [])
        .filter((r) => category === 'all' || r.category === category)
        .filter((r) => !term || `${r.title} ${r.category} ${r.description} ${ct(r.title)} ${ct(r.description)} ${r.themes.join(' ')}`.toLowerCase().includes(term))
        .sort((a, b) => b.popularity - a.popularity),
    [roles, category, term, ct],
  );

  const pill = (selected: boolean) =>
    cn('inline-flex h-9 shrink-0 items-center rounded-full px-4 text-sm font-medium transition-colors', selected ? 'bg-secondary text-white' : 'text-muted hover:bg-surface hover:text-ink');

  return (
    <div>
      <header className="mx-auto max-w-2xl pb-8 pt-4 text-center sm:pb-10 sm:pt-10">
        <h1 className="text-3xl font-bold tracking-tight sm:text-[2.75rem] sm:leading-tight">{t('catalogTitle')}</h1>
        <p className="mx-auto mt-3 max-w-xl text-muted">{t('catalogDesc')}</p>
        <div className="mt-7 flex items-center gap-2 rounded-2xl border border-line-strong bg-card px-4 transition focus-within:border-secondary focus-within:ring-4 focus-within:ring-secondary/10">
          <Search className="h-5 w-5 shrink-0 text-subtle" aria-hidden />
          <input
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t('searchPlaceholder')}
            aria-label={t('searchLabel')}
            className="h-14 min-w-0 flex-1 bg-transparent text-base text-ink placeholder:text-subtle focus:outline-none [&::-webkit-search-cancel-button]:hidden"
          />
          {search && (
            <button type="button" onClick={() => setSearch('')} aria-label={t('showAllRoles')} className="flex h-8 w-8 items-center justify-center rounded-full text-muted hover:bg-surface">
              <X className="h-4 w-4" aria-hidden />
            </button>
          )}
        </div>
        <p className="mt-4 inline-flex items-center gap-1.5 text-sm text-muted">
          <Info className="h-4 w-4 shrink-0 text-warning" aria-hidden />
          <span><span className="font-medium text-ink">{t('prototype')}:</span> {t('demoInterview')}</span>
        </p>
      </header>

      <div className="flex items-center justify-between gap-3 border-b border-line pb-3">
        <div className="-mx-4 flex flex-1 gap-1 overflow-x-auto px-4 scrollbar-thin sm:mx-0 sm:px-0" role="group" aria-label={t('filterCategory')}>
          <button type="button" aria-pressed={category === 'all'} onClick={() => setCategory('all')} className={pill(category === 'all')}>{t('allRoles')}</button>
          {categories.map((c) => (
            <button key={c} type="button" aria-pressed={category === c} onClick={() => setCategory(c)} className={pill(category === c)}>{ct(c)}</button>
          ))}
        </div>
        <p className="hidden shrink-0 text-sm text-muted sm:block" aria-live="polite">{loading ? t('loadingRoles') : filtered.length === 1 ? t('roleCountOne') : t('roleCountMany', { n: filtered.length })}</p>
      </div>

      <div className="mt-6">
        {loading ? (
          <LoadingSkeleton count={6} />
        ) : error ? (
          <ErrorState description={error} onRetry={reload} />
        ) : filtered.length === 0 ? (
          <EmptyState
            title={t('noRoles')}
            description={t('noRolesDesc')}
            action={<Button variant="outline" onClick={() => { setSearch(''); setCategory('all'); }}>{t('showAllRoles')}</Button>}
          />
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((r) => <InterviewCard key={r.id} role={r} />)}
          </div>
        )}
      </div>

      <section aria-labelledby="how-interviews" className="mt-16 border-t border-line pt-10">
        <h2 id="how-interviews" className="text-xl font-semibold">{t('howTitle')}</h2>
        <ol className="mt-6 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {HOW.map(({ icon: Icon, title, body }, i) => (
            <li key={title}>
              <div className="flex items-center gap-3">
                <span className="flex h-9 w-9 items-center justify-center rounded-full bg-secondary-soft text-secondary"><Icon className="h-4 w-4" aria-hidden /></span>
                <span className="text-xs font-medium text-subtle">0{i + 1}</span>
              </div>
              <h3 className="mt-3 font-semibold">{t(title)}</h3>
              <p className="mt-1 text-sm leading-relaxed text-muted">{t(body)}</p>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
