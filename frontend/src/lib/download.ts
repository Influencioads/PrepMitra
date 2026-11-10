/**
 * Saves a generated file for the viewer.
 * - Normal browser: a temporary download link.
 * - Inside a claude.ai artifact (the demo link): the page is framed and may not download
 *   directly, so the file goes through the viewer's `downloads` capability, which asks the
 *   viewer to confirm. Returns 'declined' if they say no.
 */
interface DownloadsNs {
  save(req: { filename: string; data: Blob }): Promise<{ status: string }>;
}
type ClaudeWindow = Window & { claude?: { use?: (name: string) => Promise<unknown> } };

/** True when the app runs inside the claude.ai artifact viewer (where print dialogs are blocked). */
export const inArtifactViewer = () => typeof window !== 'undefined' && typeof (window as ClaudeWindow).claude?.use === 'function';

const LIFECYCLE = new Set(['unavailable', 'not_granted', 'capability_disabled', 'capability_removed']);

export async function saveFile(filename: string, data: Blob): Promise<'saved' | 'declined'> {
  if (inArtifactViewer()) {
    const downloads = (await (window as ClaudeWindow).claude!.use!('downloads').catch(() => null)) as DownloadsNs | null;
    if (downloads) {
      try {
        await downloads.save({ filename, data });
        return 'saved';
      } catch (e) {
        const code = (e as { code?: string })?.code ?? '';
        if (code === 'declined') return 'declined';
        if (!LIFECYCLE.has(code)) throw Object.assign(new Error((e as { message?: string })?.message || 'The file could not be saved.'), { code });
      }
    }
  }
  const url = URL.createObjectURL(data);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  return 'saved';
}
