import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Check, CircleCheck, CircleX, Play, RotateCcw, SkipForward } from 'lucide-react';
import { examIdFromSlug } from '@prepmitra/shared';
import { Badge, Button, Modal, Notice, type BadgeTone } from '@/components/ui';
import {
  MENTOR_NEEDS_BACKEND, errorMessage, isApiError, mentorService,
  type PracticeQuestion, type PracticeResult, type PracticeSession, type Priority, type StudyTask, type TopicBrief,
} from '@/services';
import { cn } from '@/utils/cn';
import { mmss, useMentorT, type MentorKey } from './format';


const STATUS_TONE: Record<string, BadgeTone> = {
  not_started: 'neutral', insufficient_data: 'neutral', very_weak: 'danger', weak: 'danger',
  needs_improvement: 'warning', good: 'info', strong: 'success',
};
const PRIORITY_TONE: Record<Priority, BadgeTone> = { high: 'danger', medium: 'warning', low: 'neutral', maintenance: 'success' };

export function StatusBadge({ topic }: { topic: Pick<TopicBrief, 'status' | 'mastered' | 'trend'> }) {
  const t = useMentorT();
  const key = (topic.mastered ? 'st_completed' : `st_${topic.status}`) as MentorKey;
  return (
    <span className="inline-flex flex-wrap items-center gap-1">
      <Badge tone={topic.mastered ? 'success' : STATUS_TONE[topic.status]}>{t(key)}</Badge>
      {topic.trend && <span className={cn('text-xs', topic.trend === 'improving' ? 'text-success' : 'text-danger')}>{topic.trend === 'improving' ? `▲ ${t('improving')}` : `▼ ${t('declining')}`}</span>}
    </span>
  );
}

export function PriorityBadge({ priority }: { priority: Priority | null }) {
  const t = useMentorT();
  if (!priority) return null;
  return <Badge tone={PRIORITY_TONE[priority]}>{t(`pr_${priority}` as MentorKey)}</Badge>;
}

export function NeedsBackend({ error }: { error: unknown }) {
  const t = useMentorT();
  if (isApiError(error) && error.code === MENTOR_NEEDS_BACKEND) return <Notice tone="info">{t('needsBackend')}</Notice>;
  return <Notice tone="danger">{errorMessage(error)}</Notice>;
}

