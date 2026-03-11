"""
Modelos de estado estructurado del juego: World, Session y Scene.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class WorldState(BaseModel):
    """
    Estado estático del mundo.
    Define la ambientación, el tema principal, etc.
    """

    setting: str
    theme: str


class MemoryUpdates(BaseModel):
    """
    Structured updates for session memory.
    """

    updates: Dict[str, Any] = Field(default_factory=dict)


class NPCState(BaseModel):
    """
    Estado y "mente" de un NPC.
    """

    name: str
    personality: List[str]
    goal: str
    secret: Optional[str] = None
    attitude_to_player: int = Field(ge=1, le=5, default=3)
    current_plan: str = ""


class NPCAction(BaseModel):
    """
    Acción estructurada decidida por un NPC.
    """

    action: str
    intent: str


class SessionState(BaseModel):
    """
    Estado dinámico de cambios lentos.
    Almacena información persistente a lo largo de la sesión,
    como la ubicación actual, inventario y npcs conocidos.
    """

    location: str
    inventory: List[str] = Field(default_factory=list)
    npcs_conocidos: List[str] = Field(default_factory=list)
    npcs: Dict[str, NPCState] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)


class DirectorDirectives(BaseModel):
    """
    Structured directives from the Narrative Director.
    """

    tension_level: int = Field(ge=1, le=10, default=3)
    scene_goal: str = Field(default="continue adventure")
    tone: str = Field(default="neutral")


class SceneState(BaseModel):
    """
    Estado dinámico de cambios rápidos.
    Almacena la información de la escena actual para alimentar al narrador o LLM.
    """

    location_description: str
    active_npcs: List[str] = Field(default_factory=list)
    available_actions: List[str] = Field(default_factory=list)
    director_directives: DirectorDirectives = Field(default_factory=DirectorDirectives)
    npc_actions: Dict[str, str] = Field(default_factory=dict)
    triggered_events: List[str] = Field(default_factory=list)
