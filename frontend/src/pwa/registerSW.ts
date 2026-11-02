/**
 * Registers the service worker that makes PrepMitra AI installable and gives an
 * offline fallback. Production builds only; skipped on file:// or other schemes.
 */
export function registerSW() {
  if (!import.meta.env.PROD) return;
  if (typeof window === 'undefined' || !('serviceWorker' in navigator)) return;
  if (!/^https?:$/.test(window.location.protocol)) return;
  const base = import.meta.env.BASE_URL || '/';
  window.addEventListener('load', () => {
    navigator.serviceWorker.register(`${base}sw.js`, { scope: base }).catch(() => {
      /* Registration can fail in sandboxed frames or private modes; the app works without it. */
    });
  });
}
