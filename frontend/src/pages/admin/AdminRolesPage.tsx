import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Controller, useFieldArray, useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { MessageSquare, Mic, Pencil, Plus, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import type { AdminRoleInput, ExperienceLevel, InterviewRole } from '@prepmitra/shared';
import { EXPERIENCE_LEVELS, adminRoleSchema, formatDateTime } from '@prepmitra/shared';
import {
  Badge, Button, Card, CardBody, CardFooter, CardHeader, ChoiceChip, ConfirmationDialog, EmptyState, Input, Modal, Notice, PageHeader,
  SearchInput, Select, Switch, Tabs, Textarea,
} from '@/components/ui';
import { AdminLoadGate, DataTable, FilterBar, IconButton, ResultCount, StatusBadge, ToggleSwitch, type Column } from '@/components/admin/AdminUi';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { PUBLISH_OPTIONS, PUBLISH_STATUS } from '@/components/admin/labels';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { useAdminStore } from '@/store/adminStore';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

type Tab = 'roles' | 'prompt' | 'rubric';
const levelLabel = (l: ExperienceLevel) => EXPERIENCE_LEVELS.find((x) => x.value === l)?.label ?? l;

export function AdminRolesPage() {
  useDocumentTitle('Interview roles');
  const load = useAdminLoad('roles');
  const [params, setParams] = useSearchParams();
  const raw = params.get('tab');
  const tab: Tab = raw === 'prompt' || raw === 'rubric' ? raw : 'roles';
  const roles = useAdminStore((s) => s.roles);

  return (
    <div className="space-y-5">
      <PageHeader title="Interview roles" description="Roles learners can practise, plus the interviewer prompt and scoring rubric shared by every role." />
      <AdminLoadGate state={load}>
        <Tabs
          ariaLabel="Interview settings"
          value={tab}
          onChange={(v) => setParams(v === 'roles' ? {} : { tab: v }, { replace: true })}
          items={[
            { value: 'roles', label: 'Roles', count: roles.length },
            { value: 'prompt', label: 'Interviewer prompt' },
            { value: 'rubric', label: 'Scoring rubric' },
          ]}
        />
        {tab === 'roles' ? <RolesTab /> : tab === 'prompt' ? <PromptTab /> : <RubricTab />}
      </AdminLoadGate>
    </div>
  );
}

// ---------- Roles ----------
function RolesTab() {
  const roles = useAdminStore((s) => s.roles);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('all');
  const [editing, setEditing] = useState<InterviewRole | null | undefined>(undefined);
  const [toDelete, setToDelete] = useState<InterviewRole | null>(null);
  const [busy, setBusy] = useState(false);
  const term = useDebounce(search).trim().toLowerCase();

  const rows = useMemo(
    () => roles.filter((r) => (status === 'all' || r.status === status) && (!term || `${r.title} ${r.category} ${r.themes.join(' ')}`.toLowerCase().includes(term))),
    [roles, status, term],
  );

  const togglePublish = async (r: InterviewRole) => {
    const next = r.status === 'published' ? 'draft' : 'published';
    try {
      await adminService.setRoleStatus(r.id, next);
      toast.success(next === 'published' ? `${r.shortTitle} is now live` : `${r.shortTitle} moved to draft`);
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  const doDelete = async () => {
    if (!toDelete) return;
    setBusy(true);
    try {
      await adminService.deleteRole(toDelete.id);
      toast.success(`Deleted ${toDelete.shortTitle}`);
      setToDelete(null);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  const columns: Column<InterviewRole>[] = [
    {
      key: 'title',
      header: 'Role',
      cell: (r) => (
        <div className="min-w-[180px]">
          <p className="font-medium">{r.title}</p>
          <p className="text-xs text-muted">{r.category}</p>
        </div>
      ),
    },
    { key: 'levels', header: 'Levels', cell: (r) => <span className="whitespace-nowrap">{r.levels.map(levelLabel).join(', ')}</span> },
    { key: 'format', header: 'Format', cell: (r) => <span className="whitespace-nowrap text-muted">{r.durationMin} min · {r.questionCount} Q</span> },
    {
      key: 'themes',
      header: 'Themes',
      cell: (r) => (
        <div className="flex max-w-[260px] flex-wrap gap-1">
          {r.themes.slice(0, 4).map((t) => <Badge key={t}>{t}</Badge>)}
          {r.themes.length > 4 && <Badge>+{r.themes.length - 4}</Badge>}
        </div>
      ),
    },
    { key: 'voice', header: 'Voice', cell: (r) => (r.voiceAvailable ? <Badge tone="success" icon={<Mic className="h-3 w-3" aria-hidden />}>Voice</Badge> : <span className="text-muted">Text only</span>) },
    { key: 'status', header: 'Status', cell: (r) => <StatusBadge map={PUBLISH_STATUS} value={r.status} /> },
    { key: 'live', header: 'Live', cell: (r) => <ToggleSwitch checked={r.status === 'published'} onChange={() => void togglePublish(r)} label={`Publish ${r.shortTitle}`} /> },
    {
      key: 'actions',
      header: 'Actions',
      srHeader: true,
      className: 'text-right',
      cell: (r) => (
        <div className="flex justify-end gap-0.5">
          <IconButton label={`Edit ${r.shortTitle}`} onClick={() => setEditing(r)}><Pencil className="h-4 w-4" /></IconButton>
          <IconButton label={`Delete ${r.shortTitle}`} tone="danger" onClick={() => setToDelete(r)}><Trash2 className="h-4 w-4" /></IconButton>
        </div>
      ),
    },
  ];

  return (
    <>
      <FilterBar>
        <SearchInput value={search} onChange={setSearch} placeholder="Search role, category or theme" label="Search roles" className="lg:col-span-2" />
        <Select aria-label="Status" value={status} onChange={(e) => setStatus(e.target.value)} options={[{ value: 'all', label: 'All statuses' }, ...PUBLISH_OPTIONS]} />
        <Button leftIcon={<Plus className="h-4 w-4" />} onClick={() => setEditing(null)}>New role</Button>
      </FilterBar>
      <ResultCount count={rows.length} noun="role" onClear={status !== 'all' || term ? () => { setSearch(''); setStatus('all'); } : undefined} />
      <DataTable
        caption="Interview roles"
        columns={columns}
        rows={rows}
        rowKey={(r) => r.id}
        minWidth={1000}
        empty={<EmptyState icon={<MessageSquare className="h-6 w-6" />} title="No roles found" description="Adjust the filters or create a new interview role." action={<Button onClick={() => setEditing(null)}>New role</Button>} />}
      />
      <RoleModal open={editing !== undefined} role={editing ?? undefined} onClose={() => setEditing(undefined)} />
      <ConfirmationDialog
        open={!!toDelete}
        onOpenChange={(o) => !o && setToDelete(null)}
        title="Delete this role?"
        description={toDelete ? `“${toDelete.title}” will no longer be available for new interviews.` : undefined}
        confirmLabel="Delete role"
        variant="danger"
        loading={busy}
        onConfirm={doDelete}
      />
    </>
  );
}

function RoleModal({ open, role, onClose }: { open: boolean; role?: InterviewRole; onClose: () => void }) {
  const toValues = (r?: InterviewRole): AdminRoleInput => ({
    title: r?.title ?? '', shortTitle: r?.shortTitle ?? '', category: r?.category ?? '', description: r?.description ?? '',
    levels: r?.levels ?? ['fresher'], durationMin: r?.durationMin ?? 20, questionCount: r?.questionCount ?? 8,
    themes: r?.themes.join(', ') ?? '', voiceAvailable: r?.voiceAvailable ?? true, status: r?.status ?? 'draft',
  });
  const { register, control, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<AdminRoleInput>({ resolver: zodResolver(adminRoleSchema), defaultValues: toValues(role) });
  useEffect(() => {
    if (open) reset(toValues(role));
  }, [open, role, reset]);

  const onSubmit = async (v: AdminRoleInput) => {
    try {
      const saved = await adminService.saveRole(v, role?.id);
      toast.success(role ? `Saved ${saved.shortTitle}` : `Created ${saved.shortTitle}`);
      onClose();
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <Modal
      open={open}
      onOpenChange={(o) => !o && onClose()}
      size="lg"
      title={role ? `Edit ${role.shortTitle}` : 'New interview role'}
      footer={
        <>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button type="submit" form="role-form" loading={isSubmitting}>{role ? 'Save role' : 'Create role'}</Button>
        </>
      }
    >
      <form id="role-form" onSubmit={handleSubmit(onSubmit)} noValidate className="grid gap-4 sm:grid-cols-2">
        <Input label="Title" required error={errors.title?.message} {...register('title')} placeholder="e.g. Data Analyst — Fresher" />
        <Input label="Short title" required error={errors.shortTitle?.message} {...register('shortTitle')} />
        <Input label="Category" required error={errors.category?.message} {...register('category')} placeholder="e.g. IT & Technology" />
        <Select label="Status" required options={PUBLISH_OPTIONS} {...register('status')} />
        <Textarea label="Description" required rows={3} containerClassName="sm:col-span-2" error={errors.description?.message} {...register('description')} />
        <Controller
          control={control}
          name="levels"
          render={({ field }) => (
            <fieldset className="sm:col-span-2">
              <legend className="mb-1.5 text-sm font-medium">Experience levels <span className="text-danger" aria-hidden>*</span></legend>
              <div className="flex flex-wrap gap-2">
                {EXPERIENCE_LEVELS.map((l) => (
                  <ChoiceChip
                    key={l.value}
                    selected={field.value.includes(l.value)}
                    onClick={() => field.onChange(field.value.includes(l.value) ? field.value.filter((x) => x !== l.value) : [...field.value, l.value])}
                  >
                    {l.label}
                  </ChoiceChip>
                ))}
              </div>
              {errors.levels?.message && <p role="alert" className="mt-1 text-xs font-medium text-danger">{errors.levels.message}</p>}
            </fieldset>
          )}
        />
        <Input label="Duration (min)" type="number" required hint="10–60" error={errors.durationMin?.message} {...register('durationMin', { valueAsNumber: true })} />
        <Input label="Question count" type="number" required hint="5–15" error={errors.questionCount?.message} {...register('questionCount', { valueAsNumber: true })} />
        <Input label="Themes" required containerClassName="sm:col-span-2" hint="Comma-separated, e.g. SQL, Excel, Dashboards" error={errors.themes?.message} {...register('themes')} />
        <div className="sm:col-span-2">
          <Controller control={control} name="voiceAvailable" render={({ field }) => (
            <Switch checked={field.value} onChange={field.onChange} label="Voice mode available" description="Requires voice support in the learner's language." />
          )} />
        </div>
      </form>
    </Modal>
  );
}

// ---------- Interviewer prompt ----------
const promptSchema = z.object({
  persona: z.string().trim().min(10, 'Describe the interviewer persona (10+ characters)').max(300),
  systemPrompt: z.string().trim().min(40, 'The prompt is too short (40+ characters)').max(3000, 'Keep under 3,000 characters'),
  tone: z.enum(['friendly', 'neutral', 'strict']),
  maxFollowUps: z.number({ message: 'Enter a number' }).int().min(0, 'Min 0').max(4, 'Max 4'),
});
type PromptValues = z.infer<typeof promptSchema>;

function PromptTab() {
  const config = useAdminStore((s) => s.interviewer);
  const { register, handleSubmit, reset, formState: { errors, isSubmitting, isDirty } } = useForm<PromptValues>({
    resolver: zodResolver(promptSchema),
    defaultValues: { persona: config.persona, systemPrompt: config.systemPrompt, tone: config.tone, maxFollowUps: config.maxFollowUps },
  });

  const onSubmit = async (v: PromptValues) => {
    try {
      await adminService.saveInterviewer({ ...config, ...v }, 'prompt');
      reset(v);
      toast.success('Interviewer prompt saved');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <Card>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <CardHeader title="Interviewer prompt" description={`Last updated ${formatDateTime(config.updatedAt)}`} />
        <CardBody className="space-y-4">
          <Notice tone="info">Placeholders <code>{'{{role}}'}</code>, <code>{'{{level}}'}</code>, <code>{'{{language}}'}</code> and <code>{'{{maxFollowUps}}'}</code> are filled by the backend. The prompt is never sent to the browser in production.</Notice>
          <Input label="Persona" required error={errors.persona?.message} {...register('persona')} />
          <Textarea label="System prompt" required rows={8} className="font-mono text-xs" error={errors.systemPrompt?.message} {...register('systemPrompt')} />
          <div className="grid gap-4 sm:grid-cols-2">
            <Select label="Tone" options={[{ value: 'friendly', label: 'Friendly' }, { value: 'neutral', label: 'Neutral' }, { value: 'strict', label: 'Strict (panel-style)' }]} {...register('tone')} />
            <Input label="Max follow-ups per question" type="number" required error={errors.maxFollowUps?.message} {...register('maxFollowUps', { valueAsNumber: true })} />
          </div>
        </CardBody>
        <CardFooter className="justify-end">
          <Button variant="outline" onClick={() => reset()} disabled={!isDirty}>Discard</Button>
          <Button type="submit" loading={isSubmitting} disabled={!isDirty}>Save prompt</Button>
        </CardFooter>
      </form>
    </Card>
  );
}

// ---------- Rubric ----------
const rubricSchema = z
  .object({
    rubric: z
      .array(
        z.object({
          id: z.string(),
          name: z.string().trim().min(2, 'Name required'),
          description: z.string().trim().min(5, 'Describe the criterion'),
          weight: z.number({ message: 'Enter a weight' }).int('Whole numbers only').min(1, 'Min 1').max(100, 'Max 100'),
        }),
      )
      .min(2, 'Add at least two criteria'),
  })
  .superRefine((v, ctx) => {
    const total = v.rubric.reduce((s, c) => s + (Number(c.weight) || 0), 0);
    if (total !== 100) ctx.addIssue({ code: 'custom', path: ['rubric'], message: `Weights must add up to 100% (currently ${total}%)` });
  });
type RubricValues = z.infer<typeof rubricSchema>;

function RubricTab() {
  const config = useAdminStore((s) => s.interviewer);
  const { register, control, handleSubmit, reset, formState: { errors, isSubmitting, isDirty } } = useForm<RubricValues>({
    resolver: zodResolver(rubricSchema),
    defaultValues: { rubric: config.rubric },
  });
  const { fields, append, remove } = useFieldArray({ control, name: 'rubric' });
  const watched = useWatch({ control, name: 'rubric' }) ?? [];
  const total = watched.reduce((s, c) => s + (Number(c?.weight) || 0), 0);
  const rubricError = errors.rubric?.root?.message ?? errors.rubric?.message;

  const onSubmit = async (v: RubricValues) => {
    try {
      await adminService.saveInterviewer({ ...config, rubric: v.rubric }, 'rubric');
      reset(v);
      toast.success('Scoring rubric saved');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <Card>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <CardHeader
          title="Scoring rubric"
          description="Applied to every interview report. Weights must total 100%."
          action={
            <span
              className={cn('rounded-full px-3 py-1 text-sm font-semibold', total === 100 ? 'bg-success-soft text-green-700' : 'bg-warning-soft text-warning-ink')}
              aria-live="polite"
            >
              Total {total}% {total === 100 ? '✓' : `(${total > 100 ? '−' : '+'}${Math.abs(100 - total)} needed)`}
            </span>
          }
        />
        <CardBody className="space-y-3">
          {fields.map((f, i) => {
            const e = errors.rubric?.[i];
            return (
              <div key={f.id} className="grid gap-3 rounded-xl border border-line p-3 sm:grid-cols-[1.2fr_2fr_110px_auto] sm:items-start">
                <input type="hidden" {...register(`rubric.${i}.id`)} />
                <Input label="Criterion" required error={e?.name?.message} {...register(`rubric.${i}.name`)} />
                <Input label="What it measures" required error={e?.description?.message} {...register(`rubric.${i}.description`)} />
                <Input label="Weight %" type="number" required error={e?.weight?.message} {...register(`rubric.${i}.weight`, { valueAsNumber: true })} />
                <div className="flex items-end sm:pt-7">
                  <Button variant="ghost" size="sm" className="text-danger hover:bg-danger-soft" onClick={() => remove(i)} disabled={fields.length <= 2} aria-label={`Remove criterion ${i + 1}`} leftIcon={<Trash2 className="h-4 w-4" />}>
                    <span className="sm:sr-only">Remove</span>
                  </Button>
                </div>
              </div>
            );
          })}
          {rubricError && <p role="alert" className="text-sm font-medium text-danger">{rubricError}</p>}
          <Button variant="secondary" size="sm" leftIcon={<Plus className="h-4 w-4" />} disabled={fields.length >= 8} onClick={() => append({ id: `rb-${Date.now().toString(36)}`, name: '', description: '', weight: 0 })}>
            Add criterion
          </Button>
        </CardBody>
        <CardFooter className="justify-end">
          <Button variant="outline" onClick={() => reset()} disabled={!isDirty}>Discard</Button>
          <Button type="submit" loading={isSubmitting} disabled={!isDirty}>Save rubric</Button>
        </CardFooter>
      </form>
    </Card>
  );
}
