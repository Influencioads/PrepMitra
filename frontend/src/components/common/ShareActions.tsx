import toast from 'react-hot-toast';
import { FileDown, Link2, Printer } from 'lucide-react';
import { Button } from '@/components/ui';
import { copyText, currentShareUrl } from '@/lib/share';
import { useT } from '@/i18n';
import { reportMessages } from '@/i18n/messages/report';


/** Download PDF (print layout), optional HTML download, and copy share link. */
export function ShareActions({ onPrint, onDownloadHtml }: { onPrint: () => void; onDownloadHtml?: () => void }) {
  const t = useT(reportMessages);
  const copy = async () => {
    const ok = await copyText(currentShareUrl());
    if (ok) toast.success(t('linkCopied'));
    else toast.error(t('linkCopyFailed'));
  };
  return (
    <>
      <Button variant="outline" onClick={onPrint} leftIcon={<Printer className="h-4 w-4" />}>{t('downloadPdf')}</Button>
      {onDownloadHtml && (
        <Button variant="ghost" onClick={onDownloadHtml} leftIcon={<FileDown className="h-4 w-4" />}>{t('downloadHtml')}</Button>
      )}
      <Button variant="ghost" onClick={() => void copy()} leftIcon={<Link2 className="h-4 w-4" />}>{t('copyShareLink')}</Button>
    </>
  );
}
