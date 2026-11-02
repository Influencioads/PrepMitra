import { StyleSheet, View } from 'react-native';
import { initials } from '@prepmitra/shared';
import { colors } from '@/theme';
import { AppText } from './AppText';

export function Avatar({ name, size = 48 }: { name: string; size?: number }) {
  return (
    <View
      accessibilityElementsHidden
      importantForAccessibility="no-hide-descendants"
      style={[styles.avatar, { width: size, height: size, borderRadius: size / 2 }]}
    >
      <AppText style={{ color: colors.white, fontSize: size * 0.38, fontWeight: '700' }}>{initials(name) || '?'}</AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  avatar: { backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center' },
});
