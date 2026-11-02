import type { ComponentProps } from 'react';
import type Ionicons from '@expo/vector-icons/Ionicons';
import type { ExamCategory, IconKey, NotificationType } from '@prepmitra/shared';

export type IoniconName = ComponentProps<typeof Ionicons>['name'];

/** Maps the shared, library-agnostic icon keys to Ionicons glyphs. */
export const ICONS: Record<IconKey, IoniconName> = {
  landmark: 'business-outline',
  banknote: 'cash-outline',
  train: 'train-outline',
  scale: 'scale-outline',
  graduation: 'school-outline',
  briefcase: 'briefcase-outline',
  code: 'code-slash-outline',
  users: 'people-outline',
  trending: 'trending-up-outline',
  calculator: 'calculator-outline',
  brain: 'bulb-outline',
  mic: 'mic-outline',
  file: 'document-text-outline',
  target: 'locate-outline',
  languages: 'language-outline',
  chart: 'bar-chart-outline',
  sparkles: 'sparkles-outline',
  shield: 'shield-checkmark-outline',
  clock: 'time-outline',
  award: 'ribbon-outline',
};

export const CATEGORY_ICONS: Record<ExamCategory, IoniconName> = {
  government: ICONS.landmark,
  banking: ICONS.banknote,
  railway: ICONS.train,
  'civil-services': ICONS.scale,
  'higher-education': ICONS.graduation,
  'campus-placement': ICONS.briefcase,
};

export const NOTIFICATION_ICONS: Record<NotificationType, IoniconName> = {
  result: 'document-text-outline',
  payment: 'card-outline',
  reminder: 'alarm-outline',
  plan: 'calendar-outline',
  system: 'information-circle-outline',
  interview: 'chatbubbles-outline',
};
