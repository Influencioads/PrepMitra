import { useCallback, useEffect, useState } from 'react';
import { Linking, ScrollView, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import { classifyAiError, flowOrder, parseMermaid, type AiVisual, type Allowances, type MindMapNode } from '@prepmitra/shared';
import { AppText, Badge, Button, Notice } from '@/components';
import { aiService } from '@/services/aiService';
import { colors, radii, spacing } from '@/theme';

/** Shows `support` (a distress reply from the backend) above everything else on the screen. */
export function SupportBanner({ message }: { message?: string | null }) {
  if (!message) return null;
  return (
    <View style={styles.support} accessibilityRole="alert">
      <View style={styles.row}>
        <Ionicons name="heart-circle" size={26} color={colors.secondary} />
        <AppText variant="h3" color={colors.secondary}>You are not alone</AppText>
      </View>
      <AppText variant="body" style={styles.gap}>{message}</AppText>
      <Button title="Call Tele-MANAS 14416" variant="secondary" leftIcon="call" style={styles.gap} onPress={() => Linking.openURL('tel:14416')} />
    </View>
  );
}

/** 402 → upgrade prompt to the subscription screen, 422 off_topic, 503 "try again", anything else → message. */
export function AiErrorNotice({ error, onRetry }: { error: unknown; onRetry?: () => void }) {
  if (!error) return null;
  const info = classifyAiError(error);
  if (info.kind === 'upgrade') {
    return (
      <Notice tone="warning" title={info.title} style={styles.gap}
        action={<Button title="See plans" size="sm" onPress={() => router.push('/subscription')} />}>
        {info.message}
      </Notice>
    );
  }
  return (
    <Notice tone={info.kind === 'off_topic' ? 'info' : 'error'} title={info.title} style={styles.gap}
      action={info.retryable && onRetry ? <Button title="Try again" size="sm" variant="outline" leftIcon="refresh" onPress={onRetry} /> : undefined}>
      {info.message}
    </Notice>
  );
}

// ---------- visuals ----------
function MindMapTree({ node, depth = 0 }: { node: MindMapNode; depth?: number }) {
  return (
    <View style={depth > 0 ? styles.mmChild : undefined}>
      <View style={[styles.mmNode, depth === 0 ? styles.mmRoot : depth === 1 ? styles.mmL1 : null]}>
        <AppText variant="small" color={depth === 0 ? colors.white : colors.text} weight={depth < 2 ? '600' : '400'}>{node.label}</AppText>
      </View>
      {node.children.map((c, i) => <MindMapTree key={i} node={c} depth={depth + 1} />)}
    </View>
  );
}

/** Mermaid drawn natively from the shared reader (flowcharts and mind maps); other diagrams show their source. */
export function MermaidView({ source }: { source: string }) {
  const parsed = parseMermaid(source);
  if (parsed.kind === 'mindmap') return <View style={styles.visual}><MindMapTree node={parsed.root} /></View>;
  if (parsed.kind === 'flow') {
    const order = flowOrder(parsed);
    return (
      <View style={[styles.visual, { gap: spacing.xs }]} accessibilityLabel="Diagram">
        {order.map((n, i) => {
          const out = parsed.edges.filter((e) => e.from === n.id);
          return (
            <View key={n.id}>
              <View style={styles.flowNode}>
                <AppText variant="smallStrong">{n.label}</AppText>
                {out.map((e, j) => (
                  <AppText key={j} variant="caption">→ {e.label ? `${e.label}: ` : ''}{parsed.nodes.find((x) => x.id === e.to)?.label ?? e.to}</AppText>
                ))}
              </View>
              {i < order.length - 1 && <Ionicons name="arrow-down" size={14} color={colors.textMuted} style={styles.center} />}
            </View>
          );
        })}
      </View>
    );
  }
  return <View style={styles.visual}><AppText variant="caption">{parsed.source}</AppText></View>;
}

export function TableView({ rows }: { rows: string[][] }) {
  if (!rows.length) return null;
  return (
    <ScrollView horizontal style={styles.visual} contentContainerStyle={{ flexDirection: 'column' }}>
      {rows.map((r, i) => (
        <View key={i} style={[styles.tr, i === 0 && styles.th]}>
          {r.map((c, j) => (
            <AppText key={j} variant={i === 0 ? 'smallStrong' : 'small'} style={styles.td}>{c}</AppText>
          ))}
        </View>
      ))}
    </ScrollView>
  );
}

export function VisualView({ visual }: { visual?: AiVisual | null }) {
  if (!visual || visual.type === 'none') return null;
  if (visual.type === 'mermaid' && visual.mermaid?.trim()) return <MermaidView source={visual.mermaid} />;
  if (visual.type === 'table' && visual.table?.length) return <TableView rows={visual.table} />;
  return null;
}

// ---------- allowances ----------
let cache: { at: number; data: Allowances } | null = null;
const listeners = new Set<(a: Allowances) => void>();

export async function refreshAllowances(): Promise<Allowances | null> {
  try {
    const data = await aiService.allowances();
    cache = { at: Date.now(), data };
    listeners.forEach((l) => l(data));
    return data;
  } catch {
    return null;
  }
}

export function useAllowances() {
  const [data, setData] = useState<Allowances | null>(cache?.data ?? null);
  useEffect(() => {
    listeners.add(setData);
    if (!cache || Date.now() - cache.at > 60_000) void refreshAllowances();
    return () => { listeners.delete(setData); };
  }, []);
  return data;
}

export function AllowanceBadge({ feature, label }: { feature: string; label?: string }) {
  const data = useAllowances();
  if (!data) return null;
  const l = data.limits.find((x) => x.feature === feature);
  const prefix = label ? `${label}: ` : '';
  if (!l || l.limit <= 0) return <Badge label={`${prefix}not in your plan`} icon="lock-closed-outline" />;
  const tone = l.remaining === 0 ? 'error' : l.remaining <= Math.max(1, l.limit * 0.2) ? 'warning' : 'success';
  return <Badge label={`${prefix}${l.remaining} of ${l.limit} left`} tone={tone} />;
}

export function useAiAction<A extends unknown[], R>(fn: (...args: A) => Promise<R>) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const run = useCallback(async (...args: A): Promise<R | undefined> => {
    setBusy(true);
    setError(null);
    try {
      return await fn(...args);
    } catch (e) {
      setError(e);
      return undefined;
    } finally {
      setBusy(false);
      void refreshAllowances();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return { run, busy, error, setError };
}

export function useAiQuery<T>(loader: () => Promise<T>, key: string) {
  const [data, setData] = useState<T>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown>(null);
  const [tick, setTick] = useState(0);
  useEffect(() => {
    let alive = true;
    setLoading(true);
    setError(null);
    loader().then((d) => { if (alive) setData(d); }).catch((e) => { if (alive) setError(e); }).finally(() => { if (alive) setLoading(false); });
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, tick]);
  return { data, setData, loading, error, reload: () => setTick((t) => t + 1) };
}

const styles = StyleSheet.create({
  support: { borderWidth: 2, borderColor: colors.secondary, backgroundColor: colors.secondarySoft, borderRadius: radii.lg, padding: spacing.lg, marginBottom: spacing.md },
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  gap: { marginTop: spacing.sm },
  visual: { borderWidth: 1, borderColor: colors.border, borderRadius: radii.md, backgroundColor: colors.white, padding: spacing.md, marginTop: spacing.sm },
  mmChild: { marginLeft: spacing.md, paddingLeft: spacing.sm, borderLeftWidth: 1, borderLeftColor: colors.borderStrong, marginTop: spacing.xs },
  mmNode: { alignSelf: 'flex-start', paddingHorizontal: spacing.sm, paddingVertical: 4, borderRadius: radii.sm, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card },
  mmRoot: { backgroundColor: colors.primary, borderColor: colors.primary },
  mmL1: { backgroundColor: colors.primarySoft, borderColor: colors.primarySoft },
  flowNode: { borderWidth: 1, borderColor: colors.border, borderRadius: radii.sm, padding: spacing.sm, backgroundColor: colors.card },
  center: { alignSelf: 'center', marginVertical: 2 },
  tr: { flexDirection: 'row', borderTopWidth: 1, borderTopColor: colors.border },
  th: { backgroundColor: colors.background, borderTopWidth: 0 },
  td: { width: 140, padding: spacing.xs },
});
