import type { AllowanceLimit, Allowances, Plan, PlanEntitlements, PlanGroup, PlanId, PlanPeriod, SubscriptionState } from '../types/core';

/**
 * Pricing blueprint (Nov 2026), mirrored from `backend/app/services/plan_catalog.py` for mock mode and as the
 * design copy (descriptions, features, badges) for the live `GET /v1/plans` response. Prices include GST.
 *
 * `credits` = full mocks for the whole billing period (1 credit = 1 full mock or 1 interview). Every other AI
 * allowance is in `entitlements.limits`: per calendar month on subscriptions, a one-off pool on add-ons.
 */

/** Metered AI features (`entitlements.limits` keys) and their labels, as `GET /v1/me/allowances` names them. */
export const METERED_FEATURES: Record<string, string> = {
  sectional_tests: 'Sectional tests',
  doubts: 'AI doubts',
  premium_doubts: 'Doubts with premium escalation',
  personal_notes: 'Personal notes and mind maps',
  topic_decks: 'Custom Topic Explainer decks',
  cheat_code_sessions: 'Cheat Code Coach sessions',
  descriptive_evals: 'Descriptive writing evaluations',
  text_interviews: 'Text mock interviews',
  voice_interviews: 'Voice mock interviews',
  smart_credits: 'Smart tutor credits (deep dive = 1, topic deck = 3)',
  master_credits: 'Master tutor credits (deep dive or topper rewrite = 1)',
  tutor_chat_turns: 'Ask Mitra tutor chat turns',
  photo_doubts: 'Photo doubts',
  ultra_credits: 'Ultra credits (deep dive = 1, topic deck = 4)',
};

const LIBRARIES = { topic_library: true, shortcut_library: true, leaderboard: true };

const FREE_ENT: PlanEntitlements = { flags: { ...LIBRARIES, persona: 'snapshot' }, limits: { doubts: 5, smart_credits: 1 } };
const STARTER: PlanEntitlements = {
  flags: { ...LIBRARIES, persona: 'full', study_planner: true, revision_ai: true, mistake_notebook: true },
  limits: { sectional_tests: 30, doubts: 50, personal_notes: 5, cheat_code_sessions: 3 },
};
const PRO: PlanEntitlements = {
  flags: { ...STARTER.flags, deep_persona: true, current_affairs: true, rank_predictor: true },
  limits: {
    sectional_tests: 100, doubts: 150, premium_doubts: 50, personal_notes: 20, topic_decks: 5,
    cheat_code_sessions: 10, descriptive_evals: 4, text_interviews: 2,
  },
};
const TUTOR_LITE: PlanEntitlements = { flags: {}, limits: { smart_credits: 20, tutor_chat_turns: 150, photo_doubts: 15, cheat_code_sessions: 3 } };
const TUTOR_PRO: PlanEntitlements = {
  flags: { mistake_notebook_visual: true },
  limits: { smart_credits: 40, master_credits: 10, tutor_chat_turns: 300, photo_doubts: 40, cheat_code_sessions: 5 },
};

function mergeEntitlements(...parts: PlanEntitlements[]): PlanEntitlements {
  const flags: PlanEntitlements['flags'] = {};
  const limits: PlanEntitlements['limits'] = {};
  for (const p of parts) {
    Object.assign(flags, p.flags);
    for (const [k, v] of Object.entries(p.limits)) limits[k] = (limits[k] ?? 0) + v;
  }
  return { flags, limits };
}
const COMBO = mergeEntitlements(PRO, TUTOR_PRO);

export const PERIOD_DAYS: Record<'monthly' | 'quarterly' | 'annual', number> = { monthly: 30, quarterly: 90, annual: 365 };
export const PERIOD_MONTHS: Record<'monthly' | 'quarterly' | 'annual', number> = { monthly: 1, quarterly: 3, annual: 12 };
export const PERIOD_LABEL: Record<PlanPeriod, string> = {
  monthly: 'Monthly', quarterly: 'Quarterly', annual: 'Annual', one_time: 'One-time', lifetime: 'Free forever',
};
/** Suffix after a subscription price, e.g. "₹149 / month". */
export const PERIOD_SUFFIX: Record<PlanPeriod, string> = { monthly: '/ month', quarterly: '/ quarter', annual: '/ year', one_time: '', lifetime: '' };

type Copy = Pick<Plan, 'description' | 'features' | 'cta'> & Partial<Pick<Plan, 'badge' | 'highlighted'>>;

