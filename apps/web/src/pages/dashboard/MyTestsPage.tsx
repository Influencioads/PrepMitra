import { useMemo, useState } from 'react';
import { ClipboardList, MessageSquare, PlayCircle, Trash2 } from 'lucide-react';
import type { ExamCategory } from '@prepmitra/shared';
import {
  EXAM_CATEGORIES, formatDateTime, formatDuration, formatShortDate, getExamById, relativeTime, remainingSeconds, answeredCount,
} from '@prepmitra/shared';
import {
  Badge, ButtonLink, Button, Card, ConfirmationDialog, EmptyState, PageHeader, SearchInput, Select, Tabs, accuracyTone,
} from '@/components/ui';
import { selectHistory, selectInProgress, useExamStore, useInterviewStore } from '@/store';
import { useDebounce } from '@/hooks/useDebounce';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import toast from 'react-hot-toast';
import { useT } from '@/i18n';
import { accountMessages } from '@/i18n/messages/account';
import { catalogMessages, categoryText } from '@/i18n/messages/catalog';

type Tab = 'exams' | 'interviews' | 'in-progress';
type Sort = 'recent' | 'oldest' | 'score' | 'accuracy';

export function MyTestsPage() {
  const t = useT(accountMessages);
  const tcat = useT(catalogMessages);
  useDocumentTitle(t('myTestsTitle'));
  const reports = useExamStore((s) => s.reports);
  const attempts = useExamStore((s) => s.attempts);
  const discardAttempt = useExamStore((s) => s.discardAttempt);
  const interviewReports = useInterviewStore((s) => s.reports);
  const [tab, setTab] = useState<Tab>('exams');
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState<ExamCategory | 'all'>('all');
  const [sort, setSort] = useState<Sort>('recent');
  const [discardId, setDiscardId] = useState<string | null>(null);
  const term = useDebounce(search).trim().toLowerCase();

  const history = useMemo(() => selectHistory(reports), [reports]);
  const inProgress = useMemo(() => selectInProgress(attempts), [attempts]);
  const interviews = useMemo(() => Object.values(interviewReports).sort((a, b) => b.createdAt.localeCompare(a.createdAt)), [interviewReports]);

  const exams = useMemo(() => {
    const list = history.filter((h) => (category === 'all' || h.category === category) && (!term || h.examTitle.toLowerCase().includes(term)));
    const sorters: Record<Sort, (a: (typeof list)[number], b: (typeof list)[number]) => number> = {
      recent: (a, b) => b.submittedAt.localeCompare(a.submittedAt),
      oldest: (a, b) => a.submittedAt.localeCompare(b.submittedAt),
      score: (a, b) => b.score / b.maxScore - a.score / a.maxScore,
      accuracy: (a, b) => b.accuracy - a.accuracy,
    };
    return [...list].sort(sorters[sort]);
  }, [history, category, term, sort]);

  const filteredInterviews = useMemo(
    () => interviews.filter((r) => !term || r.roleTitle.toLowerCase().includes(term)).sort((a, b) =>
      sort === 'oldest' ? a.createdAt.localeCompare(b.createdAt) : sort === 'score' || sort === 'accuracy' ? b.overall - a.overall : b.createdAt.localeCompare(a.createdAt)),
    [interviews, term, sort],
  );

  return (
    <div>
      <PageHeader
        title={t('myTestsTitle')}
        description={t('myTestsDesc')}
        actions={<ButtonLink to="/exams">{t('takeNewMock')}</ButtonLink>}
      />
      <Tabs
        ariaLabel={t('testType')}
        value={tab}
        onChange={setTab}
        items={[
          { value: 'exams', label: t('tabExams'), count: history.length },
          { value: 'interviews', label: t('tabInterviews'), count: interviews.length },
          { value: 'in-progress', label: t('tabInProgress'), count: inProgress.length },
        ]}
      />

      {tab !== 'in-progress' && (
        <div className="mt-4 grid gap-3 sm:grid-cols-[1fr_200px_180px]">
          <SearchInput value={search} onChange={setSearch} placeholder={tab === 'exams' ? t('searchExams') : t('searchRoles')} label={t('searchTests')} />
          {tab === 'exams' ? (
            <Select aria-label={t('category')} value={category} onChange={(e) => setCategory(e.target.value as ExamCategory | 'all')} options={[{ value: 'all', label: t('allCategories') }, ...EXAM_CATEGORIES.map((c) => ({ value: c.id, label: categoryText(tcat, c.id).label }))]} />
          ) : (
            <span className="hidden sm:block" />
          )}
          <Select aria-label={t('sort')} value={sort} onChange={(e) => setSort(e.target.value as Sort)} options={[{ value: 'recent', label: t('sortRecent') }, { value: 'oldest', label: t('sortOldest') }, { value: 'score', label: t('sortScore') }, ...(tab === 'exams' ? [{ value: 'accuracy', label: t('sortAccuracy') }] : [])]} />
        </div>
      )}

      <div className="mt-5">
        {tab === 'exams' &&
          (exams.length === 0 ? (
            <EmptyState
              icon={<ClipboardList className="h-6 w-6" />}
              title={history.length === 0 ? t('noExamsYet') : t('noTestsMatch')}
              description={history.length === 0 ? t('noExamsYetDesc') : t('noTestsMatchDesc')}
              action={history.length === 0 ? <ButtonLink to="/exams/general-aptitude">{t('takeFreeMini')}</ButtonLink> : <Button variant="outline" onClick={() => { setSearch(''); setCategory('all'); }}>{t('clearFilters')}</Button>}
            />
          ) : (
            <>
              <Card className="hidden overflow-x-auto md:block">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-line text-left text-muted">
                      <th scope="col" className="px-5 py-3 font-medium">{t('colExam')}</th>
                      <th scope="col" className="px-5 py-3 font-medium">{t('colSubmitted')}</th>
                      <th scope="col" className="px-5 py-3 font-medium">{t('colScore')}</th>
                      <th scope="col" className="px-5 py-3 font-medium">{t('colAccuracy')}</th>
                      <th scope="col" className="px-5 py-3 font-medium">{t('colPercentile')}</th>
                      <th scope="col" className="px-5 py-3 font-medium">{t('colTime')}</th>
                      <th scope="col" className="px-5 py-3"><span className="sr-only">{t('colActions')}</span></th>
                    </tr>
                  </thead>
                  <tbody>
                    {exams.map((h) => (
                      <tr key={h.reportId} className="border-b border-line last:border-0">
                        <td className="px-5 py-3">
                          <p className="font-medium">{h.examTitle}</p>
                          <p className="text-xs text-muted">{h.category ? categoryText(tcat, h.category).label : ''}</p>
                        </td>
                        <td className="px-5 py-3 text-muted">{formatDateTime(h.submittedAt)}</td>
                        <td className="px-5 py-3 font-medium">{h.score}/{h.maxScore}</td>
                        <td className="px-5 py-3"><Badge tone={accuracyTone(h.accuracy)}>{h.accuracy}%</Badge></td>
                        <td className="px-5 py-3">{h.percentile}</td>
                        <td className="px-5 py-3 text-muted">{formatDuration(h.timeTakenSec)}</td>
                        <td className="whitespace-nowrap px-5 py-3 text-right">
                          <ButtonLink to={`/exam-result/${h.reportId}`} variant="ghost" size="sm">{t('result')}</ButtonLink>
                          <ButtonLink to={`/reports/${h.reportId}`} variant="secondary" size="sm">{t('fullReport')}</ButtonLink>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </Card>
              <ul className="space-y-3 md:hidden">
                {exams.map((h) => (
                  <li key={h.reportId}>
                    <Card className="p-4">
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <p className="font-semibold">{h.examTitle}</p>
                          <p className="text-xs text-muted">{formatShortDate(h.submittedAt)} · {formatDuration(h.timeTakenSec)}</p>
                        </div>
                        <Badge tone={accuracyTone(h.accuracy)}>{h.accuracy}%</Badge>
                      </div>
                      <p className="mt-2 text-sm">{t('scoreLabel')} <b>{h.score}/{h.maxScore}</b> · {t('percentileValue', { p: h.percentile })}</p>
                      <div className="mt-3 grid grid-cols-2 gap-2">
                        <ButtonLink to={`/exam-result/${h.reportId}`} variant="outline" size="sm">{t('result')}</ButtonLink>
                        <ButtonLink to={`/reports/${h.reportId}`} variant="secondary" size="sm">{t('fullReport')}</ButtonLink>
                      </div>
                    </Card>
                  </li>
                ))}
              </ul>
            </>
          ))}

        {tab === 'interviews' &&
          (filteredInterviews.length === 0 ? (
            <EmptyState
              icon={<MessageSquare className="h-6 w-6" />}
              title={interviews.length === 0 ? t('noInterviewsYet') : t('noInterviewsMatch')}
              description={t('interviewsEmptyDesc')}
              action={<ButtonLink to="/interviews">{t('browseRoles')}</ButtonLink>}
            />
          ) : (
            <ul className="grid gap-4 md:grid-cols-2">
              {filteredInterviews.map((r) => (
                <li key={r.id}>
                  <Card className="flex h-full flex-col p-5">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="font-semibold">{r.roleTitle}</p>
                        <p className="text-xs text-muted">{formatDateTime(r.createdAt)} · {r.mode === 'voice' ? t('modeVoice') : t('modeText')} · {formatDuration(r.durationSec)}</p>
                      </div>
                      <Badge tone={r.overall >= 7.5 ? 'success' : r.overall >= 5 ? 'warning' : 'danger'}>{r.overall}/10</Badge>
                    </div>
                    <p className="mt-3 line-clamp-2 text-sm text-muted">{r.strengths[0]}</p>
                    <div className="mt-auto flex gap-2 pt-4">
                      <ButtonLink to={`/interview/report/${r.id}`} variant="secondary" size="sm">{t('viewReport')}</ButtonLink>
                      <ButtonLink to={`/interviews/${r.roleId}`} variant="ghost" size="sm">{t('practiseAgain')}</ButtonLink>
                    </div>
                  </Card>
                </li>
              ))}
            </ul>
          ))}

        {tab === 'in-progress' &&
          (inProgress.length === 0 ? (
            <EmptyState icon={<PlayCircle className="h-6 w-6" />} title={t('nothingInProgress')} description={t('nothingInProgressDesc')} />
          ) : (
            <ul className="space-y-3">
              {inProgress.map((a) => {
                const exam = getExamById(a.examId);
                const left = remainingSeconds(a);
                const ids = a.paper.map((p) => p.questionId);
                return (
                  <li key={a.id}>
                    <Card className="flex flex-col gap-3 p-4 sm:flex-row sm:items-center">
                      <div className="flex-1">
                        <p className="font-semibold">{exam?.title ?? a.examId}</p>
                        <p className="text-sm text-muted">
                          {t('startedAnswered', { when: relativeTime(a.startedAt), answered: answeredCount(ids, a.states), total: ids.length })}{' '}
                          {left > 0 ? t('minLeftDemo', { n: Math.ceil(left / 60) }) : t('timeUp')}
                        </p>
                      </div>
                      <div className="flex gap-2">
                        <Button variant="ghost" size="sm" leftIcon={<Trash2 className="h-4 w-4" />} onClick={() => setDiscardId(a.id)}>{t('discard')}</Button>
                        <ButtonLink to={`/exam/${a.id}`} size="sm">{left > 0 ? t('resume') : t('resumeSubmit')}</ButtonLink>
                      </div>
                    </Card>
                  </li>
                );
              })}
            </ul>
          ))}
      </div>

      <ConfirmationDialog
        open={!!discardId}
        onOpenChange={(o) => !o && setDiscardId(null)}
        title={t('discardTitle')}
        description={t('discardDesc')}
        confirmLabel={t('discardConfirm')}
        variant="danger"
        onConfirm={() => {
          if (discardId) discardAttempt(discardId);
          setDiscardId(null);
          toast.success(t('discarded'));
        }}
      />
    </div>
  );
}
