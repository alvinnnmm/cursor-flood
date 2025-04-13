import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class FloodPredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.thresholds = {
            'Temperature (°F)': 30,
            'Humidity (%)': 80,
            'Wind Speed (mph)': 20,
            'Pre': 1000
        }
        self.safe_house_coords = {
            'latitude': 1.5304,
            'longitude': 110.3442
        }
        self.current_location = {
            'latitude': 0,
            'longitude': 0
        }
        
        # Create models directory if it doesn't exist
        if not os.path.exists('models'):
            os.makedirs('models')
        
        # Try to load existing model
        try:
            self.model = joblib.load('models/flood_prediction_model.joblib')
            print("Loaded existing model")
        except:
            print("No existing model found, will train a new one")
    
    def update_current_location(self, latitude: float, longitude: float):
        self.current_location = {
            'latitude': latitude,
            'longitude': longitude
        }
    
    def check_thresholds(self, data: dict) -> list:
        alerts = []
        for key, value in data.items():
            if key in self.thresholds:
                if key == 'Pre' and value < self.thresholds[key]:
                    alerts.append(f"{key} below threshold")
                elif value > self.thresholds[key]:
                    alerts.append(f"{key} above threshold")
        return alerts
    
    def predict_flood_risk(self, data: dict) -> tuple:
        if self.model is None:
            return 0.5, "Medium"
        
        # Prepare features
        features = pd.DataFrame([data])
        
        # Make prediction
        risk = self.model.predict_proba(features)[0][1]
        
        # Determine risk level
        if risk < 0.3:
            level = "Low"
        elif risk < 0.6:
            level = "Medium"
        else:
            level = "High"
        
        return risk, level
    
    def train_model(self, data_path: str):
        try:
            # Load data
            df = pd.read_excel(data_path)
            print("Data loaded successfully")
            print("\nData Preview:")
            print(df.head())
            
            # Prepare features and target
            X = df[['Temperature (°F)', 'Humidity (%)', 'Wind Speed (mph)', 'Pre']]
            y = df['Flood_Occurred']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)
            
            # Save model
            joblib.dump(self.model, 'models/flood_prediction_model.joblib')
            print("\nModel trained and saved successfully")
            
            # Print feature importance
            print("\nFeature Importance:")
            for feature, importance in zip(X.columns, self.model.feature_importances_):
                print(f"{feature}: {importance:.4f}")
            
        except Exception as e:
            print(f"Error during model training: {str(e)}")
            raise 