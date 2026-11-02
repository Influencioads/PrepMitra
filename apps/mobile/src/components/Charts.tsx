import { useState } from 'react';
import { StyleSheet, View, type LayoutChangeEvent } from 'react-native';
import Svg, { Circle, G, Line, Path, Rect, Text as SvgText } from 'react-native-svg';
import type { TrendPoint } from '@prepmitra/shared';
import { chartColors, colors, spacing } from '@/theme';
import { AppText } from './AppText';

/** Measures the available width so charts scale to any phone. */
function useWidth(initial = 300) {
  const [width, setWidth] = useState(initial);
  const onLayout = (e: LayoutChangeEvent) => {
    const w = Math.round(e.nativeEvent.layout.width);
    if (w > 0 && w !== width) setWidth(w);
  };
  return { width, onLayout };
}

export interface LineSeries {
  name: string;
  values: number[];
  color?: string;
}

export interface LineChartProps {
  labels: string[];
  series: LineSeries[];
  height?: number;
  max?: number;
  unit?: string;
  accessibilityLabel: string;
}

const PAD = { top: 12, right: 12, bottom: 26, left: 34 };

/** Multi-series line chart (0–max), e.g. score % and accuracy % over attempts. */
export function LineChart({ labels, series, height = 190, max = 100, unit = '%', accessibilityLabel }: LineChartProps) {
  const { width, onLayout } = useWidth();
  const plotW = Math.max(10, width - PAD.left - PAD.right);
  const plotH = height - PAD.top - PAD.bottom;
  const n = labels.length;
  const x = (i: number) => PAD.left + (n <= 1 ? plotW / 2 : (i / (n - 1)) * plotW);
  const y = (v: number) => PAD.top + plotH - (Math.max(0, Math.min(max, v)) / max) * plotH;
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((t) => Math.round(t * max));
  const labelEvery = Math.max(1, Math.ceil(n / Math.max(1, Math.floor(plotW / 44))));

  return (
    <View onLayout={onLayout} accessible accessibilityRole="image" accessibilityLabel={accessibilityLabel}>
      <Svg width={width} height={height}>
        {ticks.map((t) => (
          <G key={t}>
            <Line x1={PAD.left} x2={width - PAD.right} y1={y(t)} y2={y(t)} stroke={colors.border} strokeDasharray={t === 0 ? undefined : '3 4'} />
            <SvgText x={PAD.left - 6} y={y(t) + 4} fontSize={10} fill={colors.textMuted} textAnchor="end">
              {`${t}${unit}`}
            </SvgText>
          </G>
        ))}
        {series.map((s, si) => {
          const color = s.color ?? chartColors[si % chartColors.length];
          const d = s.values.map((v, i) => `${i === 0 ? 'M' : 'L'}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
          return (
            <G key={s.name}>
              {n > 1 && <Path d={d} stroke={color} strokeWidth={2.5} fill="none" strokeLinejoin="round" strokeLinecap="round" />}
              {s.values.map((v, i) => (
                <Circle key={i} cx={x(i)} cy={y(v)} r={3.5} fill={colors.white} stroke={color} strokeWidth={2} />
              ))}
            </G>
          );
        })}
        {labels.map((l, i) =>
          i % labelEvery === 0 || i === n - 1 ? (
            <SvgText key={`${l}-${i}`} x={x(i)} y={height - 8} fontSize={10} fill={colors.textSecondary} textAnchor="middle">
              {l}
            </SvgText>
          ) : null,
        )}
      </Svg>
      {series.length > 1 && <Legend items={series.map((s, i) => ({ label: s.name, color: s.color ?? chartColors[i % chartColors.length]! }))} />}
    </View>
  );
}

export interface BarChartProps {
  labels: string[];
  values: number[];
  height?: number;
  color?: string;
  unit?: string;
  accessibilityLabel: string;
  highlightLast?: boolean;
}

/** Vertical bar chart, e.g. minutes practised per day. */
export function BarChart({ labels, values, height = 170, color = chartColors[0], unit = '', accessibilityLabel, highlightLast }: BarChartProps) {
  const { width, onLayout } = useWidth();
  const top = 18;
  const bottom = 24;
  const plotH = height - top - bottom;
  const max = Math.max(1, ...values);
  const slot = width / Math.max(1, values.length);
  const barW = Math.min(32, slot * 0.6);
  return (
    <View onLayout={onLayout} accessible accessibilityRole="image" accessibilityLabel={accessibilityLabel}>
      <Svg width={width} height={height}>
        <Line x1={0} x2={width} y1={top + plotH} y2={top + plotH} stroke={colors.border} />
        {values.map((v, i) => {
          const h = (v / max) * plotH;
          const cx = slot * i + slot / 2;
          const fill = highlightLast && i === values.length - 1 ? colors.secondary : color;
          return (
            <G key={i}>
              <Rect x={cx - barW / 2} y={top + plotH - h} width={barW} height={Math.max(h, v > 0 ? 2 : 0)} rx={5} fill={fill} opacity={v > 0 ? 1 : 0.3} />
              {v > 0 && (
                <SvgText x={cx} y={top + plotH - h - 5} fontSize={10} fill={colors.textSecondary} textAnchor="middle">
                  {`${v}${unit}`}
                </SvgText>
              )}
              <SvgText x={cx} y={height - 7} fontSize={11} fill={colors.textSecondary} textAnchor="middle">
                {labels[i]}
              </SvgText>
            </G>
          );
        })}
      </Svg>
    </View>
  );
}

export function Legend({ items }: { items: { label: string; color: string }[] }) {
  return (
    <View style={styles.legend}>
      {items.map((it) => (
        <View key={it.label} style={styles.legendItem}>
          <View style={[styles.dot, { backgroundColor: it.color }]} />
          <AppText variant="caption">{it.label}</AppText>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  legend: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md, marginTop: spacing.sm },
  legendItem: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  dot: { width: 10, height: 10, borderRadius: 5 },
});

/** Score % and accuracy % across attempts (mirrors the web ScoreChart). */
export function ScoreChart({ data, showAccuracy = true }: { data: TrendPoint[]; showAccuracy?: boolean }) {
  const last = data[data.length - 1];
  return (
    <LineChart
      labels={data.map((t) => t.label)}
      series={[
        { name: 'Score %', values: data.map((t) => t.score), color: chartColors[0] },
        ...(showAccuracy ? [{ name: 'Accuracy %', values: data.map((t) => t.accuracy), color: chartColors[2] }] : []),
      ]}
      accessibilityLabel={
        last
          ? `Score trend over ${data.length} mocks. Latest score ${last.score} percent, accuracy ${last.accuracy} percent.`
          : 'No scores yet'
      }
    />
  );
}
