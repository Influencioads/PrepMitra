import { Platform, type TextStyle, type ViewStyle } from 'react-native';
import { chartColors, colors, fontSizes, paletteColors, radii, spacing } from '@prepmitra/shared';

/**
 * Mobile theme. Brand values come from the shared design tokens so web and
 * mobile stay in sync; this module only adds native-specific pieces
 * (shadows/elevation, text presets, touch-target sizes).
 */
export { chartColors, colors, fontSizes, paletteColors, radii, spacing };

/** Minimum touch target (Apple HIG 44pt / Material 48dp). */
export const TOUCH = 44;

const shadow = (elevation: number, opacity: number, radius: number, y: number): ViewStyle =>
  Platform.select<ViewStyle>({
    android: { elevation },
    default: {
      shadowColor: colors.text,
      shadowOpacity: opacity,
      shadowRadius: radius,
      shadowOffset: { width: 0, height: y },
    },
  });

export const shadows = {
  card: shadow(2, 0.06, 6, 2),
  raised: shadow(6, 0.1, 12, 4),
  overlay: shadow(16, 0.18, 24, 10),
};

const family = Platform.select({ ios: 'System', android: 'sans-serif', default: undefined });
const familyMedium = Platform.select({ ios: 'System', android: 'sans-serif-medium', default: undefined });

export const text = {
  display: { fontFamily: family, fontSize: fontSizes['3xl'], fontWeight: '800', color: colors.text, lineHeight: 36 },
  h1: { fontFamily: family, fontSize: fontSizes['2xl'], fontWeight: '700', color: colors.text, lineHeight: 30 },
  h2: { fontFamily: family, fontSize: fontSizes.xl, fontWeight: '700', color: colors.text, lineHeight: 26 },
  h3: { fontFamily: familyMedium, fontSize: fontSizes.lg, fontWeight: '600', color: colors.text, lineHeight: 24 },
  body: { fontFamily: family, fontSize: fontSizes.md, fontWeight: '400', color: colors.text, lineHeight: 22 },
  bodyStrong: { fontFamily: familyMedium, fontSize: fontSizes.md, fontWeight: '600', color: colors.text, lineHeight: 22 },
  small: { fontFamily: family, fontSize: fontSizes.sm, fontWeight: '400', color: colors.textSecondary, lineHeight: 20 },
  smallStrong: { fontFamily: familyMedium, fontSize: fontSizes.sm, fontWeight: '600', color: colors.text, lineHeight: 20 },
  caption: { fontFamily: family, fontSize: fontSizes.xs, fontWeight: '400', color: colors.textSecondary, lineHeight: 16 },
  label: { fontFamily: familyMedium, fontSize: fontSizes.sm, fontWeight: '600', color: colors.text, lineHeight: 20 },
} satisfies Record<string, TextStyle>;

export type TextVariant = keyof typeof text;

export type Tone = 'neutral' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';

export const toneColors: Record<Tone, { bg: string; fg: string; border: string }> = {
  neutral: { bg: '#F1F5F9', fg: '#334155', border: colors.border },
  primary: { bg: colors.primarySoft, fg: colors.primary, border: '#F6C9A6' },
  secondary: { bg: colors.secondarySoft, fg: colors.secondary, border: '#BFD8CA' },
  success: { bg: colors.successSoft, fg: colors.success, border: '#BBF7D0' },
  warning: { bg: colors.warningSoft, fg: colors.warningText, border: '#FDE68A' },
  error: { bg: colors.errorSoft, fg: colors.error, border: '#FECACA' },
  info: { bg: colors.infoSoft, fg: colors.info, border: '#BAE6FD' },
};

/** Accuracy/score → tone used by badges and bars across the app (matches web). */
export const accuracyTone = (value: number): Tone => (value >= 75 ? 'success' : value >= 50 ? 'warning' : 'error');

/** Handwriting for short notes (red pen, Mitra's chalk). Loaded in the root layout; falls back to the system font. */
export const fonts = {
  hand: 'Kalam_400Regular',
  handBold: 'Kalam_700Bold',
};

/** Concept B surfaces: the answer sheet and the blackboard. Mirrors the web tokens. */
export const paper = {
  paper: '#FBF8EF',
  rule: '#ECE6D4',
  margin: 'rgba(215,38,61,0.28)',
  pen: '#D7263D',
  chalk: '#17392C',
  chalkDeep: '#10241C',
  chalkText: '#F5F3EA',
  chalkMuted: 'rgba(245,243,234,0.7)',
  chalkLine: 'rgba(245,243,234,0.3)',
  marigold: '#FFD27A',
  wood: '#5C3A1E',
  woodLight: '#7A4E2A',
  ink: '#1C2321',
  stickyYellow: '#FFF3C4',
  stickyGreen: '#DDEFE4',
  stickyPurple: '#F3E8FA',
};

/** Hard offset shadow used on paper cards (a flat "printed" look). */
export const hardShadow = (color = '#1C2321', x = 4, y = 4): ViewStyle =>
  Platform.select<ViewStyle>({
    android: { elevation: 0, borderBottomWidth: 0 },
    default: { shadowColor: color, shadowOpacity: 1, shadowRadius: 0, shadowOffset: { width: x, height: y } },
  });
