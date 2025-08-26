import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';

// Screens
import TouristDashboard from '../screens/dashboards/TouristDashboard';
import ExploreScreen from '../screens/tourist/ExploreScreen';
import ProfileScreen from '../screens/tourist/ProfileScreen';
import SettingsScreen from '../screens/tourist/SettingsScreen';
import TouristSpotDetailScreen from '../screens/tourist/TouristSpotDetailScreen';
import ARScreen from '../screens/ar/ARScreen';
import LocationARScreen from '../screens/ar/LocationARScreen';

// Define Param Lists for type safety

export type ExploreStackParamList = {
  ExploreMain: undefined;
  TouristSpotDetail: { spotId: string };
};

export type ARStackParamList = {
  ARView: undefined;
  LocationARView: undefined;
};

// The tab navigator contains nested stack navigators
// Using 'object' as a temporary workaround for NavigatorScreenParams
export type TouristTabParamList = {
  Home: undefined;
  Explore: object;
  AR: object;
  Profile: undefined;
  Settings: undefined;
};

const Tab = createBottomTabNavigator<TouristTabParamList>();
const ExploreStack = createNativeStackNavigator<ExploreStackParamList>();
const ARStack = createNativeStackNavigator<ARStackParamList>();

function ExploreStackScreen() {
  return (
    <ExploreStack.Navigator>
      <ExploreStack.Screen name="ExploreMain" component={ExploreScreen} options={{ headerShown: false }} />
      <ExploreStack.Screen name="TouristSpotDetail" component={TouristSpotDetailScreen} />
    </ExploreStack.Navigator>
  );
}

function ARStackScreen() {
  return (
    <ARStack.Navigator>
      <ARStack.Screen name="ARView" component={ARScreen} options={{ headerShown: false }} />
      <ARStack.Screen name="LocationARView" component={LocationARScreen} options={{ title: 'Location AR' }} />
    </ARStack.Navigator>
  );
}

const TouristTabNavigator: React.FC = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }: { route: any }) => ({ // route is now 'any'
        tabBarIcon: ({ color, size }: { color: string, size: number }) => { // Explicitly type color and size
          let iconName: React.ComponentProps<typeof Ionicons>['name'] = 'help-circle'; // Default icon

          if (route.name === 'Home') iconName = 'home-outline';
          else if (route.name === 'Explore') iconName = 'search-outline';
          else if (route.name === 'AR') iconName = 'camera-outline';
          else if (route.name === 'Profile') iconName = 'person-outline';
          else if (route.name === 'Settings') iconName = 'settings-outline';
          
          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: 'gray',
        headerShown: false,
      })}
    >
      <Tab.Screen name="Home" component={TouristDashboard} />
      <Tab.Screen name="Explore" component={ExploreStackScreen} />
      <Tab.Screen name="AR" component={ARStackScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  );
}

export default TouristTabNavigator;
