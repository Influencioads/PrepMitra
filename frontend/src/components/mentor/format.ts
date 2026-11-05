import { useT } from '@/i18n';
import { mentorMessages } from '@/i18n/messages/mentor';

export type MentorKey = keyof typeof mentorMessages.en;
export const useMentorT = () => useT(mentorMessages);

export const pct = (x: number | null | undefined) => (x === null || x === undefined ? '—' : `${Math.round(x * 100)}%`);
export const marks = (n: number) => (Number.isInteger(n) ? String(n) : n.toFixed(2));
export const mmss = (sec: number) => (sec >= 60 ? `${Math.floor(sec / 60)}m ${sec % 60}s` : `${sec}s`);
