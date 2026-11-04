import { UI_LANGUAGES, useI18nStore, useT } from './index';
import { layoutMessages } from './messages/layout';
import { cn } from '@/utils/cn';

/** EN | हिं segmented toggle for the website UI language. */
export function LanguageSwitcher({ className, size = 'sm' }: { className?: string; size?: 'sm' | 'md' }) {
  const lang = useI18nStore((s) => s.lang);
  const setLang = useI18nStore((s) => s.setLang);
  const t = useT(layoutMessages);
  return (
    <div role="group" aria-label={t('a11yLanguage')} className={cn('inline-flex rounded-full border border-line-strong bg-card p-0.5', className)}>
      {UI_LANGUAGES.map((l) => (
        <button
          key={l.code}
          type="button"
          lang={l.code}
          aria-pressed={lang === l.code}
          aria-label={l.label}
          onClick={() => setLang(l.code)}
          className={cn(
            'rounded-full font-semibold transition-colors',
            size === 'sm' ? 'px-2.5 py-1 text-xs' : 'px-3.5 py-1.5 text-sm',
            lang === l.code ? 'bg-primary text-white' : 'text-muted hover:text-ink',
          )}
        >
          {l.short}
        </button>
      ))}
    </div>
  );
}
