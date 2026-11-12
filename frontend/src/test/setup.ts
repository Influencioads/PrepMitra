import '@testing-library/jest-dom/vitest';
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import { MotionGlobalConfig } from 'framer-motion';

// Animations finish instantly in tests.
MotionGlobalConfig.skipAnimations = true;

afterEach(() => {
  cleanup();
  localStorage.clear();
});

// Recharts' ResponsiveContainer needs ResizeObserver in jsdom.
class RO {
  observe() {}
  unobserve() {}
  disconnect() {}
}
(globalThis as unknown as { ResizeObserver: typeof RO }).ResizeObserver ??= RO;
window.scrollTo = (() => undefined) as typeof window.scrollTo;

// jsdom has no IntersectionObserver; framer-motion's whileInView / useInView need one.
// Report everything as visible right away so in-view content renders in tests.
if (!('IntersectionObserver' in globalThis)) {
  class IO {
    constructor(private cb: IntersectionObserverCallback) {}
    observe(el: Element) {
      this.cb([{ isIntersecting: true, intersectionRatio: 1, target: el } as IntersectionObserverEntry], this as unknown as IntersectionObserver);
    }
    unobserve() {}
    disconnect() {}
    takeRecords() { return []; }
    root = null; rootMargin = ''; thresholds = [];
  }
  (globalThis as unknown as { IntersectionObserver: unknown }).IntersectionObserver = IO;
}
