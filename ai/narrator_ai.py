"""
Narrador AI Mock para la validación visual de la consola (Spike 1).
"""

from models.state import SceneState


class NarratorMock:
    """Simula las respuestas de la IA sin consumir tokens."""
    
    def generate_scene(self, scene_state: SceneState) -> str:
        """
        Recibe el SceneState estructurado y devuelve un string narrativo hardcodeado.
        """
        desc = scene_state.location_description
        
        narrative = f"{desc}\n"
        if scene_state.available_actions:
            narrative += "\nOpciones de movimiento: " + ", ".join(scene_state.available_actions)
        
        return narrative
