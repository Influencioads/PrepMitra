import { useEffect, useRef, useState, type ReactNode } from 'react';
import { ActivityIndicator, Animated, Easing, Pressable, ScrollView, StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { InterviewSession, InterviewStage } from '@prepmitra/shared';
import { currentInterviewerTurn, formatClock, wordCount } from '@prepmitra/shared';
import { AppText, Badge, Button, Card, Input, ProgressBar } from '@/components';
import { useNow } from '@/hooks/useNow';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import { colors, radii, spacing, TOUCH } from '@/theme';
import { ChatBubble } from './ChatBubble';

/**
 * Simulated voice interview. Nothing here touches the microphone or a speech
 * engine: "speaking" is a timer that reveals captions, "recording" is a timer
 * with a pulsing indicator, and the "transcript" is an editable scaffold the
 * candidate rewrites to what they would say.
 */
export type VoicePhase = 'speaking' | 'idle' | 'recording' | 'processing' | 'review' | 'waiting';

const SCAFFOLD: Record<InterviewStage, string> = {
  introduction: 'I am …, a … graduate from … . I am interested in this role because … .',
  resume: 'In my project at …, I was responsible for … . The challenge was … . I solved it by … and the result was … .',
  technical: 'The concept is … . For example, … . This matters because … .',
  situational: 'First I would … . Then I would … . Finally … , so that the result is … .',
  hr: 'My key strength is … . For example, when … , I … and the result was … .',
  closing: 'Could you tell me … ?',
};

/** ~150 words per minute speaking rate for the simulated interviewer voice. */
const speakMs = (text: string) => Math.max(2500, Math.min(20_000, wordCount(text) * 400));

export interface VoiceInterviewProps {
  session: InterviewSession;
  thinking: boolean;
  finished: boolean;
  onSend: (text: string, durationSec: number) => void;
  header: ReactNode;
}

export function VoiceInterview({ session, thinking, finished, onSend, header }: VoiceInterviewProps) {
  const question = currentInterviewerTurn(session);
  const [phase, setPhase] = useState<VoicePhase>('speaking');
  const [playing, setPlaying] = useState(true);
  const [spokenMs, setSpokenMs] = useState(0);
  const [recordStart, setRecordStart] = useState<number | null>(null);
  const [recordedSec, setRecordedSec] = useState(0);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);
  const lastQuestionId = useRef(question?.id);
  const duration = question ? speakMs(question.text) : 0;

  // A new interviewer turn starts "speaking" automatically.
  useEffect(() => {
    if (question?.id !== lastQuestionId.current) {
      lastQuestionId.current = question?.id;
      setSpokenMs(0);
      setPlaying(true);
      setPhase('speaking');
    }
  }, [question?.id]);

  useEffect(() => {
    if (thinking) setPhase('waiting');
  }, [thinking]);

  // Interviewer "speech" progress, driven by a timer.
  useEffect(() => {
    if (phase !== 'speaking' || !playing) return;
    const id = setInterval(() => setSpokenMs((ms) => Math.min(duration, ms + 100)), 100);
    return () => clearInterval(id);
  }, [phase, playing, duration]);

  // When the simulated audio reaches the end, hand the turn to the candidate.
  useEffect(() => {
    if (phase === 'speaking' && playing && duration > 0 && spokenMs >= duration) {
      setPlaying(false);
      if (!finished) setPhase('idle');
    }
  }, [phase, playing, spokenMs, duration, finished]);

  // Simulated transcription.
  useEffect(() => {
    if (phase !== 'processing') return;
    const t = setTimeout(() => {
      setTranscript(SCAFFOLD[question?.stage ?? 'introduction']);
      setPhase('review');
    }, 1200);
    return () => clearTimeout(t);
  }, [phase, question?.stage]);

  const now = useNow(250, phase === 'recording');
  const elapsedSec = recordStart ? Math.max(0, Math.floor((now - recordStart) / 1000)) : 0;

  const startRecording = () => {
    setError(null);
    setRecordStart(Date.now());
    setPhase('recording');
  };
  const stopRecording = () => {
    const secs = Math.max(1, Math.round((Date.now() - (recordStart ?? Date.now())) / 1000));
    setRecordedSec(secs);
    setRecordStart(null);
    setPhase('processing');
  };
  const send = () => {
    const clean = transcript.replace(/…/g, '').trim();
    if (wordCount(clean) < 3) {
      setError('Edit the transcript so it matches what you said (at least a few words).');
      return;
    }
    onSend(clean, recordedSec);
    setTranscript('');
  };
  const replay = () => {
    setSpokenMs(0);
    setPlaying(true);
    setPhase('speaking');
  };

  const shownChars = question ? Math.ceil((spokenMs / Math.max(duration, 1)) * question.text.length) : 0;
  const captions = question ? (phase === 'speaking' ? question.text.slice(0, shownChars) : question.text) : '';
  const history = session.turns.slice(0, -1);

  return (
    <ScrollView contentContainerStyle={styles.body} keyboardShouldPersistTaps="handled" showsVerticalScrollIndicator={false}>
      {header}

      <Card style={styles.speaker}>
        <View style={styles.speakerHead}>
          <View style={[styles.avatar, phase === 'speaking' && playing && styles.avatarLive]}>
            <Ionicons name="person" size={22} color={colors.white} />
          </View>
          <View style={styles.flex}>
            <AppText variant="bodyStrong">Interviewer</AppText>
            <AppText variant="caption">
              {phase === 'speaking' ? (playing ? 'Speaking… (simulated voice)' : 'Paused') : phase === 'waiting' ? 'Thinking…' : 'Finished speaking'}
            </AppText>
          </View>
          {question?.isFollowUp && <Badge label="Follow-up" tone="secondary" />}
        </View>
        <AppText variant="body" style={styles.caption} accessibilityLiveRegion="polite">
          {phase === 'waiting' ? '…' : captions}
        </AppText>
        <ProgressBar value={phase === 'speaking' ? spokenMs : duration} max={duration || 1} size="sm" tone="secondary" label="Interviewer audio progress" />
        <View style={styles.controls}>
          <ControlButton
            icon={playing && phase === 'speaking' ? 'pause' : 'play'}
            label={playing && phase === 'speaking' ? 'Pause interviewer' : 'Play interviewer'}
            disabled={phase === 'waiting' || phase === 'recording' || phase === 'processing'}
            onPress={() => {
              if (phase !== 'speaking') {
                if (spokenMs >= duration) setSpokenMs(0);
                setPhase('speaking');
                setPlaying(true);
              } else setPlaying((p) => !p);
            }}
          />
          <ControlButton icon="refresh" label="Replay question" disabled={phase === 'waiting' || phase === 'recording' || phase === 'processing'} onPress={replay} />
          <AppText variant="caption" style={styles.flex} align="right">
            {formatClock((phase === 'speaking' ? spokenMs : duration) / 1000)} / {formatClock(duration / 1000)}
          </AppText>
        </View>
      </Card>

      {finished ? (
        <Card tone="primary">
          <AppText variant="bodyStrong">The interview is complete.</AppText>
          <AppText variant="small">Tap “End” in the top bar to see your report.</AppText>
        </Card>
      ) : phase === 'review' ? (
        <Card style={styles.review}>
          <View style={styles.reviewHead}>
            <AppText variant="bodyStrong" style={styles.flex}>Transcript preview</AppText>
            <Badge label={`${recordedSec}s recorded`} icon="mic-outline" />
          </View>
          <Input
            label="Simulated transcript — edit it to match what you said"
            value={transcript}
            onChangeText={(t) => {
              setTranscript(t);
              setError(null);
            }}
            multiline
            maxLength={2000}
            error={error ?? undefined}
            hint={`${wordCount(transcript.replace(/…/g, ''))} words`}
          />
          <View style={styles.row}>
            <Button title="Re-record" variant="outline" leftIcon="mic-outline" onPress={startRecording} style={styles.flex} />
            <Button title="Send answer" leftIcon="send" onPress={send} style={styles.flex} />
          </View>
        </Card>
      ) : (
        <MicPanel phase={phase} elapsedSec={elapsedSec} onStart={startRecording} onStop={stopRecording} />
      )}

      {history.length > 0 && (
        <View style={styles.history}>
          <Button
            title={showHistory ? 'Hide conversation' : `Show conversation (${history.length})`}
            variant="ghost"
            size="sm"
            rightIcon={showHistory ? 'chevron-up' : 'chevron-down'}
            onPress={() => setShowHistory((s) => !s)}
          />
          {showHistory && history.map((t) => <ChatBubble key={t.id} turn={t} />)}
        </View>
      )}
    </ScrollView>
  );
}

