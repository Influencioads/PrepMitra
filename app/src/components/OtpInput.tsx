import { useRef, useState } from 'react';
import { Pressable, StyleSheet, TextInput, View, type TextInputInstance } from 'react-native';
import { colors, radii, spacing } from '@/theme';
import { AppText } from './AppText';

export interface OtpInputProps {
  value: string;
  onChange: (v: string) => void;
  length?: number;
  error?: string;
  autoFocus?: boolean;
  onComplete?: (v: string) => void;
}

/**
 * Six large digit boxes backed by one hidden TextInput, so SMS autofill
 * (oneTimeCode / sms-otp) and paste both work.
 */
export function OtpInput({ value, onChange, length = 6, error, autoFocus = true, onComplete }: OtpInputProps) {
  const ref = useRef<TextInputInstance>(null);
  const [focused, setFocused] = useState(false);
  const digits = value.split('');
  return (
    <View style={styles.wrap}>
      <Pressable
        onPress={() => ref.current?.focus()}
        accessibilityRole="none"
        importantForAccessibility="no-hide-descendants"
        accessibilityElementsHidden
        style={styles.row}
      >
        {Array.from({ length }, (_, i) => {
          const active = focused && (i === digits.length || (i === length - 1 && digits.length === length));
          return (
            <View key={i} style={[styles.box, active && styles.active, !!error && styles.error, !!digits[i] && styles.filled]}>
              <AppText style={styles.digit}>{digits[i] ?? ''}</AppText>
            </View>
          );
        })}
      </Pressable>
      <TextInput
        ref={ref}
        value={value}
        onChangeText={(t) => {
          const clean = t.replace(/\D/g, '').slice(0, length);
          onChange(clean);
          if (clean.length === length) onComplete?.(clean);
        }}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        keyboardType="number-pad"
        textContentType="oneTimeCode"
        autoComplete="sms-otp"
        maxLength={length}
        autoFocus={autoFocus}
        accessibilityLabel={`Verification code, ${length} digits`}
        accessibilityHint={error}
        caretHidden
        style={styles.hidden}
      />
      {error ? <AppText variant="small" color={colors.error} accessibilityRole="alert" align="center">{error}</AppText> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: spacing.sm },
  row: { flexDirection: 'row', justifyContent: 'space-between', gap: 8 },
  box: {
    flex: 1,
    maxWidth: 52,
    aspectRatio: 0.85,
    borderRadius: radii.md,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    backgroundColor: colors.white,
    alignItems: 'center',
    justifyContent: 'center',
  },
  filled: { borderColor: colors.primary, backgroundColor: colors.primarySoft },
  active: { borderColor: colors.primary, borderWidth: 2.5 },
  error: { borderColor: colors.error },
  digit: { fontSize: 26, fontWeight: '700', color: colors.text },
  hidden: { position: 'absolute', opacity: 0.011, width: 1, height: 1 },
});
