import { Pressable, StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { colors, radii, spacing, TOUCH } from '@/theme';
import { AppText } from './AppText';

export interface CheckboxProps {
  label: string;
  checked: boolean;
  onChange: (v: boolean) => void;
  error?: string;
  description?: string;
}

export function Checkbox({ label, checked, onChange, error, description }: CheckboxProps) {
  return (
    <View style={styles.wrap}>
      <Pressable
        onPress={() => onChange(!checked)}
        accessibilityRole="checkbox"
        accessibilityState={{ checked }}
        accessibilityLabel={label}
        style={styles.row}
      >
        <View style={[styles.box, checked && styles.checked, !!error && !checked && styles.errorBox]}>
          {checked && <Ionicons name="checkmark" size={16} color={colors.white} />}
        </View>
        <View style={styles.text}>
          <AppText variant="body">{label}</AppText>
          {description ? <AppText variant="small">{description}</AppText> : null}
        </View>
      </Pressable>
      {error ? <AppText variant="small" color={colors.error} accessibilityRole="alert" style={styles.error}>{error}</AppText> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 4 },
  row: { flexDirection: 'row', alignItems: 'flex-start', gap: spacing.md, minHeight: TOUCH, paddingVertical: 8 },
  box: {
    width: 24,
    height: 24,
    marginTop: 0,
    borderRadius: radii.sm,
    borderWidth: 2,
    borderColor: colors.borderStrong,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.white,
  },
  checked: { backgroundColor: colors.primary, borderColor: colors.primary },
  errorBox: { borderColor: colors.error },
  text: { flex: 1, gap: 2 },
  error: { marginLeft: 36 },
});
