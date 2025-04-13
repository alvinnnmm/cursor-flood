import React from 'react';
import { StyleSheet, View, Text, SafeAreaView, StatusBar } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const SensorCard = ({ title, value, unit, icon }: { title: string; value: number; unit: string; icon: string }) => (
  <View style={styles.card}>
    <View style={styles.cardHeader}>
      <Ionicons name={icon as any} size={20} color="#666" />
      <Text style={styles.cardTitle}>{title}</Text>
    </View>
    <Text style={styles.cardValue}>{value}{unit}</Text>
  </View>
);

const LocationCard = () => (
  <View style={styles.locationCard}>
    <View style={styles.cardHeader}>
      <Ionicons name="location" size={20} color="#666" />
      <Text style={styles.locationTitle}>Current Location</Text>
    </View>
    <Text style={styles.locationValue}>Malaysia, Sibu</Text>
  </View>
);

const SafeLocationCard = () => (
  <View style={styles.safeLocationCard}>
    <View style={styles.cardHeader}>
      <Ionicons name="shield-checkmark" size={20} color="#4CAF50" />
      <Text style={styles.safeLocationTitle}>Nearby Safe Location</Text>
    </View>
    <View style={styles.safeStatusContainer}>
      <View style={styles.safeStatusIndicator} />
      <Text style={styles.safeStatusText}>Dewan Chancellor Hall</Text>
    </View>
    <Text style={styles.safeLocationDescription}>
       Your current location is consider safe
    </Text>
  </View>
);

const HintCard = () => (
  <View style={styles.hintCard}>
    <View style={styles.cardHeader}>
      <Ionicons name="alert-circle" size={20} color="#666" />
      <Text style={styles.hintTitle}>Hint</Text>
    </View>
    <View style={styles.hintContent}>
      <Text style={styles.hintText}>Avoid any electrical appliances during flood time!</Text>
    </View>
  </View>
);

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <View style={styles.header}>
        <Ionicons name="shield" size={40} color="white" />
        <Text style={styles.headerText}>SAFE</Text>
      </View>
      <View style={styles.content}>
        <View style={styles.row}>
          <SensorCard title="Humidity" value={65} unit="%" icon="water" />
          <SensorCard title="Temperature" value={28} unit="°C" icon="thermometer" />
        </View>
        <View style={styles.row}>
          <SensorCard title="Light Intensity" value={9000} unit="lux" icon="sunny" />
          <SensorCard title="Water Level" value={80} unit="%" icon="water" />
        </View>
        <LocationCard />
        <SafeLocationCard />
        <HintCard />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    height: '35%',
    backgroundColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerText: {
    color: 'white',
    fontSize: 35,
    fontWeight: 800,
    marginTop: 10,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    width: '48%',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  cardTitle: {
    fontSize: 16,
    color: '#666',
    marginLeft: 8,
  },
  cardValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  locationCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginTop: 0,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  locationTitle: {
    fontSize: 16,
    color: '#666',
    marginLeft: 8,
  },
  locationValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  safeLocationCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  safeLocationTitle: {
    fontSize: 16,
    color: '#666',
    marginLeft: 8,
  },
  safeStatusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  safeStatusIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#4CAF50',
    marginRight: 8,
  },
  safeStatusText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  safeLocationDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  hintCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  hintTitle: {
    fontSize: 16,
    color: '#666',
    marginLeft: 8,
  },
  hintContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  hintText: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
}); 