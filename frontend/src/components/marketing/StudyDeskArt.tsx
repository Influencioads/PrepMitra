import { useT } from '@/i18n';
import { layoutMessages } from '@/i18n/messages/layout';

/**
 * Line-art illustration for the auth screens: a laptop showing an exam with answer bubbles,
 * a stack of books and a pencil. Brand green strokes with offset saffron/marigold fills.
 */
export function StudyDeskArt({ className }: { className?: string }) {
  const t = useT(layoutMessages);
  const ink = '#1e5e47';
  const s = { fill: 'none', stroke: ink, strokeWidth: 3, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const };
  return (
    <svg viewBox="0 0 400 320" className={className} role="img" aria-label={t('a11yStudyArt')}>
      {/* soft colour shapes, offset from the lines */}
      <rect x="92" y="54" width="196" height="130" rx="14" fill="#ffd27a" opacity="0.55" />
      <rect x="300" y="196" width="70" height="22" rx="5" fill="#f28c28" />
      <circle cx="324" cy="62" r="22" fill="#f28c28" opacity="0.9" />
      <rect x="116" y="76" width="74" height="12" rx="6" fill="#f28c28" />

      {/* laptop screen */}
      <rect x="80" y="44" width="200" height="134" rx="12" {...s} />
      <rect x="94" y="58" width="172" height="106" rx="6" {...s} strokeWidth={2} />
      {/* question lines */}
      <path d="M108 84h70M108 100h120M108 112h96" {...s} strokeWidth={2.5} />
      {/* answer bubbles */}
      {[0, 1, 2, 3].map((i) => (
        <circle key={i} cx={114 + i * 30} cy={138} r={8} {...s} strokeWidth={2.5} fill={i === 2 ? '#f28c28' : 'none'} />
      ))}
      <path d="M214 138l5 5 10-11" {...s} strokeWidth={2.5} />
      {/* laptop base */}
      <path d="M62 178h236l18 22H44l18-22Z" {...s} />
      <path d="M156 189h48" {...s} strokeWidth={2.5} />

      {/* books */}
      <rect x="292" y="200" width="78" height="20" rx="4" {...s} />
      <rect x="300" y="180" width="66" height="20" rx="4" {...s} />
      <rect x="288" y="160" width="74" height="20" rx="4" {...s} />
      <path d="M298 170h20M310 190h22M302 210h28" {...s} strokeWidth={2.5} />

      {/* pencil */}
      <g transform="rotate(-28 118 252)">
        <rect x="70" y="244" width="110" height="16" rx="3" fill="#ffd27a" opacity="0.7" />
        <rect x="66" y="240" width="110" height="16" rx="3" {...s} />
        <path d="M176 240l20 8-20 8" {...s} />
        <path d="M84 240v16" {...s} strokeWidth={2.5} />
      </g>

      {/* tick badge and sparkles */}
      <circle cx="316" cy="56" r="22" {...s} />
      <path d="M306 56l7 7 13-14" {...s} />
      <path d="M48 82v14M41 89h14M362 120v10M357 125h10M240 232v12M234 238h12" {...s} strokeWidth={2.5} />
      {/* desk line */}
      <path d="M30 232c60 10 120 14 180 12" {...s} strokeWidth={2.5} />
    </svg>
  );
}
