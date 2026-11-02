import type { ReactNode } from 'react';
import { StyleSheet, View, type StyleProp, type ViewStyle } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { radii, spacing, toneColors, type Tone } from '@/theme';
import type { IoniconName } from '@/utils/icons';
import { AppText } from './AppText';

const ICON: Partial<Record<Tone, IoniconName>> = {
  info: 'information-circle',
  warning: 'warning',
  error: 'alert-circle',
  success: 'checkmark-circle',
  primary: 'sparkles',
  neutral: 'information-circle',
  secondary: 'sparkles',
};

export interface NoticeProps {
  tone?: Tone;
  title?: string;
  children?: ReactNode;
  action?: ReactNode;
  style?: StyleProp<ViewStyle>;
  icon?: IoniconName;
}

/** Inline callout for disclaimers, hints and warnings. */
export function Notice({ tone = 'info', title, children, action, style, icon }: NoticeProps) {
  const t = toneColors[tone];
  return (
    <View
      accessible
      accessibilityRole={tone === 'error' ? 'alert' : 'text'}
      style={[styles.box, { backgroundColor: t.bg, borderColor: t.border }, style]}
    >
      <Ionicons name={icon ?? ICON[tone] ?? 'information-circle'} size={20} color={t.fg} style={styles.icon} />
      <View style={styles.body}>
        {title ? <AppText variant="smallStrong" color={t.fg}>{title}</AppText> : null}
        {typeof children === 'string' ? <AppText variant="small" color="#334155">{children}</AppText> : children}
        {action ? <View style={styles.action}>{action}</View> : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  box: { flexDirection: 'row', gap: spacing.sm, padding: spacing.md, borderRadius: radii.md, borderWidth: 1 },
  icon: { marginTop: 1 },
  body: { flex: 1, gap: 4 },
  action: { marginTop: spacing.sm, alignSelf: 'flex-start' },
});
