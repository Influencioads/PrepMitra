import { LANGUAGES, type LanguageCode } from '@prepmitra/shared';
import { Select } from './FormControls';

export interface LanguageSelectorProps {
  value: LanguageCode | string;
  onChange: (code: LanguageCode) => void;
  label?: string;
  /** Restrict to these languages (e.g. the languages an exam is offered in). */
  allowed?: LanguageCode[];
  voiceOnly?: boolean;
  error?: string;
  hint?: string;
  className?: string;
  id?: string;
}

/** Language picker for all 22 scheduled Indian languages plus English. */
export function LanguageSelector({ value, onChange, label = 'Language', allowed, voiceOnly, error, hint, className, id }: LanguageSelectorProps) {
  const options = LANGUAGES.filter((l) => l.enabled && (!allowed || allowed.includes(l.code)) && (!voiceOnly || l.voiceSupported)).map((l) => ({
    value: l.code,
    label: l.code === 'en' ? 'English' : `${l.name} — ${l.nativeName}`,
  }));
  return (
    <Select
      id={id}
      label={label}
      value={value}
      onChange={(e) => onChange(e.target.value as LanguageCode)}
      options={options}
      error={error}
      hint={hint}
      containerClassName={className}
    />
  );
}
