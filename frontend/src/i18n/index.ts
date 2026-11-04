import { useCallback, useEffect } from 'react';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { setFormatLanguage } from '@prepmitra/shared';
import { demoStorage } from '@/store/storage';

/**
 * Lightweight i18n for the website UI (English + Hindi for launch, per the 15-day plan).
 * Exam content languages (22 + English) are separate: they come from the question bank.
 *
 * Usage:
 *   const t = useT(dashboardMessages);
 *   t('welcome', { name: 'Ananya' })
 * Messages live in src/i18n/messages/<namespace>.ts, one file per screen area.
 */
export type UiLang = 'en' | 'hi';

export const UI_LANGUAGES: { code: UiLang; label: string; short: string }[] = [
  { code: 'en', label: 'English', short: 'EN' },
  { code: 'hi', label: 'हिन्दी', short: 'हिं' },
];

interface I18nState {
  lang: UiLang;
  setLang: (lang: UiLang) => void;
}

export const useI18nStore = create<I18nState>()(
  persist((set) => ({ lang: 'en', setLang: (lang) => set({ lang }) }), { name: 'pm.ui-lang', storage: demoStorage }),
);

// Dates and relative times ("2 days ago") follow the UI language.
setFormatLanguage(useI18nStore.getState().lang);
useI18nStore.subscribe((s) => setFormatLanguage(s.lang));

export const useUiLang = () => useI18nStore((s) => s.lang);

export interface Messages<T extends Record<string, string>> {
  en: T;
  hi: { [K in keyof T]: string };
}

/** Declares a namespace; TypeScript enforces that Hindi has every English key. */
export function defineMessages<T extends Record<string, string>>(m: Messages<T>): Messages<T> {
  return m;
}

export type Vars = Record<string, string | number>;

export function format(template: string, vars?: Vars): string {
  if (!vars) return template;
  return template.replace(/\{\{\s*(\w+)\s*\}\}/g, (_, k: string) => (vars[k] !== undefined ? String(vars[k]) : `{{${k}}}`));
}

/** Non-hook translate, for code outside components (toasts in services, etc.). */
export function translate<T extends Record<string, string>>(messages: Messages<T>, key: keyof T, vars?: Vars): string {
  const lang = useI18nStore.getState().lang;
  return format((messages[lang] as Record<keyof T, string>)[key] ?? messages.en[key], vars);
}

export function useT<T extends Record<string, string>>(messages: Messages<T>) {
  const lang = useUiLang();
  return useCallback(
    (key: keyof T, vars?: Vars) => format((messages[lang] as Record<keyof T, string>)[key] ?? messages.en[key], vars),
    [lang, messages],
  );
}

/** Keeps <html lang> in sync for screen readers and fonts. Mount once in App. */
export function useSyncHtmlLang() {
  const lang = useUiLang();
  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);
}
