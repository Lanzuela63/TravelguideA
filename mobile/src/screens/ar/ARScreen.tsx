// mobile/src/screens/ar/ARScreen.tsx
import React, { FC } from 'react';
import { WebView } from 'react-native-webview';

import { AR_BASE_URL } from '../../config/api';

const ARScreen: FC<{ route: any }> = ({ route }) => { // route is typed as any
  const { spot_id } = route.params;
  const arUrl = `${AR_BASE_URL}/webar/${spot_id}/`;

  return (
    <WebView
      source={{ uri: arUrl }}
      style={{ flex: 1 }}
      allowsInlineMediaPlayback
      mediaPlaybackRequiresUserAction={false}
      cameraDevice="front"
    />
  );
};

export default ARScreen;
