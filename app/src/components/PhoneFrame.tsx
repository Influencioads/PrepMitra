import type { ReactNode } from 'react';
import { Platform, StyleSheet, View, useWindowDimensions } from 'react-native';
import { colors } from '@/theme';

/** Widest the app is drawn on the web. Above this the app sits in a phone-sized frame. */
const APP_MAX_WIDTH = 430;
const APP_MAX_HEIGHT = 900;
/** Screens wider than this get the framed "device" look instead of a full-bleed layout. */
const FRAME_BREAKPOINT = 600;

/**
 * Keeps the app looking like an app when it runs in a desktop browser (Expo web).
 * Native builds and phone-width browsers render children unchanged; wider browser
 * windows centre the app in a phone-sized frame so screens never stretch into a
 * website-style full-width layout.
 */
export function PhoneFrame({ children }: { children: ReactNode }) {
  const { width, height } = useWindowDimensions();
  if (Platform.OS !== 'web' || width < FRAME_BREAKPOINT) return <>{children}</>;
  const frameHeight = Math.min(height - 48, APP_MAX_HEIGHT);
  return (
    <View style={styles.backdrop}>
      <View style={[styles.device, { height: frameHeight }]}>{children}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#E7E3D6',
  },
  device: {
    width: APP_MAX_WIDTH,
    maxWidth: '100%',
    overflow: 'hidden',
    borderRadius: 36,
    borderWidth: 10,
    borderColor: '#1C2321',
    backgroundColor: colors.background,
    // Web-only shadow; native never renders this component's frame.
    boxShadow: '0 30px 60px rgba(28,35,33,0.25)',
  },
});
