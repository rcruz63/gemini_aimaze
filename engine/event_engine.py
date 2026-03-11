"""
Motor de eventos para simular un mundo vivo.
"""

from pydantic import BaseModel
from typing import List
from models.state import SceneState


class Event(BaseModel):
    """
    Representa un evento que progresa con el tiempo.
    """
    name: str
    description: str
    progress: float = 0.0
    speed: float
    triggered: bool = False


class EventEngine:
    """Gestiona el reloj interno del juego y la evolución de los eventos."""
    
    def __init__(self) -> None:
        self.events: List[Event] = []
        
    def add_event(self, event: Event) -> None:
        self.events.append(event)
        
    def tick(self, scene_state: SceneState) -> None:
        """
        Avanza un turno simulado en el mundo.
        Incrementa el progreso de los eventos y, si alcanzan 1.0, se disparan.
        """
        for event in self.events:
            if event.triggered:
                continue
                
            event.progress += event.speed
            
            if event.progress >= 1.0:
                event.progress = 1.0
                event.triggered = True
                
                # Inyectar el evento en la descripción de la escena o notificarlo
                scene_state.location_description += f"\n[EVENTO]: {event.description}"
