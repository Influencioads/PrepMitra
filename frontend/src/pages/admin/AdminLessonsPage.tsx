import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { BookText, Pencil, Plus, Sparkles, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import type { AdminGlossaryInput, AdminLessonInput, AiLesson, GlossaryTerm } from '@prepmitra/shared';
import { LANGUAGES, adminGlossarySchema, adminLessonSchema, formatDate } from '@prepmitra/shared';
import { Button, ConfirmationDialog, EmptyState, Input, Modal, PageHeader, SearchInput, Select, Switch, Tabs, Textarea } from '@/components/ui';
import { AdminLoadGate, DataTable, FilterBar, IconButton, ResultCount, StatusBadge, ToggleSwitch, type Column } from '@/components/admin/AdminUi';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { LANGUAGE_OPTIONS, LESSON_SOURCE, languageLabel } from '@/components/admin/labels';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { useAdminStore } from '@/store/adminStore';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

type Tab = 'lessons' | 'glossary';
const LANG_FILTER = [{ value: 'all', label: 'All languages' }, ...LANGUAGE_OPTIONS];

export function AdminLessonsPage() {
  useDocumentTitle('AI lessons & glossary');
  const load = useAdminLoad('lessons');
  const [params, setParams] = useSearchParams();
  const tab: Tab = params.get('tab') === 'glossary' ? 'glossary' : 'lessons';
  const lessons = useAdminStore((s) => s.lessons);
  const glossary = useAdminStore((s) => s.glossary);

  return (
    <div className="space-y-5">
      <PageHeader
        title="AI lessons & glossary"
        description="Lessons are short rules injected into generation prompts. The glossary fixes approved translations for key terms."
      />
      <AdminLoadGate state={load}>
        <Tabs
          ariaLabel="Lessons or glossary"
          value={tab}
          onChange={(v) => setParams(v === 'lessons' ? {} : { tab: v }, { replace: true })}
          items={[
            { value: 'lessons', label: 'AI lessons', count: lessons.length },
            { value: 'glossary', label: 'Glossary', count: glossary.length },
          ]}
        />
        {tab === 'lessons' ? <LessonsTab /> : <GlossaryTab />}
      </AdminLoadGate>
    </div>
  );
}

// ---------- Lessons ----------
function LessonsTab() {
  const lessons = useAdminStore((s) => s.lessons);
  const [search, setSearch] = useState('');
  const [lang, setLang] = useState('all');
  const [active, setActive] = useState('all');
  const [editing, setEditing] = useState<AiLesson | null | undefined>(undefined);
  const [toDelete, setToDelete] = useState<AiLesson | null>(null);
  const [busy, setBusy] = useState(false);
  const term = useDebounce(search).trim().toLowerCase();

  const rows = useMemo(
    () =>
      lessons.filter(
        (l) =>
          (lang === 'all' || l.language === lang) &&
          (active === 'all' || String(l.active) === active) &&
          (!term || `${l.topic} ${l.lessonText}`.toLowerCase().includes(term)),
      ),
    [lessons, lang, active, term],
  );
  const filtered = lang !== 'all' || active !== 'all' || !!term;

  const toggle = async (l: AiLesson, v: boolean) => {
    try {
      await adminService.setLessonActive(l.id, v);
      toast.success(v ? 'Lesson activated' : 'Lesson deactivated');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  const doDelete = async () => {
    if (!toDelete) return;
    setBusy(true);
    try {
      await adminService.deleteLesson(toDelete.id);
      toast.success('Lesson deleted');
      setToDelete(null);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  const columns: Column<AiLesson>[] = [
    { key: 'topic', header: 'Topic', cell: (l) => <span className="font-medium">{l.topic}</span> },
    { key: 'lang', header: 'Language', cell: (l) => languageLabel(l.language) },
    {
      key: 'text',
      header: 'Lesson',
      cell: (l) => (
        <p className="max-w-[420px] text-muted" dir={LANGUAGES.find((x) => x.code === l.language)?.rtl ? 'rtl' : undefined}>{l.lessonText}</p>
      ),
    },
    {
      key: 'source',
      header: 'Source',
      cell: (l) => (
        <div>
          <StatusBadge map={LESSON_SOURCE} value={l.source} />
          {l.sourceQuestionId && <p className="mt-0.5 text-xs text-muted">{l.sourceQuestionId}</p>}
        </div>
      ),
    },
    { key: 'active', header: 'Active', cell: (l) => <ToggleSwitch checked={l.active} onChange={(v) => void toggle(l, v)} label={`Lesson “${l.topic}” active`} /> },
    { key: 'updated', header: 'Updated', cell: (l) => <span className="whitespace-nowrap text-muted">{formatDate(l.updatedAt)}</span> },
    {
      key: 'actions',
      header: 'Actions',
      srHeader: true,
      className: 'text-right',
      cell: (l) => (
        <div className="flex justify-end gap-0.5">
          <IconButton label={`Edit lesson ${l.topic}`} onClick={() => setEditing(l)}><Pencil className="h-4 w-4" /></IconButton>
          <IconButton label={`Delete lesson ${l.topic}`} tone="danger" onClick={() => setToDelete(l)}><Trash2 className="h-4 w-4" /></IconButton>
        </div>
      ),
    },
  ];

  return (
    <>
      <FilterBar>
        <SearchInput value={search} onChange={setSearch} placeholder="Search topic or text" label="Search lessons" />
        <Select aria-label="Language" value={lang} onChange={(e) => setLang(e.target.value)} options={LANG_FILTER} />
        <Select aria-label="Active state" value={active} onChange={(e) => setActive(e.target.value)} options={[{ value: 'all', label: 'Active & inactive' }, { value: 'true', label: 'Active only' }, { value: 'false', label: 'Inactive only' }]} />
        <Button leftIcon={<Plus className="h-4 w-4" />} onClick={() => setEditing(null)}>New lesson</Button>
      </FilterBar>
      <ResultCount count={rows.length} noun="lesson" onClear={filtered ? () => { setSearch(''); setLang('all'); setActive('all'); } : undefined} />
      <DataTable
        caption="AI lessons"
        columns={columns}
        rows={rows}
        rowKey={(l) => l.id}
        minWidth={1000}
        empty={<EmptyState icon={<Sparkles className="h-6 w-6" />} title="No lessons found" description="Confirmed fixes in the review queue create lessons automatically, or add one manually." action={<Button onClick={() => setEditing(null)}>New lesson</Button>} />}
      />
      <LessonModal open={editing !== undefined} lesson={editing ?? undefined} onClose={() => setEditing(undefined)} />
      <ConfirmationDialog
        open={!!toDelete}
        onOpenChange={(o) => !o && setToDelete(null)}
        title="Delete this lesson?"
        description={toDelete ? `“${toDelete.topic}” will stop guiding question generation. Consider deactivating instead.` : undefined}
        confirmLabel="Delete lesson"
        variant="danger"
        loading={busy}
        onConfirm={doDelete}
      />
    </>
  );
}

function LessonModal({ open, lesson, onClose }: { open: boolean; lesson?: AiLesson; onClose: () => void }) {
  const toValues = (l?: AiLesson): AdminLessonInput => ({ topic: l?.topic ?? '', language: l?.language ?? 'en', lessonText: l?.lessonText ?? '', active: l?.active ?? true });
  const { register, control, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<AdminLessonInput>({ resolver: zodResolver(adminLessonSchema), defaultValues: toValues(lesson) });
  useEffect(() => {
    if (open) reset(toValues(lesson));
  }, [open, lesson, reset]);

  const onSubmit = async (v: AdminLessonInput) => {
    try {
      await adminService.saveLesson(v, lesson?.id);
      toast.success(lesson ? 'Lesson updated' : 'Lesson created');
      onClose();
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <Modal
      open={open}
      onOpenChange={(o) => !o && onClose()}
      title={lesson ? 'Edit lesson' : 'New AI lesson'}
      description="Keep lessons short, specific and testable."
      footer={
        <>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button type="submit" form="lesson-form" loading={isSubmitting}>{lesson ? 'Save lesson' : 'Create lesson'}</Button>
        </>
      }
    >
      <form id="lesson-form" onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
        <Input label="Topic" required error={errors.topic?.message} {...register('topic')} placeholder="e.g. Compound Interest" />
        <Select label="Language" required options={LANGUAGE_OPTIONS} error={errors.language?.message} {...register('language')} />
        <Textarea label="Lesson text" required rows={4} hint="15–400 characters." error={errors.lessonText?.message} {...register('lessonText')} />
        <Controller control={control} name="active" render={({ field }) => (
          <Switch checked={field.value} onChange={field.onChange} label="Active" description="Inactive lessons are kept but not used in prompts." />
        )} />
      </form>
    </Modal>
  );
}

// ---------- Glossary ----------
function GlossaryTab() {
  const glossary = useAdminStore((s) => s.glossary);
  const [search, setSearch] = useState('');
  const [lang, setLang] = useState('all');
  const [editing, setEditing] = useState<GlossaryTerm | null | undefined>(undefined);
  const [toDelete, setToDelete] = useState<GlossaryTerm | null>(null);
  const [busy, setBusy] = useState(false);
  const term = useDebounce(search).trim().toLowerCase();

  const rows = useMemo(
    () => glossary.filter((g) => (lang === 'all' || g.language === lang) && (!term || `${g.term} ${g.approvedTranslation}`.toLowerCase().includes(term))),
    [glossary, lang, term],
  );

  const doDelete = async () => {
    if (!toDelete) return;
    setBusy(true);
    try {
      await adminService.deleteGlossary(toDelete.id);
      toast.success('Glossary term deleted');
      setToDelete(null);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  const columns: Column<GlossaryTerm>[] = [
    { key: 'term', header: 'Term (English)', cell: (g) => <span className="font-medium">{g.term}</span> },
    { key: 'lang', header: 'Language', cell: (g) => languageLabel(g.language) },
    {
      key: 'tr',
      header: 'Approved translation',
      cell: (g) => <span lang={g.language} dir={LANGUAGES.find((x) => x.code === g.language)?.rtl ? 'rtl' : undefined} className="text-base">{g.approvedTranslation}</span>,
    },
    { key: 'updated', header: 'Updated', cell: (g) => <span className="whitespace-nowrap text-muted">{formatDate(g.updatedAt)}</span> },
    {
      key: 'actions',
      header: 'Actions',
      srHeader: true,
      className: 'text-right',
      cell: (g) => (
        <div className="flex justify-end gap-0.5">
          <IconButton label={`Edit ${g.term} (${g.language})`} onClick={() => setEditing(g)}><Pencil className="h-4 w-4" /></IconButton>
          <IconButton label={`Delete ${g.term} (${g.language})`} tone="danger" onClick={() => setToDelete(g)}><Trash2 className="h-4 w-4" /></IconButton>
        </div>
      ),
    },
  ];

  return (
    <>
      <FilterBar>
        <SearchInput value={search} onChange={setSearch} placeholder="Search term or translation" label="Search glossary" className="lg:col-span-2" />
        <Select aria-label="Language" value={lang} onChange={(e) => setLang(e.target.value)} options={LANG_FILTER} />
        <Button leftIcon={<Plus className="h-4 w-4" />} onClick={() => setEditing(null)}>New term</Button>
      </FilterBar>
      <ResultCount count={rows.length} noun="term" onClear={lang !== 'all' || term ? () => { setSearch(''); setLang('all'); } : undefined} />
      <DataTable
        caption="Glossary"
        columns={columns}
        rows={rows}
        rowKey={(g) => g.id}
        minWidth={680}
        empty={<EmptyState icon={<BookText className="h-6 w-6" />} title="No glossary terms found" description="Add approved translations so every paper uses the same terminology." action={<Button onClick={() => setEditing(null)}>New term</Button>} />}
      />
      <GlossaryModal open={editing !== undefined} term={editing ?? undefined} onClose={() => setEditing(undefined)} />
      <ConfirmationDialog
        open={!!toDelete}
        onOpenChange={(o) => !o && setToDelete(null)}
        title="Delete this glossary term?"
        description={toDelete ? `“${toDelete.term}” → “${toDelete.approvedTranslation}” (${languageLabel(toDelete.language)})` : undefined}
        confirmLabel="Delete term"
        variant="danger"
        loading={busy}
        onConfirm={doDelete}
      />
    </>
  );
}

function GlossaryModal({ open, term, onClose }: { open: boolean; term?: GlossaryTerm; onClose: () => void }) {
  const glossary = useAdminStore((s) => s.glossary);
  const toValues = (g?: GlossaryTerm): AdminGlossaryInput => ({ term: g?.term ?? '', language: g?.language ?? 'hi', approvedTranslation: g?.approvedTranslation ?? '' });
  const { register, handleSubmit, reset, setError, formState: { errors, isSubmitting } } = useForm<AdminGlossaryInput>({ resolver: zodResolver(adminGlossarySchema), defaultValues: toValues(term) });
  useEffect(() => {
    if (open) reset(toValues(term));
  }, [open, term, reset]);

  const onSubmit = async (v: AdminGlossaryInput) => {
    const dup = glossary.find((g) => g.id !== term?.id && g.language === v.language && g.term.trim().toLowerCase() === v.term.trim().toLowerCase());
    if (dup) {
      setError('term', { message: `“${dup.term}” already has a ${languageLabel(dup.language)} translation` });
      return;
    }
    try {
      await adminService.saveGlossary(v, term?.id);
      toast.success(term ? 'Glossary term updated' : 'Glossary term added');
      onClose();
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <Modal
      open={open}
      onOpenChange={(o) => !o && onClose()}
      title={term ? 'Edit glossary term' : 'New glossary term'}
      footer={
        <>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button type="submit" form="glossary-form" loading={isSubmitting}>{term ? 'Save term' : 'Add term'}</Button>
        </>
      }
    >
      <form id="glossary-form" onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
        <Input label="Term (English)" required error={errors.term?.message} {...register('term')} placeholder="e.g. Compound interest" />
        <Select label="Language" required options={LANGUAGE_OPTIONS.filter((o) => o.value !== 'en')} error={errors.language?.message} {...register('language')} />
        <Input label="Approved translation" required error={errors.approvedTranslation?.message} {...register('approvedTranslation')} />
      </form>
    </Modal>
  );
}
