import {
  Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart, PolarAngleAxis, PolarGrid, PolarRadiusAxis,
  Radar, RadarChart, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts';
import { chartColors, colors } from '@prepmitra/shared';
import { useT } from '@/i18n';
import { useContentT } from '@/i18n/content';
import { commonMessages } from '@/i18n/messages/common';

const axis = { stroke: colors.textMuted, fontSize: 12, tickLine: false, axisLine: false } as const;
const tooltipStyle = { borderRadius: 10, border: `1px solid ${colors.border}`, fontSize: 13, boxShadow: '0 4px 12px rgba(15,23,42,.08)' };

export interface TrendDatum {
  label: string;
  score: number;
  accuracy?: number;
}

/** Score (and optional accuracy) over time. */
export function ScoreChart({ data, height = 260, showAccuracy = true }: { data: TrendDatum[]; height?: number; showAccuracy?: boolean }) {
  const t = useT(commonMessages);
  return (
    <div style={{ height }} role="img" aria-label={t('chartScoreTrend', { count: data.length })}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
          <defs>
            <linearGradient id="scoreFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={colors.primary} stopOpacity={0.25} />
              <stop offset="100%" stopColor={colors.primary} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke={colors.border} strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="label" {...axis} />
          <YAxis domain={[0, 100]} {...axis} unit="%" />
          <Tooltip contentStyle={tooltipStyle} formatter={(v) => `${v}%`} />
          <Area type="monotone" dataKey="score" name={t('chartScore')} stroke={colors.primary} strokeWidth={2.5} fill="url(#scoreFill)" dot={{ r: 3 }} />
          {showAccuracy && (
            <Area type="monotone" dataKey="accuracy" name={t('chartAccuracy')} stroke={chartColors[1]} strokeWidth={2} fill="none" strokeDasharray="5 4" dot={false} />
          )}
          {showAccuracy && <Legend iconType="plainline" wrapperStyle={{ fontSize: 12 }} />}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

const barColor = (v: number) => (v >= 75 ? colors.success : v >= 50 ? colors.warning : colors.error);

/** Horizontal accuracy bars coloured by performance band. */
export function TopicAccuracyChart({ data, height }: { data: { topic: string; accuracy: number }[]; height?: number }) {
  const t = useT(commonMessages);
  const ct = useContentT();
  const rows = data.map((d) => ({ ...d, topic: ct(d.topic) }));
  const h = height ?? Math.max(180, data.length * 38);
  return (
    <div style={{ height: h }} role="img" aria-label={t('chartTopicAccuracy')}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={rows} layout="vertical" margin={{ top: 0, right: 24, left: 8, bottom: 0 }}>
          <CartesianGrid stroke={colors.border} strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" domain={[0, 100]} {...axis} unit="%" />
          <YAxis type="category" dataKey="topic" width={130} {...axis} tick={{ fill: colors.text, fontSize: 12 }} />
          <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`${v}%`, t('chartAccuracy')]} cursor={{ fill: colors.background }} />
          <Bar dataKey="accuracy" radius={[0, 6, 6, 0]} barSize={18}>
            {rows.map((d) => <Cell key={d.topic} fill={barColor(d.accuracy)} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

/** Grouped section bars: correct / incorrect / unanswered. */
export function SectionChart({ data, height = 260 }: { data: { name: string; correct: number; incorrect: number; unanswered: number }[]; height?: number }) {
  const t = useT(commonMessages);
  return (
    <div style={{ height }} role="img" aria-label={t('chartSection')}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
          <CartesianGrid stroke={colors.border} strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" {...axis} interval={0} tick={{ fontSize: 11, fill: colors.textSecondary }} />
          <YAxis allowDecimals={false} {...axis} />
          <Tooltip contentStyle={tooltipStyle} cursor={{ fill: colors.background }} />
          <Legend wrapperStyle={{ fontSize: 12 }} />
          <Bar dataKey="correct" name={t('chartCorrect')} stackId="a" fill={colors.success} />
          <Bar dataKey="incorrect" name={t('chartIncorrect')} stackId="a" fill={colors.error} />
          <Bar dataKey="unanswered" name={t('chartUnanswered')} stackId="a" fill={colors.borderStrong} radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function WeeklyBarChart({ data, height = 220 }: { data: { day: string; minutes: number }[]; height?: number }) {
  const t = useT(commonMessages);
  return (
    <div style={{ height }} role="img" aria-label={t('chartWeekly')}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
          <CartesianGrid stroke={colors.border} strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="day" {...axis} />
          <YAxis {...axis} unit="m" />
          <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`${v} min`, t('chartPractice')]} cursor={{ fill: colors.background }} />
          <Bar dataKey="minutes" fill={colors.primary} radius={[6, 6, 0, 0]} barSize={26} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function SkillRadar({ data, height = 280 }: { data: { skill: string; value: number }[]; height?: number }) {
  return (
    <div style={{ height }} role="img" aria-label="Skill scores out of 10">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} outerRadius="72%">
          <PolarGrid stroke={colors.border} />
          <PolarAngleAxis dataKey="skill" tick={{ fontSize: 11, fill: colors.textSecondary }} />
          <PolarRadiusAxis domain={[0, 10]} tick={false} axisLine={false} />
          <Radar dataKey="value" stroke={colors.secondary} fill={colors.secondary} fillOpacity={0.25} strokeWidth={2} />
          <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`${v}/10`, 'Score']} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function MiniLine({ data, height = 48 }: { data: { v: number }[]; height?: number }) {
  return (
    <div style={{ height }} aria-hidden>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <Line type="monotone" dataKey="v" stroke={colors.primary} strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
