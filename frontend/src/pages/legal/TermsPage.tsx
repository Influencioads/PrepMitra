import { Link } from 'react-router-dom';
import { DISCLAIMERS } from '@prepmitra/shared';
import { LegalDoc, type LegalSection } from './LegalDoc';

const SECTIONS: LegalSection[] = [
  {
    id: 'agreement',
    title: 'Agreement',
    body: (
      <p>
        These Terms of Use govern your use of the PrepMitra AI website and apps, operated by [Company legal name], [Registered
        address]. By creating an account you confirm that you are at least 18 years old and agree to these terms and our{' '}
        <Link to="/privacy" className="font-medium text-primary hover:underline">Privacy policy</Link>.
      </p>
    ),
  },
  {
    id: 'service',
    title: 'The service',
    body: (
      <>
        <p>PrepMitra AI provides practice mock exams, mock interviews and personalised performance reports for exam aspirants and job seekers.</p>
        <p><b>No affiliation:</b> {DISCLAIMERS.examAffiliation}</p>
        <p>Mock tests follow publicly known exam patterns. We do not guarantee any score, rank, selection or job offer.</p>
      </>
    ),
  },
  {
    id: 'ai-content',
    title: 'AI-generated content',
    body: (
      <>
        <p>
          Questions, explanations, interview questions and report text are generated with the help of AI and checked by automated
          verification and sample human review. Despite these checks, AI content can occasionally be wrong or unclear.
        </p>
        <ul>
          <li>Use the “Report this question” button whenever you spot a mistake. Questions with repeated reports are removed for review.</li>
          <li>Shortcuts and techniques we suggest are legitimate exam-solving methods only. We never support cheating in a real exam.</li>
          <li>Reports are guidance for practice, not professional career, legal or financial advice.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'account',
    title: 'Your account',
    body: (
      <ul>
        <li>One account per person. Keep your mobile number and one-time codes private.</li>
        <li>Give accurate profile information; reports and recommendations depend on it.</li>
        <li>You are responsible for activity on your account. Tell us immediately if you suspect misuse.</li>
      </ul>
    ),
  },
  {
    id: 'credits',
    title: 'Credits and payments',
    body: (
      <>
        <ul>
          <li>One credit allows one full mock exam or one mock interview, including its report. Some exams may need more than one credit, as shown before you start.</li>
          <li>Credits are deducted when you start an attempt, not when you buy them. Oldest-expiring credits are used first.</li>
          <li>Purchased credits are valid for the period shown at purchase (90 days for single credits and credit packs). Unused credits expire after that.</li>
          <li>Prices are shown in Indian Rupees and [include / exclude] 18% GST.</li>
          <li>Credits have no cash value and cannot be transferred or sold.</li>
        </ul>
        <p>Refunds and cancellations are covered by our <Link to="/refund-policy" className="font-medium text-primary hover:underline">Refund and cancellation policy</Link>.</p>
      </>
    ),
  },
  {
    id: 'fair-use',
    title: 'Fair use',
    body: (
      <>
        <p>You agree not to:</p>
        <ul>
          <li>Copy, scrape, resell or publish our questions, papers, reports or other content.</li>
          <li>Use bots, scripts or multiple accounts to access the service or to abuse free trials.</li>
          <li>Try to bypass the exam timer, anti-cheating checks or security measures.</li>
          <li>Upload content you do not own or that is unlawful, abusive or contains malicious code.</li>
          <li>Try to manipulate the AI interviewer or report generator with hidden instructions.</li>
        </ul>
        <p>We may suspend or close accounts that break these rules. Light anti-cheating signals (such as tab switches) are recorded and shown in your report; they do not change your score.</p>
      </>
    ),
  },
  {
    id: 'ip',
    title: 'Intellectual property',
    body: <p>All content on PrepMitra AI, including questions, explanations, designs and software, belongs to [Company legal name] or its licensors. Your answers, resume and interview responses remain yours; you allow us to use them only to provide and improve the service as described in the Privacy policy.</p>,
  },
  {
    id: 'liability',
    title: 'Limitation of liability',
    body: <p>The service is provided “as is”. To the extent permitted by law, our total liability for any claim is limited to the amount you paid us in the three months before the claim. We are not liable for indirect losses such as lost opportunities or exam outcomes.</p>,
  },
  {
    id: 'law',
    title: 'Governing law',
    body: <p>These terms are governed by the laws of India. Courts at [City] have exclusive jurisdiction, subject to any rights you have under consumer protection law.</p>,
  },
  {
    id: 'changes',
    title: 'Changes',
    body: <p>We may update these terms. We will notify you of material changes in the app or by email. Continuing to use the service after changes take effect means you accept them.</p>,
  },
];

export function TermsPage() {
  return (
    <LegalDoc
      title="Terms of use"
      description="The rules for using PrepMitra AI mock exams, mock interviews and credits."
      metaDescription="PrepMitra AI terms of use: AI-generated content notice, credits and payments, fair use, and no affiliation with any exam-conducting body."
      sections={SECTIONS}
    />
  );
}
