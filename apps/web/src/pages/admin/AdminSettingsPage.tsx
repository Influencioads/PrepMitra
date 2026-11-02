import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Download, History, Pencil, RotateCcw, Trash2, UserPlus } from 'lucide-react';
import toast from 'react-hot-toast';
import type { AdminTeamMember, AdminTeamRole, PermissionLevel, PlanConfig } from '@prepmitra/shared';
import { ADMIN_MODULES, ADMIN_PERMISSIONS, ADMIN_TEAM_ROLES, PLANS, formatDateTime, relativeTime } from '@prepmitra/shared';
import {
  Badge, Button, Card, CardBody, CardFooter, CardHeader, ChoiceChip, ConfirmationDialog, EmptyState, Input, Modal, Notice, PageHeader,
  SearchInput, Select, Switch, Tabs, type BadgeTone,
} from '@/components/ui';
import { AdminLoadGate, DataTable, FilterBar, IconButton, ResultCount, ToggleSwitch, type Column } from '@/components/admin/AdminUi';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { downloadFile, toCsv, todayStamp } from '@/components/admin/download';
import { MODULE_LABELS, TEAM_ROLE_LABELS, languageLabel } from '@/components/admin/labels';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { useAdminStore } from '@/store/adminStore';
import { useAuthStore } from '@/store';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

type Tab = 'team' | 'pricing' | 'flags' | 'audit';
const TABS: Tab[] = ['team', 'pricing', 'flags', 'audit'];

export function AdminSettingsPage() {
  useDocumentTitle('Admin settings');
  const load = useAdminLoad('settings');
  const [params, setParams] = useSearchParams();
  const raw = params.get('tab') as Tab | null;
  const tab: Tab = raw && TABS.includes(raw) ? raw : 'team';
  const auditCount = useAdminStore((s) => s.auditLog.length);

  return (
    <div className="space-y-5">
      <PageHeader title="Settings" description="Team access, pricing, feature flags and the audit trail." />
      <AdminLoadGate state={load}>
        <Tabs
          ariaLabel="Settings sections"
          value={tab}
          onChange={(v) => setParams(v === 'team' ? {} : { tab: v }, { replace: true })}
          items={[
            { value: 'team', label: 'Team & roles' },
            { value: 'pricing', label: 'Pricing' },
            { value: 'flags', label: 'Feature flags' },
            { value: 'audit', label: 'Audit log', count: auditCount },
          ]}
        />
        {tab === 'team' && <TeamTab />}
        {tab === 'pricing' && <PricingTab />}
        {tab === 'flags' && <FlagsTab />}
        {tab === 'audit' && <AuditTab />}
      </AdminLoadGate>
    </div>
  );
}

// ---------- Team ----------
const LEVEL: Record<PermissionLevel, { label: string; tone: BadgeTone }> = {
  full: { label: 'Full', tone: 'success' },
  edit: { label: 'Edit', tone: 'primary' },
  view: { label: 'View', tone: 'neutral' },
  none: { label: '—', tone: 'neutral' },
};
const ROLE_OPTIONS = ADMIN_TEAM_ROLES.map((r) => ({ value: r.id, label: r.label }));
const TEAM_LANGS = ['en', 'hi', 'bn', 'mr', 'te', 'ta', 'gu', 'kn', 'ml', 'or', 'pa', 'ur', 'as'] as const;

const memberSchema = z.object({
  name: z.string().trim().min(2, 'Enter a name'),
  email: z.email('Enter a valid work email'),
  role: z.enum(['founder', 'content-manager', 'subject-expert', 'language-reviewer', 'support', 'finance']),
  languages: z.array(z.string()).min(1, 'Pick at least one language'),
});
type MemberValues = z.infer<typeof memberSchema>;

