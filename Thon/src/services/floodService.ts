import axios from 'axios';

export interface WeatherData {
    temperature: number;
    humidity: number;
    wind_speed: number;
    pressure: number;
    latitude: number;
    longitude: number;
}

export interface PredictionResult {
    risk: number;
    level: string;
    alerts: string[];
    should_navigate: boolean;
    safe_house_coords?: {
        latitude: number;
        longitude: number;
    };
}

export interface Thresholds {
    'Temperature (°F)': number;
    'Humidity (%)': number;
    'Wind Speed (mph)': number;
    'Pre': number;
}

class FloodService {
    private baseUrl = 'http://10.100.11.44:8001/api'; // Backend API address

    async getThresholds(): Promise<Thresholds> {
        try {
            const response = await axios.get(`${this.baseUrl}/thresholds`);
            return response.data as Thresholds;
        } catch (error) {
            console.error('Error fetching thresholds:', error);
            // Return default thresholds
            return {
                'Temperature (°F)': 30,
                'Humidity (%)': 80,
                'Wind Speed (mph)': 20,
                'Pre': 1000
            };
        }
    }

    async predictFlood(weatherData: WeatherData): Promise<PredictionResult> {
        try {
            const response = await axios.post(`${this.baseUrl}/predict`, weatherData);
            return response.data as PredictionResult;
        } catch (error) {
            console.error('Error predicting flood:', error);
            // Return default prediction result
            return {
                risk: 0,
                level: 'Low',
                alerts: [],
                should_navigate: false
            };
        }
    }

    calculateRiskLevel(riskValue: number): string {
        if (riskValue < 0.3) return 'Low';
        if (riskValue < 0.6) return 'Medium';
        return 'High';
    }

    generateAlerts(weatherData: WeatherData, thresholds: Thresholds): string[] {
        const alerts: string[] = [];

        if (weatherData.temperature > thresholds['Temperature (°F)']) {
            alerts.push('Temperature exceeds threshold, may increase flood risk');
        }

        if (weatherData.humidity > thresholds['Humidity (%)']) {
            alerts.push('Humidity exceeds threshold, may increase flood risk');
        }

        if (weatherData.wind_speed > thresholds['Wind Speed (mph)']) {
            alerts.push('Wind speed exceeds threshold, may increase flood risk');
        }

        if (weatherData.pressure < thresholds['Pre']) {
            alerts.push('Pressure below threshold, may increase flood risk');
        }

        return alerts;
    }

    getGoogleMapsUrl(coords: { latitude: number; longitude: number }): string {
        return `https://www.google.com/maps/dir/?api=1&destination=${coords.latitude},${coords.longitude}`;
    }
}

export const floodService = new FloodService(); 