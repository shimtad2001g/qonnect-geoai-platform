import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("❌ Error: DATABASE_URL not found in .env file.")
    exit(1)

print("Connecting to PostGIS database...")

try:
    # Connect to the database
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    print("Enabling PostGIS extension...")
    # This command activates PostGIS in your Supabase database
    cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    
    # Query the PostGIS version to confirm it's active
    cur.execute("SELECT PostGIS_Version();")
    version = cur.fetchone()[0]
    
    print("✅ Successfully connected to the Cloud Database!")
    print(f"🌍 PostGIS is active. Version: {version}")
    
    cur.close()
    conn.close()

except Exception as e:
    print(f"❌ Connection failed. Error: {e}")
