import { useEffect, useMemo, useRef, useState } from 'react';
import { Navigate, useNavigate, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { CircleCheck, LogOut, Mic, Pause, Play, RotateCcw, Send, Square, Volume2 } from 'lucide-react';
import {
  currentInterviewerTurn, formatClock, interviewProgress, isInterviewFinished, languageName, wordCount,
} from '@prepmitra/shared';
import { Badge, Button, Card, ConfirmationDialog, ErrorState, Logo, Notice, ProgressBar } from '@/components/ui';
import { ChatBubble, STAGE_KEY, TypingIndicator } from '@/components/interview/ChatBubble';
import { useSimulatedPlayback } from '@/components/interview/useSimulatedPlayback';
import { errorMessage, interviewService } from '@/services';
import { useAuthStore, useExamStore, useInterviewStore, useNotificationStore } from '@/store';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { track } from '@/lib/analytics';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { LEVEL_KEYS, interviewMessages } from '@/i18n/messages/interview';

type VoiceState = 'idle' | 'recording' | 'processing' | 'speaking';

export function InterviewSessionPage() {
  const { sessionId = '' } = useParams();
  const navigate = useNavigate();
  const t = useT(interviewMessages);
  const session = useInterviewStore((s) => s.sessions[sessionId]);
  const saveSession = useInterviewStore((s) => s.saveSession);
  const saveReport = useInterviewStore((s) => s.saveReport);
  const pushNotification = useNotificationStore((s) => s.push);
  const logPractice = useExamStore((s) => s.logPractice);
  const userName = useAuthStore((s) => s.session?.user.name ?? 'You');
  const role = session ? interviewService.getRoleSync(session.config.roleId) : undefined;
  useDocumentTitle(role ? t('sessionDocTitle', { role: role.shortTitle }) : t('sessionFallbackTitle'));

  const [answer, setAnswer] = useState('');
  const [pending, setPending] = useState(false);
  const [ending, setEnding] = useState(false);
  const [confirmEnd, setConfirmEnd] = useState(false);
  const [recording, setRecording] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const listRef = useRef<HTMLOListElement>(null);
  const textRef = useRef<HTMLTextAreaElement>(null);

  const isVoice = session?.config.mode === 'voice';
  const current = session ? currentInterviewerTurn(session) : undefined;
  const finished = session ? isInterviewFinished(session) : false;
  const playback = useSimulatedPlayback(current?.text ?? '', {
    lang: session?.config.language === 'hi' ? 'hi-IN' : 'en-IN',
    autoPlay: isVoice && !pending,
    enabled: !!isVoice,
  });

  const answersGiven = useMemo(() => session?.turns.filter((turn) => turn.speaker === 'candidate').length ?? 0, [session?.turns]);
  const progress = session ? interviewProgress(session) : { asked: 0, total: 0 };

  // Recording timer (simulated — no microphone access).
  useEffect(() => {
    if (!recording) return;
    const timer = setInterval(() => setElapsed((e) => e + 1), 1000);
    return () => clearInterval(timer);
  }, [recording]);

  useEffect(() => {
    listRef.current?.lastElementChild?.scrollIntoView?.({ behavior: 'smooth', block: 'end' });
  }, [session?.turns.length, pending]);

  if (!session || !role) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background p-4">
        <ErrorState
          title={t('sessionNotFound')}
          description={t('sessionNotFoundDesc')}
          className="max-w-lg"
        />
      </div>
    );
  }
  if (session.status === 'completed' && session.reportId) return <Navigate to={`/interview/report/${session.reportId}`} replace />;

  const voiceState: VoiceState = recording ? 'recording' : pending ? 'processing' : playback.playing ? 'speaking' : 'idle';

  const send = async () => {
    const text = answer.trim();
    if (!text || pending || finished) return;
    const durationSec = isVoice ? Math.max(elapsed, Math.round(wordCount(text) / 2.3)) : undefined;
    setPending(true);
    setRecording(false);
    playback.pause();
    try {
      const next = await interviewService.answer(session, text, durationSec);
      saveSession(next);
      setAnswer('');
      setElapsed(0);
      textRef.current?.focus();
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setPending(false);
    }
  };

  const end = async () => {
    setEnding(true);
    playback.pause();
    try {
      const { session: done, report } = await interviewService.end(session);
      saveReport(done, report);
      track('interview_completed', { roleId: role.id, mode: session.config.mode, overall: report.overall, answers: report.questionFeedback.length });
      logPractice(report.durationSec / 60);
      pushNotification({ type: 'interview', title: t('reportReadyTitle', { role: role.shortTitle }), body: t('reportReadyBody', { score: report.overall }), link: `/interview/report/${report.id}` });
      toast.success(t('endedToast'));
      navigate(`/interview/report/${report.id}`, { replace: true });
    } catch (e) {
      toast.error(errorMessage(e));
      setEnding(false);
      setConfirmEnd(false);
    }
  };

  const toggleRecording = () => {
    if (recording) {
      setRecording(false);
      return;
    }
    playback.pause();
    setElapsed(0);
    setRecording(true);
    setTimeout(() => textRef.current?.focus(), 50);
  };

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="sticky top-0 z-20 border-b border-line bg-card">
        <div className="mx-auto flex max-w-5xl items-center gap-3 px-4 py-3">
          <Logo to="/dashboard" className="hidden sm:inline-flex" />
          <div className="min-w-0 flex-1 sm:border-l sm:border-line sm:pl-4">
            <p className="truncate text-sm font-semibold">{role.title}</p>
            <p className="truncate text-xs text-muted">
              {session.config.mode === 'voice' ? t('modeVoiceShort') : t('modeTextShort')} · {languageName(session.config.language)} · {session.config.level === 'fresher' ? t(LEVEL_KEYS.fresher.title) : t('yrs', { level: session.config.level })}
            </p>
          </div>
          <Button variant="outline" size="sm" onClick={() => setConfirmEnd(true)} leftIcon={<LogOut className="h-4 w-4" />} disabled={ending}>
            {t('endInterview')}
          </Button>
        </div>
        <div className="mx-auto flex max-w-5xl items-center gap-3 px-4 pb-3">
          <ProgressBar value={finished ? progress.total : Math.max(progress.asked - 1, 0)} max={progress.total} className="flex-1" size="sm" />
          <span className="whitespace-nowrap text-xs font-medium text-muted">
            {finished ? t('completed') : t('questionOf', { n: progress.asked, total: progress.total })}
          </span>
          {current && !finished && <Badge tone="primary" className="hidden sm:inline-flex">{t(STAGE_KEY[current.stage])}</Badge>}
        </div>
      </header>

      <main id="main" className="mx-auto flex w-full max-w-5xl flex-1 flex-col px-4 py-6">
        <Notice tone="warning" className="mb-5">{t('demoInterview')}</Notice>

        <ol ref={listRef} className="flex-1 space-y-5" aria-label={t('conversation')}>
          {session.turns.map((turn) => (
            <ChatBubble key={turn.id} turn={turn} current={!finished && turn.id === current?.id && !pending} userName={userName} />
          ))}
          {pending && <TypingIndicator />}
        </ol>
        <div className="sr-only" aria-live="polite">{!pending && current ? t('interviewerSays', { text: current.text }) : ''}</div>

        {finished ? (
          <Card className="mt-6 flex flex-col items-center p-6 text-center">
            <CircleCheck className="h-10 w-10 text-success" aria-hidden />
            <h2 className="mt-3 text-lg font-semibold">{t('completeTitle')}</h2>
            <p className="mt-1 max-w-md text-sm text-muted">{t('completeBody', { n: answersGiven })}</p>
            <Button className="mt-5" size="lg" onClick={end} loading={ending}>{t('viewMyReport')}</Button>
          </Card>
        ) : (
          <div className="sticky bottom-0 mt-6 -mx-4 border-t border-line bg-background/95 px-4 pb-4 pt-3 backdrop-blur">
            {isVoice && (
              <VoicePanel
                state={voiceState}
                elapsed={elapsed}
                onToggle={toggleRecording}
                disabled={pending || ending}
                playback={playback}
              />
            )}
            <form
              onSubmit={(e) => {
                e.preventDefault();
                void send();
              }}
              className="mt-3"
            >
              <label htmlFor="answer" className="text-sm font-medium">
                {isVoice ? t('transcriptionPreview') : t('yourAnswer')}
              </label>
              {isVoice && <p className="text-xs text-muted">{t('voiceDemoHint')}</p>}
              <textarea
                id="answer"
                ref={textRef}
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                    e.preventDefault();
                    void send();
                  }
                }}
                rows={isVoice ? 3 : 4}
                disabled={pending || ending}
                placeholder={isVoice ? (recording ? t('listeningPlaceholder') : t('pressMicPlaceholder')) : t('textPlaceholder')}
                className={cn(
                  'mt-1.5 w-full rounded-xl border bg-card px-3.5 py-3 text-sm leading-relaxed focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/30 disabled:bg-stone-50',
                  recording ? 'border-danger' : 'border-line-strong',
                )}
              />
              <div className="mt-2 flex flex-wrap items-center justify-between gap-2">
                <p className="text-xs text-muted">
                  {t('wordsSend', { n: wordCount(answer) })} <kbd className="rounded border border-line px-1">Ctrl</kbd> + <kbd className="rounded border border-line px-1">Enter</kbd> {t('toSend')}
                </p>
                <Button type="submit" disabled={!answer.trim() || pending || recording} loading={pending} leftIcon={<Send className="h-4 w-4" />}>
                  {t('sendAnswer')}
                </Button>
              </div>
            </form>
          </div>
        )}
      </main>

      <ConfirmationDialog
        open={confirmEnd}
        onOpenChange={setConfirmEnd}
        title={t('endConfirmTitle')}
        description={
          answersGiven < 3
            ? answersGiven === 1 ? t('endFewOne') : t('endFewMany', { n: answersGiven })
            : t('endSoFar')
        }
        confirmLabel={t('endAndSee')}
        variant={answersGiven < 3 ? 'danger' : 'primary'}
        onConfirm={end}
        loading={ending}
      />
    </div>
  );
}

