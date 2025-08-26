import React, { useContext, FC } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { AuthContext } from '../../context/AuthContext';

const ProfileScreen: FC = () => {
  const { user } = useContext(AuthContext);
  return (
    <View style={styles.container}>
      <Text style={styles.heading}>👤 Your Profile</Text>
      <Text>Username: {user?.username}</Text>
      <Text>Email: {user?.email}</Text>
      <Text>Role: {user?.role}</Text>
    </View>
  );
};

export default ProfileScreen;

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  heading: { fontSize: 22, fontWeight: 'bold', marginBottom: 12 },
});
