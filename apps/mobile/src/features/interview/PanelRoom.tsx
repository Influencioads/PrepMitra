import { StyleSheet, Text, View } from 'react-native';
import Svg, { Ellipse, Rect } from 'react-native-svg';
import { paper } from '@/theme';

/**
 * The interview "panel room": three panel members around a table with the chair highlighted.
 * Decorative framing for the session; the status line is announced for screen readers.
 */
export function PanelRoom({ speaking, status }: { speaking: boolean; status: string }) {
  return (
    <View style={styles.room} accessible accessibilityLabel={`Interview panel. ${status}`}>
      <Svg width="100%" height={120} viewBox="0 0 320 120" preserveAspectRatio="xMidYMid meet" style={styles.table}>
        <Ellipse cx={160} cy={78} rx={130} ry={34} fill={paper.wood} />
        <Ellipse cx={160} cy={73} rx={130} ry={34} fill={paper.woodLight} />
        <Rect x={124} y={60} width={30} height={20} rx={2} fill={paper.paper} transform="rotate(-6 139 70)" />
        <Rect x={166} y={61} width={26} height={18} rx={2} fill={paper.paper} transform="rotate(5 179 70)" />
      </Svg>
      <View style={styles.seats} importantForAccessibility="no-hide-descendants">
        <Seat initials="BK" label="Banking" />
        <Seat initials="CH" label={speaking ? 'Chair · speaking' : 'Chair · listening'} chair active={speaking} />
        <Seat initials="HR" label="HR" />
      </View>
      <Text style={styles.status} maxFontSizeMultiplier={1.3}>{status}</Text>
    </View>
  );
}

function Seat({ initials, label, chair, active }: { initials: string; label: string; chair?: boolean; active?: boolean }) {
  return (
    <View style={[styles.seat, chair && styles.chairSeat]}>
      <View style={[styles.avatar, chair && styles.chair, active && styles.active]}>
        <Text style={[styles.initials, chair && { fontSize: 17 }]}>{initials}</Text>
      </View>
      <Text style={[styles.seatLabel, chair && { color: '#F28C28', fontWeight: '700' }]} numberOfLines={1}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  room: { backgroundColor: paper.chalkDeep, borderRadius: 20, paddingTop: 14, paddingBottom: 12, paddingHorizontal: 12, overflow: 'hidden' },
  table: { position: 'absolute', left: 0, right: 0, top: 34 },
  seats: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', paddingHorizontal: 10, height: 120 },
  seat: { alignItems: 'center', gap: 4, marginTop: 14, width: 84 },
  chairSeat: { marginTop: 0 },
  avatar: { width: 48, height: 48, borderRadius: 24, backgroundColor: '#2C4A3D', borderWidth: 2, borderColor: 'rgba(245,243,234,0.3)', alignItems: 'center', justifyContent: 'center' },
  chair: { width: 58, height: 58, borderRadius: 29, backgroundColor: '#C2410C', borderColor: 'rgba(242,140,40,0.45)', borderWidth: 5 },
  active: { borderColor: '#F28C28' },
  initials: { color: paper.chalkText, fontWeight: '800', fontSize: 15 },
  seatLabel: { color: paper.chalkMuted, fontSize: 11 },
  status: { color: paper.chalkText, textAlign: 'center', fontSize: 13, marginTop: 4 },
});
