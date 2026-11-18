import type { ComponentProps } from 'react';
import { Platform, type ColorValue } from 'react-native';
import { Tabs } from 'expo-router/js-tabs';
import Ionicons from '@expo/vector-icons/Ionicons';
import { useUnreadCount } from '@/store';
import { colors } from '@/theme';

type IconName = ComponentProps<typeof Ionicons>['name'];

const icon = (active: IconName, inactive: IconName) =>
  function TabIcon({ focused, color, size }: { focused: boolean; color: ColorValue; size: number }) {
    return <Ionicons name={focused ? active : inactive} size={size} color={color as string} />;
  };

/** Home is the tab group's anchor (initial tab and back target). */
export const unstable_settings = { anchor: 'home' };

export default function TabsLayout() {
  const unread = useUnreadCount();
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textSecondary,
        tabBarLabelStyle: { fontSize: 11, fontWeight: '600', marginBottom: Platform.OS === 'web' ? 6 : 0 },
        tabBarItemStyle: { paddingTop: 6 },
        tabBarStyle: {
          backgroundColor: colors.card,
          borderTopColor: colors.border,
          minHeight: Platform.OS === 'ios' ? undefined : 64,
          borderTopLeftRadius: 20,
          borderTopRightRadius: 20,
        },
        tabBarHideOnKeyboard: true,
        sceneStyle: { backgroundColor: colors.background },
      }}
    >
      <Tabs.Screen name="home" options={{ title: 'Home', tabBarIcon: icon('home', 'home-outline') }} />
      <Tabs.Screen name="explore" options={{ title: 'Explore', tabBarIcon: icon('compass', 'compass-outline') }} />
      {/* Practice is reachable from Home's quick actions; five tabs keeps the bar readable on phones. */}
      <Tabs.Screen name="practice" options={{ title: 'Practice', href: null }} />
      <Tabs.Screen name="ai" options={{ title: 'AI', tabBarIcon: icon('sparkles', 'sparkles-outline'), tabBarAccessibilityLabel: 'AI study tools' }} />
      <Tabs.Screen name="reports" options={{ title: 'Reports', tabBarIcon: icon('bar-chart', 'bar-chart-outline') }} />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: icon('person-circle', 'person-circle-outline'),
          tabBarBadge: unread > 0 ? unread : undefined,
          tabBarAccessibilityLabel: unread > 0 ? `Profile, ${unread} unread notifications` : 'Profile',
        }}
      />
    </Tabs>
  );
}
