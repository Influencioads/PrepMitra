import { useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Copy, FileQuestion, Pencil, Plus, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import type { Exam, PublishStatus } from '@prepmitra/shared';
import { EXAM_CATEGORIES, categoryLabel, formatDate } from '@prepmitra/shared';
import { Button, ButtonLink, ConfirmationDialog, EmptyState, PageHeader, SearchInput, Select } from '@/components/ui';
import { AdminLoadGate, DataTable, FilterBar, IconButton, ResultCount, StatusBadge, ToggleSwitch, type Column } from '@/components/admin/AdminUi';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { PUBLISH_OPTIONS, PUBLISH_STATUS } from '@/components/admin/labels';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { useAdminStore } from '@/store/adminStore';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

const CATEGORY_OPTIONS = [{ value: 'all', label: 'All categories' }, ...EXAM_CATEGORIES.map((c) => ({ value: c.id, label: c.label }))];
const STATUS_OPTIONS = [{ value: 'all', label: 'All statuses' }, ...PUBLISH_OPTIONS];
const DIFFICULTY_OPTIONS = [{ value: 'all', label: 'All levels' }, { value: 'Easy', label: 'Easy' }, { value: 'Moderate', label: 'Moderate' }, { value: 'Hard', label: 'Hard' }];

export function AdminExamsPage() {
  useDocumentTitle('Exams & blueprints');
  const load = useAdminLoad('exams');
  const exams = useAdminStore((s) => s.exams);
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('all');
  const [status, setStatus] = useState('all');
  const [difficulty, setDifficulty] = useState('all');
  const [toDelete, setToDelete] = useState<Exam | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const term = useDebounce(search).trim().toLowerCase();

  const rows = useMemo(
    () =>
      exams.filter(
        (e) =>
          (category === 'all' || e.category === category) &&
          (status === 'all' || e.status === status) &&
          (difficulty === 'all' || e.difficulty === difficulty) &&
          (!term || `${e.title} ${e.shortTitle} ${e.conductingBody} ${e.id}`.toLowerCase().includes(term)),
      ),
    [exams, category, status, difficulty, term],
  );
  const filtered = category !== 'all' || status !== 'all' || difficulty !== 'all' || !!term;
  const clear = () => {
    setSearch('');
    setCategory('all');
    setStatus('all');
    setDifficulty('all');
  };

  const run = async (key: string, fn: () => Promise<unknown>, success: string) => {
    setBusy(key);
    try {
      await fn();
      toast.success(success);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(null);
    }
  };

  const togglePublish = (e: Exam) => {
    const next: PublishStatus = e.status === 'published' ? 'draft' : 'published';
    void run(`pub-${e.id}`, () => adminService.setExamStatus(e.id, next), next === 'published' ? `${e.shortTitle} is now live` : `${e.shortTitle} moved to draft`);
  };

  const duplicate = (e: Exam) =>
    void run(`dup-${e.id}`, async () => {
      const copy = await adminService.duplicateExam(e.id);
      if (copy) navigate(`/admin/exams/${copy.id}/edit`);
    }, `Duplicated ${e.shortTitle} as a draft`);

  const confirmDelete = async () => {
    if (!toDelete) return;
    await run(`del-${toDelete.id}`, () => adminService.deleteExam(toDelete.id), `Deleted ${toDelete.shortTitle}`);
    setToDelete(null);
  };

  const columns: Column<Exam>[] = [
    {
      key: 'title',
      header: 'Exam',
      cell: (e) => (
        <div className="min-w-[200px]">
          <Link to={`/admin/exams/${e.id}/edit`} className="font-medium text-ink hover:text-primary hover:underline">{e.title}</Link>
          <p className="text-xs text-muted">{e.conductingBody} · {e.id}</p>
        </div>
      ),
    },
    { key: 'category', header: 'Category', cell: (e) => <span className="whitespace-nowrap">{categoryLabel(e.category)}</span> },
    {
      key: 'blueprint',
      header: 'Blueprint',
      cell: (e) => (
        <span className="whitespace-nowrap text-muted">
          {e.sections.length} sec · {e.totalQuestions} Q · {e.totalMarks} marks · {e.durationMin} min
        </span>
      ),
    },
    { key: 'difficulty', header: 'Level', cell: (e) => e.difficulty },
    { key: 'langs', header: 'Languages', cell: (e) => <span title={e.languages.join(', ')}>{e.languages.length}</span> },
    { key: 'credits', header: 'Credits', cell: (e) => (e.creditCost === 0 ? 'Free' : e.creditCost) },
    { key: 'status', header: 'Status', cell: (e) => <StatusBadge map={PUBLISH_STATUS} value={e.status} /> },
    {
      key: 'live',
      header: 'Live',
      cell: (e) => <ToggleSwitch checked={e.status === 'published'} onChange={() => togglePublish(e)} label={`Publish ${e.shortTitle}`} disabled={busy === `pub-${e.id}`} />,
    },
    { key: 'updated', header: 'Updated', cell: (e) => <span className="whitespace-nowrap text-muted">{formatDate(e.updatedAt)}</span> },
    {
      key: 'actions',
      header: 'Actions',
      srHeader: true,
      className: 'text-right',
      cell: (e) => (
        <div className="flex justify-end gap-0.5">
          <IconButton label={`Edit ${e.shortTitle}`} onClick={() => navigate(`/admin/exams/${e.id}/edit`)}><Pencil className="h-4 w-4" /></IconButton>
          <IconButton label={`Duplicate ${e.shortTitle}`} onClick={() => duplicate(e)} disabled={busy === `dup-${e.id}`}><Copy className="h-4 w-4" /></IconButton>
          <IconButton label={`Delete ${e.shortTitle}`} tone="danger" onClick={() => setToDelete(e)}><Trash2 className="h-4 w-4" /></IconButton>
        </div>
      ),
    },
  ];

  const counts = { published: exams.filter((e) => e.status === 'published').length, draft: exams.filter((e) => e.status === 'draft').length, hidden: exams.filter((e) => e.status === 'hidden').length };

  return (
    <div className="space-y-5">
      <PageHeader
        title="Exams & blueprints"
        description={`${exams.length} exams · ${counts.published} published, ${counts.draft} draft, ${counts.hidden} hidden. Blueprints define sections, marking and languages for AI paper generation.`}
        actions={<ButtonLink to="/admin/exams/new" leftIcon={<Plus className="h-4 w-4" />}>New exam</ButtonLink>}
      />
      <AdminLoadGate state={load}>
        <FilterBar>
          <SearchInput value={search} onChange={setSearch} placeholder="Search title, body or id" label="Search exams" />
          <Select aria-label="Category" value={category} onChange={(e) => setCategory(e.target.value)} options={CATEGORY_OPTIONS} />
          <Select aria-label="Status" value={status} onChange={(e) => setStatus(e.target.value)} options={STATUS_OPTIONS} />
          <Select aria-label="Difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)} options={DIFFICULTY_OPTIONS} />
        </FilterBar>
        <ResultCount count={rows.length} noun="exam" onClear={filtered ? clear : undefined} />
        <DataTable
          caption="Exams"
          columns={columns}
          rows={rows}
          rowKey={(e) => e.id}
          minWidth={1080}
          empty={
            <EmptyState
              icon={<FileQuestion className="h-6 w-6" />}
              title={exams.length === 0 ? 'No exams yet' : 'No exams match these filters'}
              description={exams.length === 0 ? 'Create your first exam blueprint to make it available to learners.' : 'Try a different search or clear the filters.'}
              action={exams.length === 0 ? <ButtonLink to="/admin/exams/new">Create exam</ButtonLink> : <Button variant="outline" onClick={clear}>Clear filters</Button>}
            />
          }
        />
      </AdminLoadGate>

      <ConfirmationDialog
        open={!!toDelete}
        onOpenChange={(o) => !o && setToDelete(null)}
        title="Delete this exam?"
        description={toDelete ? `“${toDelete.title}” will be removed from the catalog. Past attempts and reports are kept by the backend.` : undefined}
        confirmLabel="Delete exam"
        variant="danger"
        loading={!!toDelete && busy === `del-${toDelete.id}`}
        onConfirm={confirmDelete}
      />
    </div>
  );
}
