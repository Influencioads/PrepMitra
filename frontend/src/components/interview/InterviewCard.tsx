import { Clock, Mic, MessageSquare } from 'lucide-react';
import type { InterviewRole } from '@prepmitra/shared';
import { Badge, ButtonLink, Card, IconTile } from '@/components/ui';
import { useT } from '@/i18n';
import { catalogMessages, creditsText } from '@/i18n/messages/catalog';

export function InterviewCard({ role, ctaTo }: { role: InterviewRole; ctaTo?: string }) {
  const t = useT(catalogMessages);
  const levels = role.levels.map((l) => t(`level_${l}` as 'level_fresher')).join(' · ');
  return (
    <Card className="flex h-full flex-col p-5 transition-shadow hover:shadow-raised">
      <div className="flex items-start gap-3">
        <IconTile name={role.icon} tone="secondary" />
        <div className="min-w-0">
          <p className="text-xs font-medium text-muted">{role.category}</p>
          <h3 className="mt-0.5 text-base font-semibold leading-snug">{role.title}</h3>
        </div>
      </div>
      <p className="mt-3 line-clamp-3 text-sm text-muted">{role.description}</p>
      <div className="mt-3 flex flex-wrap gap-1.5">
        <Badge icon={<Clock className="h-3 w-3" aria-hidden />}>{t('minShort', { count: role.durationMin })}</Badge>
        <Badge icon={<MessageSquare className="h-3 w-3" aria-hidden />}>{t('text')}</Badge>
        {role.voiceAvailable && <Badge tone="secondary" icon={<Mic className="h-3 w-3" aria-hidden />}>{t('voice')}</Badge>}
        <Badge tone="primary">{creditsText(t, role.creditCost)}</Badge>
      </div>
      <p className="mt-3 text-xs text-muted">{t('levels', { levels })}</p>
      <div className="mt-auto pt-5">
        <ButtonLink to={ctaTo ?? `/interviews/${role.id}`} className="w-full" variant="secondary">
          {t('setupInterview')}
        </ButtonLink>
      </div>
    </Card>
  );
}
