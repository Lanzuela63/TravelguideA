import React, { useContext, FC } from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';
import { AuthContext } from '../../context/AuthContext';

const SettingsScreen: FC = () => {
  const { logout } = useContext(AuthContext);
  return (
    <View style={styles.container}>
      <Text style={styles.heading}>⚙️ Settings</Text>
      <Button title="Logout" color="red" onPress={logout} />
    </View>
  );
};

export default SettingsScreen;

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  heading: { fontSize: 22, fontWeight: 'bold', marginBottom: 12 },
});