/** Design copy per plan family (the backend sends only names, prices and entitlements). */
export const PLAN_FAMILY_COPY: Record<string, Copy> = {
  free: {
    description: 'Start free: one full mock per exam category with the AI report, a few AI doubts and the open libraries.',
    features: ['1 free full mock per exam category', '5 AI doubts', '1 sample AI deep dive', 'Topic and shortcut libraries', 'Persona snapshot'],
    cta: 'Start free',
  },
  starter: {
    description: 'Mock Pass: regular full mocks and sectional practice with a study planner and revision AI.',
    features: ['10 full mocks / month', '30 sectional tests / month', '50 AI doubts / month', '5 personal notes and mind maps', '3 Cheat Code Coach sessions', 'Full persona, study planner, revision AI, mistake notebook'],
    cta: 'Choose Starter',
  },
  pro: {
    description: 'Selection Pass: more mocks, premium doubt escalation, topic decks, writing evaluation and interviews.',
    features: ['25 full mocks / month', '100 sectional tests / month', '150 AI doubts (50 premium) / month', '20 personal notes · 5 topic decks', '10 Cheat Code Coach sessions', '4 descriptive evaluations · 2 text interviews', 'Deep persona, current affairs, rank predictor'],
    highlighted: true,
    badge: 'Most popular',
    cta: 'Choose Pro',
  },
  tutor_lite: {
    description: 'AI Tutor Lite: a personal AI tutor on top of any plan, including Free.',
    features: ['20 Smart tutor credits / month', '150 Ask Mitra chat turns', '15 photo doubts', '3 Cheat Code Coach sessions'],
    cta: 'Add Tutor Lite',
  },
  tutor_pro: {
    description: 'AI Tutor Pro: Master deep dives and topper rewrites, more chat and photo doubts.',
    features: ['40 Smart + 10 Master tutor credits / month', '300 Ask Mitra chat turns', '40 photo doubts', '5 Cheat Code Coach sessions', 'Visual mistake notebook'],
    badge: 'Best tutor',
    cta: 'Add Tutor Pro',
  },
  combo: {
    description: 'Topper Combo: Pro (Selection Pass) and AI Tutor Pro together, for less than both.',
    features: ['Everything in Pro', 'Everything in AI Tutor Pro', '25 full mocks / month', 'Counts as your study plan and tutor pack'],
    highlighted: true,
    badge: 'Topper pick',
    cta: 'Choose Topper Combo',
  },
  single_mock: { description: 'One full mock with the AI report, valid for 90 days.', features: ['1 full mock', 'AI report', 'Valid 90 days'], cta: 'Buy 1 mock' },
  extra_mocks_5: { description: 'Five extra full mocks on top of your plan, valid for 90 days.', features: ['5 full mocks', 'Valid 90 days'], cta: 'Add 5 mocks' },
  extra_doubts_50: { description: '50 extra Smart doubts when your monthly doubts run out, valid for 90 days.', features: ['50 AI doubts', 'Valid 90 days'], cta: 'Add 50 doubts' },
  extra_master_10: { description: '10 extra Master deep dives, valid for 90 days.', features: ['10 Master tutor credits', 'Valid 90 days'], cta: 'Add 10 deep dives' },
  interview_pack: { description: 'Two voice and five text mock interviews, valid for 60 days.', features: ['2 voice mock interviews', '5 text mock interviews', 'Valid 60 days'], cta: 'Buy Interview Pack' },
  ultra_pack: { description: 'Ten Ultra credits on our strongest AI model, valid for 30 days.', features: ['10 Ultra credits (deep dive = 1, topic deck = 4)', 'Valid 30 days'], cta: 'Buy Ultra pack' },
};

/** Plan family from a backend code: 'starter_quarterly' → 'starter', 'free_trial' → 'free', add-ons → their code. */
export function planFamily(code: string): string {
  if (code === 'free_trial' || code === 'free') return 'free';
  const m = /^(.*)_(monthly|quarterly|annual)$/.exec(code);
  return m ? m[1]! : code;
}

export const planIdFromCode = (code: string): PlanId => (code === 'free_trial' ? 'free' : code);
export const planCodeFromId = (id: string): string => (id === 'free' ? 'free_trial' : id);

