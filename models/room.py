"""
Modelos para la representación de las habitaciones del juego.
"""

from typing import Dict, List
from pydantic import BaseModel, Field


class Room(BaseModel):
    """
    Representa una habitación o ubicación en el mapa.
    
    Attributes:
        room_id: Identificador único de la habitación.
        description: Descripción estática básica de la habitación.
        exits: Diccionario con direcciones (norte, sur, etc.) apuntando a otros room_ids.
        items: Lista de items presentes en la habitación.
    """
    room_id: str
    description: str = ""
    exits: Dict[str, str] = Field(default_factory=dict)
    items: List[str] = Field(default_factory=list)
