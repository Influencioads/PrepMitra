import { Pressable, StyleSheet, View } from 'react-native';
import { colors, spacing, TOUCH } from '@/theme';
import { AppText } from './AppText';

export function SectionHeader({ title, actionLabel, onAction, subtitle }: { title: string; subtitle?: string; actionLabel?: string; onAction?: () => void }) {
  return (
    <View style={styles.row}>
      <View style={styles.text}>
        <AppText variant="h3" accessibilityRole="header">{title}</AppText>
        {subtitle ? <AppText variant="small">{subtitle}</AppText> : null}
      </View>
      {actionLabel && onAction ? (
        <Pressable onPress={onAction} accessibilityRole="link" accessibilityLabel={`${actionLabel}: ${title}`} hitSlop={8} style={styles.action}>
          <AppText variant="smallStrong" color={colors.primary}>{actionLabel}</AppText>
        </Pressable>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.md, marginTop: spacing.sm },
  text: { flex: 1 },
  action: { minHeight: TOUCH, justifyContent: 'center', paddingHorizontal: 4 },
});
