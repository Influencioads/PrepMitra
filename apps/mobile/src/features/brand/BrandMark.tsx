import { StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { APP_NAME } from '@prepmitra/shared';
import { AppText } from '@/components';
import { colors, radii } from '@/theme';

/** Logo mark + word mark (drawn natively; no image assets needed). */
export function BrandMark({ size = 48, showName = true, inverted = false }: { size?: number; showName?: boolean; inverted?: boolean }) {
  return (
    <View style={styles.row} accessible accessibilityRole="image" accessibilityLabel={APP_NAME}>
      <View style={[styles.mark, { width: size, height: size, borderRadius: size * 0.28 }, inverted && styles.markInverted]}>
        <Ionicons name="school" size={size * 0.55} color={inverted ? colors.primary : colors.white} />
        <View style={[styles.spark, { right: -size * 0.08, top: -size * 0.08 }]}>
          <Ionicons name="sparkles" size={size * 0.3} color={colors.warning} />
        </View>
      </View>
      {showName ? (
        <AppText style={{ fontSize: size * 0.46, fontWeight: '800', color: inverted ? colors.white : colors.text }}>
          PrepMitra <AppText style={{ fontSize: size * 0.46, fontWeight: '800', color: inverted ? '#F6C9A6' : colors.primary }}>AI</AppText>
        </AppText>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  mark: { backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center', borderRadius: radii.lg },
  markInverted: { backgroundColor: colors.white },
  spark: { position: 'absolute' },
});
