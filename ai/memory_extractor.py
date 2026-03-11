"""
AI-powered Memory Extractor to update session state based on game events.
"""

from typing import Any, Dict, Optional

from ai.llm_client import LLMClient
from models.state import SessionState


class MemoryExtractor:
    """
    Analyzes the scene narrative to extract persistent state updates.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def extract_updates(
        self, narration: str, session: SessionState
    ) -> Dict[str, Any]:
        """
        Analyzes narration and current session to return a dictionary of updates.
        """
        if not narration.strip():
            return {}

        system_prompt = (
            "You are a state memory extractor for a text adventure game. "
            "Your job is to read the latest scene narration and identify key updates for the session memory. "
            "Memory can include NPC attitudes, important discoveries, or changed world facts. "
            "Current Session Memory: " + str(session.memory) + "\n"
            "Respond ONLY with a JSON object containing the NEW or UPDATED keys. "
            "Example: {'NPC_Lysa_attitude': 'suspicious', 'discovered_secret_passage': True}. "
            "If nothing significant changed, return an empty object {}."
        )

        user_prompt = f"Latest Narration: '{narration}'"

        try:
            updates = self.llm_client.generate_cheap(
                prompt=user_prompt, system=system_prompt, format="json"
            )

            if isinstance(updates, dict):
                return updates
            return {}

        except Exception:
            return {}
