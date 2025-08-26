import 'react-native-gesture-handler';
import React from "react";
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { AuthProvider } from "./src/context/AuthContext";
import AppNavigator from "./src/navigation/AppNavigator";
import { Provider as PaperProvider } from 'react-native-paper'

export default function App() {
  return (
      <GestureHandlerRootView style={{ flex: 1 }}>
      <PaperProvider>
      <AuthProvider>
        <AppNavigator />
      </AuthProvider>
    </PaperProvider>
    </GestureHandlerRootView>
  );
}
