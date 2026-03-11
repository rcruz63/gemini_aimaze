"""
Motor de mapas para gestionar la topología del mundo.
"""

from typing import Dict
from models.room import Room


class MapEngine:
    """
    Gestiona el grafo de habitaciones y sus conexiones.
    Asegura la coherencia espacial bidireccional de las conexiones.
    """
    
    OPPOSITE_DIRECTIONS = {
        "norte": "sur",
        "sur": "norte",
        "este": "oeste",
        "oeste": "este",
        "arriba": "abajo",
        "abajo": "arriba"
    }

    def __init__(self) -> None:
        self.rooms: Dict[str, Room] = {}

    def add_room(self, room: Room) -> None:
        """Añade una habitación al motor de mapas."""
        if room.room_id in self.rooms:
            return
        self.rooms[room.room_id] = room

    def connect(self, room_id_a: str, room_id_b: str, direction: str) -> None:
        """
        Conecta la habitación A con la habitación B en la dirección dada.
        Asegura automáticamente la conexión inversa desde B hacia A.
        """
        if room_id_a not in self.rooms or room_id_b not in self.rooms:
            raise ValueError("Ambas habitaciones deben estar añadidas al MapEngine antes de conectarlas.")

        if direction not in self.OPPOSITE_DIRECTIONS:
            raise ValueError(f"Dirección no válida: {direction}")

        opposite = self.OPPOSITE_DIRECTIONS[direction]

        room_a = self.rooms[room_id_a]
        room_b = self.rooms[room_id_b]

        room_a.exits[direction] = room_id_b
        room_b.exits[opposite] = room_id_a
