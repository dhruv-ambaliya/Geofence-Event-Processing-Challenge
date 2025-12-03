import logging
from fastapi import FastAPI, HTTPException
from models import LocationEvent, VehicleStatus
from geofence import GeofenceManager
from store import VehicleStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("geofence_service")

app = FastAPI(title="Geofence Service")

# Initialize components
geofence_manager = GeofenceManager()
vehicle_store = VehicleStore()

@app.post("/events", response_model=VehicleStatus)
async def receive_event(event: LocationEvent):
    """
    Process a location event from a vehicle.
    """
    logger.info(f"Received event for vehicle {event.vehicle_id} at ({event.latitude}, {event.longitude})")
    
    # Determine current zone
    current_zone = geofence_manager.get_containing_zone(event.latitude, event.longitude)
    
    # Get previous state to detect transitions
    previous_state = vehicle_store.get_vehicle(event.vehicle_id)
    
    # Update store
    new_state = vehicle_store.update_vehicle(event.vehicle_id, current_zone, event.timestamp)
    
    # Detect transitions
    if previous_state:
        if previous_state.zone_id != current_zone:
            if previous_state.zone_id and not current_zone:
                logger.info(f"Vehicle {event.vehicle_id} EXITED zone {previous_state.zone_id}")
            elif not previous_state.zone_id and current_zone:
                logger.info(f"Vehicle {event.vehicle_id} ENTERED zone {current_zone}")
            elif previous_state.zone_id and current_zone:
                logger.info(f"Vehicle {event.vehicle_id} MOVED from zone {previous_state.zone_id} to {current_zone}")
    elif current_zone:
         logger.info(f"Vehicle {event.vehicle_id} ENTERED zone {current_zone} (First sighting)")

    return new_state

@app.get("/vehicles/{vehicle_id}/status", response_model=VehicleStatus)
async def get_vehicle_status(vehicle_id: str):
    """
    Get the current status of a vehicle.
    """
    status = vehicle_store.get_vehicle(vehicle_id)
    if not status:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return status

@app.get("/")
async def root():
    return {"message": "Geofence Service is running"}
