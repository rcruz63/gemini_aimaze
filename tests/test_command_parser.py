"""
Tests for Semantic Command Parser.
"""

from unittest.mock import MagicMock

import pytest

from engine.command_parser import CommandParser


@pytest.fixture
def mock_llm_client():
    return MagicMock()


def test_parse_natural_language_success(mock_llm_client):
    # Setup mock to return a structured action
    mock_llm_client.generate_cheap.return_value = {
        "action": "ir",
        "target": "norte"
    }
    
    parser = CommandParser(mock_llm_client)
    available = ["ir", "mirar", "coger"]
    
    # Input is natural language
    result = parser.parse("quiero abrir la maldita puerta norte", available)
    
    assert result["action"] == "ir"
    assert result["target"] == "norte"
    
    # Verify mock was called with correct context
    mock_llm_client.generate_cheap.assert_called_once()
    call_args = mock_llm_client.generate_cheap.call_args[1]
    assert "ir, mirar, coger" in call_args["system"]


def test_parse_nonsense_to_unknown(mock_llm_client):
    # Setup mock to return unknown
    mock_llm_client.generate_cheap.return_value = {"action": "unknown"}
    
    parser = CommandParser(mock_llm_client)
    available = ["ir", "mirar"]
    
    result = parser.parse("asdfghjkl", available)
    
    assert result["action"] == "unknown"


def test_parse_empty_input(mock_llm_client):
    parser = CommandParser(mock_llm_client)
    result = parser.parse("", ["ir"])
    
    assert result["action"] == "unknown"
    mock_llm_client.generate_cheap.assert_not_called()


def test_parse_llm_error_fallback(mock_llm_client):
    # Setup mock to raise exception
    mock_llm_client.generate_cheap.side_effect = Exception("Ollama down")
    
    parser = CommandParser(mock_llm_client)
    result = parser.parse("ir norte", ["ir"])
    
    assert result["action"] == "unknown"
