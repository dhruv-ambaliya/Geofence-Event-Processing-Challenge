from shapely.geometry import Point, Polygon, box
from typing import List, Optional, Dict

class GeofenceManager:
    def __init__(self):
        # Define some sample zones
        # In a real app, these would come from a DB or config file
        self.zones = {
            "downtown": Polygon([
                (0.0, 0.0), (0.0, 0.02), (0.02, 0.02), (0.02, 0.0)
            ]),
            "airport": Point(0.05, 0.05).buffer(0.01),  # Circular zone
            "suburbs": box(0.03, 0.03, 0.06, 0.04) # Rectangular zone
        }

    def get_containing_zone(self, lat: float, lon: float) -> Optional[str]:
        """
        Returns the ID of the zone containing the point, or None if outside all zones.
        Assumes non-overlapping zones for simplicity.
        """
        point = Point(lat, lon) # Note: Shapely uses (x, y), so (lat, lon) mapping depends on convention. 
        # Usually (lon, lat) is (x, y). Let's stick to (lat, lon) as (x, y) for this abstract challenge 
        # unless we want to be strictly GIS correct. 
        # Let's use (lat, lon) as (x, y) for simplicity as the challenge is abstract.
        
        for zone_id, zone_shape in self.zones.items():
            if zone_shape.contains(point):
                return zone_id
        return None
