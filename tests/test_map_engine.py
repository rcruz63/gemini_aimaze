"""
Pruebas para el motor de mapas.
"""

import pytest
from engine.map_engine import MapEngine
from models.room import Room


def test_brujula_rota():
    """
    Valida matemáticamente la coherencia espacial.
    Si se conecta A hacia B al norte, B debe tener salida hacia A al sur.
    """
    engine = MapEngine()
    room_a = Room(room_id="sala_A", description="Sala inicial")
    room_b = Room(room_id="sala_B", description="Sala destino")

    engine.add_room(room_a)
    engine.add_room(room_b)

    # Conectar A -> B al norte
    engine.connect("sala_A", "sala_B", "norte")

    # Comprobar la ida
    assert engine.rooms["sala_A"].exits["norte"] == "sala_B"

    # Comprobar obligatoriamente la vuelta (Test de la brújula rota)
    assert engine.rooms["sala_B"].exits["sur"] == "sala_A"


def test_connect_invalid_direction():
    """Valida que una dirección inválida lanza un error."""
    engine = MapEngine()
    engine.add_room(Room(room_id="A"))
    engine.add_room(Room(room_id="B"))

    with pytest.raises(ValueError):
        engine.connect("A", "B", "noroeste")
