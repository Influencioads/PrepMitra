import { useState, type ReactNode, type Ref } from 'react';
import { StyleSheet, TextInput, View, type TextInputInstance, type TextInputProps } from 'react-native';
import { colors, fontSizes, radii, spacing, TOUCH } from '@/theme';
import { AppText } from './AppText';

export interface InputProps extends Omit<TextInputProps, 'style'> {
  label: string;
  error?: string;
  hint?: string;
  required?: boolean;
  /** Fixed prefix inside the field, e.g. "+91". */
  leftAddon?: ReactNode;
  rightElement?: ReactNode;
  showCount?: boolean;
  ref?: Ref<TextInputInstance>;
}

export function Input({ label, error, hint, required, leftAddon, rightElement, showCount, multiline, maxLength, value, ref, onFocus, onBlur, ...rest }: InputProps) {
  const [focused, setFocused] = useState(false);
  return (
    <View style={styles.wrap}>
      <AppText variant="label" nativeID={`${label}-label`}>
        {label}
        {required ? <AppText variant="label" color={colors.error}> *</AppText> : null}
      </AppText>
      <View style={[styles.field, multiline && styles.multiField, focused && styles.focused, !!error && styles.errorField]}>
        {leftAddon ? (
          <View style={styles.addon}>
            {typeof leftAddon === 'string' ? <AppText variant="bodyStrong" color={colors.textSecondary}>{leftAddon}</AppText> : leftAddon}
          </View>
        ) : null}
        <TextInput
          ref={ref}
          {...rest}
          value={value}
          multiline={multiline}
          maxLength={maxLength}
          accessibilityLabel={label}
          accessibilityHint={error ?? hint}
          placeholderTextColor={colors.textMuted}
          onFocus={(e) => {
            setFocused(true);
            onFocus?.(e);
          }}
          onBlur={(e) => {
            setFocused(false);
            onBlur?.(e);
          }}
          style={[styles.input, multiline && styles.multiline]}
          maxFontSizeMultiplier={1.6}
          textAlignVertical={multiline ? 'top' : 'center'}
        />
        {rightElement}
      </View>
      <View style={styles.meta}>
        {error ? (
          <AppText variant="small" color={colors.error} accessibilityRole="alert" style={styles.flex}>{error}</AppText>
        ) : hint ? (
          <AppText variant="caption" style={styles.flex}>{hint}</AppText>
        ) : <View style={styles.flex} />}
        {showCount && maxLength ? (
          <AppText variant="caption">{(value ?? '').length}/{maxLength}</AppText>
        ) : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 6 },
  field: {
    flexDirection: 'row',
    alignItems: 'center',
    minHeight: TOUCH + 4,
    borderWidth: 1,
    borderColor: colors.borderStrong,
    borderRadius: radii.md,
    backgroundColor: colors.white,
    paddingHorizontal: spacing.md,
    gap: spacing.sm,
  },
  multiField: { alignItems: 'flex-start', paddingVertical: spacing.sm },
  focused: { borderColor: colors.primary, borderWidth: 2, paddingHorizontal: spacing.md - 1 },
  errorField: { borderColor: colors.error },
  addon: { paddingRight: spacing.sm, borderRightWidth: 1, borderRightColor: colors.border, height: 28, justifyContent: 'center' },
  input: { flex: 1, fontSize: fontSizes.md, color: colors.text, paddingVertical: 10 },
  multiline: { minHeight: 110 },
  meta: { flexDirection: 'row', gap: spacing.sm },
  flex: { flex: 1 },
});
