import { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { DEMO_USER, loginSchema, type LoginInput } from '@prepmitra/shared';
import { AppText, AuthShell, Button, Input, toast } from '@/components';
import { authService, errorMessage } from '@/services';
import { signInWithDemoData, useAuthStore } from '@/store';
import { colors, radii, spacing } from '@/theme';

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
    <AuthShell
      art
      title="Welcome back"
      subtitle="Log in with your mobile number. We’ll send a 6-digit code."
      footer={
        <>
          <Button title="Get OTP" size="lg" rightIcon="arrow-forward" fullWidth loading={isSubmitting} onPress={handleSubmit(onSubmit)} />
          <View style={styles.switch}>
            <AppText variant="small">New to PrepMitra AI?</AppText>
            <Button title="Create an account" variant="ghost" size="sm" onPress={() => router.replace('/signup')} />
          </View>
        </>
      }
    >
      <Controller
        control={control}
        name="phone"
        render={({ field: { value, onChange, onBlur } }) => (
          <Input
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

      <View style={styles.divider}>
        <View style={styles.line} />
        <AppText variant="caption">or</AppText>
        <View style={styles.line} />
      </View>
      <Button title="Continue with Google (demo)" variant="outline" leftIcon="logo-google" fullWidth loading={googleLoading} onPress={google} />

      <View style={styles.demo}>
        <View style={styles.flex}>
          <AppText variant="smallStrong">Demo account</AppText>
          <AppText variant="caption">{`${DEMO_USER.phone} has past mocks. The code is always 123456.`}</AppText>
        </View>
        <Button title="Fill" variant="soft" size="sm" onPress={() => setValue('phone', DEMO_USER.phone, { shouldValidate: true })} />
      </View>
    </AuthShell>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1, gap: 2 },
  divider: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  line: { flex: 1, height: StyleSheet.hairlineWidth, backgroundColor: colors.border },
  switch: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', flexWrap: 'wrap' },
  demo: {
    flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.md, borderRadius: radii.lg,
    borderWidth: 1, borderStyle: 'dashed', borderColor: colors.borderStrong,
  },
});
