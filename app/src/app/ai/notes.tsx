import { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import type { DeckRequest, Notes, NotesKind, NotesLevel, TopicDeck } from '@prepmitra/shared';
import { AppText, Badge, Button, Card, CardHeader, Divider, Input, ListRow, Screen, SegmentedControl, Select, SwitchRow } from '@/components';
import { AiErrorNotice, AllowanceBadge, useAiAction, useAiQuery } from '@/features/ai/AiUi';
import { ArtifactHeader, DeckView, NotesView } from '@/features/ai/AiViews';
import { aiService } from '@/services/aiService';
import { spacing } from '@/theme';

const KINDS: { value: NotesKind; label: string }[] = [
  { value: 'notes', label: 'Notes' }, { value: 'formula_sheet', label: 'Formula sheet' }, { value: 'mind_map', label: 'Mind map' }, { value: 'revision_sheet', label: 'Revision sheet' },
];
const LEVELS: { value: NotesLevel; label: string }[] = [{ value: 'basic', label: 'Basic' }, { value: 'exam', label: 'Exam level' }, { value: 'advanced', label: 'Advanced' }];
type DeckMode = NonNullable<DeckRequest['mode']>;
const MODES: { value: DeckMode; label: string }[] = [
  { value: 'library', label: 'Library only (free)' }, { value: 'smart', label: 'Smart (1 Pro deck or 3 Smart credits)' },
  { value: 'master', label: 'Master (3 Master credits)' }, { value: 'ultra', label: 'Ultra (4 Ultra credits)' },
];

function NotesMaker() {
  const [topic, setTopic] = useState('');
  const [kind, setKind] = useState<NotesKind>('notes');
  const [level, setLevel] = useState<NotesLevel>('exam');
  const [personal, setPersonal] = useState(false);
  const [notes, setNotes] = useState<Notes | null>(null);
  const run = useAiAction(aiService.notes);
  const go = async () => { const r = await run.run({ topic: topic.trim(), kind, level, personal }); if (r) setNotes(r); };
  return (
    <View>
      <Card>
        <View style={{ gap: spacing.sm }}>
          <Input label="Topic" value={topic} onChangeText={setTopic} maxLength={120} placeholder="e.g. Time and work" />
          <Select label="Format" value={kind} onChange={setKind} options={KINDS} />
          <Select label="Level" value={level} onChange={setLevel} options={LEVELS} />
          <SwitchRow label="Make them personal" description="Built from your own mistakes. Uses 1 personal note; shared notes are free." value={personal} onValueChange={setPersonal} />
          <AllowanceBadge feature="personal_notes" label="Personal notes" />
          <Button title={run.busy ? 'Writing your notes…' : 'Make notes'} loading={run.busy} disabled={topic.trim().length < 3} onPress={go} />
          <AiErrorNotice error={run.error} onRetry={go} />
        </View>
      </Card>
      {notes ? <Card style={styles.gap}><ArtifactHeader a={notes} /><NotesView p={notes.payload} /></Card> : null}
    </View>
  );
}

function Decks() {
  const lib = useAiQuery(() => aiService.deckLibrary(), 'lib');
  const [deck, setDeck] = useState<TopicDeck | null>(null);
  const [topic, setTopic] = useState('');
  const [level, setLevel] = useState<NotesLevel>('exam');
  const [mode, setMode] = useState<DeckMode>('smart');
  const open = useAiAction(aiService.libraryDeck);
  const make = useAiAction(aiService.topicDeck);
  const go = async () => { const r = await make.run({ topic: topic.trim(), level, mode }); if (r) setDeck(r); };
  return (
    <View>
      {deck ? (
        <Card>
          <ArtifactHeader a={deck} extra={deck.paid_with ? <Badge label={deck.paid_with.replace('_', ' ')} /> : null} />
          <DeckView key={deck.id} p={deck.payload} note={deck.personal_note} />
          <Button title="Back to decks" variant="ghost" style={styles.gap} onPress={() => setDeck(null)} />
        </Card>
      ) : (
        <>
          <Card>
            <CardHeader title="Free library" subtitle="Ready-made decks, free on every plan." />
            {lib.data?.map((d, i) => (
              <View key={d.id}>
                {i > 0 && <Divider />}
                <ListRow icon="layers-outline" title={d.title} subtitle={d.level} onPress={async () => { const r = await open.run(d.id); if (r) setDeck(r); }} />
              </View>
            ))}
            {lib.loading ? <AppText variant="small">Loading…</AppText> : null}
            <AiErrorNotice error={lib.error ?? open.error} onRetry={lib.reload} />
          </Card>
          <Card style={styles.gap}>
            <CardHeader title="Custom deck" subtitle="10–15 slides with visuals, traps, cheat codes and practice." />
            <View style={{ gap: spacing.sm }}>
              <Input label="Topic" value={topic} onChangeText={setTopic} maxLength={120} />
              <Select label="Level" value={level} onChange={setLevel} options={LEVELS} />
              <Select label="Made with" value={mode} onChange={setMode} options={MODES} />
              <View style={styles.row}><AllowanceBadge feature="topic_decks" label="Decks" /><AllowanceBadge feature="smart_credits" label="Smart" /></View>
              <Button title={make.busy ? 'Building slides…' : 'Make deck'} loading={make.busy} disabled={topic.trim().length < 3} onPress={go} />
              <AiErrorNotice error={make.error} onRetry={go} />
            </View>
          </Card>
        </>
      )}
    </View>
  );
}

export default function NotesScreen() {
  const params = useLocalSearchParams<{ tab?: string }>();
  const [tab, setTab] = useState<'notes' | 'decks'>(params.tab === 'decks' ? 'decks' : 'notes');
  return (
    <Screen keyboard>
      <SegmentedControl value={tab} onChange={setTab} accessibilityLabel="Notes or decks" segments={[{ value: 'notes', label: 'Notes Maker' }, { value: 'decks', label: 'Topic decks' }]} />
      <View style={styles.gap}>{tab === 'notes' ? <NotesMaker /> : <Decks />}</View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  gap: { marginTop: spacing.md },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.xs },
});
