import AsyncStorage from '@react-native-async-storage/async-storage';

export const logout = async (): Promise<boolean> => {
  const refresh: string | null = await AsyncStorage.getItem('refreshToken');

  const response = await fetch('https://192.168.20.7:8000/api/auth/logout/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  });

  if (response.ok) {
    await AsyncStorage.removeItem('accessToken');
    await AsyncStorage.removeItem('refreshToken');
    return true;
  }

  return false;
};
