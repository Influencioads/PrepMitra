import { Children, isValidElement, type ReactNode } from 'react';
import { useLocation } from 'react-router-dom';
import { motion, type Transition, type Variants } from 'framer-motion';

/**
 * PrepMitra motion: subtle and fast (150–300 ms), never in the student's way.
 * Everything respects "reduce motion" (MotionConfig reducedMotion="user" in App).
 */
export const EASE = [0.22, 1, 0.36, 1] as const;
export const FAST: Transition = { duration: 0.18, ease: EASE };
export const BASE: Transition = { duration: 0.24, ease: EASE };

/** Each page fades in and rises 8px when the route changes (enter only, so navigation never waits). */
export function PageTransition({ children, className }: { children: ReactNode; className?: string }) {
  const { pathname } = useLocation();
  return (
    <motion.div key={pathname} className={className} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={BASE}>
      {children}
    </motion.div>
  );
}

/** Simple fade-in (optionally rising a little) for one block. */
export function FadeIn({ children, className, y = 6, delay = 0 }: { children: ReactNode; className?: string; y?: number; delay?: number }) {
  return (
    <motion.div className={className} initial={{ opacity: 0, y }} animate={{ opacity: 1, y: 0 }} transition={{ ...BASE, delay }}>
      {children}
    </motion.div>
  );
}

const item: Variants = {
  hidden: { opacity: 0, y: 10 },
  // Stagger is capped so long lists don't keep animating.
  show: (i: number) => ({ opacity: 1, y: 0, transition: { ...BASE, delay: Math.min(i, 10) * 0.035 } }),
};

/**
 * A grid or list whose children appear one after another. Use it in place of the wrapping div:
 *   <Stagger className="grid gap-4 sm:grid-cols-3">{cards}</Stagger>
 * Each child is wrapped in a motion div (`itemClassName`, default h-full so cards keep equal heights).
 */
export function Stagger({
  children, className, itemClassName = 'h-full', as = 'div', ...rest
}: { children: ReactNode; className?: string; itemClassName?: string; as?: 'div' | 'ul' | 'ol'; 'aria-label'?: string }) {
  const Comp = motion[as];
  const Item = as === 'div' ? motion.div : motion.li;
  let i = 0;
  return (
    <Comp className={className} initial="hidden" animate="show" {...rest}>
      {Children.map(children, (child) =>
        child == null || child === false ? null : (
          <Item key={isValidElement(child) && child.key != null ? child.key : i} className={itemClassName} variants={item} custom={i++}>
            {child}
          </Item>
        ),
      )}
    </Comp>
  );
}

export { motion, AnimatePresence, MotionConfig } from 'framer-motion';
