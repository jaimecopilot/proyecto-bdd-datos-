"""
Módulo de gestión de ocupación de salas de conferencias.
"""
from typing import Dict, List, Optional
from datetime import datetime


class RoomOccupancyError(Exception):
    """Excepción base para errores de ocupación de salas."""
    pass


class Room:
    """Clase que gestiona la ocupación de una sala de conferencias."""

    def __init__(self, capacity: int, name: str = "Sala Sin Nombre"):
        """
        Inicializa una sala con capacidad máxima especificada.
        
        Args:
            capacity: Número máximo de personas que puede albergar la sala
            name: Nombre identificador de la sala
        """
        if capacity <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        
        self.capacity = capacity
        self.name = name
        self.current_occupancy = 0
        self.movement_log = []
        self.created_at = datetime.now()

    def check_in(self, people_count: int) -> dict:
        """Registra la entrada de personas a la sala."""
        if people_count <= 0:
            return {"success": False, "message": "El número de personas debe ser positivo"}
        
        if self.current_occupancy + people_count > self.capacity:
            return {
                "success": False,
                "message": f"No hay capacidad. Intentas {people_count}, disponible {self.available_capacity()}"
            }
        
        self.current_occupancy += people_count
        self.movement_log.append({
            "type": "check_in",
            "count": people_count,
            "timestamp": datetime.now()
        })
        
        return {"success": True, "message": f"{people_count} personas han entrado"}

    def check_out(self, people_count: int) -> dict:
        """Registra la salida de personas de la sala."""
        if people_count <= 0:
            return {"success": False, "message": "El número de personas debe ser positivo"}
        
        if people_count > self.current_occupancy:
            return {
                "success": False,
                "message": f"No hay {people_count} personas en la sala. Actuales: {self.current_occupancy}"
            }
        
        self.current_occupancy -= people_count
        self.movement_log.append({
            "type": "check_out",
            "count": people_count,
            "timestamp": datetime.now()
        })
        
        return {"success": True, "message": f"{people_count} personas han salido"}

    def available_capacity(self) -> int:
        """Retorna la capacidad disponible de la sala."""
        return self.capacity - self.current_occupancy

    def occupancy_percentage(self) -> float:
        """Retorna el porcentaje de ocupación de la sala."""
        if self.capacity == 0:
            return 0.0
        return (self.current_occupancy / self.capacity) * 100

    def is_full(self) -> bool:
        """Retorna True si la sala está llena."""
        return self.current_occupancy == self.capacity

    def is_empty(self) -> bool:
        """Retorna True si la sala está vacía."""
        return self.current_occupancy == 0

    def reset(self) -> None:
        """Resetea la sala vaciándola y limpiando el registro de movimientos."""
        self.current_occupancy = 0
        self.movement_log = []

    def get_movement_log(self) -> list:
        """Retorna el registro de movimientos."""
        return self.movement_log.copy()

    def get_status(self) -> dict:
        """Retorna el estado completo de la sala."""
        return {
            "name": self.name,
            "capacity": self.capacity,
            "current_occupancy": self.current_occupancy,
            "available_capacity": self.available_capacity(),
            "occupancy_percentage": self.occupancy_percentage(),
            "is_full": self.is_full(),
            "is_empty": self.is_empty(),
            "movement_count": len(self.movement_log)
        }

    def __str__(self):
        return f"{self.name} ({self.current_occupancy}/{self.capacity})"

    def __repr__(self):
        return f"Room(name='{self.name}', capacity={self.capacity}, occupancy={self.current_occupancy})"


class RoomOccupancyService:
    """Servicio centralizado para gestionar múltiples salas."""

    def __init__(self):
        """Inicializa el servicio sin salas."""
        self.rooms: Dict[str, Room] = {}

    def add_room(self, room: Room) -> None:
        """Agrega una sala al servicio."""
        if room.name in self.rooms:
            raise ValueError(f"La sala '{room.name}' ya existe")
        self.rooms[room.name] = room

    def get_room(self, room_name: str) -> Optional[Room]:
        """Obtiene una sala por nombre."""
        return self.rooms.get(room_name)

    def remove_room(self, room_name: str) -> bool:
        """Elimina una sala del servicio."""
        if room_name in self.rooms:
            del self.rooms[room_name]
            return True
        return False

    def list_rooms(self) -> List[Dict]:
        """Lista todas las salas con su estado."""
        return [room.get_status() for room in self.rooms.values()]

    def get_available_rooms(self) -> List[Room]:
        """Retorna las salas con capacidad disponible."""
        return [room for room in self.rooms.values() if room.available_capacity() > 0]

    def get_full_rooms(self) -> List[Room]:
        """Retorna las salas llenas."""
        return [room for room in self.rooms.values() if room.is_full()]

    def get_empty_rooms(self) -> List[Room]:
        """Retorna las salas vacías."""
        return [room for room in self.rooms.values() if room.is_empty()]

    def get_occupancy_summary(self) -> dict:
        """Retorna un resumen de ocupación del servicio."""
        total_capacity = sum(room.capacity for room in self.rooms.values())
        total_occupancy = sum(room.current_occupancy for room in self.rooms.values())
        
        return {
            "total_rooms": len(self.rooms),
            "total_capacity": total_capacity,
            "total_occupancy": total_occupancy,
            "total_available": total_capacity - total_occupancy,
            "overall_percentage": (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0,
            "full_rooms": len(self.get_full_rooms()),
            "empty_rooms": len(self.get_empty_rooms()),
            "available_rooms": len(self.get_available_rooms())
        }
