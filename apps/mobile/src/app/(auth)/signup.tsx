import { StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { signupSchema, type SignupInput } from '@prepmitra/shared';
import { AppText, Button, Card, Input, Screen, SwitchRow, toast } from '@/components';
import { authService, errorMessage } from '@/services';
import { useAuthStore } from '@/store';
import { colors, spacing } from '@/theme';

export default function Signup() {
  const setPending = useAuthStore((s) => s.setPending);
  const { control, handleSubmit, formState: { errors, isSubmitting } } = useForm<SignupInput>({
    resolver: zodResolver(signupSchema),
    defaultValues: { name: '', phone: '', email: '', ageConfirmed: false, consent: false },
  });

  const onSubmit = async (values: SignupInput) => {
    try {
      const res = await authService.sendOtp({ phone: values.phone, purpose: 'signup' });
      setPending({
        phone: values.phone,
        requestId: res.requestId,
        purpose: 'signup',
        signup: { name: values.name.trim(), email: values.email || undefined },
        demoCode: res.demoCode,
        sentAt: Date.now(),
      });
      router.push('/verify-otp');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <Screen
      keyboard
      edges={['left', 'right', 'bottom']}
      footer={<Button title="Continue" size="lg" fullWidth loading={isSubmitting} onPress={handleSubmit(onSubmit)} />}
    >
      <View style={styles.head}>
        <AppText variant="h1" accessibilityRole="header">Create your account</AppText>
        <AppText variant="body" color={colors.textSecondary}>Start with a free 30-minute mini mock and a full report.</AppText>
      </View>
      <Controller
        control={control}
        name="name"
        render={({ field: { value, onChange, onBlur } }) => (
          <Input label="Full name" required value={value} onChangeText={onChange} onBlur={onBlur} autoComplete="name" textContentType="name" autoCapitalize="words" error={errors.name?.message} />
        )}
      />
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
            autoComplete="tel"
            maxLength={10}
            error={errors.phone?.message}
          />
        )}
      />
      <Controller
        control={control}
        name="email"
        render={({ field: { value, onChange, onBlur } }) => (
          <Input
            label="Email (optional)"
            value={value ?? ''}
            onChangeText={onChange}
            onBlur={onBlur}
            keyboardType="email-address"
            autoCapitalize="none"
            autoComplete="email"
            hint="For receipts and report emails."
            error={errors.email?.message}
          />
        )}
      />
      <Card style={styles.consents}>
        <Controller
          control={control}
          name="ageConfirmed"
          render={({ field: { value, onChange } }) => (
            <SwitchRow label="I am 18 years or older" value={value} onValueChange={onChange} error={errors.ageConfirmed?.message} />
          )}
        />
        <Controller
          control={control}
          name="consent"
          render={({ field: { value, onChange } }) => (
            <SwitchRow
              label="I agree to the Terms and Privacy Policy"
              description="We process your data under India’s DPDP Act. Recruiter sharing stays off unless you turn it on."
              value={value}
              onValueChange={onChange}
              error={errors.consent?.message}
            />
          )}
        />
      </Card>
      <View style={styles.footer}>
        <AppText variant="small">Already registered?</AppText>
        <Button title="Log in" variant="ghost" size="sm" onPress={() => router.replace('/login')} />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  head: { gap: spacing.sm },
  consents: { gap: spacing.md },
  footer: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center' },
});
