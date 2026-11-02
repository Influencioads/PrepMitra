import { useMemo } from 'react';
import { computeProgress } from '@prepmitra/shared';
import { selectHistory, useExamStore } from '@/store';

/** Derived analytics from the user's reports and practice log (numbers by code, same as web). */
export function useProgress() {
  const reports = useExamStore((s) => s.reports);
  const log = useExamStore((s) => s.practiceLog);
  return useMemo(() => {
    const list = Object.values(reports);
    const progress = computeProgress(list, log);
    const history = selectHistory(reports);
    const scores = list.map((r) => r.result.percentage);
    const avg = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0;
    const best = scores.length ? Math.max(...scores) : 0;
    const accuracies = list.map((r) => r.result.accuracy);
    const avgAccuracy = accuracies.length ? Math.round(accuracies.reduce((a, b) => a + b, 0) / accuracies.length) : 0;
    const t = progress.trend;
    const delta = t.length >= 2 ? t[t.length - 1]!.score - t[t.length - 2]!.score : 0;
    const strong = progress.topics.filter((x) => x.mastery >= 75 && x.attempts >= 2).sort((a, b) => b.mastery - a.mastery);
    const weak = progress.topics.filter((x) => x.mastery < 60 && x.attempts >= 2).sort((a, b) => a.mastery - b.mastery);
    return { ...progress, history, avg, best, avgAccuracy, delta, strong, weak, reports: list };
  }, [reports, log]);
}
