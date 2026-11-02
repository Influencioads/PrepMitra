import { useRef, useState } from 'react';
import { ActivityIndicator, Alert, Modal, Pressable, StyleSheet, View } from 'react-native';
import { Stack, router, useLocalSearchParams, usePreventRemove } from 'expo-router';
import { PanelRoom } from '@/features/interview/PanelRoom';
import { SafeAreaView } from 'react-native-safe-area-context';
import type { InterviewStage } from '@prepmitra/shared';
import { DISCLAIMERS, currentInterviewerTurn, interviewProgress, isInterviewFinished, languageName } from '@prepmitra/shared';
import { AppText, Badge, ConfirmDialog, EmptyState, Notice, ProgressBar, Screen, toast } from '@/components';
import { TextInterview } from '@/features/interview/TextInterview';
import { VoiceInterview } from '@/features/interview/VoiceInterview';
import { errorMessage, interviewService } from '@/services';
import { useInterviewStore } from '@/store';
import { colors, radii, spacing, TOUCH } from '@/theme';

const STAGE_LABEL: Record<InterviewStage, string> = {
  introduction: 'Introduction',
  resume: 'Resume',
  technical: 'Technical',
  situational: 'Situational',
  hr: 'HR',
  closing: 'Closing',
};

export default function InterviewSession() {
  const { sessionId = '' } = useLocalSearchParams<{ sessionId: string }>();
  const session = useInterviewStore((s) => s.sessions[sessionId]);
  const saveSession = useInterviewStore((s) => s.saveSession);
  const saveReport = useInterviewStore((s) => s.saveReport);
  const [thinking, setThinking] = useState(false);
  const [confirmEnd, setConfirmEnd] = useState(false);
  const [ending, setEnding] = useState(false);
  const endingRef = useRef(false);

  const active = !!session && session.status === 'in-progress' && !ending;
  const disablePrevention = usePreventRemove(active, ({ repeat }) => {
    Alert.alert('Leave the interview?', 'Your conversation is saved. You can continue it later from Home or Practice.', [
      { text: 'Stay', style: 'cancel' },
      { text: 'Leave', style: 'destructive', onPress: repeat },
    ]);
  });

  if (!session) {
    return (
      <Screen>
        <EmptyState icon="chatbubbles-outline" title="Interview not found" description="This interview isn’t on this device." actionLabel="Choose a role" onAction={() => router.replace('/interviews')} />
      </Screen>
    );
  }
  if (session.status === 'completed' && !ending) {
    return (
      <Screen>
        <EmptyState
          icon="checkmark-done-outline"
          title="This interview has ended"
          actionLabel={session.reportId ? 'View report' : 'Back to roles'}
          onAction={() => router.replace(session.reportId ? `/interview/report/${session.reportId}` : '/interviews')}
        />
      </Screen>
    );
  }

  const role = interviewService.getRoleSync(session.config.roleId);
  const finished = isInterviewFinished(session);
  const progress = interviewProgress(session);
  const stage = currentInterviewerTurn(session)?.stage ?? 'introduction';
  const answered = session.turns.filter((t) => t.speaker === 'candidate').length;

  const send = async (text: string, durationSec?: number) => {
    setThinking(true);
    try {
      const next = await interviewService.answer(session, text, durationSec);
      if (endingRef.current) return;
      saveSession(next);
    } catch (e) {
      toast.error(errorMessage(e));
    } finally {
      setThinking(false);
    }
  };

  const end = async () => {
    if (endingRef.current) return;
    endingRef.current = true;
    setConfirmEnd(false);
    setEnding(true);
    try {
      const latest = useInterviewStore.getState().sessions[sessionId] ?? session;
      const { session: done, report } = await interviewService.end(latest);
      saveReport(done, report);
      disablePrevention();
      toast.success('Interview complete. Here is your feedback.');
      router.replace(`/interview/report/${report.id}`);
    } catch (e) {
      endingRef.current = false;
      setEnding(false);
      toast.error(errorMessage(e));
    }
  };

  const header = (
    <View style={styles.header}>
      <PanelRoom
        speaking={thinking}
        status={finished ? 'The panel has finished. Tap End to get your report.' : thinking ? 'The chair is asking the next question…' : `Your turn · question ${progress.asked} of ${progress.total}`}
      />
      <View style={styles.headRow}>
        <Badge label={STAGE_LABEL[stage]} tone="secondary" />
        <Badge label={session.config.mode === 'voice' ? 'Voice (simulated)' : 'Text'} icon={session.config.mode === 'voice' ? 'mic-outline' : 'chatbubble-outline'} />
        <Badge label={languageName(session.config.language)} icon="language-outline" />
      </View>
      <ProgressBar
        value={progress.asked}
        max={progress.total}
        size="sm"
        tone="secondary"
        label={`Question ${progress.asked} of ${progress.total}`}
        showValue
        valueLabel={`${progress.asked}/${progress.total}`}
      />
      <Notice tone="warning">{DISCLAIMERS.demoInterview}</Notice>
    </View>
  );

  return (
    <SafeAreaView style={styles.flex} edges={['left', 'right']}>
      <Stack.Screen
        options={{
          title: role?.shortTitle ?? 'Interview',
          headerRight: () => (
            <Pressable
              onPress={() => setConfirmEnd(true)}
              accessibilityRole="button"
              accessibilityLabel="End interview"
              style={[styles.endBtn, finished && styles.endBtnReady]}
              hitSlop={4}
            >
              <AppText variant="smallStrong" color={finished ? colors.white : colors.error}>End</AppText>
            </Pressable>
          ),
        }}
      />
      {session.config.mode === 'voice' ? (
        <SafeAreaView style={styles.flex} edges={['bottom']}>
          <VoiceInterview session={session} thinking={thinking} finished={finished} onSend={(t, d) => void send(t, d)} header={header} />
        </SafeAreaView>
      ) : (
        <TextInterview session={session} thinking={thinking} finished={finished} onSend={(t) => void send(t)} header={header} />
      )}

      <ConfirmDialog
        visible={confirmEnd}
        title={finished ? 'See your report?' : 'End the interview now?'}
        message={
          finished
            ? 'The interview is complete. We’ll score your answers and build your report.'
            : `You’ve answered ${answered} question${answered === 1 ? '' : 's'}. Ending early lowers your scores for the questions you skipped. The credit is not refunded.`
        }
        confirmLabel={finished ? 'Get report' : 'End interview'}
        destructive={!finished}
        onCancel={() => setConfirmEnd(false)}
        onConfirm={() => void end()}
      />

      <Modal visible={ending} transparent animationType="fade" statusBarTranslucent>
        <View style={styles.overlay}>
          <View style={styles.overlayCard}>
            <ActivityIndicator size="large" color={colors.secondary} />
            <AppText variant="h3" align="center">Preparing your feedback…</AppText>
            <AppText variant="small" align="center">Scoring answers against the role rubric (demo rules).</AppText>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1, backgroundColor: colors.background },
  header: { gap: spacing.md },
  headRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  endBtn: { minHeight: TOUCH - 8, minWidth: TOUCH + 8, paddingHorizontal: 12, borderRadius: radii.full, borderWidth: 1, borderColor: colors.error, alignItems: 'center', justifyContent: 'center' },
  endBtnReady: { backgroundColor: colors.success, borderColor: colors.success },
  overlay: { flex: 1, backgroundColor: 'rgba(15, 23, 42, 0.55)', alignItems: 'center', justifyContent: 'center', padding: spacing.xl },
  overlayCard: { backgroundColor: colors.card, borderRadius: radii.xl, padding: spacing.xl, gap: spacing.md, alignItems: 'center', width: '100%', maxWidth: 340 },
});
