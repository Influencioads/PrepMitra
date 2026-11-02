import type { InterviewTurn } from '@prepmitra/shared';
import { formatDuration } from '@prepmitra/shared';
import { Avatar, Badge } from '@/components/ui';
import { cn } from '@/utils/cn';
import { translate, useT } from '@/i18n';
import { interviewMessages } from '@/i18n/messages/interview';

export const STAGE_KEY = {
  introduction: 'stageIntroduction', resume: 'stageResume', technical: 'stageTechnical', situational: 'stageSituational', hr: 'stageHr', closing: 'stageClosing',
} as const satisfies Record<InterviewTurn['stage'], keyof typeof interviewMessages.en>;
/** Non-hook stage label (current UI language). Inside components prefer t(STAGE_KEY[stage]). */
export const stageLabel = (s: InterviewTurn['stage']) => translate(interviewMessages, STAGE_KEY[s]);

export function ChatBubble({ turn, current, userName }: { turn: InterviewTurn; current?: boolean; userName: string }) {
  const mine = turn.speaker === 'candidate';
  const t = useT(interviewMessages);
  return (
    <li className={cn('flex gap-3', mine && 'flex-row-reverse')}>
      {mine ? (
        <Avatar name={userName} size="sm" />
      ) : (
        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-ink text-xs font-bold text-white" aria-hidden>AI</span>
      )}
      <div className={cn('max-w-[85%] sm:max-w-[75%]', mine && 'text-right')}>
        <div className={cn('mb-1 flex flex-wrap items-center gap-1.5 text-xs text-muted', mine && 'justify-end')}>
          <span className="font-medium text-ink">{mine ? t('you') : t('interviewer')}</span>
          {!mine && <span>· {t(STAGE_KEY[turn.stage])}</span>}
          {turn.isFollowUp && <Badge tone="secondary">{t('followUp')}</Badge>}
          {current && <Badge tone="primary">{t('currentQuestion')}</Badge>}
          {mine && turn.durationSec ? <span>· {t('spoken', { time: formatDuration(turn.durationSec) })}</span> : null}
        </div>
        <div
          className={cn(
            'inline-block whitespace-pre-wrap rounded-2xl px-4 py-3 text-left text-sm leading-relaxed',
            mine ? 'rounded-tr-sm bg-primary text-white' : 'rounded-tl-sm border border-line bg-card text-ink',
            current && 'ring-2 ring-primary/40',
          )}
        >
          {turn.text}
        </div>
      </div>
    </li>
  );
}

export function TypingIndicator() {
  const t = useT(interviewMessages);
  return (
    <li className="flex gap-3" aria-live="polite">
      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-ink text-xs font-bold text-white" aria-hidden>AI</span>
      <div className="rounded-2xl rounded-tl-sm border border-line bg-card px-4 py-3">
        <span className="sr-only">{t('typing')}</span>
        <span className="flex gap-1" aria-hidden>
          {[0, 150, 300].map((d) => (
            <span key={d} className="h-2 w-2 animate-bounce rounded-full bg-subtle" style={{ animationDelay: `${d}ms` }} />
          ))}
        </span>
      </div>
    </li>
  );
}
