import { useMemo, useState } from 'react';
import { FlatList, Pressable, StyleSheet, View } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { colors, radii, spacing, TOUCH } from '@/theme';
import { AppText } from './AppText';
import { BottomSheet } from './BottomSheet';
import { Input } from './Input';

export interface SelectOption<T extends string = string> {
  value: T;
  label: string;
  description?: string;
}

export interface SelectProps<T extends string = string> {
  label: string;
  value: T | '' | undefined;
  options: SelectOption<T>[];
  onChange: (value: T) => void;
  placeholder?: string;
  error?: string;
  hint?: string;
  required?: boolean;
  /** Shows a search field in the sheet (defaults to on for long lists). */
  searchable?: boolean;
  allowClear?: boolean;
  onClear?: () => void;
}

/** Form field that opens a bottom-sheet picker. */
export function Select<T extends string = string>({
  label, value, options, onChange, placeholder = 'Select', error, hint, required, searchable, allowClear, onClear,
}: SelectProps<T>) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const selected = options.find((o) => o.value === value);
  const showSearch = searchable ?? options.length > 10;
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return q ? options.filter((o) => `${o.label} ${o.description ?? ''}`.toLowerCase().includes(q)) : options;
  }, [options, query]);

  const close = () => {
    setOpen(false);
    setQuery('');
  };

  return (
    <View style={styles.wrap}>
      <AppText variant="label">
        {label}
        {required ? <AppText variant="label" color={colors.error}> *</AppText> : null}
      </AppText>
      <Pressable
        onPress={() => setOpen(true)}
        accessibilityRole="button"
        accessibilityLabel={`${label}: ${selected?.label ?? 'not selected'}`}
        accessibilityHint="Opens a list of options"
        style={[styles.field, !!error && styles.errorField]}
      >
        <AppText variant="body" color={selected ? colors.text : colors.textMuted} style={styles.flex} numberOfLines={1}>
          {selected?.label ?? placeholder}
        </AppText>
        <Ionicons name="chevron-down" size={18} color={colors.textSecondary} />
      </Pressable>
      {error ? (
        <AppText variant="small" color={colors.error} accessibilityRole="alert">{error}</AppText>
      ) : hint ? (
        <AppText variant="caption">{hint}</AppText>
      ) : null}

      <BottomSheet visible={open} onClose={close} title={label} scroll={false}>
        {showSearch && (
          <Input label="Search" value={query} onChangeText={setQuery} placeholder={`Search ${label.toLowerCase()}`} autoCorrect={false} returnKeyType="search" />
        )}
        {allowClear && onClear && (
          <Pressable
            onPress={() => {
              onClear();
              close();
            }}
            accessibilityRole="button"
            style={styles.option}
          >
            <AppText variant="body" color={colors.textSecondary} style={styles.flex}>None</AppText>
          </Pressable>
        )}
        <FlatList
          data={filtered}
          keyExtractor={(o) => o.value}
          keyboardShouldPersistTaps="handled"
          initialNumToRender={20}
          ListEmptyComponent={<AppText variant="small" style={styles.empty}>No matches for “{query}”.</AppText>}
          renderItem={({ item }) => {
            const active = item.value === value;
            return (
              <Pressable
                onPress={() => {
                  onChange(item.value);
                  close();
                }}
                accessibilityRole="radio"
                accessibilityState={{ checked: active }}
                accessibilityLabel={item.description ? `${item.label}, ${item.description}` : item.label}
                style={({ pressed }) => [styles.option, active && styles.optionActive, pressed && styles.pressed]}
              >
                <View style={styles.flex}>
                  <AppText variant="body" weight={active ? '600' : '400'} color={active ? colors.primary : colors.text}>
                    {item.label}
                  </AppText>
                  {item.description ? <AppText variant="caption">{item.description}</AppText> : null}
                </View>
                {active && <Ionicons name="checkmark" size={20} color={colors.primary} />}
              </Pressable>
            );
          }}
        />
      </BottomSheet>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 6 },
  field: {
    minHeight: TOUCH + 4,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    borderWidth: 1,
    borderColor: colors.borderStrong,
    borderRadius: radii.md,
    paddingHorizontal: spacing.md,
    backgroundColor: colors.white,
  },
  errorField: { borderColor: colors.error },
  flex: { flex: 1 },
  option: {
    minHeight: TOUCH + 4,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    paddingHorizontal: spacing.md,
    borderRadius: radii.md,
  },
  optionActive: { backgroundColor: colors.primarySoft },
  pressed: { backgroundColor: '#F1F5F9' },
  empty: { padding: spacing.lg, textAlign: 'center' },
});
