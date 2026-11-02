import { useId, useRef, type KeyboardEvent, type ReactNode } from 'react';
import { cn } from '@/utils/cn';

export interface RadioCardOption<T extends string> {
  value: T;
  title: ReactNode;
  description?: ReactNode;
  icon?: ReactNode;
  disabled?: boolean;
}

/** Accessible radio group rendered as selectable cards (arrow keys move selection). */
export function RadioCards<T extends string>({
  label, options, value, onChange, error, columns = 3,
}: { label: string; options: RadioCardOption<T>[]; value: T; onChange: (v: T) => void; error?: string; columns?: 2 | 3 }) {
  const id = useId();
  const refs = useRef<(HTMLButtonElement | null)[]>([]);
  const enabled = options.filter((o) => !o.disabled);
  const onKey = (e: KeyboardEvent, current: T) => {
    if (!['ArrowRight', 'ArrowDown', 'ArrowLeft', 'ArrowUp'].includes(e.key)) return;
    e.preventDefault();
    const idx = enabled.findIndex((o) => o.value === current);
    const dir = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : -1;
    const next = enabled[(idx + dir + enabled.length) % enabled.length]!;
    onChange(next.value);
    refs.current[options.indexOf(next)]?.focus();
  };
  return (
    <fieldset>
      <legend id={`${id}-label`} className="text-sm font-medium text-ink">{label}</legend>
      <div role="radiogroup" aria-labelledby={`${id}-label`} className={cn('mt-2 grid gap-2', columns === 3 ? 'sm:grid-cols-3' : 'sm:grid-cols-2')}>
        {options.map((o, i) => {
          const checked = o.value === value;
          return (
            <button
              key={o.value}
              ref={(el) => { refs.current[i] = el; }}
              type="button"
              role="radio"
              aria-checked={checked}
              disabled={o.disabled}
              tabIndex={checked ? 0 : -1}
              onClick={() => onChange(o.value)}
              onKeyDown={(e) => onKey(e, value)}
              className={cn(
                'flex items-start gap-3 rounded-xl border p-3.5 text-left transition-colors disabled:cursor-not-allowed disabled:opacity-50',
                checked ? 'border-primary bg-primary-soft ring-1 ring-primary' : 'border-line-strong bg-card hover:bg-stone-50',
              )}
            >
              {o.icon && <span className={cn('mt-0.5 shrink-0', checked ? 'text-primary' : 'text-muted')}>{o.icon}</span>}
              <span className="min-w-0">
                <span className="block text-sm font-semibold">{o.title}</span>
                {o.description && <span className="mt-0.5 block text-xs text-muted">{o.description}</span>}
              </span>
            </button>
          );
        })}
      </div>
      {error && <p role="alert" className="mt-1.5 text-xs font-medium text-danger">{error}</p>}
    </fieldset>
  );
}
