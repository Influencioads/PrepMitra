import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import type { ExamCategory } from '@prepmitra/shared';
import { EXAM_CATEGORIES } from '@prepmitra/shared';
import { AppIcon, ButtonLink, HandEyebrow, MarksLeak, PenNote, StickyNote } from '@/components/ui';
import { PricingCards } from '@/components/marketing/PricingCards';
import { AnswerSheetHero, PanelRoom, PrepPathPreview } from '@/components/marketing/PaperVisuals';
import { useAuthStore } from '@/store';
import { examService, interviewService } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useContentT } from '@/i18n/content';
import { interviewsEnabled, isCategoryOpen, openFirst } from '@/config/launch';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { homeMessages } from '@/i18n/messages/home';
import { landingMessages } from '@/i18n/messages/landing';
import { catalogMessages, categoryText } from '@/i18n/messages/catalog';
import { layoutMessages } from '@/i18n/messages/layout';

type LandingKey = keyof typeof landingMessages.en;
type HomeKey = keyof typeof homeMessages.en;

/** Index-card tab colours per category. Warm and green only — no blue. */
const CATEGORY_TAB: Record<ExamCategory, string> = {
  government: 'bg-primary-soft text-primary',
  banking: 'bg-secondary-soft text-secondary',
  railway: 'bg-sticky-yellow text-[#92400E]',
  'civil-services': 'bg-sticky-purple text-[#7E22CE]',
  'higher-education': 'bg-[#FCE7EC] text-[#9F1239]',
  'campus-placement': 'bg-sticky-green text-[#3F6212]',
};

const LOOP: { title: HomeKey; body: HomeKey; color: 'yellow' | 'saffron' | 'green' | 'purple'; tilt: number }[] = [
  { title: 'loop1Title', body: 'loop1Body', color: 'yellow', tilt: -2 },
  { title: 'loop2Title', body: 'loop2Body', color: 'saffron', tilt: 1.5 },
  { title: 'loop3Title', body: 'loop3Body', color: 'green', tilt: -1 },
  { title: 'loop4Title', body: 'loop4Body', color: 'purple', tilt: 2 },
];

const FAQS: { q: LandingKey; a: LandingKey }[] = [1, 2, 3, 4, 5, 6].map((n) => ({ q: `faq${n}q` as LandingKey, a: `faq${n}a` as LandingKey }));

/** Filled-bubble call to action: the first OMR bubble a student fills. */
function BubbleCta({ to, children, tone = 'saffron', className }: { to: string; children: string; tone?: 'saffron' | 'marigold'; className?: string }) {
  return (
    <Link
      to={to}
      className={cn(
        'group inline-flex min-h-16 items-center gap-3 rounded-[20px] py-2.5 pl-2.5 pr-6 text-base font-extrabold transition-transform hover:-translate-y-0.5 sm:text-lg',
        tone === 'saffron' ? 'bg-primary text-white shadow-[0_6px_0_#8A2E07]' : 'bg-accent text-chalk-deep shadow-[0_6px_0_#A6370A]',
        className,
      )}
    >
      <span className={cn('flex h-11 w-11 shrink-0 items-center justify-center rounded-full border-[3px]', tone === 'saffron' ? 'border-white' : 'border-chalk-deep')} aria-hidden>
        <span className={cn('h-6 w-6 scale-75 rounded-full transition-transform group-hover:scale-100', tone === 'saffron' ? 'bg-white' : 'bg-chalk-deep')} />
      </span>
      {children}
    </Link>
  );
}

