const pad = (n: number) => String(n).padStart(2, '0');

/** Countdown clock: 09:41 or 1:05:09. */
export function formatClock(totalSeconds: number): string {
  const s = Math.max(0, Math.floor(totalSeconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  return h > 0 ? `${h}:${pad(m)}:${pad(sec)}` : `${pad(m)}:${pad(sec)}`;
}

/** Human duration: 45s, 12m 30s, 1h 05m. */
export function formatDuration(totalSeconds: number): string {
  const s = Math.max(0, Math.round(totalSeconds));
  if (s < 60) return `${s}s`;
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (h > 0) return `${h}h ${pad(m)}m`;
  const sec = s % 60;
  return sec ? `${m}m ${pad(sec)}s` : `${m}m`;
}

/** ₹99, ₹1,299 — and money with paise always shows two decimals (₹15.10, not ₹15.1). */
export function formatINR(amount: number): string {
  const paise = Math.round(amount * 100);
  return paise % 100 === 0
    ? `₹${(paise / 100).toLocaleString('en-IN')}`
    : `₹${(paise / 100).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

const MONTHS_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const MONTHS_HI = ['जन॰', 'फ़र॰', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुल॰', 'अग॰', 'सित॰', 'अक्टू॰', 'नव॰', 'दिस॰'];
let dateLang: 'en' | 'hi' = 'en';
/** The website sets this from its UI language so dates and "2 days ago" follow English/Hindi. */
export function setFormatLanguage(lang: 'en' | 'hi') {
  dateLang = lang;
}
const month = (d: Date) => (dateLang === 'hi' ? MONTHS_HI : MONTHS_EN)[d.getMonth()];

export function formatDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  return `${d.getDate()} ${month(d)} ${d.getFullYear()}`;
}

export function formatShortDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  return `${d.getDate()} ${month(d)}`;
}

export function formatDateTime(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  const h = d.getHours();
  const hh = h % 12 === 0 ? 12 : h % 12;
  return `${formatDate(iso)}, ${hh}:${pad(d.getMinutes())} ${h < 12 ? 'AM' : 'PM'}`;
}

export function relativeTime(iso: string, now: number = Date.now()): string {
  const diff = Math.round((now - new Date(iso).getTime()) / 1000);
  const hi = dateLang === 'hi';
  if (diff < 60) return hi ? 'अभी' : 'just now';
  if (diff < 3600) return hi ? `${Math.floor(diff / 60)} मिनट पहले` : `${Math.floor(diff / 60)} min ago`;
  if (diff < 86400) return hi ? `${Math.floor(diff / 3600)} घंटे पहले` : `${Math.floor(diff / 3600)} h ago`;
  const days = Math.floor(diff / 86400);
  if (days === 1) return hi ? 'कल' : 'yesterday';
  if (days < 7) return hi ? `${days} दिन पहले` : `${days} days ago`;
  return formatDate(iso);
}

export function pluralize(count: number, singular: string, plural = `${singular}s`): string {
  return `${count} ${count === 1 ? singular : plural}`;
}

export function initials(name: string): string {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0]!.toUpperCase())
    .join('');
}

export function maskPhone(phone: string): string {
  return phone.length === 10 ? `+91 ${phone.slice(0, 2)}••••••${phone.slice(-2)}` : phone;
}
