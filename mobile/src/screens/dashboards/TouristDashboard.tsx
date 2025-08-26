//mobile/src/screens/dashboards/TouristDashboard.tsx
import React, {useContext, useEffect, useState, FC} from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  Image,
  TouchableOpacity,
  ActivityIndicator,
  ScrollView,
  Alert // Added Alert for error messages
} from 'react-native';
import axios from 'axios';
import {AuthContext} from "../../context/AuthContext";

import { useNavigation } from '@react-navigation/native';

import { API_BASE_URL, AR_BASE_URL } from '../../config/api';

// Define interfaces for data structures
interface Location {
  name: string;
  region: string; // Added
  province: string; // Added
}

interface TouristSpot {
  id: number;
  name: string;
  location?: Location; // Optional, as it might not always be present or fully loaded
  description: string;
  image?: string; // Optional, as it might be null or undefined
}

const TouristDashboard: FC = () => {
  const navigation = useNavigation<any>(); // Cast to any for now
  const { userToken: accessToken } = useContext(AuthContext);
  const [spots, setSpots] = useState<TouristSpot[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTouristSpots();
  }, []);

  const fetchTouristSpots = async () => {
    try {
      const response = await axios.get<TouristSpot[]>(`${API_BASE_URL}/api/tourism-spots/`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setSpots(response.data);
    } catch (error: any) { // Explicitly type error as any
      console.error('Failed to load tourism spots:', error.message);
      setError('Failed to load tourist spots. Please try again later.');
      Alert.alert('Error', 'Failed to load tourist spots. Please try again later.'); // Use Alert.alert
    } finally {
      setLoading(false);
    }
  };

  const renderSpot = ({ item }: { item: TouristSpot }) => (
    <View style={styles.card}>
      <Image
        source={{ uri: item.image || "https://via.placeholder.com/300x200" }}
        style={styles.image}
      />
      <View style={styles.cardBody}>
        <Text style={styles.title}>{item.name}</Text>
        <Text style={styles.subtitle}>{item.location?.name}</Text>
        <Text style={styles.description} numberOfLines={2}>
          {item.description}
        </Text>
        <TouchableOpacity
          style={styles.exploreButton}
          onPress={() => navigation.navigate('AR', { screen: 'ARView', params: { spot_id: item.id, arUrl: `${AR_BASE_URL}/webar/${item.id}/` } })}
        >
          <Text style={styles.exploreButtonText}>Explore in AR</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text>Loading tourist spots...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorText}>{error}</Text>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.heading}>🏞 Featured Tourist Spots</Text>
      <TouchableOpacity
        style={styles.locationArButton}
        onPress={() => navigation.navigate('AR', { screen: 'LocationARView', params: { arUrl: `${AR_BASE_URL}/location/` } })}
      >
        <Text style={styles.exploreButtonText}>Open Location AR</Text>
      </TouchableOpacity>
      <FlatList
        data={spots}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderSpot}
        contentContainerStyle={styles.list}
        scrollEnabled={false}
      />
    </ScrollView>
  );
};

export default TouristDashboard;

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#f8f9fa',
    paddingTop: 20,
    paddingHorizontal: 10,
  },
  heading: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
  list: {
    paddingBottom: 20,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 10,
    marginBottom: 15,
    overflow: 'hidden',
    elevation: 3,
  },
  image: {
    height: 180,
    width: '100%',
  },
  cardBody: {
    padding: 12,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  subtitle: {
    fontSize: 14,
    color: '#777',
    marginBottom: 5,
  },
  description: {
    fontSize: 13,
    color: '#555',
    marginBottom: 10, // Added for better spacing
  },
  exploreButton: {
    marginTop: 10,
    backgroundColor: '#4CAF50',
    padding: 8,
    borderRadius: 5,
  },
  exploreButtonText: {
    color: '#fff',
    textAlign: 'center',
    fontWeight: 'bold',
  },
  locationArButton: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 10,
    marginHorizontal: 20,
    marginBottom: 20,
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  errorText: {
    color: 'red',
    fontSize: 16,
    textAlign: 'center',
  },
});