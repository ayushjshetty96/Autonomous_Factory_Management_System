"""
Factory Layout Module
Defines the factory floor layout and zones.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ZoneType(Enum):
    """Types of zones in the factory."""
    ASSEMBLY = "assembly"
    TRANSPORT = "transport"
    STORAGE = "storage"
    INSPECTION = "inspection"
    PACKAGING = "packaging"
    CHARGING = "charging"
    MAINTENANCE = "maintenance"
    OFFICE = "office"


@dataclass
class Zone:
    """Represents a zone in the factory."""
    zone_id: str
    zone_type: ZoneType
    name: str
    position: Tuple[float, float]  # (x, y)
    width: float
    height: float
    max_capacity: int = 100
    current_occupancy: int = 0
    
    @property
    def center(self) -> Tuple[float, float]:
        """Get the center of the zone."""
        x, y = self.position
        return (x + self.width / 2, y + self.height / 2)
    
    @property
    def area(self) -> float:
        """Get the area of the zone."""
        return self.width * self.height
    
    @property
    def occupancy_percent(self) -> float:
        """Get occupancy as percentage."""
        if self.max_capacity == 0:
            return 0.0
        return (self.current_occupancy / self.max_capacity) * 100
    
    def is_full(self) -> bool:
        """Check if zone is at capacity."""
        return self.current_occupancy >= self.max_capacity
    
    def add_robot(self) -> bool:
        """Add a robot to this zone."""
        if not self.is_full():
            self.current_occupancy += 1
            return True
        return False
    
    def remove_robot(self) -> bool:
        """Remove a robot from this zone."""
        if self.current_occupancy > 0:
            self.current_occupancy -= 1
            return True
        return False


class FactoryLayout:
    """Represents the factory floor layout."""
    
    def __init__(self, width: float, height: float):
        """
        Initialize the factory layout.
        
        Args:
            width: Factory floor width
            height: Factory floor height
        """
        self.width = width
        self.height = height
        self.zones: Dict[str, Zone] = {}
        self.connections: Dict[str, List[str]] = {}  # zone_id -> connected zone_ids
    
    def create_zone(
        self,
        zone_id: str,
        zone_type: ZoneType,
        name: str,
        position: Tuple[float, float],
        width: float,
        height: float,
        max_capacity: int = 100
    ) -> Zone:
        """
        Create a new zone in the factory.
        
        Args:
            zone_id: Unique identifier for the zone
            zone_type: Type of zone
            name: Human-readable name
            position: (x, y) position on factory floor
            width: Width of the zone
            height: Height of the zone
            max_capacity: Maximum capacity of the zone
        
        Returns:
            The created Zone object
        """
        zone = Zone(zone_id, zone_type, name, position, width, height, max_capacity)
        self.zones[zone_id] = zone
        self.connections[zone_id] = []
        return zone
    
    def connect_zones(self, zone_id_1: str, zone_id_2: str) -> None:
        """
        Connect two zones (bidirectional).
        
        Args:
            zone_id_1: First zone ID
            zone_id_2: Second zone ID
        """
        if zone_id_1 in self.zones and zone_id_2 in self.zones:
            if zone_id_2 not in self.connections[zone_id_1]:
                self.connections[zone_id_1].append(zone_id_2)
            if zone_id_1 not in self.connections[zone_id_2]:
                self.connections[zone_id_2].append(zone_id_1)
    
    def get_zone(self, zone_id: str) -> Optional[Zone]:
        """Get a zone by ID."""
        return self.zones.get(zone_id)
    
    def get_zones_by_type(self, zone_type: ZoneType) -> List[Zone]:
        """Get all zones of a specific type."""
        return [z for z in self.zones.values() if z.zone_type == zone_type]
    
    def find_nearest_zone(
        self,
        position: Tuple[float, float],
        zone_type: Optional[ZoneType] = None
    ) -> Optional[Zone]:
        """
        Find the nearest zone to a position.
        
        Args:
            position: (x, y) position
            zone_type: If specified, only search zones of this type
        
        Returns:
            The nearest zone, or None if no zones found
        """
        from utils.distance import euclidean_distance
        
        search_zones = self.zones.values()
        if zone_type:
            search_zones = self.get_zones_by_type(zone_type)
        
        if not search_zones:
            return None
        
        return min(search_zones, key=lambda z: euclidean_distance(position, z.center))
    
    def get_factory_status(self) -> Dict[str, any]:
        """Get overall factory status."""
        return {
            "dimensions": {"width": self.width, "height": self.height},
            "total_zones": len(self.zones),
            "zones": [
                {
                    "zone_id": z.zone_id,
                    "name": z.name,
                    "type": z.zone_type.value,
                    "occupancy": z.current_occupancy,
                    "capacity": z.max_capacity,
                    "occupancy_percent": z.occupancy_percent,
                }
                for z in self.zones.values()
            ],
            "total_capacity": sum(z.max_capacity for z in self.zones.values()),
            "total_occupancy": sum(z.current_occupancy for z in self.zones.values()),
        }


def create_default_factory() -> FactoryLayout:
    """
    Create a default factory layout with standard zones.
    
    Returns:
        A pre-configured FactoryLayout
    """
    factory = FactoryLayout(width=100.0, height=100.0)
    
    # Create zones
    factory.create_zone(
        "assembly_1", ZoneType.ASSEMBLY, "Assembly Line 1", (0, 0), 20, 20, max_capacity=5
    )
    factory.create_zone(
        "assembly_2", ZoneType.ASSEMBLY, "Assembly Line 2", (25, 0), 20, 20, max_capacity=5
    )
    factory.create_zone(
        "transport", ZoneType.TRANSPORT, "Transport Hub", (50, 0), 20, 20, max_capacity=3
    )
    factory.create_zone(
        "storage", ZoneType.STORAGE, "Warehouse", (75, 0), 20, 20, max_capacity=10
    )
    factory.create_zone(
        "inspection", ZoneType.INSPECTION, "Quality Control", (0, 30), 20, 20, max_capacity=3
    )
    factory.create_zone(
        "packaging", ZoneType.PACKAGING, "Packaging Area", (25, 30), 20, 20, max_capacity=5
    )
    factory.create_zone(
        "charging", ZoneType.CHARGING, "Charging Station", (75, 30), 20, 20, max_capacity=10
    )
    factory.create_zone(
        "maintenance", ZoneType.MAINTENANCE, "Maintenance Bay", (50, 30), 20, 20, max_capacity=2
    )
    
    # Connect zones
    factory.connect_zones("assembly_1", "transport")
    factory.connect_zones("assembly_2", "transport")
    factory.connect_zones("transport", "storage")
    factory.connect_zones("assembly_1", "inspection")
    factory.connect_zones("inspection", "packaging")
    factory.connect_zones("packaging", "storage")
    factory.connect_zones("storage", "charging")
    factory.connect_zones("transport", "maintenance")
    
    return factory
