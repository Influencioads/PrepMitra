import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { AnimatePresence, motion } from 'framer-motion';

describe('framer-motion', () => {
  it('is installed and renders motion components', () => {
    render(<AnimatePresence><motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>Hello motion</motion.div></AnimatePresence>);
    expect(screen.getByText('Hello motion')).toBeInTheDocument();
  });
});
