import { useMemo, useState } from 'react';
import { FileText, MessageSquare, Mic, Sparkles, UserSearch } from 'lucide-react';
import { Button, ChoiceChip, EmptyState, ErrorState, LoadingSkeleton, Notice, PageHeader, SearchInput } from '@/components/ui';
import { InterviewCard } from '@/components/interview/InterviewCard';
import { interviewService } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT } from '@/i18n';
import { interviewMessages } from '@/i18n/messages/interview';

const HOW = [
  { icon: UserSearch, title: 'how1Title', body: 'how1Body' },
  { icon: MessageSquare, title: 'how2Title', body: 'how2Body' },
  { icon: Mic, title: 'how3Title', body: 'how3Body' },
  { icon: FileText, title: 'how4Title', body: 'how4Body' },
] as const;

export function InterviewCatalogPage() {
  const t = useT(interviewMessages);
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
        .filter((r) => !term || `${r.title} ${r.category} ${r.description} ${r.themes.join(' ')}`.toLowerCase().includes(term))
        .sort((a, b) => b.popularity - a.popularity),
    [roles, category, term],
  );

  return (
    <div>
      <PageHeader
        title={t('catalogTitle')}
        description={t('catalogDesc')}
      />
      <Notice tone="warning" className="mb-6" title={t('prototype')}>{t('demoInterview')}</Notice>

      <div className="space-y-4">
        <SearchInput value={search} onChange={setSearch} placeholder={t('searchPlaceholder')} label={t('searchLabel')} />
        <div className="-mx-1 flex gap-2 overflow-x-auto px-1 pb-1 scrollbar-thin" role="group" aria-label={t('filterCategory')}>
          <ChoiceChip selected={category === 'all'} onClick={() => setCategory('all')} className="shrink-0">{t('allRoles')}</ChoiceChip>
          {categories.map((c) => (
            <ChoiceChip key={c} selected={category === c} onClick={() => setCategory(c)} className="shrink-0">{c}</ChoiceChip>
          ))}
        </div>
        <p className="text-sm text-muted" aria-live="polite">{loading ? t('loadingRoles') : filtered.length === 1 ? t('roleCountOne') : t('roleCountMany', { n: filtered.length })}</p>
      </div>

      <div className="mt-4">
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
          <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
            {filtered.map((r) => <InterviewCard key={r.id} role={r} />)}
          </div>
        )}
      </div>

      <section aria-labelledby="how-interviews" className="mt-12">
        <h2 id="how-interviews" className="flex items-center gap-2 text-lg font-semibold"><Sparkles className="h-5 w-5 text-primary" aria-hidden />{t('howTitle')}</h2>
        <ol className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {HOW.map(({ icon: Icon, title, body }, i) => (
            <li key={title} className="rounded-[var(--radius-card)] border border-line bg-card p-5 shadow-card">
              <div className="flex items-center gap-2">
                <span className="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-xs font-bold text-white">{i + 1}</span>
                <Icon className="h-5 w-5 text-primary" aria-hidden />
              </div>
              <h3 className="mt-3 font-semibold">{t(title)}</h3>
              <p className="mt-1 text-sm text-muted">{t(body)}</p>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
