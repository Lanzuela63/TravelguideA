import React, { FC } from 'react';
import { View, Text } from 'react-native';

// TODO: Define props for this component
interface SceneCardProps {}

const SceneCard: FC<SceneCardProps> = (props) => {
  return (
    <View>
      <Text>SceneCard Component</Text>
    </View>
  );
};

export default SceneCard;
