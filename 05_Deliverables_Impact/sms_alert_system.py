def send_sms_alert(phone_number, farmer_name, parcel_id, status, recommendation):
    """
    Simulates sending an SMS/USSD alert to the farmer.
    In production, this connects to Twilio or Ethio Telecom API.
    """
    print(f"\n--- SMS Gateway Simulation ---")
    print(f"Sending to: {phone_number} ({farmer_name})")
    print(f"Message: QONNECT ALERT: Parcel {parcel_id} is {status}. Recommendation: {recommendation}.")
    print(f"------------------------------\n")
    return True

def process_farmers_for_alerts():
    # Simulate data from Phase 3
    farmers = [
        {
            "name": "Abebe Kebede",
            "phone": "+251911000001",
            "parcel_id": 1,
            "status": "Optimal",
            "recommendation": "Maintain current practices"
        },
        {
            "name": "Abebe Kebede",
            "phone": "+251911000001",
            "parcel_id": 2,
            "status": "High Stress (Drought/Pest)",
            "recommendation": "Irrigate immediately"
        }
    ]
    
    print("Processing Farmer Alerts...")
    for farmer in farmers:
        # Only send SMS if there is stress or an action needed
        if farmer["status"] != "Optimal":
            send_sms_alert(
                farmer["phone"], 
                farmer["name"], 
                farmer["parcel_id"], 
                farmer["status"], 
                farmer["recommendation"]
            )
        else:
            print(f"Skipping Parcel {farmer['parcel_id']} ({farmer['status']}) - No alert needed.")

if __name__ == "__main__":
    process_farmers_for_alerts()
