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
  /** Light-on-dark styling for the auth panel. */
  dark?: boolean;
  ref?: Ref<TextInputInstance>;
}

const DARK = { text: '#F5F3EA', muted: 'rgba(245,243,234,0.74)', placeholder: 'rgba(245,243,234,0.5)', line: 'rgba(255,255,255,0.32)', focus: '#FFAD66', error: '#FDA4A4' };

export function Input({ label, error, hint, required, leftAddon, rightElement, showCount, dark, multiline, maxLength, value, ref, onFocus, onBlur, ...rest }: InputProps) {
  const [focused, setFocused] = useState(false);
  const errorColor = dark ? DARK.error : colors.error;
  return (
    <View style={styles.wrap}>
      <AppText variant="label" nativeID={`${label}-label`} color={dark ? DARK.text : undefined}>
        {label}
        {required ? <AppText variant="label" color={errorColor}> *</AppText> : null}
      </AppText>
      <View style={[styles.field, dark && styles.darkField, multiline && styles.multiField, focused && (dark ? styles.darkFocused : styles.focused), !!error && { borderColor: errorColor }]}>
        {leftAddon ? (
          <View style={[styles.addon, dark && styles.darkAddon]}>
            {typeof leftAddon === 'string' ? <AppText variant="bodyStrong" color={dark ? DARK.text : colors.textSecondary}>{leftAddon}</AppText> : leftAddon}
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
          placeholderTextColor={dark ? DARK.placeholder : colors.textMuted}
          onFocus={(e) => {
            setFocused(true);
            onFocus?.(e);
          }}
          onBlur={(e) => {
            setFocused(false);
            onBlur?.(e);
          }}
          style={[styles.input, dark && styles.darkInput, multiline && styles.multiline]}
          maxFontSizeMultiplier={1.6}
          textAlignVertical={multiline ? 'top' : 'center'}
        />
        {rightElement}
      </View>
      <View style={styles.meta}>
        {error ? (
          <AppText variant="small" color={errorColor} accessibilityRole="alert" style={styles.flex}>{error}</AppText>
        ) : hint ? (
          <AppText variant="caption" color={dark ? DARK.muted : undefined} style={styles.flex}>{hint}</AppText>
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
  darkField: { backgroundColor: 'transparent', borderColor: DARK.line },
  darkFocused: { borderColor: DARK.focus, borderWidth: 2, paddingHorizontal: spacing.md - 1 },
  darkAddon: { borderRightColor: DARK.line },
  darkInput: { color: DARK.text },
  addon: { paddingRight: spacing.sm, borderRightWidth: 1, borderRightColor: colors.border, height: 28, justifyContent: 'center' },
  input: { flex: 1, fontSize: fontSizes.md, color: colors.text, paddingVertical: 10 },
  multiline: { minHeight: 110 },
  meta: { flexDirection: 'row', gap: spacing.sm },
  flex: { flex: 1 },
});
