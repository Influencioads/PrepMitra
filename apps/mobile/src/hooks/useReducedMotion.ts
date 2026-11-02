import { useEffect, useState } from 'react';
import { AccessibilityInfo } from 'react-native';
import { useProfileStore } from '@/store/profileStore';

/** True when the OS "reduce motion" setting or the in-app Settings toggle is on. */
export function useReducedMotion(): boolean {
  const appSetting = useProfileStore((s) => s.settings.reduceMotion);
  const [system, setSystem] = useState(false);
  useEffect(() => {
    let alive = true;
    AccessibilityInfo.isReduceMotionEnabled()
      .then((v) => {
        if (alive) setSystem(v);
      })
      .catch(() => undefined);
    const sub = AccessibilityInfo.addEventListener('reduceMotionChanged', setSystem);
    return () => {
      alive = false;
      sub.remove();
    };
  }, []);
  return appSetting || system;
}
