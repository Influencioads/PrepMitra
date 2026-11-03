import { useEffect } from 'react';
import { useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Plus, X } from 'lucide-react';
import toast from 'react-hot-toast';
import type { AdminQuestion, AdminQuestionInput } from '@prepmitra/shared';
import { adminQuestionSchema } from '@prepmitra/shared';
import { Button, Input, Modal, Select, Textarea } from '@/components/ui';
import { adminService } from '@/services/adminService';
import { errorMessage } from '@/services/mock';
import { cn } from '@/utils/cn';
import { SUBJECT_OPTIONS, TYPE_LABELS } from './labels';

const TYPE_OPTIONS = Object.entries(TYPE_LABELS).map(([value, label]) => ({ value, label }));
const DIFFICULTY_OPTIONS = ['Easy', 'Moderate', 'Hard'].map((d) => ({ value: d, label: d }));

function toInput(q?: AdminQuestion): AdminQuestionInput {
  if (!q) return { subject: 'quant', topic: '', type: 'single', difficulty: 'Moderate', text: '', options: ['', '', '', ''], correct: [], correctNumeric: '', explanation: '', shortcut: '' };
  return {
    subject: q.subject,
    topic: q.topic,
    type: q.type,
    difficulty: q.difficulty,
    text: q.text,
    options: q.options?.map((o) => o.text) ?? ['', '', '', ''],
    correct: (q.options ?? []).map((o, i) => (q.correctOptionIds?.includes(o.id) ? i : -1)).filter((i) => i >= 0),
    correctNumeric: q.correctNumeric !== undefined ? String(q.correctNumeric) : '',
    explanation: q.explanation,
    shortcut: q.shortcut ?? '',
  };
}

export function QuestionFormModal({
  open, onOpenChange, question,
}: { open: boolean; onOpenChange: (o: boolean) => void; question?: AdminQuestion }) {
  const {
    register, control, handleSubmit, setValue, reset, formState: { errors, isSubmitting },
  } = useForm<AdminQuestionInput>({ resolver: zodResolver(adminQuestionSchema), defaultValues: toInput(question) });

  useEffect(() => {
    if (open) reset(toInput(question));
  }, [open, question, reset]);

  const type = useWatch({ control, name: 'type' });
  const options = useWatch({ control, name: 'options' }) ?? [];
  const correct = useWatch({ control, name: 'correct' }) ?? [];

  const setCorrect = (i: number) => {
    const next = type === 'single' ? [i] : correct.includes(i) ? correct.filter((c) => c !== i) : [...correct, i].sort();
    setValue('correct', next, { shouldValidate: !!errors.correct });
  };
  const addOption = () => setValue('options', [...options, '']);
  const removeOption = (i: number) => {
    setValue('options', options.filter((_, idx) => idx !== i));
    setValue('correct', correct.filter((c) => c !== i).map((c) => (c > i ? c - 1 : c)));
  };

  const onSubmit = async (values: AdminQuestionInput) => {
    try {
      const saved = await adminService.saveQuestion(values, question?.id);
      toast.success(question ? 'Question updated' : `Question ${saved.id} created — pending review`);
      onOpenChange(false);
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  const optionsError = (errors.options as { message?: string } | undefined)?.message;

  return (
    <Modal
      open={open}
      onOpenChange={onOpenChange}
      size="lg"
      title={question ? `Edit ${question.id}` : 'New question'}
      description={question ? 'Edits apply to the English source. Translations are regenerated and re-reviewed.' : 'Manually authored questions start in “Pending review”.'}
      footer={
        <>
          <Button variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
          <Button type="submit" form="question-form" loading={isSubmitting}>{question ? 'Save question' : 'Create question'}</Button>
        </>
      }
    >
      <form id="question-form" onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <Select label="Subject" required options={SUBJECT_OPTIONS} error={errors.subject?.message} {...register('subject')} />
          <Input label="Topic" required error={errors.topic?.message} {...register('topic')} placeholder="e.g. Compound Interest" />
          <Select label="Answer type" required options={TYPE_OPTIONS} {...register('type')} />
          <Select label="Difficulty" required options={DIFFICULTY_OPTIONS} {...register('difficulty')} />
        </div>
        <Textarea label="Question text" required rows={3} error={errors.text?.message} {...register('text')} />

        {type === 'numeric' ? (
          <Input label="Correct numeric answer" required inputMode="decimal" error={errors.correctNumeric?.message} {...register('correctNumeric')} />
        ) : (
          <fieldset className="space-y-2">
            <legend className="text-sm font-medium text-ink">
              Options <span className="font-normal text-muted">— mark the correct {type === 'multiple' ? 'answers' : 'answer'}</span>
            </legend>
            {options.map((_, i) => {
              const letter = String.fromCharCode(65 + i);
              const isCorrect = correct.includes(i);
              return (
                <div key={i} className="flex items-center gap-2">
                  <input
                    type={type === 'single' ? 'radio' : 'checkbox'}
                    name="correct-option"
                    checked={isCorrect}
                    onChange={() => setCorrect(i)}
                    aria-label={`Option ${letter} is correct`}
                    className="h-4 w-4 shrink-0 accent-success"
                  />
                  <span className="w-5 text-sm font-semibold text-muted" aria-hidden>{letter}</span>
                  <input
                    {...register(`options.${i}` as const)}
                    aria-label={`Option ${letter} text`}
                    placeholder={`Option ${letter}`}
                    className={cn(
                      'h-10 w-full min-w-0 rounded-lg border px-3 text-sm focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/30',
                      isCorrect ? 'border-green-400 bg-success-soft' : 'border-line-strong',
                    )}
                  />
                  <button
                    type="button"
                    onClick={() => removeOption(i)}
                    disabled={options.length <= 2}
                    aria-label={`Remove option ${letter}`}
                    className="rounded-md p-2 text-muted hover:bg-stone-100 disabled:opacity-40"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              );
            })}
            <Button size="sm" variant="ghost" leftIcon={<Plus className="h-4 w-4" />} onClick={addOption} disabled={options.length >= 6}>
              Add option
            </Button>
            {optionsError && <p role="alert" className="text-xs font-medium text-danger">{optionsError}</p>}
            {errors.correct?.message && <p role="alert" className="text-xs font-medium text-danger">{errors.correct.message}</p>}
          </fieldset>
        )}

        <Textarea label="Explanation" required rows={3} error={errors.explanation?.message} {...register('explanation')} />
        <Input label="Shortcut (optional)" {...register('shortcut')} placeholder="A faster method learners can use" />
      </form>
    </Modal>
  );
}
