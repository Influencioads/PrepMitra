import { StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import type { InterviewRole } from '@prepmitra/shared';
import { pluralize } from '@prepmitra/shared';
import { colors, spacing } from '@/theme';
import { ICONS } from '@/utils/icons';
import { AppText } from './AppText';
import { Badge } from './Badge';
import { Card } from './Card';
import { IconTile } from './IconTile';

export function InterviewCard({ role, onPress, compact }: { role: InterviewRole; onPress: () => void; compact?: boolean }) {
  return (
    <Card
      onPress={onPress}
      accessibilityLabel={`${role.title}. ${role.category}. ${role.durationMin} minutes. ${role.voiceAvailable ? 'Text or voice.' : 'Text only.'}`}
      accessibilityHint="Opens interview setup"
      style={styles.card}
    >
      <View style={styles.top}>
        <IconTile name={ICONS[role.icon]} tone="secondary" size={44} />
        <View style={styles.titleWrap}>
          <AppText variant="caption">{role.category}</AppText>
          <AppText variant="bodyStrong" numberOfLines={2}>{role.title}</AppText>
        </View>
        <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
      </View>
      {!compact && <AppText variant="small" numberOfLines={2}>{role.description}</AppText>}
      <View style={styles.badges}>
        <Badge label={`${role.durationMin} min`} icon="time-outline" />
        <Badge label={`${role.questionCount}+ questions`} />
        <Badge label={role.voiceAvailable ? 'Text · Voice' : 'Text'} icon={role.voiceAvailable ? 'mic-outline' : 'chatbubble-outline'} tone="secondary" />
        <Badge label={pluralize(Math.max(role.creditCost, 1), 'credit')} tone="primary" icon="wallet-outline" />
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  card: { gap: spacing.md },
  top: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  titleWrap: { flex: 1, gap: 2 },
  badges: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
});
