import type { ReactNode } from 'react';
import { StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { colors, spacing, type Tone } from '@/theme';
import type { IoniconName } from '@/utils/icons';
import { AppText } from './AppText';
import { Card } from './Card';
import { IconTile } from './IconTile';

export interface StatCardProps {
  label: string;
  value: string | number;
  icon: IoniconName;
  tone?: Tone;
  hint?: ReactNode;
  trend?: number;
  onPress?: () => void;
}

/** Compact KPI tile. Two per row on phones. */
export function StatCard({ label, value, icon, tone = 'primary', hint, trend, onPress }: StatCardProps) {
  const up = (trend ?? 0) >= 0;
  return (
    <Card style={styles.card} onPress={onPress} accessibilityLabel={onPress ? `${label}: ${value}` : undefined}>
      <View style={styles.top}>
        <IconTile name={icon} tone={tone} size={34} />
        {trend !== undefined && trend !== 0 && (
          <View style={styles.trend} accessibilityLabel={`${up ? 'Up' : 'Down'} ${Math.abs(trend)} points vs previous`}>
            <Ionicons name={up ? 'arrow-up' : 'arrow-down'} size={12} color={up ? colors.success : colors.error} />
            <AppText variant="caption" color={up ? colors.success : colors.error} weight="600">
              {Math.abs(trend)}
            </AppText>
          </View>
        )}
      </View>
      <AppText variant="h2" style={styles.value} numberOfLines={1} adjustsFontSizeToFit>
        {value}
      </AppText>
      <AppText variant="caption" numberOfLines={2}>{label}</AppText>
      {typeof hint === 'string' ? (
        hint ? <AppText variant="caption" color={colors.textMuted} numberOfLines={1}>{hint}</AppText> : null
      ) : (
        hint
      )}
    </Card>
  );
}

const styles = StyleSheet.create({
  card: { flex: 1, minWidth: 0, padding: spacing.md, gap: 4 },
  top: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 4 },
  trend: { flexDirection: 'row', alignItems: 'center', gap: 2 },
  value: { marginTop: 2 },
});
