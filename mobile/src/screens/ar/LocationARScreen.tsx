// mobile/src/screens/ar/LocationARScreen.tsx
import React, { FC, useEffect, useState } from 'react';
import { WebView } from 'react-native-webview';
import * as Location from 'expo-location';

import { AR_BASE_URL } from '../../config/api';

const LocationARScreen: FC = () => {
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setErrorMsg('Permission to access location was denied');
        return;
      }

      let currentLocation = await Location.getCurrentPositionAsync({});
      setLocation(currentLocation);
    })();
  }, []);

  const arUrl = `${AR_BASE_URL}/location/?_t=${new Date().getTime()}`;

  const injectedJavaScript = `
    window.ReactNativeWebView.postMessage('Injected JS: WebView is ready!');
    if (${location}) {
      window.ReactNativeWebView.postMessage(JSON.stringify({
        type: 'native_location',
        latitude: ${location?.coords.latitude},
        longitude: ${location?.coords.longitude},
        accuracy: ${location?.coords.accuracy},
      }));
    }
  `;

  return (
    <WebView
      source={{ uri: arUrl }}
      style={{ flex: 1 }}
      geolocationEnabled={true}
      javaScriptEnabled={true}
      domStorageEnabled={true}
      allowsInlineMediaPlayback
      mediaPlaybackRequiresUserAction={false}
      onPermissionRequest={(syntheticEvent) => {
        const { permissions, request } = syntheticEvent.nativeEvent;
        if (permissions.includes('geolocation')) {
          request.grant();
        }
      }}
      onLoad={() => console.log('WebView loaded successfully!')}
      onMessage={(event) => {
        console.log('Message from WebView:', event.nativeEvent.data);
      }}
      injectedJavaScript={injectedJavaScript}
    />
  );
};

export default LocationARScreen;
