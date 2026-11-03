import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { CircleCheck, Clock, Mail, MapPin } from 'lucide-react';
import { SUPPORT_EMAIL } from '@prepmitra/shared';
import { contactSchema, type ContactInput } from './contactSchema';
import { Button, Card, Input, Notice, PageHeader, Select, Textarea } from '@/components/ui';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';



const TOPICS = [
  { value: 'payment', label: 'Payment or refund' },
  { value: 'question', label: 'Wrong or unclear question' },
  { value: 'account', label: 'Account or login' },
  { value: 'privacy', label: 'Privacy or data request' },
  { value: 'other', label: 'Something else' },
];

export function ContactPage() {
  useDocumentTitle('Contact us', 'Contact PrepMitra AI support for payments, refunds, account help or privacy requests.');
  const [sentTo, setSentTo] = useState<string | null>(null);
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<ContactInput>({
    resolver: zodResolver(contactSchema),
    defaultValues: { name: '', email: '', phone: '', topic: '', message: '' },
  });

  const onSubmit = async (data: ContactInput) => {
    await new Promise((r) => setTimeout(r, import.meta.env.MODE === 'test' ? 0 : 600));
    setSentTo(data.email);
    reset();
  };

  return (
    <div className="container-page py-10 lg:py-14">
      <PageHeader title="Contact us" description="Questions about payments, refunds, your account or your data? We reply within 2 working days." />
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_340px]">
        <Card className="min-w-0 p-6 sm:p-8">
          {sentTo ? (
            <div role="status" className="flex flex-col items-center py-8 text-center">
              <CircleCheck className="h-12 w-12 text-success" aria-hidden />
              <h2 className="mt-4 text-xl font-bold">Message recorded</h2>
              <p className="mt-2 max-w-md text-sm text-muted">
                Demo: this message is not sent anywhere. In production our support team would reply to {sentTo}.
              </p>
              <Button variant="outline" className="mt-6" onClick={() => setSentTo(null)}>Write another message</Button>
            </div>
          ) : (
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
              <Notice tone="info">Demo form: messages are checked here but not sent to anyone.</Notice>
              <div className="grid gap-4 sm:grid-cols-2">
                <Input label="Your name" required autoComplete="name" error={errors.name?.message} {...register('name')} />
                <Input label="Email" type="email" required autoComplete="email" error={errors.email?.message} {...register('email')} />
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                <Input label="Registered mobile (optional)" leftAddon="+91" type="tel" inputMode="numeric" maxLength={10} error={errors.phone?.message} {...register('phone')} />
                <Select label="Topic" required placeholder="Choose a topic" options={TOPICS} error={errors.topic?.message} {...register('topic')} />
              </div>
              <Textarea label="Message" required rows={6} hint="For payments, include the order ID from your receipt." error={errors.message?.message} {...register('message')} />
              <Button type="submit" size="lg" loading={isSubmitting}>Send message</Button>
            </form>
          )}
        </Card>
        <div className="space-y-4">
          <Card className="space-y-4 p-6 text-sm">
            <p className="flex gap-3"><Mail className="mt-0.5 h-5 w-5 shrink-0 text-primary" aria-hidden /><span><b className="block">Email</b><span className="select-all text-muted">{SUPPORT_EMAIL}</span></span></p>
            <p className="flex gap-3"><Clock className="mt-0.5 h-5 w-5 shrink-0 text-primary" aria-hidden /><span><b className="block">Support hours</b><span className="text-muted">Monday–Saturday, 10 AM – 7 PM IST</span></span></p>
            <p className="flex gap-3"><MapPin className="mt-0.5 h-5 w-5 shrink-0 text-primary" aria-hidden /><span><b className="block">Registered office</b><span className="text-muted">[Company legal name], [Registered address]</span></span></p>
          </Card>
          <Card className="p-6 text-sm">
            <b className="block">Grievance Officer</b>
            <p className="mt-1 text-muted">[Grievance Officer name] · [grievance@yourdomain.in]</p>
            <p className="mt-2 text-muted">For privacy complaints under the DPDP Act, 2023. We acknowledge within 48 hours.</p>
          </Card>
        </div>
      </div>
    </div>
  );
}
