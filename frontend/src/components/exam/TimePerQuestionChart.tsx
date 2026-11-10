import { Bar, CartesianGrid, Cell, Legend, ResponsiveContainer, Scatter, ComposedChart, Tooltip, XAxis, YAxis } from 'recharts';
import type { QuestionOutcome } from '@prepmitra/shared';
import { colors } from '@prepmitra/shared';
import { useT } from '@/i18n';
import { reportMessages } from '@/i18n/messages/report';


export interface TimeDatum {
  q: string;
  spent: number;
  expected: number;
  outcome: QuestionOutcome;
  sectionId?: string;
}

const fill: Record<QuestionOutcome, string> = { correct: colors.success, incorrect: colors.error, unanswered: colors.borderStrong };
const axis = { stroke: colors.textMuted, fontSize: 11, tickLine: false, axisLine: false } as const;

/** Seconds spent per question vs the expected time (plan Day 6), coloured by outcome. */
export function TimePerQuestionChart({ data, height = 260 }: { data: TimeDatum[]; height?: number }) {
  const t = useT(reportMessages);
  return (
    <div style={{ height }} role="img" aria-label={t('timeChartAria')}>
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
          <CartesianGrid stroke={colors.border} strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="q" {...axis} interval={Math.max(0, Math.ceil(data.length / 20) - 1)} />
          <YAxis {...axis} unit="s" />
          <Tooltip
            contentStyle={{ borderRadius: 10, border: `1px solid ${colors.border}`, fontSize: 13 }}
            formatter={(v, name) => [`${v}s`, name === 'spent' ? t('timeSpent') : t('expected')]}
            cursor={{ fill: colors.background }}
          />
          <Legend wrapperStyle={{ fontSize: 12 }} formatter={(v) => (v === 'spent' ? t('timeSpent') : t('expectedTime'))} />
          <Bar dataKey="spent" radius={[4, 4, 0, 0]} maxBarSize={22}>
            {data.map((d) => <Cell key={d.q} fill={fill[d.outcome]} />)}
          </Bar>
          <Scatter dataKey="expected" fill={colors.text} shape="diamond" />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}


