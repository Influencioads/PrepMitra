import { useEffect, useRef, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useNavigate, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ArrowLeft, CircleCheck, Clock, FileText, MessageSquare, Mic, Upload, X } from 'lucide-react';
import type { ExperienceLevel, InterviewMode, LanguageCode, ResumeInfo } from '@prepmitra/shared';
import {
  EXPERIENCE_LEVELS, LANGUAGES, RESUME_RULES, interviewSetupSchema, validateResumeFile, type InterviewSetupInput,
} from '@prepmitra/shared';
import {
  Badge, Button, ButtonLink, Card, CardBody, CardHeader, ErrorState, IconTile, LanguageSelector, LoadingSkeleton, Modal, Notice, Textarea,
} from '@/components/ui';
import { RadioCards } from '@/components/interview/RadioCards';
import { errorMessage, interviewService, profileService } from '@/services';
import { roleCreditCost, useAuthStore, useInterviewStore, useProfileStore, useSubscriptionStore } from '@/store';
import { useAsync } from '@/hooks/useAsync';
import { track } from '@/lib/analytics';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useT } from '@/i18n';
import { LEVEL_KEYS, interviewMessages } from '@/i18n/messages/interview';
import { commonMessages } from '@/i18n/messages/common';

const JD_MAX = 4000;


