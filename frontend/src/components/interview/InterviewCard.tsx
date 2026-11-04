import { ArrowRight, Mic } from 'lucide-react';
import { Link } from 'react-router-dom';
import type { InterviewRole } from '@prepmitra/shared';
import { AppIcon } from '@/components/ui';
import { useT } from '@/i18n';
import { useContentT } from '@/i18n/content';
import { catalogMessages, creditsText } from '@/i18n/messages/catalog';

/** Minimal card for one interview role; the whole card links to its setup page. */
export function InterviewCard({ role, ctaTo }: { role: InterviewRole; ctaTo?: string }) {
  const t = useT(catalogMessages);
  const ct = useContentT();
  const title = ct(role.title);
  const levels = role.levels.map((l) => t(`level_${l}` as 'level_fresher')).join(', ');
  const facts = [t('minShort', { count: role.durationMin }), role.voiceAvailable ? `${t('text')} + ${t('voice')}` : t('text'), levels];
  return (
    <Link
      to={ctaTo ?? `/interviews/${role.id}`}
      aria-label={`${t('setupInterview')}: ${title}`}
      className="group flex h-full flex-col rounded-2xl border border-line bg-card p-5 transition-colors hover:border-secondary/50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-secondary"
    >
      <div className="flex items-center gap-2 text-xs font-medium text-muted">
        <AppIcon name={role.icon} className="h-4 w-4 text-secondary" />
        {ct(role.category)}
        {role.voiceAvailable && <Mic className="ml-auto h-3.5 w-3.5 text-subtle" aria-hidden />}
      </div>
      <h3 className="mt-3 text-lg font-semibold leading-snug text-ink">{title}</h3>
      <p className="mt-2 line-clamp-2 text-sm text-muted">{ct(role.description)}</p>
      <p className="mt-2 text-sm text-muted">{facts.join(' · ')}</p>
      <div className="min-h-5 flex-1" aria-hidden />
      <div className="flex items-end justify-between gap-3 border-t border-line pt-4">
        <p className="text-sm font-semibold text-ink">{creditsText(t, role.creditCost)}</p>
        <span className="inline-flex items-center gap-1 text-sm font-semibold text-secondary">
          {t('setupInterview')}
          <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" aria-hidden />
        </span>
      </div>
    </Link>
  );
}