function ControlButton({ icon, label, onPress, disabled }: { icon: 'play' | 'pause' | 'refresh'; label: string; onPress: () => void; disabled?: boolean }) {
  return (
    <Pressable
      onPress={disabled ? undefined : onPress}
      accessibilityRole="button"
      accessibilityLabel={label}
      accessibilityState={{ disabled: !!disabled }}
      style={[styles.control, disabled && styles.disabled]}
    >
      <Ionicons name={icon} size={20} color={colors.secondary} />
    </Pressable>
  );
}

function MicPanel({ phase, elapsedSec, onStart, onStop }: { phase: VoicePhase; elapsedSec: number; onStart: () => void; onStop: () => void }) {
  const [pulse] = useState(() => new Animated.Value(0));
  const recording = phase === 'recording';
  const reduceMotion = useReducedMotion();
  useEffect(() => {
    if (!recording || reduceMotion) {
      pulse.setValue(0);
      return;
    }
    const loop = Animated.loop(Animated.timing(pulse, { toValue: 1, duration: 1200, easing: Easing.out(Easing.quad), useNativeDriver: true }));
    loop.start();
    return () => loop.stop();
  }, [recording, pulse, reduceMotion]);

  const disabled = phase === 'speaking' || phase === 'waiting' || phase === 'processing';
  const label =
    phase === 'recording' ? 'Recording… tap to stop' :
    phase === 'processing' ? 'Transcribing (simulated)…' :
    phase === 'waiting' ? 'Waiting for the interviewer…' :
    phase === 'speaking' ? 'Listen to the question first' :
    'Tap the mic to answer';

  return (
    <View style={styles.micWrap}>
      <View style={styles.micStage}>
        {recording && (
          <Animated.View
            pointerEvents="none"
            style={[
              styles.ring,
              { opacity: pulse.interpolate({ inputRange: [0, 1], outputRange: [0.5, 0] }), transform: [{ scale: pulse.interpolate({ inputRange: [0, 1], outputRange: [1, 1.7] }) }] },
            ]}
          />
        )}
        <Pressable
          onPress={disabled ? undefined : recording ? onStop : onStart}
          accessibilityRole="button"
          accessibilityLabel={recording ? 'Stop recording' : 'Start answering'}
          accessibilityHint="Simulated recording; the microphone is not used in this prototype"
          accessibilityState={{ disabled, busy: phase === 'processing' }}
          style={[styles.mic, recording && styles.micRec, disabled && styles.micOff]}
        >
          {phase === 'processing' ? (
            <ActivityIndicator color={colors.white} size="large" />
          ) : (
            <Ionicons name={recording ? 'stop' : 'mic'} size={40} color={colors.white} />
          )}
        </Pressable>
      </View>
      {recording && (
        <View style={styles.recRow} accessibilityLiveRegion="polite">
          <View style={styles.recDot} />
          <AppText variant="bodyStrong" color={colors.error} style={styles.mono}>REC {formatClock(elapsedSec)}</AppText>
        </View>
      )}
      <AppText variant="small" align="center">{label}</AppText>
      <AppText variant="caption" align="center">Aim for 45–90 seconds. The microphone is not accessed in this prototype.</AppText>
    </View>
  );
}

