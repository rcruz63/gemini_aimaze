"""
Pruebas unitarias para validar los modelos y su serialización.
"""

import json
from models.room import Room
from models.state import WorldState, SessionState, SceneState


def test_room_serialization():
    """Valida la creación y serialización de una Room a JSON."""
    room = Room(
        room_id="sala_1", description="Una sala oscura", exits={"norte": "sala_2"}
    )
    json_data = room.model_dump_json()
    data = json.loads(json_data)

    assert data["room_id"] == "sala_1"
    assert data["description"] == "Una sala oscura"
    assert data["exits"]["norte"] == "sala_2"
    assert "items" in data


def test_world_state_serialization():
    """Valida la creación y serialización del WorldState."""
    state = WorldState(setting="Castillo", theme="Fantasía")
    data = json.loads(state.model_dump_json())
    assert data["setting"] == "Castillo"
    assert data["theme"] == "Fantasía"


def test_session_state_serialization():
    """Valida la creación y serialización del SessionState."""
    state = SessionState(
        location="sala_1", inventory=["llave"], npcs_conocidos=["guardia"]
    )
    data = json.loads(state.model_dump_json())
    assert data["location"] == "sala_1"
    assert "llave" in data["inventory"]
    assert "guardia" in data["npcs_conocidos"]


def test_scene_state_serialization():
    """Valida la creación y serialización del SceneState."""
    state = SceneState(
        location_description="Estás en un pasillo iluminado",
        active_npcs=["guardia"],
        available_actions=["ir norte", "atacar guardia"],
    )
    data = json.loads(state.model_dump_json())
    assert "pasillo iluminado" in data["location_description"]
    assert "guardia" in data["active_npcs"]
    assert len(data["available_actions"]) == 2
