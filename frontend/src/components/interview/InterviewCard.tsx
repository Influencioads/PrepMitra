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
      className="group flex h-full flex-col rounded-[22px] border border-line bg-card p-5 transition duration-200 hover:-translate-y-0.5 hover:border-secondary/40 hover:shadow-[0_18px_40px_-24px_rgb(23_74_56/0.45)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-secondary"
    >
      <div className="flex items-start justify-between gap-3">
        <span className="flex h-11 w-11 items-center justify-center rounded-2xl bg-secondary text-white"><AppIcon name={role.icon} className="h-5 w-5" /></span>
        {role.voiceAvailable && (
          <span className="inline-flex items-center gap-1 rounded-full bg-secondary-soft px-2.5 py-1 text-xs font-medium text-secondary"><Mic className="h-3 w-3" aria-hidden />{t('voice')}</span>
        )}
      </div>
      <p className="mt-4 text-xs font-medium text-muted">{ct(role.category)}</p>
      <h3 className="mt-1 text-lg font-semibold leading-snug text-ink">{title}</h3>
      <p className="mt-2 line-clamp-2 text-sm text-muted">{ct(role.description)}</p>
      <p className="mt-2 text-sm text-muted">{facts.join(' · ')}</p>
      <div className="min-h-5 flex-1" aria-hidden />
      <div className="flex items-center justify-between gap-3 border-t border-dashed border-line-strong pt-4">
        <p className="text-sm font-semibold text-ink">{creditsText(t, role.creditCost)}</p>
        <span className="inline-flex items-center gap-1.5 text-sm font-semibold text-secondary">
          <span className="hidden sm:inline">{t('setupInterview')}</span>
          <span className="flex h-8 w-8 items-center justify-center rounded-full bg-secondary-soft text-secondary transition-colors group-hover:bg-secondary group-hover:text-white">
            <ArrowRight className="h-4 w-4" aria-hidden />
          </span>
        </span>
      </div>
    </Link>
  );
}
