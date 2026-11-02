import { router } from 'expo-router';
import { EmptyState, Screen } from '@/components';

export default function NotFound() {
  return (
    <Screen>
      <EmptyState
        icon="compass-outline"
        title="Page not found"
        description="This link doesn’t match any screen in the app."
        actionLabel="Go to start"
        onAction={() => router.replace('/')}
      />
    </Screen>
  );
}
