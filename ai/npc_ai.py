"""
NPC Decision AI using an LLM to simulate autonomous agents.
"""

from ai.llm_client import LLMClient
from models.state import NPCAction, NPCState, SceneState


class NPCDecisionAI:
    """
    Evaluates the state and decides the next action for a specific NPC.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def generate_action(
        self, npc: NPCState, scene: SceneState, last_player_action: str
    ) -> NPCAction:
        """
        Determines the NPC's next move based on their personality and current scene.
        """
        system_prompt = (
            f"Eres el agente de IA controlando a un NPC llamado {npc.name} en un juego de aventuras.\n"
            f"Personalidad: {', '.join(npc.personality)}\n"
            f"Objetivo actual: {npc.goal}\n"
            f"Secreto: {npc.secret if npc.secret else 'Ninguno'}\n"
            f"Actitud hacia el jugador (1 hostil - 5 amigable): {npc.attitude_to_player}\n"
            "REGLAS INNEGOCIABLES:\n"
            "1. NO hables por el jugador ni decidas el resultado de tus acciones.\n"
            "2. Responde EXCLUSIVAMENTE con un JSON que contenga 'action' (qué intentas hacer) e 'intent' (tu motivo oculto).\n"
            "Ejemplo: {'action': 'saca su espada', 'intent': 'intimidar al jugador'}"
        )

        user_prompt = (
            f"Situación en la sala: {scene.location_description}\n"
            f"Acción previa del jugador: {last_player_action}\n"
            f"Otros NPCs presentes: {[n for n in scene.active_npcs if n != npc.name.lower()]}\n"
            "¿Qué haces ahora?"
        )

        try:
            raw_action = self.llm_client.generate_cheap(
                prompt=user_prompt, system=system_prompt, format="json"
            )

            if isinstance(raw_action, dict):
                return NPCAction(**raw_action)
            return NPCAction(
                action="observa en silencio", intent="esperar a ver qué pasa"
            )

        except Exception:
            return NPCAction(action="se queda inmóvil", intent="procesando (glitch)")
