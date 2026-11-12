import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, BookOpenCheck, CalendarDays, CircleMinus, Gift, Lock, Plus } from 'lucide-react';
import type { ExamCategory } from '@prepmitra/shared';
import { EXAM_CATEGORIES } from '@prepmitra/shared';
import { AppIcon, ButtonLink, HandEyebrow, MarksLeak, PenNote, StickyNote } from '@/components/ui';
import { PricingCards } from '@/components/marketing/PricingCards';
import { PanelRoom, PrepPathPreview } from '@/components/marketing/PaperVisuals';
import { ExamMarquee } from '@/components/marketing/ExamMarquee';
import { CutoffMeter } from '@/components/marketing/CutoffMeter';
import { ExamDial } from '@/components/marketing/ExamDial';
import { DrawnArrow, FloatingBubbles, Magnetic, PenUnderline, TiltCard, TypingDots, WordsReveal } from '@/components/marketing/HomeFx';
import { AnimatePresence, CountUp, Reveal, motion, useScroll, useSpring } from '@/components/motion/landing';
import { usePlans } from '@/hooks/usePlans';
import { useAuthStore } from '@/store';
import { examService, interviewService } from '@/services';
import { useAsync } from '@/hooks/useAsync';
import { useContentT } from '@/i18n/content';
import { interviewsEnabled, isCategoryOpen, isExamOpen, openExamCategories, openFirst } from '@/config/launch';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { cn } from '@/utils/cn';
import { useT } from '@/i18n';
import { homeMessages } from '@/i18n/messages/home';
import { catalogMessages, categoryText } from '@/i18n/messages/catalog';
import { layoutMessages } from '@/i18n/messages/layout';

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

const CHAT = { hidden: { opacity: 0, y: 10 }, show: { opacity: 1, y: 0, transition: { duration: 0.35, ease: [0.22, 1, 0.36, 1] as const } } };

const FAQS: { q: HomeKey; a: HomeKey }[] = [1, 2, 3, 4, 5, 6].map((n) => ({ q: `faq${n}q` as HomeKey, a: `faq${n}a` as HomeKey }));

/** Filled-bubble call to action: the first OMR bubble a student fills. */
const MotionLink = motion.create(Link);

function BubbleCta({ to, children, tone = 'saffron', className }: { to: string; children: string; tone?: 'saffron' | 'marigold'; className?: string }) {
  return (
    <MotionLink
      whileTap={{ scale: 0.97, y: 2 }}
      to={to}
      className={cn(
        'group relative inline-flex min-h-16 items-center gap-3 overflow-hidden rounded-[20px] py-2.5 pl-2.5 pr-6 text-base font-extrabold transition-transform hover:-translate-y-0.5 sm:text-lg',
        tone === 'saffron' ? 'bg-primary text-white shadow-[0_6px_0_#8A2E07]' : 'bg-accent text-chalk-deep shadow-[0_6px_0_#A6370A]',
        className,
      )}
    >
      <motion.span
        aria-hidden
        className="pointer-events-none absolute inset-y-0 -left-1/3 w-1/4 skew-x-[-20deg] bg-white/25"
        animate={{ x: ['0%', '600%'] }}
        transition={{ duration: 1.1, repeat: Infinity, repeatDelay: 3.2, ease: 'easeInOut' }}
      />
      <span className={cn('relative flex h-11 w-11 shrink-0 items-center justify-center rounded-full border-[3px]', tone === 'saffron' ? 'border-white' : 'border-chalk-deep')} aria-hidden>
        <span className={cn('h-6 w-6 scale-75 rounded-full transition-transform group-hover:scale-100', tone === 'saffron' ? 'bg-white' : 'bg-chalk-deep')} />
      </span>
      <span className="relative">{children}</span>
    </MotionLink>
  );
}

/** Thin saffron bar at the top that fills as you scroll the page. */
function ScrollProgress() {
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, { stiffness: 140, damping: 30, mass: 0.3 });
  return <motion.div className="fixed inset-x-0 top-0 z-[60] h-[3px] origin-left bg-primary" style={{ scaleX }} aria-hidden />;
}

const HERO = (delay: number) => ({ initial: { opacity: 0, y: 16 }, animate: { opacity: 1, y: 0 }, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] as const, delay } });