export function InterviewSetupPage() {
  const { roleId = '' } = useParams();
  const navigate = useNavigate();
  const t = useT(interviewMessages);
  const tc = useT(commonMessages);
  const creditsText = (n: number) => (n === 1 ? tc('credit') : tc('credits', { count: n }));
  const { data: role, loading, error, reload } = useAsync(() => interviewService.getRole(roleId), [roleId]);
  useDocumentTitle(role ? t('setupDocTitle', { role: role.shortTitle }) : t('setupFallbackTitle'));
  const user = useAuthStore((s) => s.session?.user);
  const profileResume = useProfileStore((s) => s.profile.resume);
  const sub = useSubscriptionStore((s) => s.sub);
  const consume = useSubscriptionStore((s) => s.consume);
  const saveSession = useInterviewStore((s) => s.saveSession);
  const [resume, setResume] = useState<ResumeInfo | null>(profileResume ?? null);
  const [resumeError, setResumeError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [starting, setStarting] = useState(false);
  const [creditModal, setCreditModal] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const { handleSubmit, watch, setValue, register, reset, formState: { errors } } = useForm<InterviewSetupInput>({
    resolver: zodResolver(interviewSetupSchema),
    defaultValues: { roleId, level: 'fresher', language: user?.preferredLanguage ?? 'en', mode: 'text', jobDescription: '' },
  });

  useEffect(() => {
    if (role) reset({ roleId: role.id, level: role.levels[0] ?? 'fresher', language: role.languages.includes(user?.preferredLanguage ?? 'en') ? user?.preferredLanguage ?? 'en' : 'en', mode: 'text', jobDescription: '' });
  }, [role, reset, user?.preferredLanguage]);

  const mode = watch('mode');
  const language = watch('language') as LanguageCode;
  const jd = watch('jobDescription') ?? '';

  useEffect(() => {
    if (mode === 'voice' && !LANGUAGES.find((l) => l.code === language)?.voiceSupported) {
      setValue('language', 'en');
      toast(t('voiceSwitched'), { icon: 'ℹ️' });
    }
  }, [mode, language, setValue, t]);

  if (loading) return <LoadingSkeleton variant="page" />;
  if (error || !role) return <ErrorState title={t('roleNotFound')} description={error ?? t('roleNotAvailable')} onRetry={reload} />;

  const cost = roleCreditCost(role);
  const allowed = role.languages.filter((c) => mode === 'text' || LANGUAGES.find((l) => l.code === c)?.voiceSupported);

  const handleFile = async (file?: File) => {
    if (!file) return;
    setResumeError(null);
    const check = validateResumeFile(file);
    if (!check.ok) {
      setResumeError(check.error);
      return;
    }
    setUploading(true);
    try {
      setResume(await profileService.uploadResume(file));
      toast.success(t('resumeAttached'));
    } catch (e) {
      setResumeError(errorMessage(e));
    } finally {
      setUploading(false);
    }
  };

  const onSubmit = async (values: InterviewSetupInput) => {
    if (sub.credits < cost) {
      setCreditModal(true);
      return;
    }
    setStarting(true);
    try {
      const session = await interviewService.start({
        roleId: role.id,
        level: values.level as ExperienceLevel,
        language: values.language as LanguageCode,
        mode: values.mode as InterviewMode,
        resumeFileName: resume?.fileName,
        jobDescription: values.jobDescription?.trim() || undefined,
      });
      if (!consume(cost, 'interview', t('sessionLabel', { role: role.shortTitle }))) {
        setCreditModal(true);
        return;
      }
      saveSession(session);
      track('interview_started', { roleId: role.id, mode: values.mode, level: values.level, hasResume: !!resume });
      toast.success(t('creditsUsedGoodLuck', { credits: creditsText(cost) }));
      navigate(`/interview/session/${session.id}`);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setStarting(false);
    }
  };

  return (
    <div>
      <Link to="/interviews" className="inline-flex items-center gap-1.5 text-sm font-medium text-muted hover:text-primary">
        <ArrowLeft className="h-4 w-4" aria-hidden /> {t('allRolesBack')}
      </Link>
      <div className="mt-4 grid gap-6 lg:grid-cols-[1fr_340px]">
        <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
          <Card className="p-6">
            <div className="flex items-start gap-4">
              <IconTile name={role.icon} tone="secondary" className="h-14 w-14" />
              <div className="min-w-0">
                <p className="text-sm text-muted">{role.category}</p>
                <h1 className="mt-0.5 text-2xl font-bold sm:text-3xl">{role.title}</h1>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  <Badge icon={<Clock className="h-3 w-3" />}>{t('minutes', { n: role.durationMin })}</Badge>
                  <Badge>{t('questionsPlus', { n: role.questionCount })}</Badge>
                  <Badge tone="primary">{creditsText(cost)}</Badge>
                </div>
              </div>
            </div>
            <p className="mt-4 text-muted">{role.description}</p>
          </Card>

          <Card>
            <CardHeader title={t('configureTitle')} description={t('configureDesc')} />
            <CardBody className="space-y-6">
              <input type="hidden" {...register('roleId')} />
              <RadioCards
                label={t('experienceLevel')}
                value={watch('level') as ExperienceLevel}
                onChange={(v) => setValue('level', v, { shouldValidate: true })}
                options={EXPERIENCE_LEVELS.map((l) => ({
                  value: l.value,
                  title: t(LEVEL_KEYS[l.value].title),
                  description: t(LEVEL_KEYS[l.value].desc),
                  disabled: !role.levels.includes(l.value),
                }))}
                error={errors.level?.message}
              />
              <RadioCards
                label={t('interviewMode')}
                columns={2}
                value={mode as InterviewMode}
                onChange={(v) => setValue('mode', v, { shouldValidate: true })}
                options={[
                  { value: 'text', title: t('modeText'), description: t('modeTextDesc'), icon: <MessageSquare className="h-5 w-5" /> },
                  { value: 'voice', title: t('modeVoice'), description: role.voiceAvailable ? t('modeVoiceDesc') : t('modeVoiceUnavailable'), icon: <Mic className="h-5 w-5" />, disabled: !role.voiceAvailable },
                ]}
              />
              <LanguageSelector
                label={t('interviewLanguage')}
                value={language}
                onChange={(v) => setValue('language', v, { shouldValidate: true })}
                allowed={allowed}
                voiceOnly={mode === 'voice'}
                hint={mode === 'voice' ? t('voiceLangHint') : t('textLangHint')}
                error={errors.language?.message}
              />

              <div>
                <p className="text-sm font-medium">{t('resume')} <span className="font-normal text-muted">{t('optional')}</span></p>
                {resume ? (
                  <div className="mt-2 flex flex-wrap items-center gap-3 rounded-lg border border-line bg-background p-3">
                    <FileText className="h-6 w-6 text-primary" aria-hidden />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium">{resume.fileName}</p>
                      <p className="text-xs text-muted">{resume.sizeKb} KB{resume === profileResume ? t('fromProfile') : ''}</p>
                    </div>
                    <div className="flex w-full gap-2 sm:w-auto">
                      <Button variant="outline" size="sm" onClick={() => fileRef.current?.click()} loading={uploading}>{t('replace')}</Button>
                      <Button variant="ghost" size="sm" onClick={() => setResume(null)} leftIcon={<X className="h-4 w-4" />}>{t('remove')}</Button>
                    </div>
                  </div>
                ) : (
                  <div className="mt-2 flex flex-wrap items-center gap-3 rounded-lg border border-dashed border-line-strong p-3">
                    <Upload className="h-5 w-5 text-muted" aria-hidden />
                    <p className="flex-1 text-sm text-muted">{t('attachHint', { mb: RESUME_RULES.maxSizeMb })}</p>
                    <Button variant="outline" size="sm" onClick={() => fileRef.current?.click()} loading={uploading}>{t('uploadResume')}</Button>
                  </div>
                )}
                <input
                  ref={fileRef}
                  type="file"
                  className="sr-only"
                  aria-label={t('uploadResumeAria')}
                  accept={RESUME_RULES.acceptedExtensions.join(',')}
                  onChange={(e) => {
                    void handleFile(e.target.files?.[0]);
                    e.target.value = '';
                  }}
                />
                {resumeError && <p role="alert" className="mt-1.5 text-xs font-medium text-danger">{resumeError}</p>}
              </div>

              <Textarea
                label={t('jdLabel')}
                rows={5}
                placeholder={t('jdPlaceholder')}
                maxLength={JD_MAX}
                hint={t('jdHint', { count: jd.length.toLocaleString('en-IN'), max: JD_MAX.toLocaleString('en-IN') })}
                error={errors.jobDescription?.message}
                {...register('jobDescription')}
              />
            </CardBody>
          </Card>

          <div className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
            <ButtonLink to="/interviews" variant="outline">{t('cancel')}</ButtonLink>
            <Button type="submit" size="lg" loading={starting}>
              {t('startInterview', { credits: creditsText(cost) })}
            </Button>
          </div>
        </form>

        <aside className="space-y-4 lg:sticky lg:top-24 lg:self-start">
          <Card className="p-5">
            <p className="text-sm font-semibold">{t('whatsEvaluated')}</p>
            <ul className="mt-3 space-y-2 text-sm">
              {role.evaluates.map((e) => (
                <li key={e} className="flex gap-2"><CircleCheck className="mt-0.5 h-4 w-4 shrink-0 text-success" aria-hidden />{e}</li>
              ))}
            </ul>
            <p className="mt-4 text-sm font-semibold">{t('questionThemes')}</p>
            <div className="mt-2 flex flex-wrap gap-1.5">{role.themes.map((theme) => <Badge key={theme}>{theme}</Badge>)}</div>
            <p className="mt-4 text-sm font-semibold">{t('rounds')}</p>
            <p className="mt-1 text-sm text-muted">{t('roundsList')}</p>
          </Card>
          <Card className="p-5">
            <p className="text-sm text-muted">{t('yourCredits')}</p>
            <p className="mt-1 text-2xl font-bold">{sub.credits}</p>
            {sub.credits < cost ? (
              <p className="mt-1 text-sm text-danger">{t('needToStart', { credits: creditsText(cost) })} <Link to="/subscription" className="font-semibold underline">{t('getCredits')}</Link></p>
            ) : (
              <p className="mt-1 text-sm text-muted">{t('willBeUsed', { credits: creditsText(cost) })}</p>
            )}
          </Card>
          <Notice tone="warning">{t('demoInterview')}</Notice>
        </aside>
      </div>

      <Modal
        open={creditModal}
        onOpenChange={setCreditModal}
        title={t('notEnoughTitle')}
        description={t('notEnoughDesc', { credits: creditsText(cost), have: sub.credits })}
        size="sm"
        footer={
          <>
            <Button variant="outline" onClick={() => setCreditModal(false)}>{t('notNow')}</Button>
            <ButtonLink to="/subscription">{t('getCredits')}</ButtonLink>
          </>
        }
      >
        <p className="text-sm text-muted">{t('notEnoughBody')}</p>
      </Modal>
    </div>
  );
}
