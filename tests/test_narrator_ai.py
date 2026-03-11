"""
Tests for Narrator AI.
"""

from unittest.mock import MagicMock

import pytest

from ai.narrator_ai import NarratorAI
from models.state import SceneState


@pytest.fixture
def mock_llm_client():
    return MagicMock()


def test_generate_scene_success(mock_llm_client):
    # Setup mock to return narrative
    mock_llm_client.generate_expensive.return_value = "A long, retro-adventure narrative."
    
    narrator = NarratorAI(mock_llm_client)
    scene = SceneState(
        location_description="A pixelated forest.",
        director_directives={"tension": 5}
    )
    
    narrative = narrator.generate_scene(scene, "moved north")
    
    assert narrative == "A long, retro-adventure narrative."
    mock_llm_client.generate_expensive.assert_called_once()


def test_generate_scene_error_fallback(mock_llm_client):
    # Setup mock to raise exception
    mock_llm_client.generate_expensive.side_effect = Exception("Narrative error")
    
    narrator = NarratorAI(mock_llm_client)
    scene = SceneState(location_description="Empty void.")
    
    narrative = narrator.generate_scene(scene)
    
    assert "glitched" in narrative
    assert "Empty void." in narrative