function sub(code: string, name: string, price: number, group: PlanGroup, period: 'monthly' | 'quarterly' | 'annual', mocksPerMonth: number, ent: PlanEntitlements): Plan {
  const family = planFamily(code);
  const copy = PLAN_FAMILY_COPY[family]!;
  return {
    id: code, code, name, group, period, family, priceInr: price,
    credits: mocksPerMonth * PERIOD_MONTHS[period], validityDays: PERIOD_DAYS[period], isRecurring: true,
    entitlements: { ...ent, fullMocksPerMonth: mocksPerMonth },
    ...copy,
    badge: period === 'annual' && !copy.badge ? 'Best value' : copy.badge,
  };
}

function addon(code: string, name: string, price: number, credits: number, days: number, limits: Record<string, number> = {}): Plan {
  return {
    id: code, code, name, group: 'addon', period: 'one_time', family: code, priceInr: price, credits, validityDays: days,
    isRecurring: false, entitlements: { flags: {}, limits }, ...PLAN_FAMILY_COPY[code]!,
  };
}

export const PLAN_CATALOG: Plan[] = [
  {
    id: 'free', code: 'free_trial', name: 'Free', group: 'free', period: 'lifetime', family: 'free', priceInr: 0, credits: 1,
    validityDays: 30, isRecurring: false, entitlements: FREE_ENT, ...PLAN_FAMILY_COPY.free!,
  },
  sub('starter_monthly', 'Starter (Mock Pass) · monthly', 149, 'study', 'monthly', 10, STARTER),
  sub('starter_quarterly', 'Starter (Mock Pass) · quarterly', 399, 'study', 'quarterly', 10, STARTER),
  sub('starter_annual', 'Starter (Mock Pass) · annual', 1199, 'study', 'annual', 10, STARTER),
  sub('pro_monthly', 'Pro (Selection Pass) · monthly', 299, 'study', 'monthly', 25, PRO),
  sub('pro_quarterly', 'Pro (Selection Pass) · quarterly', 799, 'study', 'quarterly', 25, PRO),
  sub('pro_annual', 'Pro (Selection Pass) · annual', 2499, 'study', 'annual', 25, PRO),
  sub('tutor_lite_monthly', 'AI Tutor Lite · monthly', 99, 'tutor', 'monthly', 0, TUTOR_LITE),
  sub('tutor_lite_annual', 'AI Tutor Lite · annual', 999, 'tutor', 'annual', 0, TUTOR_LITE),
  sub('tutor_pro_monthly', 'AI Tutor Pro · monthly', 299, 'tutor', 'monthly', 0, TUTOR_PRO),
  sub('tutor_pro_annual', 'AI Tutor Pro · annual', 2999, 'tutor', 'annual', 0, TUTOR_PRO),
  sub('combo_monthly', 'Topper Combo (Pro + AI Tutor Pro) · monthly', 499, 'combo', 'monthly', 25, COMBO),
  sub('combo_annual', 'Topper Combo (Pro + AI Tutor Pro) · annual', 4999, 'combo', 'annual', 25, COMBO),
  addon('single_mock', 'Single mock with AI report', 29, 1, 90),
  addon('extra_mocks_5', '5 extra full mocks', 49, 5, 90),
  addon('extra_doubts_50', '50 extra Smart doubts', 39, 0, 90, { doubts: 50 }),
  addon('extra_master_10', '10 extra Master deep dives', 99, 0, 90, { master_credits: 10 }),
  addon('interview_pack', 'Interview Pack (2 voice + 5 text)', 199, 0, 60, { voice_interviews: 2, text_interviews: 5 }),
  addon('ultra_pack', 'Ultra pack (10 Ultra credits)', 349, 0, 30, { ultra_credits: 10 }),
];

/** Short display name without the period suffix: "Starter (Mock Pass) · monthly" → "Starter (Mock Pass)". */
export const planShortName = (p: Pick<Plan, 'name'>) => p.name.replace(/\s·\s(monthly|quarterly|annual)$/i, '');

/** Percent saved against paying monthly for the same family, or 0. */
export function periodSaving(plan: Plan, plans: Plan[]): number {
  if (plan.period !== 'quarterly' && plan.period !== 'annual') return 0;
  const monthly = plans.find((p) => p.family === plan.family && p.period === 'monthly');
  if (!monthly || monthly.priceInr <= 0) return 0;
  const full = monthly.priceInr * PERIOD_MONTHS[plan.period];
  return Math.max(0, Math.round((1 - plan.priceInr / full) * 100));
}

/** Pricing-screen sections, in display order. */
export function groupPlans(plans: Plan[]) {
  return {
    free: plans.find((p) => p.group === 'free'),
    study: plans.filter((p) => p.group === 'study'),
    tutor: plans.filter((p) => p.group === 'tutor'),
    combo: plans.filter((p) => p.group === 'combo'),
    addon: plans.filter((p) => p.group === 'addon'),
  };
}

