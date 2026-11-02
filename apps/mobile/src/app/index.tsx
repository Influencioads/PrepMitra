import { Redirect } from 'expo-router';
import { useAuthStore } from '@/store';

/** Entry point: sends the user to welcome, onboarding or home based on auth state. */
export default function Index() {
  const session = useAuthStore((s) => s.session);
  if (!session) return <Redirect href="/welcome" />;
  if (!session.user.onboardingComplete) return <Redirect href="/onboarding" />;
  return <Redirect href="/home" />;
}
