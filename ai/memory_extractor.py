"""
AI-powered Memory Extractor to update session state based on game events.
"""

from typing import Any, Dict

from ai.llm_client import LLMClient
from models.state import MemoryUpdates, SessionState


class MemoryExtractor:
    """
    Analyzes the scene narrative to extract persistent state updates.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def extract_updates(self, narration: str, session: SessionState) -> Dict[str, Any]:
        """
        Analyzes narration and returns validated updates as a dictionary.
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
            raw_updates = self.llm_client.generate_cheap(
                prompt=user_prompt, system=system_prompt, format="json"
            )

            if isinstance(raw_updates, dict):
                # We wrap the dictionary in our validation model
                # Note: MemoryUpdates expects a field 'updates' or we can just return the raw dict if valid.
                # To follow the prompt "Respond ONLY with a JSON object containing the NEW keys",
                # the LLM output is the dictionary itself.
                # Let's adjust MemoryUpdates to handle this or just validate the keys.
                return MemoryUpdates(updates=raw_updates).updates
            return {}

        except Exception:
            return {}