export function LandingPage() {
  useDocumentTitle('');
  const t = useT(homeMessages);
  const tf = useT(landingMessages);
  const tc = useT(catalogMessages);
  const tl = useT(layoutMessages);
  const user = useAuthStore((s) => s.session?.user);
  const startHref = user ? '/exams/general-aptitude' : '/signup';
  const ct = useContentT();
  // Live catalog (API or demo data): the ribbon, category counts and role chips only list what exists.
  const exams = useAsync(() => examService.list({ sort: 'popular' }), []).data ?? [];
  const roles = useAsync(() => interviewService.listRoles(), []).data ?? [];
  const popular = openFirst(exams).slice(0, 10);
  const categories = EXAM_CATEGORIES.map((c) => ({ ...c, count: exams.filter((e) => e.category === c.id).length }))
    .filter((c) => c.count > 0)
    .sort((a, b) => Number(isCategoryOpen(b.id)) - Number(isCategoryOpen(a.id)));

  return (
    <div className="bg-notebook [--margin-x:14px] sm:[--margin-x:28px] lg:[--margin-x:48px]">
      {/* ---------------- Hero ---------------- */}
      <section className="container-page grid items-center gap-12 pb-16 pt-10 lg:grid-cols-[1.1fr_1fr] lg:gap-8 lg:pb-20 lg:pt-14">
        <div className="min-w-0">
          <p className="font-hand text-lg text-secondary sm:text-xl">{t('heroFor')} —</p>
          <h1 className="mt-3 text-[2.7rem] font-extrabold leading-[1] tracking-tight sm:text-6xl lg:text-[4.6rem]">
            {t('heroLine1')}
            <br />
            {t('heroLine2')}
            <br />
            <span className="mt-3 inline-block -rotate-3 rounded-[50%] border-4 border-pen px-5 pb-2 text-primary sm:-ml-4 sm:px-7">{t('heroLine3')}</span>
          </h1>
          <p className="mt-7 max-w-xl text-lg leading-relaxed text-muted">{t('heroBody')}</p>
          <div className="mt-8 flex flex-col items-start gap-4 sm:flex-row sm:items-center sm:gap-6">
            <BubbleCta to={startHref}>{t('heroCta')}</BubbleCta>
            <a href="#how-it-works" className="font-bold text-ink underline decoration-2 underline-offset-4 hover:text-primary">{t('heroSecondary')} →</a>
          </div>
          <p className="mt-5 font-hand text-base text-muted">{t('heroNote')}</p>
        </div>
        <AnswerSheetHero />
      </section>

      {/* ---------------- Exam ribbon ---------------- */}
      <nav aria-label={t('examsRibbon')} className="bg-chalkboard">
        <div className="container-page flex items-center gap-x-6 gap-y-2 overflow-x-auto py-5 scrollbar-thin">
          {popular.map((e, i) => (
            <span key={e.id} className="flex shrink-0 items-center gap-6">
              {i > 0 && <span className="text-accent" aria-hidden>✦</span>}
              <Link to={`/exams/${e.id}`} className="font-hand text-xl text-chalk-text transition-colors hover:text-marigold sm:text-2xl">{ct(e.shortTitle)}</Link>
            </span>
          ))}
        </div>
      </nav>

      {/* ---------------- The loop ---------------- */}
      <section id="how-it-works" className="container-page scroll-mt-20 py-16 lg:py-24">
        <HandEyebrow>{t('loopEyebrow')}</HandEyebrow>
        <h2 className="mt-1 text-4xl font-extrabold sm:text-5xl">{t('loopTitle')}</h2>
        <ol className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-4 lg:gap-6">
          {LOOP.map((s, i) => (
            <li key={s.title}>
              <StickyNote color={s.color} tilt={s.tilt} className="h-full">
                <p className="font-hand text-4xl font-bold text-primary">{i + 1}</p>
                <h3 className="mt-1 text-xl font-bold sm:text-2xl">{t(s.title)}</h3>
                <p className="mt-2 leading-relaxed text-ink/80">{t(s.body)}</p>
              </StickyNote>
            </li>
          ))}
        </ol>
      </section>

      {/* ---------------- Marks leak ---------------- */}
      <section id="features" className="container-page scroll-mt-20 pb-16 lg:pb-24">
        <div className="grid items-center gap-10 rounded-[28px] border-2 border-ink bg-card p-6 shadow-hard sm:p-10 lg:grid-cols-[1.1fr_1fr] lg:gap-14 lg:p-14">
          <div className="min-w-0">
            <HandEyebrow tone="pen">{t('leakEyebrow')}</HandEyebrow>
            <h2 className="mt-1 text-3xl font-extrabold leading-tight sm:text-[2.6rem]">
              {t('leakTitle1')}
              <br />
              {t('leakTitle2')} <span className="text-pen">{t('leakTitle3')}</span>
            </h2>
            <p className="mt-5 text-lg leading-relaxed text-muted">{t('leakBody')}</p>
          </div>
          <MarksLeak
            className="border-dashed border-line-strong bg-paper"
            title={t('leakCardTitle')}
            items={[
              { label: t('leak1'), marks: 4, color: 'bg-pen' },
              { label: t('leak2'), marks: 2, color: 'bg-accent' },
              { label: t('leak3'), marks: 1.25, color: 'bg-[#7E22CE]' },
            ]}
            note={<PenNote>{t('leakNote')}</PenNote>}
          />
        </div>
      </section>

      {/* ---------------- Categories as index cards ---------------- */}
      <section className="container-page pb-16 lg:pb-24">
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <HandEyebrow tone="green">{t('catEyebrow')}</HandEyebrow>
            <h2 className="mt-1 text-4xl font-extrabold sm:text-5xl">{t('catTitle')}</h2>
          </div>
          <ButtonLink to="/exams" variant="outline" rightIcon={<ArrowRight className="h-4 w-4" />} className="self-start border-ink sm:self-auto">{t('catAll')}</ButtonLink>
        </div>
        <div className="mt-10 grid gap-x-5 gap-y-8 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map(({ count, ...c }) => {
            return (
              <Link key={c.id} to={`/exams?category=${c.id}`} className="group relative block rounded-[4px_16px_16px_16px] pt-5 focus-visible:outline-2">
                <span className={cn('absolute left-0 top-0 inline-flex h-7 items-center gap-1.5 rounded-t-xl px-3 text-xs font-bold', CATEGORY_TAB[c.id])}>
                  <AppIcon name={c.icon} className="h-3.5 w-3.5" />
                  {!isCategoryOpen(c.id) ? tc('comingSoon') : count === 1 ? t('mockOne') : t('mocksMany', { count })}
                </span>
                <article className="h-full rounded-[0_16px_16px_16px] border-[1.5px] border-ink bg-ruled p-6 shadow-hard-sm transition-transform duration-200 group-hover:-translate-y-1">
                  <h3 className="text-xl font-bold">{categoryText(tc, c.id).label}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted">{categoryText(tc, c.id).description}</p>
                  <p className="mt-4 flex items-center justify-between gap-3 border-t-2 border-dashed border-line-strong pt-3 text-sm">
                    <span className="min-w-0 font-hand text-base text-ink">{c.examples.split(' · ').map(ct).join(' · ')}</span>
                    <ArrowRight className="h-4 w-4 shrink-0 text-primary transition-transform group-hover:translate-x-1" aria-hidden />
                  </p>
                </article>
              </Link>
            );
          })}
        </div>
      </section>

      {/* ---------------- Path + Mitra ---------------- */}
      <section className="container-page grid gap-12 pb-16 lg:grid-cols-2 lg:gap-10 lg:pb-24">
        <div className="min-w-0">
          <HandEyebrow tone="green">{t('pathEyebrow')}</HandEyebrow>
          <h2 className="mt-1 text-3xl font-extrabold leading-tight sm:text-[2.6rem]">{t('pathTitle1')}<br />{t('pathTitle2')}</h2>
          <PrepPathPreview startHref={startHref} className="mt-8" />
        </div>
        <div className="min-w-0">
          <HandEyebrow tone="green">{t('mitraEyebrow')}</HandEyebrow>
          <h2 className="mt-1 text-3xl font-extrabold leading-tight sm:text-[2.6rem]">{t('mitraTitle1')}<br />{t('mitraTitle2')}</h2>
          <div className="mt-8 flex min-h-[360px] flex-col gap-4 rounded-3xl bg-chalkboard p-6 font-hand text-chalk-text shadow-[0_10px_0_var(--color-wood)] sm:p-7">
            <p className="self-end rounded-[16px_16px_4px_16px] bg-primary-soft px-4 py-2 text-lg text-ink">{t('mitraQ')}</p>
            <p className="text-2xl font-bold text-marigold">{t('mitraA1')}</p>
            <p className="text-lg leading-relaxed sm:text-xl">{t('mitraA2')}<br />{t('mitraA3')}</p>
            <p className="rounded-xl border-[1.5px] border-dashed border-white/45 px-4 py-2.5 text-lg"><b className="text-accent">{t('mitraShortcutLabel')}</b> {t('mitraShortcut')}</p>
            <p className="mt-auto font-sans text-xs text-white/60">{t('mitraFootnote')}</p>
          </div>
        </div>
      </section>

      {/* ---------------- Interview panel ---------------- */}
      {interviewsEnabled() && <section className="bg-panel-room py-16 text-chalk-text lg:py-24">
        <div className="container-page grid items-center gap-12 lg:grid-cols-2">
          <div className="min-w-0">
            <HandEyebrow tone="accent">{t('intEyebrow')}</HandEyebrow>
            <h2 className="mt-1 text-3xl font-extrabold leading-tight text-chalk-text sm:text-[2.75rem]">{t('intTitle1')}<br />{t('intTitle2')}</h2>
            <p className="mt-5 max-w-xl text-lg leading-relaxed text-white/80">{t('intBody')}</p>
            <div className="mt-6 flex flex-wrap gap-2">
              {roles.map((r) => (
                <Link key={r.id} to={`/interviews/${r.id}`} className="inline-flex items-center gap-1.5 rounded-full border border-white/25 px-3 py-1.5 text-sm text-white transition-colors hover:bg-white hover:text-chalk-deep">
                  <AppIcon name={r.icon} className="h-3.5 w-3.5" />
                  {ct(r.shortTitle)}
                </Link>
              ))}
            </div>
            <ButtonLink to="/interviews" size="lg" className="mt-8 bg-accent text-chalk-deep hover:bg-[#F7A04A]">{t('intCta')}</ButtonLink>
          </div>
          <PanelRoom />
        </div>
      </section>}

      {/* ---------------- Pricing as admit cards ---------------- */}
      <section id="pricing" className="container-page scroll-mt-20 py-16 lg:py-24">
        <HandEyebrow>{t('priceEyebrow')}</HandEyebrow>
        <h2 className="mt-1 text-4xl font-extrabold sm:text-5xl">{t('priceTitle')}</h2>
        <p className="mt-3 text-lg text-muted">{t('priceBody')}</p>
        <div className="mt-12">
          <PricingCards ctaHref={(p) => (user ? '/subscription' : p.id === 'free' ? '/signup' : `/signup?plan=${p.id}`)} />
        </div>
        <p className="mt-6 font-hand text-base text-muted">{t('priceRefund')}</p>
      </section>

      {/* ---------------- FAQ in the margin ---------------- */}
      <section id="faq" className="container-page grid scroll-mt-20 gap-10 pb-16 lg:grid-cols-[0.75fr_1.25fr] lg:pb-24">
        <div>
          <HandEyebrow>{t('faqEyebrow')}</HandEyebrow>
          <h2 className="mt-1 text-4xl font-extrabold leading-tight sm:text-5xl">{t('faqTitle')}</h2>
        </div>
        <div>
          {FAQS.map((f, i) => (
            <details key={f.q} open={i === 0} className="group border-b-[1.5px] border-ink py-5 [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer list-none items-center justify-between gap-4 font-display text-lg font-bold sm:text-xl">
                {tf(f.q)}
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-[1.5px] border-ink text-lg leading-none transition-transform group-open:rotate-45" aria-hidden>+</span>
              </summary>
              <p className="mt-3 font-hand text-lg leading-relaxed text-ink/80">{tf(f.a)}</p>
            </details>
          ))}
        </div>
      </section>

      {/* ---------------- Final CTA ---------------- */}
      <section className="container-page pb-16 lg:pb-20">
        <div className="flex flex-col items-start justify-between gap-8 rounded-[28px] bg-chalkboard px-6 py-10 shadow-[0_12px_0_var(--color-wood)] sm:px-12 sm:py-14 lg:flex-row lg:items-center">
          <div className="min-w-0">
            <h2 className="font-hand text-4xl font-bold leading-tight text-chalk-text sm:text-5xl">
              {t('ctaTitle1')}
              <br />
              <span className="text-marigold">{t('ctaTitle2')}</span>
            </h2>
            <p className="mt-3 text-lg text-white/80">{t('ctaBody')}</p>
          </div>
          <BubbleCta to={startHref} tone="marigold" className="shrink-0">{t('ctaBubble')}</BubbleCta>
        </div>
        <p className="mt-6 text-center text-xs text-muted">{tl('affiliation')}</p>
      </section>
    </div>
  );
}
