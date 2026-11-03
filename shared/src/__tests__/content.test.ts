import { describe, expect, it } from 'vitest';
import { QUESTION_BANK } from '../mocks/questions';
import { INTERVIEW_ROLES, INTERVIEW_SCRIPTS } from '../mocks/interviews';
import { localizeQuestion } from '../logic/paper';

const BILINGUAL = ['quant', 'reasoning', 'general-awareness', 'general-studies', 'data-interpretation', 'computer-science'];

describe('Hindi question content', () => {
  it('every bilingual-subject question has a Hindi version with matching options', () => {
    for (const q of QUESTION_BANK.filter((x) => BILINGUAL.includes(x.subject))) {
      const hi = q.translations?.hi;
      expect(hi, q.id).toBeDefined();
      expect(hi!.text.length, q.id).toBeGreaterThan(5);
      if (q.options) expect(hi!.options?.length, q.id).toBe(q.options.length);
    }
  });

  it('English-language questions stay English-only', () => {
    for (const q of QUESTION_BANK.filter((x) => x.subject === 'english')) expect(q.translations?.hi, q.id).toBeUndefined();
  });

  it('localizing keeps option ids, so answers survive a language toggle', () => {
    const q = QUESTION_BANK.find((x) => x.id === 'q-reas-3')!;
    const hi = localizeQuestion(q, 'hi');
    expect(hi.options!.map((o) => o.id)).toEqual(q.options!.map((o) => o.id));
    expect(hi.options![1]!.text).toBe('भाई');
  });
});

describe('interview scripts', () => {
  it('each role has 8–12 questions and questionCount matches the script', () => {
    for (const role of INTERVIEW_ROLES) {
      const script = INTERVIEW_SCRIPTS[role.id]!;
      expect(script.length, role.id).toBeGreaterThanOrEqual(8);
      expect(script.length, role.id).toBeLessThanOrEqual(12);
      expect(role.questionCount, role.id).toBe(script.length);
      expect(new Set(script.map((q) => q.id)).size, role.id).toBe(script.length);
    }
  });
});
