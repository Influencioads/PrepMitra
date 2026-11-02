import { Text, type TextProps } from 'react-native';
import { text, type TextVariant } from '@/theme';

export interface AppTextProps extends TextProps {
  variant?: TextVariant;
  color?: string;
  align?: 'left' | 'center' | 'right';
  weight?: '400' | '500' | '600' | '700' | '800';
}

/** Text with the app's type scale. Font scaling stays enabled for accessibility. */
export function AppText({ variant = 'body', color, align, weight, style, maxFontSizeMultiplier = 1.6, ...rest }: AppTextProps) {
  return (
    <Text
      {...rest}
      maxFontSizeMultiplier={maxFontSizeMultiplier}
      style={[text[variant], color ? { color } : null, align ? { textAlign: align } : null, weight ? { fontWeight: weight } : null, style]}
    />
  );
}
