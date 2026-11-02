import type { AuthSession } from '@prepmitra/shared';
import {
  DEFAULT_SETTINGS, DEMO_PROFILE, EMPTY_PROFILE, SEED_NOTIFICATIONS, SEED_SUBSCRIPTION, createSeedHistory, createSeedInterview, createSeedPracticeLog,
} from '@prepmitra/shared';
import { useAuthStore } from './authStore';
import { useExamStore } from './examStore';
import { useInterviewStore } from './interviewStore';
import { useNotificationStore } from './notificationStore';
import { useProfileStore } from './profileStore';
import { NEW_USER_SUBSCRIPTION, useSubscriptionStore } from './subscriptionStore';

/**
 * Signs the user in and prepares local demo data. Existing (returning) users get
 * seeded history; new sign-ups start empty with a free trial. Data already on
 * this device for the same user is kept.
 */
export function signInWithDemoData(session: AuthSession) {
  const uid = session.user.id;
  useAuthStore.getState().signIn(session);
  if (useProfileStore.getState().ownerId === uid) return;

  if (session.isNewUser) {
    useProfileStore.getState().reset(uid, EMPTY_PROFILE, DEFAULT_SETTINGS);
    useExamStore.getState().reset(uid, [], []);
    useInterviewStore.getState().reset(uid, [], []);
    useSubscriptionStore.getState().reset(uid, NEW_USER_SUBSCRIPTION);
    useNotificationStore.getState().reset(uid, [
      {
        id: 'welcome', type: 'system', title: 'Welcome to PrepMitra AI', read: false, createdAt: new Date().toISOString(),
        body: 'Your free 30-minute mini mock is ready. Finish your profile and start practising.', link: '/exams/general-aptitude',
      },
    ]);
    return;
  }

  const { attempts, reports } = createSeedHistory();
  const interview = createSeedInterview();
  useProfileStore.getState().reset(uid, DEMO_PROFILE, DEFAULT_SETTINGS);
  useExamStore.getState().reset(uid, attempts, reports, createSeedPracticeLog());
  useInterviewStore.getState().reset(uid, [interview.session], [interview.report]);
  useSubscriptionStore.getState().reset(uid, SEED_SUBSCRIPTION);
  useNotificationStore.getState().reset(uid, SEED_NOTIFICATIONS);
}

/** Clears every demo store on this device (used by "Delete account"). */
export function wipeLocalData() {
  for (const store of [useProfileStore, useExamStore, useInterviewStore, useSubscriptionStore, useNotificationStore]) {
    store.persist.clearStorage();
  }
  useProfileStore.setState({ ownerId: null, profile: EMPTY_PROFILE, settings: DEFAULT_SETTINGS, draft: null });
  useExamStore.setState({ ownerId: null, attempts: {}, reports: {}, practiceLog: {} });
  useInterviewStore.setState({ ownerId: null, sessions: {}, reports: {} });
  useSubscriptionStore.setState({ ownerId: null, sub: NEW_USER_SUBSCRIPTION, orders: [] });
  useNotificationStore.setState({ ownerId: null, items: [] });
  useAuthStore.getState().signOut();
}
