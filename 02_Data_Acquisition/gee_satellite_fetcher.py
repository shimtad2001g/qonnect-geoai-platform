import ee
import json

# Initialize Google Earth Engine (Requires authentication)
def init_gee():
    try:
        ee.Initialize()
        print("Google Earth Engine initialized successfully.")
    except Exception as e:
        print("Authentication required. Please run: earthengine authenticate")
        raise e

# Function to simulate fetching a Qonnect farmer's GPS polygon from PostGIS
def get_qonnect_farm_polygon(parcel_id):
    # Placeholder: In production, this queries PostgreSQL (PostGIS)
    # Example: SELECT ST_AsGeoJSON(geom) FROM farm_parcels WHERE parcel_id = 1;
    sample_polygon = [
        [39.95, 7.10],
        [39.98, 7.10],
        [39.98, 7.12],
        [39.95, 7.12],
        [39.95, 7.10]
    ]
    return ee.Geometry.Polygon(sample_polygon)

# Function to acquire Sentinel-2 Imagery and calculate NDVI
def fetch_sentinel_ndvi(parcel_id, start_date, end_date):
    init_gee()
    
    # 1. Get AOI (Area of Interest) from Qonnect DB
    aoi = get_qonnect_farm_polygon(parcel_id)
    
    # 2. Fetch Sentinel-2 Collection
    s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(aoi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    
    # 3. Calculate NDVI (Normalized Difference Vegetation Index)
    def add_ndvi(image):
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return image.addBands(ndvi)
    
    s2_with_ndvi = s2.map(add_ndvi)
    
    # 4. Create a time-series chart data (Mean NDVI per image)
    ndvi_timeseries = s2_with_ndvi.select('NDVI').mean().reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=aoi,
        scale=10
    )
    
    print(f"NDVI Data for Parcel {parcel_id}: {ndvi_timeseries.getInfo()}")
    return ndvi_timeseries

if __name__ == "__main__":
    # Example execution for Bale, Oromia (Harvest Season)
    fetch_sentinel_ndvi(parcel_id=1, start_date='2026-01-01', end_date='2026-03-01')
