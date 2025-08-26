// ARSceneScreen.tsx
import React, { FC } from 'react';
import { View, StyleSheet, Platform } from 'react-native';
import { WebView } from 'react-native-webview';

import { AR_BASE_URL } from '../../config/api';

const ARSceneScreen: FC = () => {
  const arUrl = `${AR_BASE_URL}/ar-view/`;

  return (
    <View style={styles.container}>
      <WebView
        source={{ uri: arUrl }}
        style={styles.webview}
        javaScriptEnabled
        allowsInlineMediaPlayback
        mediaPlaybackRequiresUserAction={false}
        originWhitelist={['*']}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  webview: {
    flex: 1,
  },
});

export default ARSceneScreen;
