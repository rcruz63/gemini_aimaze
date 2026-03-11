"""
Tests for Memory Extractor.
"""

from unittest.mock import MagicMock

import pytest

from ai.memory_extractor import MemoryExtractor
from models.state import SessionState


@pytest.fixture
def mock_llm_client():
    return MagicMock()


def test_extract_updates_success(mock_llm_client):
    # Setup mock to return a memory update
    mock_llm_client.generate_cheap.return_value = {"NPC_Lysa_attitude": "suspicious"}

    extractor = MemoryExtractor(mock_llm_client)
    session = SessionState(location="room_1", memory={})

    updates = extractor.extract_updates(
        "Lysa looked at you with narrowed eyes after your question.", session
    )

    assert updates["NPC_Lysa_attitude"] == "suspicious"
    mock_llm_client.generate_cheap.assert_called_once()


def test_extract_no_updates(mock_llm_client):
    # Setup mock to return empty object
    mock_llm_client.generate_cheap.return_value = {}

    extractor = MemoryExtractor(mock_llm_client)
    session = SessionState(location="room_1", memory={})

    updates = extractor.extract_updates("Nothing happens.", session)

    assert updates == {}


def test_extract_empty_narration(mock_llm_client):
    extractor = MemoryExtractor(mock_llm_client)
    session = SessionState(location="room_1", memory={})

    updates = extractor.extract_updates("", session)

    assert updates == {}
    mock_llm_client.generate_cheap.assert_not_called()
