/**
 * Builds a real PDF of the report as it looks on screen (every tab expanded), in the browser.
 * Used when there is no server PDF (the demo). Works for Hindi too, because the page is drawn
 * as images rather than re-typeset. The libraries load only when the student asks for a PDF.
 */
export async function buildReportPdf(container: HTMLElement): Promise<Blob> {
  const [{ toCanvas, getFontEmbedCSS }, { jsPDF }] = await Promise.all([import('html-to-image'), import('jspdf')]);
  const pdf = new jsPDF({ unit: 'mm', format: 'a4', compress: true });
  const PAGE_W = 210;
  const PAGE_H = 297;
  const M = 10;
  const box = container.getBoundingClientRect();
  const mmPerPx = (PAGE_W - 2 * M) / box.width;
  const pagePx = (PAGE_H - 2 * M) / mmPerPx;
  const skip = (n: Element) => n instanceof HTMLElement && n.dataset.printHide !== undefined;

  // Break the page into blocks no taller than an A4 page where possible (cards, rows, questions).
  const blocks: HTMLElement[] = [];
  const walk = (el: Element) => {
    for (const child of Array.from(el.children)) {
      if (!(child instanceof HTMLElement) || skip(child)) continue;
      const r = child.getBoundingClientRect();
      if (r.height < 1 || r.width < 1) continue;
      if (r.height > pagePx * 0.9 && child.children.length > 1) walk(child);
      else blocks.push(child);
    }
  };
  walk(container);
  blocks.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);

  const bg = getComputedStyle(document.body).backgroundColor || '#ffffff';
  const fontEmbedCSS = await getFontEmbedCSS(container).catch(() => '');
  const filter = (n: Node) => !skip(n as Element);

  let pageTop = blocks.length ? blocks[0]!.getBoundingClientRect().top : box.top;
  for (const el of blocks) {
    const r = el.getBoundingClientRect();
    if (r.bottom - pageTop > pagePx && r.top > pageTop + 1) {
      pdf.addPage();
      pageTop = r.top;
    }
    const canvas = await toCanvas(el, { pixelRatio: 2, backgroundColor: bg, fontEmbedCSS, filter, skipAutoScale: true });
    const x = M + (r.left - box.left) * mmPerPx;
    const w = r.width * mmPerPx;
    if (r.height <= pagePx) {
      pdf.addImage(canvas.toDataURL('image/jpeg', 0.88), 'JPEG', x, M + (r.top - pageTop) * mmPerPx, w, r.height * mmPerPx);
      continue;
    }
    // Taller than a page: slice it across pages.
    const scale = canvas.height / r.height;
    let offset = 0;
    while (offset < r.height) {
      const room = offset === 0 ? pagePx - (r.top - pageTop) : pagePx;
      const h = Math.min(room, r.height - offset);
      const slice = document.createElement('canvas');
      slice.width = canvas.width;
      slice.height = Math.max(1, Math.round(h * scale));
      slice.getContext('2d')!.drawImage(canvas, 0, Math.round(offset * scale), canvas.width, slice.height, 0, 0, canvas.width, slice.height);
      const y = offset === 0 ? M + (r.top - pageTop) * mmPerPx : M;
      pdf.addImage(slice.toDataURL('image/jpeg', 0.88), 'JPEG', x, y, w, h * mmPerPx);
      offset += h;
      if (offset < r.height) {
        pdf.addPage();
        pageTop = r.top + offset;
      }
    }
  }
  return pdf.output('blob');
}
