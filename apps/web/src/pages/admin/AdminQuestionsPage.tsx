import { useMemo, useState } from 'react';
import { BookOpenCheck, CircleCheck, Eye, Pencil, Plus, ShieldOff, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import type { AdminQuestion, QuestionStatusAdmin } from '@prepmitra/shared';
import { formatDate } from '@prepmitra/shared';
import { Badge, Button, ConfirmationDialog, EmptyState, Modal, PageHeader, SearchInput, Select, Textarea, accuracyTone } from '@/components/ui';
import { AdminLoadGate, DataTable, FilterBar, IconButton, ResultCount, StatusBadge, type Column } from '@/components/admin/AdminUi';
import { QuestionPreview } from '@/components/admin/QuestionPreview';
import { QuestionFormModal } from '@/components/admin/QuestionFormModal';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { QUESTION_STATUS, SUBJECT_LABELS, SUBJECT_OPTIONS, TYPE_LABELS } from '@/components/admin/labels';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { useAdminStore } from '@/store/adminStore';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

const ALL = { value: 'all', label: '' };
const SUBJECTS = [{ ...ALL, label: 'All subjects' }, ...SUBJECT_OPTIONS];
const TYPES = [{ ...ALL, label: 'All types' }, ...Object.entries(TYPE_LABELS).map(([value, label]) => ({ value, label }))];
const DIFFS = [{ ...ALL, label: 'All difficulties' }, ...['Easy', 'Moderate', 'Hard'].map((d) => ({ value: d, label: d }))];
const STATUSES = [{ ...ALL, label: 'All statuses' }, ...Object.entries(QUESTION_STATUS).map(([value, m]) => ({ value, label: m.label }))];
const toneText = { success: 'text-green-700', warning: 'text-warning-ink', danger: 'text-red-700' };

export function AdminQuestionsPage() {
  useDocumentTitle('Question bank');
  const load = useAdminLoad('questions');
  const questions = useAdminStore((s) => s.questions);
  const threshold = useAdminStore((s) => s.settings.featureFlags.autoQuarantineThreshold);
  const [search, setSearch] = useState('');
  const [subject, setSubject] = useState('all');
  const [type, setType] = useState('all');
  const [difficulty, setDifficulty] = useState('all');
  const [status, setStatus] = useState('all');
  const [viewing, setViewing] = useState<AdminQuestion | null>(null);
  const [editing, setEditing] = useState<AdminQuestion | null | undefined>(undefined);
  const [quarantine, setQuarantine] = useState<AdminQuestion | null>(null);
  const [quarantineReason, setQuarantineReason] = useState('');
  const [toDelete, setToDelete] = useState<AdminQuestion | null>(null);
  const [busy, setBusy] = useState(false);
  const term = useDebounce(search).trim().toLowerCase();

  const rows = useMemo(
    () =>
      questions.filter(
        (q) =>
          (subject === 'all' || q.subject === subject) &&
          (type === 'all' || q.type === type) &&
          (difficulty === 'all' || q.difficulty === difficulty) &&
          (status === 'all' || q.status === status) &&
          (!term || `${q.id} ${q.topic} ${q.text}`.toLowerCase().includes(term)),
      ),
    [questions, subject, type, difficulty, status, term],
  );
  const filtered = subject !== 'all' || type !== 'all' || difficulty !== 'all' || status !== 'all' || !!term;
  const clear = () => {
    setSearch('');
    setSubject('all');
    setType('all');
    setDifficulty('all');
    setStatus('all');
  };
  const counts = useMemo(() => {
    const c: Record<QuestionStatusAdmin, number> = { verified: 0, 'pending-review': 0, quarantined: 0, rejected: 0 };
    questions.forEach((q) => c[q.status]++);
    return c;
  }, [questions]);

  const approve = async (q: AdminQuestion) => {
    try {
      await adminService.setQuestionStatus(q.id, 'verified');
      toast.success(`${q.id} approved and verified`);
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  const doQuarantine = async () => {
    if (!quarantine) return;
    setBusy(true);
    try {
      await adminService.setQuestionStatus(quarantine.id, 'quarantined', quarantineReason.trim() || 'Manual quarantine');
      toast.success(`${quarantine.id} quarantined — it will not be served`);
      setQuarantine(null);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  const doDelete = async () => {
    if (!toDelete) return;
    setBusy(true);
    try {
      await adminService.deleteQuestion(toDelete.id);
      toast.success(`${toDelete.id} deleted`);
      setToDelete(null);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  const columns: Column<AdminQuestion>[] = [
    {
      key: 'q',
      header: 'Question',
      cell: (q) => (
        <button type="button" onClick={() => setViewing(q)} className="block max-w-[340px] text-left">
          <span className="line-clamp-2 font-medium text-ink hover:text-primary">{q.text}</span>
          <span className="text-xs text-muted">{q.id} · {q.topic}</span>
        </button>
      ),
    },
    { key: 'subject', header: 'Subject', cell: (q) => <span className="whitespace-nowrap">{SUBJECT_LABELS[q.subject]}</span> },
    { key: 'type', header: 'Type', cell: (q) => <span className="whitespace-nowrap">{TYPE_LABELS[q.type]}</span> },
    { key: 'diff', header: 'Difficulty', cell: (q) => q.difficulty },
    {
      key: 'acc',
      header: 'Accuracy',
      cell: (q) => (q.attemptCount ? <span className={cn('font-semibold', toneText[accuracyTone(q.accuracy)])}>{q.accuracy}%</span> : <span className="text-muted">—</span>),
    },
    { key: 'att', header: 'Attempts', cell: (q) => q.attemptCount.toLocaleString('en-IN') },
    {
      key: 'reports',
      header: 'Reports',
      cell: (q) => (q.reportCount > 0 ? <Badge tone={q.reportCount >= threshold ? 'danger' : 'warning'}>{q.reportCount}</Badge> : <span className="text-muted">0</span>),
    },
    { key: 'lang', header: 'Langs', cell: (q) => 1 + Object.keys(q.translations ?? {}).length },
    { key: 'status', header: 'Status', cell: (q) => <StatusBadge map={QUESTION_STATUS} value={q.status} /> },
    { key: 'updated', header: 'Updated', cell: (q) => <span className="whitespace-nowrap text-muted">{formatDate(q.updatedAt)}</span> },
    {
      key: 'actions',
      header: 'Actions',
      srHeader: true,
      className: 'text-right',
      cell: (q) => (
        <div className="flex justify-end gap-0.5">
          <IconButton label={`View ${q.id}`} onClick={() => setViewing(q)}><Eye className="h-4 w-4" /></IconButton>
          <IconButton label={`Edit ${q.id}`} onClick={() => setEditing(q)}><Pencil className="h-4 w-4" /></IconButton>
          <IconButton label={`Approve ${q.id}`} tone="success" onClick={() => void approve(q)} disabled={q.status === 'verified'}><CircleCheck className="h-4 w-4" /></IconButton>
          <IconButton label={`Quarantine ${q.id}`} onClick={() => { setQuarantineReason(''); setQuarantine(q); }} disabled={q.status === 'quarantined'}><ShieldOff className="h-4 w-4" /></IconButton>
          <IconButton label={`Delete ${q.id}`} tone="danger" onClick={() => setToDelete(q)}><Trash2 className="h-4 w-4" /></IconButton>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-5">
      <PageHeader
        title="Question bank"
        description={`${questions.length} questions · ${counts.verified} verified, ${counts['pending-review']} pending review, ${counts.quarantined} quarantined, ${counts.rejected} rejected.`}
        actions={<Button leftIcon={<Plus className="h-4 w-4" />} onClick={() => setEditing(null)}>New question</Button>}
      />
      <AdminLoadGate state={load}>
        <FilterBar className="lg:grid-cols-5">
          <SearchInput value={search} onChange={setSearch} placeholder="Search text, topic or id" label="Search questions" />
          <Select aria-label="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} options={SUBJECTS} />
          <Select aria-label="Type" value={type} onChange={(e) => setType(e.target.value)} options={TYPES} />
          <Select aria-label="Difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)} options={DIFFS} />
          <Select aria-label="Status" value={status} onChange={(e) => setStatus(e.target.value)} options={STATUSES} />
        </FilterBar>
        <ResultCount count={rows.length} noun="question" onClear={filtered ? clear : undefined} />
        <DataTable
          caption="Question bank"
          columns={columns}
          rows={rows}
          rowKey={(q) => q.id}
          minWidth={1180}
          empty={
            <EmptyState
              icon={<BookOpenCheck className="h-6 w-6" />}
              title="No questions match"
              description="Try another search term or clear the filters."
              action={<Button variant="outline" onClick={clear}>Clear filters</Button>}
            />
          }
        />
      </AdminLoadGate>

      <Modal
        open={!!viewing}
        onOpenChange={(o) => !o && setViewing(null)}
        size="lg"
        title={viewing ? viewing.id : 'Question'}
        description={viewing ? `${SUBJECT_LABELS[viewing.subject]} · ${viewing.attemptCount.toLocaleString('en-IN')} attempts · ${viewing.accuracy}% accuracy · ${viewing.reportCount} reports` : undefined}
        footer={
          viewing && (
            <>
              <Button variant="outline" onClick={() => { setEditing(viewing); setViewing(null); }} leftIcon={<Pencil className="h-4 w-4" />}>Edit</Button>
              {viewing.status !== 'verified' && (
                <Button variant="success" onClick={() => { void approve(viewing); setViewing(null); }}>Approve</Button>
              )}
            </>
          )
        }
      >
        {viewing && (
          <div className="space-y-3">
            <StatusBadge map={QUESTION_STATUS} value={viewing.status} />
            <QuestionPreview question={viewing} />
          </div>
        )}
      </Modal>

      <QuestionFormModal open={editing !== undefined} onOpenChange={(o) => !o && setEditing(undefined)} question={editing ?? undefined} />

      <ConfirmationDialog
        open={!!quarantine}
        onOpenChange={(o) => !o && setQuarantine(null)}
        title="Quarantine this question?"
        description="Quarantined questions are never served in papers until a reviewer approves them again."
        confirmLabel="Quarantine"
        variant="danger"
        loading={busy}
        onConfirm={doQuarantine}
      >
        <Textarea label="Reason (for the audit log)" rows={2} value={quarantineReason} onChange={(e) => setQuarantineReason(e.target.value)} placeholder="e.g. Answer key disputed by subject expert" />
      </ConfirmationDialog>

      <ConfirmationDialog
        open={!!toDelete}
        onOpenChange={(o) => !o && setToDelete(null)}
        title="Delete this question?"
        description={toDelete ? `${toDelete.id} and its review items will be removed. Prefer quarantine if you might need it later.` : undefined}
        confirmLabel="Delete question"
        variant="danger"
        loading={busy}
        onConfirm={doDelete}
      />
    </div>
  );
}
