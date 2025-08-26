// src/navigation/AppNavigator.tsx
import React, { useContext, ComponentType } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { ActivityIndicator, View } from "react-native";
import TouristTabNavigator from './TouristTabNavigator';

// Auth context
import { AuthContext } from "../context/AuthContext";

// Screens
import TouristDashboard from "../screens/dashboards/TouristDashboard";
import TourismDashboard from "../screens/dashboards/TourismDashboard";
import BusinessDashboard from "../screens/dashboards/BusinessDashboard";
import EventDashboard from "../screens/dashboards/EventDashboard";
import AdminDashboard from "../screens/dashboards/AdminDashboard";

// Importing the main HomeScreen for unauthenticated users
import HomeScreen from "../screens/HomeScreen";
import LoginScreen from "../screens/LoginScreen";
import RegisterScreen from "../screens/RegisterScreen";
import WelcomeScreen from "../screens/WelcomeScreen";

// Define Param lists for type safety
export type RootStackParamList = {
  Welcome: undefined;
  Home: undefined;
  Login: undefined;
  Register: undefined;
  Dashboard: undefined;
};

export type TouristStackParamList = {
    TouristDashboardMain: undefined;
    // Add other tourism screen params here
};

const Stack = createNativeStackNavigator<RootStackParamList>();
const TouristStack = createNativeStackNavigator<TouristStackParamList>();

const AppNavigator: React.FC = () => {
  const { user, isLoading } = useContext(AuthContext);

  // 🌀 Show loading indicator while checking login status
  if (isLoading) {
    return (
        <View style={{flex: 1, justifyContent: "center", alignItems: "center"}}>
          <ActivityIndicator size="large" color="#007AFF"/>
        </View>
    );
  }

  function TouristStackScreen() {
    return (
        <TouristStack.Navigator>
          <TouristStack.Screen
              name="TouristDashboardMain"
              component={TouristDashboard}
              options={{title: 'Tourist Dashboard'}}
          />
          {/* Add more tourism screens here */}
        </TouristStack.Navigator>
    );
  }

  // 🎯 Determine which screen to show based on role
  const getDashboardScreen = (): ComponentType => {
    switch (user?.role) {
      case "Admin":
        return AdminDashboard;
      case "Tourist":
        return TouristTabNavigator;
      case "Tourism Officer":
        return TourismDashboard;
      case "Business Owner":
        return BusinessDashboard;
      case "Event Organizer":
        return EventDashboard;
      default:
        return LoginScreen; // fallback for unknown role
    }
  };

  const DashboardComponent = getDashboardScreen(); // ✅ Don't call inside JSX

  return (
      <NavigationContainer>
        <Stack.Navigator screenOptions={{headerShown: false}}>
          {!user ? (
              <>
                <Stack.Screen name="Welcome" component={WelcomeScreen}/>
                <Stack.Screen name="Home" component={HomeScreen}/>
                <Stack.Screen name="Login" component={LoginScreen}/>
                <Stack.Screen name="Register" component={RegisterScreen}/>
              </>
          ) : (
              <Stack.Screen name="Dashboard" component={DashboardComponent}/>
          )}
        </Stack.Navigator>
      </NavigationContainer>
  );
}

export default AppNavigator;
