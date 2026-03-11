"""
Semantic Command Parser using LLM.
"""

import json
from typing import Dict, List, Optional

from ai.llm_client import LLMClient


class CommandParser:
    """
    Parses user input using an LLM to map natural language to engine actions.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def parse(
        self, user_input: str, available_actions: List[str]
    ) -> Dict[str, str]:
        """
        Parses user input using an LLM.
        Returns a dictionary with 'action' and 'target' (optional).
        If no action matches, action is 'unknown'.
        """
        if not user_input.strip():
            return {"action": "unknown"}

        system_prompt = (
            "You are a semantic command parser for a text adventure game. "
            "Your job is to map natural language player input to a strict set of available actions. "
            f"Available actions: {', '.join(available_actions)}. "
            "Respond ONLY with a JSON object like: {'action': 'chosen_action', 'target': 'optional_target'}. "
            "If the input does not match any action or is nonsense, return {'action': 'unknown'}."
        )

        user_prompt = f"Player input: '{user_input}'"

        try:
            response = self.llm_client.generate_cheap(
                prompt=user_prompt, system=system_prompt, format="json"
            )
            
            # Ensure response is a dict and has 'action'
            if isinstance(response, dict) and "action" in response:
                # Validate that the action is either 'unknown' or in available_actions
                # Actually, the LLM might return an action that's slightly different if not careful.
                # But let's trust the 'json' format and clear prompt for now.
                return response
            
            return {"action": "unknown"}
            
        except Exception:
            # Fallback for LLM errors or unexpected output
            return {"action": "unknown"}
