import { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { DEMO_USER, loginSchema, type LoginInput } from '@prepmitra/shared';
import { AppText, AuthShell, authColors, Button, Input, toast } from '@/components';
import { authService, errorMessage } from '@/services';
import { signInWithDemoData, useAuthStore } from '@/store';
import { spacing } from '@/theme';

export default function Login() {
  const setPending = useAuthStore((s) => s.setPending);
  const [googleLoading, setGoogleLoading] = useState(false);
  const { control, handleSubmit, setValue, formState: { errors, isSubmitting } } = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
    defaultValues: { phone: '' },
  });

  const onSubmit = async ({ phone }: LoginInput) => {
    try {
      const res = await authService.sendOtp({ phone, purpose: 'login' });
      setPending({ phone, requestId: res.requestId, purpose: 'login', demoCode: res.demoCode, sentAt: Date.now() });
      router.push('/verify-otp');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  const google = async () => {
    setGoogleLoading(true);
    try {
      const session = await authService.googleSignIn();
      toast.success(`Welcome back, ${session.user.name.split(' ')[0]}!`);
      signInWithDemoData(session);
    } catch (e) {
      toast.error(errorMessage(e));
      setGoogleLoading(false);
    }
  };

  return (
    <AuthShell>
      <View style={styles.head}>
        <AppText accessibilityRole="header" style={styles.title}>Welcome back</AppText>
        <AppText variant="body" color={authColors.muted}>Log in with your mobile number. We’ll ask for a 6-digit code next.</AppText>
      </View>
      <Controller
        control={control}
        name="phone"
        render={({ field: { value, onChange, onBlur } }) => (
          <Input
            dark
            label="Mobile number"
            required
            leftAddon="+91"
            value={value}
            onChangeText={(t) => onChange(t.replace(/\D/g, '').slice(0, 10))}
            onBlur={onBlur}
            keyboardType="phone-pad"
            textContentType="telephoneNumber"
            autoComplete="tel"
            maxLength={10}
            placeholder="98765 43210"
            error={errors.phone?.message}
            returnKeyType="done"
            onSubmitEditing={() => void handleSubmit(onSubmit)()}
          />
        )}
      />
      <Button title="Get OTP" variant="accent" size="lg" rightIcon="arrow-forward" fullWidth loading={isSubmitting} onPress={handleSubmit(onSubmit)} />

      <View style={styles.divider}>
        <View style={styles.line} />
        <AppText variant="caption" color={authColors.muted}>or</AppText>
        <View style={styles.line} />
      </View>
      <Button title="Continue with Google (demo)" variant="outlineLight" leftIcon="logo-google" fullWidth loading={googleLoading} onPress={google} />

      <View style={styles.footer}>
        <AppText variant="small" color={authColors.text}>New to PrepMitra AI?</AppText>
        <Button title="Create an account" variant="ghostLight" size="sm" onPress={() => router.replace('/signup')} />
      </View>

      <View style={styles.demo}>
        <AppText variant="smallStrong" color={authColors.text}>Demo account</AppText>
        <AppText variant="caption" color={authColors.muted}>
          {`Use ${DEMO_USER.phone} to see a returning learner with history. Any valid number works; the code is always 123456.`}
        </AppText>
        <Button
          title="Fill demo number"
          variant="outlineLight"
          size="sm"
          onPress={() => setValue('phone', DEMO_USER.phone, { shouldValidate: true })}
          style={styles.self}
        />
      </View>
    </AuthShell>
  );
}

const styles = StyleSheet.create({
  head: { gap: spacing.sm, marginBottom: spacing.xs },
  title: { color: authColors.text, fontSize: 34, lineHeight: 40, fontWeight: '800' },
  divider: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  line: { flex: 1, height: StyleSheet.hairlineWidth, backgroundColor: authColors.line },
  footer: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', flexWrap: 'wrap', marginTop: -spacing.xs },
  demo: { gap: spacing.xs, borderWidth: 1, borderStyle: 'dashed', borderColor: authColors.line, borderRadius: 16, padding: spacing.lg },
  self: { alignSelf: 'flex-start', marginTop: spacing.xs },
});
