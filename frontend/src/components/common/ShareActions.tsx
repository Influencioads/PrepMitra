import { useState } from 'react';
import toast from 'react-hot-toast';
import { FileDown, Link2, Printer } from 'lucide-react';
import { Button } from '@/components/ui';
import { errorMessage } from '@/services';
import { copyText, currentShareUrl } from '@/lib/share';
import { inArtifactViewer } from '@/lib/download';
import { useT } from '@/i18n';
import { reportMessages } from '@/i18n/messages/report';

/**
 * Download PDF, optional HTML download, and copy share link.
 * - `onDownloadPdf` (real API): downloads the server-generated PDF; "Print" then opens the print layout.
 *   Without it, "Download PDF" opens the print layout (save as PDF from the print dialog).
 * - `getShareUrl` (real API): creates a public share link; otherwise the current page link is copied.
 */
export function ShareActions({
  onPrint, onDownloadHtml, onDownloadPdf, getShareUrl,
}: { onPrint: () => void; onDownloadHtml?: () => void; onDownloadPdf?: () => Promise<void>; getShareUrl?: () => Promise<string> }) {
  const t = useT(reportMessages);
  const [pdfBusy, setPdfBusy] = useState(false);
  const [shareBusy, setShareBusy] = useState(false);

  const copy = async () => {
    let url = currentShareUrl();
    if (getShareUrl) {
      setShareBusy(true);
      try {
        url = await getShareUrl();
      } catch (e) {
        toast.error(t('shareLinkFailed', { error: errorMessage(e) }));
        return;
      } finally {
        setShareBusy(false);
      }
    }
    const ok = await copyText(url);
    if (ok) toast.success(t('linkCopied'));
    else toast.error(t('linkCopyFailed'));
  };

  const downloadPdf = async () => {
    if (!onDownloadPdf) return onPrint();
    setPdfBusy(true);
    try {
      await onDownloadPdf();
    } catch (e) {
      toast.error(t('pdfFailed', { error: errorMessage(e) }));
    } finally {
      setPdfBusy(false);
    }
  };

  return (
    <>
      <Button variant="outline" onClick={() => void downloadPdf()} loading={pdfBusy} leftIcon={onDownloadPdf ? <FileDown className="h-4 w-4" /> : <Printer className="h-4 w-4" />}>
        {t('downloadPdf')}
      </Button>
      {onDownloadPdf && !inArtifactViewer() && (
        <Button variant="ghost" onClick={onPrint} leftIcon={<Printer className="h-4 w-4" />}>{t('printReport')}</Button>
      )}
      {onDownloadHtml && !onDownloadPdf && (
        <Button variant="ghost" onClick={onDownloadHtml} leftIcon={<FileDown className="h-4 w-4" />}>{t('downloadHtml')}</Button>
      )}
      <Button variant="ghost" onClick={() => void copy()} loading={shareBusy} leftIcon={<Link2 className="h-4 w-4" />}>{t('copyShareLink')}</Button>
    </>
  );
}
