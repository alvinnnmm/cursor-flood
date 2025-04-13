from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model_trainer import FloodPredictor
import uvicorn

app = FastAPI()

# Allow CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize predictor
predictor = FloodPredictor()

class WeatherData(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    pressure: float
    latitude: float
    longitude: float

@app.post("/api/predict")
async def predict_flood(data: WeatherData):
    try:
        # Update current location
        predictor.update_current_location(data.latitude, data.longitude)
        
        # Prepare sensor data
        sensor_data = {
            'Temperature (°F)': data.temperature,
            'Humidity (%)': data.humidity,
            'Wind Speed (mph)': data.wind_speed,
            'Pre': data.pressure
        }
        
        # Check thresholds
        alerts = predictor.check_thresholds(sensor_data)
        
        # Predict risk
        risk, level = predictor.predict_flood_risk(sensor_data)
        
        # If navigation needed
        should_navigate = len(alerts) > 0
        
        return {
            "risk": risk,
            "level": level,
            "alerts": alerts,
            "should_navigate": should_navigate,
            "safe_house_coords": predictor.safe_house_coords
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/thresholds")
async def get_thresholds():
    return predictor.thresholds

@app.post("/api/update-thresholds")
async def update_thresholds(thresholds: dict):
    try:
        predictor.thresholds.update(thresholds)
        return {"message": "Thresholds updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001) 