import { StyleSheet, View, type StyleProp, type ViewStyle } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { radii, toneColors, type Tone } from '@/theme';
import type { IoniconName } from '@/utils/icons';
import { AppText } from './AppText';

export interface BadgeProps {
  label: string;
  tone?: Tone;
  icon?: IoniconName;
  style?: StyleProp<ViewStyle>;
}

export function Badge({ label, tone = 'neutral', icon, style }: BadgeProps) {
  const t = toneColors[tone];
  return (
    <View style={[styles.badge, { backgroundColor: t.bg, borderColor: t.border }, style]}>
      {icon && <Ionicons name={icon} size={12} color={t.fg} />}
      <AppText variant="caption" style={{ color: t.fg, fontWeight: '600' }} numberOfLines={1}>
        {label}
      </AppText>
    </View>
  );
}

/** Small "Demo" marker used wherever data or analysis is simulated. */
export function DemoBadge({ label = 'Demo data' }: { label?: string }) {
  return <Badge label={label} tone="warning" icon="flask-outline" />;
}

const styles = StyleSheet.create({
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: radii.full,
    borderWidth: 1,
  },
});
