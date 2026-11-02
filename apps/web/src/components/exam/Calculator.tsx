import { useState } from 'react';
import { Modal } from '@/components/ui';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { examMessages } from '@/i18n/messages/exam';


/** Safe arithmetic evaluator (no eval): supports + − × ÷, parentheses, decimals and unary minus. */
export function evaluateExpression(expr: string): number {
  const tokens = expr.replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-').match(/\d*\.?\d+|[()+\-*/]/g) ?? [];
  let pos = 0;
  const peek = () => tokens[pos];
  const next = () => tokens[pos++];
  const parseExpr = (): number => {
    let v = parseTerm();
    while (peek() === '+' || peek() === '-') v = next() === '+' ? v + parseTerm() : v - parseTerm();
    return v;
  };
  const parseTerm = (): number => {
    let v = parseFactor();
    while (peek() === '*' || peek() === '/') {
      const op = next();
      const r = parseFactor();
      v = op === '*' ? v * r : v / r;
    }
    return v;
  };
  const parseFactor = (): number => {
    const t = next();
    if (t === '-') return -parseFactor();
    if (t === '(') {
      const v = parseExpr();
      if (next() !== ')') throw new Error('Mismatched parentheses');
      return v;
    }
    const n = Number(t);
    if (t === undefined || Number.isNaN(n)) throw new Error('Invalid expression');
    return n;
  };
  const result = parseExpr();
  if (pos !== tokens.length || !Number.isFinite(result)) throw new Error('Invalid expression');
  return Math.round(result * 1e8) / 1e8;
}

const KEYS = ['C', '(', ')', '÷', '7', '8', '9', '×', '4', '5', '6', '−', '1', '2', '3', '+', '0', '.', '⌫', '='];

export function Calculator({ open, onOpenChange }: { open: boolean; onOpenChange: (o: boolean) => void }) {
  const t = useT(examMessages);
  const [expr, setExpr] = useState('');
  const [result, setResult] = useState<string>('');

  const press = (k: string) => {
    if (k === 'C') {
      setExpr('');
      setResult('');
    } else if (k === '⌫') setExpr((e) => e.slice(0, -1));
    else if (k === '=') {
      try {
        const v = evaluateExpression(expr);
        setResult(String(v));
        setExpr(String(v));
      } catch {
        setResult(t('calcError'));
      }
    } else setExpr((e) => (e + k).slice(0, 40));
  };

  return (
    <Modal open={open} onOpenChange={onOpenChange} title={t('calculator')} description={t('calculatorDesc')} size="sm" sheetOnMobile>
      <div className="rounded-lg bg-ink p-3 text-right font-mono text-white">
        <div className="min-h-6 break-all text-lg" aria-live="polite">{expr || '0'}</div>
        <div className="min-h-5 text-sm text-stone-400">{result && result !== expr ? `= ${result}` : ''}</div>
      </div>
      <div className="mt-3 grid grid-cols-4 gap-2">
        {KEYS.map((k) => (
          <button
            key={k}
            type="button"
            onClick={() => press(k)}
            aria-label={k === '⌫' ? t('calcBackspace') : k === 'C' ? t('calcClear') : k}
            className={cn(
              'h-12 rounded-lg text-lg font-semibold transition-colors',
              k === '=' ? 'bg-primary text-white hover:bg-primary-hover' : ['÷', '×', '−', '+'].includes(k) ? 'bg-primary-soft text-primary hover:bg-[#f9dcc6]' : 'bg-stone-100 hover:bg-stone-200',
            )}
          >
            {k}
          </button>
        ))}
      </div>
    </Modal>
  );
}
