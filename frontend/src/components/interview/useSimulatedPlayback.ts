import { useCallback, useEffect, useRef, useState } from 'react';

const hasSpeech = () => typeof window !== 'undefined' && 'speechSynthesis' in window && typeof SpeechSynthesisUtterance !== 'undefined';

/**
 * Simulated interviewer audio. Progress runs on a timer sized to the text; if the
 * browser supports speechSynthesis the text is also read aloud locally. No audio
 * is sent anywhere. Production streams TTS audio from the interview service.
 */
export function useSimulatedPlayback(text: string, opts: { lang?: string; autoPlay?: boolean; enabled?: boolean } = {}) {
  const { lang = 'en-IN', autoPlay = false, enabled = true } = opts;
  const durationMs = Math.min(14_000, Math.max(2_500, text.split(/\s+/).length * 330));
  const [progress, setProgress] = useState(0);
  const [playing, setPlaying] = useState(false);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);
  const progressRef = useRef(0);

  const clear = () => {
    if (timer.current) clearInterval(timer.current);
    timer.current = null;
  };

  const stopSpeech = () => {
    if (hasSpeech()) window.speechSynthesis.cancel();
  };

  const tick = useCallback(() => {
    clear();
    timer.current = setInterval(() => {
      progressRef.current = Math.min(100, progressRef.current + (100 * 100) / durationMs);
      setProgress(progressRef.current);
      if (progressRef.current >= 100) {
        clear();
        setPlaying(false);
      }
    }, 100);
  }, [durationMs]);

  const play = useCallback(() => {
    if (!enabled) return;
    if (progressRef.current >= 100) progressRef.current = 0;
    if (hasSpeech()) {
      if (window.speechSynthesis.paused && progressRef.current > 0) window.speechSynthesis.resume();
      else {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = lang;
        u.rate = 1;
        window.speechSynthesis.speak(u);
      }
    }
    setPlaying(true);
    tick();
  }, [enabled, text, lang, tick]);

  const pause = useCallback(() => {
    clear();
    setPlaying(false);
    if (hasSpeech()) window.speechSynthesis.pause();
  }, []);

  const replay = useCallback(() => {
    progressRef.current = 0;
    setProgress(0);
    stopSpeech();
    play();
  }, [play]);

  // Reset when the text changes; optionally auto-play the new question.
  useEffect(() => {
    clear();
    stopSpeech();
    progressRef.current = 0;
    setProgress(0);
    setPlaying(false);
    if (autoPlay && enabled && text) {
      const t = setTimeout(() => play(), 300);
      return () => clearTimeout(t);
    }
    return undefined;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [text, autoPlay, enabled]);

  useEffect(
    () => () => {
      clear();
      stopSpeech();
    },
    [],
  );

  return { playing, progress, play, pause, replay, durationSec: Math.round(durationMs / 1000), speechAvailable: hasSpeech() };
}
