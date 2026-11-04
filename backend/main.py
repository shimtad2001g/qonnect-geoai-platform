from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pystac_client
import odc.stac
import planetary_computer
import numpy as np
import uvicorn
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Qonnect Spatial Intelligence API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class FarmRequest(BaseModel):
    lon: float
    lat: float
    start_date: str
    end_date: str

@app.get("/")
def read_root():
    return {"status": "Qonnect GeoAI Backend is running"}

@app.post("/api/analyze")
def analyze_farm(request: FarmRequest):
    try:
        catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier=planetary_computer.sign_inplace)
        buffer = 0.001
        bbox = [request.lon - buffer, request.lat - buffer, request.lon + buffer, request.lat + buffer]
        
        search = catalog.search(collections=["sentinel-2-l2a"], bbox=bbox, datetime=f"{request.start_date}/{request.end_date}")
        items = list(search.items())
        if not items:
            raise HTTPException(status_code=404, detail="No imagery found in this date range.")
            
        items.sort(key=lambda x: x.properties.get("eo:cloud_cover", 100))
        latest_image = items[0]
        
        data = odc.stac.load([latest_image], bbox=bbox, bands=["B04", "B08", "SCL"], resolution=10)
        red = data["B04"].astype(float)
        nir = data["B08"].astype(float)
        scl = data["SCL"]
        
        cloud_mask = scl.isin([3, 8, 9, 10])
        red = red.where(~cloud_mask)
        nir = nir.where(~cloud_mask)
        
        ndvi = (nir - red) / (nir + red)
        mean_ndvi = float(ndvi.mean().values)
        
        if np.isnan(mean_ndvi):
            raise HTTPException(status_code=404, detail="Image completely covered by clouds after masking.")
        
        health_status = "Excellent" if mean_ndvi > 0.6 else "Moderate" if mean_ndvi > 0.3 else "Poor"
        date_str = latest_image.datetime.strftime("%Y-%m-%d")
        cloud_cover = latest_image.properties.get("eo:cloud_cover")
        
        # --- NEW: SAVE TO POSTGIS ---
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            insert_query = """
                INSERT INTO farm_analytics (lat, lon, geom, date_analyzed, cloud_cover, ndvi, crop_health)
                VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s, %s, %s)
            """
            cur.execute(insert_query, (
                request.lat, request.lon, request.lon, request.lat,
                date_str, cloud_cover, round(mean_ndvi, 3), health_status
            ))
            conn.commit()
            cur.close()
            conn.close()
            print(f"✅ Data saved to PostGIS for {request.lat}, {request.lon}")
        except Exception as db_err:
            print(f"❌ Failed to save to PostGIS: {db_err}")
        # -----------------------------

        return {
            "status": "success", 
            "location": {"lat": request.lat, "lon": request.lon},
            "date_analyzed": date_str,
            "cloud_cover_metadata": cloud_cover,
            "mean_ndvi": round(mean_ndvi, 3),
            "crop_health": health_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
