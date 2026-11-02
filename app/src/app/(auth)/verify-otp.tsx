import { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import { DISCLAIMERS, maskPhone, otpSchema } from '@prepmitra/shared';
import { AppText, Button, EmptyState, Notice, OtpInput, Screen, toast } from '@/components';
import { useNow } from '@/hooks/useNow';
import { authService, errorMessage, profileService } from '@/services';
import { signInWithDemoData, useAuthStore } from '@/store';
import { colors, spacing } from '@/theme';

const RESEND_AFTER_SEC = 30;

export default function VerifyOtp() {
  const pending = useAuthStore((s) => s.pending);
  const setPending = useAuthStore((s) => s.setPending);
  const [code, setCode] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [verifying, setVerifying] = useState(false);
  const [resending, setResending] = useState(false);
  const now = useNow(1000, !!pending);

  if (!pending) {
    return (
      <Screen>
        <EmptyState
          icon="keypad-outline"
          title="No code requested"
          description="Enter your mobile number first to get a verification code."
          actionLabel="Go to log in"
          onAction={() => router.replace('/login')}
        />
      </Screen>
    );
  }

  const wait = Math.max(0, RESEND_AFTER_SEC - Math.floor((now - pending.sentAt) / 1000));

  const verify = async (value = code) => {
    const parsed = otpSchema.safeParse({ otp: value });
    if (!parsed.success) {
      setError(parsed.error.issues[0]?.message ?? 'Enter the 6-digit code');
      return;
    }
    setError(null);
    setVerifying(true);
    try {
      const session = await authService.verifyOtp({ requestId: pending.requestId, phone: pending.phone, otp: value, signup: pending.signup });
      if (session.isNewUser) {
        await profileService.recordConsent('terms-privacy', true).catch(() => undefined);
        toast.success('Account created. Let’s set up your profile.');
      } else {
        toast.success(`Welcome back, ${session.user.name.split(' ')[0]}!`);
      }
      // Flipping the auth guard redirects away from the (auth) group automatically.
      signInWithDemoData(session);
    } catch (e) {
      setError(errorMessage(e));
      setVerifying(false);
    }
  };

  const resend = async () => {
    setResending(true);
    try {
      const res = await authService.sendOtp({ phone: pending.phone, purpose: pending.purpose });
      setPending({ ...pending, requestId: res.requestId, demoCode: res.demoCode, sentAt: Date.now() });
      setCode('');
      setError(null);
      toast.info('A new demo code is ready. No SMS is sent in demo mode.');
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setResending(false);
    }
  };

  return (
    <Screen keyboard edges={['left', 'right', 'bottom']}>
      <View style={styles.head}>
        <AppText variant="h1" accessibilityRole="header">Enter verification code</AppText>
        <AppText variant="body" color={colors.textSecondary}>
          Enter the 6-digit code for {maskPhone(pending.phone)}.
        </AppText>
        <Button title="Change number" variant="ghost" size="sm" style={styles.self} onPress={() => router.back()} />
      </View>
      <Notice tone="warning" title="Demo mode">{DISCLAIMERS.demoOtp}</Notice>
      <OtpInput
        value={code}
        onChange={(v) => {
          setCode(v);
          if (error) setError(null);
        }}
        error={error ?? undefined}
        onComplete={(v) => void verify(v)}
      />
      <Button title="Verify and continue" size="lg" fullWidth loading={verifying} onPress={() => void verify()} />
      <View style={styles.resend}>
        {wait > 0 ? (
          <AppText variant="small" accessibilityLiveRegion="polite">You can request a new code in {wait}s</AppText>
        ) : (
          <Button title="Get a new code" variant="ghost" size="sm" loading={resending} onPress={resend} />
        )}
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  head: { gap: spacing.sm },
  self: { alignSelf: 'flex-start', marginLeft: -spacing.md },
  resend: { alignItems: 'center', minHeight: 44, justifyContent: 'center' },
});
