import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")

print("Connecting to PostGIS to create table...")
try:
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    # Create the table with a PostGIS geometry column for mapping
    cur.execute("""
        CREATE TABLE IF NOT EXISTS farm_analytics (
            id SERIAL PRIMARY KEY,
            lat FLOAT,
            lon FLOAT,
            geom GEOGRAPHY(Point, 4326),
            date_analyzed DATE,
            cloud_cover FLOAT,
            ndvi FLOAT,
            crop_health VARCHAR(50)
        );
    """)
    print("✅ Table 'farm_analytics' created successfully!")
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Error creating table:", e)
