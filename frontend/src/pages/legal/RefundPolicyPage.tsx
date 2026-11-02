import { Link } from 'react-router-dom';
import { SUPPORT_EMAIL } from '@prepmitra/shared';
import { LegalDoc, type LegalSection } from './LegalDoc';

const SECTIONS: LegalSection[] = [
  {
    id: 'summary',
    title: 'Summary',
    body: (
      <ul>
        <li>Credits are deducted only when you start an exam or interview.</li>
        <li>If an attempt fails because of a technical problem on our side, the credit is restored automatically.</li>
        <li>Unused purchased credits can be refunded within 7 days of purchase.</li>
        <li>You can cancel auto-renew at any time; your plan stays active until it expires.</li>
      </ul>
    ),
  },
  {
    id: 'credits',
    title: 'How credits are used',
    body: (
      <>
        <p>One credit covers one full mock exam or one mock interview, including its report. A credit is deducted at the moment you press Start, not at purchase. Oldest-expiring credits are used first.</p>
        <p>Purchased credits are valid for 90 days from purchase unless a different validity is shown on the plan. Expired credits cannot be refunded or restored.</p>
      </>
    ),
  },
  {
    id: 'auto-restore',
    title: 'Automatic credit restore',
    body: (
      <>
        <p>Your credit is restored automatically, without you having to ask, if:</p>
        <ul>
          <li>The exam or interview could not start or crashed because of an error on our side.</li>
          <li>Your report was not generated within 10 minutes of submitting.</li>
        </ul>
        <p>Restored credits appear in Credits &amp; plan › Credit history with the reason “Credit restored”.</p>
      </>
    ),
  },
  {
    id: 'refunds',
    title: 'Refunds',
    body: (
      <>
        <ul>
          <li><b>Unused credits:</b> request a refund within 7 days of purchase for any credits you have not used. Partly used packs are refunded for the unused credits, pro rata.</li>
          <li><b>Duplicate or failed payments:</b> if you were charged but did not receive credits, or were charged twice, we refund the extra amount in full.</li>
          <li><b>Not refundable:</b> credits already used for a completed attempt, expired credits and the free trial.</li>
        </ul>
        <p>Approved refunds go back to the original payment method (UPI, card, net banking or wallet) within 5–7 working days. Your bank may take a few more days to show it.</p>
      </>
    ),
  },
  {
    id: 'cancellation',
    title: 'Cancelling a subscription',
    body: (
      <p>
        If you are on an auto-renewing plan, you can cancel auto-renew anytime from Credits &amp; plan. Cancellation stops future
        charges; your current plan and its credits stay active until the renewal date. Unused monthly credits expire at the end of
        each billing period. App store purchases are cancelled through Google Play or the App Store.
      </p>
    ),
  },
  {
    id: 'how-to',
    title: 'How to request a refund',
    body: (
      <p>
        Write to {SUPPORT_EMAIL} or use the <Link to="/contact" className="font-medium text-primary hover:underline">contact form</Link>{' '}
        with your registered mobile number and the order ID from your receipt. We reply within 2 working days.
      </p>
    ),
  },
];

export function RefundPolicyPage() {
  return (
    <LegalDoc
      title="Refund and cancellation policy"
      description="When credits are restored, how refunds work, and how to cancel auto-renew."
      metaDescription="PrepMitra AI refund and cancellation policy: credits deducted on attempt start, automatic restore on technical failure, refunds in 5–7 working days."
      sections={SECTIONS}
    />
  );
}
