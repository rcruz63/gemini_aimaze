"""
Pruebas del motor de eventos temporales.
"""

from engine.event_engine import EventEngine, Event
from models.state import SceneState


def test_event_progression():
    engine = EventEngine()
    event = Event(
        name="bajada_oxigeno",
        description="El nivel de oxígeno cae a niveles críticos.",
        speed=0.34
    )
    engine.add_event(event)
    
    scene = SceneState(location_description="Estás en la nave.", available_actions=["ir norte"])
    
    # Turno 1 (Progreso 0.34)
    engine.tick(scene)
    assert not event.triggered
    assert "EVENTO" not in scene.location_description
    
    # Turno 2 (Progreso 0.68)
    engine.tick(scene)
    assert not event.triggered
    
    # Turno 3 (Progreso 1.02 -> 1.0, triggered)
    engine.tick(scene)
    assert event.triggered
    assert "El nivel de oxígeno cae" in scene.location_description
