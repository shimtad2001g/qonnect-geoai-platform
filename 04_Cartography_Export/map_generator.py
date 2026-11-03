import folium
import json

def generate_qonnect_map(output_file="07_Frontend_Website/farm_map.html"):
    print("Generating automated Qonnect Cartography...")
    
    # 1. Initialize Map centered on Bale, Oromia (Sinana)
    m = folium.Map(location=[7.11, 39.96], zoom_start=12, tiles="OpenStreetMap")
    
    # 2. Define Farm Data (Simulating outputs from GeoAI Phase 3)
    farms = [
        {
            "farmer": "Abebe Kebede",
            "parcel_id": 1,
            "crop": "Durum Wheat",
            "area_ha": 2.8,
            "ndvi": 0.75,
            "yield_quintals": 130.61,
            "status": "Optimal",
            "color": "green",
            "coords": [[7.10, 39.95], [7.10, 39.98], [7.12, 39.98], [7.12, 39.95]]
        },
        {
            "farmer": "Abebe Kebede",
            "parcel_id": 2,
            "crop": "Highland Barley",
            "area_ha": 1.4,
            "ndvi": 0.35,
            "yield_quintals": 65.82,
            "status": "High Stress (Drought/Pest)",
            "color": "red",
            "coords": [[7.13, 39.96], [7.13, 39.99], [7.15, 39.99], [7.15, 39.96]]
        }
    ]
    
    # 3. Create the Polygons and Popups
    for farm in farms:
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4><b>{farm['farmer']}</b></h4>
            <p><b>Crop:</b> {farm['crop']} ({farm['area_ha']} ha)</p>
            <p><b>Status:</b> <span style="color:{farm['color']};"><b>{farm['status']}</b></span></p>
            <p><b>GeoAI Yield Prediction:</b> {farm['yield_quintals']} quintals</p>
            <p><b>NDVI Score:</b> {farm['ndvi']}</p>
            <a href="https://sprout-qonnect-clnhwfubq2y6y9bafzg.streamlit.app/" target="_blank">Verify Traceability</a>
        </div>
        """
        
        folium.Polygon(
            locations=farm['coords'],
            color=farm['color'],
            fill=True,
            fill_color=farm['color'],
            fill_opacity=0.4,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{farm['farmer']} - {farm['crop']} ({farm['status']})"
        ).add_to(m)
        
    # 4. Save Map to HTML
    m.save(output_file)
    print(f"Map successfully saved to {output_file}")

if __name__ == "__main__":
    generate_qonnect_map()
