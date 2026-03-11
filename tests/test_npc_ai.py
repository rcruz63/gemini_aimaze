"""
Tests for NPC Decision AI.
"""

from unittest.mock import MagicMock

import pytest

from ai.npc_ai import NPCDecisionAI
from models.state import NPCState, SceneState


@pytest.fixture
def mock_llm_client():
    return MagicMock()


def test_generate_action_success(mock_llm_client):
    # Setup mock
    mock_llm_client.generate_cheap.return_value = {
        "action": "se esconde en las sombras",
        "intent": "evitar ser visto",
    }

    npc_ai = NPCDecisionAI(mock_llm_client)

    npc = NPCState(
        name="Sombra",
        personality=["sigiloso", "tímido"],
        goal="sobrevivir",
        attitude_to_player=1,
    )

    scene = SceneState(location_description="Una cueva oscura.", active_npcs=["sombra"])

    action = npc_ai.generate_action(npc, scene, "El jugador enciende una antorcha.")

    assert action.action == "se esconde en las sombras"
    assert action.intent == "evitar ser visto"
    mock_llm_client.generate_cheap.assert_called_once()


def test_generate_action_fallback(mock_llm_client):
    # Setup mock to raise exception
    mock_llm_client.generate_cheap.side_effect = Exception("Error de red")

    npc_ai = NPCDecisionAI(mock_llm_client)

    npc = NPCState(name="Test", personality=["Test"], goal="Test")
    scene = SceneState(location_description="Test")

    action = npc_ai.generate_action(npc, scene, "Nada.")

    assert action.action == "se queda inmóvil"
    assert "glitch" in action.intent
