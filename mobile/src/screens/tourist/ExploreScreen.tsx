//mobile/src/screens/tourist/ExploreScreen.tsx
import React, { useContext, useEffect, useState, useCallback, FC } from 'react';
import {
  View,
  Text,
  FlatList,
  TextInput,
  StyleSheet,
  ActivityIndicator,
  TouchableOpacity,
  Image,
  Alert, // Added Alert for error messages
} from 'react-native';
import axios from 'axios';
import { AuthContext } from "../../context/AuthContext";
import { debounce } from 'lodash';
import { useNavigation } from '@react-navigation/native'; // Removed NavigationProp import

// Assuming API_BASE_URL is imported from config/api
import { API_BASE_URL } from '../../config/api';

// Define interfaces for data structures (reusing from TouristDashboard if possible)
interface Location {
  name: string;
  // Add other location properties if they exist
}

interface TouristSpot {
  id: number;
  name: string;
  location?: Location; // Optional, as it might not always be present or fully loaded
  description: string;
  image?: string; // Optional, as it might be null or undefined
}

// Removed ExploreScreenNavigationProp type definition

const ExploreScreen: FC = () => {
  const { userToken: accessToken } = useContext(AuthContext);
  const [spots, setSpots] = useState<TouristSpot[]>([]);
  const [search, setSearch] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const navigation = useNavigation<any>(); // Cast to any for now

  const fetchTouristSpots = async (searchTerm: string) => {
    setLoading(true);
    try {
      const response = await axios.get<TouristSpot[]>(`${API_BASE_URL}/api/tourism-spots/?search=${searchTerm}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setSpots(response.data);
    } catch (err: any) { // Explicitly type error as any
      console.error('Failed to load spots:', err);
      Alert.alert('Error', 'Failed to load tourist spots. Please try again later.'); // Use Alert.alert
    } finally {
      setLoading(false);
    }
  };

  const debouncedFetch = useCallback(debounce(fetchTouristSpots, 500), [accessToken]);

  useEffect(() => {
    debouncedFetch(search);
  }, [search, debouncedFetch]);

  const renderContent = () => {
    if (loading) {
      return <ActivityIndicator size="large" color="#007AFF" style={styles.centered} />;
    }

    if (spots.length === 0) {
      return <Text style={styles.centered}>No results found.</Text>;
    }

    return (
      <FlatList
        data={spots}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }: { item: TouristSpot }) => (
          <TouchableOpacity onPress={() => navigation.navigate('TouristSpotDetail', { spot: item })}>
            <View style={styles.card}>
              <Image source={{ uri: item.image || 'https://via.placeholder.com/300x200' }} style={styles.image} />
              <View style={styles.cardBody}>
                <Text style={styles.title}>{item.name}</Text>
                <Text style={styles.location}>{item.location?.name}</Text>
              </View>
            </View>
          </TouchableOpacity>
        )}
      />
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.heading}>Explore Tourist Spots</Text>
      <TextInput
        placeholder="Search by category or location"
        style={styles.input}
        value={search}
        onChangeText={setSearch}
      />
      {renderContent()}
    </View>
  );
};

export default ExploreScreen;

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#f8f9fa' },
  heading: { fontSize: 22, fontWeight: 'bold', marginBottom: 12 },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    marginBottom: 12,
    borderRadius: 8,
    backgroundColor: '#fff',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 10,
    marginBottom: 15,
    overflow: 'hidden',
    elevation: 3,
    flexDirection: 'row',
  },
  image: {
    width: 100,
    height: 100,
  },
  cardBody: {
    padding: 12,
    flex: 1,
  },
  title: { 
    fontSize: 16, 
    fontWeight: 'bold', 
    color: '#333',
  },
  location: {
    fontSize: 14,
    color: '#777',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});