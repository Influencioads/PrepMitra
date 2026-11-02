import { useEffect } from 'react';

function upsertMeta(attr: 'name' | 'property', key: string, content: string): () => void {
  let el = document.head.querySelector<HTMLMetaElement>(`meta[${attr}="${key}"]`);
  const created = !el;
  if (!el) {
    el = document.createElement('meta');
    el.setAttribute(attr, key);
    document.head.appendChild(el);
  }
  const prev = el.getAttribute('content');
  el.setAttribute('content', content);
  return () => {
    if (created) el!.remove();
    else if (prev !== null) el!.setAttribute('content', prev);
  };
}

/**
 * Sets the page title (and, when given, the meta description plus Open Graph
 * title/description) for SEO and link previews. Restores the previous values on unmount.
 */
export function useDocumentTitle(title: string, description?: string) {
  useEffect(() => {
    const prev = document.title;
    const full = title ? `${title} · PrepMitra AI` : 'PrepMitra AI';
    document.title = full;
    const restorers: (() => void)[] = [upsertMeta('property', 'og:title', full)];
    if (description) {
      restorers.push(upsertMeta('name', 'description', description), upsertMeta('property', 'og:description', description));
    }
    return () => {
      document.title = prev;
      restorers.reverse().forEach((r) => r());
    };
  }, [title, description]);
}
