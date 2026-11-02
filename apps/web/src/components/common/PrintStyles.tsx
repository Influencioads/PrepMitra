/**
 * Print stylesheet for reports ("Download PDF" uses the browser's Save as PDF).
 * Hides app chrome and interactive controls; mark anything else with data-print-hide.
 */
const CSS = `
@media print {
  @page { margin: 14mm; }
  html, body { background: #fff !important; }
  body * { box-shadow: none !important; }
  aside, header, nav, [data-print-hide], [role="tablist"], .Toastify, [data-sonner-toaster] { display: none !important; }
  main, #main { padding: 0 !important; margin: 0 !important; max-width: none !important; }
  .lg\\:pl-64 { padding-left: 0 !important; }
  [data-print-section] { break-inside: avoid; page-break-inside: avoid; }
  [data-print-break] { break-before: page; }
  a { color: inherit !important; text-decoration: none !important; }
}
`;

export function PrintStyles() {
  return <style>{CSS}</style>;
}
