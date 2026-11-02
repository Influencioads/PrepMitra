import { useEffect, useRef } from 'react';
import { StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { formatClock, remainingSeconds } from '@prepmitra/shared';
import { useNow } from '@/hooks/useNow';
import { colors, radii } from '@/theme';
import { AppText } from './AppText';

export interface CountdownTimerProps {
  endsAt: string;
  onExpire?: () => void;
  /** Turn amber below this many seconds (default 5 min) and red below 1 min. */
  warnBelowSec?: number;
  paused?: boolean;
}

/** Exam countdown derived from the absolute end time, so it survives restarts. */
export function CountdownTimer({ endsAt, onExpire, warnBelowSec = 300, paused }: CountdownTimerProps) {
  const now = useNow(1000, !paused);
  const left = remainingSeconds({ endsAt }, now);
  const fired = useRef(false);

  useEffect(() => {
    if (left <= 0 && !fired.current && !paused) {
      fired.current = true;
      onExpire?.();
    }
  }, [left, onExpire, paused]);

  const critical = left <= 60;
  const warn = left <= warnBelowSec;
  const bg = critical ? colors.errorSoft : warn ? colors.warningSoft : colors.primarySoft;
  const fg = critical ? colors.error : warn ? colors.warningText : colors.primary;
  const minutes = Math.ceil(left / 60);
  return (
    <View
      style={[styles.pill, { backgroundColor: bg }]}
      accessible
      accessibilityRole="timer"
      accessibilityLabel={`Time remaining ${minutes} minute${minutes === 1 ? '' : 's'}`}
      accessibilityLiveRegion={critical ? 'polite' : 'none'}
    >
      <Ionicons name="time-outline" size={16} color={fg} />
      <AppText variant="bodyStrong" color={fg} style={styles.mono}>{formatClock(left)}</AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  pill: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 10, paddingVertical: 6, borderRadius: radii.full },
  mono: { fontVariant: ['tabular-nums'] },
});
