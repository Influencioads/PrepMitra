/**
 * PrepMitra AI design tokens — single source of truth for brand values.
 * Web: mirrored as CSS variables in apps/web/src/styles/index.css (@theme).
 * Mobile: consumed directly by apps/mobile/theme.
 */
export const colors = {
  // Brand: saffron (action) + peepal green (trust). No blue anywhere in the palette.
  primary: '#C2410C',
  primaryHover: '#A6370A',
  primarySoft: '#FCEBDD',
  secondary: '#1E5E47',
  secondarySoft: '#E3EFE8',
  accent: '#F28C28',
  accentSoft: '#FFF1DE',
  background: '#F4F3EC',
  card: '#FFFEFA',
  text: '#1C2321',
  textSecondary: '#5B6661',
  textMuted: '#8E9792',
  border: '#E3E2D8',
  borderStrong: '#CFCFC3',
  success: '#15803D',
  successSoft: '#EAF5EC',
  warning: '#D97706',
  warningText: '#92400E',
  warningSoft: '#FEF4E2',
  error: '#DC2626',
  errorSoft: '#FDEEEC',
  info: '#1E5E47',
  infoSoft: '#E8F1EC',
  white: '#FFFFFF',
  black: '#000000',
} as const;

/** Exam question palette colours (CBT convention). */
export const paletteColors = {
  'not-visited': { bg: '#EFEFE8', fg: '#4B5550', border: '#CFCFC3' },
  'not-answered': { bg: '#FDE2DF', fg: '#B91C1C', border: '#F5A39A' },
  answered: { bg: '#15803D', fg: '#FFFFFF', border: '#116632' },
  marked: { bg: '#7E22CE', fg: '#FFFFFF', border: '#6B21A8' },
  'answered-marked': { bg: '#C2410C', fg: '#FFFFFF', border: '#A6370A' },
} as const;

/** Categorical chart palette (colour-blind aware ordering). */
export const chartColors = ['#C2410C', '#1E5E47', '#D97706', '#7E22CE', '#65A30D', '#9F1239'] as const;

export const spacing = { xs: 4, sm: 8, md: 12, lg: 16, xl: 24, '2xl': 32, '3xl': 48 } as const;

export const radii = { sm: 6, md: 10, lg: 14, xl: 20, full: 999 } as const;

export const fontFamily = {
  sans: 'DM Sans',
  display: 'Bricolage Grotesque',
  fallback: 'system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif',
} as const;

export const fontSizes = { xs: 12, sm: 14, md: 16, lg: 18, xl: 20, '2xl': 24, '3xl': 30, '4xl': 36 } as const;

export const shadows = {
  card: '0 1px 2px rgba(28, 35, 33, 0.04), 0 1px 3px rgba(28, 35, 33, 0.06)',
  raised: '0 4px 12px rgba(15, 23, 42, 0.08)',
  overlay: '0 20px 40px rgba(15, 23, 42, 0.18)',
} as const;

export const tokens = { colors, paletteColors, chartColors, spacing, radii, fontFamily, fontSizes, shadows };
export type DesignTokens = typeof tokens;
