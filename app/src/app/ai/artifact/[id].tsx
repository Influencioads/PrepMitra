import { Stack, useLocalSearchParams } from 'expo-router';
import { Card, LoadingSkeleton, Screen } from '@/components';
import { AiErrorNotice, useAiQuery } from '@/features/ai/AiUi';
import { ArtifactBody, ArtifactHeader } from '@/features/ai/AiViews';
import { aiService } from '@/services/aiService';

/** Any saved AI item (deep dive, notes, deck, card, evaluation): GET /v1/ai/artifacts/{id}. */
export default function ArtifactScreen() {
  const { id = '' } = useLocalSearchParams<{ id: string }>();
  const q = useAiQuery(() => aiService.artifact(id), id);
  return (
    <Screen>
      <Stack.Screen options={{ title: q.data?.title ?? 'Study material' }} />
      {q.loading ? <LoadingSkeleton /> : q.error ? <AiErrorNotice error={q.error} onRetry={q.reload} /> : q.data ? (
        <Card><ArtifactHeader a={q.data} /><ArtifactBody a={q.data} /></Card>
      ) : null}
    </Screen>
  );
}
