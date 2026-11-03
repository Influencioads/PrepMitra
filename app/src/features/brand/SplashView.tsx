import { ActivityIndicator, StyleSheet, View } from 'react-native';
import { APP_TAGLINE } from '@prepmitra/shared';
import { AppText } from '@/components';
import { colors } from '@/theme';
import { BrandMark } from './BrandMark';

/** Shown while persisted stores rehydrate from AsyncStorage. */
export function SplashView() {
  return (
    <View style={styles.wrap} accessibilityLabel="Loading PrepMitra AI" accessibilityRole="progressbar">
      <BrandMark size={56} inverted />
      <AppText variant="small" color="#F3DCC8" align="center">{APP_TAGLINE}</AppText>
      <ActivityIndicator color={colors.white} style={styles.spinner} />
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { flex: 1, backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center', gap: 16, padding: 24 },
  spinner: { marginTop: 12 },
});
