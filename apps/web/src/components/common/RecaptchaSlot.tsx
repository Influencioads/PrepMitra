import { firebaseEnabled } from '@/utils/env';
import { RECAPTCHA_CONTAINER_ID } from '@/services/firebaseAuth';

/** Invisible reCAPTCHA host required by Firebase phone auth. Renders nothing in demo mode. */
export function RecaptchaSlot() {
  if (!firebaseEnabled()) return null;
  return <div id={RECAPTCHA_CONTAINER_ID} />;
}
