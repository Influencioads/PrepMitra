import { describe, expect, it } from 'vitest';
import { defineMessages, format, translate, useI18nStore } from './index';

const m = defineMessages({ en: { hi: 'Hello {{name}}' }, hi: { hi: 'नमस्ते {{name}}' } });

describe('i18n', () => {
  it('interpolates variables', () => {
    expect(format('{{a}} of {{b}}', { a: 1, b: 2 })).toBe('1 of 2');
  });
  it('translates by current language', () => {
    useI18nStore.getState().setLang('en');
    expect(translate(m, 'hi', { name: 'Ananya' })).toBe('Hello Ananya');
    useI18nStore.getState().setLang('hi');
    expect(translate(m, 'hi', { name: 'Ananya' })).toBe('नमस्ते Ananya');
    useI18nStore.getState().setLang('en');
  });
});
