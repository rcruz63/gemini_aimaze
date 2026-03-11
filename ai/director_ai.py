"""
Narrative Director AI to manage pacing, tension, and scene goals.
"""

from typing import Any, Dict

from ai.llm_client import LLMClient
from models.state import SceneState, SessionState


class DirectorAI:
    """
    Orchestrates narrative tone and tension based on game state.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def generate_directives(
        self, session: SessionState, scene: SceneState
    ) -> Dict[str, Any]:
        """
        Evaluates state and returns narrative directives (tension, goals).
        """
        system_prompt = (
            "You are the Narrative Director of a text adventure game. "
            "Your job is to set the tone, tension level (1-10), and narrative goals for the next scene. "
            "You do NOT change the map or inventory, only provide guidance to the narrator. "
            "Respond ONLY with a JSON object like: {'tension_level': 5, 'scene_goal': 'build suspense', 'tone': 'mysterious'}. "
        )

        user_prompt = (
            f"Current Location: {session.location}\n"
            f"Memory: {session.memory}\n"
            f"Active NPCs: {scene.active_npcs}\n"
            f"Scene Context: {scene.location_description}"
        )

        try:
            directives = self.llm_client.generate_cheap(
                prompt=user_prompt, system=system_prompt, format="json"
            )

            if isinstance(directives, dict):
                return directives
            return {"tension_level": 3, "scene_goal": "continue adventure", "tone": "neutral"}

        except Exception:
            return {"tension_level": 3, "scene_goal": "continue adventure", "tone": "neutral"}
