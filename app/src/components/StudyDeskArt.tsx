import Svg, { Circle, G, Path, Rect } from 'react-native-svg';

const INK = '#1E5E47';
const SAFFRON = '#F28C28';
const MARIGOLD = '#FFD27A';

/**
 * Line-art illustration for the auth screens (same drawing as the website's StudyDeskArt):
 * a laptop with an exam and answer bubbles, books and a pencil.
 */
export function StudyDeskArt({ height = 180 }: { height?: number }) {
  const s = { fill: 'none', stroke: INK, strokeWidth: 3, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const };
  return (
    <Svg width={(height * 400) / 320} height={height} viewBox="0 0 400 320" accessibilityLabel="Laptop with a practice exam, books and a pencil">
      <Rect x={92} y={54} width={196} height={130} rx={14} fill={MARIGOLD} opacity={0.55} />
      <Rect x={300} y={196} width={70} height={22} rx={5} fill={SAFFRON} />
      <Circle cx={324} cy={62} r={22} fill={SAFFRON} opacity={0.9} />
      <Rect x={116} y={76} width={74} height={12} rx={6} fill={SAFFRON} />

      <Rect x={80} y={44} width={200} height={134} rx={12} {...s} />
      <Rect x={94} y={58} width={172} height={106} rx={6} {...s} strokeWidth={2} />
      <Path d="M108 84h70M108 100h120M108 112h96" {...s} strokeWidth={2.5} />
      {[0, 1, 2, 3].map((i) => (
        <Circle key={i} cx={114 + i * 30} cy={138} r={8} {...s} strokeWidth={2.5} fill={i === 2 ? SAFFRON : 'none'} />
      ))}
      <Path d="M214 138l5 5 10-11" {...s} strokeWidth={2.5} />
      <Path d="M62 178h236l18 22H44l18-22Z" {...s} />
      <Path d="M156 189h48" {...s} strokeWidth={2.5} />

      <Rect x={292} y={200} width={78} height={20} rx={4} {...s} />
      <Rect x={300} y={180} width={66} height={20} rx={4} {...s} />
      <Rect x={288} y={160} width={74} height={20} rx={4} {...s} />
      <Path d="M298 170h20M310 190h22M302 210h28" {...s} strokeWidth={2.5} />

      <G transform="rotate(-28 118 252)">
        <Rect x={70} y={244} width={110} height={16} rx={3} fill={MARIGOLD} opacity={0.7} />
        <Rect x={66} y={240} width={110} height={16} rx={3} {...s} />
        <Path d="M176 240l20 8-20 8" {...s} />
        <Path d="M84 240v16" {...s} strokeWidth={2.5} />
      </G>

      <Circle cx={316} cy={56} r={22} {...s} />
      <Path d="M306 56l7 7 13-14" {...s} />
      <Path d="M48 82v14M41 89h14M362 120v10M357 125h10M240 232v12M234 238h12" {...s} strokeWidth={2.5} />
      <Path d="M30 232c60 10 120 14 180 12" {...s} strokeWidth={2.5} />
    </Svg>
  );
}
