// src/context/AuthContext.tsx
import React, { createContext, useState, useEffect, ReactNode, FC } from "react";
import axios from "axios";
import * as SecureStore from "expo-secure-store";
import { Alert } from "react-native";
import { API_BASE_URL } from "../config/api";

// Define the shape of the user object
interface User {
  username: string;
  email: string;
  role: string;
  // Add other user properties here as they are defined in your backend
}

// Define params for the register function for clarity
interface RegisterParams {
  username: string;
  email: string;
  password: string;
  role: string;
  navigation: any; // Using 'any' for navigation is okay for now
}

// Define the shape of the context data
interface AuthContextData {
  user: User | null;
  userToken: string | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (params: RegisterParams) => Promise<void>;
}

// Define the props for the AuthProvider
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const AuthProvider: FC<AuthProviderProps> = ({ children }) => {
  const [userToken, setUserToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // 🔐 Login Function
  const login = async (username: string, password: string) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/token/`, {
        username,
        password,
      });

      const { access, refresh } = response.data;

      await SecureStore.setItemAsync("accessToken", access);
      await SecureStore.setItemAsync("refreshToken", refresh);

      setUserToken(access);
      await fetchUserProfile(access);
    } catch (error: any) { // Fixed error type
      console.error("Login failed:", error.response?.data || error.message);
      const errorMessage = error.response?.data?.detail || "An unexpected error occurred.";
      Alert.alert("Login Failed", errorMessage);
    }
  };

  // 👤 Fetch Profile
  const fetchUserProfile = async (token: string) => {
    try {
      const profile = await axios.get<User>(`${API_BASE_URL}/api/auth/me/`, { // Corrected generic type
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUser(profile.data); // Corrected setUser call
    } catch (error: any) { // Fixed error type
      console.error("Fetching profile failed. Trying to refresh token...");
      await tryTokenRefresh(); // Retry with refresh token
    }
  };

  // 🔁 Refresh Token
  const tryTokenRefresh = async () => {
    try {
      const refreshToken = await SecureStore.getItemAsync("refreshToken");
      if (!refreshToken) throw new Error("No refresh token available");

      const res = await axios.post(`${API_BASE_URL}/api/auth/token/refresh/`, {
        refresh: refreshToken,
      });

      const { access } = res.data;
      await SecureStore.setItemAsync("accessToken", access);
      setUserToken(access);

      await fetchUserProfile(access); // fetching user profile again with new token
    } catch (error: any) { // Fixed error type
      console.error("Token refresh failed:", error.message);
      await logout();
    }
  };

  // 🚪 Logout,  temporary reset button to call
  const logout = async () => {
    await SecureStore.deleteItemAsync("accessToken");
    await SecureStore.deleteItemAsync("refreshToken");
    setUserToken(null);
    setUser(null);
  };

  // 🧠 Check Login on App Load
  const checkLoginStatus = async () => {
    try {
      const token = await SecureStore.getItemAsync("accessToken");
      if (token) {
        setUserToken(token);
        await fetchUserProfile(token);
      }
    } catch (error: any) { // Fixed error type
      console.error("Error checking login:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // 🆕 Register New User
  const register = async ({ username, email, password, role, navigation }: RegisterParams) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/register/`, {
        username,
        email,
        password,
        role,
      });

      if (response.status === 201) {
        Alert.alert("Success", "Account created!");
        navigation.navigate("Login"); // 👈 navigate after registration
      }
    } catch (err: any) { // Fixed error type
      console.error("Registration error:", err.response?.data || err.message);
      Alert.alert("Registration Failed", "Please try again.");
    }
  };

  // Run login check on app start
  useEffect(() => {
    checkLoginStatus();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        login,
        logout,
        register, // ✅ Include register here so screens can use it
        user,
        userToken,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};