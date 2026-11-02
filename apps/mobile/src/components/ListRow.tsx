import type { ReactNode } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { colors, spacing, type Tone } from '@/theme';
import type { IoniconName } from '@/utils/icons';
import { AppText } from './AppText';
import { IconTile } from './IconTile';

export interface ListRowProps {
  title: string;
  subtitle?: string;
  icon?: IoniconName;
  iconTone?: Tone;
  right?: ReactNode;
  onPress?: () => void;
  chevron?: boolean;
  destructive?: boolean;
  accessibilityHint?: string;
}

export function ListRow({ title, subtitle, icon, iconTone = 'primary', right, onPress, chevron = !!onPress, destructive, accessibilityHint }: ListRowProps) {
  const content = (
    <>
      {icon && <IconTile name={icon} tone={destructive ? 'error' : iconTone} size={36} />}
      <View style={styles.text}>
        <AppText variant="bodyStrong" color={destructive ? colors.error : colors.text}>{title}</AppText>
        {subtitle ? <AppText variant="small" numberOfLines={2}>{subtitle}</AppText> : null}
      </View>
      {right}
      {chevron && <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />}
    </>
  );
  if (!onPress) return <View style={styles.row}>{content}</View>;
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel={subtitle ? `${title}. ${subtitle}` : title}
      accessibilityHint={accessibilityHint}
      style={({ pressed }) => [styles.row, pressed && styles.pressed]}
    >
      {content}
    </Pressable>
  );
}

export function Divider() {
  return <View style={styles.divider} />;
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, minHeight: 56, paddingVertical: spacing.sm },
  pressed: { opacity: 0.7 },
  text: { flex: 1, gap: 2 },
  divider: { height: StyleSheet.hairlineWidth, backgroundColor: colors.border },
});
