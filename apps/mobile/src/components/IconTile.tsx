import { StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { radii, toneColors, type Tone } from '@/theme';
import type { IoniconName } from '@/utils/icons';

export function IconTile({ name, tone = 'primary', size = 40 }: { name: IoniconName; tone?: Tone; size?: number }) {
  const t = toneColors[tone];
  return (
    <View
      importantForAccessibility="no-hide-descendants"
      accessibilityElementsHidden
      style={[styles.tile, { width: size, height: size, backgroundColor: t.bg }]}
    >
      <Ionicons name={name} size={Math.round(size * 0.5)} color={t.fg} />
    </View>
  );
}

const styles = StyleSheet.create({
  tile: { alignItems: 'center', justifyContent: 'center', borderRadius: radii.md },
});
