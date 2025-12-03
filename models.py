from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LocationEvent(BaseModel):
    vehicle_id: str = Field(..., description="Unique identifier for the vehicle")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude of the vehicle")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude of the vehicle")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time of the event")

class VehicleStatus(BaseModel):
    vehicle_id: str
    zone_id: Optional[str] = None
    status: str = "outside"  # "inside" or "outside"
    last_updated: datetime
