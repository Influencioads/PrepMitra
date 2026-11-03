import type { ReactNode } from 'react';
import { router } from 'expo-router';
import type { Recommendation } from '@prepmitra/shared';
import { AppText, Card, Divider, ListRow } from '@/components';
import { recommendationHref } from './recommendations';

export function RecommendationList({ items }: { items: Recommendation[] }) {
  if (items.length === 0) {
    return (
      <Card>
        <AppText variant="small">Complete a mock to get personalised recommendations.</AppText>
      </Card>
    );
  }
  return (
    <Card style={{ paddingVertical: 4 }}>
      {items.map((r, i) => (
        <ListRowWithDivider key={r.id} last={i === items.length - 1}>
          <ListRow
            title={r.title}
            subtitle={`${r.reason} · ${r.minutes} min`}
            icon={r.roleId ? 'chatbubbles-outline' : 'locate-outline'}
            iconTone={r.roleId ? 'secondary' : 'primary'}
            onPress={() => router.push(recommendationHref(r))}
          />
        </ListRowWithDivider>
      ))}
    </Card>
  );
}

function ListRowWithDivider({ children, last }: { children: ReactNode; last: boolean }) {
  return (
    <>
      {children}
      {!last && <Divider />}
    </>
  );
}
