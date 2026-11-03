-- Enable PostGIS for spatial tracking
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create the Farmers Table (Qonnect Identity)
CREATE TABLE farmers (
    farmer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    woreda VARCHAR(100)
);

-- Create the Farm Parcels Table (GeoAI Input)
CREATE TABLE farm_parcels (
    parcel_id SERIAL PRIMARY KEY,
    farmer_id INT REFERENCES farmers(farmer_id),
    crop_type VARCHAR(50),
    area_hectares DECIMAL(10,2),
    geom GEOMETRY(Polygon, 4326) -- The GPS Polygon from the Qonnect App
);
