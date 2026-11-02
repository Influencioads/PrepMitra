import { Pressable, StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { colors, TOUCH } from '@/theme';

export function RatingStars({ value, onChange, label = 'Rate this report' }: { value: number; onChange: (v: number) => void; label?: string }) {
  return (
    <View style={styles.row} accessibilityRole="adjustable" accessibilityLabel={label} accessibilityValue={{ min: 0, max: 5, now: value }}>
      {[1, 2, 3, 4, 5].map((n) => (
        <Pressable
          key={n}
          onPress={() => onChange(n)}
          accessibilityRole="button"
          accessibilityLabel={`${n} star${n > 1 ? 's' : ''}`}
          accessibilityState={{ selected: value === n }}
          style={styles.star}
        >
          <Ionicons name={n <= value ? 'star' : 'star-outline'} size={30} color={n <= value ? colors.warning : colors.borderStrong} />
        </Pressable>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', gap: 2 },
  star: { width: TOUCH, height: TOUCH, alignItems: 'center', justifyContent: 'center' },
});
