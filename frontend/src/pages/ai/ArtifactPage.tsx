import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button, Card, CardBody, LoadingSkeleton } from '@/components/ui';
import { AiErrorNotice, useAiQuery } from '@/components/ai/AiUi';
import { ArtifactBody, ArtifactHeader } from '@/components/ai/AiViews';
import { aiService } from '@/services/aiService';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

/** Any saved AI item (deep dive, notes, deck, card, evaluation) by id: GET /v1/ai/artifacts/{id}. */
export function ArtifactPage() {
  const { id = '' } = useParams();
  const navigate = useNavigate();
  const q = useAiQuery(() => aiService.artifact(id), id);
  useDocumentTitle(q.data?.title ?? 'Study material');
  return (
    <div className="mx-auto max-w-4xl">
      <Button variant="ghost" size="sm" className="mb-3" leftIcon={<ArrowLeft className="h-4 w-4" />} onClick={() => navigate(-1)}>Back</Button>
      {q.loading ? <LoadingSkeleton variant="page" /> : q.error ? <AiErrorNotice error={q.error} onRetry={q.reload} /> : q.data && (
        <Card><CardBody><ArtifactHeader a={q.data} /><ArtifactBody a={q.data} /></CardBody></Card>
      )}
    </div>
  );
}
