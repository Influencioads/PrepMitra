import type { AdminOrder } from '@prepmitra/shared';
import { APP_NAME, SUPPORT_EMAIL, formatDate, getPlan } from '@prepmitra/shared';

/** Triggers a real browser download for generated content. */
export function downloadFile(filename: string, content: string, mime: string) {
  const blob = new Blob([content], { type: `${mime};charset=utf-8` });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.rel = 'noopener';
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

const csvCell = (v: unknown) => {
  const s = v === undefined || v === null ? '' : String(v);
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
};

/** RFC 4180 CSV. Prefixed with a BOM so Excel opens Indian-language text correctly. */
export function toCsv(headers: string[], rows: unknown[][]): string {
  return '﻿' + [headers, ...rows].map((r) => r.map(csvCell).join(',')).join('\r\n');
}

export const todayStamp = () => new Date().toISOString().slice(0, 10);

const esc = (s: string) => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);
const inr = (n: number) => `₹${n.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

/** Self-contained printable GST invoice (demo). */
export function buildInvoiceHtml(order: AdminOrder): string {
  const plan = getPlan(order.planId);
  const taxable = Math.round((order.amountInr - order.gstInr) * 100) / 100;
  const half = Math.round((order.gstInr / 2) * 100) / 100;
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Invoice ${esc(order.invoiceNo)}</title>
<style>
body{font-family:"DM Sans",system-ui,sans-serif;color:#1c2321;max-width:720px;margin:32px auto;padding:0 16px}
h1{font-size:22px;margin:0}.muted{color:#5b6661;font-size:13px}table{width:100%;border-collapse:collapse;margin-top:24px}
th,td{border-bottom:1px solid #e3e2d8;padding:8px;text-align:left;font-size:14px}td.r,th.r{text-align:right}
.demo{background:#fffbeb;border:1px solid #fde68a;color:#92400e;padding:8px 12px;border-radius:8px;font-size:13px;margin-bottom:20px}
.total td{font-weight:700}
</style></head><body>
<div class="demo">DEMO INVOICE — generated from prototype data. No real payment was processed. Not valid for tax purposes.</div>
<h1>${esc(APP_NAME)} — Tax Invoice</h1>
<p class="muted">Invoice no. ${esc(order.invoiceNo)} · Date ${esc(formatDate(order.createdAt))} · Order ${esc(order.id)}</p>
<p class="muted">Supplier GSTIN: 27AAAAA0000A1Z5 (placeholder) · ${esc(SUPPORT_EMAIL)}</p>
<p><strong>Billed to:</strong> ${esc(order.userName)} (${esc(order.userId)})</p>
<table>
<thead><tr><th>Description</th><th>SAC</th><th class="r">Amount</th></tr></thead>
<tbody>
<tr><td>${esc(plan?.name ?? order.planId)} — ${plan?.credits ?? 0} credit(s)</td><td>999293</td><td class="r">${inr(taxable)}</td></tr>
<tr><td>CGST @ 9%</td><td></td><td class="r">${inr(half)}</td></tr>
<tr><td>SGST @ 9%</td><td></td><td class="r">${inr(order.gstInr - half)}</td></tr>
<tr class="total"><td>Total (GST inclusive)</td><td></td><td class="r">${inr(order.amountInr)}</td></tr>
</tbody></table>
<p class="muted">Payment via ${esc(order.gateway)} (${esc(order.method)}) · Status: ${esc(order.status)}${order.refundedAt ? ` · Refunded ${esc(formatDate(order.refundedAt))}` : ''}</p>
</body></html>`;
}
