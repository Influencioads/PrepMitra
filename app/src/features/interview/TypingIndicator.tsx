import { useEffect, useState } from 'react';
import { Animated, StyleSheet, View } from 'react-native';
import { AppText } from '@/components';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import { colors, radii, spacing } from '@/theme';

/** Three bouncing dots shown while the (scripted) interviewer "thinks". */
export function TypingIndicator({ label = 'Interviewer is typing' }: { label?: string }) {
  const [dots] = useState(() => [0, 1, 2].map(() => new Animated.Value(0)));
  const reduceMotion = useReducedMotion();
  useEffect(() => {
    if (reduceMotion) {
      dots.forEach((d) => d.setValue(1));
      return;
    }
    const anims = dots.map((d, i) =>
      Animated.loop(
        Animated.sequence([
          Animated.delay(i * 150),
          Animated.timing(d, { toValue: 1, duration: 300, useNativeDriver: true }),
          Animated.timing(d, { toValue: 0, duration: 300, useNativeDriver: true }),
          Animated.delay((2 - i) * 150),
        ]),
      ),
    );
    anims.forEach((a) => a.start());
    return () => anims.forEach((a) => a.stop());
  }, [dots, reduceMotion]);
  return (
    <View style={styles.row} accessible accessibilityLabel={label} accessibilityLiveRegion="polite">
      <View style={styles.bubble}>
        {dots.map((d, i) => (
          <Animated.View
            key={i}
            style={[styles.dot, { opacity: d.interpolate({ inputRange: [0, 1], outputRange: [0.35, 1] }), transform: [{ translateY: d.interpolate({ inputRange: [0, 1], outputRange: [0, -4] }) }] }]}
          />
        ))}
      </View>
      <AppText variant="caption">{label}…</AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  bubble: { flexDirection: 'row', gap: 5, paddingHorizontal: spacing.md, paddingVertical: spacing.md, borderRadius: radii.lg, backgroundColor: colors.card, borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border },
  dot: { width: 7, height: 7, borderRadius: 4, backgroundColor: colors.secondary },
});
