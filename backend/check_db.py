import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT id, lat, lon, date_analyzed, ndvi, crop_health FROM farm_analytics;")
    rows = cur.fetchall()
    
    if len(rows) == 0:
        print("❌ TABLE IS EMPTY. The insert failed or has not run yet.")
    else:
        print(f"✅ SUCCESS! Found {len(rows)} rows in the database:")
        print("-" * 50)
        for row in rows:
            print(f"ID: {row[0]} | Lat: {row[1]} | Lon: {row[2]} | Date: {row[3]} | NDVI: {row[4]} | Health: {row[5]}")
        print("-" * 50)
        
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Query failed: {e}")
