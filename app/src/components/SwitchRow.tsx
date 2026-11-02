import { StyleSheet, Switch, View } from 'react-native';
import { colors, spacing, TOUCH } from '@/theme';
import { AppText } from './AppText';

export interface SwitchRowProps {
  label: string;
  description?: string;
  value: boolean;
  onValueChange: (v: boolean) => void;
  disabled?: boolean;
  error?: string;
}

export function SwitchRow({ label, description, value, onValueChange, disabled, error }: SwitchRowProps) {
  return (
    <View style={styles.wrap}>
      <View style={styles.row}>
        <View style={styles.text}>
          <AppText variant="bodyStrong">{label}</AppText>
          {description ? <AppText variant="small">{description}</AppText> : null}
        </View>
        <Switch
          value={value}
          onValueChange={onValueChange}
          disabled={disabled}
          accessibilityLabel={label}
          accessibilityHint={description}
          trackColor={{ true: colors.primary, false: colors.borderStrong }}
          thumbColor={colors.white}
          ios_backgroundColor={colors.borderStrong}
        />
      </View>
      {error ? <AppText variant="small" color={colors.error} accessibilityRole="alert">{error}</AppText> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 4 },
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, minHeight: TOUCH },
  text: { flex: 1, gap: 2 },
});
