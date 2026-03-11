"""
Tests for Director AI.
"""

from unittest.mock import MagicMock

import pytest

from ai.director_ai import DirectorAI
from models.state import SceneState, SessionState


@pytest.fixture
def mock_llm_client():
    return MagicMock()


def test_generate_directives_success(mock_llm_client):
    # Setup mock to return director directives
    mock_llm_client.generate_cheap.return_value = {
        "tension_level": 7,
        "scene_goal": "reveal hidden truth",
        "tone": "intense"
    }
    
    director = DirectorAI(mock_llm_client)
    session = SessionState(location="cavern_entry")
    scene = SceneState(
        location_description="A dark cave entrance.",
        active_npcs=["mysterious_shadow"]
    )
    
    directives = director.generate_directives(session, scene)
    
    assert directives.tension_level == 7
    assert directives.scene_goal == "reveal hidden truth"
    mock_llm_client.generate_cheap.assert_called_once()


def test_generate_directives_fallback_on_error(mock_llm_client):
    # Setup mock to raise exception
    mock_llm_client.generate_cheap.side_effect = Exception("Model not found")
    
    director = DirectorAI(mock_llm_client)
    session = SessionState(location="room_1")
    scene = SceneState(location_description="Empty room.")
    
    directives = director.generate_directives(session, scene)
    
    # Check fallback values
    assert hasattr(directives, "tension_level")
    assert directives.tension_level == 3
