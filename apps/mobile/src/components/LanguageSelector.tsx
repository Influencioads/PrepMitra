import { useMemo } from 'react';
import type { LanguageCode } from '@prepmitra/shared';
import { LANGUAGES } from '@prepmitra/shared';
import { Select } from './Select';

export interface LanguageSelectorProps {
  label?: string;
  value: LanguageCode | '' | undefined;
  onChange: (code: LanguageCode) => void;
  /** Restrict to these codes (e.g. the exam's languages). */
  allowed?: LanguageCode[];
  voiceOnly?: boolean;
  hint?: string;
  error?: string;
  allowClear?: boolean;
  onClear?: () => void;
}

export function LanguageSelector({ label = 'Language', value, onChange, allowed, voiceOnly, hint, error, allowClear, onClear }: LanguageSelectorProps) {
  const options = useMemo(
    () =>
      LANGUAGES.filter((l) => l.enabled && (!allowed || allowed.includes(l.code)) && (!voiceOnly || l.voiceSupported)).map((l) => ({
        value: l.code,
        label: l.code === 'en' ? 'English' : `${l.name} · ${l.nativeName}`,
        description: l.voiceSupported ? 'Exams, text and voice interviews' : 'Exams and text interviews',
      })),
    [allowed, voiceOnly],
  );
  return (
    <Select<LanguageCode>
      label={label}
      value={value}
      options={options}
      onChange={onChange}
      hint={hint}
      error={error}
      searchable={options.length > 8}
      allowClear={allowClear}
      onClear={onClear}
    />
  );
}
