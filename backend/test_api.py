import requests
import json

url = "http://127.0.0.1:8000/api/analyze"
payload = {
    "lon": 36.8,   # Jimma region (Coffee)
    "lat": 7.6,
    "start_date": "2026-07-01",
    "end_date": "2026-09-30"
}

print("Testing a known agricultural area (Jimma) in the rainy season...")

try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", e)
