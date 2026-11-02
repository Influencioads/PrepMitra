import { useEffect, useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ArrowLeft } from 'lucide-react';
import { DEMO_OTP, maskPhone, otpSchema } from '@prepmitra/shared';
import { USE_MOCK } from '@/services/mock';
import { Button, Notice } from '@/components/ui';
import { OtpInput } from '@/components/auth/OtpInput';
import { authService, errorMessage, profileService } from '@/services';
import { signInWithDemoData, useAuthStore } from '@/store';
import { RecaptchaSlot } from '@/components/common/RecaptchaSlot';
import { firebaseEnabled } from '@/utils/env';
import { track } from '@/lib/analytics';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT } from '@/i18n';
import { authMessages } from '@/i18n/messages/auth';

const RESEND_AFTER = 30;

export function VerifyOtpPage() {
  const t = useT(authMessages);
  useDocumentTitle(t('verifyDocTitle'));
  const navigate = useNavigate();
  const pending = useAuthStore((s) => s.pending);
  const setPending = useAuthStore((s) => s.setPending);
  const session = useAuthStore((s) => s.session);
  const [otp, setOtp] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [resendIn, setResendIn] = useState(RESEND_AFTER);
  const [resending, setResending] = useState(false);

  useEffect(() => {
    if (resendIn <= 0) return;
    const timer = setTimeout(() => setResendIn((s) => s - 1), 1000);
    return () => clearTimeout(timer);
  }, [resendIn]);

  if (!pending) return <Navigate to={session ? '/dashboard' : '/login'} replace />;

  const verify = async (code = otp) => {
    const parsed = otpSchema.safeParse({ otp: code });
    if (!parsed.success) {
      setError(parsed.error.issues[0]?.message ?? t('enterCode'));
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      const s = await authService.verifyOtp({ requestId: pending.requestId, phone: pending.phone, otp: code, signup: pending.signup });
      // Sign in first: the consent call needs the new session's token.
      signInWithDemoData(s);
      if (s.isNewUser) await profileService.recordConsent('terms-and-privacy', true).catch(() => undefined);
      track(s.isNewUser ? 'signup_completed' : 'login', { method: 'phone' });
      if (pending.purpose === 'recovery') toast.success(t('recoveredToast'));
      else toast.success(s.isNewUser ? t('accountCreated') : t('welcomeBack', { name: s.user.name.split(' ')[0] }));
      const dest = s.user.role === 'admin' ? '/admin/dashboard' : !s.user.onboardingComplete ? '/onboarding' : pending.redirectTo ?? '/dashboard';
      navigate(dest, { replace: true });
    } catch (e) {
      setError(errorMessage(e));
      setOtp('');
    } finally {
      setSubmitting(false);
    }
  };

  const resend = async () => {
    setResending(true);
    try {
      const res = await authService.sendOtp({ phone: pending.phone, purpose: pending.purpose });
      setPending({ ...pending, requestId: res.requestId, demoCode: res.demoCode });
      setResendIn(RESEND_AFTER);
      toast.success(firebaseEnabled() ? t('newCodeSms') : t('newCodeDemo'));
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setResending(false);
    }
  };

  return (
    <div>
      <Link to={pending.purpose === 'signup' ? '/signup' : '/login'} onClick={() => setPending(null)} className="inline-flex items-center gap-1.5 text-sm font-medium text-muted hover:text-primary">
        <ArrowLeft className="h-4 w-4" aria-hidden /> {t('changeNumber')}
      </Link>
      <h1 className="mt-4 text-2xl font-bold sm:text-3xl">{t('verifyTitle')}</h1>
      <p className="mt-2 text-muted">{t('verifyBody', { phone: maskPhone(pending.phone) })}</p>

      {/* Real API: a development backend returns the code (dev_otp); a production one sends an SMS. */}
      {firebaseEnabled() || (!USE_MOCK && !pending.demoCode) ? (
        <p className="mt-6 text-sm text-muted">{t('smsSent')}</p>
      ) : (
        <Notice tone="warning" className="mt-6">{t('demoOtp', { code: pending.demoCode ?? DEMO_OTP })}</Notice>
      )}

      <form
        className="mt-6 space-y-4"
        onSubmit={(e) => {
          e.preventDefault();
          void verify();
        }}
      >
        <OtpInput
          value={otp}
          onChange={(v) => {
            setOtp(v);
            setError(null);
            if (v.length === 6) void verify(v);
          }}
          invalid={!!error}
          disabled={submitting}
          autoFocus
        />
        {error && <p role="alert" className="text-sm font-medium text-danger">{error}</p>}
        <Button type="submit" size="lg" className="w-full" loading={submitting}>{t('verifyContinue')}</Button>
      </form>
      <RecaptchaSlot />

      <p className="mt-6 text-center text-sm text-muted">
        {t('noCode')}{' '}
        {resendIn > 0 ? (
          <span>{t('resendIn', { seconds: resendIn })}</span>
        ) : (
          <button type="button" onClick={resend} disabled={resending} className="font-semibold text-primary hover:underline disabled:opacity-60">
            {t('resendCode')}
          </button>
        )}
      </p>
    </div>
  );
}
