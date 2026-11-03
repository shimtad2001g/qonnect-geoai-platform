import ee

def fetch_weather_data(aoi_coords, start_date, end_date):
    ee.Initialize()
    
    # Define AOI
    aoi = ee.Geometry.Polygon(aoi_coords)
    
    # 1. Fetch CHIRPS Daily Rainfall Data
    chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
        .filterBounds(aoi) \
        .filterDate(start_date, end_date)
    
    # Calculate total rainfall for the period
    total_rainfall = chirps.sum()
    
    # Extract the value for the specific farm polygon
    rainfall_value = total_rainfall.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=aoi,
        scale=5000
    )
    
    print(f"Total Rainfall (mm): {rainfall_value.getInfo()}")
    return rainfall_value

if __name__ == "__main__":
    # Sample polygon for Sinana, Bale
    sample_aoi = [[39.95, 7.10], [39.98, 7.10], [39.98, 7.12], [39.95, 7.12]]
    fetch_weather_data(sample_aoi, '2026-01-01', '2026-03-01')
