"""
Parser básico de comandos deterministas.
"""

from typing import Dict, Optional


class CommandParser:
    """
    Analiza la entrada del usuario y la convierte en acciones estructuradas (verbo-sustantivo).
    """

    def parse(self, command: str) -> Optional[Dict[str, str]]:
        """
        Parsea un comando de texto a un diccionario con 'action' y 'target'.
        Si no se puede parsear, devuelve None.
        """
        words = command.strip().lower().split()
        if not words:
            return None
        
        action = words[0]
        target = words[1] if len(words) > 1 else ""

        # Mapeos simples de sinónimos
        if action in ["ir", "moverse", "caminar", "go"]:
            action = "ir"
        elif action in ["coger", "tomar", "agarrar", "take", "recoger"]:
            action = "coger"
        elif action in ["mirar", "observar", "examinar", "look"]:
            action = "mirar"
            
        return {"action": action, "target": target}
