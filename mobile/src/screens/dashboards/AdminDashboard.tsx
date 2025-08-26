import React, { useContext, FC } from 'react';
import { View, Text, Button, StyleSheet, Alert } from 'react-native'; // Added Alert
import { AuthContext } from '../../context/AuthContext';

const AdminDashboard: FC = () => {
  const { logout, user } = useContext(AuthContext);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, Admin {user?.username}!</Text>

      {/* Example: Admin Actions */}
      <Button title="Manage Users" onPress={() => Alert.alert('Manage Users')} />
      <Button title="Manage Content" onPress={() => Alert.alert('Manage Content')} />
      <Button title="Logout" color="red" onPress={logout} />
    </View>
  );
};

export default AdminDashboard;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 20,
  },
});