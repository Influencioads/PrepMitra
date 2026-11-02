import { useEffect, useMemo } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Controller, useFieldArray, useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ArrowLeft, FileQuestion, Plus, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import type { Exam, Subject } from '@prepmitra/shared';
import { EXAM_CATEGORIES, LANGUAGES, TIER1_LANGUAGES, adminExamSchema } from '@prepmitra/shared';
import {
  Button, ButtonLink, Card, CardBody, CardHeader, Checkbox, ChoiceChip, EmptyState, Input, Notice, PageHeader, Select, Textarea,
} from '@/components/ui';
import { AdminLoadGate } from '@/components/admin/AdminUi';
import { useAdminLoad } from '@/components/admin/useAdminLoad';
import { PUBLISH_OPTIONS, SUBJECT_LABELS, SUBJECT_OPTIONS } from '@/components/admin/labels';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { useAdminStore } from '@/store/adminStore';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

const SUBJECTS = Object.keys(SUBJECT_LABELS) as [Subject, ...Subject[]];
const num = (msg = 'Enter a number') => z.number({ message: msg });

const sectionSchema = z
  .object({
    id: z.string().optional(),
    name: z.string().trim().min(2, 'Name the section'),
    subject: z.enum(SUBJECTS, { message: 'Pick a subject' }),
    questionCount: num().int('Use a whole number').min(1, 'At least 1').max(200, 'At most 200'),
    marksPerQuestion: num().positive('Must be more than 0').max(10, 'At most 10'),
    negativeMarks: num().min(0, 'Cannot be negative').max(10, 'At most 10'),
  })
  .refine((s) => s.negativeMarks <= s.marksPerQuestion, { message: 'Cannot exceed marks per question', path: ['negativeMarks'] });

const examFormSchema = adminExamSchema.extend({
  sections: z.array(sectionSchema).min(1, 'Add at least one section'),
});
type ExamFormValues = z.infer<typeof examFormSchema>;

const CATEGORY_OPTIONS = EXAM_CATEGORIES.map((c) => ({ value: c.id, label: c.label }));
const DIFFICULTY_OPTIONS = ['Easy', 'Moderate', 'Hard'].map((d) => ({ value: d, label: d }));
const round2 = (n: number) => Math.round(n * 100) / 100;

const EMPTY_SECTION = { name: '', subject: 'quant' as Subject, questionCount: 25, marksPerQuestion: 1, negativeMarks: 0.25 };

function toValues(exam?: Exam): ExamFormValues {
  if (!exam)
    return {
      title: '', shortTitle: '', category: 'government', conductingBody: '', description: '', durationMin: 60,
      totalQuestions: 25, totalMarks: 25, difficulty: 'Moderate', creditCost: 1, negativeMarking: '0.25 marks deducted for each wrong answer',
      languages: ['en', 'hi'], status: 'draft', calculatorAllowed: false, sections: [{ ...EMPTY_SECTION }],
    };
  return {
    title: exam.title, shortTitle: exam.shortTitle, category: exam.category, conductingBody: exam.conductingBody,
    description: exam.description, durationMin: exam.durationMin, totalQuestions: exam.totalQuestions, totalMarks: exam.totalMarks,
    difficulty: exam.difficulty, creditCost: exam.creditCost, negativeMarking: exam.negativeMarking, languages: [...exam.languages],
    status: exam.status, calculatorAllowed: exam.calculatorAllowed,
    sections: exam.sections.map((s) => ({
      id: s.id, name: s.name, subject: s.subject, questionCount: s.questionCount, marksPerQuestion: s.marksPerQuestion, negativeMarks: s.negativeMarks,
    })),
  };
}

export function AdminExamFormPage() {
  const { examId } = useParams<{ examId: string }>();
  const load = useAdminLoad('exams');
  const exam = useAdminStore((s) => (examId ? s.exams.find((e) => e.id === examId) : undefined));
  useDocumentTitle(examId ? 'Edit exam' : 'New exam');

  return (
    <div className="space-y-5">
      <ButtonLink to="/admin/exams" variant="ghost" size="sm" leftIcon={<ArrowLeft className="h-4 w-4" />} className="-ml-2">
        All exams
      </ButtonLink>
      <AdminLoadGate state={load} variant="page">
        {examId && !exam ? (
          <EmptyState
            icon={<FileQuestion className="h-6 w-6" />}
            title="Exam not found"
            description="It may have been deleted. Go back to the exam list to pick another one."
            action={<ButtonLink to="/admin/exams">Back to exams</ButtonLink>}
          />
        ) : (
          <ExamForm key={examId ?? 'new'} exam={exam} />
        )}
      </AdminLoadGate>
    </div>
  );
}

