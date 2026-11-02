import {
  Area, AreaChart, Bar, BarChart, CartesianGrid, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts';
import { colors } from '@prepmitra/shared';

const axis = { stroke: colors.textMuted, fontSize: 12, tickLine: false, axisLine: false } as const;
const tooltipStyle = { borderRadius: 10, border: `1px solid ${colors.border}`, fontSize: 13, boxShadow: '0 4px 12px rgba(15,23,42,.08)' };

export interface ChartDatum {
  label: string;
  value: number;
}

interface BaseProps {
  data: ChartDatum[];
  /** Series name shown in the tooltip. */
  name: string;
  format?: (v: number) => string;
  height?: number;
  /** Optional dashed target line (single axis — never a second scale). */
  target?: { value: number; label: string };
  ariaLabel: string;
}

const id = (v: number) => String(v);

/** Single-series trend (area). */
export function TrendChart({ data, name, format = id, height = 240, target, ariaLabel }: BaseProps) {
  const gradId = `fill-${name.replace(/\W+/g, '')}`;
  return (
    <div style={{ height }} role="img" aria-label={ariaLabel}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 12, right: 12, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id={gradId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={colors.primary} stopOpacity={0.22} />
              <stop offset="100%" stopColor={colors.primary} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke={colors.border} strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="label" {...axis} />
          <YAxis {...axis} width={56} tickFormatter={(v: number) => format(v)} />
          <Tooltip contentStyle={tooltipStyle} formatter={(v) => [format(Number(v)), name]} />
          {target && (
            <ReferenceLine
              y={target.value}
              stroke={colors.textSecondary}
              strokeDasharray="5 4"
              label={{ value: target.label, position: 'insideTopRight', fill: colors.textSecondary, fontSize: 11 }}
            />
          )}
          <Area type="monotone" dataKey="value" name={name} stroke={colors.primary} strokeWidth={2} fill={`url(#${gradId})`} dot={{ r: 3 }} activeDot={{ r: 5 }} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

/** Single-series vertical bars. */
export function ColumnChart({ data, name, format = id, height = 240, target, ariaLabel }: BaseProps) {
  return (
    <div style={{ height }} role="img" aria-label={ariaLabel}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 12, right: 12, left: 0, bottom: 0 }}>
          <CartesianGrid stroke={colors.border} strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="label" {...axis} interval={0} tick={{ fontSize: 11, fill: colors.textSecondary }} />
          <YAxis {...axis} width={56} tickFormatter={(v: number) => format(v)} />
          <Tooltip contentStyle={tooltipStyle} formatter={(v) => [format(Number(v)), name]} cursor={{ fill: colors.background }} />
          {target && (
            <ReferenceLine y={target.value} stroke={colors.textSecondary} strokeDasharray="5 4" label={{ value: target.label, position: 'insideTopRight', fill: colors.textSecondary, fontSize: 11 }} />
          )}
          <Bar dataKey="value" name={name} fill={colors.primary} radius={[4, 4, 0, 0]} maxBarSize={36} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

/** Single-series horizontal bars — best for long category labels. */
export function BarListChart({ data, name, format = id, height, target, ariaLabel }: BaseProps) {
  const h = height ?? Math.max(160, data.length * 34 + 24);
  return (
    <div style={{ height: h }} role="img" aria-label={ariaLabel}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ top: target ? 20 : 4, right: 24, left: 4, bottom: 0 }}>
          <CartesianGrid stroke={colors.border} strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" {...axis} tickFormatter={(v: number) => format(v)} />
          <YAxis type="category" dataKey="label" width={110} {...axis} tick={{ fill: colors.text, fontSize: 12 }} />
          <Tooltip contentStyle={tooltipStyle} formatter={(v) => [format(Number(v)), name]} cursor={{ fill: colors.background }} />
          {target && (
            <ReferenceLine x={target.value} stroke={colors.textSecondary} strokeDasharray="5 4" label={{ value: target.label, position: 'top', fill: colors.textSecondary, fontSize: 11 }} />
          )}
          <Bar dataKey="value" name={name} fill={colors.primary} radius={[0, 4, 4, 0]} barSize={16} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
