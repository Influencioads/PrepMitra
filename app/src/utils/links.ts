/**
 * Notifications and recommendations carry web-style paths (shared seed data).
 * Mobile routes deliberately mirror the web paths, so most links resolve
 * unchanged; the few web-only pages are mapped to their mobile equivalent.
 */
const ALIASES: Record<string, string> = {
  '/dashboard': '/home',
  '/exams': '/explore',
  '/my-tests': '/reports',
  '/pricing': '/subscription',
};

export function toMobileHref(link: string | undefined): string | null {
  if (!link) return null;
  const [path = '', query] = link.split('?');
  const mapped = ALIASES[path] ?? path;
  if (!mapped.startsWith('/')) return null;
  return query ? `${mapped}?${query}` : mapped;
}
