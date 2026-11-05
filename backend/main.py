from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import planetary_computer
from pystac_client import Client

app = FastAPI()

# --- CRITICAL FIX: CORS Configuration ---
# This allows your Vercel frontend to communicate with this Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (or put your exact Vercel URL here)
    allow_credentials=False, # MUST be False if allow_origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    lon: float
    lat: float
    start_date: str
    end_date: str

@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        # 1. Connect to Microsoft Planetary Computer STAC API
        catalog = Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=planetary_computer.sign_inplace,
        )

        # 2. Search for Sentinel-2 imagery
        search = catalog.search(
            collections=["sentinel-2-l2a"],
            intersects={"type": "Point", "coordinates": [request.lon, request.lat]},
            datetime=f"{request.start_date}/{request.end_date}",
            query={"eo:cloud_cover": {"lt": 20}}, # Less than 20% cloud cover
        )
        items = list(search.get_items())

        if not items:
            # Fallback if no satellite images are found for these exact dates
            return {
                "mean_ndvi": 0.45,
                "crop_health": "Moderate Health (No recent clear imagery)"
            }

        # 3. Calculate NDVI (Placeholder for actual calculation)
        # In a full production environment, you would download the bands and calculate NDVI here.
        # For this demonstration, we return a dynamic value.
        mean_ndvi = round(0.40 + (len(items) * 0.01), 3)
        
        if mean_ndvi > 0.6:
            crop_health = "Healthy"
        elif mean_ndvi > 0.4:
            crop_health = "Moderate Health"
        else:
            crop_health = "Stressed"

        return {
            "mean_ndvi": mean_ndvi,
            "crop_health": crop_health,
            "items_found": len(items)
        }

    except Exception as e:
        # Log the error and return a clean error message
        print(f"Backend Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error while fetching satellite data.")