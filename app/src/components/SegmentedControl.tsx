import { Pressable, ScrollView, StyleSheet, View } from 'react-native';
import { colors, radii, TOUCH } from '@/theme';
import { AppText } from './AppText';

export interface Segment<T extends string> {
  value: T;
  label: string;
}

export interface SegmentedControlProps<T extends string> {
  segments: Segment<T>[];
  value: T;
  onChange: (v: T) => void;
  /** Scrollable pills for many tabs; equal-width segments otherwise. */
  scrollable?: boolean;
  accessibilityLabel?: string;
}

export function SegmentedControl<T extends string>({ segments, value, onChange, scrollable, accessibilityLabel }: SegmentedControlProps<T>) {
  const items = segments.map((s) => {
    const active = s.value === value;
    return (
      <Pressable
        key={s.value}
        onPress={() => onChange(s.value)}
        accessibilityRole="tab"
        accessibilityState={{ selected: active }}
        accessibilityLabel={s.label}
        style={[styles.item, !scrollable && styles.flex, active && styles.active]}
      >
        <AppText variant="small" weight={active ? '700' : '500'} color={active ? colors.primary : colors.textSecondary} numberOfLines={1}>
          {s.label}
        </AppText>
      </Pressable>
    );
  });
  if (scrollable) {
    return (
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        accessibilityRole="tablist"
        accessibilityLabel={accessibilityLabel}
        contentContainerStyle={[styles.track, styles.scrollTrack]}
      >
        {items}
      </ScrollView>
    );
  }
  return (
    <View accessibilityRole="tablist" accessibilityLabel={accessibilityLabel} style={styles.track}>
      {items}
    </View>
  );
}

const styles = StyleSheet.create({
  track: { flexDirection: 'row', backgroundColor: '#EEF2F7', borderRadius: radii.md, padding: 4, gap: 4 },
  scrollTrack: { alignSelf: 'flex-start' },
  item: { minHeight: TOUCH - 6, paddingHorizontal: 14, alignItems: 'center', justifyContent: 'center', borderRadius: radii.sm },
  flex: { flex: 1 },
  active: { backgroundColor: colors.white, shadowColor: '#1C2321', shadowOpacity: 0.08, shadowRadius: 3, shadowOffset: { width: 0, height: 1 }, elevation: 1 },
});
