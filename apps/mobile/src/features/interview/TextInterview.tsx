import { use, useEffect, useRef, useState, type ReactNode } from 'react';
import { FlatList, KeyboardAvoidingView, Platform, Pressable, StyleSheet, TextInput, View, type FlatListInstance } from 'react-native';
import { HeaderHeightContext } from 'expo-router/react-navigation';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { InterviewSession } from '@prepmitra/shared';
import { wordCount } from '@prepmitra/shared';
import { AppText } from '@/components';
import { colors, radii, spacing, TOUCH } from '@/theme';
import { ChatBubble } from './ChatBubble';
import { TypingIndicator } from './TypingIndicator';

export interface TextInterviewProps {
  session: InterviewSession;
  thinking: boolean;
  finished: boolean;
  onSend: (text: string) => void;
  header: ReactNode;
}

/** Chat-style interview with a keyboard-aware composer. */
export function TextInterview({ session, thinking, finished, onSend, header }: TextInterviewProps) {
  const [text, setText] = useState('');
  const listRef = useRef<FlatListInstance>(null);
  const insets = useSafeAreaInsets();
  const headerHeight = use(HeaderHeightContext) ?? 0;
  const words = wordCount(text);
  const canSend = text.trim().length > 0 && !thinking && !finished;

  useEffect(() => {
    const t = setTimeout(() => listRef.current?.scrollToEnd({ animated: true }), 80);
    return () => clearTimeout(t);
  }, [session.turns.length, thinking]);

  const send = () => {
    if (!canSend) return;
    onSend(text.trim());
    setText('');
  };

  return (
    <KeyboardAvoidingView style={styles.flex} behavior="padding" keyboardVerticalOffset={headerHeight}>
      <FlatList
        ref={listRef}
        data={session.turns}
        keyExtractor={(t) => t.id}
        renderItem={({ item }) => <ChatBubble turn={item} />}
        ListHeaderComponent={<View style={styles.header}>{header}</View>}
        ListFooterComponent={thinking ? <TypingIndicator /> : undefined}
        contentContainerStyle={styles.list}
        keyboardShouldPersistTaps="handled"
        keyboardDismissMode={Platform.OS === 'ios' ? 'interactive' : 'on-drag'}
      />
      <View style={[styles.composer, { paddingBottom: Math.max(insets.bottom, spacing.sm) }]}>
        {finished ? (
          <AppText variant="small" align="center" style={styles.flex}>The interview is complete. Tap “End” to see your report.</AppText>
        ) : (
          <>
            <View style={styles.inputWrap}>
              <TextInput
                value={text}
                onChangeText={setText}
                placeholder={thinking ? 'Waiting for the interviewer…' : 'Type your answer'}
                placeholderTextColor={colors.textMuted}
                multiline
                maxLength={2000}
                editable={!thinking}
                accessibilityLabel="Your answer"
                accessibilityHint="Aim for 45 to 90 seconds of speaking, about 80 to 160 words"
                style={styles.input}
              />
              <AppText variant="caption" style={styles.count}>{words} words{words > 0 && words < 20 ? ' · add an example' : ''}</AppText>
            </View>
            <Pressable
              onPress={send}
              disabled={!canSend}
              accessibilityRole="button"
              accessibilityLabel="Send answer"
              accessibilityState={{ disabled: !canSend }}
              style={[styles.send, !canSend && styles.sendOff]}
            >
              <Ionicons name="send" size={20} color={colors.white} />
            </Pressable>
          </>
        )}
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  header: { gap: spacing.md, marginBottom: spacing.sm },
  list: { padding: spacing.lg, gap: spacing.md },
  composer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: spacing.sm,
    paddingHorizontal: spacing.md,
    paddingTop: spacing.sm,
    backgroundColor: colors.card,
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: colors.border,
  },
  inputWrap: { flex: 1, borderWidth: 1, borderColor: colors.borderStrong, borderRadius: radii.lg, paddingHorizontal: spacing.md, paddingTop: 8, paddingBottom: 4, backgroundColor: colors.white },
  input: { fontSize: 16, color: colors.text, minHeight: 40, maxHeight: 140, paddingVertical: 0 },
  count: { textAlign: 'right' },
  send: { width: TOUCH + 4, height: TOUCH + 4, borderRadius: (TOUCH + 4) / 2, backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center', marginBottom: 2 },
  sendOff: { backgroundColor: colors.borderStrong },
});
