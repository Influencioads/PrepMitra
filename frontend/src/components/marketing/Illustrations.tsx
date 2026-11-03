import { Mic, Sparkles, Timer, TrendingUp } from 'lucide-react';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { landingMessages } from '@/i18n/messages/landing';

/* Inline illustrations for the marketing pages. All drawn in code (no external images),
   so they stay crisp, theme-consistent and load instantly on slow networks. */

const BUBBLES = ['A', 'B', 'C', 'D'];
// Which bubble is filled on each row of the sample OMR sheet (null = left blank, "r" = marked for review).
const OMR_ROWS: { n: number; pick: number | null; review?: boolean }[] = [
  { n: 21, pick: 1 },
  { n: 22, pick: 3 },
  { n: 23, pick: null },
  { n: 24, pick: 0, review: true },
  { n: 25, pick: 2 },
  { n: 26, pick: 1 },
];

/** A CBT-style answer sheet: the most recognisable object in an Indian exam hall. */
export function OmrSheet({ className }: { className?: string }) {
  const t = useT(landingMessages);
  return (
    <div className={cn('rounded-2xl border border-line bg-card p-4 shadow-raised', className)} aria-hidden>
      <div className="flex items-center justify-between border-b border-dashed border-line-strong pb-2">
        <p className="font-display text-[11px] font-bold tracking-[0.14em] text-muted">{t('answerSheet')}</p>
        <p className="rounded bg-secondary-soft px-1.5 py-0.5 text-[10px] font-semibold text-secondary">{t('quant')}</p>
      </div>
      <ul className="mt-3 space-y-2">
        {OMR_ROWS.map((r) => (
          <li key={r.n} className="flex items-center gap-2.5">
            <span className="w-6 text-right text-[11px] font-semibold tabular-nums text-muted">{r.n}</span>
            {BUBBLES.map((b, i) => (
              <span
                key={b}
                className={cn(
                  'flex h-5 w-5 items-center justify-center rounded-full border text-[9px] font-bold',
                  r.pick === i
                    ? r.review
                      ? 'border-[#6B21A8] bg-[#7E22CE] text-white'
                      : 'border-secondary bg-secondary text-white'
                    : 'border-line-strong text-subtle',
                )}
              >
                {b}
              </span>
            ))}
            {r.pick === null && <span className="ml-1 text-[10px] font-medium text-danger">{t('skipped')}</span>}
            {r.review && <span className="ml-1 text-[10px] font-medium text-[#7E22CE]">{t('review')}</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}

export function MiniRing({ value, size = 64, stroke = 7, color = '#15803D', track = '#E3E2D8', label }: { value: number; size?: number; stroke?: number; color?: string; track?: string; label?: string }) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  return (
    <span className="relative inline-flex items-center justify-center" style={{ width: size, height: size }} aria-hidden>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} stroke={track} strokeWidth={stroke} fill="none" />
        <circle cx={size / 2} cy={size / 2} r={r} stroke={color} strokeWidth={stroke} fill="none" strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c - (value / 100) * c} />
      </svg>
      <span className="absolute font-display text-sm font-bold text-ink">{label ?? `${value}%`}</span>
    </span>
  );
}

const BARS = [0.35, 0.7, 0.5, 0.9, 0.6, 1, 0.45, 0.8, 0.55, 0.3, 0.65, 0.4];
export function Waveform({ className, color = 'currentColor', bars = BARS }: { className?: string; color?: string; bars?: number[] }) {
  return (
    <svg viewBox={`0 0 ${bars.length * 6} 24`} className={className} aria-hidden>
      {bars.map((h, i) => (
        <rect key={i} x={i * 6 + 1} y={12 - h * 10} width={3} height={h * 20} rx={1.5} fill={color} />
      ))}
    </svg>
  );
}

/** Phone showing a report — the moment the product is built around. */
export function PhoneReport({ className }: { className?: string }) {
  const t = useT(landingMessages);
  const topics = [
    { t: t('topicPercentages'), v: 86, c: '#15803D' },
    { t: t('topicSyllogism'), v: 62, c: '#D97706' },
    { t: t('topicSeating'), v: 38, c: '#DC2626' },
  ];
  return (
    <div className={cn('w-[220px] rounded-[30px] border-[6px] border-ink bg-ink shadow-overlay', className)} aria-hidden>
      <div className="overflow-hidden rounded-[24px] bg-background">
        <div className="flex items-center justify-between px-4 pt-2.5 text-[9px] font-semibold text-ink">
          <span>9:41</span>
          <span className="h-3 w-14 rounded-full bg-ink" />
          <span>4G</span>
        </div>
        <div className="space-y-2.5 p-3">
          <div className="rounded-2xl bg-card p-3 shadow-card">
            <p className="text-[10px] font-semibold text-muted">{t('phoneReport')}</p>
            <div className="mt-2 flex items-center gap-3">
              <MiniRing value={78} size={58} stroke={6} label="78%" />
              <div className="text-[10px] leading-relaxed">
                <p><b className="text-ink">27.25</b><span className="text-muted">{t('marksOf')}</span></p>
                <p><b className="text-ink">84.2</b><span className="text-muted">{t('percentileWord')}</span></p>
                <p className="font-semibold text-success">{t('vsLast')}</p>
              </div>
            </div>
          </div>
          <div className="rounded-2xl bg-card p-3 shadow-card">
            <p className="text-[10px] font-semibold text-ink">{t('topicAccuracy')}</p>
            <ul className="mt-2 space-y-1.5">
              {topics.map((x) => (
                <li key={x.t}>
                  <div className="flex justify-between text-[9px]"><span className="text-ink">{x.t}</span><span className="text-muted">{x.v}%</span></div>
                  <div className="mt-0.5 h-1.5 rounded-full bg-surface">
                    <div className="h-full rounded-full" style={{ width: `${x.v}%`, background: x.c }} />
                  </div>
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl bg-secondary p-3 text-white">
            <p className="flex items-center gap-1 text-[10px] font-semibold"><Sparkles className="h-3 w-3 text-accent" />{t('nextBestStep')}</p>
            <p className="mt-1 text-[9px] leading-snug text-white/80">{t('nextBestStepBody')}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

/** Hero composition: answer sheet, phone report and floating chips. Sample data only. */
export function HeroVisual() {
  const t = useT(landingMessages);
  return (
    <div className="relative mx-auto h-[380px] w-full max-w-[520px] sm:h-[480px]" role="img" aria-label={t('illAria')}>
      <div className="absolute left-[6%] top-[8%] h-[78%] w-[78%] rounded-[40%_60%_55%_45%] bg-primary-soft" aria-hidden />
      <div className="absolute bottom-[4%] right-[2%] h-[46%] w-[46%] rounded-full bg-secondary-soft" aria-hidden />
      <svg className="absolute right-[8%] top-[4%] h-16 w-16 text-accent" viewBox="0 0 64 64" aria-hidden>
        {Array.from({ length: 16 }).map((_, i) => (
          <circle key={i} cx={8 + (i % 4) * 16} cy={8 + Math.floor(i / 4) * 16} r={2.5} fill="currentColor" opacity={0.55} />
        ))}
      </svg>

      <OmrSheet className="absolute left-0 top-[12%] w-[54%] -rotate-[5deg] sm:left-[2%] sm:top-[14%] sm:w-[62%]" />
      <PhoneReport className="absolute right-0 top-[6%] origin-top-right scale-[0.8] sm:right-[4%] sm:scale-100" />

      <div className="absolute bottom-[3%] left-0 flex items-center sm:bottom-[16%] sm:left-[4%] gap-2 rounded-full border border-line bg-card px-3 py-2 shadow-raised motion-safe:animate-float" aria-hidden>
        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-accent-soft text-primary"><Timer className="h-4 w-4" /></span>
        <span className="text-xs"><b className="font-display tabular-nums text-ink">42:18</b> <span className="text-muted">{t('timeLeft')}</span></span>
      </div>
      <div className="absolute bottom-[2%] left-[30%] hidden items-center gap-2 rounded-2xl sm:flex border border-line bg-card px-3 py-2 shadow-raised" aria-hidden>
        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-secondary text-white"><Mic className="h-3.5 w-3.5" /></span>
        <Waveform className="h-5 w-16 text-secondary" />
        <span className="text-[11px] font-medium text-muted">{t('voiceInterview')}</span>
      </div>
      <div className="absolute right-[0%] top-[0%] rounded-2xl border border-line bg-card px-3 py-2 text-xs shadow-raised motion-safe:animate-float [animation-delay:1.5s]" aria-hidden>
        <span lang="hi">हिन्दी</span> · <span lang="ta">தமிழ்</span> · <span lang="bn">বাংলা</span> · English
      </div>
      <div className="absolute bottom-[34%] right-[-2%] hidden items-center gap-1.5 rounded-full bg-success px-3 py-1.5 text-xs font-semibold text-white shadow-raised sm:flex" aria-hidden>
        <TrendingUp className="h-3.5 w-3.5" /> {t('shortcutGain')}
      </div>
    </div>
  );
}

/** CBT question palette in miniature, used as a feature visual. */
export function MiniPalette({ className }: { className?: string }) {
  const states = 'aaanmaavaaxnaamaaanaavaa'.split('');
  const cls: Record<string, string> = {
    a: 'bg-success text-white',
    n: 'bg-danger-soft text-danger border border-[#F5A39A]',
    m: 'bg-[#7E22CE] text-white',
    x: 'bg-primary text-white',
    v: 'bg-surface text-muted',
  };
  return (
    <div className={cn('grid grid-cols-8 gap-1.5', className)} aria-hidden>
      {states.map((s, i) => (
        <span key={i} className={cn('flex aspect-square items-center justify-center rounded-md text-[10px] font-semibold tabular-nums', cls[s])}>{i + 1}</span>
      ))}
    </div>
  );
}

/** Chat preview for the interview section. */
export function InterviewChat({ className }: { className?: string }) {
  const t = useT(landingMessages);
  return (
    <div className={cn('rounded-3xl bg-card p-4 shadow-overlay sm:p-5', className)} aria-hidden>
      <div className="flex items-center justify-between border-b border-line pb-3">
        <div className="flex items-center gap-2.5">
          <span className="flex h-9 w-9 items-center justify-center rounded-full bg-secondary font-display text-sm font-bold text-white">AI</span>
          <div>
            <p className="text-sm font-semibold text-ink">{t('panelName')}</p>
            <p className="text-[11px] text-muted">{t('panelProgress')}</p>
          </div>
        </div>
        <span className="rounded-full bg-danger-soft px-2 py-0.5 text-[10px] font-semibold text-danger">● REC 01:12</span>
      </div>
      <div className="space-y-3 py-4 text-[13px] leading-relaxed">
        <p className="max-w-[85%] rounded-2xl rounded-tl-sm bg-surface px-3.5 py-2.5 text-ink">
          {t('chatQ')}
        </p>
        <p className="ml-auto max-w-[85%] rounded-2xl rounded-tr-sm bg-primary px-3.5 py-2.5 text-white">
          {t('chatA')}
        </p>
        <p className="max-w-[85%] rounded-2xl rounded-tl-sm border border-accent/40 bg-accent-soft px-3.5 py-2.5 text-ink">
          <span className="mb-0.5 block text-[10px] font-bold uppercase tracking-wide text-primary">{t('followUp')}</span>
          {t('chatF')}
        </p>
      </div>
      <div className="flex items-center gap-3 rounded-2xl bg-background p-2.5">
        <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-danger text-white motion-safe:animate-pulse-ring"><Mic className="h-4 w-4" /></span>
        <Waveform className="h-6 flex-1 text-primary" bars={[0.3, 0.6, 0.9, 0.5, 0.75, 1, 0.4, 0.85, 0.55, 0.7, 0.35, 0.95, 0.6, 0.45, 0.8, 0.5, 0.3, 0.65]} />
        <span className="text-[11px] font-medium tabular-nums text-muted">0:24</span>
      </div>
    </div>
  );
}

/** Graduation cap + certificate, for the closing call-to-action. */
export function CapIllustration({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 220 180" className={className} aria-hidden>
      <rect x="40" y="70" width="140" height="96" rx="10" fill="#FFFEFA" />
      <rect x="56" y="88" width="80" height="8" rx="4" fill="#E3E2D8" />
      <rect x="56" y="104" width="108" height="6" rx="3" fill="#E3E2D8" />
      <rect x="56" y="116" width="96" height="6" rx="3" fill="#E3E2D8" />
      <circle cx="150" cy="142" r="14" fill="#F28C28" />
      <path d="M143 154l-4 14 11-6 11 6-4-14" fill="#C2410C" />
      <path d="M110 18 30 48l80 30 80-30-80-30Z" fill="#1C2321" />
      <path d="M62 60v24c0 10 22 18 48 18s48-8 48-18V60l-48 18-48-18Z" fill="#2B3431" />
      <path d="M182 50v34" stroke="#F28C28" strokeWidth="4" strokeLinecap="round" />
      <circle cx="182" cy="88" r="6" fill="#F28C28" />
    </svg>
  );
}
