import { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { AppText, Select } from '@/components';
import { colors, spacing } from '@/theme';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const pad = (n: number) => String(n).padStart(2, '0');

/**
 * Date of birth as three pickers (day / month / year) producing YYYY-MM-DD
 * once all three are chosen (empty string otherwise). Avoids a native
 * date-picker dependency and behaves the same on iOS and Android.
 */
export function DateField({ label, value, onChange, error }: { label: string; value: string; onChange: (v: string) => void; error?: string }) {
  const initial = /^\d{4}-\d{2}-\d{2}$/.test(value) ? value.split('-') : ['', '', ''];
  const [parts, setParts] = useState({ y: initial[0] ?? '', m: initial[1] ?? '', d: initial[2] ?? '' });
  const thisYear = new Date().getFullYear();
  const years = Array.from({ length: 63 }, (_, i) => String(thisYear - 18 - i));
  const daysInMonth = parts.y && parts.m ? new Date(Number(parts.y), Number(parts.m), 0).getDate() : 31;

  const update = (key: 'y' | 'm' | 'd', v: string) => {
    const next = { ...parts, [key]: v };
    if (next.y && next.m && next.d) {
      const max = new Date(Number(next.y), Number(next.m), 0).getDate();
      if (Number(next.d) > max) next.d = pad(max);
      onChange(`${next.y}-${next.m}-${next.d}`);
    } else {
      onChange('');
    }
    setParts(next);
  };

  return (
    <View style={styles.wrap}>
      <AppText variant="label">
        {label}
        <AppText variant="label" color={colors.error}> *</AppText>
      </AppText>
      <View style={styles.row}>
        <View style={styles.day}>
          <Select
            label="Day"
            value={parts.d}
            options={Array.from({ length: daysInMonth }, (_, i) => ({ value: pad(i + 1), label: String(i + 1) }))}
            onChange={(v) => update('d', v)}
            placeholder="DD"
          />
        </View>
        <View style={styles.month}>
          <Select label="Month" value={parts.m} options={MONTHS.map((mm, i) => ({ value: pad(i + 1), label: mm }))} onChange={(v) => update('m', v)} placeholder="MM" />
        </View>
        <View style={styles.year}>
          <Select label="Year" value={parts.y} options={years.map((yy) => ({ value: yy, label: yy }))} onChange={(v) => update('y', v)} placeholder="YYYY" />
        </View>
      </View>
      {error ? <AppText variant="small" color={colors.error} accessibilityRole="alert">{error}</AppText> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 6 },
  row: { flexDirection: 'row', gap: spacing.sm },
  day: { flex: 1 },
  month: { flex: 1.1 },
  year: { flex: 1.3 },
});
