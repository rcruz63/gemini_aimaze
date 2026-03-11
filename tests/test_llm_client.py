"""
Tests for LLMClient.
"""

from unittest.mock import MagicMock, patch

import pytest

from ai.llm_client import LLMClient


@pytest.fixture
def mock_ollama_client():
    with patch("ai.llm_client.Client") as mock:
        yield mock


def test_generate_cheap_text(mock_ollama_client):
    # Setup mock
    mock_instance = mock_ollama_client.return_value
    mock_instance.chat.return_value = {
        "message": {"content": "Cheap response text"}
    }

    client = LLMClient()
    response = client.generate_cheap("Hello")

    assert response == "Cheap response text"
    mock_instance.chat.assert_called_once()


def test_generate_cheap_json(mock_ollama_client):
    # Setup mock
    mock_instance = mock_ollama_client.return_value
    mock_instance.chat.return_value = {
        "message": {"content": '{"action": "move_north"}'}
    }

    client = LLMClient()
    response = client.generate_cheap("Hello", format="json")

    assert isinstance(response, dict)
    assert response["action"] == "move_north"


def test_generate_expensive(mock_ollama_client):
    # Setup mock
    mock_instance = mock_ollama_client.return_value
    mock_instance.chat.return_value = {
        "message": {"content": "Rich narrative response"}
    }

    client = LLMClient()
    response = client.generate_expensive("Tell me a story")

    assert response == "Rich narrative response"
    # Ensure expensive model was used
    mock_instance.chat.assert_called_once()
    assert mock_instance.chat.call_args[1]["model"] == client.expensive_model