function ExamForm({ exam }: { exam?: Exam }) {
  const navigate = useNavigate();
  const defaults = useMemo(() => toValues(exam), [exam]);
  const {
    register, control, handleSubmit, setValue, formState: { errors, isSubmitting, isDirty },
  } = useForm<ExamFormValues>({ resolver: zodResolver(examFormSchema), defaultValues: defaults });
  const { fields, append, remove } = useFieldArray({ control, name: 'sections' });
  const sections = useWatch({ control, name: 'sections' });

  // Totals are derived from the section blueprint.
  useEffect(() => {
    const q = (sections ?? []).reduce((s, x) => s + (Number(x?.questionCount) || 0), 0);
    const m = (sections ?? []).reduce((s, x) => s + (Number(x?.questionCount) || 0) * (Number(x?.marksPerQuestion) || 0), 0);
    setValue('totalQuestions', q);
    setValue('totalMarks', round2(m));
  }, [sections, setValue]);

  const onSubmit = async (values: ExamFormValues) => {
    try {
      const saved = await adminService.saveExam(values, exam?.id);
      toast.success(exam ? `Saved changes to ${saved.shortTitle}` : `Created ${saved.shortTitle}`);
      navigate('/admin/exams');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  const sectionErr = errors.sections;

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
      <PageHeader
        title={exam ? `Edit ${exam.shortTitle}` : 'New exam'}
        description={exam ? `Blueprint id: ${exam.id}` : 'Define the pattern AI papers are generated from. New exams start as drafts.'}
      />

      <Card>
        <CardHeader title="Basics" />
        <CardBody className="grid gap-4 md:grid-cols-2">
          <Input label="Title" required error={errors.title?.message} {...register('title')} placeholder="e.g. SSC CGL Tier 1 Mock Test" />
          <Input label="Short title" required error={errors.shortTitle?.message} {...register('shortTitle')} placeholder="e.g. SSC CGL" hint="Max 20 characters; used on cards." />
          <Select label="Category" required error={errors.category?.message} options={CATEGORY_OPTIONS} {...register('category')} />
          <Input label="Pattern source" required error={errors.conductingBody?.message} {...register('conductingBody')} placeholder="e.g. SSC pattern" hint="We are not affiliated with exam bodies." />
          <Textarea label="Description" required containerClassName="md:col-span-2" rows={3} error={errors.description?.message} {...register('description')} />
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Rules & pricing" />
        <CardBody className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Input label="Duration (min)" type="number" inputMode="numeric" required error={errors.durationMin?.message} {...register('durationMin', { valueAsNumber: true })} />
          <Select label="Difficulty" required options={DIFFICULTY_OPTIONS} error={errors.difficulty?.message} {...register('difficulty')} />
          <Input label="Credit cost" type="number" inputMode="numeric" required hint="0 = free mini mock" error={errors.creditCost?.message} {...register('creditCost', { valueAsNumber: true })} />
          <Select label="Status" required options={PUBLISH_OPTIONS} error={errors.status?.message} {...register('status')} />
          <Input label="Negative marking" required containerClassName="sm:col-span-2" error={errors.negativeMarking?.message} {...register('negativeMarking')} />
          <div className="flex items-end pb-2 sm:col-span-2">
            <Checkbox label="On-screen calculator allowed" description="Shown in the exam instructions." {...register('calculatorAllowed')} />
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardHeader
          title="Sections"
          description="Totals are calculated from the sections."
          action={
            <Button size="sm" variant="secondary" leftIcon={<Plus className="h-4 w-4" />} onClick={() => append({ ...EMPTY_SECTION })} disabled={fields.length >= 8}>
              Add section
            </Button>
          }
        />
        <CardBody className="space-y-4">
          {fields.map((f, i) => {
            const e = sectionErr?.[i];
            return (
              <fieldset key={f.id} className="rounded-xl border border-line p-4">
                <legend className="px-1 text-xs font-semibold uppercase tracking-wide text-muted">Section {i + 1}</legend>
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-[2fr_1.4fr_1fr_1fr_1fr_auto] lg:items-start">
                  <Input label="Name" required error={e?.name?.message} {...register(`sections.${i}.name`)} placeholder="e.g. Quantitative Aptitude" />
                  <Select label="Subject" required options={SUBJECT_OPTIONS} error={e?.subject?.message} {...register(`sections.${i}.subject`)} />
                  <Input label="Questions" type="number" inputMode="numeric" required error={e?.questionCount?.message} {...register(`sections.${i}.questionCount`, { valueAsNumber: true })} />
                  <Input label="Marks / Q" type="number" step="0.01" inputMode="decimal" required error={e?.marksPerQuestion?.message} {...register(`sections.${i}.marksPerQuestion`, { valueAsNumber: true })} />
                  <Input label="Negative" type="number" step="0.01" inputMode="decimal" required error={e?.negativeMarks?.message} {...register(`sections.${i}.negativeMarks`, { valueAsNumber: true })} />
                  <div className="flex items-end lg:pt-7">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-danger hover:bg-danger-soft"
                      leftIcon={<Trash2 className="h-4 w-4" />}
                      onClick={() => remove(i)}
                      disabled={fields.length === 1}
                      aria-label={`Remove section ${i + 1}`}
                    >
                      <span className="lg:sr-only">Remove</span>
                    </Button>
                  </div>
                </div>
              </fieldset>
            );
          })}
          {sectionErr?.root?.message || sectionErr?.message ? (
            <p role="alert" className="text-xs font-medium text-danger">{sectionErr?.root?.message ?? sectionErr?.message}</p>
          ) : null}
          <div className="grid gap-4 sm:grid-cols-2">
            <Input label="Total questions" type="number" readOnly tabIndex={-1} className="bg-stone-50" error={errors.totalQuestions?.message} {...register('totalQuestions', { valueAsNumber: true })} />
            <Input label="Total marks" type="number" readOnly tabIndex={-1} className="bg-stone-50" error={errors.totalMarks?.message} {...register('totalMarks', { valueAsNumber: true })} />
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Languages" description="Learners can take the paper in any selected language." />
        <CardBody>
          <Controller
            control={control}
            name="languages"
            render={({ field }) => {
              const value = field.value as string[];
              const toggle = (code: string) => field.onChange(value.includes(code) ? value.filter((c) => c !== code) : [...value, code]);
              return (
                <div className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    <Button size="sm" variant="outline" onClick={() => field.onChange([...TIER1_LANGUAGES])}>All Tier 1</Button>
                    <Button size="sm" variant="outline" onClick={() => field.onChange(LANGUAGES.map((l) => l.code))}>All 23</Button>
                    <Button size="sm" variant="ghost" onClick={() => field.onChange([])}>Clear</Button>
                    <span className="self-center text-sm text-muted" aria-live="polite">{value.length} selected</span>
                  </div>
                  {[1, 2].map((tier) => (
                    <div key={tier} role="group" aria-label={`Tier ${tier} languages`}>
                      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted">Tier {tier}</p>
                      <div className="flex flex-wrap gap-2">
                        {LANGUAGES.filter((l) => l.tier === tier).map((l) => (
                          <ChoiceChip key={l.code} selected={value.includes(l.code)} onClick={() => toggle(l.code)}>
                            {l.name}
                          </ChoiceChip>
                        ))}
                      </div>
                    </div>
                  ))}
                  {errors.languages?.message && <p role="alert" className="text-xs font-medium text-danger">{errors.languages.message}</p>}
                </div>
              );
            }}
          />
        </CardBody>
      </Card>

      {Object.keys(errors).length > 0 && <Notice tone="danger">Please fix the highlighted fields before saving.</Notice>}

      <div className="flex flex-col-reverse gap-2 border-t border-line pt-5 sm:flex-row sm:justify-end">
        <ButtonLink to="/admin/exams" variant="outline">Cancel</ButtonLink>
        <Button type="submit" loading={isSubmitting} disabled={!!exam && !isDirty}>
          {exam ? 'Save changes' : 'Create exam'}
        </Button>
      </div>
    </form>
  );
}
