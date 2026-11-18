import { useRef, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, View, type NativeScrollEvent, type NativeSyntheticEvent, type ScrollViewInstance } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import { DISCLAIMERS, HERO_HEADLINE } from '@prepmitra/shared';
import { AppText, Button, Screen } from '@/components';
import { BrandMark } from '@/features/brand/BrandMark';
import { colors, radii, spacing, toneColors, type Tone } from '@/theme';
import type { IoniconName } from '@/utils/icons';

const SLIDES: { icon: IoniconName; tone: Tone; title: string; body: string }[] = [
  { icon: 'school', tone: 'primary', title: HERO_HEADLINE, body: 'Your personal AI coach for government exams, placements and interviews.' },
  { icon: 'document-text', tone: 'secondary', title: 'Real-pattern mock exams', body: 'SSC, banking, railway, UPSC, CAT, GATE and placement papers — timed like the real thing.' },
  { icon: 'chatbubbles', tone: 'info', title: 'Mock interviews', body: 'Practise by text or voice and get model answers with a score card.' },
  { icon: 'analytics', tone: 'warning', title: 'Reports that teach', body: 'See where marks leak and follow a 7-day plan built from your own answers — in 23 Indian languages.' },
];

export default function Welcome() {
  const [width, setWidth] = useState(0);
  const [page, setPage] = useState(0);
  const scroller = useRef<ScrollViewInstance>(null);
  const last = page === SLIDES.length - 1;

  const onScroll = (e: NativeSyntheticEvent<NativeScrollEvent>) => {
    if (!width) return;
    const next = Math.round(e.nativeEvent.contentOffset.x / width);
    if (next !== page) setPage(next);
  };
  const goTo = (i: number) => scroller.current?.scrollTo({ x: i * width, animated: true });

  return (
    <Screen
      scroll={false}
      padded={false}
      edges={['top', 'left', 'right', 'bottom']}
      footer={
        <>
          <View style={styles.dots} accessibilityLabel={`Slide ${page + 1} of ${SLIDES.length}`}>
            {SLIDES.map((s, i) => (
              <Pressable key={s.title} onPress={() => goTo(i)} accessibilityRole="button" accessibilityLabel={`Go to slide ${i + 1}`} hitSlop={8}>
                <View style={[styles.dot, i === page && styles.dotActive]} />
              </Pressable>
            ))}
          </View>
          {last ? (
            <Button title="Get started" size="lg" fullWidth rightIcon="arrow-forward" onPress={() => router.push('/signup')} />
          ) : (
            <Button title="Next" size="lg" fullWidth rightIcon="arrow-forward" onPress={() => goTo(page + 1)} />
          )}
          <Button title="I already have an account — Log in" variant="ghost" fullWidth onPress={() => router.push('/login')} />
        </>
      }
    >
      <View style={styles.top}>
        <BrandMark size={32} />
        {!last && (
          <Pressable onPress={() => goTo(SLIDES.length - 1)} accessibilityRole="button" hitSlop={8}>
            <AppText variant="smallStrong" color={colors.textSecondary}>Skip</AppText>
          </Pressable>
        )}
      </View>
      <View style={styles.flex} onLayout={(e) => setWidth(e.nativeEvent.layout.width)}>
        {width > 0 && (
          <ScrollView
            ref={scroller}
            horizontal
            pagingEnabled
            showsHorizontalScrollIndicator={false}
            onScroll={onScroll}
            scrollEventThrottle={16}
          >
            {SLIDES.map((s, i) => (
              <View key={s.title} style={[styles.slide, { width }]}>
                <View style={[styles.art, { backgroundColor: toneColors[s.tone].bg }]}>
                  <View style={[styles.artInner, { backgroundColor: toneColors[s.tone].fg }]}>
                    <Ionicons name={s.icon} size={56} color={colors.white} />
                  </View>
                </View>
                <AppText variant={i === 0 ? 'display' : 'h1'} align="center" accessibilityRole="header">{s.title}</AppText>
                <AppText variant="body" align="center" color={colors.textSecondary}>{s.body}</AppText>
              </View>
            ))}
          </ScrollView>
        )}
      </View>
      {last && <AppText variant="caption" align="center" style={styles.disclaimer}>{DISCLAIMERS.examAffiliation}</AppText>}
    </Screen>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  top: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: spacing.lg, paddingTop: spacing.md },
  slide: { flex: 1, alignItems: 'center', justifyContent: 'center', paddingHorizontal: spacing.xl, gap: spacing.md },
  art: { width: 200, height: 200, borderRadius: 100, alignItems: 'center', justifyContent: 'center', marginBottom: spacing.lg },
  artInner: { width: 112, height: 112, borderRadius: radii.xl * 1.5, alignItems: 'center', justifyContent: 'center', transform: [{ rotate: '-6deg' }] },
  dots: { flexDirection: 'row', justifyContent: 'center', gap: 8, paddingBottom: spacing.sm },
  dot: { width: 8, height: 8, borderRadius: 4, backgroundColor: colors.border },
  dotActive: { width: 24, backgroundColor: colors.primary },
  disclaimer: { paddingHorizontal: spacing.lg, paddingBottom: spacing.sm },
});
