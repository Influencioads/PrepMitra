import { useState } from 'react';
import toast from 'react-hot-toast';
import { Button, Modal, Select, Textarea } from '@/components/ui';
import { attemptService, errorMessage } from '@/services';
import { useT } from '@/i18n';
import { examMessages } from '@/i18n/messages/exam';
import { commonMessages } from '@/i18n/messages/common';

const REASONS = [
  { value: 'wrong-answer', key: 'reasonWrong' },
  { value: 'unclear', key: 'reasonUnclear' },
  { value: 'translation', key: 'reasonTranslation' },
  { value: 'typo', key: 'reasonTypo' },
  { value: 'other', key: 'reasonOther' },
] as const;

export function ReportQuestionModal({
  open, onOpenChange, questionId, questionNumber, onSent,
}: { open: boolean; onOpenChange: (o: boolean) => void; questionId: string; questionNumber: number; onSent?: () => void }) {
  const t = useT(examMessages);
  const tc = useT(commonMessages);
  const [reason, setReason] = useState('wrong-answer');
  const [note, setNote] = useState('');
  const [sending, setSending] = useState(false);

  const submit = async () => {
    setSending(true);
    try {
      await attemptService.reportQuestion(questionId, reason, note.trim() || undefined);
      toast.success(t('reportSent'));
      setNote('');
      onSent?.();
      onOpenChange(false);
    } catch (e) {
      // POST /flags returns 409 already_reported when this student flagged the question before.
      if ((e as { code?: string })?.code === 'already_reported') {
        toast(t('alreadyReported'), { id: 'already-reported' });
        onSent?.();
        onOpenChange(false);
        return;
      }
      toast.error(errorMessage(e));
    } finally {
      setSending(false);
    }
  };

  return (
    <Modal
      open={open}
      onOpenChange={onOpenChange}
      title={t('reportQuestionTitle', { n: questionNumber })}
      description={t('reportQuestionDesc')}
      size="sm"
      footer={
        <>
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={sending}>{tc('cancel')}</Button>
          <Button onClick={submit} loading={sending}>{t('sendReport')}</Button>
        </>
      }
    >
      <div className="space-y-4">
        <Select label={t('whatsWrong')} value={reason} onChange={(e) => setReason(e.target.value)} options={REASONS.map((r) => ({ value: r.value, label: t(r.key) }))} />
        <Textarea label={t('detailsOptional')} rows={3} maxLength={500} value={note} onChange={(e) => setNote(e.target.value)} placeholder={t('detailsPlaceholder')} />
      </div>
    </Modal>
  );
}
