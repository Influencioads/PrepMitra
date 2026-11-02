import { MessageSquare } from 'lucide-react';
import type { InterviewReport, InterviewScores } from '@prepmitra/shared';
import { formatShortDate } from '@prepmitra/shared';
import { ButtonLink, Card, CardBody, CardHeader, EmptyState, ProgressBar } from '@/components/ui';
import { useT } from '@/i18n';
import { dashboardMessages } from '@/i18n/messages/dashboard';

const SKILLS: (keyof InterviewScores)[] = ['roleKnowledge', 'answerStructure', 'communication', 'confidence', 'resumeConsistency'];
const tone = (v: number): 'success' | 'warning' | 'danger' => (v >= 7.5 ? 'success' : v >= 5 ? 'warning' : 'danger');

/** Latest interview scores on the dashboard (plan Day 11: "interview scores"). */
export function InterviewScoresCard({ reports }: { reports: InterviewReport[] }) {
  const t = useT(dashboardMessages);
  const latest = [...reports].sort((a, b) => b.createdAt.localeCompare(a.createdAt));
  const top = latest[0];
  return (
    <Card>
      <CardHeader
        title={t('intScores')}
        description={top ? t('intLatest', { role: top.roleTitle, date: formatShortDate(top.createdAt) }) : t('intOutOf10')}
        action={top ? <ButtonLink to={`/interview/report/${top.id}`} variant="ghost" size="sm">{t('report')}</ButtonLink> : undefined}
      />
      <CardBody>
        {!top ? (
          <EmptyState
            icon={<MessageSquare className="h-6 w-6" />}
            title={t('intNone')}
            description={t('intNoneDesc')}
            action={<ButtonLink to="/interviews" size="sm">{t('intStart')}</ButtonLink>}
            className="border-0 py-6"
          />
        ) : (
          <div className="grid gap-5 sm:grid-cols-[auto_1fr] sm:items-center">
            <div className="text-center">
              <p className="font-display text-4xl font-bold">{top.overall}</p>
              <p className="text-xs text-muted">{t('overall10')}</p>
              {latest[1] && (
                <p className={`mt-1 text-xs font-semibold ${top.overall >= latest[1].overall ? 'text-success' : 'text-danger'}`}>
                  {top.overall >= latest[1].overall ? '▲' : '▼'} {Math.abs(Math.round((top.overall - latest[1].overall) * 10) / 10)} {t('vsPrevious')}
                </p>
              )}
            </div>
            <ul className="space-y-2">
              {SKILLS.map((key) => (
                <li key={key}>
                  <ProgressBar label={`${t(`skill_${key}`)} · ${top.scores[key]}`} value={top.scores[key]} max={10} tone={tone(top.scores[key])} size="sm" />
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardBody>
    </Card>
  );
}