/** FAQ row that opens and closes smoothly (button + region, keyboard friendly). The open row gets a saffron margin bar. */
function FaqItem({ q, a, open, onToggle, id, index }: { q: string; a: string; open: boolean; onToggle: () => void; id: string; index: number }) {
  return (
    <div className={cn('relative rounded-2xl transition-colors duration-300', open ? 'bg-card shadow-hard-sm ring-[1.5px] ring-ink' : 'hover:bg-card/60')}>
      {open && <motion.span layoutId="faq-bar" className="absolute inset-y-4 left-0 w-1 rounded-full bg-primary" transition={{ type: 'spring', stiffness: 400, damping: 34 }} aria-hidden />}
      <h3>
        <button
          type="button"
          onClick={onToggle}
          aria-expanded={open}
          aria-controls={`${id}-a`}
          className="flex w-full items-center gap-4 px-5 py-5 text-left font-display text-lg font-bold sm:text-xl"
        >
          <span className={cn('font-hand text-base tabular-nums transition-colors', open ? 'text-primary' : 'text-subtle')} aria-hidden>{String(index + 1).padStart(2, '0')}</span>
          <span className="flex-1">{q}</span>
          <motion.span
            animate={{ rotate: open ? 45 : 0, backgroundColor: open ? 'var(--color-primary)' : 'rgba(0,0,0,0)', color: open ? '#fff' : 'var(--color-ink)' }}
            transition={{ duration: 0.2 }}
            className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-[1.5px] border-ink"
            aria-hidden
          >
            <Plus className="h-4 w-4" />
          </motion.span>
        </button>
      </h3>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            id={`${id}-a`}
            role="region"
            key="a"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
            className="overflow-hidden"
          >
            <p className="px-5 pb-5 pl-[3.6rem] font-hand text-lg leading-relaxed text-ink/80">{a}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

const STATS = [
  { Icon: BookOpenCheck, tile: 'bg-primary-soft text-primary', blob: 'bg-primary-soft', num: 'text-primary' },
  { Icon: CircleMinus, tile: 'bg-[#FCE7EC] text-pen', blob: 'bg-[#FCE7EC]', num: 'text-pen' },
  { Icon: CalendarDays, tile: 'bg-secondary-soft text-secondary', blob: 'bg-secondary-soft', num: 'text-secondary' },
  { Icon: Gift, tile: 'bg-sticky-yellow text-[#92400E]', blob: 'bg-sticky-yellow', num: 'text-[#92400E]' },
] as const;

export function LandingPage() {
  useDocumentTitle('');
  const t = useT(homeMessages);
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
  // Launch mode: the open category gets a featured card, the rest a compact "coming soon" row.
  const openCats = categories.filter((c) => isCategoryOpen(c.id));
  const soonCats = categories.filter((c) => !isCategoryOpen(c.id));
  const launchFocus = soonCats.length > 0 && openCats.length > 0;
  const bankingOnly = (() => {
    const open = openExamCategories();
    return open !== 'all' && open.length === 1 && open[0] === 'banking';
  })();
  const { plans } = usePlans();
  const [faqOpen, setFaqOpen] = useState(0);
  const openMockCount = exams.filter((e) => isExamOpen(e)).length;
  const dialExams = openFirst(exams.filter((e) => isExamOpen(e) && !e.isFree));

  return (
    <div className="bg-notebook [--margin-x:14px] sm:[--margin-x:28px] lg:[--margin-x:48px]">
      <ScrollProgress />
      {/* ---------------- Hero: the turn-the-dial exam picker, with the headline on top ---------------- */}
      <section className="pb-2">
        <ExamDial
          exams={dialExams}
          allHref="/exams?category=banking"
          tall
          className="rounded-none"
          heading={
            <>
              <motion.p {...HERO(0)} className="font-hand text-lg text-marigold sm:text-xl">{bankingOnly ? t('heroForBanking') : t('heroFor')} —</motion.p>
              <h1 className="mx-auto mt-2 max-w-4xl text-balance font-display text-[2.1rem] font-extrabold leading-[1.05] tracking-tight text-chalk-text sm:text-6xl">
                <WordsReveal text={`${t('heroLine1')} ${t('heroLine2')}`} delay={0.1} />{' '}
                <motion.span
                  initial={{ opacity: 0, scale: 0.85, rotate: -8 }}
                  animate={{ opacity: 1, scale: 1, rotate: -3 }}
                  transition={{ type: 'spring', stiffness: 260, damping: 16, delay: 0.55 }}
                  className="relative inline-block px-3 text-marigold sm:px-5"
                >
                  {t('heroLine3')}
                  <svg viewBox="0 0 300 100" preserveAspectRatio="none" className="pointer-events-none absolute -inset-1 h-[calc(100%+8px)] w-[calc(100%+8px)] overflow-visible text-marigold" aria-hidden>
                    <motion.path
                      d="M160 8 C 255 6, 296 28, 294 52 C 292 80, 222 96, 146 94 C 66 92, 6 80, 8 50 C 10 22, 74 6, 170 12"
                      fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" vectorEffect="non-scaling-stroke"
                      initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 0.8, ease: 'easeInOut', delay: 0.85 }}
                    />
                  </svg>
                </motion.span>
              </h1>
            </>
          }
        />
      </section>

      {/* ---------------- Exam ribbon ---------------- */}
      <div className="overflow-hidden py-4">
        <div className="-rotate-[1.2deg] scale-x-[1.04] shadow-[0_10px_0_rgba(28,35,33,0.08)]">
          <ExamMarquee exams={popular.filter((e) => isExamOpen(e))} label={t('examsRibbon')} />
        </div>
      </div>

      {/* ---------------- Numbers strip (true product facts only): one slim line ---------------- */}
      <section aria-label={t('statsLabel')} className="container-page pt-10">
        <dl className="grid grid-cols-2 gap-y-6 rounded-2xl border-[1.5px] border-ink bg-card px-5 py-5 shadow-hard-sm sm:px-6 lg:grid-cols-4 lg:divide-x-[1.5px] lg:divide-dashed lg:divide-line-strong lg:py-6">
          {[
            { to: openMockCount, decimals: 0, label: t('stat1') },
            { to: 0.25, decimals: 2, label: t('stat2') },
            { to: 7, decimals: 0, label: t('stat3') },
            { to: 1, decimals: 0, label: t('stat4') },
          ].map((stat, i) => {
            const look = STATS[i]!;
            return (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.6 }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1], delay: i * 0.08 }}
                className="group flex items-center gap-3 lg:justify-center lg:px-4"
              >
                <span className={cn('flex h-11 w-11 shrink-0 items-center justify-center rounded-xl transition-transform duration-300 group-hover:-rotate-6 group-hover:scale-110', look.tile)} aria-hidden>
                  <look.Icon className="h-5 w-5" />
                </span>
                <div className="flex min-w-0 flex-col-reverse">
                  <dt className="text-xs leading-snug text-muted sm:text-sm">{stat.label}</dt>
                  <dd className={cn('font-display text-2xl font-extrabold tabular-nums leading-tight tracking-tight sm:text-3xl', look.num)}>
                    <CountUp to={stat.to} decimals={stat.decimals} />
                  </dd>
                </div>
              </motion.div>
            );
          })}
        </dl>
      </section>

      {/* ---------------- The loop ---------------- */}
      <section id="how-it-works" className="container-page scroll-mt-20 py-16 lg:py-24">
        <Reveal>
          <HandEyebrow>{t('loopEyebrow')}</HandEyebrow>
        </Reveal>
        <h2 className="mt-1 text-4xl font-extrabold sm:text-5xl">
          <span className="relative inline-block">
            <WordsReveal text={t('loopTitle')} inView />
            <PenUnderline delay={0.5} />
          </span>
        </h2>
        <ol className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-4 lg:gap-6">
          {LOOP.map((s, i) => (
            // Sticky notes land one by one, settling at their tilt; hovering straightens and lifts one.
            <motion.li
              key={s.title}
              className="relative"
              initial={{ opacity: 0, y: 28, rotate: 0 }}
              whileInView={{ opacity: 1, y: 0, rotate: s.tilt }}
              whileHover={{ rotate: 0, y: -6, transition: { duration: 0.2 } }}
              viewport={{ once: true, amount: 0.4 }}
              transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1], delay: i * 0.1 }}
            >
              {i < LOOP.length - 1 && <DrawnArrow className="absolute -right-10 top-2 z-10 hidden h-9 w-16 lg:block" delay={0.5 + i * 0.15} />}
              <StickyNote color={s.color} className="relative h-full">
                {/* tape */}
                <span className="absolute -top-3 left-1/2 h-6 w-20 -translate-x-1/2 -rotate-2 bg-white/60 shadow-sm" aria-hidden />
                <span className="relative flex h-11 w-11 items-center justify-center rounded-full border-2 border-ink" aria-hidden>
                  <motion.span
                    className="absolute inset-[3px] rounded-full bg-ink"
                    initial={{ scale: 0 }}
                    whileInView={{ scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ type: 'spring', stiffness: 400, damping: 18, delay: 0.35 + i * 0.12 }}
                  />
                  <span className="relative font-display text-lg font-extrabold text-white">{i + 1}</span>
                </span>
                <h3 className="mt-3 text-xl font-bold sm:text-2xl">{t(s.title)}</h3>
                <p className="mt-2 leading-relaxed text-ink/80">{t(s.body)}</p>
              </StickyNote>
            </motion.li>
          ))}
        </ol>
      </section>

      {/* ---------------- Marks leak ---------------- */}
      <section id="features" className="container-page scroll-mt-20 pb-16 lg:pb-24">
        <Reveal className="relative grid items-center gap-10 overflow-hidden rounded-[28px] border-2 border-ink bg-card bg-[radial-gradient(circle,rgba(28,35,33,0.07)_1px,transparent_1px)] p-6 shadow-hard [background-size:18px_18px] sm:p-10 lg:grid-cols-[1.1fr_1fr] lg:gap-14 lg:p-14">
          <span className="pointer-events-none absolute -left-16 -top-16 h-56 w-56 rounded-full bg-pen/10 blur-3xl" aria-hidden />
          <div className="min-w-0">
            <HandEyebrow tone="pen">{t('leakEyebrow')}</HandEyebrow>
            <h2 className="mt-1 text-3xl font-extrabold leading-tight sm:text-[2.6rem]">
              {t('leakTitle1')}
              <br />
              {t('leakTitle2')}{' '}
              <span className="relative inline-block text-pen">
                {t('leakTitle3')}
                <PenUnderline delay={0.4} />
              </span>
            </h2>
            <p className="mt-5 text-lg leading-relaxed text-muted">{t('leakBody')}</p>
          </div>
          <TiltCard max={4} className="relative">
          <MarksLeak
            className="border-dashed border-line-strong bg-paper"
            title={t('leakCardTitle')}
            items={[
              { label: t('leak1'), marks: 4, color: 'bg-pen' },
              { label: t('leak2'), marks: 2, color: 'bg-accent' },
              { label: t('leak3'), marks: 1.25, color: 'bg-[#7E22CE]' },
            ]}
            note={<PenNote>{t('leakNote')}</PenNote>}
            animated
          />
          </TiltCard>
        </Reveal>
      </section>

      {/* ---------------- Cut-off meter (interactive, sample numbers) ---------------- */}
      <CutoffMeter />

      {/* ---------------- Categories as index cards ---------------- */}
      <section className="container-page py-16 lg:py-24">
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <Reveal><HandEyebrow tone="green">{t('catEyebrow')}</HandEyebrow></Reveal>
            <h2 className="mt-1 text-4xl font-extrabold sm:text-5xl"><WordsReveal text={t('catTitle')} inView /></h2>
          </div>
          <ButtonLink to="/exams" variant="outline" rightIcon={<ArrowRight className="h-4 w-4" />} className="self-start border-ink sm:self-auto">{t('catAll')}</ButtonLink>
        </div>
        {launchFocus ? (
          <>
            <Reveal className="mt-8">
              <p className="font-hand text-lg text-muted">{t('catSoonTitle')} — {t('catSoonNote')}</p>
            </Reveal>
            <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
              {soonCats.map((c, i) => (
                <motion.div key={c.id} initial={{ opacity: 0, y: 12 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.35, delay: i * 0.06 }}>
                  <Link to={`/exams?category=${c.id}`} className="group relative flex h-full flex-col gap-2 rounded-2xl border border-dashed border-line-strong bg-card/70 p-4 transition-all duration-200 hover:-translate-y-1 hover:border-solid hover:border-ink hover:shadow-hard-sm">
                    <span className="flex items-center justify-between">
                      <span className={cn('inline-flex w-fit items-center gap-1.5 rounded-full px-2 py-0.5 text-[11px] font-bold', CATEGORY_TAB[c.id])}>
                        <AppIcon name={c.icon} className="h-3 w-3" />
                        {tc('comingSoon')}
                      </span>
                      <Lock className="h-3.5 w-3.5 text-subtle transition-transform group-hover:rotate-12" aria-hidden />
                    </span>
                    <span className="text-sm font-bold leading-snug">{categoryText(tc, c.id).label}</span>
                    <span className="font-hand text-sm text-muted">{c.examples.split(' · ').map(ct).join(' · ')}</span>
                  </Link>
                </motion.div>
              ))}
            </div>
          </>
        ) : (
        <>
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
        </>
        )}
      </section>

      {/* ---------------- Path + Mitra ---------------- */}
      <section className="container-page grid gap-12 pb-16 lg:grid-cols-2 lg:gap-10 lg:pb-24">
        <Reveal className="min-w-0">
          <HandEyebrow tone="green">{t('pathEyebrow')}</HandEyebrow>
          <h2 className="mt-1 text-3xl font-extrabold leading-tight sm:text-[2.6rem]">{t('pathTitle1')}<br />{t('pathTitle2')}</h2>
          <TiltCard max={4} className="mt-8"><PrepPathPreview startHref={startHref} /></TiltCard>
        </Reveal>
        <Reveal className="min-w-0" delay={0.1}>
          <HandEyebrow tone="green">{t('mitraEyebrow')}</HandEyebrow>
          <h2 className="mt-1 text-3xl font-extrabold leading-tight sm:text-[2.6rem]">{t('mitraTitle1')}<br />{t('mitraTitle2')}</h2>
          {/* The question arrives, then Mitra's answer appears line by line. */}
          <motion.div
            className="relative mt-8 flex min-h-[380px] flex-col gap-4 overflow-hidden rounded-3xl bg-chalkboard p-6 font-hand text-chalk-text shadow-[0_10px_0_var(--color-wood)] sm:p-7"
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.4 }}
            variants={{ show: { transition: { staggerChildren: 0.35, delayChildren: 1.1 } } }}
          >
            <span className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top_left,rgba(255,255,255,0.10),transparent_55%)]" aria-hidden />
            <div className="relative flex items-center gap-2 border-b border-white/10 pb-3 font-sans text-xs font-bold uppercase tracking-[0.14em] text-white/60">
              <span className="flex h-7 w-7 items-center justify-center rounded-full bg-accent text-sm text-chalk-deep" aria-hidden>☺</span>
              Mitra · AI
              <motion.span
                className="ml-auto"
                variants={{ hidden: { opacity: 1 }, show: { opacity: 0, transition: { delay: 1.0, duration: 0.2 } } }}
              >
                <TypingDots />
              </motion.span>
            </div>
            <motion.p variants={CHAT} className="relative self-end rounded-[16px_16px_4px_16px] bg-primary-soft px-4 py-2 text-lg text-ink">{t('mitraQ')}</motion.p>
            <motion.p variants={CHAT} className="text-2xl font-bold text-marigold">{t('mitraA1')}</motion.p>
            <motion.p variants={CHAT} className="text-lg leading-relaxed sm:text-xl">{t('mitraA2')}<br />{t('mitraA3')}</motion.p>
            <motion.p variants={CHAT} className="rounded-xl border-[1.5px] border-dashed border-white/45 px-4 py-2.5 text-lg"><b className="text-accent">{t('mitraShortcutLabel')}</b> {t('mitraShortcut')}</motion.p>
            <motion.p variants={CHAT} className="mt-auto font-sans text-xs text-white/60">{t('mitraFootnote')}</motion.p>
          </motion.div>
        </Reveal>
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
      <section id="pricing" className="relative container-page scroll-mt-20 py-16 lg:py-24">
        <span className="pointer-events-none absolute right-0 top-24 -z-10 h-72 w-72 rounded-full bg-primary/10 blur-3xl" aria-hidden />
        <Reveal><HandEyebrow>{t('priceEyebrow')}</HandEyebrow></Reveal>
        <h2 className="mt-1 text-4xl font-extrabold sm:text-5xl"><WordsReveal text={t('priceTitle')} inView /></h2>
        <Reveal delay={0.15}><p className="mt-3 text-lg text-muted">{interviewsEnabled() ? t('priceBody') : t('priceBodyExams')}</p></Reveal>
        <div className="mt-12">
          <PricingCards
            inView
            plans={plans}
            ctaHref={(p) => (user ? (p.id === 'free' ? '/exams/general-aptitude' : `/subscription?plan=${p.id}`) : p.id === 'free' ? '/signup' : `/signup?plan=${p.id}`)}
          />
        </div>
        <p className="mt-6 font-hand text-base text-muted">{t('priceRefund')}</p>
      </section>

      {/* ---------------- FAQ in the margin ---------------- */}
      <section id="faq" className="container-page grid scroll-mt-20 gap-10 pb-16 lg:grid-cols-[0.75fr_1.25fr] lg:pb-24">
        <div className="lg:sticky lg:top-24 lg:self-start">
          <Reveal><HandEyebrow>{t('faqEyebrow')}</HandEyebrow></Reveal>
          <h2 className="mt-1 text-4xl font-extrabold leading-tight sm:text-5xl"><WordsReveal text={t('faqTitle')} inView /></h2>
          <motion.div
            initial={{ opacity: 0, y: 20, rotate: 0 }}
            whileInView={{ opacity: 1, y: 0, rotate: -1.5 }}
            whileHover={{ rotate: 0 }}
            viewport={{ once: true, amount: 0.5 }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1], delay: 0.2 }}
            className="mt-8 max-w-sm"
          >
            <StickyNote color="yellow" className="relative">
              <span className="absolute -top-3 left-8 h-6 w-16 -rotate-3 bg-white/60 shadow-sm" aria-hidden />
              <p className="font-display text-xl font-bold">{t('faqStillTitle')}</p>
              <p className="mt-1.5 text-sm leading-relaxed text-ink/80">{t('faqStillBody')}</p>
              <Link to={startHref} className="group mt-4 inline-flex items-center gap-1.5 font-bold text-primary">
                {t('faqStillCta')}
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" aria-hidden />
              </Link>
            </StickyNote>
          </motion.div>
        </div>
        <motion.div
          className="space-y-2"
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.2 }}
          variants={{ show: { transition: { staggerChildren: 0.06 } } }}
        >
          {FAQS.map((f, i) => (
            <motion.div key={f.q} variants={{ hidden: { opacity: 0, x: 16 }, show: { opacity: 1, x: 0, transition: { duration: 0.35, ease: [0.22, 1, 0.36, 1] } } }}>
              <FaqItem index={i} id={`faq-${i}`} q={t(f.q)} a={t(f.a)} open={faqOpen === i} onToggle={() => setFaqOpen((o) => (o === i ? -1 : i))} />
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ---------------- Final CTA ---------------- */}
      <section className="container-page pb-16 lg:pb-20">
        <motion.div
          className="relative flex flex-col items-start justify-between gap-8 overflow-hidden rounded-[28px] bg-chalkboard px-6 py-12 shadow-[0_12px_0_var(--color-wood)] sm:px-12 sm:py-16 lg:flex-row lg:items-center"
          initial={{ opacity: 0, scale: 0.97, y: 20 }}
          whileInView={{ opacity: 1, scale: 1, y: 0 }}
          viewport={{ once: true, amount: 0.4 }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        >
          <FloatingBubbles />
          <span className="pointer-events-none absolute -right-20 -top-20 h-72 w-72 rounded-full bg-accent/20 blur-3xl" aria-hidden />
          <div className="relative min-w-0">
            <h2 className="font-hand text-4xl font-bold leading-tight text-chalk-text sm:text-5xl">
              <span className="block"><WordsReveal text={t('ctaTitle1')} inView /></span>
              <span className="block text-marigold"><WordsReveal text={t('ctaTitle2')} inView delay={0.25} /></span>
            </h2>
            <p className="mt-3 text-lg text-white/80">{t('ctaBody')}</p>
          </div>
          <div className="relative shrink-0">
            <motion.span
              className="pointer-events-none absolute inset-0 rounded-[20px] border-2 border-marigold"
              animate={{ scale: [1, 1.12], opacity: [0.7, 0] }}
              transition={{ duration: 1.8, repeat: Infinity, ease: 'easeOut' }}
              aria-hidden
            />
            <Magnetic><BubbleCta to={startHref} tone="marigold">{t('ctaBubble')}</BubbleCta></Magnetic>
          </div>
        </motion.div>
        <p className="mt-6 text-center text-xs text-muted">{tl('affiliation')}</p>
      </section>
    </div>
  );
}
