from typing import Dict, Optional
from models import VehicleStatus
from datetime import datetime

class VehicleStore:
    def __init__(self):
        self._vehicles: Dict[str, VehicleStatus] = {}

    def get_vehicle(self, vehicle_id: str) -> Optional[VehicleStatus]:
        return self._vehicles.get(vehicle_id)

    def update_vehicle(self, vehicle_id: str, zone_id: Optional[str], timestamp: datetime) -> VehicleStatus:
        status = "inside" if zone_id else "outside"
        vehicle_status = VehicleStatus(
            vehicle_id=vehicle_id,
            zone_id=zone_id,
            status=status,
            last_updated=timestamp
        )
        self._vehicles[vehicle_id] = vehicle_status
        return vehicle_status