/** One planned task with its actions. `onChanged` reloads the parent after a status change or a finished quiz. */
export function TaskRow({ task, examSlug, onChanged, compact }: { task: StudyTask; examSlug?: string; onChanged: () => void; compact?: boolean }) {
  const t = useMentorT();
  const [busy, setBusy] = useState(false);
  const [quiz, setQuiz] = useState<PracticeSession | null>(null);
  const set = async (status: 'done' | 'skipped' | 'pending') => {
    setBusy(true);
    try {
      await mentorService.setTask(task.id, status);
      onChanged();
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };
  const startQuiz = async () => {
    setBusy(true);
    try {
      setQuiz(task.kind === 'mistake_review'
        ? await mentorService.startMistakeReview(10, task.id)
        : await mentorService.startTopicQuiz(task.topic_id!, task.target_questions ? Math.min(task.target_questions, 15) : 10, task.id));
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };
  const open = task.status === 'pending' || task.status === 'missed';
  const quizzable = open && (task.kind === 'mistake_review' || (task.topic_id && ['practice', 'revision'].includes(task.kind)));
  const isRest = task.kind === 'rest';
  return (
    <li className={cn('flex flex-col gap-2 rounded-lg border border-line p-3', task.status === 'done' && 'bg-success-soft/40', task.status === 'missed' && 'border-red-200')}>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-1.5">
          <Badge tone={isRest ? 'neutral' : task.kind === 'mock_test' ? 'primary' : 'secondary'}>{t(`k_${task.kind}` as MentorKey)}</Badge>
          {task.priority && task.priority !== 'medium' && <PriorityBadge priority={task.priority} />}
          {!isRest && <span className="text-xs text-muted">{t('min', { n: task.minutes })}{task.target_questions ? ` · ${t('questionsN', { n: task.target_questions })}` : ''}</span>}
          {task.status !== 'pending' && <Badge tone={task.status === 'done' ? 'success' : task.status === 'missed' ? 'danger' : 'neutral'}>{t(`s_${task.status}` as MentorKey)}</Badge>}
        </div>
        <p className={cn('mt-1 font-medium text-ink', task.status === 'done' && 'line-through decoration-1 opacity-70')}>{task.title}</p>
        {!compact && task.reason && <p className="mt-0.5 text-xs text-muted">{task.reason}</p>}
      </div>
      {!isRest && (
        <div className="flex shrink-0 flex-wrap gap-1.5">
          {open && task.kind === 'mock_test' && examSlug && (
            <Link to={`/exams/${examIdFromSlug(examSlug)}/instructions`} className="inline-flex items-center gap-1 rounded-md bg-primary px-3 py-1.5 text-sm font-medium text-white hover:bg-primary-hover">
              <Play className="h-3.5 w-3.5" aria-hidden />{t('start')}
            </Link>
          )}
          {quizzable && <Button size="sm" onClick={startQuiz} loading={busy} leftIcon={<Play className="h-3.5 w-3.5" />}>{t('start')}</Button>}
          {open && <Button size="sm" variant="outline" onClick={() => set('done')} disabled={busy} leftIcon={<Check className="h-3.5 w-3.5" />}>{t('markDone')}</Button>}
          {open && <Button size="sm" variant="ghost" onClick={() => set('skipped')} disabled={busy} leftIcon={<SkipForward className="h-3.5 w-3.5" />}>{t('markSkip')}</Button>}
          {!open && <Button size="sm" variant="ghost" onClick={() => set('pending')} disabled={busy} leftIcon={<RotateCcw className="h-3.5 w-3.5" />}>{t('undo')}</Button>}
        </div>
      )}
      {quiz && <PracticeQuiz session={quiz} onClose={() => { setQuiz(null); onChanged(); }} />}
    </li>
  );
}

type Answer = string | string[] | number | null;

function fmtAnswer(v: unknown, none: string) {
  if (v === null || v === undefined || v === '' || (Array.isArray(v) && !v.length)) return none;
  return Array.isArray(v) ? v.join(', ') : String(v);
}

/** Short graded quiz (mistake revision or topic practice). Time per question is measured here and sent with answers. */
export function PracticeQuiz({ session, onClose }: { session: PracticeSession; onClose: () => void }) {
  const t = useMentorT();
  const [i, setI] = useState(0);
  const [answers, setAnswers] = useState<Record<string, Answer>>({});
  const times = useRef<Record<string, number>>({});
  const shownAt = useRef(Date.now());
  const [result, setResult] = useState<PracticeResult | null>(null);
  const [busy, setBusy] = useState(false);
  const q: PracticeQuestion | undefined = session.questions[i];

  const track = () => {
    if (!q) return;
    times.current[q.question_id] = (times.current[q.question_id] ?? 0) + Math.round((Date.now() - shownAt.current) / 1000);
    shownAt.current = Date.now();
  };
  useEffect(() => { shownAt.current = Date.now(); }, [i]);
  const go = (n: number) => { track(); setI(n); };
  const submit = async () => {
    track();
    setBusy(true);
    try {
      setResult(await mentorService.submitPractice(session.id, session.questions.map((x) => ({
        question_id: x.question_id, answer: answers[x.question_id] ?? null, time_spent_sec: times.current[x.question_id] ?? 0,
      }))));
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(false);
    }
  };
  const setAns = (v: Answer) => q && setAnswers((a) => ({ ...a, [q.question_id]: v }));
  const cur = q ? answers[q.question_id] : null;

  return (
    <Modal open onOpenChange={(o) => !o && onClose()} size="lg" title={t('quizTitle')}
      description={result ? t('resultTitle', { correct: result.correct, total: result.total }) : q ? t('question', { n: i + 1, total: session.questions.length }) : ''}
      footer={result ? <Button onClick={onClose}>{t('close')}</Button> : (
        <div className="flex w-full justify-between gap-2">
          <Button variant="outline" disabled={i === 0} onClick={() => go(i - 1)}>{t('prev')}</Button>
          {i < session.questions.length - 1
            ? <Button onClick={() => go(i + 1)}>{t('next')}</Button>
            : <Button onClick={submit} loading={busy}>{t('submit')}</Button>}
        </div>
      )}>
      {result ? (
        <ul className="space-y-3">
          {result.results.map((r, n) => {
            const qq = session.questions.find((x) => x.question_id === r.question_id);
            return (
              <li key={r.question_id} className="rounded-lg border border-line p-3 text-sm">
                <p className="flex items-start gap-2 font-medium">
                  {r.status === 'correct' ? <CircleCheck className="mt-0.5 h-4 w-4 shrink-0 text-success" aria-label={t('correct')} /> : <CircleX className="mt-0.5 h-4 w-4 shrink-0 text-danger" aria-label={t('wrong')} />}
                  <span>{n + 1}. {qq?.text}</span>
                </p>
                <p className="mt-1 text-muted">{t('yourAnswer')}: {fmtAnswer(r.your_answer, t('noAnswer'))} · {t('correctAnswer')}: <b className="text-ink">{fmtAnswer(r.correct_answer, '—')}</b> · {mmss(r.time_sec)} / {mmss(r.target_sec)}</p>
                {r.explanation && <p className="mt-1 whitespace-pre-line">{r.explanation}</p>}
              </li>
            );
          })}
        </ul>
      ) : q ? (
        <div>
          <div className="mb-2 flex flex-wrap gap-1.5 text-xs text-muted">
            {q.topic && <Badge>{q.topic}</Badge>}<Badge>{q.difficulty}</Badge><span>{t('colTarget')}: {mmss(q.target_time_sec)}</span>
          </div>
          <p className="whitespace-pre-line text-base text-ink">{q.text}</p>
          {q.type === 'numeric' ? (
            <input type="number" inputMode="decimal" className="mt-4 w-full rounded-lg border border-line-strong px-3 py-2" placeholder={t('numericPlaceholder')}
              value={cur === null || cur === undefined ? '' : String(cur)} onChange={(e) => setAns(e.target.value === '' ? null : Number(e.target.value))} />
          ) : (
            <ul className="mt-4 space-y-2">
              {q.options.map((o) => {
                const selected = q.type === 'multi' ? Array.isArray(cur) && cur.includes(o.key) : cur === o.key;
                return (
                  <li key={o.key}>
                    <button type="button" aria-pressed={selected}
                      onClick={() => setAns(q.type === 'multi'
                        ? (Array.isArray(cur) ? (cur.includes(o.key) ? cur.filter((k) => k !== o.key) : [...cur, o.key]) : [o.key])
                        : (selected ? null : o.key))}
                      className={cn('flex w-full items-start gap-3 rounded-lg border px-3 py-2 text-left text-sm', selected ? 'border-primary bg-primary-soft' : 'border-line hover:bg-stone-50')}>
                      <b>{o.key}</b><span>{o.text}</span>
                    </button>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      ) : null}
    </Modal>
  );
}
