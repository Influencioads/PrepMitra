import { useMemo, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Ban, Eye, RotateCcw, UserRound, Users } from 'lucide-react';
import toast from 'react-hot-toast';
import type { AdminCreditAdjustInput, AdminUserRecord } from '@prepmitra/shared';
import { adminCreditAdjustSchema, formatDate, formatDateTime, maskPhone, relativeTime } from '@prepmitra/shared';
import {
  Avatar, Badge, Button, ConfirmationDialog, EmptyState, Input, KeyValue, Modal, PageHeader, SearchInput, Select, Tabs, Textarea,
} from '@/components/ui';
import { AdminLoadGate, DataTable, FilterBar, IconButton, ResultCount, type Column } from '@/components/admin/AdminUi';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { PLAN_LABELS, planLabel, planTone, languageLabel } from '@/components/admin/labels';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { useAdminStore } from '@/store/adminStore';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

const PLAN_FILTER = [{ value: 'all', label: 'All plans' }, ...Object.entries(PLAN_LABELS).map(([value, label]) => ({ value, label }))];
const STATUS_FILTER = [{ value: 'all', label: 'All statuses' }, { value: 'active', label: 'Active' }, { value: 'blocked', label: 'Blocked' }];
const SORTS = [{ value: 'joined', label: 'Newest first' }, { value: 'attempts', label: 'Most attempts' }, { value: 'credits', label: 'Most credits' }, { value: 'name', label: 'Name A–Z' }];

