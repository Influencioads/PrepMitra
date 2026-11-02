import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { CircleCheck, ClipboardCheck, Flag, ShieldOff, Shuffle, X } from 'lucide-react';
import toast from 'react-hot-toast';
import type { AdminQuestion, ReviewItem } from '@prepmitra/shared';
import { formatDateTime, relativeTime } from '@prepmitra/shared';
import {
  Badge, Button, Card, CardBody, ChoiceChip, ConfirmationDialog, EmptyState, Input, Modal, Notice, PageHeader, SearchInput, Tabs, Textarea,
} from '@/components/ui';
import { AdminLoadGate, StatusBadge } from '@/components/admin/AdminUi';
import { QuestionPreview } from '@/components/admin/QuestionPreview';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { QUESTION_STATUS, REASON_LABELS, REVIEW_STATUS, languageLabel } from '@/components/admin/labels';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { useAdminStore } from '@/store/adminStore';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

type View = 'open' | 'resolved';
type SourceFilter = 'all' | 'user-flag' | 'random-sample';

export function AdminReviewQueuePage() {
  useDocumentTitle('Review queue');
  const load = useAdminLoad('review');
  const queue = useAdminStore((s) => s.reviewQueue);
  const questions = useAdminStore((s) => s.questions);
  const exams = useAdminStore((s) => s.exams);
  const flags = useAdminStore((s) => s.settings.featureFlags);
  const [view, setView] = useState<View>('open');
  const [source, setSource] = useState<SourceFilter>('all');
  const [search, setSearch] = useState('');
  const term = useDebounce(search).trim().toLowerCase();
  const [fixing, setFixing] = useState<ReviewItem | null>(null);
  const [rejecting, setRejecting] = useState<ReviewItem | null>(null);
  const [quarantining, setQuarantining] = useState<ReviewItem | null>(null);
  const [note, setNote] = useState('');
  const [busy, setBusy] = useState(false);

  const qById = useMemo(() => new Map(questions.map((q) => [q.id, q])), [questions]);
  const examName = (id?: string) => exams.find((e) => e.id === id)?.shortTitle;

  const open = queue.filter((r) => r.status === 'open');
  const items = useMemo(
    () =>
      queue
        .filter((r) => (view === 'open' ? r.status === 'open' : r.status !== 'open'))
        .filter((r) => source === 'all' || r.source === source)
        .filter((r) => {
          if (!term) return true;
          const q = qById.get(r.questionId);
          return `${r.questionId} ${q?.topic ?? ''} ${q?.text ?? ''}`.toLowerCase().includes(term);
        })
        .sort((a, b) => (view === 'open' ? b.flags.length - a.flags.length || b.createdAt.localeCompare(a.createdAt) : (b.resolvedAt ?? '').localeCompare(a.resolvedAt ?? ''))),
    [queue, view, source, term, qById],
  );

  const resolveSimple = async (item: ReviewItem, outcome: 'rejected' | 'quarantined') => {
    setBusy(true);
    try {
      await adminService.resolveReview(item.id, outcome, { note: note.trim() || undefined });
      toast.success(outcome === 'quarantined' ? `${item.questionId} quarantined` : item.source === 'random-sample' ? `${item.questionId} passed review` : 'Flag rejected — question stays live');
      setRejecting(null);
      setQuarantining(null);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-5">
      <PageHeader
        title="Review queue"
        description="Human review of AI-generated questions before and after they reach learners."
        actions={<Link to="/admin/ai-lessons" className="text-sm font-medium text-primary hover:underline">View AI lessons</Link>}
      />
      <Notice tone="info" title="How items enter the queue">
        A {flags.reviewSampleRate}% random sample of newly generated questions, plus every question a learner flags.{' '}
        <strong>Auto-quarantine rule:</strong> a question with {flags.autoQuarantineThreshold}+ independent reports is pulled from papers automatically
        {flags.autoQuarantine ? '' : ' (currently switched off in Settings)'}. Confirmed fixes become AI lessons that guide future generation.
      </Notice>

      <AdminLoadGate state={load} variant="cards">
        <Tabs
          ariaLabel="Queue view"
          value={view}
          onChange={setView}
          items={[
            { value: 'open', label: 'Open', count: open.length },
            { value: 'resolved', label: 'Resolved', count: queue.length - open.length },
          ]}
        />
        <div className="flex flex-col gap-3 md:flex-row md:items-center">
          <div className="flex flex-wrap gap-2" role="group" aria-label="Filter by source">
            <ChoiceChip selected={source === 'all'} onClick={() => setSource('all')}>All</ChoiceChip>
            <ChoiceChip selected={source === 'user-flag'} onClick={() => setSource('user-flag')}><Flag className="h-3.5 w-3.5" aria-hidden /> User flags</ChoiceChip>
            <ChoiceChip selected={source === 'random-sample'} onClick={() => setSource('random-sample')}><Shuffle className="h-3.5 w-3.5" aria-hidden /> Random sample</ChoiceChip>
          </div>
          <SearchInput value={search} onChange={setSearch} placeholder="Search id, topic or text" label="Search review items" className="md:ml-auto md:w-72" />
        </div>

        {items.length === 0 ? (
          <EmptyState
            icon={<ClipboardCheck className="h-6 w-6" />}
            title={view === 'open' ? 'Queue is clear' : 'Nothing resolved yet'}
            description={view === 'open' ? 'No open items match. New flags and samples will appear here.' : 'Resolved items and their outcomes will be listed here.'}
          />
        ) : (
          <ul className="space-y-4" aria-label={view === 'open' ? 'Open review items' : 'Resolved review items'}>
            {items.map((item) => {
              const q = qById.get(item.questionId);
              const autoQ = item.flags.length >= flags.autoQuarantineThreshold;
              return (
                <li key={item.id}>
                  <Card>
                    <div className="flex flex-wrap items-center gap-2 border-b border-line px-5 py-3">
                      <Badge tone={item.source === 'user-flag' ? 'danger' : 'info'} icon={item.source === 'user-flag' ? <Flag className="h-3 w-3" aria-hidden /> : <Shuffle className="h-3 w-3" aria-hidden />}>
                        {item.source === 'user-flag' ? `${item.flags.length} user report${item.flags.length === 1 ? '' : 's'}` : 'Random sample'}
                      </Badge>
                      <span className="text-sm font-semibold">{item.questionId}</span>
                      {examName(item.examId) && <Badge>{examName(item.examId)}</Badge>}
                      <Badge tone="secondary">{languageLabel(item.language)}</Badge>
                      {q && <StatusBadge map={QUESTION_STATUS} value={q.status} />}
                      {item.status !== 'open' && <StatusBadge map={REVIEW_STATUS} value={item.status} />}
                      <time className="ml-auto text-xs text-muted" dateTime={item.createdAt}>{relativeTime(item.createdAt)}</time>
                    </div>
                    <CardBody className="grid gap-5 lg:grid-cols-[3fr_2fr]">
                      {q ? <QuestionPreview question={q} compact /> : <p className="text-sm text-muted">Question {item.questionId} no longer exists.</p>}
                      <div className="space-y-3">
                        <p className="text-sm font-semibold">{item.source === 'user-flag' ? 'Reports' : 'Why it is here'}</p>
                        {item.flags.length === 0 ? (
                          <p className="text-sm text-muted">Selected in the {flags.reviewSampleRate}% random sample. Check the answer key, explanation and translation quality.</p>
                        ) : (
                          <ul className="space-y-2">
                            {item.flags.map((f) => (
                              <li key={f.id} className="rounded-lg border border-line p-3 text-sm">
                                <div className="flex flex-wrap items-center gap-1.5">
                                  <Badge tone="warning">{REASON_LABELS[f.reason]}</Badge>
                                  <span className="text-xs text-muted">{f.reporter} · {languageLabel(f.language)} · {relativeTime(f.at)}</span>
                                </div>
                                {f.comment && <p className="mt-1.5 text-muted">“{f.comment}”</p>}
                              </li>
                            ))}
                          </ul>
                        )}
                        {autoQ && item.status === 'open' && (
                          <Notice tone="warning">Reached {flags.autoQuarantineThreshold}+ independent reports — {flags.autoQuarantine ? 'auto-quarantined until resolved.' : 'would be auto-quarantined if the rule were on.'}</Notice>
                        )}
                        {item.status !== 'open' && (
                          <div className="rounded-lg bg-stone-50 p-3 text-sm">
                            <p><span className="font-medium">{REVIEW_STATUS[item.status].label}</span> by {item.resolvedBy ?? '—'}</p>
                            {item.resolvedAt && <p className="text-xs text-muted">{formatDateTime(item.resolvedAt)}</p>}
                            {item.resolutionNote && <p className="mt-1 text-muted">{item.resolutionNote}</p>}
                          </div>
                        )}
                      </div>
                    </CardBody>
                    {item.status === 'open' && q && (
                      <div className="flex flex-col gap-2 border-t border-line px-5 py-4 sm:flex-row sm:flex-wrap sm:justify-end">
                        <Button variant="ghost" className="text-danger hover:bg-danger-soft" leftIcon={<ShieldOff className="h-4 w-4" />} onClick={() => { setNote(''); setQuarantining(item); }}>
                          Quarantine
                        </Button>
                        <Button variant="outline" leftIcon={<X className="h-4 w-4" />} onClick={() => { setNote(''); setRejecting(item); }}>
                          {item.source === 'random-sample' ? 'Pass — no issues' : 'Reject flag'}
                        </Button>
                        <Button leftIcon={<CircleCheck className="h-4 w-4" />} onClick={() => setFixing(item)}>
                          Confirm fix
                        </Button>
                      </div>
                    )}
                  </Card>
                </li>
              );
            })}
          </ul>
        )}
      </AdminLoadGate>

      {fixing && qById.get(fixing.questionId) && (
        <FixModal item={fixing} question={qById.get(fixing.questionId)!} onClose={() => setFixing(null)} />
      )}

      <ConfirmationDialog
        open={!!rejecting}
        onOpenChange={(o) => !o && setRejecting(null)}
        title={rejecting?.source === 'random-sample' ? 'Mark as reviewed?' : 'Reject this flag?'}
        description={rejecting?.source === 'random-sample' ? 'The question is approved and stays live.' : 'The question stays live unchanged. Reporters are not notified in this demo.'}
        confirmLabel={rejecting?.source === 'random-sample' ? 'Pass review' : 'Reject flag'}
        loading={busy}
        onConfirm={() => (rejecting ? resolveSimple(rejecting, 'rejected') : undefined)}
      >
        <Textarea label="Note (optional, saved to audit log)" rows={2} value={note} onChange={(e) => setNote(e.target.value)} placeholder="e.g. Verified the answer with a worked solution" />
      </ConfirmationDialog>

      <ConfirmationDialog
        open={!!quarantining}
        onOpenChange={(o) => !o && setQuarantining(null)}
        title="Quarantine this question?"
        description="It will be removed from all papers until a reviewer approves it again in the question bank."
        confirmLabel="Quarantine"
        variant="danger"
        loading={busy}
        onConfirm={() => (quarantining ? resolveSimple(quarantining, 'quarantined') : undefined)}
      >
        <Textarea label="Reason (optional)" rows={2} value={note} onChange={(e) => setNote(e.target.value)} />
      </ConfirmationDialog>
    </div>
  );
}

// ---------- Confirm-fix modal ----------
const fixSchema = z
  .object({
    type: z.enum(['single', 'multiple', 'numeric']),
    correct: z.array(z.number()),
    correctNumeric: z.string(),
    explanation: z.string().trim().min(10, 'Add an explanation (10+ characters)'),
    note: z.string().trim().min(5, 'Describe what was wrong (5+ characters)'),
    lessonText: z.string().trim().min(15, 'Lesson must be at least 15 characters').max(400, 'Keep the lesson under 400 characters'),
  })
  .superRefine((v, ctx) => {
    if (v.type === 'numeric') {
      if (!v.correctNumeric.trim() || Number.isNaN(Number(v.correctNumeric))) ctx.addIssue({ code: 'custom', path: ['correctNumeric'], message: 'Enter the numeric answer' });
    } else if (v.correct.length === 0) ctx.addIssue({ code: 'custom', path: ['correct'], message: 'Mark the correct option' });
    else if (v.type === 'single' && v.correct.length > 1) ctx.addIssue({ code: 'custom', path: ['correct'], message: 'Only one option can be correct' });
  });
type FixValues = z.infer<typeof fixSchema>;

function FixModal({ item, question, onClose }: { item: ReviewItem; question: AdminQuestion; onClose: () => void }) {
  const defaults: FixValues = {
    type: question.type,
    correct: (question.options ?? []).map((o, i) => (question.correctOptionIds?.includes(o.id) ? i : -1)).filter((i) => i >= 0),
    correctNumeric: question.correctNumeric !== undefined ? String(question.correctNumeric) : '',
    explanation: question.explanation,
    note: '',
    lessonText: '',
  };
  const { register, handleSubmit, control, setValue, formState: { errors, isSubmitting } } = useForm<FixValues>({ resolver: zodResolver(fixSchema), defaultValues: defaults });
  const correct = useWatch({ control, name: 'correct' }) ?? [];
  const noteValue = useWatch({ control, name: 'note' });
  const reasons = [...new Set(item.flags.map((f) => REASON_LABELS[f.reason].toLowerCase()))].join(', ');

  // Suggest a lesson from the reviewer's note until they write their own.
  const [lessonTouched, setLessonTouched] = useState(false);
  useEffect(() => {
    if (lessonTouched) return;
    const n = noteValue?.trim();
    setValue('lessonText', n ? `${question.topic}: ${n}. Verify the answer key and explanation against a worked solution before publishing.`.slice(0, 400) : '');
  }, [noteValue, lessonTouched, question.topic, setValue]);

  const toggle = (i: number) =>
    setValue('correct', question.type === 'single' ? [i] : correct.includes(i) ? correct.filter((c) => c !== i) : [...correct, i].sort(), { shouldValidate: !!errors.correct });

  const onSubmit = async (v: FixValues) => {
    try {
      const lesson = await adminService.resolveReview(item.id, 'fixed', {
        note: v.note, explanation: v.explanation, correct: v.correct, correctNumeric: v.correctNumeric, lessonText: v.lessonText,
      });
      toast.success(lesson ? `Fix confirmed. Lesson created for “${lesson.topic}”.` : 'Fix confirmed. Lesson created.');
      onClose();
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <Modal
      open
      onOpenChange={(o) => !o && onClose()}
      size="lg"
      title={`Confirm fix — ${question.id}`}
      description={reasons ? `Reported as: ${reasons}.` : 'Random-sample review.'}
      footer={
        <>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button type="submit" form="fix-form" loading={isSubmitting}>Confirm fix & create lesson</Button>
        </>
      }
    >
      <form id="fix-form" onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
        <p className="rounded-lg bg-stone-50 p-3 text-sm">{question.text}</p>
        {question.type === 'numeric' ? (
          <Input label="Correct answer" required inputMode="decimal" error={errors.correctNumeric?.message} {...register('correctNumeric')} />
        ) : (
          <fieldset className="space-y-2">
            <legend className="text-sm font-medium">Correct {question.type === 'multiple' ? 'answers' : 'answer'}</legend>
            {question.options?.map((o, i) => (
              <label key={o.id} className="flex cursor-pointer items-center gap-3 rounded-lg border border-line px-3 py-2 text-sm hover:bg-stone-50">
                <input type={question.type === 'single' ? 'radio' : 'checkbox'} name="fix-correct" checked={correct.includes(i)} onChange={() => toggle(i)} className="h-4 w-4 accent-success" />
                <span className="font-semibold text-muted">{String.fromCharCode(65 + i)}.</span> {o.text}
              </label>
            ))}
            {errors.correct?.message && <p role="alert" className="text-xs font-medium text-danger">{errors.correct.message}</p>}
          </fieldset>
        )}
        <Textarea label="Explanation" required rows={3} error={errors.explanation?.message} {...register('explanation')} />
        <Input label="What was wrong?" required error={errors.note?.message} {...register('note')} placeholder="e.g. Answer key pointed to option B; correct is D" />
        <Textarea
          label="AI lesson"
          required
          rows={3}
          hint="Added to AI lessons so future generation avoids the same mistake. Max 400 characters."
          error={errors.lessonText?.message}
          {...register('lessonText', { onChange: () => setLessonTouched(true) })}
        />
      </form>
    </Modal>
  );
}