function TeamTab() {
  const team = useAdminStore((s) => s.team);
  const myEmail = useAuthStore((s) => s.session?.user.email);
  const [editing, setEditing] = useState<AdminTeamMember | null | undefined>(undefined);
  const [removing, setRemoving] = useState<AdminTeamMember | null>(null);
  const [busy, setBusy] = useState(false);

  const setActive = async (m: AdminTeamMember, v: boolean) => {
    try {
      await adminService.setMemberActive(m.id, v);
      toast.success(`${m.name} ${v ? 'reactivated' : 'deactivated'}`);
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };
  const remove = async () => {
    if (!removing) return;
    setBusy(true);
    try {
      await adminService.removeMember(removing.id);
      toast.success(`${removing.name} removed from the team`);
      setRemoving(null);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  const columns: Column<AdminTeamMember>[] = [
    { key: 'name', header: 'Member', cell: (m) => <div><p className="font-medium">{m.name}</p><p className="text-xs text-muted">{m.email}</p></div> },
    { key: 'role', header: 'Role', cell: (m) => <Badge tone="primary">{TEAM_ROLE_LABELS[m.role]}</Badge> },
    { key: 'langs', header: 'Languages', cell: (m) => <span className="text-muted">{m.languages.map(languageLabel).join(', ')}</span> },
    { key: 'last', header: 'Last active', cell: (m) => <span className="whitespace-nowrap text-muted">{relativeTime(m.lastActiveAt)}</span> },
    {
      key: 'active',
      header: 'Active',
      cell: (m) => <ToggleSwitch checked={m.active} disabled={m.email === myEmail} onChange={(v) => void setActive(m, v)} label={m.email === myEmail ? 'You cannot deactivate yourself' : `${m.name} active`} />,
    },
    {
      key: 'actions',
      header: 'Actions',
      srHeader: true,
      className: 'text-right',
      cell: (m) => (
        <div className="flex justify-end gap-0.5">
          <IconButton label={`Edit ${m.name}`} onClick={() => setEditing(m)}><Pencil className="h-4 w-4" /></IconButton>
          <IconButton label={`Remove ${m.name}`} tone="danger" disabled={m.email === myEmail} onClick={() => setRemoving(m)}><Trash2 className="h-4 w-4" /></IconButton>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <section className="space-y-3" aria-labelledby="team-heading">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 id="team-heading" className="text-lg font-semibold">Admin team</h2>
          <Button leftIcon={<UserPlus className="h-4 w-4" />} onClick={() => setEditing(null)}>Invite member</Button>
        </div>
        <DataTable caption="Admin team" columns={columns} rows={team} rowKey={(m) => m.id} minWidth={820} empty={<EmptyState title="No team members" />} />
      </section>

      <section className="space-y-3" aria-labelledby="perm-heading">
        <h2 id="perm-heading" className="text-lg font-semibold">Role permissions</h2>
        <Notice tone="info">This matrix documents intended access. It must be enforced server-side on every <code>/v1/admin/*</code> request; the UI does not restrict anything in this demo.</Notice>
        <DataTable
          caption="Role permission matrix"
          minWidth={1100}
          rows={ADMIN_TEAM_ROLES}
          rowKey={(r) => r.id}
          columns={[
            {
              key: 'role',
              header: 'Role',
              className: 'sticky left-0 bg-card',
              cell: (r) => (
                <div className="min-w-[160px]">
                  <p className="font-medium">{r.label}</p>
                  <p className="text-xs text-muted">{r.description}</p>
                </div>
              ),
            },
            ...ADMIN_MODULES.map((m) => ({
              key: m.id,
              header: m.label,
              cell: (r: (typeof ADMIN_TEAM_ROLES)[number]) => {
                const lvl = ADMIN_PERMISSIONS[r.id as AdminTeamRole][m.id];
                return lvl === 'none' ? <span className="text-subtle" aria-label="No access">—</span> : <Badge tone={LEVEL[lvl].tone}>{LEVEL[lvl].label}</Badge>;
              },
            })),
          ]}
        />
      </section>

      <MemberModal open={editing !== undefined} member={editing ?? undefined} onClose={() => setEditing(undefined)} />
      <ConfirmationDialog
        open={!!removing}
        onOpenChange={(o) => !o && setRemoving(null)}
        title="Remove team member?"
        description={removing ? `${removing.name} will lose access to the admin console immediately.` : undefined}
        confirmLabel="Remove"
        variant="danger"
        loading={busy}
        onConfirm={remove}
      />
    </div>
  );
}

function MemberModal({ open, member, onClose }: { open: boolean; member?: AdminTeamMember; onClose: () => void }) {
  const team = useAdminStore((s) => s.team);
  const toValues = (m?: AdminTeamMember): MemberValues => ({ name: m?.name ?? '', email: m?.email ?? '', role: m?.role ?? 'subject-expert', languages: m?.languages ?? ['en'] });
  const { register, control, handleSubmit, reset, setError, formState: { errors, isSubmitting } } = useForm<MemberValues>({ resolver: zodResolver(memberSchema), defaultValues: toValues(member) });
  useEffect(() => {
    if (open) reset(toValues(member));
  }, [open, member, reset]);

  const onSubmit = async (v: MemberValues) => {
    if (team.some((m) => m.id !== member?.id && m.email.toLowerCase() === v.email.trim().toLowerCase())) {
      setError('email', { message: 'This email is already on the team' });
      return;
    }
    try {
      await adminService.saveMember({ ...v, languages: v.languages as AdminTeamMember['languages'] }, member?.id);
      toast.success(member ? `Updated ${v.name}` : `Invitation sent to ${v.email} (demo)`);
      onClose();
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <Modal
      open={open}
      onOpenChange={(o) => !o && onClose()}
      title={member ? `Edit ${member.name}` : 'Invite team member'}
      description={member ? undefined : 'In production an email invite is sent and the account is created on first sign-in.'}
      footer={
        <>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button type="submit" form="member-form" loading={isSubmitting}>{member ? 'Save member' : 'Send invite'}</Button>
        </>
      }
    >
      <form id="member-form" onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
        <Input label="Full name" required error={errors.name?.message} {...register('name')} />
        <Input label="Work email" type="email" required error={errors.email?.message} {...register('email')} />
        <Select label="Role" required options={ROLE_OPTIONS} error={errors.role?.message} {...register('role')} />
        <Controller
          control={control}
          name="languages"
          render={({ field }) => (
            <fieldset>
              <legend className="mb-1.5 text-sm font-medium">Languages <span className="text-danger" aria-hidden>*</span></legend>
              <div className="flex flex-wrap gap-2">
                {TEAM_LANGS.map((code) => (
                  <ChoiceChip key={code} selected={field.value.includes(code)} onClick={() => field.onChange(field.value.includes(code) ? field.value.filter((c) => c !== code) : [...field.value, code])}>
                    {languageLabel(code)}
                  </ChoiceChip>
                ))}
              </div>
              {errors.languages?.message && <p role="alert" className="mt-1 text-xs font-medium text-danger">{errors.languages.message}</p>}
            </fieldset>
          )}
        />
      </form>
    </Modal>
  );
}

// ---------- Pricing ----------
const planSchema = z.object({
  priceInr: z.number({ message: 'Enter a price' }).int('Whole rupees only').min(0, 'Cannot be negative').max(100000, 'Too high'),
  credits: z.number({ message: 'Enter credits' }).int().min(1, 'At least 1').max(1000, 'At most 1000'),
  validityDays: z.string().trim().refine((v) => v === '' || (/^\d+$/.test(v) && Number(v) >= 1 && Number(v) <= 730), 'Leave empty for no expiry, or 1–730 days'),
  active: z.boolean(),
});
type PlanValues = z.infer<typeof planSchema>;

function PricingTab() {
  const plans = useAdminStore((s) => s.settings.plans);
  return (
    <div className="space-y-4">
      <Notice tone="warning" title="Backend is the source of truth">
        These values are saved in the demo admin store only. In production, pricing is served by <code>GET /v1/plans</code> and changed via <code>PATCH /v1/admin/plans/:id</code>; the learner app reads <code>PLANS</code> until that API is connected. Prices include 18% GST.
      </Notice>
      <div className="grid gap-4 md:grid-cols-2">
        {plans.map((p) => <PlanCard key={p.id} plan={p} />)}
      </div>
    </div>
  );
}

function PlanCard({ plan }: { plan: PlanConfig }) {
  const meta = PLANS.find((p) => p.id === plan.id);
  const toValues = (p: PlanConfig): PlanValues => ({ priceInr: p.priceInr, credits: p.credits, validityDays: p.validityDays === null ? '' : String(p.validityDays), active: p.active });
  const { register, control, handleSubmit, reset, formState: { errors, isSubmitting, isDirty } } = useForm<PlanValues>({ resolver: zodResolver(planSchema), defaultValues: toValues(plan) });
  const isFree = plan.id === 'free';

  const onSubmit = async (v: PlanValues) => {
    try {
      const patch = { priceInr: isFree ? 0 : v.priceInr, credits: v.credits, validityDays: v.validityDays === '' ? null : Number(v.validityDays), active: v.active };
      await adminService.updatePlan(plan.id, patch);
      reset(toValues({ ...plan, ...patch }));
      toast.success(`${meta?.name ?? plan.id} pricing saved`);
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };
  const changed = meta && (meta.priceInr !== plan.priceInr || meta.credits !== plan.credits || meta.validityDays !== plan.validityDays);

  return (
    <Card>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <CardHeader
          title={meta?.name ?? plan.id}
          description={meta?.description}
          action={changed ? <Badge tone="warning">Differs from default</Badge> : <Badge>Default</Badge>}
        />
        <CardBody className="grid gap-4 sm:grid-cols-3">
          <Input label="Price (₹)" type="number" disabled={isFree} hint={isFree ? 'Always free' : 'GST inclusive'} error={errors.priceInr?.message} {...register('priceInr', { valueAsNumber: true })} />
          <Input label="Credits" type="number" error={errors.credits?.message} {...register('credits', { valueAsNumber: true })} />
          <Input label="Validity (days)" inputMode="numeric" placeholder="No expiry" error={errors.validityDays?.message} {...register('validityDays')} />
          <div className="sm:col-span-3">
            <Controller control={control} name="active" render={({ field }) => (
              <Switch checked={field.value} onChange={field.onChange} label="Available for purchase" description={isFree ? 'Turning off hides the free mini mock for new users.' : 'Hidden plans keep existing subscribers.'} />
            )} />
          </div>
        </CardBody>
        <CardFooter className="justify-end">
          <Button variant="outline" size="sm" onClick={() => reset()} disabled={!isDirty}>Discard</Button>
          <Button type="submit" size="sm" loading={isSubmitting} disabled={!isDirty}>Save</Button>
        </CardFooter>
      </form>
    </Card>
  );
}

// ---------- Feature flags ----------
const flagsSchema = z.object({
  voiceInterviews: z.boolean(),
  tabSwitchLogging: z.boolean(),
  autoQuarantine: z.boolean(),
  autoQuarantineThreshold: z.number({ message: 'Enter a number' }).int().min(2, 'At least 2 reports').max(10, 'At most 10 reports'),
  reviewSampleRate: z.number({ message: 'Enter a number' }).int().min(1, 'At least 1%').max(100, 'At most 100%'),
});
type FlagValues = z.infer<typeof flagsSchema>;

function FlagsTab() {
  const flags = useAdminStore((s) => s.settings.featureFlags);
  const simulate = useAdminStore((s) => s.settings.simulateLoadError);
  const [resetOpen, setResetOpen] = useState(false);
  const { register, control, handleSubmit, reset, formState: { errors, isSubmitting, isDirty } } = useForm<FlagValues>({ resolver: zodResolver(flagsSchema), defaultValues: flags });

  const onSubmit = async (v: FlagValues) => {
    const patch = Object.fromEntries(Object.entries(v).filter(([k, val]) => flags[k as keyof FlagValues] !== val)) as Partial<FlagValues>;
    try {
      await adminService.updateFlags(patch);
      reset(v);
      toast.success('Feature flags saved');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  const resetDemo = () => {
    useAdminStore.getState().resetDemoData();
    setResetOpen(false);
    toast.success('Admin demo data reset');
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[3fr_2fr]">
      <Card>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <CardHeader title="Feature flags" description="Changes apply to new sessions." />
          <CardBody className="divide-y divide-line py-2">
            <Controller control={control} name="voiceInterviews" render={({ field }) => (
              <Switch checked={field.value} onChange={field.onChange} label="Voice interviews" description="Speech-to-text and text-to-speech for languages with voice support." />
            )} />
            <Controller control={control} name="tabSwitchLogging" render={({ field }) => (
              <Switch checked={field.value} onChange={field.onChange} label="Anti-cheat: log tab switches" description="Records when a learner leaves the exam tab. Shown in reports; never auto-fails an attempt." />
            )} />
            <Controller control={control} name="autoQuarantine" render={({ field }) => (
              <Switch checked={field.value} onChange={field.onChange} label="Auto-quarantine reported questions" description="Pull a question from papers once it reaches the report threshold." />
            )} />
            <div className="grid gap-4 py-4 sm:grid-cols-2">
              <Input label="Auto-quarantine threshold" type="number" hint="Independent reports (default 3)" error={errors.autoQuarantineThreshold?.message} {...register('autoQuarantineThreshold', { valueAsNumber: true })} />
              <Input label="Review sample rate (%)" type="number" hint="Share of new questions sent to humans (default 10%)" error={errors.reviewSampleRate?.message} {...register('reviewSampleRate', { valueAsNumber: true })} />
            </div>
          </CardBody>
          <CardFooter className="justify-end">
            <Button variant="outline" onClick={() => reset()} disabled={!isDirty}>Discard</Button>
            <Button type="submit" loading={isSubmitting} disabled={!isDirty}>Save flags</Button>
          </CardFooter>
        </form>
      </Card>

      <Card className="h-fit">
        <CardHeader title="Demo tools" description="Only exist in the prototype." />
        <CardBody className="space-y-2">
          <Switch
            checked={simulate}
            onChange={(v) => {
              useAdminStore.getState().setSimulateLoadError(v);
              toast.success(v ? 'The next admin data load will fail — use “Try again” to recover' : 'Load errors switched off');
            }}
            label="Simulate a load error"
            description="Makes the next first-time page load fail so you can check error states. Reload the browser to re-trigger loading."
          />
          <div className="pt-2">
            <Button variant="outline" leftIcon={<RotateCcw className="h-4 w-4" />} onClick={() => setResetOpen(true)}>Reset admin demo data</Button>
          </div>
        </CardBody>
      </Card>

      <ConfirmationDialog
        open={resetOpen}
        onOpenChange={setResetOpen}
        title="Reset admin demo data?"
        description="Exams, questions, users, orders, lessons and settings return to the seeded demo state. Learner data is not affected."
        confirmLabel="Reset"
        variant="danger"
        onConfirm={resetDemo}
      />
    </div>
  );
}

// ---------- Audit log ----------
function AuditTab() {
  const log = useAdminStore((s) => s.auditLog);
  const [search, setSearch] = useState('');
  const [module, setModule] = useState('all');
  const [actor, setActor] = useState('all');
  const term = useDebounce(search).trim().toLowerCase();
  const actors = useMemo(() => [...new Set(log.map((l) => l.actor))].sort(), [log]);
  const rows = useMemo(
    () =>
      log.filter(
        (l) =>
          (module === 'all' || l.module === module) &&
          (actor === 'all' || l.actor === actor) &&
          (!term || `${l.action} ${l.target} ${l.details ?? ''}`.toLowerCase().includes(term)),
      ),
    [log, module, actor, term],
  );

  const exportCsv = () => {
    downloadFile(
      `prepmitra-audit-log-${todayStamp()}.csv`,
      toCsv(['Time (ISO)', 'Actor', 'Module', 'Action', 'Target', 'Details'], rows.map((l) => [l.at, l.actor, MODULE_LABELS[l.module] ?? l.module, l.action, l.target, l.details ?? ''])),
      'text/csv',
    );
    toast.success(`Exported ${rows.length} audit entries`);
  };

  return (
    <div className="space-y-4">
      <FilterBar>
        <SearchInput value={search} onChange={setSearch} placeholder="Search action, target or details" label="Search audit log" className="lg:col-span-2" />
        <Select aria-label="Module" value={module} onChange={(e) => setModule(e.target.value)} options={[{ value: 'all', label: 'All modules' }, ...ADMIN_MODULES.map((m) => ({ value: m.id, label: m.label }))]} />
        <Select aria-label="Actor" value={actor} onChange={(e) => setActor(e.target.value)} options={[{ value: 'all', label: 'All people' }, ...actors.map((a) => ({ value: a, label: a }))]} />
      </FilterBar>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <ResultCount count={rows.length} noun="entry" onClear={module !== 'all' || actor !== 'all' || term ? () => { setSearch(''); setModule('all'); setActor('all'); } : undefined} />
        <Button size="sm" variant="outline" leftIcon={<Download className="h-4 w-4" />} onClick={exportCsv} disabled={rows.length === 0}>Export CSV</Button>
      </div>
      <DataTable
        caption="Audit log"
        minWidth={860}
        rows={rows}
        rowKey={(l) => l.id}
        empty={<EmptyState icon={<History className="h-6 w-6" />} title="No audit entries match" description="Every create, update and delete in the console is recorded here." />}
        columns={[
          { key: 'at', header: 'When', cell: (l) => <time dateTime={l.at} className="whitespace-nowrap text-muted" title={formatDateTime(l.at)}>{relativeTime(l.at)}</time> },
          { key: 'actor', header: 'Actor', cell: (l) => <span className="whitespace-nowrap font-medium">{l.actor}</span> },
          { key: 'action', header: 'Action', cell: (l) => l.action },
          { key: 'target', header: 'Target', cell: (l) => <span className="font-medium">{l.target}</span> },
          { key: 'details', header: 'Details', cell: (l) => <span className="text-muted">{l.details ?? '—'}</span> },
          { key: 'module', header: 'Module', cell: (l) => <Badge>{MODULE_LABELS[l.module] ?? l.module}</Badge> },
        ]}
      />
      <p className="text-xs text-muted">The demo keeps the latest 300 entries in this browser. Production audit logs are append-only on the server.</p>
    </div>
  );
}

