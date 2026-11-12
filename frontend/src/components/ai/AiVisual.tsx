import { useEffect, useId, useState } from 'react';
import { cleanMermaid, flowOrder, parseMermaid, type AiVisual as Visual, type MindMapNode } from '@prepmitra/shared';
import { cn } from '@/utils/cn';

/**
 * AI visuals arrive as `{ type: 'mermaid' | 'table' | 'none', mermaid, table }`. Mermaid is drawn with the real
 * library, loaded on demand from a CDN (so it costs nothing until a diagram is shown); offline, in tests or when
 * the diagram does not parse, the shared reader draws a simple native version instead.
 */

type MermaidApi = { initialize: (c: object) => void; render: (id: string, src: string) => Promise<{ svg: string }> };
let mermaidLoad: Promise<MermaidApi | null> | null = null;
const MERMAID_URL = 'https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs';

function loadMermaid(): Promise<MermaidApi | null> {
  if (import.meta.env.MODE === 'test' || typeof window === 'undefined') return Promise.resolve(null);
  mermaidLoad ??= import(/* @vite-ignore */ MERMAID_URL)
    .then((m: { default: MermaidApi }) => {
      // strict: labels are text only, never HTML or click handlers from the AI.
      m.default.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'neutral', fontFamily: 'inherit' });
      return m.default;
    })
    .catch(() => null);
  return mermaidLoad;
}

function MindMapTree({ node, depth = 0 }: { node: MindMapNode; depth?: number }) {
  return (
    <li className={cn(depth > 0 && 'mt-1.5')}>
      <span className={cn('inline-block rounded-md px-2 py-1 text-sm', depth === 0 ? 'bg-primary font-semibold text-white' : depth === 1 ? 'bg-primary-soft font-medium text-ink' : 'border border-line bg-card text-ink')}>
        {node.label}
      </span>
      {node.children.length > 0 && (
        <ul className="ml-4 border-l border-line-strong pl-3">
          {node.children.map((c, i) => <MindMapTree key={i} node={c} depth={depth + 1} />)}
        </ul>
      )}
    </li>
  );
}

/** Native drawing of a parsed diagram (also the fallback when the Mermaid library cannot load). */
export function MermaidFallback({ source }: { source: string }) {
  const parsed = parseMermaid(source);
  if (parsed.kind === 'mindmap') return <ul aria-label="Mind map" className="space-y-1"><MindMapTree node={parsed.root} /></ul>;
  if (parsed.kind === 'flow') {
    const order = flowOrder(parsed);
    return (
      <ol aria-label="Diagram" className="space-y-2">
        {order.map((n) => {
          const out = parsed.edges.filter((e) => e.from === n.id);
          return (
            <li key={n.id} className="rounded-lg border border-line bg-card px-3 py-2 text-sm">
              <p className="font-medium text-ink">{n.label}</p>
              {out.length > 0 && (
                <ul className="mt-1 space-y-0.5 text-xs text-muted">
                  {out.map((e, i) => (
                    <li key={i}>→ {e.label ? <em>{e.label}: </em> : null}{parsed.nodes.find((x) => x.id === e.to)?.label ?? e.to}</li>
                  ))}
                </ul>
              )}
            </li>
          );
        })}
      </ol>
    );
  }
  return <pre className="overflow-x-auto whitespace-pre-wrap rounded-lg bg-surface p-3 text-xs text-muted">{parsed.source}</pre>;
}

export function MermaidDiagram({ source, className }: { source: string; className?: string }) {
  const id = `mmd-${useId().replace(/[^a-zA-Z0-9]/g, '')}`;
  const [svg, setSvg] = useState<string | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    let alive = true;
    setSvg(null);
    setFailed(false);
    loadMermaid().then(async (m) => {
      if (!m) return alive && setFailed(true);
      try {
        const out = await m.render(id, cleanMermaid(source));
        if (alive) setSvg(out.svg);
      } catch {
        if (alive) setFailed(true);
      }
    });
    return () => { alive = false; };
  }, [id, source]);
  return (
    <div className={cn('overflow-x-auto rounded-lg border border-line bg-white p-3', className)}>
      {svg && !failed ? (
        // Rendered by Mermaid with securityLevel "strict" (sanitised SVG, no scripts or links).
        <div className="[&_svg]:mx-auto [&_svg]:max-w-full" dangerouslySetInnerHTML={{ __html: svg }} />
      ) : failed ? <MermaidFallback source={source} /> : <p className="text-sm text-muted">Drawing the diagram…</p>}
    </div>
  );
}

export function AiTable({ rows, className }: { rows: string[][]; className?: string }) {
  if (!rows.length) return null;
  const [head, ...body] = rows;
  return (
    <div className={cn('overflow-x-auto rounded-lg border border-line', className)}>
      <table className="w-full text-left text-sm">
        <thead className="bg-surface">
          <tr>{head!.map((c, i) => <th key={i} scope="col" className="px-3 py-2 font-semibold">{c}</th>)}</tr>
        </thead>
        <tbody>
          {body.map((r, i) => (
            <tr key={i} className="border-t border-line">{r.map((c, j) => <td key={j} className="px-3 py-2 align-top">{c}</td>)}</tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function AiVisualView({ visual, className }: { visual?: Visual | null; className?: string }) {
  if (!visual || visual.type === 'none') return null;
  if (visual.type === 'mermaid' && visual.mermaid?.trim()) return <MermaidDiagram source={visual.mermaid} className={className} />;
  if (visual.type === 'table' && visual.table?.length) return <AiTable rows={visual.table} className={className} />;
  return null;
}
