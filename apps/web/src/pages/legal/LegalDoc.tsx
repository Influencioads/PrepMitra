import type { ReactNode } from 'react';
import { Card, Notice, PageHeader } from '@/components/ui';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

export interface LegalSection {
  id: string;
  title: string;
  body: ReactNode;
}

export const LEGAL_LAST_UPDATED = '30 October 2026';

/** Shared layout for policy pages: title, draft notice, sticky table of contents, sections. */
export function LegalDoc({
  title, description, sections, metaDescription,
}: { title: string; description: string; sections: LegalSection[]; metaDescription: string }) {
  useDocumentTitle(title, metaDescription);
  return (
    <div className="container-page py-10 lg:py-14">
      <PageHeader title={title} description={description} eyebrow={<p className="text-xs font-semibold uppercase tracking-wider text-primary">Last updated {LEGAL_LAST_UPDATED}</p>} />
      <Notice tone="warning" title="Draft for review" className="mb-8">
        Replace with lawyer-checked text before launch. Text in [square brackets] must be filled in.
      </Notice>
      <div className="grid gap-8 lg:grid-cols-[240px_minmax(0,1fr)]">
        <nav aria-label="On this page" className="hidden lg:block">
          <div className="sticky top-24">
            <p className="text-xs font-semibold uppercase tracking-wider text-subtle">On this page</p>
            <ol className="mt-3 space-y-1.5 text-sm">
              {sections.map((s, i) => (
                <li key={s.id}>
                  <a href={`#${s.id}`} className="block rounded-md px-2 py-1 text-muted hover:bg-stone-100 hover:text-ink">
                    {i + 1}. {s.title}
                  </a>
                </li>
              ))}
            </ol>
          </div>
        </nav>
        <Card className="min-w-0 p-6 sm:p-8">
          <div className="space-y-9">
            {sections.map((s, i) => (
              <section key={s.id} id={s.id} className="scroll-mt-24">
                <h2 className="text-xl font-bold">{i + 1}. {s.title}</h2>
                <div className="mt-3 space-y-3 text-[15px] leading-relaxed text-ink/85 [&_li]:ml-5 [&_li]:list-disc [&_li]:pl-1 [&_ul]:space-y-1.5">{s.body}</div>
              </section>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
