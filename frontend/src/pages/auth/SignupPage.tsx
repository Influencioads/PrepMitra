import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { signupSchema, type SignupInput } from '@prepmitra/shared';
import { Button, Checkbox, Input } from '@/components/ui';
import { authService, errorMessage } from '@/services';
import { useAuthStore } from '@/store';
import { RecaptchaSlot } from '@/components/common/RecaptchaSlot';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT } from '@/i18n';
import { authMessages } from '@/i18n/messages/auth';

export function SignupPage() {
  const t = useT(authMessages);
  useDocumentTitle(t('signupDocTitle'));
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const plan = params.get('plan');
  const setPending = useAuthStore((s) => s.setPending);
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<SignupInput>({
    resolver: zodResolver(signupSchema),
    defaultValues: { name: '', phone: '', email: '', ageConfirmed: false, consent: false },
  });

  const onSubmit = async (data: SignupInput) => {
    try {
      const res = await authService.sendOtp({ phone: data.phone, purpose: 'signup' });
      setPending({
        phone: data.phone,
        requestId: res.requestId,
        purpose: 'signup',
        signup: { name: data.name, email: data.email || undefined },
        demoCode: res.demoCode,
        redirectTo: plan ? `/subscription?plan=${plan}` : undefined,
      });
      navigate('/verify-otp');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold sm:text-3xl">{t('signupTitle')}</h1>
      <p className="mt-2 text-muted">{t('signupBody')}</p>
      <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-4" noValidate>
        <Input label={t('fullName')} autoComplete="name" placeholder={t('namePlaceholder')} required error={errors.name?.message} {...register('name')} />
        <Input
          label={t('mobileNumber')}
          leftAddon="+91"
          type="tel"
          inputMode="numeric"
          autoComplete="tel-national"
          maxLength={10}
          placeholder="98765 43210"
          required
          error={errors.phone?.message}
          {...register('phone')}
        />
        <Input label={t('emailOptional')} type="email" autoComplete="email" placeholder="you@example.com" hint={t('emailHint')} error={errors.email?.message} {...register('email')} />
        <div className="space-y-3 pt-1">
          <Checkbox label={t('ageConfirm')} error={errors.ageConfirmed?.message} {...register('ageConfirmed')} />
          <Checkbox
            label={t('consentLabel')}
            description={t('consentDesc')}
            error={errors.consent?.message}
            {...register('consent')}
          />
        </div>
        <Button type="submit" size="lg" className="w-full" loading={isSubmitting}>{t('continue')}</Button>
      </form>
      <RecaptchaSlot />
      <p className="mt-6 text-center text-sm text-muted">
        {t('haveAccount')} <Link to="/login" className="font-semibold text-primary hover:underline">{t('logIn')}</Link>
      </p>
    </div>
  );
}
