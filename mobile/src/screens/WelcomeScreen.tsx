// src/screens/WelcomeScreen.tsx
import React, { FC } from "react";
import {
  View,
  Text,
  StyleSheet,
  ImageBackground,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import { useNavigation } from "@react-navigation/native"; // Import useNavigation

const WelcomeScreen: FC = () => {
  const navigation = useNavigation<any>(); // Cast to any for now

  return (
    <ImageBackground
      source={require("../../assets/bicol_bg.jpg")} // replace with your tourism banner image
      style={styles.background}
    >
      <View style={styles.overlay}>
        <ScrollView contentContainerStyle={styles.container}>
          <Text style={styles.title}>Bicol Travel Guide</Text>
          <Text style={styles.subtitle}>
            Explore, Experience, and Enjoy the beauty of Bicol!
          </Text>

          <View style={styles.features}>
            <Text style={styles.feature}>• Discover Tourist Spots</Text>
            <Text style={styles.feature}>• Find Events and Festivals</Text>
            <Text style={styles.feature}>• Plan Your Travel with Ease</Text>
          </View>

          <TouchableOpacity
            style={styles.button}
            onPress={() => navigation.navigate("Login")}
          >
            <Text style={styles.buttonText}>Login</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.registerButton]}
            onPress={() => navigation.navigate("Register")}
          >
            <Text style={styles.buttonText}>Register</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>
    </ImageBackground>
  );
};

const styles = StyleSheet.create({
  background: {
    flex: 1,
    resizeMode: "cover",
  },
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.6)",
  },
  container: {
    flexGrow: 1,
    padding: 30,
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    fontSize: 36,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: "#ccc",
    textAlign: "center",
    marginBottom: 20,
  },
  features: {
    marginBottom: 30,
  },
  feature: {
    fontSize: 16,
    color: "#eee",
    marginVertical: 5,
  },
  button: {
    backgroundColor: "#007AFF",
    paddingVertical: 12,
    paddingHorizontal: 50,
    borderRadius: 8,
    marginVertical: 10,
  },
  registerButton: {
    backgroundColor: "#34C759",
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
  },
});

export default WelcomeScreen;