export function AdminUsersPage() {
  useDocumentTitle('Users');
  const load = useAdminLoad('users');
  const users = useAdminStore((s) => s.users);
  const [search, setSearch] = useState('');
  const [plan, setPlan] = useState('all');
  const [status, setStatus] = useState('all');
  const [sort, setSort] = useState('joined');
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [blocking, setBlocking] = useState<AdminUserRecord | null>(null);
  const term = useDebounce(search).trim().toLowerCase();
  const selected = users.find((u) => u.id === selectedId) ?? null;

  const rows = useMemo(() => {
    const r = users.filter(
      (u) =>
        (plan === 'all' || u.planId === plan) &&
        (status === 'all' || u.status === status) &&
        (!term || `${u.name} ${u.phone} ${u.email ?? ''} ${u.id} ${u.state}`.toLowerCase().includes(term)),
    );
    const sorters: Record<string, (a: AdminUserRecord, b: AdminUserRecord) => number> = {
      joined: (a, b) => b.joinedAt.localeCompare(a.joinedAt),
      attempts: (a, b) => b.attempts.length - a.attempts.length,
      credits: (a, b) => b.credits - a.credits,
      name: (a, b) => a.name.localeCompare(b.name),
    };
    return r.sort(sorters[sort]);
  }, [users, plan, status, sort, term]);
  const filtered = plan !== 'all' || status !== 'all' || !!term;

  const columns: Column<AdminUserRecord>[] = [
    {
      key: 'user',
      header: 'User',
      cell: (u) => (
        <button type="button" onClick={() => setSelectedId(u.id)} className="flex min-w-[200px] items-center gap-3 text-left">
          <Avatar name={u.name} size="sm" />
          <span className="min-w-0">
            <span className="block font-medium text-ink hover:text-primary">{u.name}</span>
            <span className="block truncate text-xs text-muted">{u.email ?? maskPhone(u.phone)}</span>
          </span>
        </button>
      ),
    },
    { key: 'state', header: 'State', cell: (u) => <span className="whitespace-nowrap">{u.state}</span> },
    { key: 'plan', header: 'Plan', cell: (u) => <Badge tone={planTone(u.planId)}>{planLabel(u.planId)}</Badge> },
    { key: 'attempts', header: 'Attempts', cell: (u) => u.attempts.length },
    { key: 'credits', header: 'Credits', cell: (u) => <span className="font-semibold">{u.credits}</span> },
    { key: 'joined', header: 'Joined', cell: (u) => <span className="whitespace-nowrap text-muted">{formatDate(u.joinedAt)}</span> },
    { key: 'status', header: 'Status', cell: (u) => <Badge tone={u.status === 'active' ? 'success' : 'danger'}>{u.status === 'active' ? 'Active' : 'Blocked'}</Badge> },
    {
      key: 'actions',
      header: 'Actions',
      srHeader: true,
      className: 'text-right',
      cell: (u) => (
        <div className="flex justify-end gap-0.5">
          <IconButton label={`View ${u.name}`} onClick={() => setSelectedId(u.id)}><Eye className="h-4 w-4" /></IconButton>
          <IconButton label={u.status === 'active' ? `Block ${u.name}` : `Unblock ${u.name}`} tone={u.status === 'active' ? 'danger' : 'success'} onClick={() => setBlocking(u)}>
            {u.status === 'active' ? <Ban className="h-4 w-4" /> : <RotateCcw className="h-4 w-4" />}
          </IconButton>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-5">
      <PageHeader
        title="Users"
        description={`${users.length} learners · ${users.filter((u) => u.planId !== 'free').length} paid · ${users.filter((u) => u.status === 'blocked').length} blocked. Personal data is masked where possible (DPDP).`}
      />
      <AdminLoadGate state={load}>
        <FilterBar>
          <SearchInput value={search} onChange={setSearch} placeholder="Name, phone, email or state" label="Search users" />
          <Select aria-label="Status" value={status} onChange={(e) => setStatus(e.target.value)} options={STATUS_FILTER} />
          <Select aria-label="Plan" value={plan} onChange={(e) => setPlan(e.target.value)} options={PLAN_FILTER} />
          <Select aria-label="Sort" value={sort} onChange={(e) => setSort(e.target.value)} options={SORTS} />
        </FilterBar>
        <ResultCount count={rows.length} noun="user" onClear={filtered ? () => { setSearch(''); setPlan('all'); setStatus('all'); } : undefined} />
        <DataTable
          caption="Users"
          columns={columns}
          rows={rows}
          rowKey={(u) => u.id}
          minWidth={900}
          rowClassName={(u) => (u.status === 'blocked' ? 'bg-danger-soft/40' : undefined)}
          empty={<EmptyState icon={<Users className="h-6 w-6" />} title="No users match" description="Try another search or clear the filters." />}
        />
      </AdminLoadGate>

      {selected && <UserDetailModal user={selected} onClose={() => setSelectedId(null)} onBlock={() => setBlocking(selected)} />}
      <BlockDialog user={blocking} onClose={() => setBlocking(null)} />
    </div>
  );
}

function BlockDialog({ user, onClose }: { user: AdminUserRecord | null; onClose: () => void }) {
  const [reason, setReason] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const blocking = user?.status === 'active';

  const confirm = async () => {
    if (!user) return;
    if (blocking && reason.trim().length < 5) {
      setError('Give a reason for the audit log (5+ characters)');
      return;
    }
    setBusy(true);
    try {
      await adminService.setUserStatus(user.id, blocking ? 'blocked' : 'active', reason.trim() || undefined);
      toast.success(blocking ? `${user.name} has been blocked` : `${user.name} has been unblocked`);
      setReason('');
      setError(null);
      onClose();
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <ConfirmationDialog
      open={!!user}
      onOpenChange={(o) => {
        if (!o) {
          setReason('');
          setError(null);
          onClose();
        }
      }}
      title={blocking ? `Block ${user?.name}?` : `Unblock ${user?.name}?`}
      description={blocking ? 'They will be signed out and cannot start exams or interviews. Credits are kept.' : 'They will be able to sign in and use their remaining credits again.'}
      confirmLabel={blocking ? 'Block user' : 'Unblock user'}
      variant={blocking ? 'danger' : 'primary'}
      loading={busy}
      onConfirm={confirm}
    >
      <Textarea
        label={blocking ? 'Reason' : 'Note (optional)'}
        required={blocking}
        rows={2}
        value={reason}
        error={error ?? undefined}
        onChange={(e) => {
          setReason(e.target.value);
          setError(null);
        }}
        placeholder={blocking ? 'e.g. Sharing paid account credentials' : ''}
      />
    </ConfirmationDialog>
  );
}

type DetailTab = 'attempts' | 'ledger' | 'credits';

function UserDetailModal({ user, onClose, onBlock }: { user: AdminUserRecord; onClose: () => void; onBlock: () => void }) {
  const [tab, setTab] = useState<DetailTab>('attempts');
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<AdminCreditAdjustInput>({
    resolver: zodResolver(adminCreditAdjustSchema),
    defaultValues: { delta: 1, reason: '' },
  });

  const onAdjust = async (v: AdminCreditAdjustInput) => {
    try {
      await adminService.adjustCredits(user.id, v.delta, v.reason.trim());
      toast.success(v.delta > 0 ? `Added ${v.delta} credit${v.delta > 1 ? 's' : ''} to ${user.name}` : `Removed ${-v.delta} credit${v.delta < -1 ? 's' : ''} from ${user.name}`);
      reset({ delta: 1, reason: '' });
      setTab('ledger');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <Modal
      open
      onOpenChange={(o) => !o && onClose()}
      size="xl"
      title={
        <span className="flex items-center gap-3">
          <Avatar name={user.name} size="sm" /> {user.name}
        </span>
      }
      description={`${user.id} · joined ${formatDate(user.joinedAt)} · last active ${relativeTime(user.lastActiveAt)}`}
      footer={
        <>
          <Button variant={user.status === 'active' ? 'danger' : 'success'} onClick={onBlock} leftIcon={user.status === 'active' ? <Ban className="h-4 w-4" /> : <RotateCcw className="h-4 w-4" />}>
            {user.status === 'active' ? 'Block user' : 'Unblock user'}
          </Button>
          <Button variant="outline" onClick={onClose}>Close</Button>
        </>
      }
    >
      <div className="grid gap-6 md:grid-cols-[240px_1fr]">
        <dl className="divide-y divide-line rounded-xl border border-line px-4">
          <KeyValue label="Status" value={<Badge tone={user.status === 'active' ? 'success' : 'danger'}>{user.status === 'active' ? 'Active' : 'Blocked'}</Badge>} />
          <KeyValue label="Plan" value={<Badge tone={planTone(user.planId)}>{planLabel(user.planId)}</Badge>} />
          <KeyValue label="Credits" value={user.credits} />
          <KeyValue label="Attempts" value={user.attempts.length} />
          <KeyValue label="Phone" value={maskPhone(user.phone)} />
          <KeyValue label="Email" value={<span className="break-all">{user.email ?? '—'}</span>} />
          <KeyValue label="State" value={user.state} />
          <KeyValue label="Language" value={languageLabel(user.preferredLanguage)} />
        </dl>
        <div className="min-w-0 space-y-4">
          <Tabs
            ariaLabel="User details"
            value={tab}
            onChange={setTab}
            items={[
              { value: 'attempts', label: 'Attempts', count: user.attempts.length },
              { value: 'ledger', label: 'Credit ledger', count: user.ledger.length },
              { value: 'credits', label: 'Add / restore credits' },
            ]}
          />
          {tab === 'attempts' &&
            (user.attempts.length === 0 ? (
              <EmptyState icon={<UserRound className="h-6 w-6" />} title="No attempts yet" description="This learner has not completed a mock exam or interview." />
            ) : (
              <ul className="divide-y divide-line rounded-xl border border-line">
                {user.attempts.map((a) => (
                  <li key={a.id} className="flex items-center justify-between gap-3 px-4 py-3 text-sm">
                    <div className="min-w-0">
                      <p className="font-medium">{a.title}</p>
                      <p className="text-xs text-muted">{a.kind === 'exam' ? 'Mock exam' : 'Mock interview'} · {formatDateTime(a.at)}</p>
                    </div>
                    <Badge tone={a.score >= 75 ? 'success' : a.score >= 50 ? 'warning' : 'danger'}>{a.score}%</Badge>
                  </li>
                ))}
              </ul>
            ))}
          {tab === 'ledger' &&
            (user.ledger.length === 0 ? (
              <EmptyState title="No credit activity" />
            ) : (
              <ul className="divide-y divide-line rounded-xl border border-line">
                {user.ledger.map((l) => (
                  <li key={l.id} className="flex items-center justify-between gap-3 px-4 py-3 text-sm">
                    <div className="min-w-0">
                      <p className="font-medium">{l.label}</p>
                      <p className="text-xs text-muted">{l.reason} · {formatDateTime(l.at)}</p>
                    </div>
                    <span className={cn('font-semibold tabular-nums', l.delta > 0 ? 'text-green-700' : l.delta < 0 ? 'text-red-700' : 'text-muted')}>
                      {l.delta > 0 ? '+' : ''}{l.delta}
                    </span>
                  </li>
                ))}
              </ul>
            ))}
          {tab === 'credits' && (
            <form onSubmit={handleSubmit(onAdjust)} noValidate className="space-y-4 rounded-xl border border-line p-4">
              <p className="text-sm text-muted">Use a negative number to remove credits. Every adjustment is written to the audit log with your name and reason.</p>
              <Input label="Credits (+/−)" type="number" required hint="Between −50 and 50" error={errors.delta?.message} {...register('delta', { valueAsNumber: true })} />
              <Textarea label="Reason" required rows={2} error={errors.reason?.message} placeholder="e.g. Exam paper failed to load — restoring credit" {...register('reason')} />
              <div className="flex justify-end">
                <Button type="submit" loading={isSubmitting}>Apply adjustment</Button>
              </div>
            </form>
          )}
        </div>
      </div>
    </Modal>
  );
}
