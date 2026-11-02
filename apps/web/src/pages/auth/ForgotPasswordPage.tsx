import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { z } from 'zod';
import { ArrowLeft, Mail, Smartphone } from 'lucide-react';
import { phoneSchema } from '@prepmitra/shared';
import { Button, Input, Notice, Tabs } from '@/components/ui';
import { authService, errorMessage } from '@/services';
import { useAuthStore } from '@/store';
import { RecaptchaSlot } from '@/components/common/RecaptchaSlot';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT } from '@/i18n';
import { authMessages } from '@/i18n/messages/auth';

const phoneForm = z.object({ phone: phoneSchema });
const emailForm = z.object({ email: z.email('Enter a valid email address') });

/**
 * PrepMitra uses passwordless OTP login, so "password recovery" means regaining
 * access: re-verify the mobile number, or request help via the registered email.
 */
export function ForgotPasswordPage() {
  const t = useT(authMessages);
  useDocumentTitle(t('recoveryDocTitle'));
  const navigate = useNavigate();
  const setPending = useAuthStore((s) => s.setPending);
  const [mode, setMode] = useState<'phone' | 'email'>('phone');
  const [emailDone, setEmailDone] = useState<string | null>(null);
  const pf = useForm<z.infer<typeof phoneForm>>({ resolver: zodResolver(phoneForm), defaultValues: { phone: '' } });
  const ef = useForm<z.infer<typeof emailForm>>({ resolver: zodResolver(emailForm), defaultValues: { email: '' } });

  const onPhone = pf.handleSubmit(async ({ phone }) => {
    try {
      const res = await authService.sendOtp({ phone, purpose: 'recovery' });
      setPending({ phone, requestId: res.requestId, purpose: 'recovery', demoCode: res.demoCode });
      navigate('/verify-otp');
    } catch (e) {
      toast.error(errorMessage(e));
    }
  });

  const onEmail = ef.handleSubmit(async ({ email }) => {
    await new Promise((r) => setTimeout(r, 700));
    setEmailDone(email);
  });

  return (
    <div>
      <Link to="/login" className="inline-flex items-center gap-1.5 text-sm font-medium text-muted hover:text-primary">
        <ArrowLeft className="h-4 w-4" aria-hidden /> {t('backToLogin')}
      </Link>
      <h1 className="mt-4 text-2xl font-bold sm:text-3xl">{t('recoveryTitle')}</h1>
      <p className="mt-2 text-muted">{t('recoveryBody')}</p>

      <RecaptchaSlot />
      <Tabs
        className="mt-6"
        ariaLabel={t('recoveryMethod')}
        value={mode}
        onChange={setMode}
        items={[
          { value: 'phone', label: <span className="inline-flex items-center gap-1.5"><Smartphone className="h-4 w-4" />{t('tabMobile')}</span> },
          { value: 'email', label: <span className="inline-flex items-center gap-1.5"><Mail className="h-4 w-4" />{t('tabEmail')}</span> },
        ]}
      />

      {mode === 'phone' ? (
        <form onSubmit={onPhone} className="mt-6 space-y-4" noValidate>
          <Input label={t('registeredMobile')} leftAddon="+91" type="tel" inputMode="numeric" maxLength={10} required error={pf.formState.errors.phone?.message} {...pf.register('phone')} />
          <Button type="submit" size="lg" className="w-full" loading={pf.formState.isSubmitting}>{t('getNewCode')}</Button>
        </form>
      ) : emailDone ? (
        <Notice tone="success" className="mt-6" title={t('requestRecorded')}>
          {t('requestRecordedBody', { email: emailDone })}
        </Notice>
      ) : (
        <form onSubmit={onEmail} className="mt-6 space-y-4" noValidate>
          <Input label={t('registeredEmail')} type="email" required error={ef.formState.errors.email?.message} {...ef.register('email')} hint={t('registeredEmailHint')} />
          <Button type="submit" size="lg" className="w-full" loading={ef.formState.isSubmitting}>{t('requestRecovery')}</Button>
        </form>
      )}
    </div>
  );
}
