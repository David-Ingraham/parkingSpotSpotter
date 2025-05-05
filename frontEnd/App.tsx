// App.tsx
import React, {useState} from 'react';
import {
  View,
  Text,
  Button,
  Image,
  StyleSheet,
  PermissionsAndroid,
} from 'react-native';
import Geolocation from 'react-native-geolocation-service';

const SERVER_URL = 'http://10.0.2.2:8000/photo';

/* 1️⃣ ask for runtime permission (Android “dangerous” permission) ﻿*/
async function askPermission(): Promise<boolean> {
  const res = await PermissionsAndroid.request(
    PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
  );                               // Returns "granted" | "denied" | "never_ask_again"  :contentReference[oaicite:0]{index=0}
  return res === PermissionsAndroid.RESULTS.GRANTED;
}

/* 2️⃣ wrap Geolocation once  ﻿*/
async function getCoords(): Promise<{lat: number; lng: number}> {
  return new Promise((resolve, reject) => {
    Geolocation.getCurrentPosition(
      pos => resolve({lat: pos.coords.latitude, lng: pos.coords.longitude}),
      err => reject(err),
      {enableHighAccuracy: true, timeout: 15000, maximumAge: 10000}, // :contentReference[oaicite:1]{index=1}
    );
  });
}

/* 3️⃣ POST coords and receive base‑64 PNG  ﻿*/
async function fetchPhoto({ lat, lng }: { lat: number; lng: number }): Promise<string> {
  const res = await fetch(SERVER_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lat, lng }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);

  // expect PNG now, not JSON
  const base64 = await blobToBase64(await res.blob());
  return base64;                          // just the b64 string
}

/* helper lives in same file */
function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () =>
      resolve((reader.result as string).split(',')[1]); // strip "data:image/png;base64,"
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}


/* 4️⃣ custom hook orchestrating the flow  ﻿*/
function usePhoto() {
  const [coords, setCoords] = useState<{lat: number; lng: number} | null>(null);
  const [photo, setPhoto] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const start = async () => {
    setError(null); setLoading(true); setPhoto(null);
    try {
      if (!(await askPermission())) throw new Error('perm‑denied');
      const c = await getCoords();     setCoords(c);
      const imgB64 = await fetchPhoto(c);
      setPhoto(`data:image/jpeg;base64,${imgB64}`);      // RN Image accepts data‑URIs  :contentReference[oaicite:2]{index=2}
    } catch (e: any) {
      console.log(e);
      setError(e.message || 'unknown');
    } finally {
      setLoading(false);
    }
  };

  return {coords, photo, error, loading, start};
}

/* 5️⃣ UI layer – no networking logic inside ﻿*/
export default function App() {
  const {coords, photo, error, loading, start} = usePhoto();

  return (
    <View style={styles.container}>
      <Button title="Get Location" onPress={start} disabled={loading} />
      <Text>{coords ? `Lat ${coords.lat}  Lng ${coords.lng}` : ''}</Text>
      {error && <Text style={{color: 'red'}}>Error: {error}</Text>}
      {photo && <Image source={{uri: photo}} style={{width: 300, height: 200}} />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, alignItems: 'center', justifyContent: 'center'},
});
