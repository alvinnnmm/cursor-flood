import React, { useState, useEffect } from 'react';
import { floodService, WeatherData, PredictionResult, Thresholds } from '../services/floodService';

const FloodPrediction: React.FC = () => {
    const [weatherData, setWeatherData] = useState<WeatherData>({
        temperature: 0,
        humidity: 0,
        wind_speed: 0,
        pressure: 0,
        latitude: 0,
        longitude: 0
    });
    
    const [prediction, setPrediction] = useState<PredictionResult | null>(null);
    const [thresholds, setThresholds] = useState<Thresholds | null>(null);

    useEffect(() => {
        // Get current thresholds
        floodService.getThresholds()
            .then(setThresholds)
            .catch(console.error);
    }, []);

    const handlePredict = async () => {
        try {
            const result = await floodService.predictFlood(weatherData);
            setPrediction(result);
            
            if (result.should_navigate) {
                window.open(floodService.getGoogleMapsUrl(result.safe_house_coords), '_blank');
            }
        } catch (error) {
            console.error('Prediction failed:', error);
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setWeatherData(prev => ({
            ...prev,
            [name]: parseFloat(value)
        }));
    };

    return (
        <div className="flood-prediction">
            <h2>Flood Prediction System</h2>
            
            <div className="input-group">
                <label>Temperature (°F):</label>
                <input
                    type="number"
                    name="temperature"
                    value={weatherData.temperature}
                    onChange={handleInputChange}
                />
                {thresholds && <span>Threshold: {thresholds['Temperature (°F)']}°F</span>}
            </div>

            <div className="input-group">
                <label>Humidity (%):</label>
                <input
                    type="number"
                    name="humidity"
                    value={weatherData.humidity}
                    onChange={handleInputChange}
                />
                {thresholds && <span>Threshold: {thresholds['Humidity (%)']}%</span>}
            </div>

            <div className="input-group">
                <label>Wind Speed (mph):</label>
                <input
                    type="number"
                    name="wind_speed"
                    value={weatherData.wind_speed}
                    onChange={handleInputChange}
                />
                {thresholds && <span>Threshold: {thresholds['Wind Speed (mph)']} mph</span>}
            </div>

            <div className="input-group">
                <label>Pressure:</label>
                <input
                    type="number"
                    name="pressure"
                    value={weatherData.pressure}
                    onChange={handleInputChange}
                />
                {thresholds && <span>Threshold: {thresholds['Pre']}</span>}
            </div>

            <div className="input-group">
                <label>Latitude:</label>
                <input
                    type="number"
                    name="latitude"
                    value={weatherData.latitude}
                    onChange={handleInputChange}
                />
            </div>

            <div className="input-group">
                <label>Longitude:</label>
                <input
                    type="number"
                    name="longitude"
                    value={weatherData.longitude}
                    onChange={handleInputChange}
                />
            </div>

            <button onClick={handlePredict}>Predict Flood Risk</button>

            {prediction && (
                <div className="prediction-result">
                    <h3>Prediction Result</h3>
                    <p>Risk Value: {prediction.risk.toFixed(2)}</p>
                    <p>Risk Level: {prediction.level}</p>
                    
                    {prediction.alerts.length > 0 && (
                        <div className="alerts">
                            <h4>Alerts:</h4>
                            <ul>
                                {prediction.alerts.map((alert, index) => (
                                    <li key={index}>{alert}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default FloodPrediction; 