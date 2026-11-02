import { Link } from 'react-router-dom';
import { Check } from 'lucide-react';
import { Bubble, MitraSays, PenNote, PenScore, Stamp } from '@/components/ui';
import { useT } from '@/i18n';
import { homeMessages } from '@/i18n/messages/home';
import { cn } from '@/utils/cn';

type Mark = 'ok' | 'x' | 'skip';
const LEFT: [number, number, Mark][] = [[1, 1, 'ok'], [2, 3, 'ok'], [3, 2, 'ok'], [4, 0, 'x'], [5, 1, 'ok'], [6, 0, 'ok']];
const RIGHT: [number, number, Mark][] = [[9, 0, 'ok'], [10, -1, 'skip'], [11, -1, 'skip'], [12, 1, 'ok'], [13, 3, 'ok'], [14, 2, 'ok']];

function OmrRow({ n, pick, mark, skipLabel }: { n: number; pick: number; mark: Mark; skipLabel: string }) {
  return (
    <div className="flex h-6 items-center gap-1.5 sm:gap-2">
      {mark === 'skip' ? (
        <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 border-pen text-[10px] font-bold text-pen">{n}</span>
      ) : (
        <span className="w-6 shrink-0 text-xs font-bold">{n}</span>
      )}
      {[0, 1, 2, 3].map((i) => <Bubble key={i} filled={i === pick} size={16} />)}
      <span className="ml-0.5 text-xs">
        {mark === 'ok' && <Check className="h-3.5 w-3.5 text-success" aria-hidden />}
        {mark === 'x' && <span className="font-bold text-pen">✗</span>}
        {mark === 'skip' && <span className="font-hand text-pen">{skipLabel}</span>}
      </span>
    </div>
  );
}

/** Hero visual: a checked OMR sheet with a red-pen score and Mitra's note. Sample data, labelled as such. */
export function AnswerSheetHero({ className }: { className?: string }) {
  const t = useT(homeMessages);
  return (
    <div className={cn('relative mx-auto w-full max-w-[460px] pb-24 sm:pb-20', className)} role="img" aria-label={`${t('sheetTitle')} — ${t('sampleLabel')}: 27¾/35, ${t('percentile')} 84.2`}>
      <div className="rotate-[2deg] rounded-[10px] border-[1.5px] border-ink bg-card p-5 shadow-[14px_14px_0_var(--color-rule)] sm:p-7" aria-hidden>
        <div className="flex items-center justify-between gap-3 border-b-2 border-ink pb-3">
          <span className="font-display text-xs font-extrabold uppercase tracking-[0.12em] sm:text-sm">{t('sheetTitle')}</span>
          <span className="text-[11px] text-muted sm:text-xs">{t('sheetExam')}</span>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-x-4 gap-y-2.5 sm:gap-x-6">
          {LEFT.map((l, i) => (
            <div key={l[0]} className="contents">
              <OmrRow n={l[0]} pick={l[1]} mark={l[2]} skipLabel={t('sheetSkip')} />
              <OmrRow n={RIGHT[i][0]} pick={RIGHT[i][1]} mark={RIGHT[i][2]} skipLabel={t('sheetSkip')} />
            </div>
          ))}
        </div>
        <PenNote className="mt-4">{t('sheetNote')}</PenNote>
        <div className="mt-5 flex items-center justify-between gap-3">
          <PenScore score="27¾" total={35} size="sm" className="sm:text-5xl" />
          <Stamp value="84.2" label={t('percentile')} />
        </div>
      </div>
      <MitraSays tone="chalk" size={52} className="absolute -left-2 bottom-0 max-w-[330px] -rotate-2 sm:-left-10">{t('mitraHero')}</MitraSays>
    </div>
  );
}

