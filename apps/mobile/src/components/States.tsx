import { useEffect, useState, type ReactNode } from 'react';
import { Animated, StyleSheet, View, type DimensionValue, type StyleProp, type ViewStyle } from 'react-native';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import { colors, radii, spacing } from '@/theme';
import type { IoniconName } from '@/utils/icons';
import { AppText } from './AppText';
import { Button } from './Button';
import { IconTile } from './IconTile';

export interface EmptyStateProps {
  icon?: IoniconName;
  title: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
  children?: ReactNode;
  compact?: boolean;
}

export function EmptyState({ icon = 'file-tray-outline', title, description, actionLabel, onAction, children, compact }: EmptyStateProps) {
  return (
    <View style={[styles.empty, compact && styles.compact]} accessible accessibilityLabel={`${title}. ${description ?? ''}`}>
      <IconTile name={icon} tone="primary" size={compact ? 40 : 52} />
      <AppText variant="h3" align="center">{title}</AppText>
      {description ? <AppText variant="small" align="center">{description}</AppText> : null}
      {actionLabel && onAction ? <Button title={actionLabel} onPress={onAction} style={styles.action} /> : null}
      {children}
    </View>
  );
}

export function ErrorState({ title = 'Something went wrong', description, onRetry }: { title?: string; description?: string; onRetry?: () => void }) {
  return (
    <View style={styles.empty} accessibilityRole="alert">
      <IconTile name="cloud-offline-outline" tone="error" size={52} />
      <AppText variant="h3" align="center">{title}</AppText>
      {description ? <AppText variant="small" align="center">{description}</AppText> : null}
      {onRetry ? <Button title="Try again" leftIcon="refresh" variant="outline" onPress={onRetry} style={styles.action} /> : null}
    </View>
  );
}

/** Pulsing placeholder block. */
export function Skeleton({ width = '100%', height = 16, radius = radii.sm, style }: { width?: DimensionValue; height?: number; radius?: number; style?: StyleProp<ViewStyle> }) {
  const [pulse] = useState(() => new Animated.Value(0.5));
  const reduceMotion = useReducedMotion();
  useEffect(() => {
    if (reduceMotion) {
      pulse.setValue(0.7);
      return;
    }
    const loop = Animated.loop(
      Animated.sequence([
        Animated.timing(pulse, { toValue: 1, duration: 650, useNativeDriver: true }),
        Animated.timing(pulse, { toValue: 0.5, duration: 650, useNativeDriver: true }),
      ]),
    );
    loop.start();
    return () => loop.stop();
  }, [pulse, reduceMotion]);
  return <Animated.View style={[{ width, height, borderRadius: radius, backgroundColor: '#E2E8F0', opacity: pulse }, style]} />;
}

/** Page-level loading placeholder: header + cards. */
export function LoadingSkeleton({ variant = 'page', rows = 3 }: { variant?: 'page' | 'list' | 'card'; rows?: number }) {
  return (
    <View style={styles.skeleton} accessibilityRole="progressbar" accessibilityLabel="Loading">
      {variant === 'page' && (
        <>
          <Skeleton width="60%" height={26} />
          <Skeleton width="85%" height={14} />
          <Skeleton height={140} radius={radii.lg} style={styles.gapTop} />
        </>
      )}
      {Array.from({ length: rows }, (_, i) => (
        <View key={i} style={styles.skelCard}>
          <Skeleton width={40} height={40} radius={radii.md} />
          <View style={styles.skelLines}>
            <Skeleton width="70%" />
            <Skeleton width="45%" height={12} />
          </View>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  empty: { alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingVertical: spacing['2xl'], paddingHorizontal: spacing.lg },
  compact: { paddingVertical: spacing.lg },
  action: { marginTop: spacing.sm, minWidth: 180 },
  skeleton: { padding: spacing.lg, gap: spacing.md },
  gapTop: { marginTop: spacing.sm },
  skelCard: {
    flexDirection: 'row',
    gap: spacing.md,
    alignItems: 'center',
    padding: spacing.lg,
    borderRadius: radii.lg,
    backgroundColor: colors.card,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: colors.border,
  },
  skelLines: { flex: 1, gap: 8 },
});
