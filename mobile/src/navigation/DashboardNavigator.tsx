import React, { useContext } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { AuthContext } from '../context/AuthContext';

import AdminDashboard from '../screens/dashboards/AdminDashboard';
import BusinessDashboard from '../screens/dashboards/BusinessDashboard';
import EventDashboard from '../screens/dashboards/EventDashboard';
import TourismDashboard from '../screens/dashboards/TourismDashboard';
import TouristDashboard from '../screens/dashboards/TouristDashboard';
import ARSceneScreen from "../screens/ar/ARSceneScreen";

export type DashboardStackParamList = {
  AdminDashboard: undefined;
  BusinessDashboard: undefined;
  EventDashboard: undefined;
  TourismDashboard: undefined;
  TouristDashboard: undefined;
  ARScene: undefined; // Assuming no params are passed
};

const Stack = createNativeStackNavigator<DashboardStackParamList>();

const DashboardNavigator: React.FC = () => {
  const { user } = useContext(AuthContext);

  return (
    <Stack.Navigator>
      {user?.role === 'Admin' && (
        <Stack.Screen name="AdminDashboard" component={AdminDashboard} />
      )}
      {user?.role === 'Business Owner' && (
        <Stack.Screen name="BusinessDashboard" component={BusinessDashboard} />
      )}
      {user?.role === 'Event Organizer' && (
        <Stack.Screen name="EventDashboard" component={EventDashboard} />
      )}
      {user?.role === 'Tourism Officer' && (
        <Stack.Screen name="TourismDashboard" component={TourismDashboard} />
      )}
      {user?.role === 'Tourist' && (
        <Stack.Screen name="TouristDashboard" component={TouristDashboard} />
      )}
      {
        user?.role === 'Tourist' && (
            <Stack.Screen name="ARScene" component={ARSceneScreen} />
          )
      }
    </Stack.Navigator>
  );
};

export default DashboardNavigator;
