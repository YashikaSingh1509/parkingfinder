import networkx as nx
import math

class ParkingRouter:
    def __init__(self):
        # Initialize graph for parking network
        self.graph = nx.Graph()
        
        # Predefined parking slots (mock data)
        self.parking_slots = [
            {
                "id": 1,
                "name": "City Center Parking",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "capacity": 100,
                "available": 50
            },
            {
                "id": 2,
                "name": "Downtown Parking",
                "latitude": 40.7150,
                "longitude": -74.0080,
                "capacity": 75,
                "available": 30
            }
        ]
    
    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate distance between two geographical points
        """
        R = 6371  # Earth's radius in kilometers
        
        # Convert latitude and longitude to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def find_nearest_parking(self, user_lat, user_lon):
        """
        Find nearest available parking slot using Dijkstra's algorithm
        """
        # Find closest parking slot
        nearest_slot = min(
            self.parking_slots, 
            key=lambda slot: self._haversine_distance(
                user_lat, user_lon, 
                slot['latitude'], slot['longitude']
            )
        )
        
        # Check slot availability
        if nearest_slot['available'] > 0:
            return {
                "slot": nearest_slot,
                "distance": self._haversine_distance(
                    user_lat, user_lon, 
                    nearest_slot['latitude'], 
                    nearest_slot['longitude']
                )
            }
        
        return None