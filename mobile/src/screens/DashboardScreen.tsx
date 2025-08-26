//This is dummy dashboard screen for the app
// It will be replaced with the actual dashboard screen later
import React, { FC } from 'react';
import { View, Text, StyleSheet } from 'react-native';

const DashboardScreen: FC = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Welcome to the Dashboard!</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  text: { fontSize: 20 },
});

export default DashboardScreen;
