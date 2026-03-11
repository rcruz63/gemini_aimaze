"""
Narrative AI to generate immersive descriptions based on game state and director directives.
"""

from ai.llm_client import LLMClient
from models.state import SceneState


class NarratorAI:
    """
    Generates rich narrative text using a powerful LLM.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def generate_scene(self, scene_state: SceneState, last_action_result: str = "") -> str:
        """
        Generates narrative based on scene state and the last engine action.
        """
        system_prompt = (
            "You are the Narrator of an 8-bit text adventure game. "
            "TONE: Retro-adventure, humorous, slightly sarcastic, and immersive. "
            "STYLE: Describe the scene vividly but keep it punchy. "
            "LENGTH: Strictly between 80 and 150 words. "
            "REGLA 1: NO inventes salidas, puertas, caminos u objetos que no estén explícitamente en el JSON del SceneState. "
            "REGLA 2: NUNCA digas que un camino está bloqueado o cubierto a menos que el JSON lo indique. "
            "REGLA 3: Limítate a describir con tono oscuro y algo de humor lo que dice el estado, sin tomar decisiones. "
            "Your output is ONLY the narrative text. Do not add metadata or AI chatter."
        )

        user_prompt = (
            f"Director Directives: {scene_state.director_directives}\n"
            f"Location: {scene_state.location_description}\n"
            f"Active NPCs: {scene_state.active_npcs}\n"
            f"Available Actions: {scene_state.available_actions}\n"
            f"Result of last action: {last_action_result}"
        )

        try:
            narrative = self.llm_client.generate_expensive(
                prompt=user_prompt, system=system_prompt
            )
            return narrative
        except Exception as e:
            return f"The narration glitched (AI Error): {str(e)}\n{scene_state.location_description}"
