import { useMemo, useState } from 'react';
import { Languages, Mic, Percent, UserX } from 'lucide-react';
import toast from 'react-hot-toast';
import type { LanguageConfig } from '@prepmitra/shared';
import { LANGUAGES } from '@prepmitra/shared';
import { Badge, Card, CardHeader, EmptyState, PageHeader, ProgressBar, SearchInput, Select, StatCard } from '@/components/ui';
import { AdminLoadGate, DataTable, ToggleSwitch, type Column } from '@/components/admin/AdminUi';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { useAdminStore } from '@/store/adminStore';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

const meta = (code: string) => LANGUAGES.find((l) => l.code === code)!;
const coverageTone = (v: number) => (v >= 75 ? 'success' : v >= 40 ? 'warning' : 'danger') as 'success' | 'warning' | 'danger';

export function AdminLanguagesPage() {
  useDocumentTitle('Languages');
  const load = useAdminLoad('languages');
  const languages = useAdminStore((s) => s.languages);
  const team = useAdminStore((s) => s.team);
  const [search, setSearch] = useState('');
  const term = useDebounce(search).trim().toLowerCase();

  const reviewerOptions = useMemo(
    () => [{ value: '', label: 'Unassigned' }, ...team.filter((m) => m.active).map((m) => ({ value: m.name, label: m.name }))],
    [team],
  );

  const update = async (l: LanguageConfig, patch: Partial<Omit<LanguageConfig, 'code' | 'tier'>>, msg: string) => {
    try {
      await adminService.updateLanguage(l.code, patch);
      toast.success(msg);
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  const visible = languages.filter((l) => {
    const m = meta(l.code);
    return !term || `${m.name} ${m.nativeName} ${l.code}`.toLowerCase().includes(term);
  });
  const enabled = languages.filter((l) => l.enabled).length;
  const voice = languages.filter((l) => l.enabled && l.voiceSupported).length;
  const avgCoverage = Math.round(languages.reduce((s, l) => s + l.coverage, 0) / Math.max(languages.length, 1));
  const unassigned = languages.filter((l) => l.enabled && !l.reviewer).length;

  const columns: Column<LanguageConfig>[] = [
    {
      key: 'name',
      header: 'Language',
      cell: (l) => {
        const m = meta(l.code);
        return (
          <div>
            <p className="font-medium">{m.name} <span className="ml-1 text-muted" lang={l.code} dir={m.rtl ? 'rtl' : undefined}>{m.nativeName}</span></p>
            <p className="text-xs text-muted">{l.code}{m.rtl ? ' · right-to-left' : ''}</p>
          </div>
        );
      },
    },
    {
      key: 'enabled',
      header: 'Enabled',
      cell: (l) => (
        <ToggleSwitch
          checked={l.enabled}
          disabled={l.code === 'en'}
          onChange={(v) => void update(l, { enabled: v }, `${meta(l.code).name} ${v ? 'enabled' : 'disabled'} for learners`)}
          label={l.code === 'en' ? 'English is the source language and cannot be disabled' : `${meta(l.code).name} enabled`}
        />
      ),
    },
    {
      key: 'voice',
      header: 'Voice',
      cell: (l) => (
        <ToggleSwitch
          checked={l.voiceSupported}
          disabled={!l.enabled}
          onChange={(v) => void update(l, { voiceSupported: v }, `Voice interviews ${v ? 'on' : 'off'} for ${meta(l.code).name}`)}
          label={`Voice interviews in ${meta(l.code).name}`}
        />
      ),
    },
    {
      key: 'coverage',
      header: 'Question coverage',
      cell: (l) => (
        <div className="flex min-w-[150px] items-center gap-2">
          <ProgressBar value={l.coverage} tone={coverageTone(l.coverage)} size="sm" className="flex-1" />
          <span className="w-10 text-right text-xs font-semibold">{l.coverage}%</span>
        </div>
      ),
    },
    {
      key: 'reviewer',
      header: 'Reviewer',
      cell: (l) => (
        <Select
          aria-label={`Reviewer for ${meta(l.code).name}`}
          value={l.reviewer ?? ''}
          options={reviewerOptions}
          containerClassName="min-w-[180px]"
          className="h-9"
          onChange={(e) => void update(l, { reviewer: e.target.value || null }, e.target.value ? `${e.target.value} now reviews ${meta(l.code).name}` : `Reviewer removed from ${meta(l.code).name}`)}
        />
      ),
    },
  ];

  return (
    <div className="space-y-5">
      <PageHeader title="Languages" description="All 23 supported languages. Tier 1 launches with full content and voice; Tier 2 is text-only while coverage grows." />
      <AdminLoadGate state={load}>
        <section aria-label="Language summary" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Enabled" value={`${enabled} / ${languages.length}`} icon={<Languages className="h-5 w-5" />} />
          <StatCard label="Voice interviews" value={voice} icon={<Mic className="h-5 w-5" />} hint="Enabled languages with voice" />
          <StatCard label="Average coverage" value={`${avgCoverage}%`} icon={<Percent className="h-5 w-5" />} hint="Verified translations" />
          <StatCard label="Without reviewer" value={unassigned} icon={<UserX className="h-5 w-5" />} hint="Enabled languages" />
        </section>
        <SearchInput value={search} onChange={setSearch} placeholder="Search language or code" label="Search languages" className="sm:max-w-sm" />
        {visible.length === 0 ? (
          <EmptyState title="No languages match" description="Try the English or native name, or the language code." />
        ) : (
          [1, 2].map((tier) => {
            const rows = visible.filter((l) => l.tier === tier);
            if (rows.length === 0) return null;
            return (
              <section key={tier} aria-labelledby={`tier-${tier}`} className="space-y-3">
                <Card className="border-none bg-transparent shadow-none">
                  <CardHeader
                    className="px-0 pt-0"
                    title={<span id={`tier-${tier}`}>Tier {tier} <Badge tone={tier === 1 ? 'primary' : 'neutral'} className="ml-1">{rows.length}</Badge></span>}
                    description={tier === 1 ? 'Full exam content, interviews and voice at launch.' : 'Text-first; enable voice once speech models and reviewers are ready.'}
                  />
                </Card>
                <DataTable caption={`Tier ${tier} languages`} columns={columns} rows={rows} rowKey={(l) => l.code} minWidth={820} />
              </section>
            );
          })
        )}
      </AdminLoadGate>
    </div>
  );
}
