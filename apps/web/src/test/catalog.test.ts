import { EXAMS } from '@prepmitra/shared';
import { filterExams } from '@/services/examService';

describe('filterExams', () => {
  it('returns all published exams sorted by popularity by default', () => {
    const r = filterExams(EXAMS, {});
    expect(r.length).toBe(EXAMS.filter((e) => e.status === 'published').length);
    for (let i = 1; i < r.length; i++) expect(r[i - 1]!.popularity).toBeGreaterThanOrEqual(r[i]!.popularity);
  });

  it('searches title, short title and description case-insensitively', () => {
    expect(filterExams(EXAMS, { search: 'gate' }).map((e) => e.id).sort()).toEqual(['gate-cse', 'gate-ece']);
    expect(filterExams(EXAMS, { search: 'IBPS' }).map((e) => e.id)).toEqual(expect.arrayContaining(['ibps-po', 'ibps-clerk']));
    expect(filterExams(EXAMS, { search: 'zzzz-no-match' })).toHaveLength(0);
  });

  it('filters by category, difficulty and language', () => {
    expect(filterExams(EXAMS, { category: 'banking' }).every((e) => e.category === 'banking')).toBe(true);
    expect(filterExams(EXAMS, { difficulty: 'Hard' }).every((e) => e.difficulty === 'Hard')).toBe(true);
    const tamil = filterExams(EXAMS, { language: 'ta' });
    expect(tamil.length).toBeGreaterThan(0);
    expect(tamil.every((e) => e.languages.includes('ta'))).toBe(true);
    expect(filterExams(EXAMS, { category: 'banking', difficulty: 'Easy' })).toHaveLength(0);
  });

  it('sorts by duration and title', () => {
    const asc = filterExams(EXAMS, { sort: 'duration-asc' });
    expect(asc[0]!.durationMin).toBeLessThanOrEqual(asc.at(-1)!.durationMin);
    const titles = filterExams(EXAMS, { sort: 'title' }).map((e) => e.shortTitle);
    expect(titles).toEqual([...titles].sort((a, b) => a.localeCompare(b)));
  });

  it('excludes hidden or draft exams', () => {
    const hidden = EXAMS.map((e, i) => (i === 0 ? { ...e, status: 'hidden' as const } : e));
    expect(filterExams(hidden, {}).find((e) => e.id === EXAMS[0]!.id)).toBeUndefined();
  });
});
