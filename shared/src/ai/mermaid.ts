/**
 * A small Mermaid reader for the AI visuals (`visual.type === 'mermaid'`, `mind_map_mermaid`).
 *
 * The website renders Mermaid with the real library and falls back to this; the mobile app has no web view, so it
 * draws what this returns natively. It understands the two shapes the AI prompts ask for:
 *  - flowcharts (`graph TD` / `flowchart LR`) with `A[label] --> B(label)` edges, optional `-- text -->` / `-->|text|`;
 *  - mind maps (`mindmap`, indentation = depth).
 * Anything else comes back as `{ kind: 'unknown' }` and the screens show the source text.
 */

export interface MermaidNode {
  id: string;
  label: string;
}
export interface MermaidEdge {
  from: string;
  to: string;
  label?: string;
}
export interface MindMapNode {
  label: string;
  children: MindMapNode[];
}

export type ParsedMermaid =
  | { kind: 'flow'; direction: 'TD' | 'LR'; nodes: MermaidNode[]; edges: MermaidEdge[] }
  | { kind: 'mindmap'; root: MindMapNode }
  | { kind: 'unknown'; source: string };

const SHAPES: [RegExp, number][] = [
  [/^\(\((.*)\)\)$/, 2],
  [/^\[\[(.*)\]\]$/, 2],
  [/^\{\{(.*)\}\}$/, 2],
  [/^\(\[(.*)\]\)$/, 2],
  [/^\[\((.*)\)\]$/, 2],
  [/^\[(.*)\]$/, 1],
  [/^\((.*)\)$/, 1],
  [/^\{(.*)\}$/, 1],
  [/^>(.*)\]$/, 1],
];

const unquote = (s: string) => s.trim().replace(/^"(.*)"$/, '$1').replace(/<br\s*\/?>/gi, ' ').replace(/\s+/g, ' ').trim();

/** `A[Label]` → { id: 'A', label: 'Label' }; a bare `A` keeps its id as the label. */
function nodeOf(token: string): MermaidNode | null {
  const t = token.trim().replace(/:::\w+$/, '');
  const m = /^([\w\-.\u0080-￿]+)\s*(.*)$/.exec(t);
  if (!m) return null;
  const id = m[1]!;
  const shape = m[2]!.trim();
  if (!shape) return { id, label: id };
  for (const [re] of SHAPES) {
    const s = re.exec(shape);
    if (s) return { id, label: unquote(s[1]!) };
  }
  return { id, label: unquote(shape) };
}

// Edge operators: -->, ---, -.->, ==>, with an optional |label| or "-- label -->" form.
const EDGE = /\s*(?:--\s*([^-|>][^>]*?)\s*-->|==\s*([^=|>][^>]*?)\s*==>|-\.\s*([^.>]+?)\s*\.->|-->|---|-\.->|==>|--x|--o)\s*(?:\|([^|]*)\|)?\s*/;

function parseFlow(lines: string[], header: string): ParsedMermaid {
  const dir = /\b(LR|RL)\b/.test(header) ? 'LR' : 'TD';
  const nodes = new Map<string, MermaidNode>();
  const edges: MermaidEdge[] = [];
  const add = (n: MermaidNode | null) => {
    if (!n) return null;
    const prev = nodes.get(n.id);
    // Keep the first real label (later bare references only repeat the id).
    if (!prev || (prev.label === prev.id && n.label !== n.id)) nodes.set(n.id, n);
    return n.id;
  };
  for (const raw of lines) {
    for (const stmt of raw.split(';')) {
      const line = stmt.trim();
      if (!line || /^(subgraph|end$|classDef|class |style |linkStyle|click |%%)/.test(line)) continue;
      const parts: string[] = [];
      const labels: (string | undefined)[] = [];
      let rest = line;
      for (;;) {
        const m = EDGE.exec(rest);
        if (!m) break;
        parts.push(rest.slice(0, m.index));
        labels.push((m[1] ?? m[2] ?? m[3] ?? m[4])?.trim() || undefined);
        rest = rest.slice(m.index + m[0].length);
      }
      parts.push(rest);
      if (parts.length === 1) {
        add(nodeOf(line));
        continue;
      }
      // "A & B --> C" fans out.
      const groups = parts.map((p) => p.split(/\s+&\s+/).map((x) => add(nodeOf(x))).filter((x): x is string => !!x));
      for (let i = 0; i < groups.length - 1; i++)
        for (const from of groups[i]!) for (const to of groups[i + 1]!) edges.push({ from, to, label: labels[i] });
    }
  }
  return { kind: 'flow', direction: dir, nodes: [...nodes.values()], edges };
}

