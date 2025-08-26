import React, { FC } from 'react';
import { View, Text, StyleSheet } from 'react-native';

const TourismDashboard: FC = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tourism Officer Dashboard</Text>
    </View>
  );
};
const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 22, fontWeight: 'bold' },
});
export default TourismDashboard;
