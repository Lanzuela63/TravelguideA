import React, { useState, useContext, FC } from "react";
import {
  View,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import {
  Card,
  Title,
  TextInput,
  Button,
  IconButton,
  Text,
} from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import { AuthContext } from "../context/AuthContext";
import { AuthStackParamList } from '../navigation/AuthNavigator'; // Import AuthStackParamList

const LoginScreen: FC = () => {
  const navigation = useNavigation<any>(); // Changed to any
  const { login } = useContext(AuthContext);
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const handleLogin = async () => {
    if (!username || !password) return;
    await login(username, password);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        <Card style={styles.card}>
          <Card.Content>
            <View style={styles.header}>
              <IconButton icon="arrow-left" onPress={() => navigation.goBack()} />
              <Title style={styles.title}>Login to Your Account</Title>
            </View>

            <TextInput
              label="Username"
              value={username}
              onChangeText={setUsername}
              mode="outlined"
              style={styles.input}
              autoCapitalize="none"
            />

            <TextInput
              label="Password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              mode="outlined"
              style={styles.input}
            />

            <Button
              mode="contained"
              onPress={handleLogin}
              style={{ marginTop: 20 }}
            >
              Login
            </Button>

            <Text style={styles.registerText}>
              Don't have an account?{" "}
              <Text
                style={styles.linkText}
                onPress={() => navigation.navigate("Register")}
              >
                Register here
              </Text>
            </Text>
          </Card.Content>
        </Card>
      </KeyboardAvoidingView>
    </ScrollView>
  );
};

export default LoginScreen;

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: "center",
    padding: 20,
    backgroundColor: "#f0f4f8",
  },
  card: {
    padding: 10,
    borderRadius: 12,
    elevation: 4,
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
  },
  input: {
    marginBottom: 12,
  },
  registerText: {
    marginTop: 20,
    textAlign: "center",
  },
  linkText: {
    color: "#007BFF",
  },
});