import type { ReactNode } from 'react';
import { ActivityIndicator, Pressable, StyleSheet, View, type StyleProp, type ViewStyle } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { colors, radii, TOUCH } from '@/theme';
import type { IoniconName } from '@/utils/icons';
import { AppText } from './AppText';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'soft' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps {
  title: string;
  onPress?: () => void;
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  disabled?: boolean;
  leftIcon?: IoniconName;
  rightIcon?: IoniconName;
  fullWidth?: boolean;
  style?: StyleProp<ViewStyle>;
  accessibilityLabel?: string;
  accessibilityHint?: string;
  children?: ReactNode;
  testID?: string;
}

const VARIANTS: Record<ButtonVariant, { bg: string; fg: string; border: string; pressed: string }> = {
  primary: { bg: colors.primary, fg: colors.white, border: colors.primary, pressed: colors.primaryHover },
  secondary: { bg: colors.secondary, fg: colors.white, border: colors.secondary, pressed: '#174A38' },
  outline: { bg: colors.white, fg: colors.text, border: colors.borderStrong, pressed: '#F1F5F9' },
  ghost: { bg: 'transparent', fg: colors.primary, border: 'transparent', pressed: colors.primarySoft },
  soft: { bg: colors.primarySoft, fg: colors.primary, border: colors.primarySoft, pressed: '#F9DCC6' },
  danger: { bg: colors.error, fg: colors.white, border: colors.error, pressed: '#B91C1C' },
};

const SIZES: Record<ButtonSize, { height: number; px: number; font: number; icon: number }> = {
  sm: { height: TOUCH, px: 12, font: 14, icon: 16 },
  md: { height: 48, px: 16, font: 15, icon: 18 },
  lg: { height: 54, px: 20, font: 16, icon: 20 },
};

export function Button({
  title, onPress, variant = 'primary', size = 'md', loading, disabled, leftIcon, rightIcon, fullWidth, style,
  accessibilityLabel, accessibilityHint, testID,
}: ButtonProps) {
  const v = VARIANTS[variant];
  const s = SIZES[size];
  const inactive = disabled || loading;
  return (
    <Pressable
      testID={testID}
      onPress={inactive ? undefined : onPress}
      accessibilityRole="button"
      accessibilityLabel={accessibilityLabel ?? title}
      accessibilityHint={accessibilityHint}
      accessibilityState={{ disabled: !!inactive, busy: !!loading }}
      hitSlop={size === 'sm' ? 4 : 0}
      style={({ pressed }) => [
        styles.base,
        {
          minHeight: s.height,
          paddingHorizontal: s.px,
          backgroundColor: pressed && !inactive ? v.pressed : v.bg,
          borderColor: v.border,
          opacity: disabled && !loading ? 0.5 : 1,
        },
        fullWidth && styles.full,
        style,
      ]}
    >
      {loading ? (
        <ActivityIndicator color={v.fg} size="small" accessibilityLabel="Loading" />
      ) : (
        leftIcon && <Ionicons name={leftIcon} size={s.icon} color={v.fg} />
      )}
      <View style={styles.labelWrap}>
        <AppText numberOfLines={2} align="center" style={{ color: v.fg, fontSize: s.font, fontWeight: '600', lineHeight: s.font + 6 }}>
          {title}
        </AppText>
      </View>
      {rightIcon && !loading && <Ionicons name={rightIcon} size={s.icon} color={v.fg} />}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    borderRadius: radii.md,
    borderWidth: 1,
    paddingVertical: 8,
  },
  full: { alignSelf: 'stretch' },
  labelWrap: { flexShrink: 1 },
});
