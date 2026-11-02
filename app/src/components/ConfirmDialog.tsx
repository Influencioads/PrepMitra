import type { ReactNode } from 'react';
import { KeyboardAvoidingView, Modal, Pressable, StyleSheet, View } from 'react-native';
import { colors, radii, shadows, spacing } from '@/theme';
import { AppText } from './AppText';
import { Button } from './Button';

export interface ConfirmDialogProps {
  visible: boolean;
  title: string;
  message?: string;
  children?: ReactNode;
  confirmLabel?: string;
  cancelLabel?: string;
  destructive?: boolean;
  loading?: boolean;
  confirmDisabled?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

/** Centered confirmation dialog (used where a native Alert can't hold custom content). */
export function ConfirmDialog({
  visible, title, message, children, confirmLabel = 'Confirm', cancelLabel = 'Cancel', destructive, loading, confirmDisabled, onConfirm, onCancel,
}: ConfirmDialogProps) {
  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={onCancel} statusBarTranslucent>
      <KeyboardAvoidingView behavior="padding" style={styles.center}>
        <Pressable style={StyleSheet.absoluteFill} onPress={loading ? undefined : onCancel} accessibilityLabel="Dismiss" accessibilityRole="button" />
        <View style={styles.card} accessibilityViewIsModal accessibilityRole="alert">
          <AppText variant="h3" accessibilityRole="header">{title}</AppText>
          {message ? <AppText variant="small" style={styles.message}>{message}</AppText> : null}
          {children ? <View style={styles.body}>{children}</View> : null}
          <View style={styles.actions}>
            <Button title={cancelLabel} variant="outline" onPress={onCancel} disabled={loading} style={styles.flex} />
            <Button
              title={confirmLabel}
              variant={destructive ? 'danger' : 'primary'}
              onPress={onConfirm}
              loading={loading}
              disabled={confirmDisabled}
              style={styles.flex}
            />
          </View>
        </View>
      </KeyboardAvoidingView>
    </Modal>
  );
}

const styles = StyleSheet.create({
  center: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: spacing.xl, backgroundColor: 'rgba(15, 23, 42, 0.5)' },
  card: { width: '100%', maxWidth: 420, backgroundColor: colors.card, borderRadius: radii.xl, padding: spacing.xl, gap: spacing.sm, ...shadows.overlay },
  message: { color: colors.textSecondary },
  body: { marginTop: spacing.sm, gap: spacing.md },
  actions: { flexDirection: 'row', gap: spacing.sm, marginTop: spacing.lg },
  flex: { flex: 1 },
});
