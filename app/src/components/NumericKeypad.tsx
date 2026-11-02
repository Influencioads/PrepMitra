import { Pressable, StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { colors, radii, spacing } from '@/theme';
import { AppText } from './AppText';

const KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '0', '.'] as const;

/**
 * On-screen keypad for numeric-answer (NAT) questions, like the CBT virtual
 * keypad. Keeps the system keyboard away so the question stays visible.
 */
export function NumericKeypad({ value, onChange, maxLength = 12 }: { value: string; onChange: (v: string) => void; maxLength?: number }) {
  const press = (k: (typeof KEYS)[number]) => {
    if (value.length >= maxLength) return;
    if (k === '-') {
      onChange(value.startsWith('-') ? value.slice(1) : `-${value}`);
      return;
    }
    if (k === '.' && value.includes('.')) return;
    const decimals = value.split('.')[1];
    if (decimals !== undefined && decimals.length >= 4 && k !== '.') return;
    onChange(value + k);
  };
  return (
    <View style={styles.wrap}>
      <View
        style={styles.display}
        accessible
        accessibilityRole="text"
        accessibilityLabel={value ? `Your answer: ${value}` : 'No answer entered'}
        accessibilityLiveRegion="polite"
      >
        <AppText style={styles.value} color={value ? colors.text : colors.textMuted}>{value || 'Enter your answer'}</AppText>
      </View>
      <View style={styles.grid}>
        {KEYS.map((k) => (
          <Pressable
            key={k}
            onPress={() => press(k)}
            accessibilityRole="keyboardkey"
            accessibilityLabel={k === '-' ? 'Toggle minus sign' : k === '.' ? 'Decimal point' : k}
            style={({ pressed }) => [styles.key, pressed && styles.pressed]}
          >
            <AppText style={styles.keyText}>{k === '-' ? '±' : k}</AppText>
          </Pressable>
        ))}
        <Pressable
          onPress={() => onChange(value.slice(0, -1))}
          accessibilityRole="keyboardkey"
          accessibilityLabel="Backspace"
          style={({ pressed }) => [styles.key, styles.wide, pressed && styles.pressed]}
        >
          <Ionicons name="backspace-outline" size={22} color={colors.text} />
        </Pressable>
        <Pressable
          onPress={() => onChange('')}
          accessibilityRole="keyboardkey"
          accessibilityLabel="Clear all"
          style={({ pressed }) => [styles.key, styles.wide, pressed && styles.pressed]}
        >
          <AppText variant="smallStrong">Clear all</AppText>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: spacing.md },
  display: {
    minHeight: 56,
    borderWidth: 2,
    borderColor: colors.primary,
    borderRadius: radii.md,
    justifyContent: 'center',
    paddingHorizontal: spacing.lg,
    backgroundColor: colors.white,
  },
  value: { fontSize: 24, fontWeight: '700', fontVariant: ['tabular-nums'] },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  key: {
    width: '31.5%',
    flexGrow: 1,
    height: 50,
    borderRadius: radii.md,
    backgroundColor: '#F1F5F9',
    alignItems: 'center',
    justifyContent: 'center',
  },
  wide: { width: '48%' },
  pressed: { backgroundColor: '#E2E8F0' },
  keyText: { fontSize: 20, fontWeight: '600', color: colors.text },
});
