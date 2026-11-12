import { useEffect } from 'react';
import { Stack } from 'expo-router';
import { useFonts } from 'expo-font';
import { Kalam_400Regular } from '@expo-google-fonts/kalam/400Regular';
import { Kalam_700Bold } from '@expo-google-fonts/kalam/700Bold';
import * as SplashScreen from 'expo-splash-screen';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { ToastProvider } from '@/components';
import { SplashView } from '@/features/brand/SplashView';
import { useAuthStore, useStoresHydrated } from '@/store';
import { colors } from '@/theme';

SplashScreen.preventAutoHideAsync().catch(() => undefined);

/**
 * Root navigator. Route groups are gated with `Stack.Protected` (UI-only — the
 * backend must enforce real authorization):
 *  - (auth) screens only while signed out,
 *  - onboarding only while signed in with an incomplete profile,
 *  - tabs and every app screen only when signed in and onboarded.
 * When a guard flips (sign-in, onboarding done, logout) the guarded screens
 * are removed and the user lands on `/`, which redirects to the right place.
 */
export default function RootLayout() {
  const storesHydrated = useStoresHydrated();
  // Kalam is the handwriting used for red-pen notes and Mitra's chalk. If it fails to load we fall back to the system font.
  const [fontsLoaded, fontError] = useFonts({ Kalam_400Regular, Kalam_700Bold });
  const hydrated = storesHydrated && (fontsLoaded || !!fontError);
  const session = useAuthStore((s) => s.session);
  const authed = !!session;
  const onboarded = !!session?.user.onboardingComplete;

  useEffect(() => {
    if (hydrated) SplashScreen.hideAsync().catch(() => undefined);
  }, [hydrated]);

  return (
    <SafeAreaProvider>
      <StatusBar style={hydrated ? 'dark' : 'light'} />
      {!hydrated ? (
        <SplashView />
      ) : (
        <ToastProvider>
          <Stack
            screenOptions={{
              headerTintColor: colors.primary,
              headerTitleStyle: { color: colors.text, fontWeight: '700' },
              headerStyle: { backgroundColor: colors.card },
              headerShadowVisible: false,
              headerBackButtonDisplayMode: 'minimal',
              contentStyle: { backgroundColor: colors.background },
            }}
          >
            <Stack.Screen name="index" options={{ headerShown: false }} />

            <Stack.Protected guard={!authed} redirectTo="/">
              <Stack.Screen name="(auth)" options={{ headerShown: false }} />
            </Stack.Protected>

            <Stack.Protected guard={authed && !onboarded} redirectTo="/">
              <Stack.Screen name="onboarding" options={{ headerShown: false, gestureEnabled: false }} />
            </Stack.Protected>

            <Stack.Protected guard={authed && onboarded} redirectTo="/">
              <Stack.Screen name="(tabs)" options={{ headerShown: false, title: 'Home' }} />
              <Stack.Screen name="exams/[id]/index" options={{ title: 'Exam details' }} />
              <Stack.Screen name="exams/[id]/instructions" options={{ title: 'Instructions' }} />
              <Stack.Screen
                name="exam/[attemptId]"
                options={{ headerShown: false, gestureEnabled: false, fullScreenGestureEnabled: false, animation: 'slide_from_bottom' }}
              />
              <Stack.Screen name="exam-result/[reportId]" options={{ title: 'Result', gestureEnabled: false }} />
              <Stack.Screen name="reports/[reportId]" options={{ title: 'Performance report' }} />
              <Stack.Screen name="interviews/index" options={{ title: 'Mock interviews' }} />
              <Stack.Screen name="interviews/[roleId]" options={{ title: 'Interview setup' }} />
              <Stack.Screen name="interview/session/[sessionId]" options={{ title: 'Interview', gestureEnabled: false, fullScreenGestureEnabled: false }} />
              <Stack.Screen name="interview/report/[reportId]" options={{ title: 'Interview report' }} />
              <Stack.Screen name="progress" options={{ title: 'Progress analytics' }} />
              <Stack.Screen name="subscription" options={{ title: 'Credits & plans' }} />
              <Stack.Screen name="ai/doubts" options={{ title: 'Doubt Solver' }} />
              <Stack.Screen name="ai/tutor" options={{ title: 'AI Tutor' }} />
              <Stack.Screen name="ai/persona" options={{ title: 'Persona & rank' }} />
              <Stack.Screen name="ai/notes" options={{ title: 'Notes & decks' }} />
              <Stack.Screen name="ai/practice" options={{ title: 'Revision & practice' }} />
              <Stack.Screen name="ai/coach" options={{ title: 'Cheat Code Coach' }} />
              <Stack.Screen name="ai/artifact/[id]" options={{ title: 'Study material' }} />
              <Stack.Screen name="notifications" options={{ title: 'Notifications' }} />
              <Stack.Screen name="settings" options={{ title: 'Settings' }} />
              <Stack.Screen name="edit-profile" options={{ title: 'Edit profile' }} />
            </Stack.Protected>

            <Stack.Screen name="+not-found" options={{ title: 'Not found' }} />
          </Stack>
        </ToastProvider>
      )}
    </SafeAreaProvider>
  );
}