/** Subscription slots a plan takes: one study plan and one tutor pack at a time; the combo takes both. */
export const planSlots = (group: PlanGroup): ('study' | 'tutor')[] =>
  group === 'study' ? ['study'] : group === 'tutor' ? ['tutor'] : group === 'combo' ? ['study', 'tutor'] : [];

/** Plan ids the student holds now (study plan / combo and tutor pack), free tier excluded. */
export const heldPlanIds = (sub: Pick<SubscriptionState, 'planId' | 'tutorPlanId'>): PlanId[] =>
  [sub.planId, sub.tutorPlanId].filter((id): id is PlanId => !!id && id !== 'free');

/** Held plans plus add-ons still inside their validity (mock mode's input to `mockAllowances`). */
export function activePurchaseIds(
  sub: Pick<SubscriptionState, 'planId' | 'tutorPlanId'>,
  orders: { planId: PlanId; status: string; createdAt: string }[],
  plans: Plan[] = PLAN_CATALOG,
  now = Date.now(),
): PlanId[] {
  const addons = orders
    .filter((o) => o.status === 'success')
    .map((o) => ({ o, p: plans.find((p) => p.id === o.planId) }))
    .filter(({ o, p }) => p?.group === 'addon' && Date.parse(o.createdAt) + (p.validityDays ?? 0) * 86_400_000 > now)
    .map(({ o }) => o.planId);
  return [...heldPlanIds(sub), ...addons];
}

/**
 * The held plan whose slot `plan` would take (the server answers 409 `already_subscribed`), or undefined.
 * Add-ons never conflict.
 */
export function conflictingPlan(plan: Plan, held: PlanId[], plans: Plan[]): Plan | undefined {
  const want = planSlots(plan.group);
  if (!want.length) return undefined;
  return held.map((id) => plans.find((p) => p.id === id)).find((h) => h && planSlots(h.group).some((s) => want.includes(s)));
}

/** Splits held backend codes into the study plan (or combo) and the tutor pack. */
export function subscriptionSlots(codes: string[], plans: Plan[] = PLAN_CATALOG): { planId: PlanId; tutorPlanId?: PlanId } {
  let planId: PlanId = 'free';
  let tutorPlanId: PlanId | undefined;
  for (const code of codes) {
    const id = planIdFromCode(code);
    const group = plans.find((p) => p.id === id)?.group ?? groupFromCode(code);
    if (group === 'study' || group === 'combo') planId = id;
    else if (group === 'tutor') tutorPlanId = id;
  }
  return { planId, tutorPlanId };
}

/** Best guess at a group for a code missing from the plan list (older or newer catalogs). */
export function groupFromCode(code: string): PlanGroup {
  if (code === 'free_trial' || code === 'free') return 'free';
  const fam = planFamily(code);
  if (fam === 'combo') return 'combo';
  if (fam.startsWith('tutor')) return 'tutor';
  if (fam !== code) return 'study';
  return 'addon';
}

/**
 * Allowances for mock mode, computed the way the backend does: Free plus every held plan, plus add-ons bought.
 * `used` comes from the caller (the demo keeps no per-feature usage, so it defaults to 0).
 */
export function mockAllowances(held: PlanId[], plans: Plan[] = PLAN_CATALOG, used: Record<string, number> = {}): Allowances {
  const owned = held.map((id) => plans.find((p) => p.id === id)).filter((p): p is Plan => !!p);
  const free = plans.find((p) => p.group === 'free')?.entitlements ?? FREE_ENT;
  const flags: Allowances['flags'] = { ...free.flags };
  for (const p of owned) {
    for (const [k, v] of Object.entries(p.entitlements.flags)) if (v && !(k === 'persona' && flags[k] === 'full')) flags[k] = v;
  }
  const merged = mergeEntitlements(free, ...owned.map((p) => ({ flags: {}, limits: p.entitlements.limits })));
  const limits: AllowanceLimit[] = Object.entries(METERED_FEATURES).map(([feature, label]) => {
    const limit = merged.limits[feature] ?? 0;
    const u = Math.min(used[feature] ?? 0, limit);
    return { feature, label, limit, used: u, remaining: limit - u };
  });
  const now = new Date();
  const resetsAt = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + 1, 1)).toISOString();
  return { plans: owned.map((p) => p.id), flags, limits, resetsAt };
}
