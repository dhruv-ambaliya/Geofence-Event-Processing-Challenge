import requests
import time
import json

BASE_URL = "http://localhost:8000"

def send_event(vehicle_id, lat, lon):
    payload = {
        "vehicle_id": vehicle_id,
        "latitude": lat,
        "longitude": lon
    }
    try:
        response = requests.post(f"{BASE_URL}/events", json=payload)
        response.raise_for_status()
        print(f"Sent event: {payload}, Response: {response.json()}")
    except Exception as e:
        print(f"Error sending event: {e}")

def get_status(vehicle_id):
    try:
        response = requests.get(f"{BASE_URL}/vehicles/{vehicle_id}/status")
        response.raise_for_status()
        print(f"Status for {vehicle_id}: {response.json()}")
    except Exception as e:
        print(f"Error getting status: {e}")

def main():
    vehicle_id = "taxi-001"
    
    print("--- Starting Simulation ---")
    
    # 1. Start outside
    print("\n1. Vehicle starts outside any zone")
    send_event(vehicle_id, 0.0, -0.01)
    get_status(vehicle_id)
    time.sleep(1)

    # 2. Enter downtown (Polygon: (0,0) to (0.02, 0.02))
    print("\n2. Vehicle enters 'downtown'")
    send_event(vehicle_id, 0.01, 0.01) 
    get_status(vehicle_id)
    time.sleep(1)

    # 3. Move within downtown
    print("\n3. Vehicle moves within 'downtown'")
    send_event(vehicle_id, 0.015, 0.015)
    get_status(vehicle_id)
    time.sleep(1)

    # 4. Exit downtown
    print("\n4. Vehicle exits 'downtown'")
    send_event(vehicle_id, 0.03, 0.03)
    get_status(vehicle_id)
    time.sleep(1)
    
    # 5. Enter suburbs (Box: 0.03, 0.03 to 0.06, 0.04)
    # Note: 0.03, 0.03 is on the boundary of suburbs.
    print("\n5. Vehicle enters 'suburbs'")
    send_event(vehicle_id, 0.04, 0.035)
    get_status(vehicle_id)

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    main()
