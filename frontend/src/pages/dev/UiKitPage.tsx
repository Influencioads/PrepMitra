import { useState, type ReactNode } from 'react';
import toast from 'react-hot-toast';
import { Bell, Coins, Menu, Search } from 'lucide-react';
import {
  Avatar, Badge, Bubble, Button, Card, CardBody, CardHeader, Checkbox, ChoiceChip, EmptyState, Input, LanguageSelector, LoadingSkeleton, Logo,
  MarksLeak, Mitra, MitraSays, Modal, Notice, PenNote, PenScore, ProgressBar, Select, Spinner, Stamp, StatCard, StickyNote, Switch, Tabs, Textarea,
} from '@/components/ui';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';

/**
 * UI kit (15-day plan, Day 2): every shared component on one page, for design review and
 * as a reference while building screens. Internal page — not linked from the menus, no data.
 * Check it at phone width (≈390 px) and desktop.
 */
const COLORS: { name: string; token: string; text?: string }[] = [
  { name: 'Primary · saffron', token: 'primary', text: 'text-white' },
  { name: 'Primary soft', token: 'primary-soft' },
  { name: 'Secondary · peepal green', token: 'secondary', text: 'text-white' },
  { name: 'Accent · marigold', token: 'accent' },
  { name: 'Background', token: 'background' },
  { name: 'Card', token: 'card' },
  { name: 'Ink', token: 'ink', text: 'text-white' },
  { name: 'Muted', token: 'muted', text: 'text-white' },
  { name: 'Line', token: 'line' },
  { name: 'Success', token: 'success', text: 'text-white' },
  { name: 'Warning', token: 'warning', text: 'text-white' },
  { name: 'Danger', token: 'danger', text: 'text-white' },
  { name: 'Paper', token: 'paper' },
  { name: 'Red pen', token: 'pen', text: 'text-white' },
  { name: 'Chalkboard', token: 'chalk', text: 'text-white' },
];

const PALETTE_STATES = [
  { label: 'Not visited', cls: 'border border-line-strong bg-[#EFEFE8] text-ink' },
  { label: 'Not answered', cls: 'bg-[#FDE2DF] text-[#B91C1C]' },
  { label: 'Answered', cls: 'bg-[#15803D] text-white' },
  { label: 'Marked for review', cls: 'bg-[#7E22CE] text-white' },
  { label: 'Answered + marked', cls: 'bg-[#C2410C] text-white' },
];

function Section({ id, title, note, children }: { id: string; title: string; note?: string; children: ReactNode }) {
  return (
    <section id={id} aria-labelledby={`${id}-h`} className="scroll-mt-20 space-y-4">
      <div>
        <h2 id={`${id}-h`} className="text-2xl font-bold">{title}</h2>
        {note && <p className="mt-1 max-w-2xl text-sm text-muted">{note}</p>}
      </div>
      {children}
    </section>
  );
}

/** Static copy of the app header (logo, language, credit balance, alerts, avatar) at both widths. */
function HeaderPreview({ narrow, credits }: { narrow?: boolean; credits: number }) {
  return (
    <div className={cn('overflow-hidden rounded-xl border border-line bg-card', narrow ? 'w-[360px] max-w-full' : 'w-full')}>
      <div className="flex h-14 items-center gap-2 border-b border-line px-3 sm:px-4">
        {narrow && <span className="rounded-md p-1.5" aria-hidden><Menu className="h-5 w-5" /></span>}
        <Logo to="/ui-kit" />
        <div className="ml-auto flex items-center gap-1.5 sm:gap-3">
          {!narrow && <span className="rounded-full border border-line px-2.5 py-1 text-xs font-bold">EN · हिं</span>}
          <span className="inline-flex items-center gap-1.5 rounded-full border border-line px-2.5 py-1.5 text-sm font-medium" aria-label={`${credits} credits available`}>
            <Coins className="h-4 w-4 text-warning" aria-hidden />
            <span aria-hidden>{narrow ? credits : `${credits} credits`}</span>
          </span>
          <span className="relative rounded-full p-1.5" aria-hidden><Bell className="h-5 w-5" /><span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-danger" /></span>
          <Avatar name="Ananya Rao" size="sm" />
        </div>
      </div>
      <p className="px-4 py-2 text-xs text-muted">{narrow ? 'Phone (360 px): balance shows as a number' : 'Desktop: balance shows with the word “credits”'}</p>
    </div>
  );
}