function parseMindmap(lines: string[]): ParsedMermaid {
  const rows = lines
    .filter((l) => l.trim() && !l.trim().startsWith('%%'))
    .map((l) => {
      const depth = (/^\s*/.exec(l)?.[0] ?? '').replace(/\t/g, '  ').length;
      const text = l.trim().replace(/^::icon\(.*\)$/, '');
      // A mind map line is usually just text; "root((Topic))" or "id[Topic]" has an id plus a shape.
      const shaped = /^[\w\-.]*\s*[[({]/.test(text) ? nodeOf(text.replace(/^([[({])/, 'n$1')) : null;
      const label = shaped ? shaped.label : unquote(text);
      return { depth, label };
    })
    .filter((r) => r.label);
  if (!rows.length) return { kind: 'unknown', source: lines.join('\n') };
  const root: MindMapNode = { label: rows[0]!.label, children: [] };
  const stack: { depth: number; node: MindMapNode }[] = [{ depth: rows[0]!.depth, node: root }];
  for (const r of rows.slice(1)) {
    while (stack.length > 1 && stack[stack.length - 1]!.depth >= r.depth) stack.pop();
    const node: MindMapNode = { label: r.label, children: [] };
    stack[stack.length - 1]!.node.children.push(node);
    stack.push({ depth: r.depth, node });
  }
  return { kind: 'mindmap', root };
}

/** Strips ```mermaid fences the model sometimes adds. */
export function cleanMermaid(source: string): string {
  return source.replace(/^\s*```(?:mermaid)?\s*/i, '').replace(/```\s*$/, '').trim();
}

export function parseMermaid(source: string | null | undefined): ParsedMermaid {
  const src = cleanMermaid(source ?? '');
  const lines = src.split(/\r?\n/);
  const firstIdx = lines.findIndex((l) => l.trim() && !l.trim().startsWith('%%'));
  if (firstIdx < 0) return { kind: 'unknown', source: src };
  const header = lines[firstIdx]!.trim();
  const body = lines.slice(firstIdx + 1);
  if (/^(graph|flowchart)\b/i.test(header)) {
    // "graph TD; A-->B" on one line.
    const inline = header.replace(/^(graph|flowchart)\s+\w*\s*;?/i, '');
    const parsed = parseFlow(inline ? [inline, ...body] : body, header);
    return parsed.kind === 'flow' && parsed.nodes.length ? parsed : { kind: 'unknown', source: src };
  }
  if (/^mindmap\b/i.test(header)) return parseMindmap(body);
  return { kind: 'unknown', source: src };
}

/** Flow nodes in reading order (topological where possible), for a simple top-to-bottom native layout. */
export function flowOrder(flow: Extract<ParsedMermaid, { kind: 'flow' }>): MermaidNode[] {
  const indeg = new Map(flow.nodes.map((n) => [n.id, 0]));
  for (const e of flow.edges) indeg.set(e.to, (indeg.get(e.to) ?? 0) + 1);
  const byId = new Map(flow.nodes.map((n) => [n.id, n]));
  const queue = flow.nodes.filter((n) => !indeg.get(n.id));
  const out: MermaidNode[] = [];
  const seen = new Set<string>();
  while (queue.length) {
    const n = queue.shift()!;
    if (seen.has(n.id)) continue;
    seen.add(n.id);
    out.push(n);
    for (const e of flow.edges.filter((x) => x.from === n.id)) {
      indeg.set(e.to, (indeg.get(e.to) ?? 1) - 1);
      if (!indeg.get(e.to) && byId.get(e.to)) queue.push(byId.get(e.to)!);
    }
  }
  for (const n of flow.nodes) if (!seen.has(n.id)) out.push(n); // cycles keep source order
  return out;
}
