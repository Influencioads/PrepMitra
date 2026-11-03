import { z } from 'zod';
import { phoneSchema } from '@prepmitra/shared';

export const contactSchema = z.object({
  name: z.string().trim().min(2, 'Enter your name'),
  email: z.email('Enter a valid email address'),
  phone: z.union([z.literal(''), phoneSchema]).optional(),
  topic: z.string().min(1, 'Choose a topic'),
  message: z.string().trim().min(20, 'Tell us a little more (at least 20 characters)').max(2000, 'Keep it under 2,000 characters'),
});
export type ContactInput = z.infer<typeof contactSchema>;
