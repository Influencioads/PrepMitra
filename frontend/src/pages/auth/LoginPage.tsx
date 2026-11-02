import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ShieldCheck } from 'lucide-react';
import { USE_MOCK } from '@/services/mock';
import { DEMO_OTP, DEMO_USER, loginSchema, type LoginInput } from '@prepmitra/shared';
import { Button, Input, Notice } from '@/components/ui';
import { authService, errorMessage } from '@/services';
import { signInWithDemoData, useAuthStore } from '@/store';
import { RecaptchaSlot } from '@/components/common/RecaptchaSlot';
import { firebaseEnabled } from '@/utils/env';
import { track } from '@/lib/analytics';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT } from '@/i18n';
import { authMessages } from '@/i18n/messages/auth';

export function LoginPage() {
  const t = useT(authMessages);
  useDocumentTitle(t('loginDocTitle'));
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const redirect = params.get('redirect') ?? undefined;
  const setPending = useAuthStore((s) => s.setPending);
  const [busy, setBusy] = useState<'google' | 'admin' | null>(null);
  const { register, handleSubmit, setValue, formState: { errors, isSubmitting } } = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
    defaultValues: { phone: '' },
  });

  const onSubmit = async ({ phone }: LoginInput) => {
    try {
      const res = await authService.sendOtp({ phone, purpose: 'login' });
      setPending({ phone, requestId: res.requestId, purpose: 'login', demoCode: res.demoCode, redirectTo: redirect });
      navigate('/verify-otp');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  };

  const google = async () => {
    setBusy('google');
    try {
      const session = await authService.googleSignIn();
      signInWithDemoData(session);
      track('login', { method: 'google' });
      toast.success(t('welcomeBack', { name: session.user.name.split(' ')[0] }));
      navigate(redirect ?? '/dashboard');
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setBusy(null);
    }
  };

  const admin = async () => {
    setBusy('admin');
    const session = await authService.demoAdminSignIn();
    signInWithDemoData(session);
    toast.success(t('adminSignedIn'));
    navigate('/admin/dashboard');
  };

  return (
    <div>
      <h1 className="text-2xl font-bold sm:text-3xl">{t('loginTitle')}</h1>
      <p className="mt-2 text-muted">{t('loginBody')}</p>

      <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-5" noValidate>
        <Input
          label={t('mobileNumber')}
          leftAddon="+91"
          type="tel"
          inputMode="numeric"
          autoComplete="tel-national"
          placeholder="98765 43210"
          maxLength={10}
          required
          error={errors.phone?.message}
          {...register('phone')}
        />
        <Button type="submit" size="lg" className="w-full" loading={isSubmitting}>{t('sendCode')}</Button>
      </form>
      <RecaptchaSlot />

      <div className="my-6 flex items-center gap-3 text-xs text-muted">
        <span className="h-px flex-1 bg-line" /> {t('or')} <span className="h-px flex-1 bg-line" />
      </div>
      <Button variant="outline" size="lg" className="w-full" onClick={google} loading={busy === 'google'}>
        <svg viewBox="0 0 24 24" className="h-4 w-4" aria-hidden>
          <path fill="#4285F4" d="M22.6 12.2c0-.8-.1-1.5-.2-2.2H12v4.2h5.9a5 5 0 0 1-2.2 3.3v2.7h3.6c2.1-1.9 3.3-4.8 3.3-8Z" />
          <path fill="#34A853" d="M12 23c3 0 5.5-1 7.3-2.7l-3.6-2.7c-1 .7-2.2 1-3.7 1-2.9 0-5.3-1.9-6.2-4.5H2.1v2.8A11 11 0 0 0 12 23Z" />
          <path fill="#FBBC05" d="M5.8 14.1a6.6 6.6 0 0 1 0-4.2V7.1H2.1a11 11 0 0 0 0 9.8l3.7-2.8Z" />
          <path fill="#EA4335" d="M12 5.4c1.6 0 3.1.6 4.2 1.7l3.2-3.2A11 11 0 0 0 2.1 7.1l3.7 2.8C6.7 7.3 9.1 5.4 12 5.4Z" />
        </svg>
        {t('googleDemo')}
      </Button>

      <p className="mt-6 text-center text-sm text-muted">
        {t('newHere')} <Link to="/signup" className="font-semibold text-primary hover:underline">{t('createFree')}</Link>
      </p>
      <p className="mt-2 text-center text-sm">
        <Link to="/forgot-password" className="text-muted hover:text-primary hover:underline">{t('cantAccess')}</Link>
      </p>

      {!firebaseEnabled() && (
      <Notice tone="info" className="mt-8" title={t('demoAccounts')}>
        {USE_MOCK && <p>{t('demoOtp', { code: DEMO_OTP })}</p>}
        <div className="mt-2 flex flex-wrap gap-2">
          <button type="button" className="font-semibold text-primary hover:underline" onClick={() => setValue('phone', DEMO_USER.phone, { shouldValidate: true })}>
            {t('fillLearner')}
          </button>
          <span aria-hidden>·</span>
          <button type="button" className="inline-flex items-center gap-1 font-semibold text-primary hover:underline disabled:opacity-60" onClick={admin} disabled={busy === 'admin'}>
            <ShieldCheck className="h-3.5 w-3.5" aria-hidden /> {t('openAdmin')}
          </button>
        </div>
      </Notice>
      )}
    </div>
  );
}
