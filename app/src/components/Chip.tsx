import { Pressable, StyleSheet } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { colors, radii, TOUCH } from '@/theme';
import type { IoniconName } from '@/utils/icons';
import { AppText } from './AppText';

export interface ChipProps {
  label: string;
  selected?: boolean;
  onPress: () => void;
  icon?: IoniconName;
  accessibilityLabel?: string;
  /** "radio" for single-select groups, "checkbox" for multi-select. */
  role?: 'radio' | 'checkbox' | 'button';
}

export function Chip({ label, selected, onPress, icon, accessibilityLabel, role = 'button' }: ChipProps) {
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole={role}
      accessibilityLabel={accessibilityLabel ?? label}
      accessibilityState={role === 'button' ? { selected: !!selected } : { checked: !!selected }}
      style={({ pressed }) => [styles.chip, selected && styles.selected, pressed && styles.pressed]}
    >
      {(selected && role === 'checkbox') ? (
        <Ionicons name="checkmark-circle" size={16} color={colors.primary} />
      ) : icon ? (
        <Ionicons name={icon} size={16} color={selected ? colors.primary : colors.textSecondary} />
      ) : null}
      <AppText variant="small" color={selected ? colors.primary : colors.text} weight={selected ? '600' : '500'} numberOfLines={1}>
        {label}
      </AppText>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  chip: {
    minHeight: TOUCH - 4,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 14,
    borderRadius: radii.full,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.white,
  },
  selected: { backgroundColor: colors.primarySoft, borderColor: colors.primary },
  pressed: { opacity: 0.8 },
});
