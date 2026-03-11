"""
Client for interacting with local LLMs via Ollama.
"""

import json
from typing import Any, Dict, Optional, Union

from ollama import Client


class LLMClient:
    """
    Agnostic client for local LLM interactions.
    Handles cheap/fast models for logic and expensive/rich models for narrative.
    """

    def __init__(
        self,
        cheap_model: str = "llama3.2:3b",
        expensive_model: str = "qwen2.5:7b",
        host: str = "http://localhost:11434",
    ):
        self.client = Client(host=host)
        self.cheap_model = cheap_model
        self.expensive_model = expensive_model

    def generate_cheap(
        self,
        prompt: str,
        system: Optional[str] = None,
        format: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Union[str, Dict[str, Any]]:
        """
        Generates a response using the cheap model, ideal for structured logic.
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat(
            model=self.cheap_model,
            messages=messages,
            format=format,
            options=options,
        )

        content = response["message"]["content"]

        if format == "json":
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback if model fails to provide valid JSON despite format='json'
                return {"error": "invalid_json", "raw": content}

        return content

    def generate_expensive(
        self,
        prompt: str,
        system: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generates a response using the expensive model, ideal for rich narrative.
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat(
            model=self.expensive_model,
            messages=messages,
            options=options,
        )

        return response["message"]["content"]
