import React, { useContext, FC } from 'react';
import {View, Text, StyleSheet, Button} from 'react-native';
import { AuthContext } from '../../context/AuthContext';

const BusinessDashboard: FC = () => {
  const { logout, user } = useContext(AuthContext);

return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, Owner {user?.username}!</Text>

      {/* Example: Admin Actions */}
      <Button title="Logout" color="red" onPress={logout} />
    </View>
  );
};

export default BusinessDashboard;

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 22, fontWeight: 'bold' },
});
