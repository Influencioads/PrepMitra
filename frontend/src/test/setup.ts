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