function VoicePanel({
  state, elapsed, onToggle, disabled, playback,
}: {
  state: VoiceState;
  elapsed: number;
  onToggle: () => void;
  disabled: boolean;
  playback: ReturnType<typeof useSimulatedPlayback>;
}) {
  const t = useT(interviewMessages);
  const recording = state === 'recording';
  const label = t(({ idle: 'voiceIdle', recording: 'voiceRecording', processing: 'voiceProcessing', speaking: 'voiceSpeaking' } as const)[state]);
  return (
    <Card className="flex flex-col gap-4 p-4 sm:flex-row sm:items-center">
      <div className="flex items-center gap-4">
        <button
          type="button"
          onClick={onToggle}
          disabled={disabled}
          aria-pressed={recording}
          aria-label={recording ? t('stopRecording') : t('startRecording')}
          className={cn(
            'flex h-14 w-14 shrink-0 items-center justify-center rounded-full text-white transition-colors disabled:opacity-50',
            recording ? 'bg-danger animate-pulse-ring' : 'bg-primary hover:bg-primary-hover',
          )}
        >
          {recording ? <Square className="h-5 w-5 fill-current" /> : <Mic className="h-6 w-6" />}
        </button>
        <div>
          <p className="text-sm font-semibold" aria-live="polite">{label}</p>
          <p className="text-xs text-muted">
            {recording ? (
              <span className="inline-flex items-center gap-1.5 font-medium text-danger">
                <span className="h-2 w-2 rounded-full bg-danger" aria-hidden /> {formatClock(elapsed)}
              </span>
            ) : (
              t('noAudio')
            )}
          </p>
        </div>
      </div>
      <div className="flex flex-1 items-center gap-2 sm:border-l sm:border-line sm:pl-4">
        <Volume2 className="h-4 w-4 shrink-0 text-muted" aria-hidden />
        <Button variant="ghost" size="icon" onClick={playback.playing ? playback.pause : playback.play} aria-label={playback.playing ? t('pauseAudio') : t('playAudio')} disabled={disabled}>
          {playback.playing ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
        </Button>
        <Button variant="ghost" size="icon" onClick={playback.replay} aria-label={t('replayAudio')} disabled={disabled}>
          <RotateCcw className="h-4 w-4" />
        </Button>
        <ProgressBar value={playback.progress} className="flex-1" size="sm" />
        <span className="w-10 text-right text-xs text-muted">{playback.durationSec}s</span>
      </div>
      {!playback.speechAvailable && <p className="text-xs text-muted sm:hidden">{t('audioSimulated')}</p>}
    </Card>
  );
}