export function UiKitPage() {
  useDocumentTitle('UI kit');
  const [modal, setModal] = useState(false);
  const [sw, setSw] = useState(true);
  const [chip, setChip] = useState('ssc-cgl');
  const [tab, setTab] = useState<'one' | 'two' | 'three'>('one');
  const [lang, setLang] = useState('en');

  return (
    <div className="container-page space-y-14 py-10">
      <header className="space-y-3">
        <p className="text-xs font-bold uppercase tracking-[0.14em] text-primary">Internal · Design reference</p>
        <h1 className="text-4xl font-extrabold">PrepMitra UI kit</h1>
        <p className="max-w-2xl text-muted">All shared components with their real styles. Use these instead of one-off styles when building screens. Resize the window to check the phone layout.</p>
        <nav aria-label="UI kit sections" className="flex flex-wrap gap-2 pt-2 text-sm">
          {['colours', 'type', 'buttons', 'forms', 'cards', 'feedback', 'overlays', 'header', 'exam', 'paper'].map((s) => (
            <a key={s} href={`#${s}`} className="rounded-full border border-line bg-card px-3 py-1.5 font-medium capitalize hover:border-primary hover:text-primary">{s}</a>
          ))}
        </nav>
      </header>

      <Section id="colours" title="Colours" note="Saffron for action, peepal green for trust, warm stone for the canvas. No blue. Tokens live in styles/index.css and packages/shared design-tokens.">
        <ul className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
          {COLORS.map((c) => (
            <li key={c.token} className="overflow-hidden rounded-xl border border-line bg-card">
              <div className={cn('flex h-16 items-end p-2 text-xs font-semibold', c.text)} style={{ background: `var(--color-${c.token})` }}>{c.token}</div>
              <p className="px-2 py-1.5 text-xs">{c.name}</p>
            </li>
          ))}
        </ul>
      </Section>

      <Section id="type" title="Typography" note="Bricolage Grotesque for headings, DM Sans for text, Noto Sans Devanagari for Hindi, Kalam only for short handwritten notes.">
        <Card className="space-y-3 p-5">
          <p className="font-display text-4xl font-extrabold">Display · Practice like it’s the real exam</p>
          <h2 className="text-2xl font-bold">Heading 2 · Your 7-day path</h2>
          <h3 className="text-lg font-semibold">Heading 3 · Section-wise performance</h3>
          <p className="max-w-2xl">Body · A fresh paper every time, in the real exam pattern. Your marks are counted by code, then Mitra explains every mistake.</p>
          <p className="text-sm text-muted">Small muted · Submitted 2 Nov 2026 · 17 min 40 s</p>
          <p lang="hi" className="text-lg">हिन्दी · कोई धनराशि 10% वार्षिक चक्रवृद्धि ब्याज पर 3 वर्ष में ₹1,331 हो जाती है।</p>
          <p className="font-hand text-xl text-pen">Handwritten note · Fix seating puzzles first.</p>
        </Card>
      </Section>

      <Section id="buttons" title="Buttons">
        <Card className="space-y-4 p-5">
          <div className="flex flex-wrap items-center gap-3">
            <Button>Primary</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="success">Success</Button>
            <Button variant="danger">Danger</Button>
            <Button variant="link">Link</Button>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <Button size="sm">Small</Button>
            <Button>Medium</Button>
            <Button size="lg">Large</Button>
            <Button size="icon" variant="outline" aria-label="Search"><Search className="h-4 w-4" /></Button>
            <Button loading>Saving</Button>
            <Button disabled>Disabled</Button>
          </div>
        </Card>
      </Section>

      <Section id="forms" title="Form controls" note="Every control has a visible label; errors are announced to screen readers.">
        <Card className="grid gap-4 p-5 md:grid-cols-2">
          <Input label="Mobile number" placeholder="98765 43210" hint="We send a 6-digit code. Demo code: 123456" />
          <Input label="Full name" required error="Enter your full name" />
          <Select label="Highest education" placeholder="Select" options={[{ value: 'g', label: 'Graduate' }, { value: 'pg', label: 'Postgraduate' }]} />
          <LanguageSelector label="Preferred language" value={lang as never} onChange={setLang} />
          <Textarea label="Your answer" placeholder="Type here…" rows={3} />
          <div className="space-y-4">
            <Checkbox label="I agree to the Terms of Use and Privacy Policy" description="Required to continue." />
            <Switch checked={sw} onChange={setSw} label="Exam reminders" description="One notification a day." />
            <div className="flex flex-wrap gap-2" role="group" aria-label="Target exams">
              {['ssc-cgl', 'ibps-po', 'placement'].map((id) => (
                <ChoiceChip key={id} selected={chip === id} onClick={() => setChip(id)}>{id.toUpperCase().replace('-', ' ')}</ChoiceChip>
              ))}
            </div>
          </div>
        </Card>
      </Section>

      <Section id="cards" title="Cards and stats">
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader title="Card with header" description="Cards set off one object; don’t nest them." />
            <CardBody><p className="text-sm text-muted">Body text inside a card.</p></CardBody>
          </Card>
          <StatCard label="Mock tests taken" value={7} icon={<Badge tone="primary">7</Badge>} hint="Last: 29 Oct" />
          <StatCard label="Average score" value="57%" trend={{ value: 18, label: '% vs previous' }} />
        </div>
        <Tabs<'one' | 'two' | 'three'> ariaLabel="Example tabs" value={tab} onChange={setTab} items={[{ value: 'one', label: 'Overview' }, { value: 'two', label: 'Review', count: 15 }, { value: 'three', label: '7-day plan' }]} />
      </Section>

      <Section id="feedback" title="Feedback">
        <div className="flex flex-wrap gap-2">
          {(['neutral', 'primary', 'secondary', 'success', 'warning', 'danger', 'info'] as const).map((t) => <Badge key={t} tone={t}>{t}</Badge>)}
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          <Notice tone="info" title="Info">Answers save on this device as you go.</Notice>
          <Notice tone="success" title="Success">Payment received. 10 credits added.</Notice>
          <Notice tone="warning" title="Warning">5 minutes left. The test submits automatically.</Notice>
          <Notice tone="danger" title="Error">That code is incorrect. Request a new one.</Notice>
        </div>
        <Card className="space-y-4 p-5">
          <ProgressBar value={78} tone="success" label="Accuracy" showValue />
          <ProgressBar value={42} tone="warning" label="Seating puzzles" showValue />
          <div className="flex items-center gap-3 text-sm"><Spinner /> Loading…</div>
          <LoadingSkeleton variant="list" count={2} />
        </Card>
        <Card><EmptyState title="No attempts yet" description="Your attempts and reports will be listed here." /></Card>
      </Section>

      <Section id="overlays" title="Modal and toast" note="Modals become bottom sheets on phones. Toasts confirm what just happened.">
        <div className="flex flex-wrap gap-3">
          <Button onClick={() => setModal(true)}>Open modal</Button>
          <Button variant="outline" onClick={() => toast.success('Profile saved')}>Show success toast</Button>
          <Button variant="outline" onClick={() => toast.error('Unable to reach the server. Check your connection and try again.')}>Show error toast</Button>
        </div>
        <Modal
          open={modal}
          onOpenChange={setModal}
          title="Submit your test?"
          description="You can’t change answers after submitting."
          footer={<><Button variant="outline" onClick={() => setModal(false)}>Keep working</Button><Button onClick={() => setModal(false)}>Submit</Button></>}
        >
          <p className="text-sm">12 answered · 2 marked · 1 not visited</p>
        </Modal>
      </Section>

      <Section id="header" title="Header with credit balance" note="The balance stays visible on phones as a number; tapping it opens Credits & plans.">
        <div className="flex flex-col gap-4">
          <div className="hidden sm:block"><HeaderPreview credits={6} /></div>
          <HeaderPreview narrow credits={6} />
        </div>
      </Section>

      <Section id="exam" title="Exam palette states" note="Same colours as the real CBT palette.">
        <ul className="flex flex-wrap gap-3">
          {PALETTE_STATES.map((p, i) => (
            <li key={p.label} className="flex items-center gap-2 text-sm">
              <span className={cn('flex h-9 w-9 items-center justify-center rounded-lg text-sm font-bold', p.cls)}>{i + 1}</span>{p.label}
            </li>
          ))}
        </ul>
      </Section>

      <Section id="paper" title="Answer sheet & blackboard" note="Paper and red pen for results; chalkboard for Mitra, the AI coach.">
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="space-y-4 rounded-xl border-[1.5px] border-ink bg-ruled p-6">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <PenScore score="27¾" total={35} />
              <Stamp value="84.2" label="Percentile" />
            </div>
            <PenNote>Seating puzzles: draw the grid first.</PenNote>
            <div className="flex items-center gap-2" aria-label="OMR bubbles">{[false, true, false, false].map((f, i) => <Bubble key={i} filled={f} />)}</div>
          </div>
          <MarksLeak title="Where your marks leaked" items={[{ label: 'Skipped (4)', marks: 4, color: 'bg-pen' }, { label: 'Wrong answers (1)', marks: 1, color: 'bg-accent' }, { label: 'Negative marking', marks: 0.25, color: 'bg-[#7E22CE]' }]} />
          <MitraSays>Seating puzzles cost you 4 marks. Let’s fix that today.</MitraSays>
          <div className="rounded-2xl bg-chalkboard p-5"><MitraSays tone="chalk">Shortcut: 1331 = 11³, so the principal is 1000.</MitraSays></div>
          <div className="flex gap-4"><StickyNote color="yellow" tilt={-2} className="flex-1"><b>Sticky note</b><p className="text-sm">Step cards</p></StickyNote><StickyNote color="green" tilt={2} className="flex-1"><b>Green</b><p className="text-sm">Second colour</p></StickyNote></div>
          <div className="flex items-center gap-4"><Mitra size={64} label="Mitra, the AI coach" /><p className="text-sm text-muted">Mitra mascot, 64 px</p></div>
        </div>
      </Section>
    </div>
  );
}
