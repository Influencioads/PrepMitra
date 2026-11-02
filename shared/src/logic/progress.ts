import type { ExamReport, ProgressData, TopicMastery, TrendPoint, WeeklyPractice } from '../types/core';
import type { PracticeLog } from '../mocks/user';
import { dayKey } from '../mocks/user';
import { getExamById } from '../mocks/exams';

const DAY = 86_400_000;
const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export function buildTrend(reports: ExamReport[]): TrendPoint[] {
  return [...reports]
    .sort((a, b) => a.createdAt.localeCompare(b.createdAt))
    .map((r) => {
      const d = new Date(r.createdAt);
      return {
        date: r.createdAt,
        label: `${d.getDate()}/${d.getMonth() + 1}`,
        score: r.result.percentage,
        accuracy: r.result.accuracy,
        examId: r.examId,
        category: getExamById(r.examId)?.category ?? 'government',
      };
    });
}

/** Aggregates topic accuracy across all reports into a mastery score (0–100). */
export function buildTopicMastery(reports: ExamReport[]): TopicMastery[] {
  const sorted = [...reports].sort((a, b) => a.createdAt.localeCompare(b.createdAt));
  const map = new Map<string, { subject: TopicMastery['subject']; correct: number; total: number; history: number[] }>();
  for (const r of sorted) {
    for (const t of r.result.topics) {
      const e = map.get(t.topic) ?? { subject: t.subject, correct: 0, total: 0, history: [] };
      e.correct += t.correct;
      e.total += t.total;
      e.history.push(t.accuracy);
      map.set(t.topic, e);
    }
  }
  return [...map.entries()]
    .map(([topic, e]) => {
      const last = e.history[e.history.length - 1] ?? 0;
      const prev = e.history.length > 1 ? e.history[e.history.length - 2]! : last;
      return { topic, subject: e.subject, mastery: e.total ? Math.round((e.correct / e.total) * 100) : 0, attempts: e.total, trend: last - prev };
    })
    .sort((a, b) => b.attempts - a.attempts || b.mastery - a.mastery);
}

export function buildWeekly(log: PracticeLog, now: number = Date.now()): WeeklyPractice[] {
  return Array.from({ length: 7 }, (_, i) => {
    const ms = now - (6 - i) * DAY;
    return { day: WEEKDAYS[new Date(ms).getDay()]!, minutes: log[dayKey(ms)] ?? 0 };
  });
}

/** Consecutive days with practice, counting back from today (or yesterday if today has none yet). */
export function computeStreak(log: PracticeLog, now: number = Date.now()): number {
  let streak = 0;
  let cursor = now;
  if (!log[dayKey(cursor)]) cursor -= DAY;
  while (log[dayKey(cursor)]) {
    streak += 1;
    cursor -= DAY;
  }
  return streak;
}

export function computeProgress(reports: ExamReport[], log: PracticeLog, now: number = Date.now()): ProgressData {
  const weekly = buildWeekly(log, now);
  return {
    trend: buildTrend(reports),
    topics: buildTopicMastery(reports),
    weekly,
    streakDays: computeStreak(log, now),
    totalMinutes: weekly.reduce((s, d) => s + d.minutes, 0),
  };
}

export function addPractice(log: PracticeLog, minutes: number, now: number = Date.now()): PracticeLog {
  const k = dayKey(now);
  return { ...log, [k]: (log[k] ?? 0) + Math.max(1, Math.round(minutes)) };
}