/** A winding 7-day path. Positions are fixed so the dotted line never crosses a label. */
export function PrepPathPreview({ startHref, className }: { startHref: string; className?: string }) {
  const t = useT(homeMessages);
  const done = 'bg-success text-white shadow-[0_4px_0_#116632]';
  return (
    <div className={cn('relative h-[360px] overflow-hidden rounded-3xl border border-line bg-card', className)}>
      <svg viewBox="0 0 260 360" preserveAspectRatio="none" className="absolute left-0 top-0 h-[360px] w-[160px] sm:w-[260px]" aria-hidden>
        <path d="M70 52 C 170 60, 190 100, 160 132 C 130 170, 70 180, 80 222 C 90 266, 190 270, 170 312" fill="none" stroke="#1C2321" strokeWidth="3" strokeDasharray="2 10" strokeLinecap="round" />
      </svg>
      <ol className="contents">
        <li>
          <span className={cn('absolute left-[19px] top-[28px] sm:left-[46px] flex h-12 w-12 items-center justify-center rounded-full', done)} aria-hidden><Check className="h-5 w-5" /></span>
          <p className="absolute left-[150px] sm:left-[232px] top-[40px] pr-4 text-sm text-muted sm:text-base">{t('pathDay1')}</p>
        </li>
        <li>
          <span className={cn('absolute left-[74px] top-[108px] sm:left-[136px] flex h-12 w-12 items-center justify-center rounded-full', done)} aria-hidden><Check className="h-5 w-5" /></span>
          <p className="absolute left-[150px] sm:left-[232px] top-[120px] pr-4 text-sm text-muted sm:text-base">{t('pathDay2')}</p>
        </li>
        <li>
          <Link to={startHref} className="absolute left-[9px] top-[182px] sm:left-[40px] flex h-20 w-20 items-center justify-center rounded-full bg-primary text-sm font-extrabold uppercase text-white shadow-[0_6px_0_#8A2E07,0_0_0_10px_rgb(242_140_40/0.25)] transition-transform hover:-translate-y-0.5">
            {t('start')}
          </Link>
          <p className="absolute left-[150px] sm:left-[232px] top-[190px] pr-4 text-sm leading-snug sm:text-base">
            <b className="block text-xs font-bold uppercase tracking-[0.1em] text-primary">{t('pathToday')}</b>
            <b className="block">{t('pathDay3')}</b>
            <span className="text-muted">{t('pathDay3Meta')}</span>
          </p>
        </li>
        <li>
          <span className="absolute left-[81px] top-[288px] sm:left-[146px] flex h-12 w-12 items-center justify-center rounded-full border-2 border-dashed border-primary bg-card font-extrabold text-primary" aria-hidden>6</span>
          <p className="absolute left-[150px] sm:left-[232px] top-[288px] pr-4 text-sm leading-snug sm:text-base"><b className="block">{t('pathDay6')}</b><span className="text-muted">{t('pathDay6Meta')}</span></p>
        </li>
      </ol>
    </div>
  );
}

/** Three-member interview panel around a table, with the chair speaking. */
export function PanelRoom({ className }: { className?: string }) {
  const t = useT(homeMessages);
  const seat = 'flex items-center justify-center rounded-full font-extrabold';
  return (
    <div className={cn('relative mx-auto h-[300px] w-full max-w-[560px]', className)} aria-hidden>
      <svg viewBox="0 0 560 300" className="absolute inset-0 h-full w-full">
        <ellipse cx="280" cy="180" rx="230" ry="70" fill="#5C3A1E" />
        <ellipse cx="280" cy="172" rx="230" ry="70" fill="#7A4E2A" />
        <rect x="220" y="150" width="56" height="38" rx="3" fill="#FBF8EF" transform="rotate(-6 248 169)" />
        <rect x="296" y="152" width="48" height="34" rx="3" fill="#FBF8EF" transform="rotate(5 320 169)" />
      </svg>
      <div className="absolute left-[16%] top-[16%] flex flex-col items-center gap-1 text-chalk-text">
        <span className={cn(seat, 'h-14 w-14 border-2 border-white/30 bg-[#2C4A3D] sm:h-16 sm:w-16')}>BK</span>
        <span className="text-xs text-white/70">{t('panelBanking')}</span>
      </div>
      <div className="absolute left-1/2 top-[2%] flex -translate-x-1/2 flex-col items-center gap-1 text-chalk-text">
        <span className={cn(seat, 'h-16 w-16 bg-primary text-lg shadow-[0_0_0_8px_rgb(242_140_40/0.35),0_0_0_16px_rgb(242_140_40/0.14)] sm:h-20 sm:w-20 sm:text-xl')}>CH</span>
        <span className="text-xs font-bold text-accent">{t('panelChair')}</span>
      </div>
      <div className="absolute right-[16%] top-[16%] flex flex-col items-center gap-1 text-chalk-text">
        <span className={cn(seat, 'h-14 w-14 border-2 border-white/30 bg-[#2C4A3D] sm:h-16 sm:w-16')}>HR</span>
        <span className="text-xs text-white/70">{t('panelHr')}</span>
      </div>
      <p className="absolute inset-x-0 bottom-2 text-center font-hand text-lg text-white/85">{t('intQuote')}</p>
    </div>
  );
}
