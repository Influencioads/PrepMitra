import { StyleSheet, View } from 'react-native';
import type { InterviewTurn } from '@prepmitra/shared';
import { AppText } from '@/components';
import { colors, radii, spacing } from '@/theme';

export function ChatBubble({ turn }: { turn: InterviewTurn }) {
  const mine = turn.speaker === 'candidate';
  return (
    <View
      style={[styles.row, mine && styles.rowMine]}
      accessible
      accessibilityLabel={`${mine ? 'You' : 'Interviewer'}${turn.isFollowUp ? ', follow-up' : ''}: ${turn.text}`}
    >
      <View style={[styles.bubble, mine ? styles.mine : styles.theirs]}>
        {!mine && (
          <AppText variant="caption" color={colors.secondary} weight="700">
            Interviewer{turn.isFollowUp ? ' · follow-up' : ''}
          </AppText>
        )}
        <AppText variant="body" color={mine ? colors.white : colors.text} selectable>{turn.text}</AppText>
        {mine && turn.durationSec ? <AppText variant="caption" color="#FCD9A8">{turn.durationSec}s spoken (simulated)</AppText> : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', justifyContent: 'flex-start' },
  rowMine: { justifyContent: 'flex-end' },
  bubble: { maxWidth: '86%', paddingHorizontal: spacing.md, paddingVertical: spacing.sm + 2, borderRadius: radii.lg, gap: 2 },
  mine: { backgroundColor: colors.primary, borderBottomRightRadius: 4 },
  theirs: { backgroundColor: colors.card, borderWidth: StyleSheet.hairlineWidth, borderColor: colors.border, borderBottomLeftRadius: 4 },
});
