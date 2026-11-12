import { Link } from 'react-router-dom';
import { Bot, BrainCircuit, Camera, FileText, Gauge, GraduationCap, Newspaper, PenLine, Repeat, Sparkles, Wand2 } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { Card, PageHeader } from '@/components/ui';
import { AllowanceChip, hasFlag, useAllowances } from '@/components/ai/AiUi';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { formatDate } from '@prepmitra/shared';

interface Tool {
  to: string;
  title: string;
  desc: string;
  icon: LucideIcon;
  feature?: string;
  flag?: string;
  plan?: string;
}

const AI_TOOLS: Tool[] = [
  { to: '/ai/doubts', title: 'Doubt Solver', desc: 'Type or photograph any question. Verified step-by-step answers, shortcuts and the trap to avoid.', icon: Sparkles, feature: 'doubts' },
  { to: '/ai/doubts?tab=photo', title: 'Photo doubt', desc: 'Snap a question from a book or paper and get it solved.', icon: Camera, feature: 'photo_doubts' },
  { to: '/ai/tutor', title: 'Ask Mitra (AI tutor)', desc: 'Chat with a tutor that knows your mocks. Ask for a story or a different explanation.', icon: Bot, feature: 'tutor_chat_turns' },
  { to: '/ai/tutor?tab=deep', title: 'Deep dives', desc: 'One-page visual, concept from zero, the trap, a checklist and three practice questions.', icon: GraduationCap, feature: 'smart_credits' },
  { to: '/ai/persona', title: 'Persona & rank', desc: 'Your topic mastery, error mix, speed profile, deep strategy and rank predictor.', icon: Gauge, flag: 'rank_predictor', plan: 'Pro' },
  { to: '/ai/notes', title: 'Notes & topic decks', desc: 'Notes, formula sheets and mind maps; free library decks or a custom slide deck.', icon: FileText, feature: 'personal_notes' },
  { to: '/ai/practice?tab=revision', title: 'Revision AI', desc: 'Today’s spaced quiz from your mistakes, with hints and your flashcards.', icon: Repeat, flag: 'revision_ai', plan: 'Starter' },
  { to: '/ai/practice?tab=current', title: 'Current affairs', desc: 'Daily fact-checked digest with a 10-question GA quiz.', icon: Newspaper, flag: 'current_affairs', plan: 'Pro' },
  { to: '/ai/practice?tab=writing', title: 'Writing evaluator', desc: 'Essay, letter and précis scored on a rubric, with corrections and a model answer.', icon: PenLine, feature: 'descriptive_evals' },
  { to: '/ai/coach', title: 'Cheat Code Coach', desc: 'Discover a shortcut yourself, test it on real questions and lock it as a revision card.', icon: Wand2, feature: 'cheat_code_sessions' },
];

export function AiHubPage() {
  useDocumentTitle('AI study tools');
  const { data } = useAllowances();
  return (
    <div>
      <PageHeader eyebrow={<span className="inline-flex items-center gap-1 text-xs font-semibold uppercase tracking-wide text-primary"><BrainCircuit className="h-4 w-4" /> PrepMitra AI</span>}
        title="AI study tools" description="Everything Mitra can do for you. Each tool shows what is left on your plan this month." />
      {data?.resetsAt && <p className="-mt-3 mb-5 text-xs text-muted">Monthly allowances reset on {formatDate(data.resetsAt)}. <Link to="/subscription" className="font-semibold text-primary hover:underline">Plans and top-ups</Link></p>}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {AI_TOOLS.map((t) => {
          const locked = t.flag && data && !hasFlag(data, t.flag);
          return (
            <Link key={t.to} to={t.to} className="group">
              <Card className="h-full p-5 transition-shadow group-hover:shadow-md">
                <div className="flex items-start gap-3">
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary-soft text-primary"><t.icon className="h-5 w-5" aria-hidden /></span>
                  <div className="min-w-0">
                    <h2 className="font-semibold group-hover:text-primary">{t.title}</h2>
                    <p className="mt-1 text-sm text-muted">{t.desc}</p>
                    <div className="mt-3">
                      {t.feature && <AllowanceChip feature={t.feature} />}
                      {t.flag && data && (locked
                        ? <span className="rounded-full bg-stone-100 px-2 py-0.5 text-xs font-medium text-muted">{t.plan} plan feature</span>
                        : <span className="rounded-full bg-success-soft px-2 py-0.5 text-xs font-medium text-success">Included</span>)}
                    </div>
                  </div>
                </div>
              </Card>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
