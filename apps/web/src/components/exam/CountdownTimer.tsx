import { useEffect, useRef, useState } from 'react';
import { Timer } from 'lucide-react';
import { formatClock, remainingSeconds } from '@prepmitra/shared';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { examMessages } from '@/i18n/messages/exam';


export interface CountdownTimerProps {
  /** ISO end time. Demo: client-computed. Production: server-controlled. */
  endsAt: string;
  onExpire: () => void;
  className?: string;
  paused?: boolean;
}

/** Countdown clock with warning (<5 min) and danger (<1 min) states plus screen-reader announcements. */
export function CountdownTimer({ endsAt, onExpire, className, paused }: CountdownTimerProps) {
  const t = useT(examMessages);
  const tRef = useRef(t);
  tRef.current = t;
  const [left, setLeft] = useState(() => remainingSeconds({ endsAt }));
  const [announce, setAnnounce] = useState('');
  const expired = useRef(false);
  const onExpireRef = useRef(onExpire);
  onExpireRef.current = onExpire;

  useEffect(() => {
    if (paused) return;
    const tick = () => {
      const s = remainingSeconds({ endsAt });
      setLeft(s);
      if (s === 300) setAnnounce(tRef.current('fiveMinLeft'));
      if (s === 60) setAnnounce(tRef.current('oneMinLeft'));
      if (s <= 0 && !expired.current) {
        expired.current = true;
        onExpireRef.current();
      }
    };
    tick();
    const id = window.setInterval(tick, 1000);
    return () => window.clearInterval(id);
  }, [endsAt, paused]);

  const tone = left < 60 ? 'danger' : left < 300 ? 'warning' : 'normal';
  return (
    <div
      className={cn(
        'inline-flex items-center gap-2 rounded-lg px-3 py-1.5 font-mono text-base font-semibold tabular-nums',
        tone === 'normal' && 'bg-stone-100 text-ink',
        tone === 'warning' && 'bg-warning-soft text-warning-ink',
        tone === 'danger' && 'animate-pulse bg-danger-soft text-danger',
        className,
      )}
      role="timer"
      aria-label={t('timeRemaining', { time: formatClock(left) })}
    >
      <Timer className="h-4 w-4" aria-hidden />
      <span aria-hidden>{formatClock(left)}</span>
      <span className="sr-only" aria-live="assertive">{announce}</span>
    </div>
  );
}
