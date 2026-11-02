import { createContext, use, type ReactNode } from 'react';
import { StyleSheet, View } from 'react-native';
import { AppText, Button, Screen } from '@/components';
import { colors, spacing } from '@/theme';
import { Stepper } from './Stepper';

export interface WizardContextValue {
  steps: string[];
  step: number;
  back: () => void;
  saveLater: () => void;
  logout: () => void;
}

export const WizardContext = createContext<WizardContextValue | null>(null);

export interface StepScreenProps {
  title: string;
  description: string;
  children: ReactNode;
  onContinue: () => void;
  continueLabel?: string;
  loading?: boolean;
  /** Hide "Save and finish later" (e.g. on the final review step). */
  hideSave?: boolean;
}

/** Shared chrome for every onboarding step: progress, title, sticky Back/Continue footer. */
export function StepScreen({ title, description, children, onContinue, continueLabel = 'Continue', loading, hideSave }: StepScreenProps) {
  const ctx = use(WizardContext);
  if (!ctx) throw new Error('StepScreen must be used inside the onboarding wizard');
  const { steps, step, back, saveLater, logout } = ctx;
  return (
    <Screen
      keyboard
      edges={['top', 'left', 'right', 'bottom']}
      footer={
        <>
          <View style={styles.navRow}>
            {step > 0 && <Button title="Back" variant="outline" leftIcon="chevron-back" onPress={back} disabled={loading} style={styles.back} />}
            <Button title={continueLabel} onPress={onContinue} loading={loading} style={styles.flex} rightIcon={continueLabel === 'Continue' ? 'chevron-forward' : undefined} />
          </View>
          {!hideSave && <Button title="Save and finish later" variant="ghost" size="sm" onPress={saveLater} disabled={loading} />}
        </>
      }
    >
      <View style={styles.top}>
        <AppText variant="caption">Takes about 2 minutes</AppText>
        <Button title="Log out" variant="ghost" size="sm" onPress={logout} accessibilityHint="Signs you out. Your progress stays saved on this device." />
      </View>
      <Stepper steps={steps} current={step} />
      <View style={styles.head}>
        <AppText variant="h1" accessibilityRole="header">{title}</AppText>
        <AppText variant="body" color={colors.textSecondary}>{description}</AppText>
      </View>
      {children}
    </Screen>
  );
}

const styles = StyleSheet.create({
  top: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: -spacing.sm },
  head: { gap: spacing.xs },
  navRow: { flexDirection: 'row', gap: spacing.sm },
  back: { minWidth: 110 },
  flex: { flex: 1 },
});