const MIC = 104;

const styles = StyleSheet.create({
  flex: { flex: 1 },
  body: { padding: spacing.lg, gap: spacing.lg, paddingBottom: spacing['3xl'] },
  speaker: { gap: spacing.md },
  speakerHead: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  avatar: { width: 44, height: 44, borderRadius: 22, backgroundColor: colors.secondary, alignItems: 'center', justifyContent: 'center' },
  avatarLive: { borderWidth: 3, borderColor: '#BFD8CA' },
  caption: { fontSize: 17, lineHeight: 26, minHeight: 52 },
  controls: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  control: { width: TOUCH, height: TOUCH, borderRadius: TOUCH / 2, backgroundColor: colors.secondarySoft, alignItems: 'center', justifyContent: 'center' },
  disabled: { opacity: 0.4 },
  micWrap: { alignItems: 'center', gap: spacing.sm, paddingVertical: spacing.lg },
  micStage: { width: MIC * 1.8, height: MIC * 1.8, alignItems: 'center', justifyContent: 'center' },
  ring: { position: 'absolute', width: MIC, height: MIC, borderRadius: MIC / 2, backgroundColor: colors.error },
  mic: { width: MIC, height: MIC, borderRadius: MIC / 2, backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center', elevation: 6, shadowColor: colors.primary, shadowOpacity: 0.35, shadowRadius: 12, shadowOffset: { width: 0, height: 6 } },
  micRec: { backgroundColor: colors.error, shadowColor: colors.error },
  micOff: { backgroundColor: colors.borderStrong, shadowOpacity: 0, elevation: 0 },
  recRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  recDot: { width: 10, height: 10, borderRadius: 5, backgroundColor: colors.error },
  mono: { fontVariant: ['tabular-nums'] },
  review: { gap: spacing.md },
  reviewHead: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  row: { flexDirection: 'row', gap: spacing.sm },
  history: { gap: spacing.md, borderRadius: radii.lg },
});
