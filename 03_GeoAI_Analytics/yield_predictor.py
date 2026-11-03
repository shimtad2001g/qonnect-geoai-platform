import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import json

def train_yield_model():
    """
    Simulates training a Random Forest model using historical Qonnect data.
    Features: Mean_NDVI, Total_Rainfall, Area_Hectares, Soil_Type_Code
    Target: Yield_Quintals
    """
    print("Starting GeoAI Model Training...")
    
    # 1. Generate synthetic historical data (In production, this queries PostGIS)
    np.random.seed(42)
    num_samples = 500
    
    # Features
    mean_ndvi = np.random.uniform(0.3, 0.9, num_samples)
    total_rainfall = np.random.uniform(100, 600, num_samples)
    area_ha = np.random.uniform(1.0, 10.0, num_samples)
    
    # Target (Yield) - Highly correlated with NDVI and Rainfall
    # Formula: (Area * 20) + (NDVI * 50) + (Rainfall * 0.1) + Random Noise
    yield_quintals = (area_ha * 20) + (mean_ndvi * 50) + (total_rainfall * 0.1) + np.random.normal(0, 5, num_samples)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Mean_NDVI': mean_ndvi,
        'Total_Rainfall': total_rainfall,
        'Area_Hectares': area_ha,
        'Yield_Quintals': yield_quintals
    })
    
    # 2. Split Data
    X = df[['Mean_NDVI', 'Total_Rainfall', 'Area_Hectares']]
    y = df['Yield_Quintals']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Train Random Forest Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 4. Evaluate Model
    predictions = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"Model Trained Successfully!")
    print(f"Metrics -> RMSE: {rmse:.2f}, MAE: {mae:.2f}, R-squared: {r2:.2f}")
    
    return model

def predict_farm_yield(model, parcel_id, mean_ndvi, total_rainfall, area_ha):
    """
    Predicts yield for a specific Qonnect farm parcel.
    """
    features = pd.DataFrame([{
        'Mean_NDVI': mean_ndvi,
        'Total_Rainfall': total_rainfall,
        'Area_Hectares': area_ha
    }])
    
    predicted_yield = model.predict(features)[0]
    
    # Crop Health Stress Mapping
    stress_level = "Optimal"
    if mean_ndvi < 0.4:
        stress_level = "High Stress (Drought/Pest)"
    elif mean_ndvi < 0.6:
        stress_level = "Moderate Stress"
        
    result = {
        "parcel_id": parcel_id,
        "predicted_yield_quintals": round(predicted_yield, 2),
        "ndvi_score": round(mean_ndvi, 2),
        "crop_health_status": stress_level,
        "recommendation": "Irrigate immediately" if stress_level == "High Stress (Drought/Pest)" else "Maintain current agronomic practices"
    }
    
    print(f"\nPrediction for Parcel {parcel_id}:")
    print(json.dumps(result, indent=4))
    return result

if __name__ == "__main__":
    # Train the model
    rf_model = train_yield_model()
    
    # Test prediction (Example: Parcel 1 in Sinana, Bale - Healthy crop, good rain)
    predict_farm_yield(rf_model, parcel_id=1, mean_ndvi=0.75, total_rainfall=350, area_ha=2.8)
    
    # Test prediction (Example: Parcel 2 - Unhealthy crop, low rain)
    predict_farm_yield(rf_model, parcel_id=2, mean_ndvi=0.35, total_rainfall=120, area_ha=1.4)
