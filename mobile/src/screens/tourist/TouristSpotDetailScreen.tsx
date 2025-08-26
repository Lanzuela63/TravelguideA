import React, { FC } from 'react';
import { View, Text, StyleSheet, Image, ScrollView } from 'react-native';
import { Card, Title, Paragraph } from 'react-native-paper';

// Reusing TouristSpot interface from other files
interface Location {
  name: string;
}

interface TouristSpot {
  id: number;
  name: string;
  location?: Location;
  description: string;
  image?: string;
}

const TouristSpotDetailScreen: FC<{ route: any }> = ({ route }) => { // route is typed as any
  const { spot } = route.params;

  return (
    <ScrollView style={styles.container}>
      <Card>
        <Card.Cover source={{ uri: spot.image || 'https://via.placeholder.com/400x200' }} />
        <Card.Content>
          <Title style={styles.title}>{spot.name}</Title>
          <Paragraph style={styles.location}>{spot.location?.name}</Paragraph>
          <Paragraph style={styles.description}>{spot.description}</Paragraph>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 10,
  },
  location: {
    fontSize: 16,
    color: 'gray',
    marginBottom: 10,
  },
  description: {
    fontSize: 16,
    lineHeight: 24,
  },
});

export default TouristSpotDetailScreen;
